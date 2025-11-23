import yt_dlp
import os
import aiofiles
import aiohttp
from typing import Dict, Optional, Tuple
from utils.time import format_duration
import logging

logger = logging.getLogger(__name__)

class YTDLConverter:
    """YouTube Downloader & Converter"""
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'restrictfilenames': True,
    }
    
    @staticmethod
    async def extract_info(url: str) -> Optional[Dict]:
        """Extract video info from URL"""
        try:
            with yt_dlp.YoutubeDL(YTDLConverter.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    return {
                        "title": info.get("title", "Unknown"),
                        "duration": info.get("duration", 0),
                        "url": info.get("url"),
                        "webpage_url": info.get("webpage_url"),
                        "thumbnail": info.get("thumbnail"),
                        "uploader": info.get("uploader", "Unknown"),
                        "source": "youtube"
                    }
        except Exception as e:
            logger.error(f"YTDL Error: {e}")
        return None
    
    @staticmethod
    async def download_audio(url: str) -> Optional[str]:
        """Download audio file"""
        try:
            with yt_dlp.YoutubeDL(YTDLConverter.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if os.path.exists(filename):
                    return filename
        except Exception as e:
            logger.error(f"Download Error: {e}")
        return None
    
    @staticmethod
    async def search_yt(query: str, max_results: int = 5) -> list:
        """Search YouTube videos"""
        search_opts = {
            'skip_download': True,
            'noplaylist': True,
            'extract_flat': True,
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
                if search_results and 'entries' in search_results:
                    results = []
                    for entry in search_results['entries']:
                        results.append({
                            "title": entry.get("title", "Unknown"),
                            "duration": entry.get("duration", 0),
                            "url": f"https://youtube.com/watch?v={entry.get('id')}",
                            "thumbnail": entry.get("thumbnail"),
                            "source": "youtube"
                        })
                    return results
        except Exception as e:
            logger.error(f"Search Error: {e}")
        return []
