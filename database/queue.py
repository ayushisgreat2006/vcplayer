from database.mongodb import mongo_db
from typing import List, Dict, Any

class QueueDB:
    """Persistent queue storage (for future features like saved playlists)"""
    
    @staticmethod
    async def save_playlist(chat_id: int, name: str, queue_data: List[Dict[str, Any]]):
        """Save a playlist"""
        await mongo_db.db.playlists.insert_one({
            "chat_id": chat_id,
            "name": name,
            "queue": queue_data
        })
    
    @staticmethod
    async def get_playlist(chat_id: int, name: str) -> Dict[str, Any]:
        """Get a saved playlist"""
        return await mongo_db.db.playlists.find_one({"chat_id": chat_id, "name": name})
