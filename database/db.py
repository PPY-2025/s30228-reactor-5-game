from pymongo import MongoClient
from database.models import *
from flask import current_app

def get_mongo_client():
    mongo_uri = current_app.config.get('MONGODB_URI')
    return MongoClient(mongo_uri)

def get_db():
    client = get_mongo_client()
    return client["reactor_game"]

def get_users_collection():
    db = get_db()
    return db["users"]

def save_score(username: str, survival_time: int):
    users_collection = get_users_collection()
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        if survival_time > existing_user["survival_time"]:
            users_collection.update_one(
                {"username": username},
                {"$set": {
                    "survival_time": survival_time,
                    "timestamp": datetime.utcnow()
                }}
            )
    else:
        users_collection.insert_one({
            "username": username,
            "survival_time": survival_time,
            "timestamp": datetime.utcnow()
        })

def get_leaderboard(limit=10):
    users_collection = get_users_collection()
    cursor = users_collection.find({}, {"_id": 0}).sort("survival_time", -1).limit(limit)
    return list(cursor)

def create_user(user: User):
    return save_score(user.username, user.survival_time)

def get_user(username: str):
    users_collection = get_users_collection()
    return users_collection.find_one({"username": username}, {"_id": 0})

def update_user(username: str, survival_time: int):
    users_collection = get_users_collection()
    result = users_collection.update_one(
        {"username": username},
        {"$set": {
            "survival_time": survival_time,
            "timestamp": datetime.utcnow()
        }}
    )
    return result.modified_count

def delete_user(username: str):
    users_collection = get_users_collection()
    result = users_collection.delete_one({"username": username})
    return result.deleted_count

def delete_all_users():
    users_collection = get_users_collection()
    result = users_collection.delete_many({})
    return result.deleted_count