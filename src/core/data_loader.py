"""
Data ingestion, cleaning, normalization, and statistical profiling.
Zero-dependency implementation with transparent pandas compatibility.
"""

import csv
import math
from typing import List, Dict, Any, Tuple, Optional
from src.core.schema import FEATURE_COLUMNS, TARGET_COLUMN, DEFAULT_STATUSES, clean_float, clean_emp_length

class DataLoader:
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath
        self.raw_records: List[Dict[str, str]] = []
        self.feature_names: List[str] = FEATURE_COLUMNS.copy()
        self.stats: Dict[str, Dict[str, float]] = {}
        if filepath:
            self.load(filepath)

    def load(self, filepath: str) -> List[Dict[str, str]]:
        self.filepath = filepath
        records = []
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        self.raw_records = records
        self._compute_feature_stats()
        return self.raw_records

    def _compute_feature_stats(self) -> None:
        if not self.raw_records:
            return
        for col in self.feature_names:
            vals = [clean_float(r.get(col, 0.0)) for r in self.raw_records]
            if not vals:
                continue
            n = len(vals)
            mean_val = sum(vals) / n
            variance = sum((x - mean_val) ** 2 for x in vals) / (n if n > 1 else 1)
            std_val = math.sqrt(variance) if variance > 1e-9 else 1.0
            self.stats[col] = {
                "mean": mean_val,
                "std": std_val,
                "min": min(vals),
                "max": max(vals),
                "count": float(n)
            }

    def get_features_and_labels(self) -> Tuple[List[List[float]], List[int], List[str]]:
        """Extract numerical feature matrix X and binary default label y."""
        X: List[List[float]] = []
        y: List[int] = []
        valid_ids: List[str] = []

        for r in self.raw_records:
            status = r.get(TARGET_COLUMN, "").strip()
            if status not in DEFAULT_STATUSES:
                # Default to 0 (non-default) if unknown
                label = 0
            else:
                label = DEFAULT_STATUSES[status]

            row_vec = []
            for col in self.feature_names:
                v = clean_float(r.get(col, 0.0))
                # standardize
                mean = self.stats.get(col, {}).get("mean", 0.0)
                std = self.stats.get(col, {}).get("std", 1.0)
                z = (v - mean) / (std if std != 0 else 1.0)
                row_vec.append(z)

            X.append(row_vec)
            y.append(label)
            valid_ids.append(r.get("id", str(len(valid_ids))))

        return X, y, self.feature_names

    def train_test_split(self, test_size: float = 0.25, seed: int = 42) -> Tuple[List[List[float]], List[List[float]], List[int], List[int]]:
        import random
        X, y, _ = self.get_features_and_labels()
        combined = list(zip(X, y))
        rng = random.Random(seed)
        rng.shuffle(combined)
        split_idx = int(len(combined) * (1 - test_size))
        train = combined[:split_idx]
        test = combined[split_idx:]
        X_train = [c[0] for c in train]
        y_train = [c[1] for c in train]
        X_test = [c[0] for c in test]
        y_test = [c[1] for c in test]
        return X_train, X_test, y_train, y_test

    def get_summary_profile(self) -> Dict[str, Any]:
        return {
            "total_records": len(self.raw_records),
            "features_tracked": len(self.feature_names),
            "feature_stats": self.stats
        }
