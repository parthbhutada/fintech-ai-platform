"""
Demo: Quantum Risk Computing & Blockchain Proof-of-Authority Audit Ledger.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quantum_sim.quantum_risk import QuantumRiskSimulator
from src.blockchain.audit_ledger import BlockchainAuditLedger

def main():
    print("=" * 75)
    print("DEMO: QUANTUM COMPUTING IN FINANCE & BLOCKCHAIN SMART LEDGER")
    print("=" * 75)
    
    # 1. Quantum Monte Carlo VaR Simulation
    print("[1] Quantum Amplitude Estimation (QAE) for Tail Risk:")
    q_sim = QuantumRiskSimulator(n_qubits=8, shots=2048)
    q_res = q_sim.simulate_quantum_var(portfolio_exposure=5000000.0, base_loss_rate=0.075)

    print(f"    Portfolio Exposure:    ${q_res['portfolio_exposure_usd']:,.2f}")
    print(f"    Qubit Registers:       {q_res['quantum_registers_used']}")
    print(f"    Quantum 99% VaR:       ${q_res['quantum_estimated_var_99_usd']:,.2f} ({q_res['quantum_var_rate_pct']:.2f}%)")
    print(f"    Classical Complexity:  {q_res['computational_complexity']['classical_monte_carlo_complexity']}")
    print(f"    Quantum Complexity:    {q_res['computational_complexity']['quantum_amplitude_estimation_complexity']}")
    print(f"    Quantum Acceleration:  {q_res['computational_complexity']['theoretical_quantum_speedup']}")

    # 2. Blockchain Audit Ledger & Merkle Validation
    print("\n[2] Blockchain Smart Contract & Proof-of-Authority Mining:")
    ledger = BlockchainAuditLedger(difficulty=2)
    ledger.record_transaction("SMART_LOAN_ISSUED", "LOAN_88921", {"principal": 25000.0, "rate": 11.5})
    ledger.record_transaction("COLLATERAL_LOCKED", "LOAN_88921", {"token_id": "NFT_COLLATERAL_99"})
    
    block = ledger.mine_pending_transactions(authority_validator="Consortium_Node_ALPHA")
    print(f"    Mined Block Index:     #{block.index}")
    print(f"    Block Hash:            {block.hash}")
    print(f"    Previous Block Hash:   {block.previous_hash}")
    print(f"    Merkle Tree Root:      {block.merkle_root}")
    print(f"    Proof-of-Work Nonce:   {block.nonce}")

    integrity = ledger.verify_chain_integrity()
    print(f"    Cryptographic Integrity Status: {integrity['valid']} ({integrity['total_blocks_verified']} blocks verified)")
    print("=" * 75)

if __name__ == "__main__":
    main()
