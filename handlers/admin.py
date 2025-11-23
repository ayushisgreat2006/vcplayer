from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.admins import AdminDB
from utils.decorators import authorized_only, admin_only, owner_only, chat_watcher
from strings import Messages
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("addadmin") & filters.group)
@authorized_only
@owner_only
@chat_watcher
async def add_admin(client: Client, message: Message):
    """Add bot admin to a group"""
    chat_id = message.chat.id
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply("❌ Please reply to a user or provide their user ID!")
            return
    else:
        await message.reply("❌ Please reply to a user or provide their user ID!")
        return
    
    await AdminDB.add_admin(chat_id, user_id)
    await message.reply(Messages.ADMIN_ADDED.format(user_id=user_id))

@Client.on_message(filters.command("deladmin") & filters.group)
@authorized_only
@owner_only
@chat_watcher
async def del_admin(client: Client, message: Message):
    """Remove bot admin from a group"""
    chat_id = message.chat.id
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply("❌ Please reply to a user or provide their user ID!")
            return
    else:
        await message.reply("❌ Please reply to a user or provide their user ID!")
        return
    
    await AdminDB.remove_admin(chat_id, user_id)
    await message.reply(Messages.ADMIN_REMOVED.format(user_id=user_id))

@Client.on_message(filters.command("clearqueue") & filters.group)
@authorized_only
@admin_only
@chat_watcher
async def clear_queue(client: Client, message: Message):
    """Clear the queue"""
    from callsmusic import queue_manager
    
    chat_id = message.chat.id
    queue_manager.clear_queue(chat_id)
    await message.reply(Messages.QUEUE_CLEARED)

@Client.on_message(filters.command("syncadmins") & filters.group)
@authorized_only
@owner_only
@chat_watcher
async def sync_admins(client: Client, message: Message):
    """Sync admins from Telegram"""
    chat_id = message.chat.id
    
    # Get all chat admins
    admins = []
    async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if not member.user.is_bot:
            admins.append(member.user.id)
    
    # Sync to DB
    added = await AdminDB.sync_group_admins(chat_id, admins)
    await message.reply(f"✅ Synced {added} new admins from Telegram!")
