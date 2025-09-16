from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.warm_transfer_service import initiate_warm_transfer

router = APIRouter()

class WarmTransferRequest(BaseModel):
    original_room_id: str
    agent_a_id: str
    agent_b_id: str
    caller_id: str


@router.post("/initiate")
async def start_warm_transfer(req: WarmTransferRequest):
    try:
        result = await initiate_warm_transfer(
            original_room_id=req.original_room_id,
            agent_a_id=req.agent_a_id,
            agent_b_id=req.agent_b_id,
            caller_id=req.caller_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
