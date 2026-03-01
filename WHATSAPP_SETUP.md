# WhatsApp Watcher - Quick Setup Guide

**Quick Start:** Get the WhatsApp Watcher running in 5 minutes

---

## 🚀 Installation Steps

### Step 1: Install Dependencies

```bash
pip install playwright pyyaml
playwright install chromium
```

### Step 2: First-Time Setup (QR Code Scan)

Run the watcher to open WhatsApp Web:

**Windows:**
```bash
cd watchers
start_whatsapp_watcher.bat
```

**Mac/Linux:**
```bash
cd watchers
chmod +x start_whatsapp_watcher.sh
./start_whatsapp_watcher.sh
```

Or run directly:
```bash
python watchers/whatsapp_watcher.py
```

### Step 3: Scan QR Code

1. A Chromium browser window will open
2. You'll see a QR code on web.whatsapp.com
3. Open WhatsApp on your phone:
   - **Android:** Settings → Linked Devices → Link a Device
   - **iOS:** Settings → Linked Devices → Link a Device
4. Scan the QR code with your phone
5. WhatsApp Web will load with your chats

### Step 4: The Watcher is Running!

The watcher will now:
- Check for new messages every 60 seconds
- Look for keywords (urgent, invoice, payment, help, etc.)
- Create action files in `AI_Employee_Vault/Needs_Action/`

### Step 5: Stop the Watcher

Press `Ctrl+C` in the terminal to stop

---

## 📝 Customization

### Change Monitoring Keywords

Edit `watchers/whatsapp_keywords.yaml`:

```yaml
keywords:
  - urgent
  - asap
  - invoice
  - your-custom-keyword
```

### Change Check Interval

Edit `watchers/whatsapp_watcher.py` line 225:

```python
watcher = WhatsAppWatcher(
    vault_path=str(vault_path),
    session_path=session_path,
    check_interval=30  # Change to 30 seconds
)
```

---

## 📁 How It Works

```
WhatsApp Message
    ↓
[Contains Keyword?]
    ↓ Yes
Create Action File → Needs_Action/WHATSAPP_sender_timestamp.md
    ↓
AI Employee Reads & Processes
    ↓
Responds (if needed)
```

---

## 🧪 Testing

Send yourself a test message on WhatsApp with any of these keywords:
- "urgent"
- "invoice"
- "payment"
- "help"
- "pricing"

Example:
```
"Hey, can you send me the invoice?"
```

The watcher should create an action file in:
```
AI_Employee_Vault/Needs_Action/WHATSAPP_YourName_20260301_123456.md
```

---

## ⚠️ Important Notes

1. **Session Storage:** Your WhatsApp session is stored in `watchers/whatsapp_session/` - never share this folder
2. **First Run:** You'll need to scan the QR code only on first run
3. **Headless Mode:** After first login, you can set `headless=True` in the script for background operation
4. **ToS Warning:** This automation may violate WhatsApp's Terms of Service - use at your own risk
5. **Rate Limits:** Don't set check_interval too low (minimum 60 seconds recommended)

---

## 🔐 Security

- Session data is stored locally and never synced
- Only message IDs are saved, not full message content
- Sensitive files are gitignored automatically
- No data is transmitted to external servers

---

## 📚 Documentation

Full documentation available in: `WHATSAPP_WATCHER_SKILL.md`

---

## 🆘 Troubleshooting

**Problem:** QR code appears every time
- **Solution:** Ensure `whatsapp_session/` directory exists and is writable

**Problem:** No messages detected
- **Solution:** Check that messages contain keywords from `whatsapp_keywords.yaml`

**Problem:** Playwright errors
- **Solution:** Run `playwright install chromium --force`

**Problem:** Account banned
- **Solution:** Stop using automation immediately. Consider WhatsApp Business API for business use.

---

**That's it! Your WhatsApp Watcher is ready to monitor for urgent messages.** 🎉
