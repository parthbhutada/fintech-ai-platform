import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.biometrics.biometric_auth import BiometricAuthenticationEngine

class TestBiometrics(unittest.TestCase):
    def test_biometric_auth(self):
        engine = BiometricAuthenticationEngine()
        user_id = "USER_99"
        template = [0.2, 0.5, 0.8, 0.1]
        engine.enroll_user(user_id, template)

        # Same template should pass
        res = engine.verify_biometric(user_id, template, liveness_score=0.95)
        self.assertTrue(res["authenticated"])

        # Different template should fail
        impostor = [-0.8, -0.2, 0.1, 0.9]
        res_fail = engine.verify_biometric(user_id, impostor, liveness_score=0.95)
        self.assertFalse(res_fail["authenticated"])
