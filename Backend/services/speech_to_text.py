from fastapi import APIRouter, File, UploadFile, HTTPException
import httpx
from config.settings import settings
from services.llm_service import generate_call_summary

router = APIRouter()

SPEECH_TO_TEXT_API_URL = settings.SPEECH_TO_TEXT_API_URL
SPEECH_TO_TEXT_API_KEY = settings.SPEECH_TO_TEXT_API_KEY

@router.post("/speech-to-summary")
async def speech_to_summary(audio: UploadFile = File(...)):
    try:
        # Send audio file to speech-to-text provider
        async with httpx.AsyncClient() as client:
            files = {"audio": (audio.filename, await audio.read(), audio.content_type)}
            headers = {"Authorization": f"Bearer {SPEECH_TO_TEXT_API_KEY}"}
            response = await client.post(SPEECH_TO_TEXT_API_URL, files=files, headers=headers)
            response.raise_for_status()
            transcript = response.json().get("transcript", "")
            if not transcript:
                raise HTTPException(status_code=400, detail="No transcript returned from ASR provider")
        # Generate summary from transcript
        summary = await generate_call_summary(transcript)
        return {"transcript": transcript, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))