from pyrogram import Client, filters, enums
from pyrogram.types import Message, CallbackQuery
from callsmusic import player
from callsmusic.queue import queue_manager
from utils.time import format_duration, generate_progress_bar
from utils.decorators import authorized_only, admin_only, chat_watcher
from strings import Messages
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command(["pause", "resume", "skip", "stop"]) & filters.group)
@authorized_only
@admin_only
@chat_watcher
async def playback_commands(client: Client, message: Message):
    """Handle basic playback commands"""
    chat_id = message.chat.id
    command = message.command[0].lower()
    
    if command == "pause":
        success = await player.pause(chat_id)
        if success:
            await message.reply("⏸ **Paused**")
    
    elif command == "resume":
        success = await player.resume(chat_id)
        if success:
            await message.reply("▶️ **Resumed**")
    
    elif command == "skip":
        next_item = await player.skip(chat_id)
        if next_item:
            await message.reply(f"⏭ **Skipped**\n\nNow playing: {next_item.title}")
        else:
            await message.reply(Messages.QUEUE_EMPTY)
    
    elif command == "stop":
        success = await player.stop(chat_id)
        if success:
            await message.reply("⏹ **Stopped**")

@Client.on_message(filters.command("current") & filters.group)
@authorized_only
@chat_watcher
async def current_command(client: Client, message: Message):
    """Show current playing track with progress"""
    chat_id = message.chat.id
    
    current = queue_manager.get_current(chat_id)
    if not current:
        await message.reply(Messages.NO_SONG_PLAYING)
        return
    
    # Get position
    position = await player.get_position(chat_id)
    duration = current.duration
    
    # Generate progress bar
    progress_bar = generate_progress_bar(position, duration)
    
    status_msg = Messages.PLAYING.format(
        status="▶️ Playing",
        title=current.title,
        duration=f"{format_duration(position)} / {format_duration(duration)}",
        mention=message.from_user.mention,
        source=current.source,
        progress_bar=progress_bar,
        footer=Messages.footer()
    )
    
    await message.reply(status_msg, parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.command("queue") & filters.group)
@authorized_only
@chat_watcher
async def queue_command(client: Client, message: Message):
    """Show queue list"""
    chat_id = message.chat.id
    
    queue = queue_manager.get_queue(chat_id)
    if not queue:
        await message.reply(Messages.QUEUE_EMPTY)
        return
    
    items = []
    for i, item in enumerate(queue[:10], 1):  # Show first 10
        items.append(f"**{i}.** {item.title} ({format_duration(item.duration)})")
    
    queue_text = "\n".join(items)
    if len(queue) > 10:
        queue_text += f"\n\n... and {len(queue) - 10} more"
    
    await message.reply(
        Messages.QUEUE.format(items=queue_text, total=len(queue), footer=Messages.footer()),
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("shuffle") & filters.group)
@authorized_only
@admin_only
@chat_watcher
async def shuffle_command(client: Client, message: Message):
    """Shuffle queue"""
    chat_id = message.chat.id
    
    queue_manager.shuffle_queue(chat_id)
    await message.reply("🔀 **Queue shuffled!**")

@Client.on_message(filters.command("loop") & filters.group)
@authorized_only
@admin_only
@chat_watcher
async def loop_command(client: Client, message: Message):
    """Toggle loop mode"""
    chat_id = message.chat.id
    
    current = queue_manager.is_looping(chat_id)
    new_status = not current
    queue_manager.set_loop(chat_id, new_status)
    
    status = "enabled" if new_status else "disabled"
    await message.reply(f"🔁 **Loop {status}!**")

@Client.on_message(filters.command("volume") & filters.group)
@authorized_only
@admin_only
@chat_watcher
async def volume_command(client: Client, message: Message):
    """Change volume"""
    chat_id = message.chat.id
    
    if len(message.command) < 2:
        await message.reply("❌ Please provide volume level (1-200)")
        return
    
    try:
        volume = int(message.command[1])
        if not 1 <= volume <= 200:
            raise ValueError
        
        success = await player.set_volume(chat_id, volume)
        if success:
            await message.reply(f"🔊 **Volume set to {volume}%**")
    except:
        await message.reply("❌ Invalid volume! Use a number between 1-200")
