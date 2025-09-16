from services.livekit_service import (
    create_room,
    invite_participant_to_room,
    remove_participant_from_room,
    send_message_to_room
)
from services.transcript_service import get_transcript
from services.llm_service import generate_call_summary


async def initiate_warm_transfer(original_room_id: str, agent_a_id: str, agent_b_id: str, caller_id: str):
    new_room_id = await create_room()  # Create new room for warm transfer

    agent_b_token = await invite_participant_to_room(new_room_id, agent_b_id)

    transcript = get_transcript(original_room_id)

    summary = await generate_call_summary(transcript)

    await send_message_to_room(new_room_id, agent_b_id, summary)

    await remove_participant_from_room(original_room_id, agent_a_id)

    # Caller connection management to new room would go here

    return {
        "new_room_id": new_room_id,
        "agent_b_token": agent_b_token,
        "summary": summary,
        "status": "Warm transfer initiated successfully"
    }
