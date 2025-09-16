from livekit import AccessToken, RoomGrant
from app.config.settings import settings
import time

def generate_livekit_token(identity: str, room_name: str = None) -> str:
    # Create a new access token using LiveKit API keys
    token = AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET, identity=identity)

    # Add grants for room access if room_name is specified
    if room_name:
        room_grant = RoomGrant(room=room_name)
        token.add_grant(room_grant)

    # Set token expiry (default 1 hour)
    token.ttl_seconds = 3600

    # Generate and return JWT token string
    return token.to_jwt()