# utils/decorators.py
from functools import wraps
from database.bans import BanDB
from config.config import OWNER_ID

def check_banned(func):
    @wraps(func)
    async def wrapper(_, message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else None
        if user_id and await BanDB.is_banned(user_id):
            await message.reply_text("🚫 You are globally banned.")
            return
        return await func(_, message, *args, **kwargs)
    return wrapper

def owner_only(func):
    @wraps(func)
    async def wrapper(bot, message, *args, **kwargs):
        user = message.from_user
        if not user or user.id != OWNER_ID:
            await message.reply_text("⛔ Owner only.")
            return
        return await func(bot, message, *args, **kwargs)
    return wrapper
