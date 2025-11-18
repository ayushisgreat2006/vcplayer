# utils/buttons.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def control_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏯️ Pause/Resume", callback_data="toggle_pause"),
                InlineKeyboardButton("⏭️ Skip", callback_data="skip"),
            ],
            [
                InlineKeyboardButton("⏹️ Stop", callback_data="stop"),
                InlineKeyboardButton("❌ Close", callback_data="close"),
            ],
        ]
    )
