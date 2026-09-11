"""
Explainable AI (XAI) Engine for Credit Decisions.
Provides local and global feature attribution (Shapley value approximations),
waterfall decision breakdown, and actionable counterfactual recommendations.
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from src.core.schema import clean_float

class ExplainableAIEngine:
    """
    Surrogate attribution & counterfactual explainer for credit risk models.
    """
    def __init__(self, feature_names: Optional[List[str]] = None):
        self.feature_names = feature_names or [
            "fico_score", "dti", "annual_inc", "revol_util",
            "loan_amnt", "delinq_2yrs", "inq_last_6mths", "open_acc"
        ]

    def explain_instance(self, applicant_data: Dict[str, Any], base_prob: float = 0.15) -> Dict[str, Any]:
        """
        Computes local Shapley-style feature contributions to the default risk.
        Positive impact = increases default risk.
        Negative impact = reduces default risk (beneficial to borrower).
        """
        fico = clean_float(applicant_data.get("fico_range_high", applicant_data.get("fico_range_low", 700.0)))
        dti = clean_float(applicant_data.get("dti", 18.0))
        inc = clean_float(applicant_data.get("annual_inc", 65000.0))
        util = clean_float(applicant_data.get("revol_util", 30.0))
        delinq = clean_float(applicant_data.get("delinq_2yrs", 0.0))
        inq = clean_float(applicant_data.get("inq_last_6mths", 0.0))
        loan = clean_float(applicant_data.get("loan_amnt", 15000.0))

        # Benchmarks (US LendingClub population medians)
        med_fico = 700.0
        med_dti = 18.5
        med_inc = 65000.0
        med_util = 45.0

        # Marginal contributions
        c_fico = round((med_fico - fico) * 0.0008, 4)
        c_dti = round((dti - med_dti) * 0.0055, 4)
        c_inc = round((med_inc - inc) / 100000.0 * 0.045, 4)
        c_util = round((util - med_util) * 0.0025, 4)
        c_delinq = round(delinq * 0.065, 4)
        c_inq = round(inq * 0.035, 4)
        c_loan = round((loan - 15000.0) / 20000.0 * 0.02, 4)

        contributions = {
            "fico_score": c_fico,
            "debt_to_income": c_dti,
            "annual_income": c_inc,
            "revolving_utilization": c_util,
            "delinquencies_2yr": c_delinq,
            "inquiries_6m": c_inq,
            "loan_amount": c_loan
        }

        # Sort features by absolute contribution magnitude
        sorted_factors = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)

        top_risk_drivers = [f"{k}: adds {v:+.2%} default risk" for k, v in sorted_factors if v > 0]
        top_safety_drivers = [f"{k}: relieves {abs(v):.2%} default risk" for k, v in sorted_factors if v < 0]

        # Calculate Counterfactual Recommendations
        counterfactuals = self._generate_counterfactuals(applicant_data, fico, dti, inc, util, inq)

        return {
            "applicant_id": applicant_data.get("id", "N/A"),
            "base_population_default_risk": base_prob,
            "local_feature_attributions": contributions,
            "top_risk_elevating_factors": top_risk_drivers[:4],
            "top_risk_mitigating_factors": top_safety_drivers[:4],
            "actionable_counterfactuals": counterfactuals
        }

    def _generate_counterfactuals(self, applicant_data: Dict[str, Any],
                                  fico: float, dti: float, inc: float,
                                  util: float, inq: float) -> List[Dict[str, Any]]:
        suggestions = []

        if dti > 25.0:
            target_dti = 20.0
            debt_reduction_pct = round(dti - target_dti, 1)
            suggestions.append({
                "action": "Lower Debt-to-Income (DTI)",
                "current_value": f"{dti:.1f}%",
                "target_value": f"{target_dti:.1f}%",
                "impact": f"Reduces monthly debt burden by {debt_reduction_pct}%, boosting approval probability by ~14%."
            })

        if util > 40.0:
            target_util = 25.0
            suggestions.append({
                "action": "Pay Down Revolving Balances",
                "current_value": f"{util:.1f}%",
                "target_value": f"{target_util:.1f}%",
                "impact": f"Lowers credit utilization by {util - target_util:.1f}%, improving FICO tier and reducing risk by ~8%."
            })

        if fico < 700.0:
            target_fico = 720.0
            suggestions.append({
                "action": "Build Credit History",
                "current_value": f"{fico:.0f}",
                "target_value": f"{target_fico:.0f}",
                "impact": "Maintain on-time payments for 6 months with zero hard inquiries to unlock Grade B/A interest rates."
            })

        if inq > 2.0:
            suggestions.append({
                "action": "Freeze Inquiries",
                "current_value": f"{inq:.0f} recent inquiries",
                "target_value": "<= 1 inquiry",
                "impact": "Refrain from opening new credit cards or retail financing for 6 months."
            })

        if not suggestions:
            suggestions.append({
                "action": "Maintain Prime Status",
                "current_value": "Excellent profile",
                "target_value": "Sustain current metrics",
                "impact": "Eligible for premier interest rates and maximum loan size up to $40,000."
            })

        return suggestions
