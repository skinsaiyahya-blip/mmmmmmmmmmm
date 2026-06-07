import os
from pathlib import Path

def read_file(filepath, encoding='utf-8'):
    """Safely read file contents"""
    try:
        with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
            return f.read()
    except Exception as e:
        return None

def write_file(filepath, content, encoding='utf-8'):
    """Safely write to file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def find_files(directory, pattern="*", recursive=False):
    """Find files matching pattern"""
    try:
        path = Path(directory)
        if recursive:
            return list(path.rglob(pattern))
        else:
            return list(path.glob(pattern))
    except Exception as e:
        return []

def safe_remove(filepath):
    """Safely remove file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception as e:
        return False
