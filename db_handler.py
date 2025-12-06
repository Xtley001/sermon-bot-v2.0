"""
Database handler for storing and retrieving sermon data.
Uses SQLite for fast, reliable storage of thousands of sermons.
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os

logger = logging.getLogger(__name__)


class SermonDatabase:
    """Handles all database operations for sermons."""
    
    def __init__(self, db_path: str):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Create tables with optimized schema for thousands of records."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main sermons table with indexes for fast search
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sermons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                channel TEXT NOT NULL,
                message_link TEXT UNIQUE NOT NULL,
                image_url TEXT,
                date TEXT,
                theme TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_channel ON sermons(channel)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON sermons(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_theme ON sermons(theme)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON sermons(title)")
        
        # Full-text search index for title and description
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS sermons_fts USING fts5(
                title, description, theme, content='sermons', content_rowid='id'
            )
        """)
        
        # Trigger to keep FTS table in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS sermons_ai AFTER INSERT ON sermons BEGIN
                INSERT INTO sermons_fts(rowid, title, description, theme)
                VALUES (new.id, new.title, new.description, new.theme);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS sermons_ad AFTER DELETE ON sermons BEGIN
                DELETE FROM sermons_fts WHERE rowid = old.id;
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS sermons_au AFTER UPDATE ON sermons BEGIN
                UPDATE sermons_fts SET title=new.title, description=new.description, 
                    theme=new.theme WHERE rowid=new.id;
            END
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_sermon(self, sermon_data: Dict) -> Optional[int]:
        """Add a new sermon to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO sermons 
                (title, description, channel, message_link, image_url, date, theme)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                sermon_data.get('title', ''),
                sermon_data.get('description', ''),
                sermon_data.get('channel', ''),
                sermon_data.get('message_link', ''),
                sermon_data.get('image_url'),
                sermon_data.get('date'),
                sermon_data.get('theme', '')
            ))
            
            sermon_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Added sermon: {sermon_data.get('title', 'Untitled')}")
            return sermon_id
            
        except sqlite3.IntegrityError:
            logger.debug(f"Sermon already exists: {sermon_data.get('message_link')}")
            return None
        except Exception as e:
            logger.error(f"Error adding sermon: {e}")
            return None
    
    def get_sermon_by_link(self, message_link: str) -> Optional[Dict]:
        """Get a sermon by its message link."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sermons WHERE message_link = ?", (message_link,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all_sermons(self) -> List[Dict]:
        """Get all sermons from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sermons ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def search_sermons(self, query: str, limit: int = 50) -> List[Dict]:
        """Full-text search in sermons."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Use FTS5 for fast full-text search
        cursor.execute("""
            SELECT s.* FROM sermons s
            JOIN sermons_fts fts ON s.id = fts.rowid
            WHERE sermons_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_sermons_by_channel(self, channel: str) -> List[Dict]:
        """Get all sermons from a specific channel."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sermons WHERE channel = ? ORDER BY date DESC", (channel,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_sermon_count(self) -> int:
        """Get total number of sermons in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sermons")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def delete_all_sermons(self):
        """Delete all sermons (admin only)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sermons")
        conn.commit()
        conn.close()
        
        logger.info("All sermons deleted from database")