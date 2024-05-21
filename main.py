from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import config
import logging
from handlers.mustjoin import check_user_joined_channels, generate_join_channels_keyboard
from handlers.stats import setup_stats_handlers
from handlers.database import add_user, get_required_channels
from handlers.broadcast import setup_broadcast

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Fetch required channel IDs at startup
required_channel_ids = []

async def fetch_channel_ids():
    global required_channel_ids
    required_channel_ids = get_required_channels()
    logger.info(f"Fetched required channel IDs: {required_channel_ids}")

async def pre_check_channels(client):
    """Pre-check if the bot itself can access the required channels."""
    for channel_id in required_channel_ids:
        try:
            await client.get_chat(channel_id)
            logger.info(f"Bot has access to channel: {channel_id}")
        except Exception as e:
            logger.error(f"Bot cannot access channel {channel_id}: {e}")

async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    user_full_name = message.from_user.first_name
    logger.info(f"Received /start command from user {user_id} ({username}) in chat {chat_id}")

    add_user(user_id, username)
    if message.from_user.last_name:
        user_full_name += ' ' + message.from_user.last_name

    try:
        if await check_user_joined_channels(client, user_id, required_channel_ids):
            welcome_message = (
                "**👀 Welcome to BDG Win Support Bot!**\n"
                "**👋 How can I assist you today?**\n\n"
                "**💡First, send me your UID screenshot.**\n"
                "**Register with [this link](https://bdgwin.com/#/register?invitationCode=48854928) if you haven't.**\n"
                "**Thank you!**\n"
                "**────────────────────────────**"
            )
            photo_url = "https://telegra.ph/file/a3852757146a2c0fcc184.jpg"
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("Recharge / Withdrawal Issue", url="https://t.me/lauraBDG66666")],
                [InlineKeyboardButton("VIP Channel", url="https://t.me/+Fp_scQvsGKsyZDhl")],
                [InlineKeyboardButton("Become an Agent 👨‍💼", url="https://t.me/AgentAvaniG"), InlineKeyboardButton("Collaboration 💬", url="https://t.me/RgC21")]
            ])
            await client.send_photo(chat_id=chat_id, photo=photo_url, caption=welcome_message, reply_markup=reply_markup)
            logger.info(f"Sent welcome message to user {user_id} ({username})")
        else:
            join_channels_message = (
                "**😎To use the BOT 🤖 you must join the below channels otherwise you can't access the bot**\n\n"
                "**👉JOIN & GET BENEFITS👇**"
            )
            reply_markup = generate_join_channels_keyboard()
            await message.reply_text(join_channels_message, reply_markup=reply_markup)
            logger.info(f"Sent join channels message to user {user_id} ({username})")
    except Exception as e:
        logger.error(f"Error in start handler for user {user_id} ({username}): {e}")
        await message.reply_text("An error occurred. Please try again later.")

async def on_callback_query(client, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    logger.info(f"Received callback query with data {data} in chat {chat_id}")

    if data == "check_joined":
        if await check_user_joined_channels(client, callback_query.from_user.id, required_channel_ids):
            await callback_query.message.edit(
                "Thank you for joining the channels! How can I assist you today?",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Get Started", callback_data="get_started")]]
                )
            )
            logger.info(f"User {callback_query.from_user.id} joined the required channels")
        else:
            await callback_query.answer("Please join all required channels first.", show_alert=True)
            logger.info(f"User {callback_query.from_user.id} has not joined the required channels")
    elif data == "get_started":
        welcome_message = (
            "**👀 Welcome to BDG Win Support Bot!**\n"
            "**👋 How can I assist you today?**\n\n"
            "**💡First, send me your UID screenshot.**\n"
            "**Register with [this link](https://bdgwin.com/#/register?invitationCode=48854928) if you haven't.**\n"
            "**Thank you!**\n"
            "**────────────────────────────**"
        )
        photo_url = "https://telegra.ph/file/a3852757146a2c0fcc184.jpg"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Recharge / Withdrawal Issue", url="https://t.me/lauraBDG66666")],
            [InlineKeyboardButton("VIP Channel", url="https://t.me/+Fp_scQvsGKsyZDhl")],
            [InlineKeyboardButton("Become an Agent 👨‍💼", url="https://t.me/AgentAvaniG"), InlineKeyboardButton("Collaboration 💬", url="https://t.me/RgC21")]
        ])
        await client.send_photo(chat_id=chat_id, photo=photo_url, caption=welcome_message, reply_markup=reply_markup)
        logger.info(f"Sent get started message to user {callback_query.from_user.id}")

app.add_handler(MessageHandler(start, filters.command("start")))
app.add_handler(CallbackQueryHandler(on_callback_query))
setup_stats_handlers(app)
setup_broadcast(app)

async def start_bot():
    logger.info(">> Bot Starting")
    await fetch_channel_ids()  # Fetch channel IDs before starting the bot
    await pre_check_channels(app)  # Pre-check channels before starting the bot
    await app.start()
    logger.info(">> Bot Started - Press CTRL+C to exit")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_bot())
    finally:
        loop.close()
