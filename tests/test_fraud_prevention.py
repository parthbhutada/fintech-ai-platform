import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.fraud_prevention.anomaly_detector import FraudAnomalyDetector

class TestFraud(unittest.TestCase):
    def test_anomaly_detection(self):
        detector = FraudAnomalyDetector()
        clean_app = {"id": "C1", "loan_amnt": 5000.0, "annual_inc": 60000.0, "inq_last_6mths": 0}
        res_clean = detector.analyze_application(clean_app)
        self.assertEqual(res_clean["fraud_risk_tier"], "LOW")

        fraud_app = {"id": "F1", "loan_amnt": 35000.0, "annual_inc": 20000.0, "inq_last_6mths": 7}
        res_fraud = detector.analyze_application(fraud_app)
        self.assertIn(res_fraud["fraud_risk_tier"], ["HIGH", "CRITICAL"])
        self.assertTrue(res_fraud["is_flagged"])
