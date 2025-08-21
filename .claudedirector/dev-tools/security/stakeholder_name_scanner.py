#!/usr/bin/env python3
"""
Stakeholder Name Security Scanner
Prevents sensitive stakeholder names from being committed to git
"""

import re
import sys
import os
from typing import List, Tuple

# CRITICAL: Sensitive stakeholder names that must NEVER be committed
SENSITIVE_PATTERNS = [
    # Real stakeholder names (add patterns, not exact names for security)
    r"(?i)\b(executive_a|executive_b)\b",  # Placeholder patterns to prevent self-detection
    r"(?i)\b(target_exec|ally_exec|opposition_exec)\b",
    r"(?i)\b(platform_executive|product_executive)\b",
    # Pattern-based detection
    r"(?i)(real[_-]?stakeholder[_-]?name)",
    r"(?i)(actual[_-]?procore[_-]?stakeholder)",
]


def scan_file(file_path: str) -> List[Tuple[int, str, str]]:
    """
    Scan file for sensitive stakeholder information
    Returns list of (line_number, line_content, pattern_matched)
    """
    violations = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, line):
                        violations.append((line_num, line.strip(), pattern))
    except (UnicodeDecodeError, IOError):
        # Skip binary files or files that can't be read
        pass

    return violations


def scan_staged_files() -> bool:
    """
    Scan all staged files for sensitive information
    Returns True if clean, False if violations found
    """
    # Get staged files
    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True
        )
        staged_files = (
            result.stdout.strip().split("\n") if result.stdout.strip() else []
        )
    except subprocess.CalledProcessError:
        print("Error: Could not get staged files from git")
        return False

    total_violations = 0

    for file_path in staged_files:
        if not os.path.exists(file_path):
            continue

        # Skip certain file types
        if file_path.endswith((".db", ".sqlite", ".pyc", ".png", ".jpg", ".jpeg")):
            continue

        violations = scan_file(file_path)

        if violations:
            total_violations += len(violations)
            print(f"\n🚨 SENSITIVE DATA DETECTED: {file_path}")
            for line_num, line_content, pattern in violations:
                print(f"   Line {line_num}: {line_content[:100]}...")
                print(f"   Pattern: {pattern}")

    if total_violations > 0:
        print(f"\n🚨 TOTAL VIOLATIONS: {total_violations}")
        print("\n🛡️ MANDATORY SECURITY POLICY:")
        print("❌ Stakeholder names MUST NOT be committed to git")
        print("❌ Use generic placeholders (Director A, VP Engineering, etc.)")
        print("❌ Remove sensitive data before committing")
        print("\n✅ Fix violations and retry commit")
        return False

    return True


def main():
    """Main security scanner entry point"""
    print("🛡️ Scanning for sensitive stakeholder information...")

    if len(sys.argv) > 1 and sys.argv[1] == "--staged":
        # Scan staged files (for pre-commit hook)
        if not scan_staged_files():
            sys.exit(1)
        else:
            print("✅ No sensitive stakeholder data detected")
            sys.exit(0)
    else:
        # Scan specific file
        if len(sys.argv) < 2:
            print("Usage: python sensitive_data_scanner.py <file_path>")
            print("       python sensitive_data_scanner.py --staged")
            sys.exit(1)

        file_path = sys.argv[1]
        violations = scan_file(file_path)

        if violations:
            print(f"🚨 VIOLATIONS in {file_path}:")
            for line_num, line_content, pattern in violations:
                print(f"   Line {line_num}: {line_content}")
            sys.exit(1)
        else:
            print(f"✅ Clean: {file_path}")
            sys.exit(0)


if __name__ == "__main__":
    main()
