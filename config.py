import os

API_ID       = int(os.environ["API_ID"])
API_HASH     = os.environ["API_HASH"]
BOT_TOKEN    = os.environ["BOT_TOKEN"]
MONGO_URI    = os.environ["MONGO_URI"]
OWNER_ID     = int(os.environ["OWNER_ID"])           # the admin who runs /f_on
DELAY_SECS   = int(os.getenv("DELAY_SECS", "2"))     # safe gap between copies
