# bot.py
import asyncio
from pyrogram import Client
from config.config import BOT_TOKEN, API_ID, API_HASH
from handlers.start import register_handlers as start_handlers
from handlers.play import register_handlers as play_handlers
from handlers.playback import register_handlers as playback_handlers
from handlers.admin import register_handlers as admin_handlers
from handlers.ban import register_handlers as ban_handlers
from handlers.misc import register_handlers as misc_handlers
from assistant import assistant_app, pytgcalls, player

BOT_APP = Client("stark_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def register_all(app):
    start_handlers(app)
    play_handlers(app, player)
    playback_handlers(app, player)
    admin_handlers(app)
    ban_handlers(app)
    misc_handlers(app)

async def main():
    register_all(BOT_APP)
    await BOT_APP.start()
    # assistant already started in assistant.py import
    print("Bot & Assistant started.")
    await asyncio.get_event_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
