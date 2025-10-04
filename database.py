"""Database module for storing history and tracking content."""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class Database:
    """SQLite database for content tracking and history."""
    
    def __init__(self, db_path: str = "reporter.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                category TEXT,
                collected_at TIMESTAMP,
                used_in_video BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Scripts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                script_text TEXT,
                description TEXT,
                tags TEXT,
                word_count INTEGER,
                estimated_duration INTEGER,
                language TEXT DEFAULT 'en',
                video_generated BOOLEAN DEFAULT 0,
                uploaded BOOLEAN DEFAULT 0,
                youtube_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_id INTEGER,
                file_path TEXT,
                thumbnail_path TEXT,
                video_mode TEXT,
                duration REAL,
                uploaded BOOLEAN DEFAULT 0,
                youtube_id TEXT,
                youtube_url TEXT,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                uploaded_at TIMESTAMP,
                FOREIGN KEY (script_id) REFERENCES scripts(id)
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                watch_time REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        """)
        
        # Upload queue table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS upload_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                scheduled_time TIMESTAMP,
                status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        """)
        
        self.conn.commit()
        print("✓ Database initialized")
    
    def add_article(self, article: Dict) -> int:
        """
        Add article to database.
        
        Returns:
            Article ID or existing ID if duplicate
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO articles (url, title, content, category, collected_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                article['url'],
                article.get('title', ''),
                article.get('content', ''),
                article.get('category', ''),
                article.get('collected_at', datetime.now().isoformat())
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Article already exists
            cursor.execute("SELECT id FROM articles WHERE url = ?", (article['url'],))
            row = cursor.fetchone()
            return row[0] if row else None
    
    def is_article_used(self, url: str) -> bool:
        """Check if article was already used in a video."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT used_in_video FROM articles WHERE url = ?", (url,))
        row = cursor.fetchone()
        return row[0] == 1 if row else False
    
    def mark_articles_used(self, urls: List[str]):
        """Mark articles as used in video."""
        cursor = self.conn.cursor()
        for url in urls:
            cursor.execute("UPDATE articles SET used_in_video = 1 WHERE url = ?", (url,))
        self.conn.commit()
    
    def add_script(self, script_data: Dict) -> int:
        """Add generated script to database."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO scripts (
                title, category, script_text, description, tags,
                word_count, estimated_duration, language
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            script_data.get('title', ''),
            script_data.get('category', ''),
            script_data.get('script', ''),
            script_data.get('description', ''),
            json.dumps(script_data.get('tags', [])),
            script_data.get('word_count', 0),
            script_data.get('estimated_duration', 0),
            script_data.get('language', 'en')
        ))
        
        self.conn.commit()
        script_id = cursor.lastrowid
        
        # Mark source articles as used
        if 'sources' in script_data:
            self.mark_articles_used(script_data['sources'])
        
        return script_id
    
    def add_video(self, video_data: Dict) -> int:
        """Add generated video to database."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO videos (
                script_id, file_path, thumbnail_path, video_mode, duration
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            video_data.get('script_id'),
            video_data.get('file_path', ''),
            video_data.get('thumbnail_path', ''),
            video_data.get('video_mode', ''),
            video_data.get('duration', 0)
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def mark_video_uploaded(self, video_id: int, youtube_url: str, youtube_id: str):
        """Mark video as uploaded to YouTube."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE videos 
            SET uploaded = 1, youtube_url = ?, youtube_id = ?, uploaded_at = ?
            WHERE id = ?
        """, (youtube_url, youtube_id, datetime.now().isoformat(), video_id))
        
        self.conn.commit()
    
    def get_statistics(self, days: int = 30) -> Dict:
        """Get statistics for the last N days."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_scripts,
                COUNT(CASE WHEN video_generated = 1 THEN 1 END) as videos_generated,
                COUNT(CASE WHEN uploaded = 1 THEN 1 END) as videos_uploaded
            FROM scripts
            WHERE created_at >= datetime('now', '-' || ? || ' days')
        """, (days,))
        
        stats = dict(cursor.fetchone())
        
        # Get category breakdown
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM scripts
            WHERE created_at >= datetime('now', '-' || ? || ' days')
            GROUP BY category
        """, (days,))
        
        stats['by_category'] = {row['category']: row['count'] for row in cursor.fetchall()}
        
        return stats
    
    def get_recent_topics(self, category: str, days: int = 7) -> List[str]:
        """Get recent topics to avoid duplicates."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT title FROM scripts
            WHERE category = ? AND created_at >= datetime('now', '-' || ? || ' days')
            ORDER BY created_at DESC
        """, (category, days))
        
        return [row['title'] for row in cursor.fetchall()]
    
    def get_unused_articles(self, category: str, limit: int = 10) -> List[Dict]:
        """Get articles that haven't been used yet."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM articles
            WHERE category = ? AND used_in_video = 0
            ORDER BY collected_at DESC
            LIMIT ?
        """, (category, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


# Singleton instance
_db_instance = None

def get_database() -> Database:
    """Get database singleton instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance

