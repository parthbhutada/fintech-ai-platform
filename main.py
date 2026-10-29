"""Run the complete CA-2 workflow from dataset to saved decision output."""

import argparse
import json
import os

from src.core.data_loader import DEFAULT_DATASET, DataLoader
from src.automation.orchestrator import FinTechSTPOrchestrator


def run(dataset_path: str, max_records: int, output_path: str) -> dict:
    orchestrator = FinTechSTPOrchestrator()
    training = orchestrator.bootstrap_models(dataset_path)

    loader = DataLoader(dataset_path, max_records=max_records)
    if not loader.raw_records:
        raise ValueError("The selected dataset does not contain any records.")

    application = loader.raw_records[0]
    decision = orchestrator.process_application_stp(application)
    result = {
        "dataset": dataset_path,
        "records_used": len(loader.raw_records),
        "selected_model": training["best_model_name"],
        "model_metrics": training["best_metrics"],
        "application_id": decision["application_id"],
        "decision": decision["underwriting_decision"],
        "fraud_check": decision["fraud_detection_result"],
        "audit_receipt": decision["blockchain_audit_receipt"],
    }

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=2)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and run the FinTech lending workflow.")
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--max-records", type=int, default=10000)
    parser.add_argument("--output", default="outputs/run_result.json")
    args = parser.parse_args()

    result = run(args.dataset, args.max_records, args.output)
    print(f"Dataset records used: {result['records_used']}")
    print(f"Selected model: {result['selected_model']}")
    print(f"Application decision: {result['decision']['decision']}")
    print(f"Saved result: {args.output}")


if __name__ == "__main__":
    main()