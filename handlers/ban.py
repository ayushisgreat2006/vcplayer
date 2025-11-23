from pyrogram import Client, filters
from pyrogram.types import Message
from database.bans import BanDB
from utils.decorators import authorized_only, owner_only, chat_watcher
from strings import Messages
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("globalban"))
@authorized_only
@owner_only
@chat_watcher
async def global_ban(client: Client, message: Message):
    """Globally ban a user"""
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        reason = " ".join(message.command[1:]) or "No reason"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            reason = " ".join(message.command[2:]) or "No reason"
        except:
            await message.reply("❌ Please reply to a user or provide: `/globalban <user_id> [reason]`")
            return
    else:
        await message.reply("❌ Please reply to a user or provide their user ID!")
        return
    
    await BanDB.ban_user(user_id, reason)
    await message.reply(Messages.USER_BANNED.format(user_id=user_id))

@Client.on_message(filters.command("globalunban"))
@authorized_only
@owner_only
@chat_watcher
async def global_unban(client: Client, message: Message):
    """Globally unban a user"""
    if len(message.command) < 2:
        await message.reply("❌ Please provide a user ID: `/globalunban <user_id>`")
        return
    
    try:
        user_id = int(message.command[1])
        await BanDB.unban_user(user_id)
        await message.reply(Messages.USER_UNBANNED.format(user_id=user_id))
    except:
        await message.reply("❌ Invalid user ID!")
