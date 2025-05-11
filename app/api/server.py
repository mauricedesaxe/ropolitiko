import os
from fastapi import FastAPI
from dotenv import load_dotenv
import psutil

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Ropolitiko",
    description="Romanian Political News Analyzer",
    version="0.1.0",
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