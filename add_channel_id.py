from handlers.database import add_channel


channel_ids = [
    "-1002092826606"
]

for channel_id in channel_ids:
    add_channel(channel_id)
    print(f"Added channel ID: {channel_id}")
