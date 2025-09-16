from fastapi import FastAPI
from routes import livekit_routes,llm_routes, warm_transfer_routes,transcript_routes


app = FastAPI()


app.include_router(livekit_routes.router, prefix="/livekit")
app.include_router(llm_routes.router, prefix="/llm")
app.include_router(warm_transfer_routes.router, prefix="/warm-transfer")
app.include_router(transcript_routes.router, prefix="/transcript")