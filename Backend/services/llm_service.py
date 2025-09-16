# backend/services/llm_service.py

import os
import httpx
from config.settings import settings 

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Correct Groq OpenAI-compatible endpoint

async def generate_call_summary(transcript: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following call transcript:\n{transcript}"
            }
        ],
        "max_tokens": 200
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        summary = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return summary
