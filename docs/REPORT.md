# CA-2 FinTech Application Reference Guide

> This file is a technical reference draft. The submitted report should be rewritten in the student's own words to satisfy the originality requirement.

## 1. Need Analysis

Small lenders need a quick and consistent way to review loan applications. Manual review takes time, while a prediction without supporting checks can miss fraud, unfair outcomes, or poor portfolio risk. This application demonstrates how AI-based scoring can support an initial lending decision using LendingClub records.

## 2. Technical Functionality

The application provides five related functions:

- **Credit scoring:** a small AutoML-style component compares simple logistic and boosting models and selects the best validation result.
- **Underwriting:** credit score, income, debt-to-income ratio, utilisation, enquiries, and delinquencies are converted into an approval, review, or denial decision.
- **Application checks:** text sentiment, basic anomaly detection, identity matching, and fairness metrics add practical safeguards around the decision.
- **Risk summary:** portfolio exposure, expected loss, VaR, stress scenarios, and simple allocation results demonstrate finance use cases.
- **Workflow and audit:** one orchestrator runs the checks in order and records a tamper-evident audit entry.

The main dataset is `dataset/accepted_2007_to_2018Q4.csv`. It is large, so local runs read the first 10,000 records by default. `DataLoader(..., max_records=None)` can be used when a full scan is required.

## 3. Architecture

The code is grouped into four easy-to-follow areas:

1. `src/data_credit.py` loads records and performs credit scoring and underwriting.
2. `src/analysis.py` contains fraud, text, fairness, identity, and decision-support checks.
3. `src/finance.py` contains portfolio, pricing, and risk calculations.
4. `src/operations.py` contains security, audit, and the end-to-end workflow.

The command-line interface and the small HTTP API call these modules. Existing feature folders contain the individual implementations, while the four modules above provide the simpler public structure.

## 4. Usage and Scope

Use Python 3.8 or newer. From the project directory:

```bash
python3 tests/run_all_tests.py
python3 src/cli.py pipeline
python3 src/cli.py audit
python3 src/cli.py risk
python3 src/cli.py portfolio
python3 src/cli.py serve --port 5050
```

The API is available at `http://localhost:5050`. The system is an educational simulator, not a production lending or financial-advice system. Its rules and model outputs require validation before any real lending use.

## 5. Impact Overview

The project demonstrates how AI can reduce repetitive first-pass review and make a credit workflow more consistent. Fairness checks, risk summaries, and audit records make the result easier to inspect. The main limitations are the simplified models, the fixed row cap for local runs, and the fact that LendingClub historical data may not represent current applicants.

## 6. Rubric Mapping

| Criterion | Evidence |
| --- | --- |
| Functionality (4) | Credit scoring, underwriting, fraud checks, risk analysis, workflow, CLI, API, and 18 tests |
| Code quality (2) | Grouped public modules, typed helper classes, configuration files, and focused tests |
| Report quality (2) | Need, technical functionality, architecture, usage, scope, and impact sections |
| Guidelines (2) | Private repository can be shared with `anupkumar-bongale`; the main dataset and test command are documented |
