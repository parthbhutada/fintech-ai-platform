# NexusFin AI - REST API & Library Reference

The application provides a small HTTP API and reusable Python modules.

---

## 1. REST Microservice Endpoints

Base URL: `http://localhost:5050`

### `GET /health`
Returns system operational state and registered modules.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "modules": ["credit", "analysis", "risk", "workflow"]
}
```

---

### `POST /api/v1/stp`
Executes straight-through automated credit underwriting, fraud screening, XAI attribution, blockchain mining, and personalized offer generation.

**Request Payload:**
```json
{
  "id": "68407277",
  "loan_amnt": 3600.0,
  "annual_inc": 55000.0,
  "fico_range_high": 679.0,
  "dti": 5.91,
  "revol_util": 29.7,
  "purpose": "debt_consolidation",
  "title": "Debt consolidation"
}
```

**Response (200 OK):**
```json
{
  "application_id": "68407277",
  "borrower_hash": "4a91b...",
  "straight_through_processing_latency_ms": 0.25,
  "biometric_verification": {
    "authenticated": true,
    "similarity_score": 1.0,
    "liveness_passed": true
  },
  "underwriting_decision": {
    "decision": "APPROVED",
    "assigned_grade": "C",
    "offered_interest_rate_pct": 14.49,
    "default_probability": 0.125
  },
  "explainable_ai": {
    "top_risk_elevating_factors": ["inquiries_6m: adds +3.50% default risk"],
    "actionable_counterfactuals": [
      {
        "action": "Lower Debt-to-Income (DTI)",
        "impact": "Reduces monthly debt burden, boosting approval probability."
      }
    ]
  },
  "blockchain_audit_receipt": {
    "block_index": 1,
    "block_hash": "0c53...",
    "merkle_root": "7951..."
  }
}
```

---

### `GET /api/v1/risk`
Returns portfolio-wide credit exposure, Value-at-Risk (95%/99%), Conditional VaR (Expected Shortfall), and macroeconomic stress test projections.

---

### `GET /api/v1/portfolio`
Returns Modern Portfolio Theory (Markowitz) optimal asset allocation weights across credit tiers to maximize the Sharpe ratio.

---

### `GET /api/v1/quantum`
Returns simulated Quantum Amplitude Estimation (QAE) Value-at-Risk results and computational complexity comparisons.

---

## 2. Python SDK Usage

```python
from src.automation.orchestrator import FinTechSTPOrchestrator

orchestrator = FinTechSTPOrchestrator()
orchestrator.bootstrap_models("dataset/accepted_2007_to_2018Q4.csv")

applicant = {
    "id": "LOAN_401",
    "loan_amnt": 10000.0,
    "annual_inc": 75000.0,
    "fico_range_high": 725.0,
    "dti": 14.2,
    "revol_util": 22.5
}

result = orchestrator.process_application_stp(applicant)
print("Decision:", result["underwriting_decision"]["decision"])
print("Offered Rate:", result["underwriting_decision"]["offered_interest_rate_pct"])
print("Blockchain Block:", result["blockchain_audit_receipt"]["block_index"])
```
