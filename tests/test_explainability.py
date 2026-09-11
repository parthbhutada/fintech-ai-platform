import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainability.xai_engine import ExplainableAIEngine

class TestExplainability(unittest.TestCase):
    def test_xai_engine(self):
        xai = ExplainableAIEngine()
        applicant = {
            "id": "X1",
            "fico_range_high": 640,
            "dti": 32.0,
            "annual_inc": 42000.0,
            "revol_util": 68.0,
            "inq_last_6mths": 3
        }
        res = xai.explain_instance(applicant)
        self.assertIn("local_feature_attributions", res)
        self.assertIn("actionable_counterfactuals", res)
        self.assertGreater(len(res["top_risk_elevating_factors"]), 0)
        self.assertGreater(len(res["actionable_counterfactuals"]), 0)
