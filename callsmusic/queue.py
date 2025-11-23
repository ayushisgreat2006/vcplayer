from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class QueueItem:
    """Queue item structure"""
    title: str
    duration: int
    file_path: Optional[str]
    stream_url: str
    requester: int
    thumbnail: Optional[str]
    source: str
    webpage_url: str

class QueueManager:
    """In-memory queue manager"""
    
    def __init__(self):
        self.queues: Dict[int, List[QueueItem]] = {}
        self.loop_status: Dict[int, bool] = {}
        self.current_item: Dict[int, Optional[QueueItem]] = {}
        self.last_activity: Dict[int, float] = {}
    
    def get_queue(self, chat_id: int) -> List[QueueItem]:
        """Get queue for chat"""
        return self.queues.get(chat_id, [])
    
    def add_to_queue(self, chat_id: int, item: QueueItem) -> int:
        """Add item to queue"""
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(item)
        return len(self.queues[chat_id])
    
    def get_next(self, chat_id: int) -> Optional[QueueItem]:
        """Get next item from queue"""
        if chat_id in self.queues and self.queues[chat_id]:
            if self.loop_status.get(chat_id, False):
                # Return current item if loop is enabled
                return self.current_item.get(chat_id)
            return self.queues[chat_id].pop(0)
        return None
    
    def clear_queue(self, chat_id: int):
        """Clear queue for chat"""
        self.queues[chat_id] = []
    
    def shuffle_queue(self, chat_id: int):
        """Shuffle queue"""
        if chat_id in self.queues and len(self.queues[chat_id]) > 1:
            import random
            random.shuffle(self.queues[chat_id])
    
    def set_loop(self, chat_id: int, status: bool):
        """Set loop status"""
        self.loop_status[chat_id] = status
    
    def is_looping(self, chat_id: int) -> bool:
        """Check if loop is enabled"""
        return self.loop_status.get(chat_id, False)
    
    def set_current(self, chat_id: int, item: Optional[QueueItem]):
        """Set currently playing item"""
        self.current_item[chat_id] = item
    
    def get_current(self, chat_id: int) -> Optional[QueueItem]:
        """Get currently playing item"""
        return self.current_item.get(chat_id)
    
    def remove_chat(self, chat_id: int):
        """Remove chat from manager"""
        self.queues.pop(chat_id, None)
        self.loop_status.pop(chat_id, None)
        self.current_item.pop(chat_id, None)
        self.last_activity.pop(chat_id, None)

# Global queue instance
queue_manager = QueueManager()
