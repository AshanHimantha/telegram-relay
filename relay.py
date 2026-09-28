import os
import sys
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
TARGET_CHAT = int(os.environ["TARGET_CHAT"])

session_path = os.path.join(os.path.dirname(__file__), "telegram_relay")
client = TelegramClient(session_path, API_ID, API_HASH)

# Listen strictly to the TARGET_CHAT group
@client.on(events.NewMessage(chats=TARGET_CHAT))
async def on_group_message(event):
    # Ignore our own messages to avoid endless loops
    if event.out:
        return

    sender = await event.get_sender()
    if not sender:
        return

    # Check if the sender is a bot
    is_bot = getattr(sender, "bot", False)
    if not is_bot:
        return

    text = (event.raw_text or "").strip()

    # Only relay commands starting with '/'
    if not text.startswith("/"):
        return

    sender_name = getattr(sender, "username", "") or getattr(sender, "first_name", "Bot")
    print(f"\n[BOT COMMAND DETECTED]")
    print(f"  Bot:     @{sender_name}")
    print(f"  Command: {text}")

    try:
        # Re-send the command to the group as the user account
        await client.send_message(TARGET_CHAT, text)
        print("  --> Relayed command to group successfully!")
    except Exception as e:
        print(f"  [ERROR] Failed to send: {e}")

async def main():
    await client.start()
    me = await client.get_me()
    print("=" * 60)
    print(f"RELAY ACTIVE: Logged in as {me.first_name} (@{me.username or 'No username'})")
    print(f"Listening for bot commands in group: {TARGET_CHAT}")
    print("=" * 60)
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nRelay stopped.")
