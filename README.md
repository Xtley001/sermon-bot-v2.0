# 🙏 Pastor Tara Advisor Bot

A warm, intelligent Telegram bot that provides spiritual guidance through Pastor Tara Akinkuade's teachings. Chat naturally and receive personalized sermon recommendations with love! ✨

## 🌟 Features

- 💬 **Natural Conversation**: Chat freely - no rigid commands needed!
- 🤖 **AI-Powered**: Smart recommendations using RAG + OpenAI
- 📖 **Bible Verses**: Each response includes relevant scripture
- 🎧 **Sermon Library**: Access 400-500+ teachings from 4 channels
- ⚡ **Fast & Cached**: Instant responses with 6-hour caching
- 🔥 **Warm & Pastoral**: Emoji-filled, encouraging tone
- 🐳 **Docker Ready**: Easy deployment anywhere

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

- Python 3.11+
- Telegram account
- OpenAI API account (free trial OK)

### 2️⃣ Get Your API Keys

#### **Telegram Bot Token**
1. Open Telegram and chat with [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Name it: `Pastor Tara Advisor`
4. Username: `YourBotName_bot`
5. Copy the **token** you receive

#### **Telegram API Credentials (for scraping)**
1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone
3. Go to "API development tools"
4. Create an app - copy **API ID** and **API Hash**

#### **OpenAI API Key**
1. Sign up at [openai.com](https://openai.com)
2. Go to [API Keys](https://platform.openai.com/api-keys)
3. Click "Create new secret key"
4. Copy the key

#### **Your Telegram User ID**
1. Chat with [@myidbot](https://t.me/myidbot)
2. Send `/getid`
3. Copy your user ID

### 3️⃣ Setup Project
```bash
# Clone or download the project
cd pastor-tara-advisor

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your keys
nano .env  # or use any text editor
```

**Fill in your `.env` file:**
```env
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_ADMIN_IDS=123456789
OPENAI_API_KEY=sk-proj-abc123...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_PHONE=+1234567890
```

### 4️⃣ Load Sermon Data
```bash
# This scrapes the 4 channels and loads materials
python run_ingest.py
```

**Expected output:**
```
🚀 Starting data ingestion...
📡 Scraping Telegram channels...
✅ Scraped 450 sermons from channels
📁 Loading materials from folder...
✅ Materials loaded successfully
🎉 All files loaded!
📊 Total sermons in database: 450
```

### 5️⃣ Run the Bot
```bash
python main.py
```

**You'll see:**
```
🚀 Starting Pastor Tara Advisor Bot
✅ Configuration loaded successfully
✅ Bot initialized successfully
🎉 Bot is now running! Press Ctrl+C to stop.
```

### 6️⃣ Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Chat naturally: "I need encouragement about faith"
5. Get warm responses + sermon recommendations! 🎉

---

## 📁 Adding Materials

Drop sermon files into `materials/` folder:
```bash
materials/
├── Faith and Purpose.txt
├── Healing Power [https://t.me/link].docx
├── Prosperity Message.pdf
```

**Filename format** (optional metadata):
```
Title [link] [image.jpg].ext
```

Then run:
```bash
python run_ingest.py
```

Files are automatically processed and deleted after loading! ✅

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t pastor-tara-bot .
```

### Run Container
```bash
docker run -d \
  --name pastor-tara-bot \
  -v $(pwd)/db:/app/db \
  -v $(pwd)/materials:/app/materials \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  pastor-tara-bot
```

### View Logs
```bash
docker logs -f pastor-tara-bot
```

### Stop Container
```bash
docker stop pastor-tara-bot
docker rm pastor-tara-bot
```

---

## 💬 Usage Examples

### Natural Conversation (Recommended)
```
User: I'm struggling with fear today
Bot: I hear your heart, beloved! 🙏 Remember...
     [Bible verse + encouragement]
     [3 sermon recommendations with photos]
```

### With Commands
```
/start - Welcome message
/recommend faith 5 - Get 5 faith sermons
/more - Get next 5 from last search
/help - Show help
```

### Getting More
```
User: more
Bot: 🎧 Here are more sermons for you:
     [Next 5 recommendations]
```

---

## 📊 Project Structure
```
pastor-tara-advisor/
├── main.py                 # Bot starter
├── telegram_bot.py         # Chat handler & commands
├── utils.py                # AI & RAG engine
├── rag_ingest.py          # Channel scraper & loader
├── run_ingest.py          # Ingestion runner
├── db_handler.py          # SQLite database
├── config.py              # Configuration loader
├── requirements.txt       # Python packages
├── Dockerfile             # Container setup
├── .env.example           # Environment template
├── .env                   # Your keys (git-ignored)
├── README.md              # This file
├── db/                    # Database files
│   ├── sermons.db        # SQLite database
│   └── chroma/           # Vector store
├── cache/                 # Response cache
├── materials/             # Drop sermon files here
└── logs/                  # Application logs
    └── app.log
```

---

## 🔧 Configuration

### Channels Scraped
- @pst_tara
- @TheSupernaturalBusinessMan
- @TheSupernaturalFamily
- @TheSupernaturalStudent

### AI Models
- **Chat**: gpt-4o-mini (fast & affordable)
- **Embeddings**: text-embedding-3-small

### Caching
- Duration: 6 hours per user
- Location: `cache/` folder

### Search
- Initial retrieval: Top 20 results
- AI ranking: Relevance score ≥ 0.7
- Default recommendations: 5 sermons

---

## 🛠️ Troubleshooting

### Bot doesn't respond
- Check `.env` has correct `TELEGRAM_TOKEN`
- Verify bot is running: `python main.py`
- Check logs: `tail -f logs/app.log`

### No sermons found
- Run ingestion: `python run_ingest.py`
- Check Telegram API credentials in `.env`
- Ensure channels are public

### OpenAI errors
- Verify `OPENAI_API_KEY` is correct
- Check you have API credits
- Try regenerating the key

### Docker issues
```bash
# Check container status
docker ps -a

# View logs
docker logs pastor-tara-bot

# Restart
docker restart pastor-tara-bot
```

---

## 📝 Maintenance

### Re-scrape Channels
```bash
# Get latest sermons
python run_ingest.py
```

### Clear Cache
```bash
rm -rf cache/*
```

### View Database Stats
```bash
sqlite3 db/sermons.db "SELECT COUNT(*) FROM sermons;"
```

### Backup Database
```bash
cp -r db/ db_backup/
```

---

## 🎯 Best Practices

1. **Run ingestion weekly** to get new sermons
2. **Monitor logs** for errors: `tail -f logs/app.log`
3. **Backup database** before major updates
4. **Test locally** before deploying to production
5. **Keep API keys secret** - never commit `.env`

---

## 🙏 Support

Need help? Here's what to do:

1. Check logs: `logs/app.log`
2. Review this README
3. Verify all API keys are correct
4. Try running ingestion again

---

## ✨ Features in Detail

### Warm Pastoral Responses
Every reply includes:
- 💖 Loving acknowledgment
- 📖 Relevant Bible verse
- 🔥 Encouraging message with emojis
- 🎧 Sermon recommendations

### Smart Recommendation Engine
- Uses RAG (Retrieval Augmented Generation)
- Searches 400-500+ sermons semantically
- AI ranks by relevance
- Filters duplicates automatically
- Caches for speed

### Natural Language Processing
- No strict command syntax required
- Understands: "recommend 3 messages on healing"
- Extracts: topic="healing", num=3
- Responds naturally like a friend

---

## 📜 License

This project is for pastoral ministry use. May God bless your work! 🙏✨

---

**Built with ❤️ for the Body of Christ**

🔥 _"Let the word of Christ dwell in you richly"_ - Colossians 3:16
```

---

## 📂 Complete Project Directory Structure
```
pastor-tara-advisor/
│
├── 📄 main.py                      # Bot entry point
├── 📄 telegram_bot.py              # Telegram handler
├── 📄 utils.py                     # AI & RAG utilities
├── 📄 rag_ingest.py               # Channel scraper
├── 📄 run_ingest.py               # Ingestion runner
├── 📄 db_handler.py               # Database handler
├── 📄 config.py                    # Configuration
│
├── 📄 requirements.txt             # Python packages
├── 📄 Dockerfile                   # Docker config
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Your keys (create this)
├── 📄 README.md                    # Documentation
│
├── 📁 db/                          # Database directory
│   ├── sermons.db                 # SQLite database
│   └── chroma/                    # Vector store
│
├── 📁 cache/                       # Response cache
│
├── 📁 materials/                   # Drop sermon files here
│   └── (empty - add your files)
│
└── 📁 logs/                        # Log files
    ├── app.log                    # Main log
    └── ingest.log                 # Ingestion log







    stuffs to do:Yes! It's likely a cached/compiled Python file issue. The error is coming from a mismatch between `openai==1.54.0` and `langchain-openai==0.2.0`. Let's fix this:

## Step 1: Clear Python cache and reinstall

```bash
# Delete all cache
rd /s /q __pycache__
rd /s /q venv\Lib\site-packages\__pycache__
del /s *.pyc

# Uninstall conflicting packages
pip uninstall -y openai langchain-openai langchain-chroma langchain langchain-community langchain-text-splitters

# Install compatible versions
pip install openai==1.12.0
pip install langchain==0.3.0
pip install langchain-openai==0.2.0
pip install langchain-chroma==0.1.4
pip install langchain-text-splitters==0.3.0
pip install langchain-community==0.3.0
```

## Step 2: Update requirements.txt to these compatible versions:

```txt
telethon==1.36.0
langchain==0.3.0
langchain-openai==0.2.0
langchain-chroma==0.1.4
langchain-text-splitters==0.3.0
langchain-community==0.3.0
openai==1.12.0
chromadb==0.5.0
python-dotenv==1.0.1
unstructured==0.16.0
python-docx==1.1.0
PyPDF2==3.0.1
pillow==10.3.0
python-telegram-bot==21.0
pydantic==2.9.0
```

## Step 3: Test again

```bash
python test_imports.py
```

## If that still doesn't work, try a fresh virtual environment:

```bash
# Deactivate current venv
deactivate

# Delete old venv
rd /s /q venv

# Create new venv
python -m venv venv

# Activate
venv\Scripts\activate

# Install with the downgraded openai version
pip install -r requirements.txt
```

The key issue is `openai==1.54.0` is too new for `langchain-openai==0.2.0`. Using `openai==1.12.0` will fix this.

Let me know if this works! 🔧