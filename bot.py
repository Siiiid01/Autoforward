import asyncio, os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from db import ensure_doc, update

app  = Client("autofwd", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
WAIT = {}  # per-admin mini-state machine

@app.on_message(filters.command("start"))
async def start(_, m): await m.reply("👋 Hi! Use /f_on to set up auto-copy.")

@app.on_message(filters.command("f_on") & filters.user(OWNER_ID))
async def f_on(_, m):
    cfg = await ensure_doc()
    if cfg["active"]:
        kb  = InlineKeyboardMarkup([[InlineKeyboardButton("Set new IDs", b"new"),
                                     InlineKeyboardButton("Deactivate", b"off")]])
        cap = f"🔄 Active\nSRC: `{cfg['src']}`\nDST: `{cfg['dest']}`"
        await m.reply_photo("https://i.imgur.com/GrJ3l2Q.png", caption=cap, reply_markup=kb)
    else:
        await m.reply("Send **source** channel ID (or forward a post).")
        WAIT[m.from_user.id] = "src"

@app.on_callback_query(filters.user(OWNER_ID))
async def cb(_, q):
    if q.data == "new":
        await update(active=False, src=None, dest=None)
        await q.message.edit("Old IDs cleared.\nSend **source** channel ID.")
        WAIT[q.from_user.id] = "src"
    elif q.data == "off":
        await update(active=False)
        await q.message.edit("🔕 Auto-copy paused.")

@app.on_message(filters.private & filters.user(OWNER_ID))
async def id_collector(_, m):
    if m.from_user.id not in WAIT: return
    step = WAIT[m.from_user.id]
    cid  = m.forward_from_chat.id if m.forward_from_chat else int(m.text)
    if step == "src":
        await update(src=cid)
        WAIT[m.from_user.id] = "dest"
        await m.reply("Got it. Now send **destination** channel ID (or forward a post).")
    elif step == "dest":
        await update(dest=cid, active=True)
        WAIT.pop(m.from_user.id, None)
        cfg = await ensure_doc()
        cap = f"✅ Set!\nSRC: `{cfg['src']}`\nDST: `{cfg['dest']}`\nAuto-copy is live."
        await m.reply_photo("https://i.imgur.com/FQz0MY5.png", caption=cap)

@app.on_message(filters.channel)
async def copier(_, msg):
    cfg = await ensure_doc()
    if not cfg["active"] or msg.chat.id != cfg["src"]: return
    try:
        await asyncio.sleep(DELAY_SECS)
        await msg.copy(cfg["dest"])
    except FloodWait as e:
        await asyncio.sleep(e.value + 1)
        await msg.copy(cfg["dest"])

if __name__ == "__main__":
    app.run()
