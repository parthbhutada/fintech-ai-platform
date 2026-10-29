"""
FinTech Risk Management Engine.
Implements Value-at-Risk (VaR), Conditional VaR (CVaR / Expected Shortfall),
Expected Loss (EL = PD x LGD x EAD), Concentration Risk, and Macroeconomic Stress Testing.
"""

import math
from typing import List, Dict, Any, Optional
from src.core.schema import clean_float

class PortfolioRiskManager:
    def __init__(self, lgd_default: float = 0.45):
        """
        lgd_default: Loss Given Default (typically 45% for unsecured peer-to-peer personal loans).
        """
        self.lgd_default = lgd_default

    def analyze_portfolio(self, loans: List[Dict[str, Any]], custom_pds: Optional[List[float]] = None) -> Dict[str, Any]:
        if not loans:
            return {"error": "Empty portfolio"}

        total_exposure = 0.0
        expected_loss_total = 0.0
        grade_exposure: Dict[str, float] = {}
        state_exposure: Dict[str, float] = {}
        individual_losses: List[float] = []

        for i, loan in enumerate(loans):
            ead = clean_float(loan.get("loan_amnt", loan.get("funded_amnt", 0.0)))
            total_exposure += ead

            # Grade & State breakdown
            g = str(loan.get("grade", "Unknown")).strip()
            grade_exposure[g] = grade_exposure.get(g, 0.0) + ead

            st = str(loan.get("addr_state", "Other")).strip()
            state_exposure[st] = state_exposure.get(st, 0.0) + ead

            # Probability of default
            if custom_pds and i < len(custom_pds):
                pd = custom_pds[i]
            else:
                grade_pd_map = {"A": 0.04, "B": 0.09, "C": 0.16, "D": 0.26, "E": 0.35, "F": 0.45, "G": 0.55}
                pd = grade_pd_map.get(g, 0.18)

            el = pd * self.lgd_default * ead
            expected_loss_total += el
            individual_losses.append(el)

        n = len(individual_losses)
        mean_loss = expected_loss_total / n if n > 0 else 0.0
        variance = sum((l - mean_loss) ** 2 for l in individual_losses) / (n if n > 1 else 1)
        std_loss = math.sqrt(variance)

        # Parametric Portfolio Value-at-Risk (VaR)
        # Z-scores: 95% = 1.645, 99% = 2.326
        portfolio_std = std_loss * math.sqrt(n)
        var_95 = round(expected_loss_total + 1.645 * portfolio_std, 2)
        var_99 = round(expected_loss_total + 2.326 * portfolio_std, 2)

        # Expected Shortfall (CVaR) ~ mean loss beyond VaR
        # For normal tail: CVaR_alpha = mean + std * phi(z) / (1 - alpha)
        cvar_95 = round(expected_loss_total + portfolio_std * (math.exp(-0.5 * 1.645**2) / (math.sqrt(2 * math.pi) * 0.05)), 2)
        cvar_99 = round(expected_loss_total + portfolio_std * (math.exp(-0.5 * 2.326**2) / (math.sqrt(2 * math.pi) * 0.01)), 2)

        # Macroeconomic Stress Testing Scenarios
        stress_tests = {
            "baseline": {
                "scenario_name": "Baseline Economic Growth",
                "projected_loss_usd": round(expected_loss_total, 2),
                "projected_loss_rate_pct": round((expected_loss_total / total_exposure * 100.0) if total_exposure > 0 else 0, 2),
                "capital_adequacy_status": "SUFFICIENT"
            },
            "mild_recession": {
                "scenario_name": "Mild Recession (+2% Unemployment, +150 bps Rates)",
                "projected_loss_usd": round(expected_loss_total * 1.45, 2),
                "projected_loss_rate_pct": round((expected_loss_total * 1.45 / total_exposure * 100.0) if total_exposure > 0 else 0, 2),
                "capital_adequacy_status": "MONITOR_RESERVES"
            },
            "severe_stagflation": {
                "scenario_name": "Severe Stagflation (+5% Unemployment, +400 bps Rates)",
                "projected_loss_usd": round(expected_loss_total * 2.20, 2),
                "projected_loss_rate_pct": round((expected_loss_total * 2.20 / total_exposure * 100.0) if total_exposure > 0 else 0, 2),
                "capital_adequacy_status": "CAPITAL_BUFFER_REQUIRED"
            }
        }

        return {
            "total_portfolio_exposure_usd": round(total_exposure, 2),
            "loan_count": n,
            "expected_loss_usd": round(expected_loss_total, 2),
            "expected_loss_rate_pct": round((expected_loss_total / total_exposure * 100.0) if total_exposure > 0 else 0, 2),
            "value_at_risk_95_pct": var_95,
            "value_at_risk_99_pct": var_99,
            "conditional_var_95_pct": cvar_95,
            "conditional_var_99_pct": cvar_99,
            "grade_distribution": {k: round(v, 2) for k, v in sorted(grade_exposure.items())},
            "top_state_concentrations": sorted(state_exposure.items(), key=lambda x: x[1], reverse=True)[:5],
            "stress_testing": stress_tests
        }
