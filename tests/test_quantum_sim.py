import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quantum_sim.quantum_risk import QuantumRiskSimulator

class TestQuantumSim(unittest.TestCase):
    def test_quantum_var(self):
        sim = QuantumRiskSimulator(n_qubits=6, shots=512)
        res = sim.simulate_quantum_var(portfolio_exposure=100000.0, base_loss_rate=0.08)
        self.assertIn("quantum_estimated_var_99_usd", res)
        self.assertGreater(res["quantum_estimated_var_99_usd"], 0)
        self.assertIn("computational_complexity", res)
