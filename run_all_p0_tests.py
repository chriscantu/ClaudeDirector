#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path


def run_all_p0_tests():
    """Run all P0 tests and collect results"""
    p0_dir = Path(".claudedirector/tests/regression/p0_blocking/")

    if not p0_dir.exists():
        print("❌ P0 test directory not found!")
        return

    # Find all test files
    test_files = list(p0_dir.glob("test_*.py"))
    test_files.extend(list(p0_dir.glob("memory_context_modules/test_*.py")))

    print(f"🔍 Found {len(test_files)} P0 test files")

    results = {"passed": [], "failed": [], "skipped": [], "error": []}

    total_tests = 0

    for test_file in sorted(test_files):
        try:
            print(f"\n🧪 Running: {test_file.name}")
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Count tests in this file
            if "Ran " in result.stderr:
                test_count_line = [
                    line
                    for line in result.stderr.split("\n")
                    if line.startswith("Ran ")
                ][0]
                test_count = int(test_count_line.split()[1])
                total_tests += test_count
            elif "Ran " in result.stdout:
                test_count_line = [
                    line
                    for line in result.stdout.split("\n")
                    if line.startswith("Ran ")
                ][0]
                test_count = int(test_count_line.split()[1])
                total_tests += test_count

            if result.returncode == 0:
                if (
                    "skipping P0 tests" in result.stdout
                    or "not available" in result.stdout
                ):
                    results["skipped"].append(test_file.name)
                    print(f"⚠️  SKIPPED: {test_file.name}")
                else:
                    results["passed"].append(test_file.name)
                    print(f"✅ PASSED: {test_file.name}")
            else:
                results["failed"].append(test_file.name)
                print(f"❌ FAILED: {test_file.name}")
                if result.stderr:
                    print(
                        f"   Error: {result.stderr.split('FAILED')[0].strip()[-100:]}"
                    )

        except subprocess.TimeoutExpired:
            results["error"].append(test_file.name)
            print(f"⏰ TIMEOUT: {test_file.name}")
        except Exception as e:
            results["error"].append(test_file.name)
            print(f"💥 ERROR: {test_file.name} - {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 P0 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"✅ PASSED:  {len(results['passed'])} files")
    print(f"❌ FAILED:  {len(results['failed'])} files")
    print(f"⚠️  SKIPPED: {len(results['skipped'])} files")
    print(f"💥 ERROR:   {len(results['error'])} files")
    print(f"🧪 TOTAL TESTS: {total_tests}")

    if results["failed"]:
        print(f"\n❌ FAILED FILES:")
        for f in results["failed"]:
            print(f"  - {f}")

    if results["error"]:
        print(f"\n💥 ERROR FILES:")
        for f in results["error"]:
            print(f"  - {f}")

    success_rate = (
        len(results["passed"])
        / (len(results["passed"]) + len(results["failed"]) + len(results["error"]))
        * 100
        if (len(results["passed"]) + len(results["failed"]) + len(results["error"])) > 0
        else 0
    )
    print(
        f"\n🎯 SUCCESS RATE: {success_rate:.1f}% ({len(results['passed'])}/{len(results['passed']) + len(results['failed']) + len(results['error'])} files)"
    )


if __name__ == "__main__":
    run_all_p0_tests()
