"""queue + flood‑safe copy helpers"""
import asyncio
from pyrogram.errors import FloodWait
from config import DELAY_SECS

queue: asyncio.Queue = asyncio.Queue()

# minimalist style helper
def style(text: str) -> str:
    return f"\u2022 {text.lower()} \u2022"

async def _copy_safe(msg, dest):
    try:
        await msg.copy(dest)
        await asyncio.sleep(DELAY_SECS)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await _copy_safe(msg, dest)

async def worker(app, dest):
    while True:
        msg = await queue.get()
        await _copy_safe(msg, dest)
        queue.task_done()