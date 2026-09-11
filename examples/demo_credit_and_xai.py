"""
Demo: AutoML Credit Scoring Leaderboard & Explainable AI (XAI) Counterfactuals.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.data_loader import DataLoader
from src.credit_scoring.automl import AutoMLCreditScorer
from src.explainability.xai_engine import ExplainableAIEngine

def main():
    print("=" * 75)
    print("DEMO: AUTOML CREDIT SCORING & EXPLAINABLE AI (XAI)")
    print("=" * 75)
    loader = DataLoader("dataset/lending_club_sample.csv")
    X_train, X_val, y_train, y_val = loader.train_test_split(test_size=0.25, seed=42)

    scorer = AutoMLCreditScorer()
    print("[*] Training candidate credit models...")
    res = scorer.train_and_select(X_train, y_train, X_val, y_val, loader.feature_names)

    print("\n[+] Model Leaderboard:")
    print(f"    {'Algorithm':<35} | {'ROC-AUC':<8} | {'F1-Score':<8} | {'Accuracy':<8}")
    print("    " + "-" * 66)
    for entry in res['leaderboard']:
        alg = entry['algorithm']
        m = entry['metrics']
        print(f"    {alg:<35} | {m['roc_auc']:<8.4f} | {m['f1_score']:<8.4f} | {m['accuracy']:<8.2%}")

    print(f"\n[*] Champion Model Selected: {res['best_model_name']}")

    # XAI Deep Dive
    xai = ExplainableAIEngine()
    sample_borrower = loader.raw_records[3]
    explanation = xai.explain_instance(sample_borrower)

    print(f"\n[+] Explainable AI Attribution for Applicant {sample_borrower.get('id')}:")
    for feat, val in explanation['local_feature_attributions'].items():
        bar = ("+" if val > 0 else "-") * int(abs(val) * 100)
        print(f"    {feat:<24}: {val:+.4f} {bar}")

    print("\n[+] Actionable Counterfactual Guidance:")
    for cf in explanation['actionable_counterfactuals']:
        print(f"    -> Action: {cf['action']}")
        print(f"       Current: {cf['current_value']} | Target: {cf['target_value']}")
        print(f"       Impact:  {cf['impact']}\n")
    print("=" * 75)

if __name__ == "__main__":
    main()
