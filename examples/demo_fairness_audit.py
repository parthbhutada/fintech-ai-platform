"""
Demo: Trust & Ethics in AI: Fair Lending Audit & Bias Mitigation.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.data_loader import DataLoader
from src.credit_scoring.underwriting import UnderwritingEngine
from src.ethics_fairness.bias_auditor import BiasAuditor

def main():
    print("=" * 75)
    print("DEMO: TRUST & ETHICS IN AI (FAIR LENDING AUDIT)")
    print("=" * 75)
    loader = DataLoader("dataset/lending_club_10k.csv")
    underwriter = UnderwritingEngine()

    decisions = [underwriter.evaluate_application(r)['decision'] for r in loader.raw_records]
    auditor = BiasAuditor(disparate_impact_threshold=0.80, demographic_parity_limit=0.10)

    print("[*] Auditing Credit Decisions across Application Types (Individual vs. Joint)...")
    res = auditor.audit_decisions(loader.raw_records, decisions, protected_attribute_key="application_type", privileged_value="Individual")

    print(f"    Privileged Selection Rate:   {res['privileged_approval_rate']:.2%}")
    print(f"    Unprivileged Selection Rate: {res['unprivileged_approval_rate']:.2%}")
    print(f"    Disparate Impact Ratio:      {res['disparate_impact_ratio']:.4f}")
    print(f"    EEOC 80% Rule Passed:        {res['four_fifths_rule_passed']}")
    print(f"    Demographic Parity Passed:   {res['demographic_parity_passed']}")
    print(f"    Regulatory Assessment:       {res['regulatory_summary']}")

    print("\n[*] Applying Post-Processing Threshold Calibration...")
    calibrated = auditor.calibrate_fair_thresholds(base_threshold=0.50, di_ratio=res['disparate_impact_ratio'])
    print(f"    Standard Cutoff:             {calibrated['privileged_threshold']}")
    print(f"    Calibrated Parity Cutoff:    {calibrated['unprivileged_threshold']}")
    print("    Outcome: Enforces equalized opportunity across diverse borrower applicant groups.")
    print("=" * 75)

if __name__ == "__main__":
    main()
