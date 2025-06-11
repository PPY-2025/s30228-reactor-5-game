from pymongo import MongoClient
from pymongo.collection import Collection
from database.models import *

client = MongoClient("mongodb://localhost:27017")
db = client["reactor_game"]
users_collection: Collection = db["users"]

def save_score(username: str, survival_time: int):
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
    cursor = users_collection.find({}, {"_id": 0}).sort("survival_time", -1).limit(limit)
    return list(cursor)

def create_user(user: User):
    return save_score(user.username, user.survival_time)

def get_user(username: str):
    return users_collection.find_one({"username": username}, {"_id": 0})

def update_user(username: str, survival_time: int):
    result = users_collection.update_one(
        {"username": username},
        {"$set": {
            "survival_time": survival_time,
            "timestamp": datetime.utcnow()
        }}
    )
    return result.modified_count

def delete_user(username: str):
    result = users_collection.delete_one({"username": username})
    return result.deleted_count

def delete_all_users():
    result = users_collection.delete_many({})
    return result.deleted_count