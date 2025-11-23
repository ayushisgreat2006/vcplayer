import asyncio
import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from callsmusic import player, QueueItem
from utils.ytsearch import YouTubeSearch
from utils.ytdl import YouTubeDL
from utils.decorators import authorized_only, bot_admin_required, chat_watcher
from utils.permissions import PermissionChecker
from strings import Messages
from database.admins import AdminDB
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("play") & filters.group)
@authorized_only
@bot_admin_required
@chat_watcher
async def play_command(client: Client, message: Message):
    """Handle /play command with auto-invite"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if assistant is in chat
    try:
        await client.get_chat_member(chat_id, Config.ASSISTANT_ID)
        assistant_in_chat = True
    except:
        assistant_in_chat = False
    
    # Invite assistant if not present
    if not assistant_in_chat:
        msg = await message.reply(Messages.ASSISTANT_INVITING)
        
        # Check bot permissions
        perms = await PermissionChecker.check_bot_permissions(client, chat_id)
        
        if not perms["can_invite_users"]:
            await msg.edit(Messages.BOT_NOT_ADMIN.format(missing="❌ Invite Users permission"))
            return
        
        try:
            # Generate invite link
            invite_link = await client.create_chat_invite_link(chat_id)
            
            # Assistant joins via User client
            from callsmusic import assistant_client
            await assistant_client.join_chat(invite_link.invite_link)
            
            await asyncio.sleep(3)  # Wait for assistant to join
            
            assistant_in_chat = True
            await msg.edit(Messages.ASSISTANT_JOINED)
        except Exception as e:
            logger.error(f"Assistant invite error: {e}")
            await msg.edit(Messages.ASSISTANT_FAILED, reply_markup=buttons.updates_channel(Config.UPDATES_CHANNEL))
            return
    
    # Parse query
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply("❌ Please provide a song name or reply to an audio file!")
        return
    
    # Get query
    query = ""
    if len(message.command) > 1:
        query = " ".join(message.command[1:])
    elif message.reply_to_message:
        if message.reply_to_message.audio:
            query = message.reply_to_message.audio.file_id
    
    # Process based on input type
    if query.startswith("http"):  # URL
        await process_url(client, message, query, user_id, chat_id)
    elif query:  # Search query
        await process_search(client, message, query, user_id, chat_id)
    else:
        await message.reply("❌ Invalid input!")

async def process_url(client: Client, message: Message, url: str, user_id: int, chat_id: int):
    """Process YouTube URL"""
    processing = await message.reply("🔍 Processing YouTube URL...")
    
    try:
        info = await YouTubeSearch.get_video_info(url)
        if not info:
            await processing.edit("❌ Failed to fetch video info!")
            return
        
        # Create queue item
        item = QueueItem(
            title=info["title"],
            duration=info["duration"],
            file_path=None,
            stream_url=info["url"],
            requester=user_id,
            thumbnail=info["thumbnail"],
            source=info["source"],
            webpage_url=info["webpage_url"]
        )
        
        # Check if we need to join VC first
        if not await player.join_vc(chat_id):
            await processing.edit("❌ Failed to join voice chat!")
            return
        
        # Play or queue
        position = await player.play(chat_id, item)
        
        if position == 0:
            await processing.edit(
                Messages.PLAYING.format(
                    status="▶️ Playing",
                    title=item.title,
                    duration=format_duration(item.duration),
                    mention=message.from_user.mention,
                    source=item.source,
                    progress_bar="▰▰▰▰▰▰▰▰▰▰",
                    footer=Messages.footer()
                ),
                reply_markup=buttons.player_controls()
            )
        else:
            await processing.edit(
                f"✅ **Added to queue** at position #{position}\n\n"
                f"🎵 {item.title}\n"
                f"⏱ {format_duration(item.duration)}\n"
                f"👤 {message.from_user.mention}"
            )
    
    except Exception as e:
        logger.error(f"URL processing error: {e}")
        await processing.edit(f"❌ Error: {str(e)}")

async def process_search(client: Client, message: Message, query: str, user_id: int, chat_id: int):
    """Process search query"""
    searching = await message.reply(f"🔍 Searching for \"{query}\"...")
    
    try:
        results = await YouTubeSearch.search(query)
        
        if not results:
            await searching.edit("❌ No results found!")
            return
        
        # Auto-play first result
        info = results[0]
        
        item = QueueItem(
            title=info["title"],
            duration=info["duration"],
            file_path=None,
            stream_url=info["url"],
            requester=user_id,
            thumbnail=info["thumbnail"],
            source=info["source"],
            webpage_url=info["webpage_url"]
        )
        
        # Join VC if needed
        if not await player.join_vc(chat_id):
            await searching.edit("❌ Failed to join voice chat!")
            return
        
        # Play or queue
        position = await player.play(chat_id, item)
        
        if position == 0:
            await searching.edit(
                Messages.PLAYING.format(
                    status="▶️ Playing",
                    title=item.title,
                    duration=format_duration(item.duration),
                    mention=message.from_user.mention,
                    source=item.source,
                    progress_bar="▰▰▰▰▰▰▰▰▰▰",
                    footer=Messages.footer()
                ),
                reply_markup=buttons.player_controls()
            )
        else:
            await searching.edit(
                f"✅ **Added to queue** at position #{position}\n\n"
                f"🎵 {item.title}\n"
                f"⏱ {format_duration(item.duration)}\n"
                f"👤 {message.from_user.mention}"
            )
    
    except Exception as e:
        logger.error(f"Search processing error: {e}")
        await searching.edit(f"❌ Error: {str(e)}")

@Client.on_inline_query()
async def inline_search(client: Client, inline_query: InlineQuery):
    """Handle inline search"""
    query = inline_query.query
    
    if not query:
        await inline_query.answer([], switch_pm_text="Type a song name...", switch_pm_parameter="help")
        return
    
    results = await YouTubeSearch.search(query, max_results=5)
    
    inline_results = []
    for i, result in enumerate(results):
        inline_results.append(
            InlineQueryResultArticle(
                title=result["title"],
                description=f"{format_duration(result['duration'])} | {result['source']}",
                thumb_url=result["thumbnail"],
                input_message_content=InputTextMessageContent(
                    f"/play {result['webpage_url']}"
                )
            )
        )
    
    await inline_query.answer(inline_results, cache_time=10)
