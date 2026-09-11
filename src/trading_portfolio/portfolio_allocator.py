"""
AI Trading & Loan Portfolio Optimization Engine.
Applies Modern Portfolio Theory (Markowitz Mean-Variance framework)
to peer-to-peer loan assets to compute the Efficient Frontier, maximize Sharpe Ratio,
and determine risk-budgeted capital allocation.
"""

import math
from typing import List, Dict, Any, Tuple

class PortfolioAllocator:
    def __init__(self, risk_free_rate: float = 0.045):
        """
        risk_free_rate: Benchmark US Treasury risk-free rate (e.g., 4.5%).
        """
        self.rf = risk_free_rate

    def optimize_allocation(self, loan_grades: List[str] = None,
                            interest_rates: Dict[str, float] = None,
                            default_probs: Dict[str, float] = None,
                            lgd: float = 0.45) -> Dict[str, Any]:
        grades = loan_grades or ["Grade_A", "Grade_B", "Grade_C", "Grade_D", "Grade_E"]
        rates = interest_rates or {
            "Grade_A": 0.075,
            "Grade_B": 0.115,
            "Grade_C": 0.155,
            "Grade_D": 0.195,
            "Grade_E": 0.245
        }
        pds = default_probs or {
            "Grade_A": 0.035,
            "Grade_B": 0.085,
            "Grade_C": 0.155,
            "Grade_D": 0.245,
            "Grade_E": 0.350
        }

        # Expected Net Return per asset: E[R] = Coupon - (PD * LGD)
        expected_returns = {g: round(rates[g] - (pds[g] * lgd), 4) for g in grades}

        # Volatility / Variance approximation based on default variance Bernoulli(PD): sigma = LGD * sqrt(PD * (1 - PD))
        volatilities = {g: round(lgd * math.sqrt(pds[g] * (1.0 - pds[g])), 4) for g in grades}

        # Candidate asset weights optimization (Grid search over simplex to maximize Sharpe ratio)
        best_weights = {}
        best_sharpe = -float("inf")
        best_ret = 0.0
        best_vol = 0.0

        # Discretized simplex generation for 5 assets
        steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        for w_a in [0.1, 0.2, 0.3, 0.4, 0.5]:
            for w_b in [0.1, 0.2, 0.3, 0.4]:
                for w_c in [0.0, 0.1, 0.2, 0.3]:
                    for w_d in [0.0, 0.05, 0.1, 0.15]:
                        w_e = round(1.0 - (w_a + w_b + w_c + w_d), 2)
                        if w_e < 0 or w_e > 0.15:
                            continue

                        weights = {
                            "Grade_A": w_a, "Grade_B": w_b,
                            "Grade_C": w_c, "Grade_D": w_d, "Grade_E": w_e
                        }

                        # Portfolio Expected Return
                        p_ret = sum(weights[g] * expected_returns[g] for g in grades)

                        # Portfolio Volatility with cross-grade correlation rho = 0.35
                        rho = 0.35
                        p_var = 0.0
                        for g1 in grades:
                            for g2 in grades:
                                corr = 1.0 if g1 == g2 else rho
                                p_var += weights[g1] * weights[g2] * volatilities[g1] * volatilities[g2] * corr

                        p_vol = math.sqrt(max(1e-8, p_var))
                        sharpe = (p_ret - self.rf) / p_vol if p_vol > 0 else 0.0

                        if sharpe > best_sharpe:
                            best_sharpe = sharpe
                            best_weights = weights
                            best_ret = p_ret
                            best_vol = p_vol

        # Conservative profile benchmark
        conservative_weights = {"Grade_A": 0.50, "Grade_B": 0.35, "Grade_C": 0.15, "Grade_D": 0.0, "Grade_E": 0.0}
        c_ret = sum(conservative_weights[g] * expected_returns[g] for g in grades)
        c_var = sum(conservative_weights[g1] * conservative_weights[g2] * volatilities[g1] * volatilities[g2] * (1.0 if g1 == g2 else 0.35) for g1 in grades for g2 in grades)
        c_vol = math.sqrt(c_var)
        c_sharpe = (c_ret - self.rf) / c_vol if c_vol > 0 else 0.0

        # Equal-weighted benchmark
        eq_weights = {g: 0.20 for g in grades}
        eq_ret = sum(eq_weights[g] * expected_returns[g] for g in grades)
        eq_var = sum(eq_weights[g1] * eq_weights[g2] * volatilities[g1] * volatilities[g2] * (1.0 if g1 == g2 else 0.35) for g1 in grades for g2 in grades)
        eq_vol = math.sqrt(eq_var)
        eq_sharpe = (eq_ret - self.rf) / eq_vol if eq_vol > 0 else 0.0

        return {
            "risk_free_rate_pct": self.rf * 100.0,
            "asset_characteristics": {
                g: {
                    "nominal_coupon_pct": rates[g] * 100.0,
                    "default_probability_pct": pds[g] * 100.0,
                    "net_expected_return_pct": round(expected_returns[g] * 100.0, 2),
                    "annualized_volatility_pct": round(volatilities[g] * 100.0, 2)
                } for g in grades
            },
            "ai_optimal_tangency_portfolio": {
                "allocation_weights": best_weights,
                "expected_net_return_pct": round(best_ret * 100.0, 2),
                "expected_volatility_pct": round(best_vol * 100.0, 2),
                "sharpe_ratio": round(best_sharpe, 3)
            },
            "benchmarks": {
                "conservative_portfolio": {
                    "allocation_weights": conservative_weights,
                    "expected_return_pct": round(c_ret * 100.0, 2),
                    "expected_volatility_pct": round(c_vol * 100.0, 2),
                    "sharpe_ratio": round(c_sharpe, 3)
                },
                "equal_weighted_portfolio": {
                    "allocation_weights": eq_weights,
                    "expected_return_pct": round(eq_ret * 100.0, 2),
                    "expected_volatility_pct": round(eq_vol * 100.0, 2),
                    "sharpe_ratio": round(eq_sharpe, 3)
                }
            }
        }
