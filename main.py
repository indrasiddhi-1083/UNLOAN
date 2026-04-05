from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import json
from datetime import datetime
import os

app = FastAPI()

# ✅ CORS (correct + strict)

app.add_middleware(
CORSMiddleware,
allow_origins=["https://indrasiddhi-1083.github.io"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# ✅ ENV VARIABLES

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "indrasiddhi-1083"
REPO = "unloan-data"
BRANCH = "main"

class UserData(BaseModel):
    data: dict

@app.get("/")
def home():
    return {"status": "backend running"}

# ✅ OPTIONAL DEBUG (REMOVE LATER)

@app.get("/debug")
def debug():
    return {
        "token_present": GITHUB_TOKEN is not None,
        "token_preview": str(GITHUB_TOKEN)[:5] if GITHUB_TOKEN else "None"
    }

# ✅ CORRECT SAVE ENDPOINT

@app.post("/save")
def save_to_github(payload: UserData):
    try:
        if not GITHUB_TOKEN:
            return {"status": "error", "message": "Missing GitHub token"}

        url = f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/submissions.json"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

    # 🔹 GET existing file
        get_res = requests.get(url, headers=headers, params={"ref": BRANCH})

        if get_res.status_code == 200:
            file_data = get_res.json()
            sha = file_data.get("sha")
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            existing = json.loads(content)
        else:
            existing = []
            sha = None

    # 🔹 VALIDATE PAYLOAD
        if not payload or not payload.data:
            return {"status": "error", "message": "Invalid payload"}

        new_entry = payload.data
        new_entry["timestamp"] = datetime.utcnow().isoformat()
        existing.append(new_entry)

    # 🔹 ENCODE
        updated_content = base64.b64encode(
            json.dumps(existing, indent=2).encode("utf-8")
        ).decode("utf-8")

    # 🔹 PUSH TO GITHUB
        body = {
            "message": "New submission",
            "content": updated_content,
            "branch": BRANCH
        }

        if sha:
            body["sha"] = sha

        put_res = requests.put(url, headers=headers, json=body)

        return {
            "status": "success" if put_res.status_code in [200, 201] else "error",
            "github_status": put_res.status_code,
            "github_response": put_res.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
