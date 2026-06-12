"""
Train TF-IDF + Logistic Regression document classifier.

Categories: Resume, Invoice, Research Paper, Legal Document
"""

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "dataset" / "dataset.csv"
MODEL_PATH = ROOT / "model" / "classifier.pkl"
VECTORIZER_PATH = ROOT / "model" / "vectorizer.pkl"
METRICS_PATH = ROOT / "static" / "metrics.json"
CONFUSION_MATRIX_PATH = ROOT / "static" / "confusion_matrix.png"

LABELS = ["Resume", "Invoice", "Research Paper", "Legal Document"]


def load_dataset() -> tuple[list[str], list[str]]:
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip()
    return df["text"].tolist(), df["label"].tolist()


def save_confusion_matrix(y_test, y_pred) -> None:
    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=LABELS,
        yticklabels=LABELS,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix — Document Classifier")
    plt.tight_layout()
    CONFUSION_MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CONFUSION_MATRIX_PATH, dpi=120)
    plt.close(fig)


def save_metrics(y_test, y_pred) -> None:
    report = classification_report(y_test, y_pred, labels=LABELS, output_dict=True)
    metrics = {
        "accuracy": round(report["accuracy"] * 100, 2),
        "macro_f1": round(report["macro avg"]["f1-score"] * 100, 2),
        "weighted_f1": round(report["weighted avg"]["f1-score"] * 100, 2),
        "per_class": {
            label: {
                "precision": round(report[label]["precision"] * 100, 2),
                "recall": round(report[label]["recall"] * 100, 2),
                "f1": round(report[label]["f1-score"] * 100, 2),
            }
            for label in LABELS
        },
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))


def train() -> None:
    texts, labels = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=2000,
        C=1.0,
        class_weight="balanced",
    )
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    print("Test set evaluation:\n")
    print(classification_report(y_test, y_pred, labels=LABELS))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    save_confusion_matrix(y_test, y_pred)
    save_metrics(y_test, y_pred)

    print(f"Saved {MODEL_PATH}")
    print(f"Saved {VECTORIZER_PATH}")
    print(f"Saved {CONFUSION_MATRIX_PATH}")
    print(f"Saved {METRICS_PATH}")


if __name__ == "__main__":
    train()
