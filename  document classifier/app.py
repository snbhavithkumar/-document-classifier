import json
from io import BytesIO



from pathlib import Path

import joblib
from flask import Flask, render_template, request
from pypdf import PdfReader

from database import init_db, save_prediction, get_history

ROOT = Path(__file__).resolve().parent

MODEL_PATH = ROOT / "model" / "classifier.pkl"
VECTORIZER_PATH = ROOT / "model" / "vectorizer.pkl"
METRICS_PATH = ROOT / "static" / "metrics.json"
CONFUSION_MATRIX_PATH = ROOT / "static" / "confusion_matrix.png"




app = Flask(__name__)

model = None
vectorizer = None
metrics = None


def load_artifacts():
    global model
    global vectorizer
    global metrics

    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    except FileNotFoundError:
        print("Warning: Model files not found. Train model with: python train.py")

    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            metrics = json.load(f)


def extract_pdf_text(file_storage):
    data = file_storage.read()
    reader = PdfReader(BytesIO(data))
    text_parts = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)

    return "\n".join(text_parts)


def predict(text, filename=""):
    if not model or not vectorizer:
        return {"error": "Model not loaded. Please train the model first."}

    if not text.strip():
        return {"error": "No text found"}

    vec = vectorizer.transform([text])
    label = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    confidence = float(max(proba)) * 100

    # Get per-class scores
    scores = {}
    for i, class_label in enumerate(model.classes_):
        scores[class_label] = round(float(proba[i]) * 100, 1)

    result = {
        "category": label,
        "confidence": round(confidence, 1),
        "preview": text[:500],
        "scores": scores,
    }

    # Save to database
    if filename:
        save_prediction(filename, label, confidence)

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = "user_input"

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if "pdf" in request.files:
            pdf_file = request.files["pdf"]
            if pdf_file.filename:
                filename = pdf_file.filename
                try:
                    text = extract_pdf_text(pdf_file)
                except Exception as exc:
                    result = {"error": str(exc)}
                    return render_template(
                        "index.html",
                        result=result,
                        metrics=metrics,
                        has_confusion_matrix=CONFUSION_MATRIX_PATH.exists(),
                        confusion_matrix_url="/static/confusion_matrix.png",
                    )

        result = predict(text, filename)

    return render_template(
        "index.html",
        result=result,
        metrics=metrics,
        has_confusion_matrix=CONFUSION_MATRIX_PATH.exists(),
        confusion_matrix_url="/static/confusion_matrix.png",
    )


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)


# Initialize at module load (for Gunicorn)
init_db()
load_artifacts()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
