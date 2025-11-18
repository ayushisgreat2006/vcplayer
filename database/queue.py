# database/queue.py
from .mongodb import db

class QueueDB:
    col = db.queue

    @classmethod
    async def push(cls, chat_id: int, item: dict):
        await cls.col.update_one({"chat_id": chat_id}, {"$push": {"queue": item}}, upsert=True)

    @classmethod
    async def pop(cls, chat_id: int):
        doc = await cls.col.find_one({"chat_id": chat_id})
        if not doc or not doc.get("queue"):
            return None
        item = doc["queue"].pop(0)
        await cls.col.update_one({"chat_id": chat_id}, {"$set": {"queue": doc["queue"]}})
        return item

    @classmethod
    async def get_all(cls, chat_id: int):
        doc = await cls.col.find_one({"chat_id": chat_id})
        return doc.get("queue", []) if doc else []
    
    @classmethod
    async def clear(cls, chat_id: int):
        await cls.col.update_one({"chat_id": chat_id}, {"$set": {"queue": []}})
