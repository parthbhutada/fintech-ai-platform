import unittest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.schema import clean_float, clean_emp_length, FEATURE_COLUMNS
from src.core.data_loader import DataLoader

class TestCore(unittest.TestCase):
    def test_clean_float(self):
        self.assertEqual(clean_float("3600.0"), 3600.0)
        self.assertEqual(clean_float("$10,500.50"), 10500.5)
        self.assertEqual(clean_float("13.99%"), 13.99)
        self.assertEqual(clean_float("", 5.0), 5.0)
        self.assertEqual(clean_float(None, 0.0), 0.0)

    def test_clean_emp_length(self):
        self.assertEqual(clean_emp_length("10+ years"), 10.0)
        self.assertEqual(clean_emp_length("< 1 year"), 0.5)
        self.assertEqual(clean_emp_length("3 years"), 3.0)
        self.assertEqual(clean_emp_length(""), 0.0)

    def test_data_loader(self):
        loader = DataLoader("dataset/lending_club_snippet.csv")
        self.assertEqual(len(loader.raw_records), 5)
        X, y, f_names = loader.get_features_and_labels()
        self.assertEqual(len(X), 5)
        self.assertEqual(len(y), 5)
        self.assertEqual(len(f_names), len(FEATURE_COLUMNS))
