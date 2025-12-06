"""
Utility functions for AI interactions, RAG search, and recommendation ranking.
This is the brain of the bot - handles intelligent sermon recommendations.
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

import config

logger = logging.getLogger(__name__)

# Set OpenAI API key as environment variable (required for langchain-openai 0.2.0)
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

# Initialize AI components without passing api_key directly
embeddings = OpenAIEmbeddings(
    model=config.EMBEDDING_MODEL
)

llm = ChatOpenAI(
    model=config.AI_MODEL,
    temperature=0.7
)


class RAGEngine:
    """Handles vector storage and semantic search for sermons."""
    
    def __init__(self):
        """Initialize Chroma vector store."""
        os.makedirs(config.CHROMA_PATH, exist_ok=True)
        
        self.vectorstore = Chroma(
            persist_directory=config.CHROMA_PATH,
            embedding_function=embeddings,
            collection_name="sermons"
        )
        logger.info("RAG Engine initialized")
    
    def add_documents(self, documents: List[Document]):
        """Add documents to vector store."""
        if not documents:
            return
        
        try:
            self.vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
    
    def search(self, query: str, k: int = 20) -> List[Dict]:
        """
        Semantic search for relevant sermons.
        Returns top k most relevant sermons with metadata.
        """
        try:
            # Perform similarity search
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Format results
            sermons = []
            for doc, score in results:
                sermon = {
                    'title': doc.metadata.get('title', 'Untitled'),
                    'description': doc.metadata.get('description', ''),
                    'message_link': doc.metadata.get('message_link', ''),
                    'image_url': doc.metadata.get('image_url'),
                    'channel': doc.metadata.get('channel', ''),
                    'date': doc.metadata.get('date', ''),
                    'theme': doc.metadata.get('theme', ''),
                    'similarity_score': float(1 - score)  # Convert distance to similarity
                }
                sermons.append(sermon)
            
            logger.info(f"Found {len(sermons)} results for query: {query[:50]}")
            return sermons
            
        except Exception as e:
            logger.error(f"Error in RAG search: {e}")
            return []
    
    def clear_all(self):
        """Clear all documents from vector store."""
        try:
            # Delete and recreate collection
            self.vectorstore.delete_collection()
            self.vectorstore = Chroma(
                persist_directory=config.CHROMA_PATH,
                embedding_function=embeddings,
                collection_name="sermons"
            )
            logger.info("Vector store cleared")
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")


class RecommendationEngine:
    """Intelligently ranks and filters sermon recommendations."""
    
    def __init__(self):
        self.cache = CacheManager()
    
    def rank_sermons(self, query: str, sermons: List[Dict], user_id: int) -> List[Dict]:
        """
        Use AI to intelligently rank sermons by relevance.
        Filters out low-quality matches and removes duplicates.
        """
        if not sermons:
            return []
        
        # Check cache first
        cache_key = f"rank_{user_id}_{hashlib.md5(query.encode()).hexdigest()}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Using cached ranking for user {user_id}")
            return cached
        
        try:
            # Prepare sermon summaries for AI
            sermon_summaries = []
            for i, sermon in enumerate(sermons):
                summary = f"{i}. {sermon['title']}\n{sermon['description'][:200]}..."
                sermon_summaries.append(summary)
            
            # Ask AI to rank by relevance
            prompt = f"""You are helping recommend sermons from Pastor Tara Akinkuade.

User query: "{query}"

Available sermons:
{chr(10).join(sermon_summaries[:15])}

Task: Return a JSON array of sermon indexes (0-{min(14, len(sermon_summaries)-1)}) ranked by relevance to the query.
Only include sermons that are truly relevant (relevance score >= 0.7).
Return ONLY the JSON array, nothing else.

Example: [3, 0, 7, 1]
"""
            
            response = llm.invoke(prompt)
            content = response.content.strip()
            
            # Parse AI response
            if content.startswith('[') and content.endswith(']'):
                ranked_indexes = json.loads(content)
            else:
                # Fallback: use original order
                ranked_indexes = list(range(min(10, len(sermons))))
            
            # Reorder sermons based on AI ranking
            ranked_sermons = []
            seen_links = set()
            
            for idx in ranked_indexes:
                if 0 <= idx < len(sermons):
                    sermon = sermons[idx]
                    link = sermon['message_link']
                    
                    # Remove duplicates
                    if link not in seen_links:
                        ranked_sermons.append(sermon)
                        seen_links.add(link)
            
            # Cache the results
            self.cache.set(cache_key, ranked_sermons)
            
            logger.info(f"Ranked {len(ranked_sermons)} sermons for query: {query[:50]}")
            return ranked_sermons
            
        except Exception as e:
            logger.error(f"Error ranking sermons: {e}")
            # Fallback: return original sermons filtered by similarity score
            return [s for s in sermons if s.get('similarity_score', 0) >= config.MIN_RELEVANCE_SCORE]


class ResponseGenerator:
    """Generates warm, pastoral responses with AI."""
    
    def generate_response(self, query: str, sermons: List[Dict], num_requested: int = 5) -> str:
        """
        Generate a warm, encouraging response with Bible verse.
        Does NOT include sermon recommendations (those are sent separately as photos).
        """
        try:
            prompt = f"""You are Pastor Tara Akinkuade's AI assistant, helping people with spiritual guidance.

User message: "{query}"

Task: Respond with warmth and pastoral care:
1. Acknowledge their message with love and empathy
2. Share ONE relevant Bible verse (book chapter:verse format)
3. Give brief encouragement with emojis (📖 🙏 🔥 ✨ 💖)

Keep it SHORT (3-4 sentences max). Be warm, natural, and uplifting.
DO NOT mention sermon recommendations - those will be sent separately.

Example tone:
"I hear your heart, beloved! 🙏 Remember, *'Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.'* - Joshua 1:9 📖 God is with you in this season, and His word will guide you! ✨"
"""
            
            response = llm.invoke(prompt)
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "🙏 Thank you for reaching out! God bless you, and may His word minister to your heart today. ✨"
    
    def extract_intent(self, message: str) -> Dict:
        """
        Extract user intent: topic and number of recommendations requested.
        """
        try:
            # Simple pattern matching for number
            num = config.DEFAULT_RECOMMENDATIONS
            for word in message.split():
                if word.isdigit():
                    num = min(int(word), 20)  # Max 20 at once
                    break
            
            # Topic is the whole message (RAG will handle it)
            return {
                'topic': message,
                'num_requested': num
            }
            
        except Exception as e:
            logger.error(f"Error extracting intent: {e}")
            return {
                'topic': message,
                'num_requested': config.DEFAULT_RECOMMENDATIONS
            }


class CacheManager:
    """Simple file-based caching for fast responses."""
    
    def __init__(self):
        os.makedirs(config.CACHE_PATH, exist_ok=True)
    
    def get(self, key: str) -> Optional[any]:
        """Get cached data if not expired."""
        cache_file = os.path.join(config.CACHE_PATH, f"{key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check expiration
            expires_at = datetime.fromisoformat(data['expires_at'])
            if datetime.now() > expires_at:
                os.remove(cache_file)
                return None
            
            return data['value']
            
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def set(self, key: str, value: any):
        """Cache data with expiration."""
        cache_file = os.path.join(config.CACHE_PATH, f"{key}.json")
        
        expires_at = datetime.now() + timedelta(hours=config.CACHE_DURATION_HOURS)
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'value': value,
                    'expires_at': expires_at.isoformat()
                }, f)
        except Exception as e:
            logger.error(f"Error writing cache: {e}")


# Global instances - initialized when module is imported
rag_engine = RAGEngine()
recommendation_engine = RecommendationEngine()
response_generator = ResponseGenerator()