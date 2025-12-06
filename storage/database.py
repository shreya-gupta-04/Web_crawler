import sqlite3
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for storing crawled pages"""
    
    def __init__(self, db_path: str = "crawler.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create pages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                text TEXT,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create words table for inverted index
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                document_frequency INTEGER DEFAULT 0
            )
        ''')
        
        # Create word-page mapping table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_page (
                word_id INTEGER NOT NULL,
                page_id INTEGER NOT NULL,
                term_frequency REAL DEFAULT 0,
                PRIMARY KEY (word_id, page_id),
                FOREIGN KEY (word_id) REFERENCES words(id),
                FOREIGN KEY (page_id) REFERENCES pages(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized: {self.db_path}")
    
    def insert_page(self, url: str, title: str, text: str) -> Optional[int]:
        """Insert a crawled page"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pages (url, title, text)
                VALUES (?, ?, ?)
            ''', (url, title, text))
            
            page_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return page_id
        except sqlite3.IntegrityError:
            logger.warning(f"Page already exists: {url}")
            return None
        except Exception as e:
            logger.error(f"Error inserting page: {e}")
            return None
    
    def get_page(self, url: str) -> Optional[Dict]:
        """Retrieve a page by URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, url, title, text, crawled_at FROM pages WHERE url = ?', (url,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'text': row[3],
                'crawled_at': row[4]
            }
        return None
    
    def get_all_pages(self) -> List[Dict]:
        """Retrieve all pages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, url, title, text, crawled_at FROM pages')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'text': row[3],
                'crawled_at': row[4]
            }
            for row in rows
        ]
    
    def insert_word(self, word: str, document_frequency: int = 0) -> Optional[int]:
        """Insert a word into the index"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO words (word, document_frequency)
                VALUES (?, ?)
            ''', (word, document_frequency))
            
            cursor.execute('SELECT id FROM words WHERE word = ?', (word,))
            word_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return word_id
        except Exception as e:
            logger.error(f"Error inserting word: {e}")
            return None
    
    def link_word_to_page(self, word_id: int, page_id: int, tf: float):
        """Link a word to a page with TF score"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO word_page (word_id, page_id, term_frequency)
                VALUES (?, ?, ?)
            ''', (word_id, page_id, tf))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error linking word to page: {e}")
    
    def update_document_frequency(self, word_id: int):
        """Update document frequency for a word"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE words
                SET document_frequency = (
                    SELECT COUNT(DISTINCT page_id) FROM word_page WHERE word_id = ?
                )
                WHERE id = ?
            ''', (word_id, word_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error updating document frequency: {e}")
    
    def search_pages_by_word(self, word: str) -> List[Dict]:
        """Search pages containing a word"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.url, p.title, p.text, wp.term_frequency
            FROM pages p
            JOIN word_page wp ON p.id = wp.page_id
            JOIN words w ON wp.word_id = w.id
            WHERE w.word = ?
            ORDER BY wp.term_frequency DESC
        ''', (word.lower(),))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'text': row[3],
                'tf': row[4]
            }
            for row in rows
        ]
    
    def clear_database(self):
        """Clear all data (use with caution)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM word_page')
        cursor.execute('DELETE FROM words')
        cursor.execute('DELETE FROM pages')
        
        conn.commit()
        conn.close()
        logger.info("Database cleared")
