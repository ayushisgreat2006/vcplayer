class Messages:
    """Centralized message strings"""
    
    START = """
🎵 **Welcome to Stark Music Bot!**

I'm an advanced AI-enhanced music bot that can play music in your voice chats with high quality and zero lag.

**Features:**
• YouTube & Telegram Audio Streaming
• Sophisticated Queue Management
• Admin Controls & Global Ban System
• Inline Search Mode
• Auto Assistant Invite System

{footer}
"""

    HELP = """
🎵 **Stark Music Bot - Help Menu**

Use the buttons below to explore commands:

{footer}
"""

    HELP_MUSIC = """
🎵 **Music Commands**

/play <song/url> - Play a song
/pause - Pause playback
/resume - Resume playback
/skip - Skip current song
/stop - Stop playback
/seek <seconds> - Seek position
/current - Show current track
/queue - Show queue list
/shuffle - Shuffle queue
/loop - Toggle loop
/volume <1-200> - Set volume
/lyrics <song> - Get lyrics

**Inline Mode:** `@BotUsername <song>`

{footer}
"""

    HELP_ADMIN = """
🛠 **Admin Commands**

/addadmin <user> - Add bot admin
/deladmin <user> - Remove admin
/clearqueue - Clear queue
/syncadmins - Sync from Telegram

**Admin Rights Required:**
• Control playback
• Manage queue

{footer}
"""

    HELP_OWNER = """
👮 **Owner Commands**

/addadmin <user> - Add global admin
/deladmin <user> - Remove admin
/globalban <user> - Ban globally
/globalunban <user> - Unban
/broadcast - Broadcast message
/stats - Bot statistics
/leaveall - Leave all groups
/syncadmins - Sync all admins

{footer}
"""

    HELP_GENERAL = """
💬 **General Commands**

/start - Start the bot
/help - Show this menu
/ping - Check bot latency

{footer}
"""

    PLAYING = """
🎵 **Now Playing**

{status}

💿 **Title:** {title}
⏱ **Duration:** {duration}
🎤 **Requester:** {mention}
🔗 **Source:** {source}

{progress_bar}

{footer}
"""

    QUEUE = """
📋 **Queue List**

{items}

**Total:** {total} songs

{footer}
"""

    QUEUE_EMPTY = """
📭 **Queue is empty**

Add some songs with /play

{footer}
"""

    BANNED = "🚫 You are globally banned from using this bot!\nReason: {reason}"

    NOT_ADMIN = "🚫 You need to be an admin to use this command!"

    NOT_OWNER = "🚫 This command is for the bot owner only!"

    BOT_NOT_ADMIN = """
⚠️ **Bot is missing required permissions!**

{missing}

Please make the bot an admin with these permissions.
"""

    ASSISTANT_INVITING = """
⚡ **Inviting assistant to the group...**

Please wait, this may take a few seconds.
"""

    ASSISTANT_JOINED = "✅ Assistant joined successfully!"

    ASSISTANT_FAILED = """
❌ **Failed to invite assistant!**

Please add the assistant manually by clicking the button below.
"""

    NO_VOICE_CHAT = "❌ No active voice chat found! Start one first."

    NO_SONG_PLAYING = "❌ No song is currently playing!"

    SONG_SKIPPED = "⏭ Skipped to next song."

    QUEUE_CLEARED = "🗑️ Queue cleared successfully."

    USER_BANNED = "🚫 User {user_id} has been globally banned!"

    USER_UNBANNED = "✅ User {user_id} has been unbanned."

    ADMIN_ADDED = "✅ User {user_id} is now an admin."

    ADMIN_REMOVED = "✅ User {user_id} is no longer an admin."

    BROADCAST_START = "📡 Broadcasting your message...\nThis may take a while."

    BROADCAST_DONE = """
📊 **Broadcast Completed!**

✅ **Success:** {success}
❌ **Failed:** {failed}
"""

    STATS = """
📊 **Bot Statistics**

👥 **Users:** {users}
👥 **Groups:** {groups}
🎵 **Active Chats:** {active}

Uptime: {uptime}
"""

    PING = "🏓 **Pong!** `{ms}ms`"

    LYRICS_NOT_FOUND = "❌ Lyrics not found for this song."

    @staticmethod
    def footer():
        """Generate footer with dynamic config"""
        return f"Made by @{Config.DEV_USERNAME} | Updates: @{Config.UPDATES_CHANNEL}"

# Dynamic config
from config import Config
if not hasattr(Config, 'DEV_USERNAME'):
    Config.DEV_USERNAME = os.getenv("DEV_USERNAME", "YourUsername")
if not hasattr(Config, 'UPDATES_CHANNEL'):
    Config.UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "YourUpdatesChannel")
