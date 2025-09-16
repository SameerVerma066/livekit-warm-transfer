from livekit import api
from config.settings import settings  # Adjusted for your backend folder structure
import time

def generate_livekit_token(identity: str, room_name: str = None) -> str:
    token = api.AccessToken()
    token.with_identity(identity)
    token.with_name(identity)  # Optional: set a display name or use identity

    # Add grants for room joining, and room if specified
    if room_name:
        token.with_grants(api.VideoGrants(room_join=True, room=room_name))
    else:
        token.with_grants(api.VideoGrants(room_join=True))

    # Set expiry TTL in seconds (default is 1 hour)
    token.ttl_seconds = 3600

    # Generate and return JWT token string
    return token.to_jwt()
