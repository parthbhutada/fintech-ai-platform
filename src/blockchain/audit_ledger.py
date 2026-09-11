"""
Blockchain & Smart Contract Audit Ledger for FinTech.
Provides immutable transaction ledger, Merkle tree root verification,
and self-executing smart contract state machine for automated loan issuance.
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional

def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def compute_merkle_root(transactions: List[Dict[str, Any]]) -> str:
    if not transactions:
        return sha256_hash("empty_block")
    hashes = [sha256_hash(json.dumps(tx, sort_keys=True)) for tx in transactions]
    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i + 1]
            next_level.append(sha256_hash(combined))
        hashes = next_level
    return hashes[0]

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict[str, Any]], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = compute_merkle_root(transactions)
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.merkle_root}{self.previous_hash}{self.nonce}"
        return sha256_hash(block_string)

class SmartLoanContract:
    """
    Smart contract managing the lifecycle of an individual credit agreement.
    State transitions: SUBMITTED -> FRAUD_CLEARED -> UNDERWRITTEN -> APPROVED -> FUNDED -> CLOSED / DEFAULTED
    """
    VALID_TRANSITIONS = {
        "SUBMITTED": ["FRAUD_CLEARED", "REJECTED_FRAUD"],
        "FRAUD_CLEARED": ["UNDERWRITTEN"],
        "UNDERWRITTEN": ["APPROVED", "DENIED"],
        "APPROVED": ["FUNDED"],
        "FUNDED": ["IN_REPAYMENT"],
        "IN_REPAYMENT": ["FULLY_PAID", "CHARGED_OFF", "HARDSHIP_RELIEF"]
    }

    def __init__(self, loan_id: str, borrower_hash: str, principal: float, interest_rate: float):
        self.loan_id = loan_id
        self.borrower_hash = borrower_hash
        self.principal = principal
        self.interest_rate = interest_rate
        self.state = "SUBMITTED"
        self.history: List[Dict[str, Any]] = [{
            "timestamp": time.time(),
            "from_state": "NONE",
            "to_state": "SUBMITTED",
            "actor": "BORROWER"
        }]

    def transition_state(self, new_state: str, actor: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.state, [])
        if new_state not in allowed:
            raise ValueError(f"Illegal state transition from {self.state} to {new_state}.")
        self.history.append({
            "timestamp": time.time(),
            "from_state": self.state,
            "to_state": new_state,
            "actor": actor,
            "metadata": metadata or {}
        })
        self.state = new_state
        return True

class BlockchainAuditLedger:
    """
    Consortium Proof-of-Authority Blockchain for immutable credit records.
    """
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.smart_contracts: Dict[str, SmartLoanContract] = {}
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis_tx = [{"type": "GENESIS", "message": "NexusFin AI Consortium Banking Ledger Initiated"}]
        genesis_block = Block(0, 1600000000.0, genesis_tx, "0" * 64, nonce=0)
        self.chain.append(genesis_block)

    def record_transaction(self, tx_type: str, loan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        tx = {
            "tx_id": sha256_hash(f"{loan_id}_{time.time()}_{len(self.pending_transactions)}"),
            "tx_type": tx_type,
            "loan_id": loan_id,
            "timestamp": time.time(),
            "payload": data
        }
        self.pending_transactions.append(tx)
        return tx

    def mine_pending_transactions(self, authority_validator: str = "Central_Reserve_Node") -> Block:
        if not self.pending_transactions:
            raise ValueError("No pending transactions to commit.")

        prev_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=prev_block.hash
        )

        # Proof-of-Work / Difficulty target
        prefix = "0" * self.difficulty
        while not new_block.hash.startswith(prefix):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """
        Cryptographically validates every block, previous hash link, and Merkle tree root.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return {"valid": False, "error_block": i, "reason": "Current block hash invalid/tampered"}

            if current.previous_hash != prev.hash:
                return {"valid": False, "error_block": i, "reason": "Previous block hash pointer broken"}

            if current.merkle_root != compute_merkle_root(current.transactions):
                return {"valid": False, "error_block": i, "reason": "Merkle root checksum corrupted"}

        return {
            "valid": True,
            "total_blocks_verified": len(self.chain),
            "latest_block_hash": self.chain[-1].hash,
            "consensus_protocol": "Proof-of-Authority (Consortium Banking)"
        }
