# utils/ytdl.py
import os
import asyncio
from yt_dlp import YoutubeDL
from config.config import DOWNLOADS, YTDL_FORMAT

YDL_OPTS = {
    "format": YTDL_FORMAT,
    "outtmpl": os.path.join(DOWNLOADS, "%(id)s.%(ext)s"),
    "nocheckcertificate": True,
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
    "noplaylist": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}

async def extract_info(url_or_query: str):
    loop = asyncio.get_event_loop()
    def _extract():
        with YoutubeDL({"format": "bestaudio/best", "quiet": True}) as ydl:
            # If looks like URL -> download info; else search
            if url_or_query.startswith("http"):
                info = ydl.extract_info(url_or_query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch1:{url_or_query}", download=False)['entries'][0]
            return info
    return await loop.run_in_executor(None, _extract)

async def download_audio(info: dict):
    loop = asyncio.get_event_loop()
    def _download():
        with YoutubeDL(YDL_OPTS) as ydl:
            res = ydl.extract_info(info.get("webpage_url") or info.get("url"), download=True)
            # res contains keys id, ext
            filename = ydl.prepare_filename(res)
            return filename, res
    return await loop.run_in_executor(None, _download)
