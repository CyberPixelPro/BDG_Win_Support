from handlers.database import db
from pyrogram import Client, filters

ALLOWED_USER_IDS = [5014174694, 5693070387]

def setup_stats(app):
    global extern_app
    extern_app = app

def count_users():
    users_collection = db['users']
    return users_collection.count_documents({})

def setup_stats_handlers(app):
    @app.on_message(filters.command("stats") & filters.user(ALLOWED_USER_IDS))
    async def send_stats(client, message):
        num_users = count_users()
        await message.reply_text(f"**Total users: {num_users}**")
