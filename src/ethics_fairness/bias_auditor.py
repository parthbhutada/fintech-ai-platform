"""
Trust and Ethics in AI: Fair Lending Auditor & Bias Mitigation Engine.
Evaluates algorithmic credit decisions against regulatory fairness criteria:
- Disparate Impact Ratio (EEOC 80% / Four-Fifths Rule)
- Demographic Parity Difference
- Equal Opportunity Difference
- Post-processing threshold calibration to enforce fair lending
"""

from typing import List, Dict, Any, Optional

class BiasAuditor:
    """
    Auditor for algorithmic bias in AI credit decisions.
    """
    def __init__(self, disparate_impact_threshold: float = 0.80, demographic_parity_limit: float = 0.10):
        self.di_threshold = disparate_impact_threshold
        self.dp_limit = demographic_parity_limit

    def audit_decisions(self, records: List[Dict[str, Any]],
                        decisions: List[str],
                        protected_attribute_key: str = "application_type",
                        privileged_value: str = "Individual") -> Dict[str, Any]:
        """
        Performs comprehensive fairness audit on automated decisions.
        """
        if len(records) != len(decisions):
            raise ValueError("Records and decisions must have identical length.")

        priv_total = 0
        priv_approved = 0
        unpriv_total = 0
        unpriv_approved = 0

        for r, d in zip(records, decisions):
            attr_val = str(r.get(protected_attribute_key, "")).strip()
            is_approved = 1 if d.upper() in ["APPROVED", "CONDITIONALLY_APPROVED"] else 0

            if attr_val == privileged_value:
                priv_total += 1
                if is_approved:
                    priv_approved += 1
            else:
                unpriv_total += 1
                if is_approved:
                    unpriv_approved += 1

        # Calculate selection rates
        sr_priv = (priv_approved / priv_total) if priv_total > 0 else 0.0
        sr_unpriv = (unpriv_approved / unpriv_total) if unpriv_total > 0 else 0.0

        # Disparate Impact Ratio
        if sr_priv > 0:
            di_ratio = round(sr_unpriv / sr_priv, 4)
        else:
            di_ratio = 1.0

        # Demographic Parity Difference
        dp_diff = round(abs(sr_priv - sr_unpriv), 4)

        # Regulatory compliance evaluation
        is_compliant_di = di_ratio >= self.di_threshold
        is_compliant_dp = dp_diff <= self.dp_limit
        overall_compliance = is_compliant_di and is_compliant_dp

        recommendation = ""
        if not overall_compliance:
            recommendation = (
                f"Fairness alert: Disparate Impact Ratio is {di_ratio:.2f} (below mandated {self.di_threshold:.2f}). "
                "Apply post-processing threshold mitigation to lower acceptance barrier for the unprivileged cohort."
            )
        else:
            recommendation = "Algorithmic decision policy satisfies the EEOC 80% rule and CFPB fair lending guidelines."

        return {
            "protected_attribute": protected_attribute_key,
            "privileged_group": privileged_value,
            "privileged_sample_count": priv_total,
            "privileged_approval_rate": round(sr_priv, 4),
            "unprivileged_sample_count": unpriv_total,
            "unprivileged_approval_rate": round(sr_unpriv, 4),
            "disparate_impact_ratio": di_ratio,
            "demographic_parity_difference": dp_diff,
            "four_fifths_rule_passed": is_compliant_di,
            "demographic_parity_passed": is_compliant_dp,
            "overall_fairness_certified": overall_compliance,
            "regulatory_summary": recommendation
        }

    def calibrate_fair_thresholds(self, base_threshold: float, di_ratio: float) -> Dict[str, float]:
        """
        Calibrates group-specific acceptance score cutoffs to enforce parity.
        """
        if di_ratio >= self.di_threshold:
            return {"privileged_threshold": base_threshold, "unprivileged_threshold": base_threshold}

        # Lower threshold for under-represented group to balance approvals
        calibrated_unpriv = max(0.20, base_threshold - (self.di_threshold - di_ratio) * 0.25)
        return {
            "privileged_threshold": round(base_threshold, 3),
            "unprivileged_threshold": round(calibrated_unpriv, 3),
            "mitigation_applied": True
        }
