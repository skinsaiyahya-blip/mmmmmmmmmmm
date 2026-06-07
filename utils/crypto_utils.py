import json
import base64
import os

def is_windows():
    """Check if running on Windows"""
    return os.name == 'nt'

def decrypt_windows_dpapi(encrypted_data):
    """Decrypt Windows DPAPI encrypted data"""
    if not is_windows():
        return None
    
    try:
        import win32crypt
        return win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)[1].decode()
    except:
        return "[ENCRYPTED - Cannot decrypt without credentials]"

def decode_base64(data):
    """Decode base64 string"""
    try:
        return base64.b64decode(data).decode()
    except:
        return None

def encode_base64(data):
    """Encode string to base64"""
    try:
        return base64.b64encode(data.encode()).decode()
    except:
        return None
