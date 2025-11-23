import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """Configuration manager for Stark Music Bot"""
    
    # Required Vars
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
    ASSISTANT_STRING: str = os.getenv("ASSISTANT_STRING", "")
    ASSISTANT_ID: int = int(os.getenv("ASSISTANT_ID", "0"))
    
    # Optional Vars
    UPDATES_CHANNEL: Optional[str] = os.getenv("UPDATES_CHANNEL")
    SPOTIFY_CLIENT_ID: Optional[str] = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET: Optional[str] = os.getenv("SPOTIFY_CLIENT_SECRET")
    GENIUS_API_TOKEN: Optional[str] = os.getenv("GENIUS_API_TOKEN")
    
    # Bot Settings
    AUTO_LEAVE_DURATION: int = int(os.getenv("AUTO_LEAVE_DURATION", "300"))  # 5 minutes
    TEMP_FILE_CLEANUP: int = int(os.getenv("TEMP_FILE_CLEANUP", "3600"))     # 1 hour
    BROADCAST_DELAY: float = float(os.getenv("BROADCAST_DELAY", "0.2"))
    
    # Validation
    @classmethod
    def validate(cls) -> bool:
        """Validate critical config variables"""
        required = [
            cls.BOT_TOKEN,
            cls.API_ID,
            cls.API_HASH,
            cls.MONGO_URI,
            cls.OWNER_ID,
            cls.ASSISTANT_STRING,
            cls.ASSISTANT_ID,
        ]
        return all(required)

# Validate on import
if not Config.validate():
    raise ValueError("❌ Missing critical environment variables! Please check your .env file.")
