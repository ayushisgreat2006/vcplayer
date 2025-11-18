# callsmusic/converter.py
import asyncio
import os
from config.config import DOWNLOADS

async def ensure_wav(file_path: str) -> str:
    """
    Convert to .raw or .mp3 compatible with PyTgCalls (we stream .raw or direct file).
    For simplicity, we keep as mp3 (AudioPiped supports mp3).
    """
    if file_path.endswith(".mp3") or file_path.endswith(".m4a") or file_path.endswith(".wav"):
        return file_path
    mp3_path = os.path.splitext(file_path)[0] + ".mp3"
    if os.path.exists(mp3_path):
        return mp3_path
    cmd = f'ffmpeg -y -i "{file_path}" -vn -ab 128k -ar 44100 -ac 2 "{mp3_path}"'
    proc = await asyncio.create_subprocess_shell(cmd)
    await proc.communicate()
    return mp3_path
