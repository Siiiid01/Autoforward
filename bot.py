import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config     import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from db         import ensure_doc, update
from forwarder  import queue, worker, style

app = Client("autofwd", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# cmd handler (admin‑only)
@app.on_message(filters.command("f_on") & filters.user(OWNER_ID))
async def f_on(_, m):
    cfg = await ensure_doc()
    if cfg["src"] and cfg["dest"]:
        cap  = style(f"forwarding active\nsource: {cfg['src']}\ndest: {cfg['dest']}")
        kb   = InlineKeyboardMarkup([[InlineKeyboardButton("set new ids", b"reset")]])
        await m.reply_caption(cap, reply_markup=kb)
    else:
        await update(active=True)
        await m.reply_text(style("send source channel id"))

# callback for reset button
@app.on_callback_query(filters.user(OWNER_ID))
async def callbacks(_, q):
    if q.data == "reset":
        await update(src=None, dest=None, active=True)
        await q.message.edit_caption(style("send source channel id"))

# id collection step‑by‑step
@app.on_message(filters.private & filters.user(OWNER_ID))
async def collect_ids(_, m):
    cfg = await ensure_doc()
    if cfg["active"] and not cfg["src"]:
        await update(src=int(m.text))
        await m.reply_text(style("source saved\nsend dest id"))
    elif cfg["active"] and cfg["src"] and not cfg["dest"]:
        await update(dest=int(m.text), active=False)
        await m.reply_text(style("destination saved\nwatching source"))
        # start queue worker now that both ids exist
        asyncio.create_task(worker(app, int(m.text)))

# watch channel posts
@app.on_message(filters.channel)
async def enqueue(_, msg):
    cfg = await ensure_doc()
    if cfg["src"] and cfg["dest"] and msg.chat.id == cfg["src"]:
        await queue.put(msg)

async def main():
    await app.start()
    cfg = await ensure_doc()
    if cfg["src"] and cfg["dest"]:
        asyncio.create_task(worker(app, cfg["dest"]))
    print("• autofwd running •")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())