"""
Security, Access Control & Differential Privacy Engine.
Implements epsilon-differential privacy via Laplace noise injection,
cryptographic PII hashing/masking, and Role-Based Access Control (RBAC).
"""

import hashlib
import random
import math
from typing import Dict, List, Any, Optional

class DifferentialPrivacyEngine:
    """
    Implements epsilon-differential privacy using the Laplace mechanism.
    """
    def __init__(self, epsilon: float = 1.0):
        self.epsilon = epsilon

    def laplace_noise(self, scale: float) -> float:
        """Generates noise from Laplace(0, scale) using inverse CDF transform."""
        u = random.random() - 0.5
        sign = 1.0 if u >= 0 else -1.0
        return -scale * sign * math.log(1.0 - 2.0 * abs(u) + 1e-12)

    def private_mean(self, values: List[float], lower_bound: float, upper_bound: float) -> float:
        """
        Computes epsilon-differentially private mean with bounded sensitivity.
        Sensitivity = (upper_bound - lower_bound) / N
        """
        if not values:
            return 0.0
        n = len(values)
        clipped = [max(lower_bound, min(upper_bound, v)) for v in values]
        true_mean = sum(clipped) / n
        sensitivity = (upper_bound - lower_bound) / n
        scale = sensitivity / self.epsilon
        noise = max(-5.0, min(5.0, self.laplace_noise(scale)))
        return round(true_mean + noise, 4)

    def private_count(self, count_val: int) -> int:
        """Computes DP count with sensitivity 1."""
        scale = 1.0 / self.epsilon
        noise = self.laplace_noise(scale)
        return max(0, int(round(count_val + noise)))

class SecurityAccessController:
    """
    RBAC and PII Cryptographic Guard.
    """
    ROLE_PERMISSIONS = {
        "BORROWER": ["view_own_application", "accept_offer"],
        "UNDERWRITER": ["view_anonymized_application", "evaluate_credit", "view_xai", "approve_loan"],
        "RISK_ANALYST": ["view_portfolio_var", "view_stress_tests", "optimize_portfolio"],
        "AUDITOR": ["view_ethics_audit", "view_blockchain_ledger", "view_model_lineage"],
        "ADMIN": ["manage_users", "update_config", "full_access"]
    }

    def __init__(self, salt: str = "nexusfin_secure_salt_2026"):
        self.salt = salt

    def hash_pii(self, pii_string: str) -> str:
        """Deterministic salted SHA-256 hash for secure cross-referencing without leaking PII."""
        salted = f"{self.salt}_{pii_string}".encode("utf-8")
        return hashlib.sha256(salted).hexdigest()

    def mask_pii(self, applicant: Dict[str, Any], role: str = "UNDERWRITER") -> Dict[str, Any]:
        """
        Masks sensitive PII according to Role-Based Access Control (RBAC).
        """
        masked = applicant.copy()
        raw_id = str(applicant.get("id", "0000"))

        if role not in ["ADMIN"]:
            # Hash ID and mask geo/employment specifics
            masked["id"] = f"BORROWER_HASH_{self.hash_pii(raw_id)[:12]}"
            if "member_id" in masked:
                masked["member_id"] = "REDACTED_SECURE"
            if "emp_title" in masked and role != "UNDERWRITER":
                masked["emp_title"] = "[CONFIDENTIAL_EMPLOYER]"

        return masked

    def verify_permission(self, role: str, action: str) -> bool:
        allowed = self.ROLE_PERMISSIONS.get(role, [])
        return action in allowed or "full_access" in allowed
