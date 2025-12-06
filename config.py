"""
Configuration loader for the Pastor Tara Advisor bot.
Loads all environment variables from .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ADMIN_IDS = [int(id.strip()) for id in os.getenv("TELEGRAM_ADMIN_IDS", "").split(",") if id.strip()]

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Telegram API for scraping (get from my.telegram.org)
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")

# Channels to scrape
CHANNELS_TO_SCRAPE = [
    "@pst_tara",
    "@TheSupernaturalBusinessMan",
    "@TheSupernaturalFamily",
    "@TheSupernaturalStudent"
]

# Database paths
DB_PATH = "db/sermons.db"
CHROMA_PATH = "db/chroma"
CACHE_PATH = "cache"
MATERIALS_PATH = "materials"
LOGS_PATH = "logs"

# AI Configuration
AI_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CACHE_DURATION_HOURS = 6

# Search Configuration
TOP_K_SEARCH = 20  # Initial retrieval
MIN_RELEVANCE_SCORE = 0.7  # Minimum score to recommend
DEFAULT_RECOMMENDATIONS = 5  # Default number of recommendations