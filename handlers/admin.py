# handlers/admin.py
from pyrogram import filters
from pyrogram.types import Message
from utils.decorators import owner_only
from database.admins import AdminDB

def register_handlers(app):
    @app.on_message(filters.command("addadmin"))
    @owner_only
    async def add_admin(_, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /addadmin <user_id>")
            return
        uid = int(message.command[1])
        await AdminDB.add_admin(message.chat.id, uid)
        await message.reply_text(f"✅ Added {uid} as admin for this chat.")

    @app.on_message(filters.command("deladmin"))
    @owner_only
    async def del_admin(_, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /deladmin <user_id>")
            return
        uid = int(message.command[1])
        await AdminDB.remove_admin(message.chat.id, uid)
        await message.reply_text(f"✅ Removed {uid} from admins for this chat.")
