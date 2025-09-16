from fastapi import FastAPI
from app.routes import livekit_routes

app = FastAPI()
app.include_router(livekit_routes.router, prefix="/livekit")

