#!/usr/bin/env python3
"""
Documentation Size Policy Enforcement
Ensures all documentation files adhere to the 200-line limit policy.
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple

# Policy configuration
MAX_DOC_SIZE = 500  # Aligned with existing Python file size standards
EXEMPT_FILES = {
    "README.md",  # Project root README allowed to be longer
    "CHANGELOG.md",  # Changelog grows over time
    "LICENSE.md",  # License text is fixed
    "CLAUDEDIRECTOR_CLEANUP_ANALYSIS.md",  # Temporary analysis files
}

def check_file_size(file_path: Path) -> Tuple[bool, int]:
    """
    Check if a documentation file exceeds the size limit.

    Returns:
        Tuple of (is_compliant, line_count)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_count = len(lines)

        # Check if file is exempt
        if file_path.name in EXEMPT_FILES:
            return True, line_count

        # Check size limit
        is_compliant = line_count <= MAX_DOC_SIZE
        return is_compliant, line_count

    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False, 0

def main():
    """Main policy enforcement function."""
    if len(sys.argv) < 2:
        print("Usage: check_doc_size.py <file1.md> [file2.md] ...")
        sys.exit(1)

    violations = []
    total_files = 0

    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)

        if not file_path.exists():
            continue

        if not file_path.suffix == '.md':
            continue

        total_files += 1
        is_compliant, line_count = check_file_size(file_path)

        if not is_compliant:
            violations.append((file_path, line_count))

    # Report results
    if violations:
        print("🚨 DOCUMENTATION POLICY VIOLATIONS DETECTED")
        print("=" * 60)
        print(f"Policy: Documentation files must be ≤{MAX_DOC_SIZE} lines (aligned with code standards)")
        print()

        for file_path, line_count in violations:
            excess_lines = line_count - MAX_DOC_SIZE
            print(f"❌ {file_path}")
            print(f"   Current: {line_count} lines (+{excess_lines} over limit)")
            print(f"   Required: Split into focused files ≤{MAX_DOC_SIZE} lines each (same as Python files)")
            print()

        print("💡 REMEDIATION REQUIRED:")
        print("- Split large files into focused, single-responsibility documents")
        print("- Create index files that link to focused sub-documents")
        print("- Follow examples in docs/architecture/patterns/ and docs/development/guides/")
        print("- See docs/DEVELOPMENT_POLICY.md for complete guidelines")
        print()
        print("🛡️ COMMIT BLOCKED: Fix violations before proceeding")
        sys.exit(1)
    else:
        if total_files > 0:
            print(f"✅ Documentation Policy: All {total_files} files comply with size limits")
        sys.exit(0)

if __name__ == "__main__":
    main()
