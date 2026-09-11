"""
AI Fraud Prevention & Anomaly Detection Engine.
Detects synthetic identity fraud, multivariate outlier patterns, and high-velocity application bursts.
"""

import math
from typing import Dict, List, Any, Optional
from src.core.schema import clean_float

class FraudAnomalyDetector:
    def __init__(self, zscore_threshold: float = 2.5):
        self.zscore_thresh = zscore_threshold
        # Application submission history for velocity tracking {identifier: [timestamps]}
        self.submission_log: Dict[str, List[float]] = {}

    def analyze_application(self, applicant_data: Dict[str, Any], timestamp_epoch: float = 1600000000.0) -> Dict[str, Any]:
        flags: List[str] = []
        score_penalties = 0.0

        loan_amnt = clean_float(applicant_data.get("loan_amnt", 10000.0))
        annual_inc = clean_float(applicant_data.get("annual_inc", 50000.0))
        dti = clean_float(applicant_data.get("dti", 15.0))
        revol_bal = clean_float(applicant_data.get("revol_bal", 5000.0))
        revol_util = clean_float(applicant_data.get("revol_util", 30.0))
        inq_6m = clean_float(applicant_data.get("inq_last_6mths", 0.0))
        pub_rec = clean_float(applicant_data.get("pub_rec", 0.0))
        earliest_cr = str(applicant_data.get("earliest_cr_line", "2010"))

        # 1. Synthetic Identity Fraud Check
        # Disproportionate loan request compared to reported annual income
        if annual_inc > 0 and (loan_amnt / annual_inc) > 0.65:
            flags.append(f"Synthetic identity risk: Requested loan (${loan_amnt:,.0f}) is excessively large relative to income (${annual_inc:,.0f})")
            score_penalties += 30.0

        # Unrealistic credit profile combinations
        if annual_inc < 20000.0 and revol_bal > 40000.0:
            flags.append("High debt-to-income mismatch: Revolving balance exceeds double the stated annual income")
            score_penalties += 25.0

        # 2. Velocity Anomaly Check (Application Burst)
        applicant_id = str(applicant_data.get("id", applicant_data.get("member_id", "default_user")))
        if applicant_id not in self.submission_log:
            self.submission_log[applicant_id] = []
        self.submission_log[applicant_id].append(timestamp_epoch)

        # Count submissions in last 3600 seconds (1 hour)
        recent_count = sum(1 for t in self.submission_log[applicant_id] if (timestamp_epoch - t) <= 3600.0)
        if recent_count > 3:
            flags.append(f"Velocity risk: {recent_count} rapid loan applications detected within 1 hour")
            score_penalties += 35.0

        # 3. Credit Inquiries Anomaly
        if inq_6m >= 5:
            flags.append(f"Inquiry burst: {inq_6m:.0f} credit inquiries in past 6 months indicates aggressive credit seeking / bust-out risk")
            score_penalties += 20.0

        # 4. Multivariate Outlier Score (Z-distance heuristic)
        # Standardized distance from typical borrower centroid
        z_loan = abs(loan_amnt - 15000.0) / 10000.0
        z_inc = max(0.0, (25000.0 - annual_inc) / 15000.0)
        z_util = max(0.0, (revol_util - 50.0) / 25.0)
        multivariate_z = math.sqrt((z_loan**2 + z_inc**2 + z_util**2) / 3.0)

        if multivariate_z > self.zscore_thresh:
            flags.append(f"Multivariate outlier: Anomalous credit footprint (Z-distance: {multivariate_z:.2f})")
            score_penalties += 15.0

        total_fraud_score = min(100.0, round(score_penalties, 1))

        if total_fraud_score >= 60.0:
            risk_tier = "CRITICAL"
            action = "IMMEDIATE_FREEZE_AND_INVESTIGATE"
        elif total_fraud_score >= 35.0:
            risk_tier = "HIGH"
            action = "STEP_UP_IDENTITY_VERIFICATION"
        elif total_fraud_score >= 15.0:
            risk_tier = "MEDIUM"
            action = "ENHANCED_DOCUMENT_AUDIT"
        else:
            risk_tier = "LOW"
            action = "STANDARD_PROCESSING"

        return {
            "applicant_id": applicant_id,
            "fraud_score": total_fraud_score,
            "fraud_risk_tier": risk_tier,
            "recommended_action": action,
            "multivariate_anomaly_distance": round(multivariate_z, 2),
            "detected_anomalies": flags,
            "is_flagged": len(flags) > 0
        }
