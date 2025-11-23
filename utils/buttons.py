from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_buttons() -> InlineKeyboardMarkup:
    """Start command buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Commands", callback_data="help"),
            InlineKeyboardButton("📢 Updates", url=f"t.me/{Config.UPDATES_CHANNEL}")
        ],
        [
            InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true")
        ]
    ])

def player_controls() -> InlineKeyboardMarkup:
    """Player control buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸", callback_data="pause"),
            InlineKeyboardButton("▶️", callback_data="resume"),
            InlineKeyboardButton("⏭", callback_data="skip"),
            InlineKeyboardButton("⏹", callback_data="stop")
        ],
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data="shuffle"),
            InlineKeyboardButton("🔁 Loop", callback_data="loop")
        ]
    ])

def search_results(results: list) -> InlineKeyboardMarkup:
    """Search result buttons"""
    buttons = []
    for i, result in enumerate(results[:5]):
        buttons.append([InlineKeyboardButton(
            f"{i+1}. {result['title'][:50]}",
            callback_data=f"play_{i}"
        )])
    return InlineKeyboardMarkup(buttons)

def updates_channel(channel: str) -> InlineKeyboardMarkup:
    """Updates channel button"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 Join Updates Channel", url=f"t.me/{channel}")
    ]])

def help_menu() -> InlineKeyboardMarkup:
    """Help menu categories"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 Music Commands", callback_data="help_music")],
        [InlineKeyboardButton("🛠 Admin Commands", callback_data="help_admin")],
        [InlineKeyboardButton("👮 Owner Commands", callback_data="help_owner")],
        [InlineKeyboardButton("💬 General Commands", callback_data="help_general")],
        [InlineKeyboardButton("🔙 Back", callback_data="help_back")]
    ])

def footer_buttons() -> InlineKeyboardMarkup:
    """Footer buttons for commands"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 Updates Channel", url=f"t.me/{Config.UPDATES_CHANNEL}"),
        InlineKeyboardButton("👤 Developer", url=f"t.me/{Config.DEV_USERNAME}")
    ]])

# Dynamic config for buttons
from config import Config
if not hasattr(Config, 'BOT_USERNAME'):
    Config.BOT_USERNAME = os.getenv("BOT_USERNAME", "StarkMusicBot")
if not hasattr(Config, 'DEV_USERNAME'):
    Config.DEV_USERNAME = os.getenv("DEV_USERNAME", "YourUsername")
