# Telegram Bot-to-Bot Command Relay 🔄

A lightweight MTProto-powered relay bridge that enables Telegram bots to listen and respond to commands sent by other bots in Telegram groups.

---

## 📌 The Problem This Solves

By design, the **Telegram Bot API server strictly filters out messages sent by bots to other bots** in groups and channels. This is an intentional restriction enforced by Telegram to prevent infinite messaging loops.

* **The Issue:** If **Bot A** posts a command (e.g. `/topup 12345` or `/info`) inside a group, **Bot B** will **never** receive the update from Telegram. Disabling Privacy Mode or granting Administrator rights does **not** bypass this restriction.
* **The Solution:** Regular Telegram user accounts are **not** restricted by this filter. This relay logs in as a Telegram user client (Userbot) using MTProto, listens for commands sent by other bots, and instantly re-posts them into the group under the user account. Your bot sees a command sent by a user and responds immediately!

---

## 🏗️ How It Works

```text
┌─────────────────┐           ┌───────────────────┐
│    Other Bot    │           │  Telegram Group   │
│  (Third-Party)  │──posts───>│     Chat ID:      │
└─────────────────┘  /command │   -100xxxxxxxxx   │
                              └─────────┬─────────┘
                                        │
                                        │ (sees bot message)
                                        ▼
                              ┌───────────────────┐
                              │   Relay Client    │
                              │ (MTProto Userbot) │
                              └─────────┬─────────┘
                                        │
                                        │ (re-sends /command as User)
                                        ▼
┌─────────────────┐           ┌───────────────────┐
│    Your Bot     │<──sees────│  Telegram Group   │
│  (e.g. ShopBot) │  command  │                   │
└────────┬────────┘           └───────────────────┘
         │
         │ (processes command & replies)
         ▼
┌─────────────────┐
│ Response posted │
│    to Group     │
└─────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* **Python 3.8+** installed ([python.org](https://www.python.org/))
* A Telegram phone number (a dedicated secondary account is recommended)
* A Telegram API ID and API Hash (free from Telegram)

### 2. Get Telegram API Credentials (One-time only)
1. Go to [https://my.telegram.org](https://my.telegram.org) and log in with your phone number.
2. Click on **API development tools**.
3. Create a new application (enter any name, e.g. `CommandRelay`).
4. Copy your **`api_id`** (numeric) and **`api_hash`** (string).

### 3. Installation

Clone or download this repository and install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configuration

Create your `.env` file by copying the example:

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your values:

```ini
# Credentials from https://my.telegram.org
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef0123456789abcdef0123456789

# Group Chat ID where the bots communicate (starts with -100 or -)
TARGET_CHAT=-1001234567890
```

> **How to get your Group Chat ID?**  
> Add [@RawDataBot](https://t.me/RawDataBot) or forward any group message to [@userinfobot](https://t.me/userinfobot) to get the numeric group chat ID (e.g. `-100...` or `-...`).

---

## 💻 Usage

### Option A: Automatic Background Relay (`relay.py`)
Runs continuously in the background. Whenever another bot sends any `/command` in your group, it instantly repeats it under your user profile:

```bash
python relay.py
```

* **First run:** You will be prompted to enter your phone number and the verification code sent to your Telegram app.
* **Subsequent runs:** Credentials are saved locally to `telegram_relay.session`—you will never be asked to log in again.

```text
============================================================
RELAY ACTIVE: Logged in as YourName (@your_username)
Listening for bot commands in group: -1001234567890
============================================================

[BOT COMMAND DETECTED]
  Bot:     @OtherBot
  Command: /info 9999990000
  --> Relayed command to group successfully!
```

---

### Option B: Manual Command Tester (`send_test.py`)
Quickly test sending commands to your group to confirm your bot responds:

```bash
# 1. Send the default command configured in the script:
python send_test.py

# 2. Or pass any custom command directly:
python send_test.py "/info 1234567890"
python send_test.py "/balance"
```

You can also open `send_test.py` and modify the default command at the top:
```python
MESSAGE_TO_SEND = "/info 9999990000"
```

---

## 🔒 Security & Privacy

* **`.gitignore` protection:** Your `.env` and `*.session` files are strictly excluded from Git. Never commit or share these files as they contain authentication keys.
* **Secondary account recommendation:** It is recommended to use a dedicated spare account or SIM card for automation tasks rather than your primary personal account.

---

## 🛠️ Running in Production (24/7)

To keep `relay.py` running in the background on a server:

### Using PM2 (Recommended):
```bash
npm install -g pm2
pm2 start "python relay.py" --name "telegram-relay"
pm2 save
pm2 startup
```

### Using systemd (Linux):
Create `/etc/systemd/system/telegram-relay.service`:
```ini
[Unit]
Description=Telegram Bot-to-Bot Command Relay
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/telegram-relay
ExecStart=/usr/bin/python3 relay.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Enable and start:
```bash
sudo systemctl enable --now telegram-relay
```
