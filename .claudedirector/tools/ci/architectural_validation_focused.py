#!/usr/bin/env python3
"""
Focused Architectural Validation for ClaudeDirector
Validates only our source code structure, ignoring virtual environments and dependencies.

Author: Martin | Platform Architecture
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


def validate_docs_directory() -> List[Tuple[str, str]]:
    """Validate that docs/ contains only documentation files."""
    violations = []
    docs_path = Path("docs")

    if not docs_path.exists():
        return violations

    forbidden_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h"}

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in forbidden_extensions:
                violations.append(
                    (
                        str(file_path),
                        f"Code file {file_path.suffix} found in documentation directory",
                    )
                )

    return violations


def validate_test_file_placement() -> List[Tuple[str, str]]:
    """Validate that test files are in proper test directories."""
    violations = []

    # Find all Python test files
    for root, dirs, files in os.walk("."):
        # Skip virtual environments and git
        if any(skip in root for skip in ["venv/", ".venv/", ".git/", "site-packages/"]):
            continue

        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)

                # Check if it's in a proper test directory
                if not any(
                    test_dir in file_path
                    for test_dir in [
                        ".claudedirector/tests/",
                        "/tests/",  # Allow tests in subdirectories
                    ]
                ):
                    violations.append(
                        (
                            file_path,
                            f"Test file {file} not in proper test directory (.claudedirector/tests/)",
                        )
                    )

    return violations


def validate_config_file_placement() -> List[Tuple[str, str]]:
    """Validate that config files are in appropriate directories."""
    violations = []

    for root, dirs, files in os.walk(".claudedirector"):
        for file in files:
            if file == "config.py":
                file_path = os.path.join(root, file)

                # Config files should be in core/, config/, or infrastructure/ directories
                if not any(
                    config_dir in file_path
                    for config_dir in ["/core/", "/config/", "/infrastructure/"]
                ):
                    violations.append(
                        (
                            file_path,
                            f"Configuration file should be in core/ or config/ directory",
                        )
                    )

    return violations


def check_for_python_in_docs() -> List[Tuple[str, str]]:
    """Check for any Python imports of ClaudeDirector source in docs."""
    violations = []
    docs_path = Path("docs")

    if not docs_path.exists():
        return violations

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if ".claudedirector" in content or "from lib." in content:
                            violations.append(
                                (
                                    str(file_path),
                                    "Documentation file importing ClaudeDirector source code",
                                )
                            )
                except (UnicodeDecodeError, IOError):
                    pass

    return violations


def main():
    """Run focused architectural validation."""
    print("🏗️ ClaudeDirector Architectural Validation (Focused)")
    print("=" * 60)

    all_violations = []

    # Run focused validations
    print("📁 Validating docs/ directory structure...")
    all_violations.extend(validate_docs_directory())

    print("🧪 Validating test file placement...")
    all_violations.extend(validate_test_file_placement())

    print("⚙️ Validating config file placement...")
    all_violations.extend(validate_config_file_placement())

    print("🔗 Checking for inappropriate imports...")
    all_violations.extend(check_for_python_in_docs())

    # Report results
    print("\n" + "=" * 60)

    if not all_violations:
        print("✅ ARCHITECTURAL VALIDATION PASSED")
        print("🏗️ All architectural principles adhered to")
        return 0

    print("❌ ARCHITECTURAL VALIDATION FAILED")
    print(f"🚨 {len(all_violations)} violation(s) found:")
    print()

    for file_path, description in all_violations:
        print(f"  📁 {file_path}")
        print(f"     {description}")
        print()

    print("💡 Fix these architectural violations before pushing")
    return 1


if __name__ == "__main__":
    sys.exit(main())
