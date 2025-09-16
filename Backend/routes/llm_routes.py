import httpx
from config.settings import settings  # Adjusted to your backend folder structure

from fastapi import APIRouter, Body

router = APIRouter()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_call_summary(transcript: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # Choose the model you prefer
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following call transcript:\n{transcript}"
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        summary = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return summary


# FastAPI endpoint for call summary
@router.post("/summary")
async def get_call_summary(transcript: str = Body(..., embed=True)):
    summary = await generate_call_summary(transcript)
    return {"summary": summary}
