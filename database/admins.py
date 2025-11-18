# database/admins.py
from .mongodb import db

class AdminDB:
    col = db.admins

    @classmethod
    async def add_admin(cls, chat_id: int, user_id: int):
        await cls.col.update_one({"chat_id": chat_id}, {"$addToSet": {"admins": user_id}}, upsert=True)

    @classmethod
    async def remove_admin(cls, chat_id: int, user_id: int):
        await cls.col.update_one({"chat_id": chat_id}, {"$pull": {"admins": user_id}})

    @classmethod
    async def is_admin(cls, chat_id: int, user_id: int) -> bool:
        doc = await cls.col.find_one({"chat_id": chat_id})
        if not doc: return False
        return user_id in doc.get("admins", [])
