# callsmusic/calls.py
from pytgcalls import PyTgCalls
from pyrogram import Client
from config.config import ASSISTANT_STRING, API_ID, API_HASH, ASSISTANT_ID
from callsmusic.player import Player
import asyncio

def init_calls(assistant_app: Client):
    pytgcalls = PyTgCalls(assistant_app)
    return pytgcalls
