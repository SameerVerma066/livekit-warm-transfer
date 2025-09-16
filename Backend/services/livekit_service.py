import logging
from livekit import api
from config.settings import settings
import time
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LIVEKIT_API_URL = settings.LIVEKIT_API_URL
LIVEKIT_API_KEY = settings.LIVEKIT_API_KEY
LIVEKIT_API_SECRET = settings.LIVEKIT_API_SECRET


def generate_livekit_token(identity: str, room_name: str = None) -> str:
    logger.info(f"Generating livekit token for identity '{identity}', room '{room_name}'")
    token = api.AccessToken()
    token.with_identity(identity)
    token.with_name(identity)
    if room_name:
        token.with_grants(api.VideoGrants(room_join=True, room=room_name))
    else:
        token.with_grants(api.VideoGrants(room_join=True))
    token.ttl_seconds = 3600
    jwt = token.to_jwt()
    logger.info(f"Generated livekit token for identity '{identity}'")
    return jwt


def generate_admin_token() -> str:
    logger.info("Generating admin token for LiveKit REST API")
    token = api.AccessToken(api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET)
    token.with_name("admin")
    token.with_grants(api.VideoGrants(room_admin=True))
    token.ttl_seconds = 3600
    jwt = token.to_jwt()
    logger.info("Generated admin token")
    return jwt


async def create_room(room_name: str = None) -> str:
    if not room_name:
        room_name = f"warmtransfer-{int(time.time())}"

    url = f"{LIVEKIT_API_URL}/rooms"
    admin_token = generate_admin_token()
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }
    json_data = {"name": room_name, "empty_timeout": 30}
    logger.info(f"Creating room '{room_name}' at {url}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data, headers=headers)
    logger.info(f"LiveKit create room - status: {response.status_code}")
    logger.info(f"LiveKit create room - response: '{response.text}'")

    if response.status_code == 200:
        if not response.content:
            raise Exception("LiveKit response content is empty")
        if response.text.strip() == "OK":
            # Handle plain "OK" response as success with no JSON body
            data = {"name": room_name}
            logger.info(f"Room creation returned plain 'OK', using room name: {room_name}")
        else:
            try:
                data = await response.json()
                logger.info(f"Room created with JSON data: {data}")
            except Exception as e:
                logger.error(f"Failed to parse LiveKit JSON: {e}")
                raise
    else:
        logger.error(f"Room creation failed with status {response.status_code}")
        raise Exception(f"Failed to create room: Status {response.status_code}")

    return data.get("name", room_name) if data else room_name


async def invite_participant_to_room(room_name: str, identity: str):
    logger.info(f"Generating join token for participant '{identity}' in room '{room_name}'")
    token = generate_livekit_token(identity, room_name)
    logger.info(f"Generated token for participant '{identity}'")
    return token


async def remove_participant_from_room(room_name: str, identity: str):
    url = f"{LIVEKIT_API_URL}/rooms/{room_name}/participants/{identity}"
    admin_token = generate_admin_token()
    headers = {"Authorization": f"Bearer {admin_token}"}
    logger.info(f"Removing participant '{identity}' from room '{room_name}'")

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
    if response.status_code == 200:
        logger.info(f"Successfully removed participant '{identity}' from room '{room_name}'")
    else:
        logger.error(f"Failed to remove participant '{identity}': Status {response.status_code} - Response text: {response.text}")
        raise Exception(f"Failed to remove participant: Status {response.status_code}")


async def send_message_to_room(room_name: str, identity: str, message: str):
    # Placeholder for actual messaging implementation
    logger.info(f"Sending message to room '{room_name}' for participant '{identity}': {message}")
    # Real implementation would be event or WebSocket based
    return True
