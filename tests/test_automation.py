import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.automation.orchestrator import FinTechSTPOrchestrator
from src.automation.rpa_engine import RPAIngestionBot

class TestAutomation(unittest.TestCase):
    def test_rpa_validation(self):
        rpa = RPAIngestionBot()
        valid_res = rpa.validate_document_rules({"id": "A1", "loan_amnt": "10000", "annual_inc": "50000"})
        self.assertTrue(valid_res["passed_validation"])

    def test_orchestrator_stp(self):
        orch = FinTechSTPOrchestrator()
        app = {
            "id": "STP_TEST_01",
            "loan_amnt": 12000.0,
            "annual_inc": 75000.0,
            "fico_range_high": 720.0,
            "dti": 14.5,
            "revol_util": 22.0,
            "purpose": "debt_consolidation",
            "title": "Debt Consolidation"
        }
        res = orch.process_application_stp(app)
        self.assertIn("underwriting_decision", res)
        self.assertIn("blockchain_audit_receipt", res)
        self.assertTrue(res["straight_through_processing_latency_ms"] >= 0)
