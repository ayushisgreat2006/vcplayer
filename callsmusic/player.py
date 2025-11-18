# callsmusic/player.py
import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types import Update
from utils.ytdl import download_audio, extract_info
from callsmusic.converter import ensure_wav
from callsmusic.queue import ChatQueue
from config.config import ASSISTANT_ID
from utils.time import seconds_to_time

class Player:
    def __init__(self, assistant_app: Client, pytgcalls: PyTgCalls):
        self.assistant_app = assistant_app
        self.pytgcalls = pytgcalls
        self.playing = {}  # chat_id -> current item
        self.lock = asyncio.Lock()
        # register handlers
        self.pytgcalls.add_handler(self._on_left)

    async def _on_left(self, update):
        # handle ended or left
        pass

    async def ensure_join_and_play(self, chat_id: int, requester_id: int, info: dict, message):
        """
        Push to queue, join VC if required, and start play cycle
        """
        # push to queue
        item = {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),
            "thumbnail": info.get("thumbnail"),
            "requester": requester_id,
            "id": info.get("id"),
            "file": None
        }
        await ChatQueue.push(chat_id, item)
        await message.reply_text(f"➕ Added **{item['title']}** to queue.")
        # if not playing, start
        if chat_id not in self.playing:
            asyncio.create_task(self._play_loop(chat_id, message))

    async def _play_loop(self, chat_id: int, message):
        async with self.lock:
            while True:
                queued = await ChatQueue.list(chat_id)
                if not queued:
                    # leave vc if active
                    try:
                        await self.pytgcalls.leave_group_call(chat_id)
                    except Exception:
                        pass
                    if chat_id in self.playing:
                        del self.playing[chat_id]
                    await message.reply_text("📭 Queue finished. Leaving VC.")
                    break
                # pop next
                item = await ChatQueue.pop(chat_id)
                # get info/download
                info = await extract_info(item["webpage_url"])
                fname, res = await download_audio(info)
                path = await ensure_wav(fname)
                item["file"] = path
                self.playing[chat_id] = item
                # join vc & play
                try:
                    # join or change stream
                    await self.pytgcalls.join_group_call(
                        chat_id,
                        AudioPiped(path),
                    )
                    await message.reply_text(f"▶️ Now playing: **{item['title']}** — `{seconds_to_time(item['duration'])}`")
                    # block until finished by checking stream status: naive sleep duration
                    await asyncio.sleep(item.get("duration", 0) + 1)
                except Exception as e:
                    await message.reply_text(f"Error playing: {e}")
                # continue loop to next
            # end while
