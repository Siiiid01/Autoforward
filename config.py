"""load env variables and basic constants"""
import os

API_ID     = int(os.environ["API_ID"])
API_HASH   = os.environ["API_HASH"]
BOT_TOKEN  = os.environ["BOT_TOKEN"]
MONGO_URI  = os.environ["MONGO_URI"]             # full connection string
MONGO_DB   = os.getenv("MONGO_DB", "autofwd")   # default db name
OWNER_ID   = int(os.environ["OWNER_ID"])        # admin telegram id
DELAY_SECS = int(os.getenv("DELAY_SECS", 2))    # gap between copies