import csv
import io
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Googleシートの「公開CSV」URLをここに貼る
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1zZiRZFA1XZe1Nq474amPu20M4XW63fZNsJkanOpAGSCDgubPRS4kZk9krH_QBLXj6fjNZc4NSNPR/pub?gid=0&single=true&output=csv"


@app.get("/")
def read_root():
    return {"message": "root ok"}


@app.get("/words")
def get_words():
    resp = requests.get(SHEET_CSV_URL)
    resp.raise_for_status()

    # ★ ここを変更：UTF-8 として明示的にデコード
    text = resp.content.decode("utf-8")  # or "utf-8-sig" でも可
    f = io.StringIO(text)
    reader = csv.reader(f)

    words = []
    first = True
    for row in reader:
        if first:
            first = False
            continue
        if not row:
            continue

        word = row[0].strip()
        meaning_ja = row[1].strip() if len(row) > 1 else ""
        if not word:
            continue

        words.append({
            "word": word,
            "meaning_ja": meaning_ja,
        })

    return {"words": words}