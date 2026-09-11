import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cognitive_ai.nlp_underwriter import CognitiveNLPUnderwriter

class TestCognitiveAI(unittest.TestCase):
    def test_nlp_sentiment(self):
        nlp = CognitiveNLPUnderwriter()
        res_pos = nlp.analyze_text(title="Debt consolidation loan", description="To refinance high interest credit cards for stable debt payoff")
        self.assertEqual(res_pos["intent_classification"], "PRUDENT_REFINANCING")
        self.assertLess(res_pos["risk_adjustment_factor"], 0)

        res_neg = nlp.analyze_text(title="Urgent loan", description="Need cash advance to cover payday loan and behind on payments")
        self.assertEqual(res_neg["intent_classification"], "DISTRESSED_BORROWING")
        self.assertGreater(res_neg["risk_adjustment_factor"], 0)
