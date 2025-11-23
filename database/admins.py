from database.mongodb import mongo_db
from typing import List, Optional

class AdminDB:
    """Admin management in MongoDB"""
    
    @staticmethod
    async def add_admin(chat_id: int, user_id: int) -> bool:
        """Add admin to a chat"""
        await mongo_db.db.admins.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"admin_ids": user_id}},
            upsert=True
        )
        return True
    
    @staticmethod
    async def remove_admin(chat_id: int, user_id: int) -> bool:
        """Remove admin from a chat"""
        await mongo_db.db.admins.update_one(
            {"chat_id": chat_id},
            {"$pull": {"admin_ids": user_id}}
        )
        return True
    
    @staticmethod
    async def get_admins(chat_id: int) -> List[int]:
        """Get all admin IDs for a chat"""
        doc = await mongo_db.db.admins.find_one({"chat_id": chat_id})
        if doc:
            return doc.get("admin_ids", [])
        return []
    
    @staticmethod
    async def is_admin(chat_id: int, user_id: int) -> bool:
        """Check if user is admin in chat"""
        admins = await AdminDB.get_admins(chat_id)
        return user_id in admins or user_id == Config.OWNER_ID
    
    @staticmethod
    async def sync_group_admins(chat_id: int, admin_ids: List[int]) -> int:
        """Sync admins from Telegram group"""
        existing = await AdminDB.get_admins(chat_id)
        new_admins = [uid for uid in admin_ids if uid not in existing]
        
        if new_admins:
            await mongo_db.db.admins.update_one(
                {"chat_id": chat_id},
                {"$addToSet": {"admin_ids": {"$each": new_admins}}},
                upsert=True
            )
        return len(new_admins)
