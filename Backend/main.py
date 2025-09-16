from fastapi import FastAPI
from routes import livekit_routes,llm_routes
app = FastAPI()
app.include_router(livekit_routes.router, prefix="/livekit")
app.include_router(llm_routes.router, prefix="/llm")

