import os
import re
from pathlib import Path

class EnvScanner:
    """Scan for secrets in .env and config files"""
    
    ENV_FILES = ['.env', '.env.local', '.env.production', 'config.env']
    SECRET_PATTERNS = {
        'discord_token': r'DISCORD[_-]TOKEN\s*=\s*([^\s]+)',
        'api_key': r'API[_-]KEY\s*=\s*([^\s]+)',
        'aws_key': r'AWS[_-]ACCESS[_-]KEY[_-]ID\s*=\s*([^\s]+)',
        'password': r'PASSWORD\s*=\s*([^\s]+)',
        'secret': r'SECRET\s*=\s*([^\s]+)',
        'github_token': r'GITHUB[_-]TOKEN\s*=\s*([^\s]+)',
    }
    
    def scan_env_files(self, start_path=None):
        """Scan for .env files with secrets"""
        secrets = []
        
        if start_path is None:
            start_path = os.path.expanduser("~")
        
        try:
            for root, dirs, files in os.walk(start_path):
                # Skip system directories
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
                
                for filename in files:
                    if filename in self.ENV_FILES:
                        filepath = os.path.join(root, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                for pattern_name, pattern in self.SECRET_PATTERNS.items():
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    for match in matches:
                                        secrets.append({
                                            "file": filepath,
                                            "type": pattern_name,
                                            "value": match[:50] + "..." if len(match) > 50 else match
                                        })
                        except Exception as e:
                            pass
        except Exception as e:
            pass
        
        return secrets
