from pyrogram import Client
from pytgcalls import PyTgCalls
from config import Config
import logging

logger = logging.getLogger(__name__)

# Assistant Client for PyTgCalls
assistant_client = Client(
    "stark_assistant",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.ASSISTANT_STRING,
    in_memory=True
)

# PyTgCalls instance
call_py = PyTgCalls(assistant_client)

class CallManager:
    """Manages active voice calls"""
    
    active_calls = {}  # chat_id -> call data
    
    @staticmethod
    async def start():
        """Start PyTgCalls client"""
        await call_py.start()
        logger.info("🎵 PyTgCalls client started")
    
    @staticmethod
    async def stop():
        """Stop PyTgCalls client"""
        await call_py.stop()
        logger.info("🎵 PyTgCalls client stopped")
    
    @staticmethod
    def get_call(chat_id: int):
        """Get call instance for chat"""
        return call_py.get_active_call(chat_id)
