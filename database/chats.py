from database.mongodb import mongo_db

class ChatDB:
    """Chat management for broadcast"""
    
    @staticmethod
    async def add_chat(chat_id: int, chat_type: str):
        """Add chat to database"""
        await mongo_db.db.chats.update_one(
            {"chat_id": chat_id},
            {"$set": {"type": chat_type}},
            upsert=True
        )
    
    @staticmethod
    async def get_all_chats(chat_type: str = None) -> list:
        """Get all chats"""
        filter_dict = {}
        if chat_type:
            filter_dict["type"] = chat_type
        
        cursor = mongo_db.db.chats.find(filter_dict)
        return [doc["chat_id"] async for doc in cursor]
    
    @staticmethod
    async def get_stats():
        """Get database stats"""
        total_chats = await mongo_db.db.chats.count_documents({})
        total_users = await mongo_db.db.chats.count_documents({"type": "private"})
        total_groups = await mongo_db.db.chats.count_documents({"type": {"$in": ["group", "supergroup"]}})
        
        return {
            "chats": total_chats,
            "users": total_users,
            "groups": total_groups
        }
