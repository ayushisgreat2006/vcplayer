from functools import wraps
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from database.admins import AdminDB
from database.bans import BanDB
from config import Config
from utils.permissions import PermissionChecker
import logging

logger = logging.getLogger(__name__)

def authorized_only(func):
    """Block banned users and check updates channel"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        
        # Check global ban
        is_banned, reason = await BanDB.is_banned(user_id)
        if is_banned:
            await message.reply(f"🚫 You are globally banned!\nReason: {reason}")
            return
        
        # Check updates channel
        if not await PermissionChecker.is_updates_member(client, user_id):
            channel = Config.UPDATES_CHANNEL
            await message.reply(
                f"⚠️ **You must join our updates channel to use this bot!**\n\n"
                f"📢 @{channel}\n\n"
                f"After joining, try again.",
                reply_markup=decorators_buttons.updates_channel(channel)
            )
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper

def admin_only(func):
    """Allow only admins and owner"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        if user_id == Config.OWNER_ID:
            return await func(client, message, *args, **kwargs)
        
        if not await AdminDB.is_admin(chat_id, user_id):
            await message.reply("🚫 This command is for admins only!")
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper

def owner_only(func):
    """Allow only owner"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        
        if user_id != Config.OWNER_ID:
            await message.reply("🚫 This command is for the bot owner only!")
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper

def bot_admin_required(func):
    """Check if bot has admin privileges"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        chat_id = message.chat.id
        
        perms = await PermissionChecker.check_bot_permissions(client, chat_id)
        
        missing = []
        if not perms["can_invite_users"]:
            missing.append("❌ Invite Users permission")
        if not perms["can_manage_voice_chats"]:
            missing.append("❌ Manage Voice Chats permission")
        
        if missing:
            await message.reply(
                "⚠️ **Bot is missing required permissions!**\n\n"
                + "\n".join(missing) + "\n\n"
                "Please make the bot an admin with these permissions.",
                quote=True
            )
            return
        
        return await func(client, message, *args, **kwargs)
    return wrapper

def chat_watcher(func):
    """Track chats for broadcast"""
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if message.chat:
            chat_type = message.chat.type.value
            await ChatDB.add_chat(message.chat.id, chat_type)
        
        if message.from_user:
            await ChatDB.add_chat(message.from_user.id, "private")
        
        return await func(client, message, *args, **kwargs)
    return wrapper

# Import buttons after function definitions to avoid circular import
from utils import buttons as decorators_buttons
