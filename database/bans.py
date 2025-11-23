from database.mongodb import mongo_db

class BanDB:
    """Global ban management"""
    
    @staticmethod
    async def ban_user(user_id: int, reason: str = "No reason") -> bool:
        """Globally ban a user"""
        await mongo_db.db.bans.insert_one({
            "user_id": user_id,
            "reason": reason
        })
        return True
    
    @staticmethod
    async def unban_user(user_id: int) -> bool:
        """Globally unban a user"""
        result = await mongo_db.db.bans.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    
    @staticmethod
    async def is_banned(user_id: int) -> tuple[bool, str]:
        """Check if user is banned"""
        doc = await mongo_db.db.bans.find_one({"user_id": user_id})
        if doc:
            return True, doc.get("reason", "No reason")
        return False, ""
