import os
from pathlib import Path
from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from google_auth_oauthlib.flow import Flow

# Import our internal modules
from .engine import engine
from .google_docs_helper import create_doc

# --- CONFIGURATION ---

# Robust way to find client_secret.json in the root folder
# (Goes up one level from this file's location)
BASE_DIR = Path(__file__).resolve().parent.parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file"
]

# --- APP SETUP ---

app = FastAPI(
    title="YouTube to Notes API",
    description="An AI agent that converts YouTube videos into study notes.",
    version="1.0.0"
)

# --- REQUEST MODELS ---

class NoteRequest(BaseModel):
    url: str

class SaveRequest(BaseModel):
    token: str
    title: str
    notes: str

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Service is live"}

@app.post("/api/v1/generate")
async def generate_notes(request: NoteRequest):
    """
    Takes a YouTube URL, runs the AI agent, and returns the notes.
    """
    try:
        # Trigger the LangGraph workflow
        result = engine.invoke({"video_url": request.url})

        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])

        return {
            "video_url": request.url,
            "notes": result["notes"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- GOOGLE AUTH FLOW ---

@app.get("/auth/login")
def login():
    """
    Step 1: Redirect user to Google Login.
    """
    # Check if secret file exists before crashing
    if not CLIENT_SECRETS_FILE.exists():
        raise HTTPException(status_code=500, detail="client_secret.json not found in root directory.")

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/callback"
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)

@app.get("/auth/callback")
def callback(code: str):
    """
    Step 2: Handle the callback from Google.
    """
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/callback"
    )

    # Exchange authorization code for access token
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Return the token to the user (In a real app, you'd save this to a DB)
    return {
        "message": "Login successful!",
        "access_token": credentials.token,
        "instruction": "Copy this 'access_token' and use it in the /save-doc endpoint."
    }

@app.post("/api/v1/save-doc")
def save_doc_endpoint(payload: SaveRequest):
    """
    Step 3: Use the token to create a Google Doc.
    """
    try:
        link = create_doc(payload.token, payload.title, payload.notes)
        return {"status": "success", "doc_link": link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)