import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")
    LIVEKIT_API_URL: str = os.getenv("LIVEKIT_API_URL", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SPEECH_TO_TEXT_API_KEY: str = os.getenv("SPEECH_TO_TEXT_API_KEY", "")
    SPEECH_TO_TEXT_API_URL: str = os.getenv("SPEECH_TO_TEXT_API_URL", "")  
    ASSEMBLYAI_UPLOAD_URL :str = os.getenv("ASSEMBLYAI_UPLOAD_URL","")

    def validate(self):
        errors = []
        if not self.LIVEKIT_API_KEY:
            errors.append("LIVEKIT_API_KEY is not set")
        if not self.LIVEKIT_API_SECRET:
            errors.append("LIVEKIT_API_SECRET is not set")
        if not self.LIVEKIT_API_URL:
            errors.append("LIVEKIT_API_URL is not set")
        if not self.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is not set")
        if not self.SPEECH_TO_TEXT_API_KEY:
            errors.append("SPEECH_TO_TEXT_API_KEY is not set")
        if not self.SPEECH_TO_TEXT_API_URL:  # Add validation here too
            errors.append("SPEECH_TO_TEXT_API_URL is not set")
        if errors:
            raise EnvironmentError(", ".join(errors))


settings = Settings()
settings.validate()
