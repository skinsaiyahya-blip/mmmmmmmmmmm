import sqlite3
import json
from datetime import datetime
from config import CONSENT_DB_FILE
import os

class ConsentManager:
    """Manages user consent for scanning operations"""
    
    def __init__(self):
        self.db_file = CONSENT_DB_FILE
        self.init_db()
        self.log_file = "consent_log.txt"
    
    def init_db(self):
        """Initialize consent database"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consent (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                action TEXT,
                granted BOOLEAN,
                timestamp DATETIME,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def log_consent(self, user_id, action, granted, details=""):
        """Log consent action"""
        timestamp = datetime.now().isoformat()
        
        # Log to text file
        with open(self.log_file, "a") as f:
            status = "GRANTED" if granted else "DENIED"
            f.write(f"[{timestamp}] USER:{user_id} ACTION:{action} STATUS:{status} DETAILS:{details}\n")
        
        # Log to database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO consent (user_id, action, granted, timestamp, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(user_id), action, granted, timestamp, details))
        conn.commit()
        conn.close()
    
    def has_consent(self, user_id, action):
        """Check if user has granted consent for action"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT granted FROM consent 
            WHERE user_id = ? AND action = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (str(user_id), action))
        result = cursor.fetchone()
        conn.close()
        
        return result and result[0]
    
    def revoke_all_consent(self, user_id):
        """Revoke all consents for user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Mark all as revoked
        cursor.execute('''
            UPDATE consent SET granted = 0 
            WHERE user_id = ?
        ''', (str(user_id),))
        
        conn.commit()
        conn.close()
        
        self.log_consent(user_id, "revoke_all", True, "All consents revoked")
