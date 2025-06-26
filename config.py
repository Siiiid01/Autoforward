import os

API_ID     = int(os.environ["API_ID"])
API_HASH   = os.environ["API_HASH"]
BOT_TOKEN  = os.environ["BOT_TOKEN"]
MONGO_URI  = os.environ["MONGO_URI"]          # full SRV or normal URI
MONGO_DB   = os.getenv("MONGO_DB", "autofwd") # fallback db name
OWNER_ID   = int(os.environ["OWNER_ID"])
DELAY_SECS = int(os.getenv("DELAY_SECS", "2"))
