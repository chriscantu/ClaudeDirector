#!/usr/bin/env python3
"""
Temporary File Blocker - Pre-commit Hook
Prevents temporary working files from being committed to source control
"""

import sys
import subprocess
import re
from pathlib import Path


# Patterns for temporary files that should NEVER be committed
TEMP_FILE_PATTERNS = [
    # Development artifacts
    r".*_AUDIT_REPORT\.md$",
    r".*_TEST_RESULTS\.md$",
    r".*_COMPLETION_SUMMARY\.md$",
    r"temp_.*\.md$",
    r"draft_.*\.md$",
    r"working_.*\.md$",
    r"notes_.*\.md$",
    # Process documentation
    r"CLEANUP_.*\.md$",
    r"BACKWARDS_COMPATIBILITY_.*\.md$",
    r"MANUAL_TESTING_.*\.md$",
    r"OPTION_.*_.*\.md$",
    # Release preparation artifacts
    r"RELEASE_NOTES_.*\.md$",
    r"temp_release_.*\.md$",
    r"draft_release_.*\.md$",
    # Development session files
    r"session_.*\.md$",
    r"debug_.*\.md$",
    r"scratch_.*\.md$",
    # Common temp patterns
    r".*\.tmp$",
    r".*\.temp$",
    r".*~$",
    r".*\.bak$",
]

# Critical files that must ALWAYS be present
CRITICAL_FILES = [
    "README.md",
]


def get_staged_files():
    """Get list of staged files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def check_temp_files(staged_files):
    """Check for temporary files in staged changes"""
    violations = []

    for file_path in staged_files:
        if not file_path:  # Skip empty strings
            continue

        for pattern in TEMP_FILE_PATTERNS:
            if re.match(pattern, Path(file_path).name):
                violations.append(
                    {
                        "file": file_path,
                        "pattern": pattern,
                        "type": "TEMP_FILE_VIOLATION",
                    }
                )
                break

    return violations


def check_critical_files():
    """Check that critical files exist and are not being deleted"""
    violations = []

    for critical_file in CRITICAL_FILES:
        if not Path(critical_file).exists():
            violations.append({"file": critical_file, "type": "CRITICAL_FILE_MISSING"})

    return violations


def check_deletions():
    """Check for deletions of critical files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True,
            text=True,
            check=True,
        )

        violations = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                status = parts[0]
                file_path = parts[1]

                if status == "D" and file_path in CRITICAL_FILES:
                    violations.append(
                        {"file": file_path, "type": "CRITICAL_FILE_DELETION"}
                    )

        return violations

    except subprocess.CalledProcessError:
        return []


def main():
    """Main pre-commit check"""
    print("🛡️ TEMPORARY FILE BLOCKER - Preventing temp files from commit")

    staged_files = get_staged_files()

    # Check for temporary file violations
    temp_violations = check_temp_files(staged_files)

    # Check for critical file issues
    critical_missing = check_critical_files()
    critical_deletions = check_deletions()

    all_violations = temp_violations + critical_missing + critical_deletions

    if all_violations:
        print("\n🚨 COMMIT BLOCKED - VIOLATIONS DETECTED:")
        print("=" * 60)

        for violation in all_violations:
            if violation["type"] == "TEMP_FILE_VIOLATION":
                print(f"❌ TEMP FILE: {violation['file']}")
                print(f"   Pattern: {violation['pattern']}")
                print("   → Use .gitignore or remove from staging")

            elif violation["type"] == "CRITICAL_FILE_MISSING":
                print(f"🚨 CRITICAL FILE MISSING: {violation['file']}")
                print("   → This file MUST exist for project discovery")

            elif violation["type"] == "CRITICAL_FILE_DELETION":
                print(f"🚨 CRITICAL FILE DELETION: {violation['file']}")
                print("   → This file MUST NOT be deleted")

        print("\n💡 SOLUTIONS:")
        print("🔧 For temp files: git reset HEAD <file> && git add to .gitignore")
        print("🚨 For README.md: python3 .claudedirector/dev-tools/protect-readme.py")
        print("\n🛡️ NEW RULE: Keep temporary working files out of source control")
        print("=" * 60)

        return 1

    print("✅ No temporary file violations detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
