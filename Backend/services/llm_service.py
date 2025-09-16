# backend/services/llm_service.py

import os
import httpx
from config.settings import settings 

GROQ_API_URL = "https://api.groq.com/v1/llm/generate"  # Example URL, update if different

async def generate_call_summary(transcript: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "groq-chat",  # Replace with actual model name
        "prompt": f"Summarize the following call transcript:\n{transcript}",
        "max_tokens": 200,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Assuming the summary is in data['choices'][0]['text'] or adjust according to API
        summary = data.get("choices", [{}])[0].get("text", "")
        return summary
