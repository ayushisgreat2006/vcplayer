from pyrogram.types import Message, ChatMember
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from config import Config
import logging

logger = logging.getLogger(__name__)

class PermissionChecker:
    """Check bot and user permissions"""
    
    @staticmethod
    async def check_bot_permissions(client, chat_id: int) -> dict:
        """Check what permissions bot has in chat"""
        try:
            bot_member = await client.get_chat_member(chat_id, "me")
            perms = {
                "can_invite_users": bot_member.privileges.can_invite_users if bot_member.privileges else False,
                "can_manage_voice_chats": bot_member.privileges.can_manage_voice_chats if bot_member.privileges else False,
                "can_delete_messages": bot_member.privileges.can_delete_messages if bot_member.privileges else False,
                "is_admin": bot_member.status in ["administrator", "creator"],
            }
            return perms
        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return {
                "can_invite_users": False,
                "can_manage_voice_chats": False,
                "can_delete_messages": False,
                "is_admin": False,
            }
    
    @staticmethod
    async def is_updates_member(client, user_id: int) -> bool:
        """Check if user is member of updates channel"""
        if not Config.UPDATES_CHANNEL:
            return True
        
        try:
            await client.get_chat_member(Config.UPDATES_CHANNEL, user_id)
            return True
        except UserNotParticipant:
            return False
        except Exception as e:
            logger.error(f"Updates channel check error: {e}")
            return True  # Assume true on error to avoid blocking
    
    @staticmethod
    async def get_chat_member_count(client, chat_id: int) -> int:
        """Get total member count of chat"""
        try:
            chat = await client.get_chat(chat_id)
            return chat.members_count
        except:
            return 0
