"""Kaggle-ready QLoRA SFT for StockLens AI.

Upload ``stocklens_train.jsonl`` and ``stocklens_eval.jsonl`` as a Kaggle
Dataset, attach it to a GPU notebook, then set DATA_DIR below to that mounted
dataset directory.  Outputs contain a PEFT adapter, metrics and tokenizer.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer


# Kaggle lets you override these in the notebook Environment variables.
MODEL_NAME = os.environ.get("STOCKLENS_BASE_MODEL", "Qwen/Qwen3-4B")
DATA_DIR = Path(os.environ.get("STOCKLENS_DATA_DIR", "/kaggle/input/stocklens-sft"))
OUTPUT_DIR = Path(os.environ.get("STOCKLENS_OUTPUT_DIR", "/kaggle/working/stocklens-qwen3-4b-lora"))
MAX_LENGTH = int(os.environ.get("STOCKLENS_MAX_LENGTH", "2048"))


def main() -> None:
    train_path = DATA_DIR / "stocklens_train.jsonl"
    eval_path = DATA_DIR / "stocklens_eval.jsonl"
    if not train_path.is_file() or not eval_path.is_file():
        raise FileNotFoundError(
            "Không tìm thấy stocklens_train.jsonl và stocklens_eval.jsonl. "
            "Hãy attach Kaggle Dataset rồi đặt STOCKLENS_DATA_DIR đúng thư mục input."
        )
    if not torch.cuda.is_available():
        raise RuntimeError("Notebook này cần bật GPU accelerator trên Kaggle.")

    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quantization,
        device_map="auto",
        torch_dtype=compute_dtype,
        trust_remote_code=True,
    )
    model.config.use_cache = False
    dataset = load_dataset(
        "json",
        data_files={"train": str(train_path), "eval": str(eval_path)},
    )
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    arguments = SFTConfig(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=2,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        gradient_checkpointing=True,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        bf16=compute_dtype == torch.bfloat16,
        fp16=compute_dtype == torch.float16,
        max_length=MAX_LENGTH,
        report_to="none",
        seed=42,
    )
    trainer = SFTTrainer(
        model=model,
        args=arguments,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        processing_class=tokenizer,
        peft_config=lora,
    )
    trainer.train()
    metrics = trainer.evaluate()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    (OUTPUT_DIR / "eval_results.json").write_text(
        json.dumps({key: float(value) for key, value in metrics.items()}, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "stocklens_training_manifest.json").write_text(
        json.dumps(
            {
                "base_model": MODEL_NAME,
                "method": "QLoRA",
                "max_length": MAX_LENGTH,
                "train_examples": len(dataset["train"]),
                "eval_examples": len(dataset["eval"]),
                "note": "Adapter trains tutor behavior only. Historical OHLCV remains a deterministic report lookup.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Đã lưu LoRA adapter và metrics tại: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
