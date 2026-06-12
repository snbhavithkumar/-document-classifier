# Fix "Page Not Found" on live URL

## 1. Use the correct URL (most common mistake)

This project is a **Python web app**. It does **not** run on GitHub Pages.


| URL type                                           | Works?                        |
| -------------------------------------------------- | ----------------------------- |
| `https://something.onrender.com`                   | Yes (if deploy succeeded)     |
| `https://something.up.railway.app`                 | Yes                           |
| `https://YOUR_USER.github.io/Document-Classifier/` | **No** — always 404 for Flask |


**Live link must be your Render or Railway URL**, not `github.io`.

Open the **root** URL only (no extra path):

```text
https://your-service.onrender.com/
```

Test health: `https://your-service.onrender.com/health` → should show `{"status":"ok"}`.

---

## 2. Render: deploy the branch that has your code

Your app lives on branch `cursor/pdf-document-classifier`. If Render deploys empty `main`, the site fails.

**Render dashboard → your service → Settings → Build & Deploy:**

- **Branch:** `cursor/pdf-document-classifier` (or merge that branch into `main` and use `main`)
- **Root directory:** leave blank
- **Runtime:** Python 3
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

Click **Manual Deploy → Deploy latest commit**.

---

## 3. Confirm GitHub has model files

On GitHub, open the repo and check these exist:

- `model.pkl`
- `vectorizer.pkl`
- `app.py`
- `templates/index.html`

If missing, push again:

```bash
cd /Users/apple/Projects/Document-Classifier
git push origin cursor/pdf-document-classifier
```

---

## 4. Check Render logs

**Render → Logs**

- **Build failed** → fix `pip install` errors, redeploy
- **"No open ports" / gunicorn error** → start command must be `gunicorn app:app --bind 0.0.0.0:$PORT`
- **FileNotFoundError model.pkl** → commit and push `model.pkl` / `vectorizer.pkl`

---

## 5. Free tier cold start

First visit after idle can take 30–60 seconds. Wait, then refresh `/` — not a 404, just slow.

---

## Quick checklist

- Live URL is `*.onrender.com` or `*.railway.app`, not `github.io`
- Render branch has `app.py` + `model.pkl`
- Start command uses gunicorn and `$PORT`
- `/health` returns OK after deploy

