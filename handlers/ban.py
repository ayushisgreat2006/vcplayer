# handlers/ban.py
from pyrogram import filters
from pyrogram.types import Message
from utils.decorators import owner_only
from database.bans import BanDB

def register_handlers(app):
    @app.on_message(filters.command("globalban"))
    @owner_only
    async def global_ban(_, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /globalban <user_id>")
            return
        uid = int(message.command[1])
        await BanDB.add_ban(uid)
        await message.reply_text(f"🚫 Globally banned {uid}.")

    @app.on_message(filters.command("globalunban"))
    @owner_only
    async def global_unban(_, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /globalunban <user_id>")
            return
        uid = int(message.command[1])
        await BanDB.remove_ban(uid)
        await message.reply_text(f"✅ Globally unbanned {uid}.")
