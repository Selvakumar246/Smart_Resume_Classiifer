"""Train and evaluate the production classifier from a labeled CSV.

Required columns:
- text: extracted resume text
- label: one category name used by the application taxonomy

Example:
python training/train_classifier.py --data /path/to/resumes.csv --output models/resume_classifier.joblib
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def train(data_path: Path, output_path: Path, test_size: float, random_state: int) -> dict:
    frame = pd.read_csv(data_path)
    required = {"text", "label"}
    if not required.issubset(frame.columns):
        raise ValueError("Dataset must contain text and label columns.")
    frame = frame.dropna(subset=["text", "label"]).copy()
    frame["text"] = frame["text"].astype(str).str.strip()
    frame["label"] = frame["label"].astype(str).str.strip()
    frame = frame[frame["text"].str.len() >= 80]
    counts = frame["label"].value_counts()
    rare = counts[counts < 5].index.tolist()
    if rare:
        raise ValueError(f"Each label needs at least 5 examples. Too small: {rare}")

    x_train, x_test, y_train, y_test = train_test_split(
        frame["text"], frame["label"], test_size=test_size, random_state=random_state, stratify=frame["label"]
    )
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True, min_df=2, max_df=.97, max_features=80_000)),
        ("classifier", LogisticRegression(max_iter=2500, class_weight="balanced", C=3.0)),
    ])
    pipeline.fit(x_train, y_train)
    predicted = pipeline.predict(x_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predicted)), 4),
        "macro_f1": round(float(f1_score(y_test, predicted, average="macro")), 4),
        "weighted_f1": round(float(f1_score(y_test, predicted, average="weighted")), 4),
        "test_examples": int(len(y_test)),
        "train_examples": int(len(y_train)),
        "labels": sorted(frame["label"].unique().tolist()),
        "classification_report": classification_report(y_test, predicted, output_dict=True, zero_division=0),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "labels": metrics["labels"], "metrics": metrics}, output_path)
    output_path.with_suffix(".metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("models/resume_classifier.joblib"))
    parser.add_argument("--test-size", type=float, default=.2)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    metrics = train(args.data, args.output, args.test_size, args.random_state)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
