import os
from pyrogram import Client, filters
import re

API_ID = int(os.environ.get("API_ID"))         # Get from https://my.telegram.org
API_HASH = os.environ.get("API_HASH")          # Get from https://my.telegram.org
BOT_TOKEN = os.environ.get("BOT_TOKEN")        # Get from @BotFather

app = Client("public_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.text)
async def forward_public_message(client, message):
    link = message.text.strip()

    # Match Telegram message link (like https://t.me/channelname/123)
    match = re.match(r"https?://t\.me/([\w\d_]+)/(\d+)", link)
    if not match:
        await message.reply("❌ Please send a valid public Telegram post link.\nExample:\nhttps://t.me/example_channel/123")
        return

    channel_username, msg_id = match.groups()

    try:
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=channel_username,
            message_id=int(msg_id)
        )
        await message.reply("✅ Message copied successfully.")
    except Exception as e:
        await message.reply(f"❌ Failed to copy message:\n`{e}`")

app.run()
