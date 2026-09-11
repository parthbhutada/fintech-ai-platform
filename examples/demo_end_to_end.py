"""
NexusFin AI - Full End-to-End Straight-Through Processing Demonstration.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.automation.orchestrator import FinTechSTPOrchestrator
from src.core.data_loader import DataLoader

def main():
    print("=" * 75)
    print("NEXUSFIN AI: END-TO-END STRAIGHT-THROUGH UNDERWRITING DEMO")
    print("=" * 75)
    orchestrator = FinTechSTPOrchestrator()
    orchestrator.bootstrap_models("dataset/lending_club_sample.csv")

    loader = DataLoader("dataset/lending_club_snippet.csv")
    sample_borrower = loader.raw_records[0]

    print(f"\nEvaluating Applicant ID: {sample_borrower.get('id')}")
    print(f"Requested Loan Amount:  ${float(sample_borrower.get('loan_amnt', 0)):,.2f}")
    print(f"Stated Annual Income:   ${float(sample_borrower.get('annual_inc', 0)):,.2f}")
    print(f"Credit Score (FICO):    {sample_borrower.get('fico_range_high')}")
    print(f"Debt-to-Income (DTI):   {sample_borrower.get('dti')}%")

    res = orchestrator.process_application_stp(sample_borrower)

    print("\n" + "-" * 40 + " STP DECISION ENGINE OUTPUT " + "-" * 40)
    print(f"1. Biometric Match:       {res['biometric_verification']['status_message']} ({res['biometric_verification']['biometric_confidence_pct']}%)")
    print(f"2. Cognitive NLP:         {res['cognitive_nlp_analysis']['intent_classification']} (Sentiment: {res['cognitive_nlp_analysis']['cognitive_sentiment_score']:+.2f})")
    print(f"3. Fraud Screening:       Tier: {res['fraud_detection_result']['fraud_risk_tier']} (Score: {res['fraud_detection_result']['fraud_score']}/100)")
    print(f"4. Underwriting Decision: {res['underwriting_decision']['decision']}")
    print(f"   - Assigned Grade:      {res['underwriting_decision']['assigned_grade']} (Subgrade: {res['underwriting_decision']['assigned_subgrade']})")
    print(f"   - Offered APR:         {res['underwriting_decision']['offered_interest_rate_pct']:.2f}%")
    print(f"   - Monthly Capacity:    ${res['underwriting_decision']['available_monthly_capacity_usd']:,.2f}")
    print(f"5. Explainable AI:")
    for driver in res['explainable_ai']['top_risk_elevating_factors'][:2]:
        print(f"   - Risk Driver:         {driver}")
    for cf in res['explainable_ai']['actionable_counterfactuals'][:1]:
        print(f"   - Actionable Guidance: {cf['action']} -> {cf['impact']}")
    print(f"6. Blockchain Audit:      Block #{res['blockchain_audit_receipt']['block_index']} Hash: {res['blockchain_audit_receipt']['block_hash'][:28]}...")
    print(f"7. STP Processing Time:   {res['straight_through_processing_latency_ms']} ms")
    print("=" * 75)

if __name__ == "__main__":
    main()
