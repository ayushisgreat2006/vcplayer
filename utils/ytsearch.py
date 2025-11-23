from callsmusic.converter import YTDLConverter
from typing import List, Dict

class YouTubeSearch:
    """YouTube search utility"""
    
    @staticmethod
    async def search(query: str, max_results: int = 5) -> List[Dict]:
        """Search YouTube and return results"""
        results = await YTDLConverter.search_yt(query, max_results)
        return results
    
    @staticmethod
    async def get_video_info(url: str) -> Dict:
        """Get detailed video info from URL"""
        info = await YTDLConverter.extract_info(url)
        return info
