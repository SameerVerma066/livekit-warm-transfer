from typing import Dict
import logging

logger = logging.getLogger(__name__)

_transcript_store: Dict[str, str] = {}

def save_transcript(call_id: str, transcript: str):
    if not call_id or not transcript:
        logger.warning("Empty call_id or transcript on save_transcript")
        return
    _transcript_store[call_id] = transcript
    logger.info(f"Transcript saved for call_id: {call_id}")

def get_transcript(call_id: str) -> str:
    if not call_id:
        logger.warning("Empty call_id in get_transcript")
        return ""
    transcript = _transcript_store.get(call_id, "")
    if not transcript:
        logger.warning(f"No transcript found for call_id: {call_id}")
    return transcript
