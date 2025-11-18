# assistant.py
import asyncio
from pyrogram import Client
from config.config import ASSISTANT_STRING, API_ID, API_HASH, ASSISTANT_ID
from callsmusic.calls import init_calls
from callsmusic.player import Player

if not ASSISTANT_STRING:
    raise RuntimeError("ASSISTANT_STRING not set in env")

assistant_app = Client("stark_assistant", api_id=API_ID, api_hash=API_HASH, session_string=ASSISTANT_STRING)
pytgcalls = None
player = None

async def start_assistant():
    global pytgcalls, player
    await assistant_app.start()
    pytgcalls = init_calls(assistant_app)
    pytgcalls.start()
    # create Player
    player = Player(assistant_app, pytgcalls)
    print("Assistant started.")

# start in background when imported by bot.py
loop = asyncio.get_event_loop()
loop.create_task(start_assistant())
