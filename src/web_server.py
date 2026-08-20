"""Local web workspace for launching and viewing one-symbol stock reports.

The existing CLI remains the source of truth for analysis.  This module only
queues a validated symbol, streams the CLI output into an in-memory job record,
and serves the generated report directory.  It deliberately does not expose a
generic shell-command API.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import queue
import re
import subprocess
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from src.ai.ollama_report import answer_report_question
from src.config import PROJECT_ROOT
from src.reports.dashboard import CHAT_WIDGET_CSS, CHAT_WIDGET_MARKUP, CHAT_WIDGET_SCRIPT


SYMBOL_PATTERN = re.compile(r"^[A-Z]{3}$")
REPORT_PATH_PATTERN = re.compile(r"Báo cáo xem nhanh:\s*(.+)$")
ACTIVE_STATUSES = {"queued", "running"}
MAX_LOG_LINES = 220
MAX_CHAT_PAYLOAD_BYTES = 32_000


def normalize_symbol(value: object) -> str:
    """Validate the only user input passed to the report CLI."""

    symbol = str(value or "").strip().upper()
    if not SYMBOL_PATTERN.fullmatch(symbol):
        raise ValueError("Mã cổ phiếu phải gồm đúng 3 chữ cái, ví dụ VCB hoặc FPT.")
    return symbol


def timestamp() -> str:
    return datetime.now(UTC).isoformat()


def dashboard_file(report_directory: Path) -> Path | None:
    compact = report_directory / "dashboard_report" / "dashboard.html"
    if compact.is_file():
        return compact
    direct = report_directory / "dashboard.html"
    return direct if direct.is_file() else None


def report_url(project_root: Path, report_directory: Path) -> str | None:
    dashboard = dashboard_file(report_directory)
    if dashboard is None:
        return None
    try:
        relative = dashboard.resolve().relative_to((project_root / "reports").resolve())
    except ValueError:
        return None
    return "/reports/" + relative.as_posix()


def chat_report_directory(project_root: Path, report_path: object) -> Path:
    """Resolve only a dashboard belonging to the local reports directory."""

    raw = str(report_path or "").strip()
    if not raw:
        raise ValueError("Thiếu report đang mở để trả lời câu hỏi.")
    relative = Path(unquote(raw.removeprefix("/reports/")))
    root = (project_root / "reports").resolve()
    candidate = (root / relative).resolve()
    if root not in candidate.parents or candidate.name != "dashboard.html" or not candidate.is_file():
        raise ValueError("Report chat không hợp lệ hoặc không tồn tại.")

    report_root = candidate.parent.parent if candidate.parent.name == "dashboard_report" else candidate.parent
    artifact_directory = report_root / "all_files"
    if not (artifact_directory / "signal_decision.json").is_file():
        artifact_directory = report_root
    if not (artifact_directory / "signal_decision.json").is_file():
        raise ValueError("Report này chưa có artifact đủ để trả lời bằng AI.")
    return artifact_directory


def inject_report_chat_widget(document: str) -> str:
    """Add the assistant to reports generated before the widget existed."""

    if 'id="report-chat-launcher"' in document:
        return document
    if "</style>" not in document or "</body>" not in document:
        return document
    document = document.replace("</style>", CHAT_WIDGET_CSS + "\n</style>", 1)
    return document.replace(
        "</body>",
        CHAT_WIDGET_MARKUP + CHAT_WIDGET_SCRIPT + "\n</body>",
        1,
    )


@dataclass
class AnalysisJob:
    id: str
    symbol: str
    created_at: str
    status: str = "queued"
    phase: str = "Đang chờ worker"
    started_at: str | None = None
    finished_at: str | None = None
    return_code: int | None = None
    report_directory: str | None = None
    error: str | None = None
    logs: list[str] = field(default_factory=list)


class AnalysisJobManager:
    """Single-worker queue so local resource-heavy analyses never overlap."""

    def __init__(self, project_root: Path, python_executable: Path) -> None:
        self.project_root = project_root.resolve()
        # Do not call ``resolve()`` here.  In a venv, ``bin/python`` is a
        # symlink to the base interpreter; resolving it bypasses the venv and
        # makes project dependencies such as ``typer`` unavailable.
        self.python_executable = python_executable.absolute()
        self._jobs: dict[str, AnalysisJob] = {}
        self._queue: queue.Queue[str] = queue.Queue()
        self._lock = threading.Lock()
        self._worker = threading.Thread(target=self._work_forever, daemon=True)
        self._worker.start()

    def submit(self, symbol: object) -> AnalysisJob:
        normalized = normalize_symbol(symbol)
        with self._lock:
            existing = next(
                (
                    job
                    for job in self._jobs.values()
                    if job.symbol == normalized and job.status in ACTIVE_STATUSES
                ),
                None,
            )
            if existing is not None:
                return existing
            job = AnalysisJob(
                id=uuid.uuid4().hex[:12],
                symbol=normalized,
                created_at=timestamp(),
            )
            self._jobs[job.id] = job
            self._queue.put(job.id)
            return job

    def get(self, job_id: str) -> AnalysisJob | None:
        with self._lock:
            return self._jobs.get(job_id)

    def snapshot(self, job: AnalysisJob) -> dict[str, Any]:
        with self._lock:
            payload = asdict(job)
        report_directory = Path(job.report_directory) if job.report_directory else None
        payload["dashboard_url"] = (
            report_url(self.project_root, report_directory)
            if report_directory is not None
            else None
        )
        return payload

    def _append_log(self, job: AnalysisJob, line: str) -> None:
        clean = line.rstrip()
        if not clean:
            return
        with self._lock:
            job.logs.append(clean)
            if len(job.logs) > MAX_LOG_LINES:
                del job.logs[:-MAX_LOG_LINES]
            if "[1/4]" in clean:
                job.phase = "Đang tạo ML report và backtest"
            elif "[2/4]" in clean:
                job.phase = "Đang lấy headline và đọc tin có nguồn"
            elif "[3/4]" in clean:
                job.phase = "Đang cập nhật news model (shadow)"
            elif "[4/4]" in clean:
                job.phase = "Đang tạo tóm tắt AI grounded"
            elif "Ollama AI chưa hoàn tất" in clean:
                job.phase = "AI fallback từ artifact local"

    def _work_forever(self) -> None:
        while True:
            job_id = self._queue.get()
            try:
                job = self.get(job_id)
                if job is not None:
                    self._run(job)
            finally:
                self._queue.task_done()

    def _run(self, job: AnalysisJob) -> None:
        command = [
            str(self.python_executable),
            "-m",
            "src.finai_cli",
            "full",
            job.symbol,
            "--no-postgres",
        ]
        with self._lock:
            job.status = "running"
            job.phase = "Đang tạo ML report và backtest"
            job.started_at = timestamp()

        try:
            process = subprocess.Popen(
                command,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                self._append_log(job, line)
            return_code = process.wait()
        except OSError as exc:
            with self._lock:
                job.status = "failed"
                job.phase = "Không thể khởi chạy pipeline"
                job.error = str(exc)
                job.finished_at = timestamp()
            return

        report_directory = self._report_directory_from_logs(job)
        with self._lock:
            job.return_code = return_code
            job.finished_at = timestamp()
            if return_code == 0 and report_directory is not None:
                job.status = "completed"
                job.phase = "Đã hoàn tất — mở dashboard"
                job.report_directory = str(report_directory)
            else:
                job.status = "failed"
                job.phase = "Pipeline không hoàn tất"
                job.error = (
                    "Không tìm thấy dashboard đầu ra."
                    if return_code == 0
                    else f"Pipeline dừng với mã lỗi {return_code}."
                )

    def _report_directory_from_logs(self, job: AnalysisJob) -> Path | None:
        for line in reversed(job.logs):
            match = REPORT_PATH_PATTERN.search(line)
            if not match:
                continue
            candidate = Path(match.group(1).strip()).expanduser()
            if not candidate.is_absolute():
                candidate = self.project_root / candidate
            candidate = candidate.resolve()
            if dashboard_file(candidate) is not None:
                return candidate

        symbol_root = self.project_root / "reports" / job.symbol
        candidates = sorted(
            path for path in symbol_root.glob("*") if path.is_dir() and dashboard_file(path)
        )
        return candidates[-1] if candidates else None


def list_reports(project_root: Path, symbol: object) -> list[dict[str, str]]:
    normalized = normalize_symbol(symbol)
    root = project_root / "reports" / normalized
    if not root.is_dir():
        return []
    rows = []
    for path in sorted((item for item in root.iterdir() if item.is_dir()), reverse=True):
        url = report_url(project_root, path)
        if url:
            rows.append({"symbol": normalized, "run_id": path.name, "dashboard_url": url})
    return rows[:20]


INDEX_HTML = r"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>VN Stock Analysis Workspace</title>
  <style>
    :root{--bg:#080d17;--panel:#111927;--panel2:#0d1522;--line:#26364c;--text:#edf3fb;--muted:#91a0b6;--blue:#4d96ff;--green:#22d3a5;--amber:#f4bf4f;--red:#fb7185}
    *{box-sizing:border-box} body{margin:0;background:radial-gradient(circle at 78% -5%,#172f52 0,transparent 33%),var(--bg);font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--text)}
    .shell{max-width:1440px;margin:auto;padding:36px clamp(18px,4vw,56px) 52px}.eyebrow{color:#8dd9d0;font-weight:800;font-size:11px;letter-spacing:.11em;text-transform:uppercase}h1{font-size:clamp(30px,4vw,48px);margin:10px 0 8px;letter-spacing:-.04em}.lead{max-width:760px;margin:0;color:var(--muted);line-height:1.55}
    .top{display:grid;grid-template-columns:minmax(0,1fr) minmax(320px,.65fr);gap:28px;align-items:center}.launch{padding:20px;border:1px solid var(--line);background:rgba(17,25,39,.9);border-radius:16px;box-shadow:0 22px 60px rgba(0,0,0,.28)}label{display:block;margin-bottom:9px;font-size:12px;font-weight:800;color:#cbd8ea;text-transform:uppercase;letter-spacing:.06em}.form-row{display:flex;gap:10px}.form-row input{min-width:0;flex:1;border:1px solid #41658e;background:#0b1422;color:#fff;border-radius:10px;padding:13px 14px;font:700 18px ui-monospace,SFMono-Regular,monospace;text-transform:uppercase}.form-row input:focus{outline:3px solid rgba(77,150,255,.25);border-color:var(--blue)}button{border:0;border-radius:10px;padding:13px 16px;background:linear-gradient(135deg,#2563eb,#2f8cff);color:#fff;font:800 14px Inter,system-ui;cursor:pointer}button:disabled{opacity:.55;cursor:wait}.hint{margin:10px 0 0;color:var(--muted);font-size:12px;line-height:1.45}
    .notice{display:flex;gap:12px;margin:30px 0 22px;padding:15px 17px;border:1px solid #725817;border-radius:13px;background:#2a2415;color:#f7dc91;line-height:1.5}.notice strong{color:#ffe88c}.workspace{display:grid;grid-template-columns:minmax(310px,.45fr) minmax(0,1.55fr);gap:22px}.card{border:1px solid var(--line);background:var(--panel);border-radius:15px;padding:18px;box-shadow:0 18px 50px rgba(0,0,0,.18)}.card h2{font-size:16px;margin:0 0 14px}.state{display:flex;align-items:center;gap:10px}.dot{width:10px;height:10px;border-radius:50%;background:var(--muted);box-shadow:0 0 0 5px rgba(145,160,182,.12)}.dot.queued{background:var(--amber)}.dot.running{background:var(--blue)}.dot.completed{background:var(--green)}.dot.failed{background:var(--red)}.state strong{font-size:15px}.state small{color:var(--muted)}.phase{margin:16px 0 10px;padding:12px;border-radius:10px;background:var(--panel2);color:#d6e4f6;line-height:1.45}.progress{height:5px;overflow:hidden;background:#28364a;border-radius:10px}.progress i{display:block;width:35%;height:100%;background:linear-gradient(90deg,#2563eb,#2dd4bf);border-radius:10px;animation:load 1.3s ease-in-out infinite}@keyframes load{50%{transform:translateX(170%)}}.logs{max-height:285px;overflow:auto;margin:14px 0 0;padding:12px;border:1px solid #223148;background:#09111d;border-radius:10px;color:#b7c6d9;font:12px/1.5 ui-monospace,SFMono-Regular,monospace;white-space:pre-wrap}.reports{display:grid;gap:8px}.report-link{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:11px 12px;border-radius:9px;border:1px solid #263a53;background:#0d1624;color:#ddecff;text-decoration:none;font:700 13px ui-monospace,SFMono-Regular,monospace}.report-link:hover{border-color:#4d96ff;color:#9bc7ff}.report-link span{color:var(--muted);font-family:Inter,system-ui;font-size:11px}.empty{color:var(--muted);font-size:13px}.viewer-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}.viewer-head a{color:#8bbcff;font-size:13px;font-weight:750}.frame{width:100%;height:850px;border:1px solid #2a3c55;border-radius:11px;background:#0a111c}.placeholder{height:850px;display:grid;place-items:center;text-align:center;color:var(--muted);padding:30px;border:1px dashed #2a3c55;border-radius:11px;background:#0b1420}.placeholder strong{display:block;color:#dce8f7;margin-bottom:8px}
    @media(max-width:980px){.top,.workspace{grid-template-columns:1fr}.frame,.placeholder{height:720px}}@media(max-width:540px){.shell{padding:24px 16px}.form-row{flex-direction:column}.form-row button{width:100%}.frame,.placeholder{height:620px}}
  </style>
</head>
<body>
  <main class="shell">
    <div class="top"><div><div class="eyebrow">Local research workspace</div><h1>Nhập mã, chạy pipeline, xem report.</h1><p class="lead">Server gọi pipeline có sẵn của project: giá, ML/backtest, headline, News Reader và AI grounded. Mỗi lần chạy tạo một report có timestamp để đối chiếu lại.</p></div>
      <form class="launch" id="analysis-form"><label for="symbol">Mã cổ phiếu</label><div class="form-row"><input id="symbol" name="symbol" value="VCB" maxlength="3" autocomplete="off" aria-label="Mã cổ phiếu"><button id="submit" type="submit">Phân tích mã</button></div><p class="hint">Ví dụ: VCB, FPT, HPG. Server chạy tuần tự để không chồng chéo train/AI trên máy local.</p></form></div>
    <div class="notice"><div>⚠</div><div><strong>Phân tích nghiên cứu, không phải lệnh giao dịch.</strong><br>AI chỉ tóm tắt artifact và tin có nguồn; trạng thái <code>NO_EDGE</code> vẫn chặn vị thế.</div></div>
    <section class="workspace"><aside class="card"><h2>Trạng thái phân tích</h2><div id="job-state" class="empty">Chưa có job. Nhập mã để bắt đầu.</div><div id="reports" class="reports" style="margin-top:18px"></div></aside><section class="card"><div class="viewer-head"><h2>Dashboard report</h2><a id="open-report" hidden target="_blank" rel="noopener">Mở dashboard riêng ↗</a></div><iframe id="viewer" class="frame" title="Dashboard report" hidden></iframe><div id="placeholder" class="placeholder"><div><strong>Chưa có report để hiển thị</strong>Nhập mã ở phía trên. Khi job hoàn tất, dashboard sẽ tự xuất hiện tại đây.</div></div></section></section>
  </main>
  <script>
    const form=document.querySelector('#analysis-form'), input=document.querySelector('#symbol'), submit=document.querySelector('#submit'), state=document.querySelector('#job-state'), reports=document.querySelector('#reports'), viewer=document.querySelector('#viewer'), placeholder=document.querySelector('#placeholder'), openReport=document.querySelector('#open-report');
    let activeJob=null, timer=null;
    const esc=(value)=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    function renderReports(items){reports.innerHTML=items.length?'<h2 style="margin-top:10px">Report gần đây</h2>'+items.map(item=>`<a class="report-link" href="${esc(item.dashboard_url)}" data-dashboard="${esc(item.dashboard_url)}"><b>${esc(item.symbol)} · ${esc(item.run_id)}</b><span>Mở</span></a>`).join(''):'<p class="empty">Chưa có report đã hoàn tất cho mã này.</p>';reports.querySelectorAll('[data-dashboard]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();showReport(link.dataset.dashboard)}));}
    async function refreshReports(symbol){const response=await fetch('/api/reports?symbol='+encodeURIComponent(symbol));if(response.ok)renderReports(await response.json());}
    function showReport(url){viewer.src=url;viewer.hidden=false;placeholder.hidden=true;openReport.href=url;openReport.hidden=false;}
    function renderJob(job){const logs=(job.logs||[]).slice(-12).join('\n')||'Đang chờ log từ pipeline…';state.innerHTML=`<div class="state"><i class="dot ${esc(job.status)}"></i><div><strong>${esc(job.symbol)} · ${esc(job.status)}</strong><br><small>${esc(job.created_at)}</small></div></div><div class="phase">${esc(job.phase)}</div>${job.status==='running'||job.status==='queued'?'<div class="progress"><i></i></div>':''}${job.error?`<p style="color:#fb7185">${esc(job.error)}</p>`:''}<pre class="logs">${esc(logs)}</pre>`;submit.disabled=job.status==='queued'||job.status==='running';}
    async function poll(){if(!activeJob)return;const response=await fetch('/api/jobs/'+activeJob);if(!response.ok)return;const job=await response.json();renderJob(job);if(job.status==='completed'){showReport(job.dashboard_url);await refreshReports(job.symbol);activeJob=null;timer=null;submit.disabled=false;return;}if(job.status==='failed'){activeJob=null;timer=null;submit.disabled=false;return;}timer=setTimeout(poll,1400);}
    form.addEventListener('submit',async event=>{event.preventDefault();const symbol=input.value.trim().toUpperCase();input.value=symbol;submit.disabled=true;try{const response=await fetch('/api/analyses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({symbol})});const payload=await response.json();if(!response.ok)throw new Error(payload.error||'Không thể tạo job.');activeJob=payload.id;renderJob(payload);if(timer)clearTimeout(timer);poll();}catch(error){state.innerHTML='<p style="color:#fb7185">'+esc(error.message)+'</p>';submit.disabled=false;}});
    input.addEventListener('input',()=>input.value=input.value.toUpperCase().replace(/[^A-Z]/g,''));
    input.addEventListener('change',()=>refreshReports(input.value.trim().toUpperCase()).catch(()=>{}));
    refreshReports(input.value).catch(()=>{});
  </script>
</body>
</html>"""


class WorkspaceHandler(BaseHTTPRequestHandler):
    server: "WorkspaceServer"

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_bytes(INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if parsed.path.startswith("/api/jobs/"):
            job = self.server.manager.get(parsed.path.rsplit("/", 1)[-1])
            if job is None:
                self._send_json({"error": "Không tìm thấy job."}, HTTPStatus.NOT_FOUND)
                return
            self._send_json(self.server.manager.snapshot(job))
            return
        if parsed.path == "/api/reports":
            query = parse_qs(parsed.query)
            try:
                self._send_json(list_reports(self.server.project_root, query.get("symbol", [""])[0]))
            except ValueError as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        if parsed.path.startswith("/reports/"):
            self._serve_report(parsed.path)
            return
        self._send_json({"error": "Không tìm thấy đường dẫn."}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/chat":
            self._handle_chat()
            return
        if path != "/api/analyses":
            self._send_json({"error": "Không tìm thấy endpoint."}, HTTPStatus.NOT_FOUND)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 4096:
                raise ValueError("Payload không hợp lệ.")
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            job = self.server.manager.submit(payload.get("symbol"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        self._send_json(self.server.manager.snapshot(job), HTTPStatus.ACCEPTED)

    def _handle_chat(self) -> None:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > MAX_CHAT_PAYLOAD_BYTES:
                raise ValueError("Payload chat không hợp lệ.")
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Payload chat phải là JSON object.")
            history = payload.get("history", [])
            if not isinstance(history, list):
                raise ValueError("Lịch sử chat không hợp lệ.")
            report_directory = chat_report_directory(self.server.project_root, payload.get("report"))
            answer = answer_report_question(
                report_directory,
                str(payload.get("message") or ""),
                history=history[-8:],
                model=os.environ.get("FINAI_CHAT_MODEL", "qwen3:8b"),
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        self._send_json(answer)

    def _serve_report(self, raw_path: str) -> None:
        relative = Path(unquote(raw_path.removeprefix("/reports/")))
        root = (self.server.project_root / "reports").resolve()
        candidate = (root / relative).resolve()
        if root not in candidate.parents or not candidate.is_file():
            self._send_json({"error": "Không tìm thấy artifact report."}, HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
        if content_type.startswith("text/") or candidate.suffix in {".json", ".md", ".csv"}:
            content_type += "; charset=utf-8"
        body = candidate.read_bytes()
        if candidate.name == "dashboard.html":
            try:
                body = inject_report_chat_widget(body.decode("utf-8")).encode("utf-8")
            except UnicodeDecodeError:
                pass
        self._send_bytes(body, content_type)

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._send_bytes(
            json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            "application/json; charset=utf-8",
            status,
        )

    def _send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


class WorkspaceServer(ThreadingHTTPServer):
    manager: AnalysisJobManager
    project_root: Path


def serve(host: str = "127.0.0.1", port: int = 8787) -> None:
    python = PROJECT_ROOT / ".venv" / "bin" / "python"
    if not python.is_file():
        raise RuntimeError(f"Không tìm thấy Python môi trường project: {python}")
    server = WorkspaceServer((host, port), WorkspaceHandler)
    server.project_root = PROJECT_ROOT.resolve()
    server.manager = AnalysisJobManager(server.project_root, python)
    print(f"VN Stock workspace đang chạy: http://{host}:{port}")
    print("Nhấn Ctrl+C để dừng server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng VN Stock workspace.")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Local web workspace cho VN Stock Analysis.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8787, type=int)
    args = parser.parse_args()
    serve(args.host, args.port)


if __name__ == "__main__":
    main()
