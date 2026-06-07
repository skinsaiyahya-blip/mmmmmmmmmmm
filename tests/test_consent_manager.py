import unittest
from core.consent_manager import ConsentManager

class TestConsentManager(unittest.TestCase):
    """Test consent manager"""
    
    def setUp(self):
        self.manager = ConsentManager()
    
    def test_log_consent(self):
        """Test logging consent"""
        user_id = "test_user_123"
        self.manager.log_consent(user_id, "test_action", True, "test_details")
        
        # Check if consent was logged
        has_consent = self.manager.has_consent(user_id, "test_action")
        self.assertTrue(has_consent)
    
    def test_revoke_consent(self):
        """Test revoking consent"""
        user_id = "test_user_456"
        self.manager.log_consent(user_id, "test_action", True)
        self.manager.revoke_all_consent(user_id)
        
        has_consent = self.manager.has_consent(user_id, "test_action")
        self.assertFalse(has_consent)

if __name__ == '__main__':
    unittest.main()
