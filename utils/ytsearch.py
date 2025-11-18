# utils/ytsearch.py
from .ytdl import extract_info

async def search_youtube(query: str):
    info = await extract_info(query)
    if not info:
        return None
    return {
        "title": info.get("title"),
        "webpage_url": info.get("webpage_url") or info.get("url"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "id": info.get("id"),
        "uploader": info.get("uploader")
    }
