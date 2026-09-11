import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.security_privacy.privacy_guard import DifferentialPrivacyEngine, SecurityAccessController

class TestSecurityPrivacy(unittest.TestCase):
    def test_differential_privacy(self):
        dp = DifferentialPrivacyEngine(epsilon=1.0)
        vals = [10.0, 12.0, 11.0, 10.5]
        p_mean = dp.private_mean(vals, 0.0, 20.0)
        self.assertIsInstance(p_mean, float)
        self.assertTrue(5.0 <= p_mean <= 18.0)

    def test_access_controller(self):
        sec = SecurityAccessController()
        h = sec.hash_pii("USER_123")
        self.assertEqual(len(h), 64)
        masked = sec.mask_pii({"id": "123", "member_id": "456"}, role="UNDERWRITER")
        self.assertIn("BORROWER_HASH_", masked["id"])
        self.assertTrue(sec.verify_permission("UNDERWRITER", "evaluate_credit"))
        self.assertFalse(sec.verify_permission("BORROWER", "approve_loan"))
