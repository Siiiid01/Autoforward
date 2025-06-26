from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB

cli  = AsyncIOMotorClient(MONGO_URI)
db   = cli[MONGO_DB]                     # explicit db
coll = db.settings

async def ensure_doc():
    doc = await coll.find_one({"_id": "global"})
    if not doc:
        await coll.insert_one({"_id": "global",
                               "active": False,
                               "src": None,
                               "dest": None})
    return await coll.find_one({"_id": "global"})

async def update(**kwargs):
    await coll.update_one({"_id": "global"}, {"$set": kwargs})
