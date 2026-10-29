"""
NexusFin AI - Unified Command Line Interface (CLI).
Provides subcommands for credit underwriting, fairness audits, portfolio risk,
trading optimization, quantum simulation, and blockchain verification.
"""

import argparse
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analysis import BiasAuditor, ExplainableAIEngine, FraudAnomalyDetector
from src.data_credit import DEFAULT_DATASET, DataLoader, UnderwritingEngine
from src.finance import PortfolioAllocator, PortfolioRiskManager, QuantumRiskSimulator
from src.operations import BlockchainAuditLedger, FinTechSTPOrchestrator
from src.api.server import run_server

def cmd_pipeline(args):
    print("NexusFin AI: Straight-Through Processing (STP) Execution")
    orchestrator = FinTechSTPOrchestrator()
    dataset_path = args.dataset or DEFAULT_DATASET
    print(f"[*] Bootstrapping machine learning models using: {dataset_path}")
    train_res = orchestrator.bootstrap_models(dataset_path)
    b_name = train_res["best_model_name"]
    b_acc = train_res["best_metrics"]["accuracy"]
    b_prec = train_res["best_metrics"]["precision"]
    b_rec = train_res["best_metrics"]["recall"]
    b_auc = train_res["best_metrics"]["roc_auc"]
    print(f"[+] Best Model Selected: {b_name}")
    print(f"    - Accuracy:  {b_acc:.2%}")
    print(f"    - Precision: {b_prec:.2%}")
    print(f"    - Recall:    {b_rec:.2%}")
    print(f"    - ROC-AUC:   {b_auc:.4f}")

    loader = DataLoader(dataset_path)
    sample_record = loader.raw_records[0]
    rec_id = sample_record.get("id", "N/A")
    print(f"\n[*] Processing Straight-Through Application for Loan ID: {rec_id}")
    res = orchestrator.process_application_stp(sample_record)

    bio_msg = res["biometric_verification"]["status_message"]
    bio_conf = res["biometric_verification"]["biometric_confidence_pct"]
    nlp_intent = res["cognitive_nlp_analysis"]["intent_classification"]
    nlp_score = res["cognitive_nlp_analysis"]["cognitive_sentiment_score"]
    fraud_tier = res["fraud_detection_result"]["fraud_risk_tier"]
    fraud_score = res["fraud_detection_result"]["fraud_score"]
    dec = res["underwriting_decision"]["decision"]
    grade = res["underwriting_decision"]["assigned_grade"]
    subgrade = res["underwriting_decision"]["assigned_subgrade"]
    rate = res["underwriting_decision"]["offered_interest_rate_pct"]
    blk_idx = res["blockchain_audit_receipt"]["block_index"]
    blk_hash = res["blockchain_audit_receipt"]["block_hash"]
    latency = res["straight_through_processing_latency_ms"]

    print(f"\n[1] Biometric Authentication: {bio_msg}")
    print(f"    Confidence: {bio_conf}%")
    print(f"[2] Cognitive NLP Sentiment:   {nlp_intent}")
    print(f"    Score: {nlp_score:+.2f}")
    print(f"[3] Fraud & Anomaly Screening: Tier: {fraud_tier}")
    print(f"    Fraud Score: {fraud_score}/100")
    print(f"[4] Credit Decision:           {dec}")
    print(f"    Assigned Grade: {grade} ({subgrade})")
    print(f"    Interest Rate:  {rate:.2f}%")
    print(f"[5] Explainable AI (Top Attribution Drivers):")
    for factor in res["explainable_ai"]["top_risk_elevating_factors"][:2]:
        print(f"    - {factor}")
    print(f"[6] Blockchain Proof-of-Authority Audit Receipt:")
    print(f"    Block #{blk_idx} Hash: {blk_hash[:24]}...")
    print(f"\n[+] Total Straight-Through Processing Latency: {latency} ms")

def cmd_audit(args):
    print("NexusFin AI: Trust & Ethics Fair Lending Audit")
    dataset_path = args.dataset or DEFAULT_DATASET
    loader = DataLoader(dataset_path)
    underwriter = UnderwritingEngine()

    decisions = []
    for r in loader.raw_records:
        d = underwriter.evaluate_application(r)["decision"]
        decisions.append(d)

    auditor = BiasAuditor(disparate_impact_threshold=0.80)
    audit_res = auditor.audit_decisions(loader.raw_records, decisions, protected_attribute_key="application_type", privileged_value="Individual")

    prot = audit_res["protected_attribute"]
    priv_grp = audit_res["privileged_group"]
    priv_rate = audit_res["privileged_approval_rate"]
    unpriv_rate = audit_res["unprivileged_approval_rate"]
    di_ratio = audit_res["disparate_impact_ratio"]
    ff_pass = audit_res["four_fifths_rule_passed"]
    dp_pass = audit_res["demographic_parity_passed"]
    summary = audit_res["regulatory_summary"]

    print(f"Protected Attribute:       {prot}")
    print(f"Privileged Group:          {priv_grp} (Approval Rate: {priv_rate:.2%})")
    print(f"Unprivileged Group:        Joint App (Approval Rate: {unpriv_rate:.2%})")
    print(f"Disparate Impact Ratio:    {di_ratio:.4f}")
    print(f"Four-Fifths (80%) Passed:  {ff_pass}")
    print(f"Demographic Parity Passed: {dp_pass}")
    print(f"Regulatory Assessment:     {summary}")

def cmd_risk(args):
    print("NexusFin AI: Portfolio Credit Risk Management & Stress Testing")
    dataset_path = args.dataset or DEFAULT_DATASET
    loader = DataLoader(dataset_path)
    risk_mgr = PortfolioRiskManager()
    res = risk_mgr.analyze_portfolio(loader.raw_records)

    exposure = res["total_portfolio_exposure_usd"]
    count = res["loan_count"]
    el = res["expected_loss_usd"]
    el_rate = res["expected_loss_rate_pct"]
    var95 = res["value_at_risk_95_pct"]
    var99 = res["value_at_risk_99_pct"]
    cvar99 = res["conditional_var_99_pct"]

    print(f"Total Portfolio Exposure:  ${exposure:,.2f}")
    print(f"Total Number of Loans:     {count}")
    print(f"Expected Loss (EL):        ${el:,.2f} ({el_rate:.2f}%)")
    print(f"Value-at-Risk (95% VaR):   ${var95:,.2f}")
    print(f"Value-at-Risk (99% VaR):   ${var99:,.2f}")
    print(f"Conditional VaR (99% CVaR):${cvar99:,.2f}")
    print("\nMacroeconomic Stress Testing Projections:")
    for key, sc in res["stress_testing"].items():
        s_name = sc["scenario_name"]
        s_loss = sc["projected_loss_usd"]
        s_rate = sc["projected_loss_rate_pct"]
        s_status = sc["capital_adequacy_status"]
        print(f"  [{s_name}]")
        print(f"    Loss: ${s_loss:,.2f} ({s_rate}%) | Status: {s_status}")

def cmd_portfolio(args):
    print("NexusFin AI: Modern Portfolio Theory (Markowitz) Loan Optimization")
    allocator = PortfolioAllocator()
    res = allocator.optimize_allocation()

    opt = res["ai_optimal_tangency_portfolio"]
    print("AI Optimal Tangency Portfolio (Maximum Sharpe Ratio):")
    ret = opt['expected_net_return_pct']
    print(f"  Expected Net Return: {ret:.2f}%")
    vol = opt['expected_volatility_pct']
    print(f"  Expected Volatility: {vol:.2f}%")
    shp = opt['sharpe_ratio']
    print(f"  Sharpe Ratio:        {shp:.3f}")
    print("  Optimal Asset Allocation Weights:")
    for grade, weight in opt["allocation_weights"].items():
        print(f"    - {grade}: {weight:.1%}")

    print("\nComparison Against Benchmarks:")
    cons = res["benchmarks"]["conservative_portfolio"]
    eq = res["benchmarks"]["equal_weighted_portfolio"]
    cs = cons['sharpe_ratio']
    cr = cons['expected_return_pct']
    print(f"  - Conservative Portfolio Sharpe: {cs:.3f} (Return: {cr}%)")
    es = eq['sharpe_ratio']
    er = eq['expected_return_pct']
    print(f"  - Equal-Weighted Portfolio Sharpe: {es:.3f} (Return: {er}%)")

def cmd_quantum(args):
    print("NexusFin AI: Quantum Computing in Finance Simulation")
    sim = QuantumRiskSimulator(n_qubits=8, shots=2048)
    res = sim.simulate_quantum_var(portfolio_exposure=1000000.0, base_loss_rate=0.08)

    exp = res["portfolio_exposure_usd"]
    regs = res["quantum_registers_used"]
    shots = res["quantum_shots_evaluated"]
    qvar = res["quantum_estimated_var_99_usd"]
    c_mc = res["computational_complexity"]["classical_monte_carlo_complexity"]
    q_ae = res["computational_complexity"]["quantum_amplitude_estimation_complexity"]
    spd = res["computational_complexity"]["theoretical_quantum_speedup"]

    print(f"Simulated Portfolio Exposure: ${exp:,.2f}")
    print(f"Quantum Registers:            {regs}")
    print(f"Quantum Measurement Shots:    {shots}")
    print(f"Quantum Estimated 99% VaR:    ${qvar:,.2f}")
    print("Classical vs Quantum Complexity:")
    print(f"  - Classical Monte Carlo:    {c_mc}")
    print(f"  - Quantum Amplitude Est.:   {q_ae}")
    print(f"  - Theoretical Speedup:      {spd}")

    pqc = sim.assess_post_quantum_cryptography_impact()
    algo = pqc["pqc_migration_roadmap"]["nist_standardized_algorithms"][0]
    print("\nPost-Quantum Cryptography Assessment:")
    print(f"  Lattice Algorithms: {algo}")

def cmd_blockchain(args):
    print("NexusFin AI: Proof-of-Authority Blockchain Audit Ledger")
    ledger = BlockchainAuditLedger(difficulty=2)
    print("[*] Created Genesis Block.")
    print("[*] Recording credit transactions...")
    ledger.record_transaction("LOAN_DISBURSEMENT", "LN_1001", {"borrower": "B_991", "amount": 15000.0, "rate": 8.5})
    ledger.record_transaction("REPAYMENT_INSTALLMENT", "LN_1001", {"installment_num": 1, "amount": 473.50})
    mined = ledger.mine_pending_transactions(authority_validator="Consortium_Node_1")
    print(f"[+] Mined Block #{mined.index} with Hash: {mined.hash}")
    print(f"    Merkle Root: {mined.merkle_root}")
    print(f"    Nonce: {mined.nonce}")

    integrity = ledger.verify_chain_integrity()
    valid = integrity["valid"]
    tot = integrity["total_blocks_verified"]
    print(f"[+] Chain Cryptographic Integrity: {valid} ({tot} blocks verified)")

def main():
    parser = argparse.ArgumentParser(description="NexusFin AI - FinTech Banking Intelligence Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Pipeline
    p_pipe = subparsers.add_parser("pipeline", help="Run straight-through processing pipeline")
    p_pipe.add_argument("--dataset", type=str, default=DEFAULT_DATASET)

    # Audit
    p_audit = subparsers.add_parser("audit", help="Run trust & ethics fair lending audit")
    p_audit.add_argument("--dataset", type=str, default=DEFAULT_DATASET)

    # Risk
    p_risk = subparsers.add_parser("risk", help="Run portfolio risk and stress test")
    p_risk.add_argument("--dataset", type=str, default=DEFAULT_DATASET)

    # Portfolio
    subparsers.add_parser("portfolio", help="Run Markowitz portfolio optimization")

    # Quantum
    subparsers.add_parser("quantum", help="Run Quantum VaR simulation")

    # Blockchain
    subparsers.add_parser("blockchain", help="Run blockchain audit ledger verification")

    # Serve
    p_serve = subparsers.add_parser("serve", help="Start REST API & Web Dashboard")
    p_serve.add_argument("--port", type=int, default=5050)

    args = parser.parse_args()

    if args.command == "pipeline":
        cmd_pipeline(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "risk":
        cmd_risk(args)
    elif args.command == "portfolio":
        cmd_portfolio(args)
    elif args.command == "quantum":
        cmd_quantum(args)
    elif args.command == "blockchain":
        cmd_blockchain(args)
    elif args.command == "serve":
        run_server(args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
