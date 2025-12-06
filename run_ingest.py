"""
Run this script to ingest all data:
- Scrape the 4 Telegram channels
- Load materials from materials/ folder

Usage: python run_ingest.py
"""
import asyncio
import logging
import sys
import os

import config
from rag_ingest import ChannelScraper, MaterialsLoader

# Create necessary directories
os.makedirs('logs', exist_ok=True)
os.makedirs('db', exist_ok=True)
os.makedirs('cache', exist_ok=True)
os.makedirs(config.MATERIALS_PATH, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ingest.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main ingestion process."""
    print("🚀 Starting data ingestion...")
    print("=" * 50)
    
    try:
        # Step 1: Scrape Telegram channels
        print("\n📡 Scraping Telegram channels...")
        scraper = ChannelScraper()
        sermons = await scraper.scrape_all_channels()
        print(f"✅ Scraped {len(sermons)} sermons from channels")
        
        # Step 2: Load materials from folder
        print("\n📁 Loading materials from folder...")
        loader = MaterialsLoader()
        loader.load_all_materials()
        print("✅ Materials loaded successfully")
        
        # Summary
        from db_handler import SermonDatabase
        db = SermonDatabase(config.DB_PATH)
        total_count = db.get_sermon_count()
        
        print("\n" + "=" * 50)
        print(f"🎉 All files loaded!")
        print(f"📊 Total sermons in database: {total_count}")
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())