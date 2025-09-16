import logging
import httpx
from config.settings import settings

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_call_summary(transcript: str) -> str:
    if not transcript:
        logger.warning("Empty transcript received for summary generation")
        return ""

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following call transcript:\n{transcript}"
            }
        ],
        "max_tokens": 200,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            summary = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not summary:
                logger.warning("Summary generation returned empty content")
            return summary
    except Exception as e:
        logger.error(f"Error generating call summary: {e}")
        return ""
