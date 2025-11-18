# config/config.py
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ASSISTANT_STRING = os.getenv("ASSISTANT_STRING", None)  # user session string
ASSISTANT_ID = int(os.getenv("ASSISTANT_ID", "0"))

# local storage for downloaded audio
DOWNLOADS = os.getenv("DOWNLOADS", "downloads")
os.makedirs(DOWNLOADS, exist_ok=True)

# yt-dlp options
YTDL_FORMAT = "bestaudio/best"
FFMPEG_OPTIONS = "-vn -af aformat=s16:44100 -ar 44100 -ac 2"
