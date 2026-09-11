"""
Quantum Computing in Banking & Finance Simulator.
Simulates:
1. Quantum Amplitude Estimation (QAE) for quadratic speedup in Value-at-Risk (VaR).
2. Quantum Approximate Optimization Algorithm (QAOA) for portfolio knapsack allocation.
3. Post-Quantum Cryptography (PQC) impact assessment on banking security.
"""

import math
import random
from typing import Dict, List, Any

class QuantumRiskSimulator:
    def __init__(self, n_qubits: int = 8, shots: int = 2048):
        self.n_qubits = n_qubits
        self.shots = shots

    def simulate_quantum_var(self, portfolio_exposure: float, base_loss_rate: float, confidence_level: float = 0.99) -> Dict[str, Any]:
        """
        Simulates Quantum Amplitude Estimation (Brassard et al.) for credit loss distribution.
        Classical Monte Carlo convergence: O(1/sqrt(M)).
        Quantum Amplitude Estimation convergence: O(1/M) (quadratic speedup).
        """
        # Simulated quantum state vector across 2^n_qubits states
        num_states = 2 ** min(self.n_qubits, 10)
        state_amplitudes = []

        # Construct quantum probability distribution
        total_amp_sq = 0.0
        for k in range(num_states):
            x = k / num_states
            # Tail risk distribution
            prob_density = math.exp(-0.5 * ((x - base_loss_rate) / 0.08) ** 2)
            state_amplitudes.append(prob_density)
            total_amp_sq += prob_density ** 2

        # Normalize state amplitudes (sum of |alpha_i|^2 = 1)
        norm_factor = math.sqrt(total_amp_sq)
        normalized_probs = [(a / norm_factor) ** 2 for a in state_amplitudes]

        # Quantum measurement shots sampling
        cumulative_probs = []
        c = 0.0
        for p in normalized_probs:
            c += p
            cumulative_probs.append(c)

        quantum_samples = []
        for _ in range(self.shots):
            r = random.random()
            for idx, cp in enumerate(cumulative_probs):
                if r <= cp:
                    quantum_samples.append((idx / num_states) * portfolio_exposure)
                    break

        quantum_samples.sort()
        idx_var = int(confidence_level * len(quantum_samples))
        quantum_var = round(quantum_samples[min(idx_var, len(quantum_samples) - 1)], 2)

        # Classical vs Quantum convergence analysis
        classical_iterations_needed = int((1.0 / (0.005 ** 2)))  # ~40,000 iterations for 0.5% precision
        quantum_oracle_calls_needed = int(1.0 / 0.005)           # ~200 oracle calls for 0.5% precision
        speedup_factor = round(classical_iterations_needed / quantum_oracle_calls_needed, 1)

        return {
            "portfolio_exposure_usd": portfolio_exposure,
            "quantum_registers_used": f"{self.n_qubits} qubits (Hilbert space dimension: {num_states})",
            "quantum_shots_evaluated": self.shots,
            "quantum_estimated_var_99_usd": quantum_var,
            "quantum_var_rate_pct": round((quantum_var / portfolio_exposure) * 100.0, 2),
            "computational_complexity": {
                "classical_monte_carlo_complexity": "O(1 / epsilon^2)",
                "quantum_amplitude_estimation_complexity": "O(1 / epsilon)",
                "theoretical_quantum_speedup": f"{speedup_factor}x reduction in query evaluations"
            }
        }

    def simulate_qaoa_portfolio_selection(self, loan_returns: List[float], loan_risks: List[float], budget: float) -> Dict[str, Any]:
        """
        Simulates QAOA (Quantum Approximate Optimization Algorithm) for combinatorial credit portfolio selection.
        Minimizes Ising Hamiltonian: H = lambda1 * Risk - lambda2 * Return + penalty * (Weight - Budget)^2
        """
        n_assets = len(loan_returns)
        best_state = None
        best_cost = float("inf")

        # Simulate quantum superposition phase sampling
        for _ in range(min(512, 2 ** n_assets)):
            # Random bitstring representing candidate loan selection
            bitstring = [random.choice([0, 1]) for _ in range(n_assets)]
            selected_count = sum(bitstring)
            if selected_count == 0:
                continue

            cost_risk = sum(b * r for b, r in zip(bitstring, loan_risks))
            gain_ret = sum(b * r for b, r in zip(bitstring, loan_returns))
            penalty = 5.0 * abs(selected_count - budget)

            hamiltonian_energy = cost_risk - 1.5 * gain_ret + penalty
            if hamiltonian_energy < best_cost:
                best_cost = hamiltonian_energy
                best_state = bitstring

        return {
            "qaoa_optimal_qubit_state": best_state,
            "selected_asset_indices": [i for i, b in enumerate(best_state) if b == 1] if best_state else [],
            "ground_state_energy": round(best_cost, 4),
            "optimization_paradigm": "Quantum Variational Eigensolver (VQE/QAOA)"
        }

    def assess_post_quantum_cryptography_impact(self) -> Dict[str, Any]:
        """
        Assesses quantum threats to banking infrastructure and evaluates PQC readiness.
        """
        return {
            "threat_analysis": {
                "rsa_and_elliptic_curves": "VULNERABLE: Shor algorithm factors RSA-2048 in polynomial time O((log N)^3)",
                "symmetric_encryption_aes": "SAFE_WITH_UPGRADE: Grover algorithm provides square-root speedup; AES-256 remains secure with 128-bit quantum security."
            },
            "pqc_migration_roadmap": {
                "nist_standardized_algorithms": [
                    "CRYSTALS-Kyber (Lattice-based Key Encapsulation)",
                    "CRYSTALS-Dilithium (Lattice-based Digital Signatures)",
                    "SPHINCS+ (Stateless Hash-based Signatures)"
                ],
                "banking_impact": "Financial institutions must transition SWIFT, core banking ledgers, and API tokens to hybrid Classical-PQC algorithms by 2030."
            }
        }
