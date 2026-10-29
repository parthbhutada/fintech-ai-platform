"""
Intelligent Underwriting Engine.
Combines rule-based policies (CFPB/ECOA guidelines) with machine learning default probabilities
to issue automated credit decisions, risk tiers, and personalized pricing.
"""

from typing import Dict, Any, List, Optional
from src.core.schema import clean_float

class UnderwritingEngine:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            "min_fico": 620,
            "max_dti": 43.0,
            "max_revol_util": 85.0,
            "max_inq_6m": 4,
            "default_prob_cutoff": 0.25
        }

    def evaluate_application(self, applicant_data: Dict[str, Any], ml_default_prob: Optional[float] = None) -> Dict[str, Any]:
        fico = clean_float(applicant_data.get("fico_range_high", applicant_data.get("fico_range_low", 650.0)))
        dti = clean_float(applicant_data.get("dti", 20.0))
        annual_inc = clean_float(applicant_data.get("annual_inc", 50000.0))
        loan_amnt = clean_float(applicant_data.get("loan_amnt", 10000.0))
        revol_util = clean_float(applicant_data.get("revol_util", 30.0))
        delinq_2yrs = clean_float(applicant_data.get("delinq_2yrs", 0.0))
        inq_6m = clean_float(applicant_data.get("inq_last_6mths", 0.0))

        # Default probability estimation fallback if not supplied
        if ml_default_prob is None:
            # Baseline logistic risk score based on credit characteristics
            z = -3.2 + (800 - fico) * 0.015 + dti * 0.04 + revol_util * 0.012 + delinq_2yrs * 0.35 + inq_6m * 0.2 - (annual_inc / 100000.0) * 0.4
            import math
            ml_default_prob = round(1.0 / (1.0 + math.exp(-min(40.0, max(-40.0, z)))), 4)

        # Adverse Action / Risk Flags
        min_f = self.config['min_fico']
        max_d = self.config['max_dti']
        reasons_for_adverse_action = []
        if fico < self.config["min_fico"]:
            reasons_for_adverse_action.append(f"Credit score ({fico:.0f}) below minimum policy threshold ({min_f})")
        if dti > self.config["max_dti"]:
            reasons_for_adverse_action.append(f"Debt-to-income ratio ({dti:.1f}%) exceeds maximum limit ({max_d}%)")
        if revol_util > self.config["max_revol_util"]:
            reasons_for_adverse_action.append(f"Revolving credit utilization ({revol_util:.1f}%) is too elevated")
        if inq_6m > self.config["max_inq_6m"]:
            reasons_for_adverse_action.append(f"Excessive recent credit inquiries ({inq_6m:.0f} inquiries in last 6 months)")
        if delinq_2yrs >= 2:
            reasons_for_adverse_action.append(f"Multiple delinquencies recorded in past 2 years ({delinq_2yrs:.0f})")

        # Risk Grade Assignment
        if fico >= 750 and dti <= 18.0 and ml_default_prob < 0.08:
            grade = "A"
            subgrade = "A1" if fico >= 780 else "A3"
            base_rate = 6.49
        elif fico >= 700 and dti <= 24.0 and ml_default_prob < 0.14:
            grade = "B"
            subgrade = "B2"
            base_rate = 10.99
        elif fico >= 660 and dti <= 30.0 and ml_default_prob < 0.22:
            grade = "C"
            subgrade = "C3"
            base_rate = 14.49
        elif fico >= 630 and dti <= 38.0 and ml_default_prob < 0.32:
            grade = "D"
            subgrade = "D2"
            base_rate = 18.99
        elif fico >= 600 and ml_default_prob < 0.42:
            grade = "E"
            subgrade = "E4"
            base_rate = 23.49
        else:
            grade = "F"
            subgrade = "F1"
            base_rate = 27.99

        # Decision Logic
        if reasons_for_adverse_action and len(reasons_for_adverse_action) >= 2 or ml_default_prob > 0.40:
            decision = "DENIED"
            approved_amount = 0.0
            offered_rate = 0.0
        elif len(reasons_for_adverse_action) == 1:
            decision = "CONDITIONALLY_APPROVED"
            # Offer reduced loan amount to mitigate risk
            approved_amount = min(loan_amnt, round(annual_inc * 0.20, -2))
            offered_rate = round(base_rate + 2.50, 2)
        elif ml_default_prob <= self.config["default_prob_cutoff"]:
            decision = "APPROVED"
            approved_amount = loan_amnt
            offered_rate = base_rate
        else:
            decision = "MANUAL_REVIEW"
            approved_amount = loan_amnt * 0.8
            offered_rate = round(base_rate + 1.5, 2)

        # Maximum Debt Capacity
        monthly_income = annual_inc / 12.0
        max_monthly_debt = monthly_income * (self.config["max_dti"] / 100.0)
        current_monthly_debt = monthly_income * (dti / 100.0)
        available_monthly_debt_capacity = max(0.0, round(max_monthly_debt - current_monthly_debt, 2))

        return {
            "application_id": applicant_data.get("id", "N/A"),
            "decision": decision,
            "requested_amount": loan_amnt,
            "approved_amount": approved_amount,
            "assigned_grade": grade,
            "assigned_subgrade": subgrade,
            "offered_interest_rate_pct": offered_rate,
            "default_probability": ml_default_prob,
            "credit_score": fico,
            "debt_to_income_pct": dti,
            "available_monthly_capacity_usd": available_monthly_debt_capacity,
            "adverse_action_reasons": reasons_for_adverse_action,
            "is_straight_through_eligible": decision == "APPROVED" and len(reasons_for_adverse_action) == 0
        }
