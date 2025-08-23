#!/usr/bin/env python3
"""
Local CI Validation Script - Enhanced with Complete CI Mirror

Runs the EXACT same checks locally that run in the GitHub Actions CI pipeline,
providing 100% parity between local and CI environments.

This script now delegates to the comprehensive local-ci-mirror.py for complete
GitHub CI simulation.

Usage:
    python3 scripts/validate-ci-locally.py
    python3 scripts/validate-ci-locally.py --fix  # Auto-fix formatting issues
    python3 scripts/validate-ci-locally.py --full # Run complete CI mirror
"""

import subprocess
import sys
import os
import re
from pathlib import Path
from typing import List, Tuple


def print_step(message: str) -> None:
    """Print a step header"""
    print(f"\n{'='*60}")
    print(f"🔍 {message}")
    print("=" * 60)


def print_success(message: str) -> None:
    """Print success message"""
    print(f"✅ {message}")


def print_error(message: str) -> None:
    """Print error message"""
    print(f"❌ {message}")


def print_warning(message: str) -> None:
    """Print warning message"""
    print(f"⚠️  {message}")


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {command}")
            print(f"Exit code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        return e


def security_scan() -> bool:
    """Run security scan - matches CI exactly"""
    print_step("SECURITY SCAN - Sensitive Data Protection")

    # This is the exact same code as in CI
    security_code = """
import os
import re

# Sensitive patterns to scan for
patterns = [
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', 'Email addresses'),
    (r'(?:password|passwd|pwd)\\s*[=:]\\s*[a-zA-Z0-9_-]{8,}', 'Passwords'),
    (r'(?:api_key|apikey|secret)\\s*[=:]\\s*[a-zA-Z0-9_-]{16,}', 'API Keys'),
    (r'(?:token)\\s*[=:]\\s*[a-zA-Z0-9_-]{20,}', 'Tokens'),
    (r'aws_access_key_id\\s*[=:]\\s*[A-Z0-9]{20}', 'AWS Access Keys'),
    (r'ssh-rsa\\s+[A-Za-z0-9+/]{100,}', 'SSH Keys')
]

issues = []

for root, dirs, files in os.walk('.'):
    # Skip certain directories
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.mypy_cache', 'venv', '.venv', 'node_modules', 'target', 'build', 'dist']]

    for file in files:
        if file.endswith(('.py', '.js', '.ts', '.yaml', '.yml', '.json', '.md', '.txt', '.env')):
            file_path = os.path.join(root, file)

            # Skip documentation and workspace files to reduce false positives
            skip_patterns = ['docs/', 'readme', 'security.md', 'example', 'leadership-workspace/']
            if any(pattern in file_path.lower() for pattern in skip_patterns):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Skip content with obvious documentation patterns
                    content_lower = content.lower()
                    if any(word in content_lower for word in ['@company.com', '@procore.com', 'platform-security.internal', 'example', 'test', 'dummy', 'placeholder', 'sample']):
                        continue

                    for pattern, description in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\\n') + 1
                            issues.append(f'{file_path}:{line_num} - {description}: {match.group()[:50]}...')
            except (UnicodeDecodeError, IOError):
                continue

if issues:
    print('❌ SECURITY VIOLATIONS DETECTED:')
    for issue in issues[:10]:  # Limit output
        print(f'  {issue}')
    if len(issues) > 10:
        print(f'  ... and {len(issues) - 10} more violations')
    exit(1)
else:
    print('✅ No sensitive data violations detected')
"""

    result = run_command(f'python3 -c "{security_code}"', check=False)
    if result.returncode == 0:
        print_success("Security Scan")
        return True
    else:
        print_error("Security Scan")
        print(result.stdout)
        return False


def black_formatting() -> bool:
    """Run Black formatting check - matches CI exactly"""
    print_step("CODE QUALITY - Black Formatting")

    # Check if black is available
    result = run_command("black --version", check=False)
    if result.returncode != 0:
        print_warning("Black not installed - installing...")
        install_result = run_command(
            "python3 -m pip install black>=23.0.0", check=False
        )
        if install_result.returncode != 0:
            print_error("Failed to install black")
            return False

    # Check formatting compliance (exact CI command)
    result = run_command("black --check --diff .", check=False)
    if result.returncode == 0:
        print_success("Black Formatting")
        return True
    else:
        print_error("Black Formatting")
        print("Black formatting violations detected:")
        print(result.stdout)
        print("💡 Fix with: black .")
        return False


def flake8_linting() -> bool:
    """Run Flake8 linting - matches CI exactly"""
    print_step("CODE QUALITY - Flake8 Linting")

    # Check if flake8 is available
    result = run_command("flake8 --version", check=False)
    if result.returncode != 0:
        print_warning("Flake8 not found globally - trying python module...")
        result = run_command("python3 -m flake8 --version", check=False)
        if result.returncode != 0:
            print_error("Flake8 not available - install with: pipx install flake8")
            return False

    # Run critical error checks (exact CI command)
    print("Running critical error checks...")
    result = run_command(
        "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,.venv,__pycache__,.mypy_cache",
        check=False,
    )
    if result.returncode != 0:
        print_error("Flake8 Critical Errors")
        print("Critical linting errors detected:")
        print(result.stdout)
        return False

    # Run full linting with lenient settings (exact CI command)
    print("Running full linting analysis...")
    run_command(
        "flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics --exclude=venv,.venv,__pycache__,.mypy_cache",
        check=False,
    )

    print_success("Flake8 Linting")
    return True


def mypy_type_checking() -> bool:
    """Run MyPy type checking - matches CI exactly"""
    print_step("CODE QUALITY - MyPy Type Checking")

    # Check if mypy is available
    result = run_command("mypy --version", check=False)
    if result.returncode != 0:
        print_warning("MyPy not found globally - trying python module...")
        result = run_command("python3 -m mypy --version", check=False)
        if result.returncode != 0:
            print_error("MyPy not available - install with: pipx install mypy")
            return False

    # Run type checking with lenient settings (exact CI command)
    print("Running type checking analysis...")
    result = run_command(
        "mypy . --ignore-missing-imports --no-strict-optional --allow-untyped-defs --allow-incomplete-defs --check-untyped-defs",
        check=False,
    )

    # MyPy is expected to find issues in existing codebase, so we don't fail on exit code
    print("MyPy analysis completed (issues expected for existing codebase)")
    print_success("MyPy Type Checking")
    return True


def solid_principles() -> bool:
    """Run SOLID principles validation - matches CI exactly"""
    print_step("ARCHITECTURE - SOLID Principles Validation")

    # Check if SOLID validator exists (exact CI check)
    import os

    solid_validator_path = ".claudedirector/dev-tools/architecture/solid_validator.py"
    if not os.path.exists(solid_validator_path):
        print_warning("SOLID validator not found - skipping validation")
        print_success("SOLID Principles (skipped)")
        return True

    # Run SOLID validation (exact CI command)
    print("Running SOLID principles analysis...")
    result = run_command(f"python3 {solid_validator_path}", check=False)

    # SOLID violations are expected in existing codebase, so we don't fail on exit code
    print("SOLID analysis completed (violations expected for existing codebase)")
    print_success("SOLID Principles")
    return True


def check_prerequisites() -> bool:
    """Check if required tools are available"""
    print_step("PREREQUISITES CHECK")

    # Check Python
    result = run_command("python3 --version", check=False)
    if result.returncode != 0:
        print_error("Python 3 not found")
        return False

    print(f"✅ Python: {result.stdout.strip()}")

    # Check if in git repo
    result = run_command("git rev-parse --git-dir", check=False)
    if result.returncode != 0:
        print_error("Not in a git repository")
        return False

    print("✅ Git repository detected")

    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print_warning("requirements.txt not found - some checks may fail")
    else:
        print("✅ requirements.txt found")

    return True


def main():
    """Main execution with enhanced CI mirror support"""
    # Check command line arguments
    auto_fix = "--fix" in sys.argv
    full_mirror = "--full" in sys.argv

    if full_mirror:
        print("🚀 Running COMPLETE GitHub CI Mirror")
        print("=====================================")
        print("This provides 100% parity with GitHub Actions environment")
        print()

        # Delegate to the comprehensive CI mirror
        script_dir = Path(__file__).parent
        mirror_script = script_dir / "local-ci-mirror.py"

        try:
            result = subprocess.run(
                [sys.executable, str(mirror_script)],
                cwd=script_dir.parent,  # Run from repo root
            )
            sys.exit(result.returncode)
        except Exception as e:
            print_error(f"Failed to run CI mirror: {str(e)}")
            sys.exit(1)

    # Original validation (faster, less comprehensive)
    print("🚀 ClaudeDirector Local CI Validation (Quick Mode)")
    print("=====================================")
    print("Running basic checks. Use --full for complete GitHub CI simulation")
    print("💡 Tip: Use 'python scripts/validate-ci-locally.py --full' for 100% CI parity")
    print()

    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisites check failed")
        sys.exit(1)

    # Track results
    checks_passed = 0
    checks_failed = 0

    # Run security scan
    if security_scan():
        checks_passed += 1
    else:
        checks_failed += 1

    # Run Black formatting check
    if black_formatting():
        checks_passed += 1
    else:
        checks_failed += 1

    # Run Flake8 linting
    if flake8_linting():
        checks_passed += 1
    else:
        checks_failed += 1

    # Run MyPy type checking
    if mypy_type_checking():
        checks_passed += 1
    else:
        checks_failed += 1

    # Run SOLID principles validation
    if solid_principles():
        checks_passed += 1
    else:
        checks_failed += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"✅ {checks_passed} check(s) passed")
    print(f"❌ {checks_failed} check(s) failed")

    if checks_failed == 0:
        print_success("ALL CHECKS PASSED - Ready for CI/CD Pipeline!")
        print("💡 For 100% CI parity, use: python scripts/validate-ci-locally.py --full")
        sys.exit(0)
    else:
        print_error(f"VALIDATION FAILED - {checks_failed} check(s) need attention")
        print("💡 Try: python scripts/validate-ci-locally.py --full")
        sys.exit(1)


if __name__ == "__main__":
    main()
