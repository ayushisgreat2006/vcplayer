from pyrogram import Client, filters, enums
from pyrogram.types import Message, CallbackQuery
from strings import Messages
from utils import buttons
from utils.decorators import authorized_only, chat_watcher
from database.chats import ChatDB

@Client.on_message(filters.command("start") & filters.private)
@authorized_only
@chat_watcher
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    mention = message.from_user.mention
    await message.reply(
        Messages.START.format(footer=Messages.footer()),
        reply_markup=buttons.start_buttons(),
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r"^help"))
async def help_callback(client: Client, callback: CallbackQuery):
    """Handle help menu callbacks"""
    data = callback.data
    
    if data == "help":
        await callback.message.edit_text(
            Messages.HELP.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif data == "help_music":
        await callback.message.edit_text(
            Messages.HELP_MUSIC.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif data == "help_admin":
        await callback.message.edit_text(
            Messages.HELP_ADMIN.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif data == "help_owner":
        await callback.message.edit_text(
            Messages.HELP_OWNER.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif data == "help_general":
        await callback.message.edit_text(
            Messages.HELP_GENERAL.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif data == "help_back":
        await callback.message.edit_text(
            Messages.HELP.format(footer=Messages.footer()),
            reply_markup=buttons.help_menu(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    await callback.answer()
