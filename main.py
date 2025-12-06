"""
Main entry point for Pastor Tara Advisor bot.
Starts the bot and keeps it running.
"""
import logging
import sys
import os
import time

# Fix Windows console encoding FIRST
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from telegram import Update
from telegram.error import TimedOut, NetworkError

import config
from telegram_bot import setup_bot

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
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to start the bot."""
    logger.info("=" * 60)
    logger.info("Starting Pastor Tara Advisor Bot")
    logger.info("=" * 60)
    
    # Validate configuration
    if not config.TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env file!")
        sys.exit(1)
    
    if not config.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not found in .env file!")
        sys.exit(1)
    
    logger.info("Configuration loaded successfully")
    
    # Retry loop for network issues
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            application = setup_bot()
            logger.info("Bot initialized successfully")
            logger.info("Bot is now running! Press Ctrl+C to stop.")
            logger.info("=" * 60)
            
            # Start bot (polling mode) with custom settings
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                connect_timeout=30.0,
                read_timeout=30.0,
                write_timeout=30.0,
                pool_timeout=30.0
            )
            break  # If successful, exit loop
            
        except (TimedOut, NetworkError) as e:
            retry_count += 1
            logger.warning(f"Connection failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                wait_time = retry_count * 5  # Progressive backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached. Please check your internet connection.")
                logger.error("Possible issues:")
                logger.error("1. Telegram servers blocked in your region (use VPN)")
                logger.error("2. Firewall blocking connection")
                logger.error("3. Internet connection unstable")
                sys.exit(1)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
            
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()