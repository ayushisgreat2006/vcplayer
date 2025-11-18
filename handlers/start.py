# handlers/start.py
from pyrogram import filters
from pyrogram.types import Message
from strings.messages import START
from config.config import BOT_TOKEN

def register_handlers(app):
    @app.on_message(filters.command("start") & ~filters.edited)
    async def start(_, message: Message):
        await message.reply_text(START)
