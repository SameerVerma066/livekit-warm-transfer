from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.warm_transfer_service import initiate_warm_transfer, create_room

router = APIRouter()

class WarmTransferRequest(BaseModel):
    caller_identity: str
    agent_identity: str
    room_name: str

@router.post("/start")
def start_warm_transfer(req: WarmTransferRequest):
    try:
        create_room(req.room_name)
        tokens = initiate_warm_transfer(req.caller_identity, req.agent_identity, req.room_name)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
