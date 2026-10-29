import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.blockchain.audit_ledger import BlockchainAuditLedger

class TestBlockchain(unittest.TestCase):
    def test_blockchain_ledger(self):
        ledger = BlockchainAuditLedger(difficulty=1)
        ledger.record_transaction("TEST_TX", "L1", {"data": 123})
        mined = ledger.mine_pending_transactions()
        self.assertEqual(mined.index, 1)
        self.assertGreater(len(ledger.chain), 1)
        integrity = ledger.verify_chain_integrity()
        self.assertTrue(integrity["valid"])
