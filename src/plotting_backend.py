from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import cnsplots as cns
except ImportError:  # pragma: no cover - optional dependency
    cns = None


def has_cnsplots() -> bool:
    return cns is not None


def configure_publication_style() -> None:
    if cns is None:
        return
    cns.setup_matplotlib(color_cycle="Tableau")


def save_figure(figure: Any, output_path: Path, *, dpi: int = 170) -> None:
    if cns is None:
        figure.savefig(output_path, dpi=dpi)
        return

    figure.canvas.draw_idle()
    figure.canvas.flush_events()
    cns.savefig(str(output_path))

