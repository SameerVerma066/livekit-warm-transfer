# app/routes/livekit_routes.py

from fastapi import APIRouter, Query, HTTPException
from app.services.livekit_service import generate_livekit_token

router = APIRouter()

@router.get("/token")
async def get_livekit_token(identity: str = Query(..., description="User identity"), room_name: str = Query(None, description="Room name")):
    try:
        token = generate_livekit_token(identity, room_name)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
