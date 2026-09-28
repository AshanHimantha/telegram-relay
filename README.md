# Telegram Bot-to-Bot Command Relay

Enables your Telegram bot to respond to commands posted by other bots in a group.

### Configuration (`.env`)
Copy `.env.example` to `.env` and fill in your values:
```ini
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TARGET_CHAT=-100xxxxxxxxxx
```

---

### Usage

1. **Send a manual command to the group:**
   ```powershell
   python send_test.py "/info 9999990000"
   ```

2. **Run the automatic relay:**
   ```powershell
   python relay.py
   ```
   * It listens strictly to your `TARGET_CHAT` group.
   * Whenever another bot sends any `/command`, it instantly repeats it as a user so your bot can receive and execute it.
