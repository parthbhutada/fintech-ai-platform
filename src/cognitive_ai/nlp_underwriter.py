"""
Cognitive AI & Financial NLP Engine.
Analyzes unstructured text in loan titles, borrower descriptions, and purposes
to extract financial sentiment, intent categories, and latent risk indicators.
"""

import re
from typing import Dict, List, Any

class CognitiveNLPUnderwriter:
    def __init__(self):
        # Financial domain intent lexicons
        self.positive_keywords = {
            "consolidation": 0.4, "refinance": 0.4, "lower interest": 0.5, "business expansion": 0.45,
            "equipment": 0.35, "home improvement": 0.3, "career": 0.3, "stable": 0.35, "discipline": 0.4,
            "pay off": 0.4, "savings": 0.35, "reliable": 0.3, "growth": 0.3, "investment": 0.25
        }

        self.high_risk_keywords = {
            "payday": -0.8, "cash advance": -0.75, "urgent": -0.5, "emergency": -0.4,
            "behind on payments": -0.85, "overdue": -0.7, "lawsuit": -0.9, "legal fee": -0.6,
            "gambling": -1.0, "desperate": -0.8, "foreclosure": -0.9, "medical debt": -0.35,
            "struggling": -0.6, "bailout": -0.75
        }

    def analyze_text(self, title: str = "", description: str = "", purpose: str = "") -> Dict[str, Any]:
        combined_text = f"{title} {description} {purpose}".lower()
        cleaned_text = re.sub(r"[^a-z0-9\s]", " ", combined_text)
        tokens = cleaned_text.split()

        pos_matches = []
        neg_matches = []
        score = 0.0

        for phrase, weight in self.positive_keywords.items():
            if phrase in combined_text:
                pos_matches.append(phrase)
                score += weight

        for phrase, weight in self.high_risk_keywords.items():
            if phrase in combined_text:
                neg_matches.append(phrase)
                score += weight

        # Normalize score between -1.0 and 1.0
        cognitive_score = max(-1.0, min(1.0, round(score, 3)))

        # Qualitative assessment
        if cognitive_score >= 0.3:
            sentiment_rating = "PRUDENT_REFINANCING"
            risk_delta = -0.03  # Lowers default probability by 3%
        elif cognitive_score <= -0.4:
            sentiment_rating = "DISTRESSED_BORROWING"
            risk_delta = +0.08  # Adds 8% to default probability
        else:
            sentiment_rating = "NEUTRAL_STANDARD"
            risk_delta = 0.0

        return {
            "analyzed_text_excerpt": combined_text[:120] + ("..." if len(combined_text) > 120 else ""),
            "cognitive_sentiment_score": cognitive_score,
            "intent_classification": sentiment_rating,
            "risk_adjustment_factor": risk_delta,
            "positive_financial_cues": pos_matches,
            "distress_risk_indicators": neg_matches,
            "word_count": len(tokens)
        }
