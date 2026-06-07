import os
from utils.path_utils import get_ssh_path

class SSHScanner:
    """Scan for SSH keys and config"""
    
    SSH_KEY_NAMES = ['id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519', 'id_rsa.pub', 'config']
    
    def scan_ssh_keys(self):
        """Scan SSH directory for keys"""
        keys = []
        ssh_path = get_ssh_path()
        
        if not os.path.exists(ssh_path):
            return keys
        
        try:
            for filename in os.listdir(ssh_path):
                if filename in self.SSH_KEY_NAMES or filename.startswith('id_'):
                    filepath = os.path.join(ssh_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            keys.append({
                                "filename": filename,
                                "path": filepath,
                                "size": len(content),
                                "is_private": not filename.endswith('.pub') and 'PRIVATE' in content
                            })
                    except Exception as e:
                        pass
        except Exception as e:
            pass
        
        return keys
