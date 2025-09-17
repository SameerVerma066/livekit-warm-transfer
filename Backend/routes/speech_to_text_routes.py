from fastapi import APIRouter, File, UploadFile, HTTPException
import httpx
import asyncio
from config.settings import settings
from services.llm_service import generate_call_summary

router = APIRouter()

SPEECH_TO_TEXT_API_KEY = settings.SPEECH_TO_TEXT_API_KEY
SPEECH_TO_TEXT_API_URL = settings.SPEECH_TO_TEXT_API_URL 
ASSEMBLYAI_UPLOAD_URL = settings.ASSEMBLYAI_UPLOAD_URL  

@router.post("/speech-to-summary")
async def speech_to_summary(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        headers = {"authorization": SPEECH_TO_TEXT_API_KEY}

        async with httpx.AsyncClient() as client:
            # Step 1: Upload audio to AssemblyAI
            upload_response = await client.post(
                ASSEMBLYAI_UPLOAD_URL,
                content=audio_bytes,
                headers=headers,
            )
            upload_response.raise_for_status()
            upload_url = upload_response.json().get("upload_url")
            if not upload_url:
                raise HTTPException(status_code=400, detail="Failed to upload audio to AssemblyAI")

            # Step 2: Request transcription job
            transcript_payload = {"audio_url": upload_url}
            transcript_response = await client.post(
                SPEECH_TO_TEXT_API_URL,
                json=transcript_payload,
                headers=headers,
            )
            transcript_response.raise_for_status()
            transcript_id = transcript_response.json().get("id")
            if not transcript_id:
                raise HTTPException(status_code=400, detail="Failed to start transcription job")

            # Step 3: Poll for transcription status up to ~30 seconds
            poll_url = f"{SPEECH_TO_TEXT_API_URL}/{transcript_id}"
            transcript_text = None
            for _ in range(30):
                poll_response = await client.get(poll_url, headers=headers)
                poll_response.raise_for_status()
                poll_data = poll_response.json()
                status = poll_data.get("status")
                if status == "completed":
                    transcript_text = poll_data.get("text", "")
                    break
                elif status == "failed":
                    raise HTTPException(status_code=400, detail="AssemblyAI transcription failed")
                await asyncio.sleep(1)

            if not transcript_text:
                raise HTTPException(status_code=504, detail="Transcription timed out")

        # Step 4: Generate call summary
        summary = await generate_call_summary(transcript_text)

        return {"transcript": transcript_text, "summary": summary}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
