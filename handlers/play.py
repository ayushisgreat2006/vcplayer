# handlers/play.py
from pyrogram import filters
from pyrogram.types import Message
from utils.ytsearch import search_youtube
from utils.decorators import check_banned
from strings.messages import NO_RESULT
from callsmusic.player import Player

def register_handlers(app, player: Player):
    @app.on_message(filters.command("play") & ~filters.edited)
    @check_banned
    async def play_cmd(_, message: Message):
        if not message.command or len(message.command) < 2:
            await message.reply_text("Usage: /play <song name or youtube url>")
            return
        query = " ".join(message.command[1:])
        info = await search_youtube(query)
        if not info:
            await message.reply_text(NO_RESULT)
            return
        chat_id = message.chat.id
        requester = message.from_user.id
        # hand to player
        await player.ensure_join_and_play(chat_id, requester, info, message)
