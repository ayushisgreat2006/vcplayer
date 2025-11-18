# database/chats.py
from .mongodb import db

class ChatsDB:
    col = db.chats

    @classmethod
    async def add_chat(cls, chat_id: int):
        await cls.col.update_one({"chat_id": chat_id}, {"$setOnInsert": {"chat_id": chat_id}}, upsert=True)

    @classmethod
    async def get_all_chats(cls):
        return await cls.col.find().to_list(length=None)
