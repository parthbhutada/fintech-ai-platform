import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.trading_portfolio.portfolio_allocator import PortfolioAllocator

class TestTradingPortfolio(unittest.TestCase):
    def test_portfolio_optimization(self):
        allocator = PortfolioAllocator(risk_free_rate=0.04)
        res = allocator.optimize_allocation()
        self.assertIn("ai_optimal_tangency_portfolio", res)
        opt = res["ai_optimal_tangency_portfolio"]
        self.assertGreater(opt["sharpe_ratio"], 0)
        tot_weight = sum(opt["allocation_weights"].values())
        self.assertAlmostEqual(tot_weight, 1.0, places=1)
