# AI-Powered Document Classifier

A production-ready machine learning web app that classifies documents into four categories:

- **Resume**
- **Invoice**
- **Legal Document**
- **Research Paper**

Built with Flask, Scikit-learn (TF-IDF + Logistic Regression), PyPDF, SQLite, and Bootstrap.

## Features

- Upload PDF files and extract text automatically
- Classify pasted text or PDF content
- Confidence score and per-class probabilities
- Prediction history stored in SQLite
- Confusion matrix visualization
- Accuracy / F1-score performance report
- Bootstrap UI with responsive layout
- Render deployment ready

## How it works

```text
Upload PDF (or paste text)
        ↓
Extract text (PyPDF)
        ↓
TF-IDF vectorization
        ↓
Logistic Regression classifier
        ↓
Category + confidence %
        ↓
Save to SQLite history
```

## Project structure

Document-Classifier/
│
├── app.py                          # Flask web application
├── train.py                        # Model training script
├── database.py                     # SQLite database setup
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
├── render.yaml                     # Render blueprint config
├── runtime.txt                     # Python runtime version
├── predictions.db                  # SQLite prediction history
├── .gitignore
├── README.md
├── DEPLOY.md
├── Document-Classifier.code-workspace
│
├── model/
│   ├── classifier.pkl              # Trained Logistic Regression model
│   └── vectorizer.pkl              # TF-IDF vectorizer
│
├── scripts/
│   └── expand_training_data.py     # Data augmentation script
│
├── static/
│   ├── style.css                   # Application styling
│   ├── confusion_matrix.png        # Model evaluation visualization
│   └── metrics.json                # Accuracy & F1-score metrics
│
├── templates/
│   ├── index.html                  # Classification interface
│   └── history.html                # Prediction history page
│
├── data/                           # Training/reference data
│
└── dataset/
    └── dataset.csv                 # Labeled training dataset


## 
in shot 

    Document Classifier
├── Backend (Flask)
├── Machine Learning (Scikit-learn)
├── Database (SQLite)
├── Frontend (HTML, CSS, Bootstrap)
├── Dataset
├── Trained Models
└── Deployment (Render)



## Local setup

```bash
git clone https://github.com/YOUR_USERNAME/Document-Classifier.git
cd Document-Classifier
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/expand_training_data.py   # optional: regenerate training CSV
python train.py
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Model details

| Component   | Choice              |
|------------|---------------------|
| Features   | TF-IDF (1–2 grams)  |
| Classifier | Logistic Regression |
| Labels     | 4 document types    |

After training, `train.py` saves:

- `model/classifier.pkl` and `model/vectorizer.pkl`
- `static/confusion_matrix.png`
- `static/metrics.json` (accuracy, macro F1, per-class scores)

## Improve accuracy

1. Add more labeled rows to `dataset/dataset.csv` (real PDF text snippets work best).
2. Run `python train.py` again.
3. Commit updated model files and static assets for deployment.

## Deploy on Render (free tier)

1. Push this repo to GitHub (include `model/` and `static/` artifacts after training).
2. [render.com](https://render.com) → **New** → **Web Service** → connect repo.
3. Settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Python version:** 3.11+
4. Deploy and copy the live URL for your internship portal.

Or use the included `render.yaml` with **Blueprint** deploy.

## Internship submission

| Field      | Value                                                   |
|-----------|----------------------------------------------------------|
| GitHub    | `https://github.com/YOUR_USERNAME/Document-Classifier`  |
| Live link | Your Render/Railway URL                                 |

## License

MIT — use freely for portfolio and internship submissions.
