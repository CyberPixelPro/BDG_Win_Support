from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_join_channels_keyboard():

    channel_links = [
        "https://t.me/Colourtrading",
        "https://t.me/addlist/WvSzEb1soLEzZTBl",
    ]
    keyboard = []
    for link in channel_links:
        button = InlineKeyboardButton("𝙈𝙐𝙎𝙏 𝙅𝙊𝙄𝙉 💰", url=link)  # Updated button text to "Join Channel"
        keyboard.append([button])
    
    
    
    
    
    keyboard.append([InlineKeyboardButton("𝙉𝙀𝙓𝙏 ➡️", callback_data="check_joined")])
    
    return InlineKeyboardMarkup(keyboard)

async def check_user_joined_channels(client, user_id, required_channel_ids):
    for channel_id in required_channel_ids:
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            return False
    return True
