from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .engine import engine  # Import your LangGraph engine

# 1. Define Request Model
# This ensures the user sends valid JSON data
class NoteRequest(BaseModel):
    url: str

# 2. Initialize FastAPI
app = FastAPI(
    title="YouTube to Notes API",
    description="An AI agent that converts YouTube videos into study notes.",
    version="1.0.0"
)

# 3. Define Endpoints

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
        # invoke() returns the final state of the graph
        result = engine.invoke({"video_url": request.url})

        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])

        return {
            "video_url": request.url,
            "notes": result["notes"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Run Instruction (for debugging)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)