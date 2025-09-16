from livekit import api
from config.settings import settings

def create_room(room_name: str):
    # Placeholder: LiveKit server API call to create a room if needed
    # LiveKit rooms are created on demand usually, so may not need explicit call
    return room_name

def generate_livekit_token(identity: str, room_name: str = None) -> str:
    token = api.AccessToken()
    token.with_identity(identity)
    if room_name:
        token.with_grants(api.VideoGrants(room_join=True, room=room_name))
    else:
        token.with_grants(api.VideoGrants(room_join=True))
    token.ttl_seconds = 3600
    return token.to_jwt()

def initiate_warm_transfer(caller_identity: str, agent_identity: str, room_name: str):
    # Caller and agent both join the same room for warm transfer
    caller_token = generate_livekit_token(caller_identity, room_name)
    agent_token = generate_livekit_token(agent_identity, room_name)
    return {
        "room_name": room_name,
        "caller_token": caller_token,
        "agent_token": agent_token,
    }
