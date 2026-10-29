"""
Unified Test Runner for NexusFin AI Platform.
Discovers and executes the project's unit tests, then prints a short summary.
"""

import unittest
import sys
import os

def run_suite():
    print("Running project tests")
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("TEST SUITE EXECUTION SUMMARY:")
    print(f"  Tests Run:   {result.testsRun}")
    print(f"  Failures:    {len(result.failures)}")
    print(f"  Errors:      {len(result.errors)}")
    print(f"  Success:     {result.wasSuccessful()}")

    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
