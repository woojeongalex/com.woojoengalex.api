"""
Watson Policy Filter — beomi/KcELECTRA-base 파인튜닝
Case A/B 라우팅 전 욕설·비상식 텍스트 정책 필터
"""

from datasets import Dataset
import pandas as pd
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "beomi/KcELECTRA-base"
DATA_PATH = "/app/data/train.csv"
OUTPUT_DIR = "/app/output"
NUM_LABELS = 2  # 0=PASS, 1=BLOCK


def load_dataset():
    df = pd.read_csv(DATA_PATH)
    dataset = Dataset.from_pandas(df)
    return dataset


def tokenize(batch, tokenizer):
    return tokenizer(
        batch["text"], padding="max_length", truncation=True, max_length=128
    )


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=NUM_LABELS,
        id2label={0: "PASS", 1: "BLOCK"},
        label2id={"PASS": 0, "BLOCK": 1},
    )

    dataset = load_dataset()
    dataset = dataset.map(lambda b: tokenize(b, tokenizer), batched=True)
    dataset = dataset.rename_column("label", "labels")
    dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    split = dataset.train_test_split(test_size=0.2, seed=42)

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir=f"{OUTPUT_DIR}/logs",
        logging_steps=10,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=split["train"],
        eval_dataset=split["test"],
    )

    trainer.train()
    trainer.save_model(f"{OUTPUT_DIR}/watson-policy-filter")
    tokenizer.save_pretrained(f"{OUTPUT_DIR}/watson-policy-filter")
    print(f"\n[Watson] 모델 저장 완료: {OUTPUT_DIR}/watson-policy-filter")


if __name__ == "__main__":
    main()
