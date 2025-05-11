import os
from dotenv import load_dotenv

# Load .env file on module import
load_dotenv()

def get_env(key: str, default=None):
    """Get environment variable or return default value"""
    if default is None and key not in os.environ:
        raise ValueError(f"Environment variable {key} is not set")
    return os.getenv(key, default)

# Define required environment variables (these will fail if not present)
SCRAPING_BEE_API_KEY = get_env("SCRAPING_BEE_API_KEY")
DATABASE_URL = get_env("DATABASE_URL", "postgresql://@localhost/ropolitiko")

# Define optional environment variables with defaults
# OTHER_API_KEY = get_env("OTHER_API_KEY", "")

# Validate required environment variables on import
def validate_env_vars():
    """Validate all required environment variables are set"""
    print("Running validate_env_vars")
    required_vars = [
        "SCRAPING_BEE_API_KEY",
        # Add other required environment variables here
    ]
    
    missing_vars = []
    for var in required_vars:
        if var not in os.environ:
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Required environment variables not set: {', '.join(missing_vars)}")

# Run validation on module import
validate_env_vars()