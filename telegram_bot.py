"""
Telegram bot handler for Pastor Tara Advisor.
Handles all user interactions, commands, and conversations.
"""
import logging
import os
from typing import Dict, List
import hashlib

from telegram import Update, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

import config
from db_handler import SermonDatabase
from utils import (
    rag_engine,
    recommendation_engine,
    response_generator,
    CacheManager
)

logger = logging.getLogger(__name__)


class PastorTaraBot:
    """Main bot class handling all interactions."""
    
    def __init__(self):
        self.db = SermonDatabase(config.DB_PATH)
        self.cache = CacheManager()
        self.user_sessions = {}  # Store ranked sermons for "more" command
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with warm welcome."""
        welcome_message = """✨ *Welcome to Pastor Tara Advisor!* ✨

I'm here to help you grow in faith with teachings from Pastor Tara Akinkuade! 🙏

💬 *Chat naturally with me:*
- "I need encouragement about faith"
- "Recommend 3 sermons on healing"
- "How do I trust God more?"
- "Messages about purpose"

🔥 *Just share your heart, and I'll respond with:*
- A loving acknowledgment 💖
- A Bible verse 📖
- Encouragement ✨
- Relevant sermon recommendations 🎧

📌 *Commands (if you prefer):*
/start - See this welcome message
/recommend <topic> [number] - Get sermon recommendations
/help - View all commands
/more - Get more sermons from your last search

Let's grow together! What's on your heart today? 🌟"""
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown'
        )
        logger.info(f"User {update.effective_user.id} started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """🤝 *How to Use Pastor Tara Advisor*

📱 *Natural Conversation (Recommended):*
Just chat with me naturally! Tell me what you need:
- "I'm struggling with fear"
- "Recommend sermons on prosperity"
- "I need hope today"

⚡ *Commands:*
/start - Welcome message
/recommend <topic> [num] - Get recommendations
  Example: /recommend faith 3
/more - Get next 5 sermons from last search
/help - This help message

💡 *Tips:*
- You can specify how many sermons (1-20)
- Say "more" anytime to continue your search
- Be specific about your needs for best results

God bless you! 🙏✨"""
        
        await update.message.reply_text(
            help_message,
            parse_mode='Markdown'
        )
    
    async def recommend_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /recommend command."""
        user_id = update.effective_user.id
        
        # Parse arguments
        if not context.args:
            await update.message.reply_text(
                "Please provide a topic! 💭\n\nExample: /recommend faith 3"
            )
            return
        
        # Extract topic and number
        args = context.args
        num = config.DEFAULT_RECOMMENDATIONS
        
        # Check if last arg is a number
        if args[-1].isdigit():
            num = min(int(args[-1]), 20)
            topic = ' '.join(args[:-1])
        else:
            topic = ' '.join(args)
        
        # Process recommendation
        await self._process_recommendation(update, user_id, topic, num)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural conversation messages."""
        user_id = update.effective_user.id
        message_text = update.message.text.strip()
        
        # Handle "more" requests
        if message_text.lower() in ['more', 'more sermons', 'show more']:
            await self._handle_more(update, user_id)
            return
        
        # Extract intent
        intent = response_generator.extract_intent(message_text)
        topic = intent['topic']
        num = intent['num_requested']
        
        # Process recommendation
        await self._process_recommendation(update, user_id, topic, num)
    
    async def _process_recommendation(
        self, 
        update: Update, 
        user_id: int, 
        topic: str, 
        num: int
    ):
        """Core recommendation logic."""
        try:
            # Send typing indicator
            await update.message.chat.send_action("typing")
            
            # Step 1: Search with RAG
            logger.info(f"User {user_id} searching for: {topic}")
            search_results = rag_engine.search(topic, k=config.TOP_K_SEARCH)
            
            if not search_results:
                await update.message.reply_text(
                    "🤔 I couldn't find sermons matching that topic. "
                    "Try different keywords or be more specific! 💭"
                )
                return
            
            # Step 2: Rank with AI
            ranked_sermons = recommendation_engine.rank_sermons(
                topic, 
                search_results, 
                user_id
            )
            
            if not ranked_sermons:
                await update.message.reply_text(
                    "🤔 I couldn't find highly relevant sermons for that. "
                    "Try rephrasing your request! 💭"
                )
                return
            
            # Store for "more" command
            self.user_sessions[user_id] = {
                'sermons': ranked_sermons,
                'index': 0
            }
            
            # Step 3: Generate AI response (warm message + verse + encouragement)
            ai_response = response_generator.generate_response(topic, ranked_sermons, num)
            await update.message.reply_text(ai_response, parse_mode='Markdown')
            
            # Step 4: Send sermon recommendations as photo messages
            await self._send_sermon_recommendations(
                update, 
                ranked_sermons[:num],
                user_id
            )
            
            # Update index
            self.user_sessions[user_id]['index'] = num
            
            # Suggest "more" if more sermons available
            if len(ranked_sermons) > num:
                await update.message.reply_text(
                    f"💡 Want more? Just say 'more' to see the next 5 sermons! ✨"
                )
            
        except Exception as e:
            logger.error(f"Error processing recommendation: {e}")
            await update.message.reply_text(
                "🙏 Sorry, I encountered an error. Please try again!"
            )
    
    async def _send_sermon_recommendations(
        self, 
        update: Update, 
        sermons: List[Dict],
        user_id: int
    ):
        """Send each sermon as a separate photo message."""
        for sermon in sermons:
            try:
                # Format caption
                caption = self._format_sermon_caption(sermon)
                
                # Send as photo if image available, otherwise as text
                if sermon.get('image_url'):
                    try:
                        await update.message.reply_photo(
                            photo=sermon['image_url'],
                            caption=caption,
                            parse_mode='Markdown'
                        )
                    except Exception:
                        # Fallback to text if image fails
                        await update.message.reply_text(caption, parse_mode='Markdown')
                else:
                    # No image, send as text with emoji
                    await update.message.reply_text(f"🎧 {caption}", parse_mode='Markdown')
                
                logger.info(f"Sent sermon to user {user_id}: {sermon['title']}")
                
            except Exception as e:
                logger.error(f"Error sending sermon: {e}")
    
    def _format_sermon_caption(self, sermon: Dict) -> str:
        """Format sermon data into a beautiful caption."""
        title = sermon.get('title', 'Untitled')
        description = sermon.get('description', 'No description available')
        link = sermon.get('message_link', '')
        
        caption = f"""*{title}*

{description}

✨ _Listen. Share. Be Transformed._ ✨

🔗 {link}"""
        
        return caption
    
    async def _handle_more(self, update: Update, user_id: int):
        """Handle 'more' requests to get next batch of sermons."""
        if user_id not in self.user_sessions:
            await update.message.reply_text(
                "🤔 Please search for sermons first before asking for more!"
            )
            return
        
        session = self.user_sessions[user_id]
        sermons = session['sermons']
        current_index = session['index']
        
        # Get next 5 sermons
        next_batch = sermons[current_index:current_index + 5]
        
        if not next_batch:
            await update.message.reply_text(
                "✅ That's all the sermons I found for your search! "
                "Try a new search for more. 🙏"
            )
            return
        
        # Send next batch
        await update.message.reply_text("🎧 Here are more sermons for you:")
        await self._send_sermon_recommendations(update, next_batch, user_id)
        
        # Update index
        session['index'] = current_index + 5
        
        # Check if more available
        if session['index'] < len(sermons):
            await update.message.reply_text(
                "💡 Still more available! Say 'more' again. ✨"
            )
        else:
            await update.message.reply_text(
                "✅ That's all! Try a new search for different sermons. 🙏"
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors gracefully."""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "🙏 Oops! Something went wrong. Please try again or contact support."
            )


def setup_bot() -> Application:
    """Setup and configure the bot."""
    # Create application
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    # Initialize bot handler
    bot = PastorTaraBot()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("recommend", bot.recommend_command))
    
    # Add message handler for natural conversation
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        bot.handle_message
    ))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    logger.info("Bot handlers configured successfully")
    return application