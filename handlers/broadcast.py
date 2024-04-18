import asyncio
from pyrogram import Client, filters, errors

from handlers.database import db

app = None
ALLOWED_USER_IDS = [5014174694, 5693070387]

def setup_broadcast(application):
    global app
    app = application

    @app.on_message(filters.command("broadcast") & filters.user(ALLOWED_USER_IDS))
    async def broadcast_message(client, message):
        if message.reply_to_message:
            x = message.reply_to_message.id
            y = message.chat.id
            reply_markup = message.reply_to_message.reply_markup if message.reply_to_message.reply_markup else None
            content = None
        else:
            if len(message.command) > 1:
                content = message.text.split(None, 1)[1]
            else:
                return await message.reply_text(
                    "<b>Example:</b>\n/broadcast [message] or reply to a message with /broadcast"
                )

        susr = 0
        susers = await fetch_all_user_ids()
        for user_id in susers:
            try:
                if message.reply_to_message:
                    await client.copy_message(chat_id=user_id, from_chat_id=y, message_id=x, reply_markup=reply_markup)
                else:
                    await client.send_message(chat_id=user_id, text=content)
                susr += 1
                await asyncio.sleep(0.3)
            except errors.FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

        try:
            await message.reply_text(f"<b>Broadcasted message to {susr} users.</b>")
        except Exception as e:
            print(f"Failed to send completion message: {e}")

async def fetch_all_user_ids():
    """Fetch all user IDs from the users collection in the database."""
    users_collection = db['users']
    all_users = users_collection.find({}, {'user_id': 1, '_id': 0})
    return [user['user_id'] for user in all_users]
