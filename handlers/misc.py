import time
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.chats import ChatDB
from database.admins import AdminDB
from utils.decorators import authorized_only, owner_only, admin_only, chat_watcher
from strings import Messages
from callsmusic import player
from utils.time import format_duration
import aiofiles
import os
import logging

logger = logging.getLogger(__name__)

# Store start time for uptime calculation
START_TIME = time.time()

@Client.on_message(filters.command("ping"))
@authorized_only
@chat_watcher
async def ping_command(client: Client, message: Message):
    """Check bot latency"""
    start = time.time()
    reply = await message.reply("🔄 Checking ping...")
    end = time.time()
    
    ms = int((end - start) * 1000)
    await reply.edit(Messages.PING.format(ms=ms))

@Client.on_message(filters.command("lyrics"))
@authorized_only
@chat_watcher
async def lyrics_command(client: Client, message: Message):
    """Fetch song lyrics"""
    if len(message.command) < 2:
        # Try to get current playing song
        chat_id = message.chat.id
        current = player.queue.get_current(chat_id)
        if current:
            query = current.title
        else:
            await message.reply("❌ Please provide a song name: `/lyrics <song>`")
            return
    else:
        query = " ".join(message.command[1:])
    
    try:
        # Use lyricsgenius if available
        if Config.GENIUS_API_TOKEN:
            import lyricsgenius
            genius = lyricsgenius.Genius(Config.GENIUS_API_TOKEN)
            song = genius.search_song(query)
            
            if song:
                lyrics = song.lyrics[:4000]  # Telegram limit
                await message.reply(f"📜 **Lyrics for {song.title}**\n\n{lyrics}")
                return
        
        # Fallback to basic search
        await message.reply(Messages.LYRICS_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Lyrics error: {e}")
        await message.reply(Messages.LYRICS_NOT_FOUND)

@Client.on_message(filters.command("help"))
@authorized_only
@chat_watcher
async def help_command(client: Client, message: Message):
    """Show help menu"""
    await message.reply(
        Messages.HELP.format(footer=Messages.footer()),
        reply_markup=buttons.help_menu(),
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("stats"))
@authorized_only
@owner_only
@chat_watcher
async def stats_command(client: Client, message: Message):
    """Show bot statistics"""
    stats = await ChatDB.get_stats()
    
    uptime = int(time.time() - START_TIME)
    uptime_str = format_duration(uptime)
    
    await message.reply(
        Messages.STATS.format(
            users=stats["users"],
            groups=stats["groups"],
            active=len(player.queue.queues),
            uptime=uptime_str,
            footer=Messages.footer()
        ),
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("broadcast") & filters.private)
@authorized_only
@owner_only
@chat_watcher
async def broadcast_command(client: Client, message: Message):
    """Broadcast message to all users and groups"""
    if not message.reply_to_message:
        await message.reply("📡 **Broadcast Mode**\n\nSend me any message (text, photo, video, audio, document) and I'll broadcast it to all users and groups.\n\nReply to a message with /broadcast to start.")
        return
    
    confirm = await message.reply(Messages.BROADCAST_START)
    
    # Get all chats
    all_chats = await ChatDB.get_all_chats()
    
    success = 0
    failed = 0
    
    broadcast_msg = message.reply_to_message
    
    for chat_id in all_chats:
        try:
            await
