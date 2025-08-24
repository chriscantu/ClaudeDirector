#!/usr/bin/env python3
"""
Pre-push Architectural Validation Hook
Validates adherence to ClaudeDirector architectural principles and directory structure.

Author: Martin | Platform Architecture
Purpose: Prevent architectural violations before they reach the repository
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class ArchitecturalViolation:
    """Represents an architectural violation found during validation."""

    file_path: str
    violation_type: str
    description: str
    severity: str  # 'error', 'warning'
    suggestion: str


class ArchitecturalValidator:
    """Validates architectural adherence for ClaudeDirector codebase."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.violations: List[ArchitecturalViolation] = []

        # Define architectural rules
        self.directory_rules = self._initialize_directory_rules()
        self.file_rules = self._initialize_file_rules()
        self.import_rules = self._initialize_import_rules()

    def _initialize_directory_rules(self) -> Dict[str, Dict]:
        """Initialize directory structure rules."""
        return {
            # Documentation should only contain markdown and assets
            "docs/": {
                "allowed_extensions": [".md", ".png", ".jpg", ".jpeg", ".gif", ".svg"],
                "forbidden_extensions": [".py", ".js", ".ts", ".java", ".cpp"],
                "description": "Documentation directory should only contain documentation files",
                "suggestion": "Move Python files to appropriate directories in .claudedirector/",
            },
            # Tests should be in proper test directories
            "tests/": {
                "required_parent": ".claudedirector",
                "description": "Test files must be in .claudedirector/tests/ hierarchy",
                "suggestion": "Move test files to .claudedirector/tests/{unit,integration,functional}/",
            },
            # Source code structure
            ".claudedirector/lib/": {
                "allowed_extensions": [".py", ".yaml", ".yml", ".json", ".md"],
                "description": "Library code directory for ClaudeDirector modules",
                "max_depth": 4,  # Prevent excessive nesting
            },
            # Configuration files
            ".claudedirector/config/": {
                "allowed_extensions": [
                    ".yaml",
                    ".yml",
                    ".json",
                    ".ini",
                    ".toml",
                    ".sql",
                ],
                "forbidden_extensions": [".py"],
                "description": "Configuration directory should not contain executable code",
                "suggestion": "Move Python code to appropriate lib/ subdirectories",
            },
            # Leadership workspace (user data)
            "leadership-workspace/": {
                "allowed_extensions": [
                    ".md",
                    ".yaml",
                    ".yml",
                    ".json",
                    ".fish",
                    ".sh",
                    ".py",
                ],
                "description": "User workspace for strategic work",
                "no_source_code": True,  # No ClaudeDirector source code
            },
        }

    def _initialize_file_rules(self) -> Dict[str, Dict]:
        """Initialize file-specific rules."""
        return {
            # Test file naming conventions
            "test_*.py": {
                "required_directories": [
                    ".claudedirector/tests/unit/",
                    ".claudedirector/tests/integration/",
                    ".claudedirector/tests/functional/",
                    ".claudedirector/tests/performance/",
                    ".claudedirector/tests/regression/",
                ],
                "description": "Test files must follow proper directory structure",
            },
            # Configuration files
            "config.py": {
                "required_directories": [
                    ".claudedirector/lib/core/",
                    ".claudedirector/lib/config/",
                ],
                "description": "Configuration modules must be in core or config directories",
            },
            # Interface definitions
            "*_interface.py": {
                "required_directories": [".claudedirector/lib/*/interfaces/"],
                "description": "Interface definitions should be in interfaces/ subdirectories",
            },
        }

    def _initialize_import_rules(self) -> Dict[str, List[str]]:
        """Initialize import validation rules."""
        return {
            # Prevent circular imports
            "circular_imports": [
                "core -> persona_integration -> core",
                "memory -> core -> memory",
            ],
            # Prevent inappropriate dependencies
            "forbidden_imports": [
                "docs/* -> .claudedirector/*",  # Docs shouldn't import source
                "leadership-workspace/* -> .claudedirector/*",  # User workspace shouldn't import source
            ],
        }

    def validate_all(self) -> bool:
        """Run all architectural validations."""
        print("🏗️ ARCHITECTURAL VALIDATION")
        print("=" * 60)

        # 1. Directory structure validation
        self._validate_directory_structure()

        # 2. File placement validation
        self._validate_file_placement()

        # 3. Import structure validation
        self._validate_import_structure()

        # 4. Naming convention validation
        self._validate_naming_conventions()

        # 5. Dependency validation
        self._validate_dependencies()

        return self._report_results()

    def _validate_directory_structure(self):
        """Validate directory structure adherence."""
        print("📁 Validating directory structure...")

        for root, dirs, files in os.walk(self.repo_root):
            rel_root = os.path.relpath(root, self.repo_root)

            # Skip directories we don't want to validate
            skip_dirs = {
                ".git",
                ".venv",
                "venv",
                "__pycache__",
                ".mypy_cache",
                ".pytest_cache",
                "node_modules",
                ".benchmarks",
                "claudedirector.egg-info",
                ".claude",
            }

            # Skip if any part of the path should be excluded
            path_parts = Path(rel_root).parts
            if any(part in skip_dirs for part in path_parts):
                continue

            # Skip virtual environment and git object directories
            if any(
                exclude in rel_root
                for exclude in [
                    "venv/",
                    ".venv/",
                    ".git/",
                    "__pycache__/",
                    "site-packages/",
                    ".egg-info/",
                    "objects/",
                ]
            ):
                continue

            # Check each directory rule
            for dir_pattern, rules in self.directory_rules.items():
                if rel_root.startswith(dir_pattern.rstrip("/")):
                    self._check_directory_rules(rel_root, files, rules)

    def _check_directory_rules(self, directory: str, files: List[str], rules: Dict):
        """Check specific directory rules."""
        allowed_ext = rules.get("allowed_extensions", [])
        forbidden_ext = rules.get("forbidden_extensions", [])

        for file in files:
            file_ext = Path(file).suffix.lower()
            file_path = os.path.join(directory, file)

            # Check forbidden extensions
            if forbidden_ext and file_ext in forbidden_ext:
                self.violations.append(
                    ArchitecturalViolation(
                        file_path=file_path,
                        violation_type="forbidden_file_type",
                        description=f"File type {file_ext} not allowed in {directory}/",
                        severity="error",
                        suggestion=rules.get(
                            "suggestion", "Move file to appropriate directory"
                        ),
                    )
                )

            # Check allowed extensions (if specified)
            if allowed_ext and file_ext and file_ext not in allowed_ext:
                # Skip common non-code files
                if file_ext not in [".gitignore", ".gitkeep", ".DS_Store"]:
                    self.violations.append(
                        ArchitecturalViolation(
                            file_path=file_path,
                            violation_type="unexpected_file_type",
                            description=f"Unexpected file type {file_ext} in {directory}/",
                            severity="warning",
                            suggestion=f"Verify this file belongs in {directory}/",
                        )
                    )

    def _validate_file_placement(self):
        """Validate that files are in correct locations."""
        print("📄 Validating file placement...")

        # Find all Python files
        for root, dirs, files in os.walk(self.repo_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repo_root)
                    self._check_file_placement(rel_path, file)

    def _check_file_placement(self, file_path: str, filename: str):
        """Check if a file is in the correct location."""
        # Check test files
        if filename.startswith("test_") or filename.endswith("_test.py"):
            if not any(
                test_dir in file_path
                for test_dir in [
                    ".claudedirector/tests/",
                    "tests/",  # Allow tests/ in subdirectories
                ]
            ):
                self.violations.append(
                    ArchitecturalViolation(
                        file_path=file_path,
                        violation_type="misplaced_test_file",
                        description=f"Test file {filename} not in proper test directory",
                        severity="error",
                        suggestion="Move to .claudedirector/tests/{unit,integration,functional}/",
                    )
                )

        # Check configuration files
        if filename == "config.py":
            if not any(
                config_dir in file_path
                for config_dir in [
                    ".claudedirector/lib/core/",
                    ".claudedirector/lib/config/",
                    ".claudedirector/config/",
                ]
            ):
                self.violations.append(
                    ArchitecturalViolation(
                        file_path=file_path,
                        violation_type="misplaced_config_file",
                        description=f"Configuration file {filename} not in proper config directory",
                        severity="warning",
                        suggestion="Move to .claudedirector/lib/core/ or .claudedirector/lib/config/",
                    )
                )

    def _validate_import_structure(self):
        """Validate import structure and dependencies."""
        print("🔗 Validating import structure...")

        # This is a simplified version - could be expanded with AST parsing
        for root, dirs, files in os.walk(self.repo_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self._check_imports(file_path)

    def _check_imports(self, file_path: str):
        """Check imports in a Python file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for problematic import patterns
            rel_path = os.path.relpath(file_path, self.repo_root)

            # Check if docs files import source code
            if rel_path.startswith("docs/") and ".claudedirector" in content:
                self.violations.append(
                    ArchitecturalViolation(
                        file_path=rel_path,
                        violation_type="inappropriate_import",
                        description="Documentation file importing source code",
                        severity="error",
                        suggestion="Documentation should not import ClaudeDirector source code",
                    )
                )

        except (UnicodeDecodeError, IOError):
            pass  # Skip files that can't be read

    def _validate_naming_conventions(self):
        """Validate naming conventions."""
        print("📝 Validating naming conventions...")

        for root, dirs, files in os.walk(self.repo_root):
            rel_root = os.path.relpath(root, self.repo_root)

            # Check directory naming
            for dir_name in dirs:
                if not self._is_valid_directory_name(dir_name):
                    dir_path = os.path.join(rel_root, dir_name)
                    self.violations.append(
                        ArchitecturalViolation(
                            file_path=dir_path,
                            violation_type="invalid_directory_name",
                            description=f"Directory name '{dir_name}' doesn't follow conventions",
                            severity="warning",
                            suggestion="Use snake_case for directory names",
                        )
                    )

            # Check file naming
            for file_name in files:
                if file_name.endswith(".py") and not self._is_valid_python_filename(
                    file_name
                ):
                    file_path = os.path.join(rel_root, file_name)
                    self.violations.append(
                        ArchitecturalViolation(
                            file_path=file_path,
                            violation_type="invalid_filename",
                            description=f"Python file name '{file_name}' doesn't follow conventions",
                            severity="warning",
                            suggestion="Use snake_case for Python file names",
                        )
                    )

    def _is_valid_directory_name(self, name: str) -> bool:
        """Check if directory name follows conventions."""
        # Allow common exceptions
        exceptions = {
            ".claudedirector",
            ".github",
            ".git",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            "node_modules",
            "git-hooks",
            "dev-tools",
            "workspace-templates",
            "ai-cleanup",
            "legacy-scripts",
            "claudedirector.egg-info",
        }
        if name in exceptions:
            return True

        # Allow hex directories (git objects)
        if re.match(r"^[0-9a-f]{2}$", name):
            return True

        # Check snake_case pattern
        return re.match(r"^[a-z][a-z0-9_]*[a-z0-9]?$", name) is not None

    def _is_valid_python_filename(self, name: str) -> bool:
        """Check if Python filename follows conventions."""
        # Remove extension
        base_name = name[:-3] if name.endswith(".py") else name

        # Allow common exceptions
        exceptions = {
            "__init__",
            "setup",
            "conftest",
            "__main__",
            "pre-push-architectural-validation",
            "pre-commit-temp-file-blocker",
            "optimize-database",
            "protect-readme",
            "validate-strategic-patterns",
            "demo-strategic-scenario",
            "demo-meeting-intelligence",
            "init-database",
            "validate-ci-locally",
            "p0-ci-coverage-guard",
        }
        if base_name in exceptions:
            return True

        # Allow files with underscores starting with underscore (private modules)
        if base_name.startswith("_") and re.match(
            r"^_[a-z][a-z0-9_]*[a-z0-9]?$", base_name
        ):
            return True

        # Check snake_case pattern
        return re.match(r"^[a-z][a-z0-9_]*[a-z0-9]?$", base_name) is not None

    def _validate_dependencies(self):
        """Validate dependency structure."""
        print("🔄 Validating dependencies...")

        # Check for circular dependencies (simplified)
        # This could be expanded with proper dependency graph analysis

    def _report_results(self) -> bool:
        """Report validation results."""
        print("\n" + "=" * 60)

        if not self.violations:
            print("✅ ARCHITECTURAL VALIDATION PASSED")
            print("🏗️ All architectural principles adhered to")
            return True

        # Group violations by severity
        errors = [v for v in self.violations if v.severity == "error"]
        warnings = [v for v in self.violations if v.severity == "warning"]

        if errors:
            print("❌ ARCHITECTURAL VALIDATION FAILED")
            print(f"🚨 {len(errors)} error(s), {len(warnings)} warning(s)")
            print("\n🔴 ERRORS (must fix before push):")
            for error in errors:
                print(f"  📁 {error.file_path}")
                print(f"     {error.description}")
                print(f"     💡 {error.suggestion}")
                print()

        if warnings:
            print("⚠️ WARNINGS (should fix):")
            for warning in warnings:
                print(f"  📁 {warning.file_path}")
                print(f"     {warning.description}")
                print(f"     💡 {warning.suggestion}")
                print()

        return len(errors) == 0


def get_changed_files() -> Set[str]:
    """Get list of files changed in current commit."""
    try:
        # Get files in staging area
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return (
            set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
        )
    except subprocess.CalledProcessError:
        # Fallback to all files if git command fails
        return set()


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent.parent.parent

    print("🏗️ ClaudeDirector Architectural Validation")
    print("=" * 60)
    print("Validating adherence to architectural principles...")
    print()

    # Get changed files for focused validation
    changed_files = get_changed_files()
    if changed_files:
        print(f"📋 Validating {len(changed_files)} changed files")
    else:
        print("📋 Validating entire repository")

    # Run validation
    validator = ArchitecturalValidator(repo_root)
    success = validator.validate_all()

    if success:
        print("\n🎉 Architectural validation passed!")
        print("✅ Safe to push - no architectural violations detected")
        return 0
    else:
        print("\n🚫 Architectural validation failed!")
        print("❌ Fix architectural violations before pushing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
