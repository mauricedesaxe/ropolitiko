from contextlib import asynccontextmanager
from fastapi import FastAPI
import psutil
from app.env import validate_env_vars  # noqa: F401
import alembic.config

@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)
    
    # Start the scraping scheduler
    from app.scraper.orchestration import start_scraping_scheduler, stop_scraping_scheduler
    start_scraping_scheduler()
    
    yield
    
    # Stop the scheduler on shutdown
    stop_scraping_scheduler()

# Create FastAPI app
app = FastAPI(
    title="Ropolitiko",
    description="Romanian Political News Analyzer",
    version="0.1.0",
    lifespan=lifespan,
)

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