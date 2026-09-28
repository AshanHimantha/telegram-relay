import os
import sys
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

# =============================================================
#  CHANGE YOUR MESSAGE / COMMAND HERE:
# =============================================================
MESSAGE_TO_SEND = "/info 9999990000"
# =============================================================

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

async def main():
    # Uses command line argument if provided, otherwise uses MESSAGE_TO_SEND above
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else MESSAGE_TO_SEND

    await client.start()
    
    print(f"Sending to group ({TARGET_CHAT}): {msg}")
    await client.send_message(TARGET_CHAT, msg)
    print("SUCCESS: Sent to group!")

if __name__ == "__main__":
    asyncio.run(main())
