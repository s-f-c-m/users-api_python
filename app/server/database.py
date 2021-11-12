import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client[config('MONGO_DB')]

users_collection = database.get_collection(config('MONGO_COLLECTION'))

def user_helper(user) -> dict:
    return{
        'id': str(user['_id']),
        'user': user['user'],
        'name': user['name'],
        'password': user['password'],
        'roles': user['roles']
    }

async def fetch_users():
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({'_id': user.inserted_id})
    return user_helper(new_user)

async def fetch_user(user: str) -> dict:
    user = await users_collection.find_one({"user": user})
    if user:
        return user_helper(user)
    return {}

async def update_user(user: str, data: dict):
    if len(data) < 1:
        return False
    user_to_update = await users_collection.find_one({"user": user})
    if user_to_update:
        updated_user = await users_collection.update_one(
            {"user": user}, {'$set': data}
        )
        if updated_user:
            return True
        return False

async def delete_user(user: str):
    user_to_delete = await users_collection.find_one({"user":user})
    if user_to_delete:
        res = await users_collection.delete_one({"user": user})
        if res.deleted_count > 0:
            return True
    return False

