# handlers/misc.py
from pyrogram import filters
from pyrogram.types import Message
import time

def register_handlers(app):
    @app.on_message(filters.command("ping"))
    async def ping(_, message: Message):
        t = time.time()
        m = await message.reply_text("Pinging...")
        ping_ms = int((time.time() - t) * 1000)
        await m.edit_text(f"Pong! `{ping_ms} ms`")
