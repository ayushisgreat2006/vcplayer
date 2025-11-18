# database/bans.py
from .mongodb import db

class BanDB:
    col = db.global_bans

    @classmethod
    async def add_ban(cls, user_id: int):
        await cls.col.update_one({"_id": "global"}, {"$addToSet": {"banned": user_id}}, upsert=True)

    @classmethod
    async def remove_ban(cls, user_id: int):
        await cls.col.update_one({"_id": "global"}, {"$pull": {"banned": user_id}})

    @classmethod
    async def is_banned(cls, user_id: int) -> bool:
        doc = await cls.col.find_one({"_id": "global"})
        if not doc: return False
        return user_id in doc.get("banned", [])
