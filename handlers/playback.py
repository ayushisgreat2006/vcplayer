# handlers/playback.py
from pyrogram import filters
from pyrogram.types import Message
from utils.decorators import check_banned
from callsmusic.queue import ChatQueue

def register_handlers(app, player):
    @app.on_message(filters.command("pause"))
    @check_banned
    async def pause(_, message: Message):
        try:
            await player.pytgcalls.pause_stream(message.chat.id)
            await message.reply_text("⏸️ Paused.")
        except Exception as e:
            await message.reply_text(f"Error: {e}")

    @app.on_message(filters.command("resume"))
    @check_banned
    async def resume(_, message: Message):
        try:
            await player.pytgcalls.resume_stream(message.chat.id)
            await message.reply_text("▶️ Resumed.")
        except Exception as e:
            await message.reply_text(f"Error: {e}")

    @app.on_message(filters.command("skip"))
    @check_banned
    async def skip(_, message: Message):
        try:
            # stopping current stream will make loop play next
            await player.pytgcalls.leave_group_call(message.chat.id)
            await message.reply_text("⏭️ Skipped.")
            # leaving might end; player loop will rejoin next track
        except Exception as e:
            await message.reply_text(f"Error: {e}")

    @app.on_message(filters.command("stop"))
    @check_banned
    async def stop(_, message: Message):
        try:
            await ChatQueue.clear(message.chat.id)
            await player.pytgcalls.leave_group_call(message.chat.id)
            await message.reply_text("⏹️ Stopped and cleared queue.")
        except Exception as e:
            await message.reply_text(f"Error: {e}")

    @app.on_message(filters.command("queue"))
    @check_banned
    async def queue_cmd(_, message: Message):
        q = await ChatQueue.list(message.chat.id)
        if not q:
            await message.reply_text("📭 Queue is empty.")
            return
        txt = "🎶 Queue:\n"
        for i, item in enumerate(q, start=1):
            txt += f"{i}. {item.get('title')} — {item.get('duration')}s\n"
        await message.reply_text(txt)
