"""
SEG301 Exam Prep Portal - Comprehensive E2E Test Suite Runner
Runs baseline regression tests and all 4 test tiers (Tiers 1-4, >=173 tests)
Outputs TAP version 13 results and structured execution summaries.
"""

import argparse
import os
import subprocess
import sys
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.test_harness import CSSAnalyzer, JSAnalyzer, EdgeCDPDriver, TestReporter
from tests.tier1_features import run_tier1_tests
from tests.tier2_boundaries import run_tier2_tests
from tests.tier3_cross_feature import run_tier3_tests
from tests.tier4_real_world import run_tier4_tests


def run_baseline_regression() -> bool:
    print("=" * 70)
    print("GATE 0: BASELINE KNOWLEDGE INTEGRITY REGRESSION CHECK")
    print("=" * 70)
    cmd = [sys.executable, os.path.join(PROJECT_ROOT, "test_knowledge_integrity.py")]
    res = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("❌ BASELINE REGRESSION FAILED:")
        print(res.stderr)
        return False
    print("✓ Gate 0: Knowledge integrity regression check PASSED (8/8 gates intact).\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="SEG301 Exam Prep Portal E2E Test Runner")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Run only specified tier (1-4)")
    parser.add_argument("--tap-file", type=str, default="tests/results.tap", help="Path to save TAP output")
    parser.add_argument("--skip-baseline", action="store_true", help="Skip Gate 0 baseline regression check")
    parser.add_argument("--allow-failures", action="store_true", help="Exit 0 even if feature tests fail (for pre-implementation assessment)")
    args = parser.parse_args()

    start_time = time.time()

    # Step 1: Run Gate 0 Baseline Regression
    if not args.skip_baseline:
        if not run_baseline_regression():
            sys.exit(1)

    # Step 2: Initialize Analyzers
    css = CSSAnalyzer()
    js = JSAnalyzer()
    reporter = TestReporter()

    # Step 3: Initialize Headless Edge Browser via CDP
    print("=" * 70)
    print("INITIALIZING E2E RUNTIME: MICROSOFT EDGE HEADLESS (CDP)")
    print("=" * 70)
    driver = EdgeCDPDriver(headless=True)
    try:
        driver.start()
        print(f"✓ Edge Browser connected via CDP on port {driver.cdp_port}")
        print(f"✓ Local HTTP Server running on http://127.0.0.1:{driver.http_port}")
        print("=" * 70)

        # Step 4: Execute Selected Tiers
        if args.tier is None or args.tier == 1:
            run_tier1_tests(driver, css, js, reporter)

        if args.tier is None or args.tier == 2:
            run_tier2_tests(driver, css, js, reporter)

        if args.tier is None or args.tier == 3:
            run_tier3_tests(driver, css, js, reporter)

        if args.tier is None or args.tier == 4:
            run_tier4_tests(driver, css, js, reporter)

    finally:
        driver.stop()
        print("\n✓ Headless Edge browser and local test server safely terminated.")

    # Step 5: Generate and Save TAP Output
    tap_output = reporter.generate_tap()
    tap_path = os.path.join(PROJECT_ROOT, args.tap_file)
    with open(tap_path, "w", encoding="utf-8") as f:
        f.write(tap_output)
    print(f"✓ TAP version 13 test report saved to: {tap_path}")

    # Step 6: Print Formatted Summary
    reporter.print_summary()
    total_duration = time.time() - start_time
    print(f"Total Test Run Time: {total_duration:.2f}s\n")

    # Step 7: Check Failures
    failed_count = sum(1 for r in reporter.results if not r.passed)
    if failed_count > 0:
        print(f"⚠️  {failed_count} tests failed.")
        if not args.allow_failures:
            sys.exit(1)
        else:
            print("Note: --allow-failures specified. Exiting with code 0.")
            sys.exit(0)
    else:
        print("🎉 ALL TESTS PASSED SUCCESSFULLY! (100% Pass Rate)")
        sys.exit(0)


if __name__ == "__main__":
    main()
