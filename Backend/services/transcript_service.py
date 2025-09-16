from typing import Dict

# Simple in-memory storage: {call_id: transcript}
_transcript_store: Dict[str, str] = {}

def save_transcript(call_id: str, transcript: str):
    _transcript_store[call_id] = transcript

def get_transcript(call_id: str) -> str:
    return _transcript_store.get(call_id, "")
