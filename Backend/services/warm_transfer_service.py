from services.livekit_service import (
    create_room,
    invite_participant_to_room,
    remove_participant_from_room,
    send_message_to_room
)
from services.transcript_service import get_transcript
from services.llm_service import generate_call_summary


async def initiate_warm_transfer(original_room_id: str, agent_a_id: str, agent_b_id: str, caller_id: str):
    # Create a new room for warm transfer
    new_room_id = await create_room()

    # Generate join token for Agent B
    agent_b_token = await invite_participant_to_room(new_room_id, agent_b_id)

    # Generate join token for Caller
    caller_token = await invite_participant_to_room(new_room_id, caller_id)

    # Get transcript of the original room
    transcript = get_transcript(original_room_id)

    # Generate call summary from transcript
    summary = await generate_call_summary(transcript)

    # Send summary message to Agent B in the new room
    await send_message_to_room(new_room_id, agent_b_id, summary)

    # Remove Agent A from the original room
    await remove_participant_from_room(original_room_id, agent_a_id)

    # Return details including tokens and summary for frontend use
    return {
        "new_room_id": new_room_id,
        "agent_b_token": agent_b_token,
        "caller_token": caller_token,
        "summary": summary,
        "status": "Warm transfer initiated successfully"
    }
