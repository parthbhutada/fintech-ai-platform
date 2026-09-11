"""
Demo: Portfolio Allocation (Markowitz Efficient Frontier) & Fraud Screening.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.trading_portfolio.portfolio_allocator import PortfolioAllocator
from src.fraud_prevention.anomaly_detector import FraudAnomalyDetector

def main():
    print("=" * 75)
    print("DEMO: AI PORTFOLIO OPTIMIZATION & FRAUD PREVENTION")
    print("=" * 75)

    # 1. Modern Portfolio Theory Allocator
    print("[1] AI Loan Portfolio Asset Allocation (Markowitz Mean-Variance):")
    allocator = PortfolioAllocator(risk_free_rate=0.045)
    res = allocator.optimize_allocation()

    opt = res['ai_optimal_tangency_portfolio']
    print(f"    Max Sharpe Ratio:      {opt['sharpe_ratio']:.3f}")
    print(f"    Expected Net Return:   {opt['expected_net_return_pct']:.2f}%")
    print(f"    Portfolio Volatility:  {opt['expected_volatility_pct']:.2f}%")
    print("    AI Optimal Allocations:")
    for g, w in opt['allocation_weights'].items():
        print(f"      * {g}: {w:.1%}")

    # 2. Fraud Prevention & Synthetic Identity Detection
    print("\n[2] Fraud Prevention & Anomaly Detection Screening:")
    detector = FraudAnomalyDetector()

    suspicious_app = {
        "id": "FRAUD_TEST_999",
        "loan_amnt": 38000.0,
        "annual_inc": 22000.0,  # Loan is 172% of annual income!
        "revol_bal": 55000.0,
        "inq_last_6mths": 6.0,  # Credit inquiry burst
        "revol_util": 96.5
    }

    fraud_res = detector.analyze_application(suspicious_app)
    print(f"    Applicant ID:          {fraud_res['applicant_id']}")
    print(f"    Calculated Fraud Score:{fraud_res['fraud_score']}/100")
    print(f"    Assigned Risk Tier:    {fraud_res['fraud_risk_tier']}")
    print(f"    Recommended Action:    {fraud_res['recommended_action']}")
    print("    Triggered Anomalies:")
    for anom in fraud_res['detected_anomalies']:
        print(f"      ! {anom}")
    print("=" * 75)

if __name__ == "__main__":
    main()
