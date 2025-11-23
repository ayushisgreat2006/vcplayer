from callsmusic.converter import YTDLConverter
from typing import Optional

class YouTubeDL:
    """YouTube download wrapper"""
    
    @staticmethod
    async def get_stream_url(url: str) -> Optional[str]:
        """Get direct stream URL without downloading"""
        info = await YTDLConverter.extract_info(url)
        return info.get("url") if info else None
    
    @staticmethod
    async def download(url: str) -> Optional[str]:
        """Download audio file"""
        return await YTDLConverter.download_audio(url)
