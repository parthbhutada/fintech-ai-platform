import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.risk_management.portfolio_risk import PortfolioRiskManager

class TestRiskManagement(unittest.TestCase):
    def test_portfolio_risk(self):
        mgr = PortfolioRiskManager()
        loans = [
            {"loan_amnt": 10000.0, "grade": "A", "addr_state": "CA"},
            {"loan_amnt": 20000.0, "grade": "C", "addr_state": "NY"},
            {"loan_amnt": 15000.0, "grade": "E", "addr_state": "TX"}
        ]
        res = mgr.analyze_portfolio(loans)
        self.assertEqual(res["total_portfolio_exposure_usd"], 45000.0)
        self.assertGreater(res["value_at_risk_95_pct"], 0)
        self.assertGreater(res["value_at_risk_99_pct"], res["value_at_risk_95_pct"])
        self.assertIn("stress_testing", res)
