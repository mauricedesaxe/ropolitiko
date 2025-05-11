from fastapi import FastAPI
import psutil
from app.env import validate_env_vars  # noqa: F401
import alembic.config

# Create FastAPI app
app = FastAPI(
    title="Ropolitiko",
    description="Romanian Political News Analyzer",
    version="0.1.0",
)

# Use traditional event handlers instead of lifespan
@app.on_event("startup")
async def startup_event():
    """Run database migrations automatically when the app starts"""
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)

@app.get("/")
async def root():
    return {"message": "Welcome to Ropolitiko API"}

@app.get("/health")
async def health():
    """Check if the server is running, its memory usage and cpu usage"""
    return {
        "status": "ok",
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent(interval=1)
    }