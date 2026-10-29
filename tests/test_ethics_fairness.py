import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ethics_fairness.bias_auditor import BiasAuditor

class TestEthics(unittest.TestCase):
    def test_bias_auditor(self):
        auditor = BiasAuditor(disparate_impact_threshold=0.80)
        records = [
            {"application_type": "Individual"},
            {"application_type": "Individual"},
            {"application_type": "Joint App"},
            {"application_type": "Joint App"}
        ]
        decisions = ["APPROVED", "APPROVED", "APPROVED", "DENIED"]
        res = auditor.audit_decisions(records, decisions, "application_type", "Individual")
        self.assertIn("disparate_impact_ratio", res)
        self.assertEqual(res["privileged_approval_rate"], 1.0)
        self.assertEqual(res["unprivileged_approval_rate"], 0.5)
        self.assertEqual(res["disparate_impact_ratio"], 0.5)
        self.assertFalse(res["four_fifths_rule_passed"])

        calibrated = auditor.calibrate_fair_thresholds(0.5, res["disparate_impact_ratio"])
        self.assertIn("unprivileged_threshold", calibrated)
