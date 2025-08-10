#!/usr/bin/env python3
"""
P1 Test Coverage Checker
Pre-commit hook to ensure P1 features maintain test coverage threshold
"""

import subprocess
import sys

def main():
    """Check P1 test coverage"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/p1_features/unit/',
            '--cov=lib/claudedirector/p1_features',
            '--cov-fail-under=80',
            '--quiet'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print('❌ P1 test coverage below 80%')
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            sys.exit(1)

        print('✅ P1 test coverage meets threshold')

    except FileNotFoundError:
        print('⚠️  pytest not available - skipping coverage check')
        # Don't fail if pytest is not installed
        sys.exit(0)
    except Exception as e:
        print(f'❌ Coverage check failed: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
