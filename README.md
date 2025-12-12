# 🙏 Pastor Tara Akinkuade Advisor Bot

A warm, intelligent Telegram bot that provides spiritual guidance through Pastor Tara Akinkuade's teachings. Chat naturally and receive personalized sermon recommendations with love! ✨

## 🌟 Features

- 💬 **Natural Conversation**: Chat freely - no rigid commands needed!
- 🤖 **AI-Powered**: Smart recommendations using RAG + OpenAI
- 📖 **Bible Verses**: Each response includes relevant scripture
- 🎧 **Sermon Library**: 669+ teachings from 4 channels
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

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

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

**What happens:**
- Connects to Telegram (you'll enter verification code on first run)
- Scrapes @pst_tara, @TheSupernaturalBusinessMan, @TheSupernaturalFamily, @TheSupernaturalStudent
- Extracts sermon titles, descriptions, themes with AI
- Saves to SQLite database
- Loads any files from `materials/` folder
- Adds everything to vector store for fast search

**Expected output:**
```
🚀 Starting data ingestion...
📡 Scraping Telegram channels...
Please enter the code you received: 12345
Signed in successfully...
Scraped 450 sermons from @pst_tara
Scraped 85 sermons from @TheSupernaturalBusinessMan
...
✅ Scraped 550 sermons from channels
📁 Loading materials from folder...
✅ Materials loaded successfully
🎉 All files loaded!
📊 Total sermons in database: 669
```

### 5️⃣ Run the Bot

```bash
python main.py
```

**You'll see:**
```
Starting Pastor Tara Advisor Bot
Configuration loaded successfully
Bot initialized successfully
Bot is now running! Press Ctrl+C to stop.
```

### 6️⃣ Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Chat naturally: "I need encouragement about faith"
5. Get warm responses + sermon recommendations! 🎉

---

## 📁 Project Structure

```
pastor-tara-advisor/
├── main.py                 # Bot entry point - starts the bot
├── telegram_bot.py         # Telegram handlers - chat & commands
├── utils.py                # AI & RAG engine - recommendation logic
├── rag_ingest.py          # Channel scraper & file loader
├── run_ingest.py          # Ingestion runner script
├── db_handler.py          # SQLite database operations
├── config.py              # Configuration loader from .env
├── fix_vector_store.py    # Utility to repair vector store
├── view_sermons.py        # Utility to view all sermons
├── test_imports.py        # Test if all packages work
│
├── requirements.txt       # Python packages (DO NOT MODIFY)
├── Dockerfile             # Docker container setup
├── .env.example           # Environment template
├── .env                   # Your API keys (CREATE THIS)
├── README.md              # This documentation
│
├── db/                    # Database directory (auto-created)
│   ├── sermons.db        # SQLite database with all sermons
│   └── chroma/           # Vector store for semantic search
│
├── cache/                 # Response cache (auto-created)
│   └── rank_*.json       # Cached AI rankings
│
├── materials/             # Drop sermon files here
│   └── (place .txt, .docx, .pdf files)
│
└── logs/                  # Application logs (auto-created)
    ├── app.log           # Main bot logs
    └── ingest.log        # Ingestion logs
```

---

## 🛠️ Utility Scripts

### View All Sermons
```bash
python view_sermons.py
```
Shows all scraped sermons with titles, channels, dates, themes.

### Test Imports
```bash
python test_imports.py
```
Checks if all dependencies are installed correctly.

### Fix Vector Store
```bash
python fix_vector_store.py
```
If search returns 0 results, run this to rebuild the vector store from database.

### Export to CSV
```bash
python export_sermons.py  # (create this if needed)
```

---

## 📁 Adding More Materials

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
Bot: I hear your heart, beloved! 🙏 Remember, 'For God has not 
     given us a spirit of fear, but of power and of love and of 
     a sound mind.' - 2 Timothy 1:7 📖 God is with you in this 
     season! ✨

     [Then sends 3-5 sermon recommendations as separate photo 
     messages with images, titles, descriptions, and links]
```

### With Commands
```
/start - Welcome message with instructions
/recommend faith 5 - Get 5 sermons about faith
/more - Get next 5 from last search
/help - Show all commands
```

### Getting More Results
```
User: more
Bot: 🎧 Here are more sermons for you:
     [Next 5 recommendations from previous search]
```

---

## 🔧 Configuration

### Channels Scraped
- @pst_tara
- @TheSupernaturalBusinessMan
- @TheSupernaturalFamily
- @TheSupernaturalStudent

### AI Models Used
- **Chat**: gpt-4o-mini (fast & affordable)
- **Embeddings**: text-embedding-3-small
- **Provider**: OpenAI

### Caching System
- **Duration**: 6 hours per user
- **Location**: `cache/` folder
- **Type**: File-based JSON cache
- **Benefit**: Instant responses for repeated queries

### Search Configuration
- **Initial retrieval**: Top 20 most similar sermons
- **AI ranking**: Filters relevance score ≥ 0.7
- **Default recommendations**: 5 sermons per request
- **Max per request**: 20 sermons

---

## 🛠️ Troubleshooting

### Bot doesn't respond
```bash
# Check if bot is running
ps aux | grep python  # Mac/Linux
tasklist | findstr python  # Windows

# Check logs
tail -f logs/app.log  # Mac/Linux
type logs\app.log  # Windows

# Verify .env configuration
cat .env  # Check TELEGRAM_TOKEN is set
```

### No sermons found (0 results)
```bash
# Check database
python -c "from db_handler import SermonDatabase; import config; print(f'Count: {SermonDatabase(config.DB_PATH).get_sermon_count()}')"

# If database has sermons but search returns 0, fix vector store:
python fix_vector_store.py

# Then restart bot
python main.py
```

### Connection timeout errors
```bash
# Check internet connection
ping api.telegram.org

# If blocked, use VPN or check firewall
# On Windows: Allow Python through Windows Firewall
# Settings → Windows Security → Firewall → Allow an app
```

### OpenAI API errors
- Verify `OPENAI_API_KEY` is correct in `.env`
- Check you have API credits at https://platform.openai.com/usage
- Try regenerating the key
- Make sure you're using `openai==1.12.0` (check requirements.txt)

### Import errors
```bash
# Test all imports
python test_imports.py

# If any fail, reinstall dependencies
pip uninstall -y langchain langchain-openai openai
pip install -r requirements.txt
```

### Database locked error
```bash
# Kill all Python processes
taskkill /F /IM python.exe  # Windows
pkill python  # Mac/Linux

# Then restart
python main.py
```

---

## 📝 Maintenance Tasks

### Weekly: Re-scrape for New Sermons
```bash
python run_ingest.py
```
Gets latest messages from channels (skips duplicates automatically).

### Monthly: Clear Old Cache
```bash
rm -rf cache/*  # Mac/Linux
rd /s /q cache  # Windows
mkdir cache
```

### View Database Statistics
```bash
sqlite3 db/sermons.db "SELECT COUNT(*) FROM sermons;"
sqlite3 db/sermons.db "SELECT channel, COUNT(*) FROM sermons GROUP BY channel;"
```

### Backup Database
```bash
# Full backup
cp -r db/ db_backup_$(date +%Y%m%d)/  # Mac/Linux
xcopy db db_backup /E /I  # Windows

# Just SQLite
cp db/sermons.db sermons_backup.db
```

### Monitor Logs
```bash
# Real-time monitoring
tail -f logs/app.log  # Mac/Linux
Get-Content logs\app.log -Wait  # PowerShell

# Search for errors
grep ERROR logs/app.log
```

---

## 🎯 Best Practices

1. **Run ingestion weekly** to get new sermons from channels
2. **Monitor logs** for errors: `tail -f logs/app.log`
3. **Backup database** before major updates or monthly
4. **Test locally** before deploying to production server
5. **Keep API keys secret** - never commit `.env` to git
6. **Use virtual environment** to isolate dependencies
7. **Set up monitoring** for production deployments
8. **Disable PC sleep** during ingestion (takes 10-20 minutes)

---

## 🙏 Support & Help

### If Bot Stops Working

1. **Check logs first**
   ```bash
   tail -50 logs/app.log
   ```

2. **Verify configuration**
   ```bash
   python test_imports.py
   ```

3. **Test database**
   ```bash
   python view_sermons.py
   ```

4. **Rebuild vector store if needed**
   ```bash
   python fix_vector_store.py
   ```

5. **Restart bot**
   ```bash
   python main.py
   ```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Found 0 results" | Run `python fix_vector_store.py` |
| "Database locked" | Kill all Python processes, restart |
| "Connection timeout" | Check internet/VPN, verify bot token |
| "Invalid API key" | Regenerate OpenAI key, update `.env` |
| Import errors | Run `pip install -r requirements.txt` |

---

## ✨ Features in Detail

### Warm Pastoral Responses
Every reply includes:
- 💖 Loving acknowledgment of user's message
- 📖 Relevant Bible verse with reference
- 🔥 Encouraging message with emojis
- 🎧 3-5 sermon recommendations as separate photo messages

### Smart Recommendation Engine
- **RAG Search**: Semantic search through 669+ sermons
- **AI Ranking**: GPT-4 ranks by relevance to user query
- **Deduplication**: Removes duplicate recommendations
- **Caching**: 6-hour cache for instant repeated queries
- **Fallback**: Graceful degradation if AI fails

### Natural Language Processing
- No strict command syntax required
- Understands: "recommend 3 messages on healing"
- Extracts: topic="healing", num=3
- Responds naturally like a caring friend
- Handles typos and variations gracefully

---

## 📊 Technical Details

### Database Schema
```sql
CREATE TABLE sermons (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    channel TEXT NOT NULL,
    message_link TEXT UNIQUE NOT NULL,
    image_url TEXT,
    date TEXT,
    theme TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Vector Store
- **Engine**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **Dimensions**: 1536
- **Distance**: Cosine similarity
- **Collection**: "sermons"

### Performance
- **Search speed**: <1 second (cached)
- **Initial search**: 2-3 seconds
- **AI response**: 3-5 seconds
- **Total response time**: 5-8 seconds

---

**Built with ❤️ for the Body of Christ**

🔥 _"Let the word of Christ dwell in you richly"_ - Colossians 3:16

---

## 🆘 Quick Reference

```bash
# Start bot
python main.py

# Load sermons
python run_ingest.py

# View all sermons
python view_sermons.py

# Fix search issues
python fix_vector_store.py

# Test setup
python test_imports.py

# Check database count
python -c "from db_handler import SermonDatabase; import config; print(SermonDatabase(config.DB_PATH).get_sermon_count())"

# Monitor logs
tail -f logs/app.log
```

---

For issues or questions, check the logs first, then review the Troubleshooting section above. God bless! ✨
