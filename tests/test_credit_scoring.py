import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.credit_scoring.automl import AutoMLCreditScorer
from src.credit_scoring.underwriting import UnderwritingEngine

class TestCreditScoring(unittest.TestCase):
    def test_automl_training(self):
        scorer = AutoMLCreditScorer()
        X_train = [[0.5, 1.2], [-0.8, -0.4], [1.1, 0.9], [-1.2, -1.0]]
        y_train = [1, 0, 1, 0]
        X_val = [[0.6, 1.0], [-0.5, -0.2]]
        y_val = [1, 0]
        res = scorer.train_and_select(X_train, y_train, X_val, y_val, ["feat1", "feat2"])
        self.assertIn("best_model_name", res)
        self.assertGreater(len(res["leaderboard"]), 0)
        probs = scorer.predict_default_probability(X_val)
        self.assertEqual(len(probs), 2)
        self.assertTrue(0.0 <= probs[0] <= 1.0)

    def test_underwriting_engine(self):
        engine = UnderwritingEngine()
        applicant = {
            "id": "T1",
            "fico_range_high": 780,
            "dti": 12.0,
            "annual_inc": 110000.0,
            "loan_amnt": 15000.0,
            "revol_util": 15.0
        }
        res = engine.evaluate_application(applicant)
        self.assertIn(res["decision"], ["APPROVED", "CONDITIONALLY_APPROVED", "MANUAL_REVIEW", "DENIED"])
        self.assertEqual(res["assigned_grade"], "A")
