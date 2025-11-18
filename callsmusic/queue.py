# callsmusic/queue.py
from typing import List, Dict
from database.queue import QueueDB

class ChatQueue:
    """
    Lightweight in-memory queue with DB persistence.
    """
    _mem = {}  # chat_id -> list

    @classmethod
    async def push(cls, chat_id: int, item: dict):
        cls._mem.setdefault(chat_id, []).append(item)
        await QueueDB.push(chat_id, item)

    @classmethod
    async def pop(cls, chat_id: int):
        if chat_id in cls._mem and cls._mem[chat_id]:
            item = cls._mem[chat_id].pop(0)
            await QueueDB.pop(chat_id)
            return item
        item = await QueueDB.pop(chat_id)
        return item

    @classmethod
    async def list(cls, chat_id: int):
        mem = cls._mem.get(chat_id)
        if mem is not None:
            return mem
        return await QueueDB.get_all(chat_id)

    @classmethod
    async def clear(cls, chat_id: int):
        cls._mem[chat_id] = []
        await QueueDB.clear(chat_id)
