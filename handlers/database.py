from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URI)
db = client['BdgWinSupport']


def add_channel(channel_id):
    channels_collection = db['channels']
    channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"channel_id": channel_id}},
        upsert=True
    )

def get_required_channels():
    channels_collection = db['channels']
    return [channel['channel_id'] for channel in channels_collection.find({}, {'channel_id': 1, '_id': 0})]

def add_user(user_id, username):
    users_collection = db['users']
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"username": username}},
        upsert=True
    )

def add_chat(chat_id, chat_title):
    chats_collection = db['chats']
    chats_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": chat_title}},
        upsert=True
    )

def get_all_users():
    users_collection = db['users']
    return list(users_collection.find({}))

def get_all_chats():
    chats_collection = db['chats']
    return list(chats_collection.find({}))
