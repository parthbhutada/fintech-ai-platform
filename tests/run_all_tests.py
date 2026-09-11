"""
Unified Test Runner for NexusFin AI Platform.
Discovers and executes all unit tests across all 13 modules, generating a summary report.
"""

import unittest
import sys
import os

def run_suite():
    print("=" * 75)
    print("NEXUSFIN AI - AUTOMATED TEST RUNNER (ALL 13 MODULES)")
    print("=" * 75)
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 75)
    print("TEST SUITE EXECUTION SUMMARY:")
    print(f"  Tests Run:   {result.testsRun}")
    print(f"  Failures:    {len(result.failures)}")
    print(f"  Errors:      {len(result.errors)}")
    print(f"  Success:     {result.wasSuccessful()}")
    print("=" * 75)

    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
