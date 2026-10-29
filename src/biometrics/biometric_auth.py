"""
Biometric Data Processing & Identity Authentication Engine.
Implements cosine similarity matching on high-dimensional facial/voice embeddings,
anti-spoofing liveness verification, and risk-based Step-Up MFA authentication.
"""

import math
from typing import List, Dict, Any, Optional

def vector_norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = vector_norm(v1)
    n2 = vector_norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)

class BiometricAuthenticationEngine:
    def __init__(self, match_threshold: float = 0.82, liveness_threshold: float = 0.90):
        self.match_threshold = match_threshold
        self.liveness_threshold = liveness_threshold
        # Enrolled templates: {user_id: {"facial_embedding": [...], "enrolled_at": "..."}}
        self.enrolled_templates: Dict[str, Dict[str, Any]] = {}

    def enroll_user(self, user_id: str, biometric_vector: List[float], modality: str = "facial") -> Dict[str, Any]:
        self.enrolled_templates[user_id] = {
            "embedding": biometric_vector,
            "modality": modality,
            "dimension": len(biometric_vector)
        }
        return {
            "status": "ENROLLED_SUCCESSFULLY",
            "user_id": user_id,
            "modality": modality,
            "vector_dimension": len(biometric_vector)
        }

    def verify_biometric(self, user_id: str, probe_vector: List[float], liveness_score: float = 0.95) -> Dict[str, Any]:
        if user_id not in self.enrolled_templates:
            return {
                "authenticated": False,
                "reason": "USER_NOT_ENROLLED",
                "similarity_score": 0.0,
                "liveness_passed": False
            }

        enrolled_vec = self.enrolled_templates[user_id]["embedding"]
        if len(enrolled_vec) != len(probe_vector):
            return {
                "authenticated": False,
                "reason": "DIMENSION_MISMATCH",
                "similarity_score": 0.0,
                "liveness_passed": False
            }

        sim = round(cosine_similarity(enrolled_vec, probe_vector), 4)
        match_passed = sim >= self.match_threshold
        liveness_passed = liveness_score >= self.liveness_threshold

        auth_success = match_passed and liveness_passed

        status_msg = "AUTHENTICATION_SUCCESS"
        if not match_passed:
            status_msg = "BIOMETRIC_MISMATCH_POTENTIAL_IMPOSTOR"
        elif not liveness_passed:
            status_msg = "LIVENESS_FAILED_SPOOF_ATTACK_DETECTED"

        return {
            "authenticated": auth_success,
            "status_message": status_msg,
            "similarity_score": sim,
            "match_threshold": self.match_threshold,
            "liveness_score": round(liveness_score, 4),
            "liveness_threshold": self.liveness_threshold,
            "biometric_confidence_pct": round(sim * 100.0, 2)
        }

    def evaluate_step_up_mfa(self, loan_amount: float, auth_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates whether high-value transaction requires secondary multi-factor authentication.
        """
        requires_step_up = loan_amount >= 10000.0 or not auth_result.get("authenticated", False)
        return {
            "loan_amount_usd": loan_amount,
            "step_up_mfa_required": requires_step_up,
            "action": "PROMPT_FIDO2_HARDWARE_TOKEN" if requires_step_up else "DISBURSEMENT_AUTHORIZED"
        }
