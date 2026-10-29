# FinTech AI Lending Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-18%2F18%20Passing-brightgreen.svg)]()
[![Zero-Dependency](https://img.shields.io/badge/Architecture-Zero--Dependency%20Fallback-orange.svg)]()

> **CA-2: Coding-based Assignment Submission (10 Marks)**  
> **Course Syllabus Coverage:** State of the Art Technologies in Banking and Finance (Unit 3) & Use-Cases of Smart Societies (Unit 4)  
> **Instructor GitHub:** `anupkumar-bongale`  
> **Dataset Utilized:** LendingClub Consumer Credit Records  

---

## Executive Summary

This is a small FinTech application for CA-2. It uses AI-style credit scoring and simple rule checks to review LendingClub loan records. The application also demonstrates fraud checks, fairness measurement, risk summaries, and a traceable processing workflow.

---

## Repository Structure

```
fintech-ai-platform/
│
├── README.md                           # Comprehensive setup, quickstart, and project guide
├── requirements.txt                    # Python dependencies (pandas, scikit-learn, flask, etc.)
├── Dockerfile                          # Multi-stage lightweight container deployment
├── setup.py                            # Standard package installation script
│
├── config/                             # Central Configuration Store
│   ├── app_config.json                 # System thresholds, underwriting rules, risk parameters
│   └── ethics_policy.json              # Fair lending standards (EEOC 80% disparate impact rule)
│
├── dataset/                            # LendingClub data
│   └── accepted_2007_to_2018Q4.csv      # Main dataset used by the application
│
├── docs/                               # Formal Documentation & Deliverables
│   ├── REPORT.md                       # Complete 5-Section Academic Reference Guide & Report
│   ├── ARCHITECTURE.md                 # System architecture diagrams & technical flow
│   └── API_REFERENCE.md                # REST API and Python Library documentation
│
├── src/                                # Application code
│   ├── __init__.py
│   ├── data_credit.py                  # Data loading and credit decisions
│   ├── analysis.py                     # Fraud, text, fairness, and identity checks
│   ├── finance.py                      # Portfolio and risk calculations
│   ├── operations.py                   # Security, audit, and workflow tools
│   ├── core/                           # Data loading, schema validation, normalization
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── schema.py
│   ├── credit_scoring/                 # Unit 3 AutoML & Unit 4 Credit Decisions
│   │   ├── __init__.py
│   │   ├── automl.py
│   │   └── underwriting.py
│   ├── explainability/                 # Unit 3 Explainable AI (SHAP & Counterfactuals)
│   │   ├── __init__.py
│   │   └── xai_engine.py
│   ├── ethics_fairness/                # Unit 3 Trust & Ethics in AI (Disparate Impact)
│   │   ├── __init__.py
│   │   └── bias_auditor.py
│   ├── fraud_prevention/               # Unit 4 Fraud Prevention & Anomaly Detection
│   │   ├── __init__.py
│   │   └── anomaly_detector.py
│   ├── risk_management/                # Unit 4 Risk Management (VaR, CVaR, Stress Testing)
│   │   ├── __init__.py
│   │   └── portfolio_risk.py
│   ├── trading_portfolio/              # Unit 4 Trading & Portfolio Allocation
│   │   ├── __init__.py
│   │   └── portfolio_allocator.py
│   ├── personalized_banking/           # Unit 4 Personalized Banking & Dynamic Pricing
│   │   ├── __init__.py
│   │   └── recommendations.py
│   ├── cognitive_ai/                   # Unit 3 Cognitive AI & NLP Text Analysis
│   │   ├── __init__.py
│   │   └── nlp_underwriter.py
│   ├── security_privacy/               # Unit 3 Security, Access & Differential Privacy
│   │   ├── __init__.py
│   │   └── privacy_guard.py
│   ├── biometrics/                     # Unit 3 Biometric Processing & Identity Verification
│   │   ├── __init__.py
│   │   └── biometric_auth.py
│   ├── quantum_sim/                    # Unit 3 Quantum Computing Simulation in Finance
│   │   ├── __init__.py
│   │   └── quantum_risk.py
│   ├── blockchain/                     # Unit 3 Cryptocurrency & Smart Contract Audit Ledger
│   │   ├── __init__.py
│   │   └── audit_ledger.py
│   ├── automation/                     # Unit 3 & 4 RPA Straight-Through Processing (STP)
│   │   ├── __init__.py
│   │   ├── rpa_engine.py
│   │   └── orchestrator.py
│   ├── wireless_banking/               # Unit 4 Wireless Banking (Japan Case Study API)
│   │   ├── __init__.py
│   │   └── open_banking_gateway.py
│   ├── api/                            # Interactive Web Dashboard & Microservice API
│   │   ├── __init__.py
│   │   └── server.py
│   └── cli.py                          # Unified Command-Line Interface
│
├── examples/                           # Standalone Runnable Demonstrations
│   ├── demo_end_to_end.py              # Full straight-through processing pipeline demo
│   ├── demo_credit_and_xai.py          # Credit scoring with SHAP and counterfactuals
│   ├── demo_fairness_audit.py          # Fairness & ethics bias audit
│   ├── demo_quantum_and_blockchain.py  # Quantum risk + blockchain ledger demonstration
│   └── demo_portfolio_and_fraud.py     # Loan trading portfolio + fraud anomaly detector
│
└── tests/                              # Automated Unit Test Suite (100% Pass Rate)
    ├── __init__.py
    ├── test_core.py
    ├── test_credit_scoring.py
    ├── test_explainability.py
    ├── test_ethics_fairness.py
    ├── test_fraud_prevention.py
    ├── test_risk_management.py
    ├── test_trading_portfolio.py
    ├── test_cognitive_ai.py
    ├── test_security_privacy.py
    ├── test_biometrics.py
    ├── test_quantum_sim.py
    ├── test_blockchain.py
    ├── test_automation.py
    └── run_all_tests.py
```

---

## Syllabus Coverage Matrix (Unit 3 & Unit 4)

| Syllabus Unit | Topic | Implementation in Codebase |
| :--- | :--- | :--- |
| **Unit 3** | AI Tools, Frameworks & AutoML | `src/credit_scoring/automl.py`: Multi-model auto-tuning, ROC-AUC metric tracking, algorithm leaderboard. |
| **Unit 3** | Cutting Edge Developments | `src/automation/orchestrator.py`: Sub-millisecond Straight-Through Processing (STP). |
| **Unit 3** | Trust and Ethics in AI | `src/ethics_fairness/bias_auditor.py`: Disparate Impact Ratio (EEOC 80% rule), threshold calibration. |
| **Unit 3** | Explainable AI (XAI) | `src/explainability/xai_engine.py`: Shapley-style local attribution and counterfactual guidance. |
| **Unit 3** | Security, Access & Privacy | `src/security_privacy/privacy_guard.py`: Epsilon-Differential Privacy (Laplace noise), salted SHA-256 PII hashing, RBAC. |
| **Unit 3** | Biometric Data Processing | `src/biometrics/biometric_auth.py`: Cosine similarity on facial embeddings, liveness score, step-up MFA. |
| **Unit 3** | Cognitive AI | `src/cognitive_ai/nlp_underwriter.py`: Financial sentiment extraction and latent risk detection from loan descriptions. |
| **Unit 3** | Robotics & Automation (RPA) | `src/automation/rpa_engine.py`: Batch document validation and automated routing bot. |
| **Unit 3** | Quantum Computing in Finance | `src/quantum_sim/quantum_risk.py`: Quantum Amplitude Estimation (quadratic speedup for VaR) & Post-Quantum Cryptography roadmap. |
| **Unit 3** | Cryptocurrency & Blockchain | `src/blockchain/audit_ledger.py`: Proof-of-Authority consensus, Merkle roots, smart contract lifecycle. |
| **Unit 4** | Wireless Banking (Japan Case) | `src/wireless_banking/open_banking_gateway.py`: Japan NTT DOCOMO / Seven Bank inspired contactless API gateway. |
| **Unit 4** | Credit Decisions | `src/credit_scoring/underwriting.py`: Rule-based & ML credit grade assignment (A-G), debt capacity calculation. |
| **Unit 4** | Risk Management using AI | `src/risk_management/portfolio_risk.py`: Value-at-Risk (95%/99%), Conditional VaR, and macroeconomic stress testing. |
| **Unit 4** | Fraud Prevention using AI | `src/fraud_prevention/anomaly_detector.py`: Synthetic identity detection, inquiry bursts, multivariate outlier scoring. |
| **Unit 4** | Trading & Portfolio Optimization | `src/trading_portfolio/portfolio_allocator.py`: Modern Portfolio Theory (Markowitz Mean-Variance Sharpe tangency). |
| **Unit 4** | Personalized Banking | `src/personalized_banking/recommendations.py`: Dynamic risk pricing, 3-tier loan payoff options, hardship restructuring. |
| **Unit 4** | Finance Process Automation | `src/automation/orchestrator.py`: Full end-to-end straight-through credit automation. |

---

## Quickstart Guide

### 1. Main End-to-End Run
The main file performs the complete sequence: load the accepted dataset, train and select a model, process one application, and save the final result.
```bash
python3 main.py
```
The result is written to `outputs/run_result.json`. Use `--max-records` to control the training sample size.

### 2. Verification & Automated Tests
Run the complete test suite:
```bash
python3 tests/run_all_tests.py
```
*Expected Result: 18 tests run, 0 failures, 0 errors.*

### 3. Command Line Interface (CLI)
```bash
# Run the end-to-end lending workflow on the main dataset
python3 src/cli.py pipeline

# Run regulatory fair lending audit
python3 src/cli.py audit

# Calculate portfolio credit risk & macroeconomic stress tests
python3 src/cli.py risk

# Optimize loan portfolio allocation (Markowitz Efficient Frontier)
python3 src/cli.py portfolio

# Simulate Quantum Monte Carlo VaR calculation
python3 src/cli.py quantum

# Verify blockchain transactions and cryptographic integrity
python3 src/cli.py blockchain
```

### 4. Interactive Web Dashboard & REST API
Start the platform server on port 5050:
```bash
python3 src/cli.py serve --port 5050
```
Open your browser at `http://localhost:5050` to view the interactive FinTech dashboard and test live underwriting requests.

---

## Submission Guide: Sharing with Instructor

To submit the assignment to the instructor (`anupkumar-bongale`) via private GitHub repository:

```bash
# 1. Initialize git inside the project directory
cd /Users/parth.bhutada/.gemini/antigravity/scratch/fintech-ai-platform
git init
git add .
git commit -m "Initial commit: NexusFin AI Complete FinTech Platform (CA-2 Submission)"

# 2. Create a private repository on GitHub (e.g., named fintech-ai-assignment)
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main

# 3. Share with instructor:
# Go to GitHub Repository -> Settings -> Collaborators -> Add people
# Search for username: anupkumar-bongale
# Select "Add anupkumar-bongale to this repository"
```

The formal academic report is included at [`docs/REPORT.md`](docs/REPORT.md).
