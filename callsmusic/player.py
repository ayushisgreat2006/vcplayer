from callsmusic.calls import call_py
from callsmusic.queue import QueueManager, QueueItem
from utils.time import format_duration
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import LeaveGroupCall
from pyrogram.raw.types import InputGroupCall
import os
import logging

logger = logging.getLogger(__name__)

class MusicPlayer:
    """Main music player controller"""
    
    def __init__(self, queue_manager: QueueManager):
        self.queue = queue_manager
    
    async def join_vc(self, chat_id: int):
        """Join voice chat"""
        try:
            await call_py.join_group_call(
                chat_id,
                None,  # Will be set when playing
                stream_type=1  # Video | Audio
            )
            logger.info(f"🔊 Joined VC in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to join VC: {e}")
            return False
    
    async def leave_vc(self, chat_id: int):
        """Leave voice chat"""
        try:
            await call_py.leave_group_call(chat_id)
            self.queue.remove_chat(chat_id)
            logger.info(f"🔇 Left VC in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to leave VC: {e}")
            return False
    
    async def play(self, chat_id: int, item: QueueItem):
        """Play a track"""
        try:
            # If already playing, just add to queue
            if self.queue.get_current(chat_id):
                position = self.queue.add_to_queue(chat_id, item)
                return position
            
            # Play directly
            await self._start_playback(chat_id, item)
            return 0
        except Exception as e:
            logger.error(f"Play error: {e}")
            raise
    
    async def _start_playback(self, chat_id: int, item: QueueItem):
        """Internal playback starter"""
        try:
            # Update current track
            self.queue.set_current(chat_id, item)
            
            # Get audio source
            audio_source = item.stream_url
            
            # Start playing
            await call_py.change_stream(
                chat_id,
                audio_source
            )
            
            logger.info(f"🎵 Now playing: {item.title}")
        except Exception as e:
            logger.error(f"Playback start error: {e}")
            raise
    
    async def pause(self, chat_id: int):
        """Pause playback"""
        try:
            await call_py.pause_stream(chat_id)
            logger.info(f"⏸ Paused in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Pause error: {e}")
            return False
    
    async def resume(self, chat_id: int):
        """Resume playback"""
        try:
            await call_py.resume_stream(chat_id)
            logger.info(f"▶️ Resumed in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Resume error: {e}")
            return False
    
    async def skip(self, chat_id: int):
        """Skip current track"""
        try:
            next_item = self.queue.get_next(chat_id)
            
            if next_item:
                await self._start_playback(chat_id, next_item)
                return next_item
            else:
                # Queue empty
                await self.stop(chat_id)
                return None
        except Exception as e:
            logger.error(f"Skip error: {e}")
            return False
    
    async def stop(self, chat_id: int):
        """Stop playback and clear queue"""
        try:
            await call_py.leave_group_call(chat_id)
            self.queue.clear_queue(chat_id)
            self.queue.set_current(chat_id, None)
            logger.info(f"⏹ Stopped in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Stop error: {e}")
            return False
    
    async def seek(self, chat_id: int, seconds: int):
        """Seek to position (requires re-downloading)"""
        # Note: PyTgCalls seek is complex, this is a simplified version
        # In production, you'd need to get the file, cut it, and re-stream
        try:
            current = self.queue.get_current(chat_id)
            if not current:
                return False
            
            # This is a placeholder - real implementation needs more work
            logger.warning("Seek not fully implemented - requires stream manipulation")
            return False
        except Exception as e:
            logger.error(f"Seek error: {e}")
            return False
    
    async def set_volume(self, chat_id: int, volume: int):
        """Set playback volume"""
        try:
            await call_py.change_volume_call(chat_id, volume)
            logger.info(f"🔊 Volume set to {volume}% in {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Volume error: {e}")
            return False
    
    async def get_position(self, chat_id: int) -> int:
        """Get current playback position in seconds"""
        try:
            call = call_py.get_active_call(chat_id)
            if call:
                return call.played_time
            return 0
        except:
            return 0

# Initialize player
from callsmusic.queue import queue_manager
player = MusicPlayer(queue_manager)
