from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.transcript_service import save_transcript, get_transcript
from services.llm_service import generate_call_summary

router = APIRouter()

class TranscriptRequest(BaseModel):
    call_id: str
    transcript: str

@router.post("/save")
async def save_call_transcript(req: TranscriptRequest):
    try:
        print(f"Received transcript for call_id: {req.call_id}")
        save_transcript(req.call_id, req.transcript)
        print("Transcript saved successfully.")
        
        summary = await generate_call_summary(req.transcript)
        
        return {
            "message": "Transcript saved",
            "summary": summary
        }
    except Exception as e:
        print(f"Error in /transcript/save: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{call_id}")
def get_call_transcript(call_id: str):
    transcript = get_transcript(call_id)
    if transcript:
        return {"call_id": call_id, "transcript": transcript}
    raise HTTPException(status_code=404, detail="Transcript not found")
