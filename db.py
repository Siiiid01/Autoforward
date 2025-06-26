"""motor helpers for persistent settings"""
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB

client = AsyncIOMotorClient(MONGO_URI)
db     = client[MONGO_DB]
config = db.settings  # single‑document collection

async def ensure_doc():
    doc = await config.find_one({"_id": "global"})
    if not doc:
        await config.insert_one({"_id": "global", "active": False, "src": None, "dest": None})
    return await config.find_one({"_id": "global"})

async def update(**kw):
    await config.update_one({"_id": "global"}, {"$set": kw})