# database/mongodb.py
import motor.motor_asyncio
from config.config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["starkmusic"]
