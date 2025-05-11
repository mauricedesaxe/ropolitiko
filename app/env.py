import os
from dotenv import load_dotenv

# Load .env file on module import
load_dotenv()

def get_env(key: str, default=None):
    """Get environment variable or return default value"""
    return os.getenv(key, default)

# Commonly used environment variables
API_PREFIX = get_env("API_PREFIX", "/api/v1")
OPENAI_API_KEY = get_env("OPENAI_API_KEY", "")
NEWS_SOURCES = get_env("NEWS_SOURCES", "").split(",") 