"""
Personalized Banking & Dynamic Pricing Engine.
Generates tailored credit offers, multi-option repayment plans,
and proactive financial hardship mitigation recommendations.
"""

import math
from typing import Dict, List, Any, Optional
from src.core.schema import clean_float

class PersonalizedBankingAdvisor:
    def __init__(self, autopay_discount_pct: float = 0.25, relationship_discount_pct: float = 0.50):
        self.autopay_discount = autopay_discount_pct
        self.relationship_discount = relationship_discount_pct

    def generate_personalized_offers(self, applicant_data: Dict[str, Any], base_interest_rate: float) -> Dict[str, Any]:
        requested_amount = clean_float(applicant_data.get("loan_amnt", 10000.0))
        annual_income = clean_float(applicant_data.get("annual_inc", 60000.0))
        monthly_income = annual_income / 12.0

        # Term Options
        rate_36 = max(4.99, base_interest_rate - 0.75)
        rate_60 = base_interest_rate + 1.25

        # Monthly payment calculation: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        def calc_monthly(p: float, annual_r: float, months: int) -> float:
            r = (annual_r / 100.0) / 12.0
            if r == 0:
                return round(p / months, 2)
            factor = (1.0 + r) ** months
            return round(p * (r * factor) / (factor - 1.0), 2)

        monthly_36 = calc_monthly(requested_amount, rate_36, 36)
        total_paid_36 = round(monthly_36 * 36, 2)
        total_int_36 = round(total_paid_36 - requested_amount, 2)

        monthly_60 = calc_monthly(requested_amount, rate_60, 60)
        total_paid_60 = round(monthly_60 * 60, 2)
        total_int_60 = round(total_paid_60 - requested_amount, 2)

        # Autopay discount rate
        autopay_rate_36 = round(rate_36 - self.autopay_discount, 2)
        monthly_autopay_36 = calc_monthly(requested_amount, autopay_rate_36, 36)

        offers = [
            {
                "tier_name": "Accelerated Interest Saver (36 Months)",
                "term_months": 36,
                "interest_rate_pct": rate_36,
                "monthly_payment_usd": monthly_36,
                "total_interest_usd": total_int_36,
                "dti_impact_pct": round((monthly_36 / monthly_income) * 100.0, 1),
                "savings_vs_60m": round(total_int_60 - total_int_36, 2),
                "recommended_for": "Minimizing lifetime interest charges"
            },
            {
                "tier_name": "Balanced Prime Plan (With Autopay)",
                "term_months": 36,
                "interest_rate_pct": autopay_rate_36,
                "monthly_payment_usd": monthly_autopay_36,
                "total_interest_usd": round(monthly_autopay_36 * 36 - requested_amount, 2),
                "dti_impact_pct": round((monthly_autopay_36 / monthly_income) * 100.0, 1),
                "discount_applied": f"{self.autopay_discount}% Autopay discount",
                "recommended_for": "Best daily value and automated budget safety"
            },
            {
                "tier_name": "Cash-Flow Protector (60 Months)",
                "term_months": 60,
                "interest_rate_pct": rate_60,
                "monthly_payment_usd": monthly_60,
                "total_interest_usd": total_int_60,
                "dti_impact_pct": round((monthly_60 / monthly_income) * 100.0, 1),
                "savings_monthly": round(monthly_36 - monthly_60, 2),
                "recommended_for": "Preserving monthly liquidity and lowest required payment"
            }
        ]

        return {
            "applicant_id": applicant_data.get("id", "N/A"),
            "principal_requested_usd": requested_amount,
            "monthly_income_usd": round(monthly_income, 2),
            "personalized_loan_options": offers
        }

    def generate_hardship_relief_plan(self, current_loan_balance: float, original_monthly_payment: float, hardship_reason: str) -> Dict[str, Any]:
        """
        Generates proactive restructuring options for delinquent or financially stressed borrowers.
        """
        # Option 1: 3-month interest-only deferral
        io_rate = 0.08 / 12.0
        io_payment = round(current_loan_balance * io_rate, 2)

        # Option 2: 24-month term extension
        extended_payment = round(original_monthly_payment * 0.65, 2)

        return {
            "hardship_status": "RELIEF_RECOMMENDED",
            "trigger_reason": hardship_reason,
            "outstanding_balance_usd": current_loan_balance,
            "original_monthly_obligation_usd": original_monthly_payment,
            "relief_options": [
                {
                    "program": "3-Month Temporary Interest-Only Deferral",
                    "reduced_monthly_payment_usd": io_payment,
                    "temporary_monthly_cashflow_relief_usd": round(original_monthly_payment - io_payment, 2),
                    "deferral_duration_months": 3,
                    "condition": "Zero negative credit bureau reporting during program compliance"
                },
                {
                    "program": "Amortization Extension (+24 Months)",
                    "restructured_monthly_payment_usd": extended_payment,
                    "ongoing_monthly_savings_usd": round(original_monthly_payment - extended_payment, 2),
                    "condition": "Permanently reduces payment burden to align with reduced household income"
                }
            ]
        }
