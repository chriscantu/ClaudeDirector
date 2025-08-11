#!/usr/bin/env python3
"""
P1 Unit Test Runner
Pre-commit hook to run P1 unit tests with graceful fallback
"""

import subprocess
import sys

def main():
    """Run P1 unit tests"""
    # First check if pytest is available
    try:
        check_result = subprocess.run([
            sys.executable, '-c', 'import pytest'
        ], capture_output=True, text=True)

        if check_result.returncode != 0:
            print('⚠️  pytest not available - skipping unit tests')
            print('💡 Install test dependencies: pip install -r requirements-test.txt')
            sys.exit(0)
    except Exception:
        print('⚠️  pytest not available - skipping unit tests')
        sys.exit(0)

    # Run tests if pytest is available
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/p1_features/unit/',
            '-x', '--tb=short'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print('❌ P1 unit tests failed')
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            sys.exit(1)

        print('✅ P1 unit tests passed')

    except Exception as e:
        print(f'❌ Unit test execution failed: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
