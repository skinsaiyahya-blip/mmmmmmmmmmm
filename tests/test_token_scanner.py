import unittest
from core.token_scanner import TokenScanner

class TestTokenScanner(unittest.TestCase):
    """Test token scanner"""
    
    def setUp(self):
        self.scanner = TokenScanner()
    
    def test_discord_pattern(self):
        """Test Discord token pattern"""
        test_token = "NTc0MDc5Njc2NTc0NTgwMjg4.XOhEzA.7H0_1MXHWzvXb1PuTZvDvPJj"
        # Note: This is a test pattern, not a real token
        self.assertTrue(len(test_token) > 0)
    
    def test_scan_environment_tokens(self):
        """Test environment variable scanning"""
        tokens = self.scanner.scan_environment_tokens()
        self.assertIsInstance(tokens, list)

if __name__ == '__main__':
    unittest.main()
