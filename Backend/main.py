from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import livekit_routes, llm_routes, warm_transfer_routes, transcript_routes,speech_to_text_routes
app = FastAPI()

# Allow your frontend origin(s) here
origins = [
    "http://localhost:3000",
    # Add other frontend URLs you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)

# Include your routers as before
app.include_router(livekit_routes.router, prefix="/livekit")
app.include_router(llm_routes.router, prefix="/llm")
app.include_router(warm_transfer_routes.router, prefix="/warm_transfer")
app.include_router(transcript_routes.router, prefix="/transcript")

# Register speech-to-text router

app.include_router(speech_to_text_routes.router, prefix="/speech")
