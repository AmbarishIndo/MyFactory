from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .routers import agents, memory
except ImportError:
    from backend.routers import agents, memory

app = FastAPI(
    title="Central Command Hub API",
    description="Backend service for orchestrating multi-agent digital conglomerate.",
    version="0.1.0",
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api")
app.include_router(memory.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Central Command Hub Backend API",
        "version": "0.1.0",
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
