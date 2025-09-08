#!/usr/bin/env python3
"""
Systematic Commit Checker - Prevents Uncommitted Changes Issue

This tool addresses the recurring issue of incomplete commits by providing:
1. Systematic validation of all changes before commits
2. Detection of formatter-induced changes (black, pre-commit hooks)
3. Prevention of accidental file deletions (like README.md)
4. Complete changeset validation for PR integrity

Author: Martin | Platform Architecture
Created: January 2025
Purpose: Systematic resolution of uncommitted changes workflow issue
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json
import logging
from dataclasses import dataclass
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class GitStatus:
    """Git status information"""

    staged_files: List[str]
    unstaged_files: List[str]
    untracked_files: List[str]
    deleted_files: List[str]
    modified_files: List[str]
    has_changes: bool


@dataclass
class CommitValidation:
    """Commit validation result"""

    is_valid: bool
    issues: List[str]
    warnings: List[str]
    suggestions: List[str]
    critical_files_missing: List[str]


class SystematicCommitChecker:
    """
    Systematic commit checker that prevents incomplete commits

    Follows SOLID principles:
    - Single Responsibility: Validates git commit completeness
    - Open/Closed: Extensible validation rules
    - Liskov Substitution: Consistent validation interface
    - Interface Segregation: Focused validation methods
    - Dependency Inversion: Depends on git abstractions

    DRY Compliance:
    - Reuses git status parsing logic
    - Consolidates validation rules
    - Avoids duplicate file checking
    """

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize systematic commit checker"""
        self.project_root = project_root or Path.cwd()
        self.critical_files = {
            "README.md": "Project must always have README.md on main branch",
            ".gitignore": "Git ignore file is critical for repository hygiene",
            "pyproject.toml": "Python project configuration must be maintained",
        }

        # Files that commonly get modified by formatters/pre-commit hooks
        self.formatter_patterns = [
            "*.py",  # Black formatter
            "*.md",  # Markdown formatting
            "*.yaml",
            "*.yml",  # YAML formatting
            "*.json",  # JSON formatting
        ]

    def get_git_status(self) -> GitStatus:
        """Get comprehensive git status"""
        try:
            # Get staged files
            staged_result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            staged_files = (
                staged_result.stdout.strip().split("\n")
                if staged_result.stdout.strip()
                else []
            )

            # Get unstaged files
            unstaged_result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            unstaged_files = (
                unstaged_result.stdout.strip().split("\n")
                if unstaged_result.stdout.strip()
                else []
            )

            # Get untracked files
            untracked_result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True,
            )
            untracked_files = (
                untracked_result.stdout.strip().split("\n")
                if untracked_result.stdout.strip()
                else []
            )

            # Get status for deleted/modified analysis
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )

            deleted_files = []
            modified_files = []

            for line in status_result.stdout.strip().split("\n"):
                if line:
                    status_code = line[:2]
                    filename = line[3:]

                    if "D" in status_code:
                        deleted_files.append(filename)
                    if "M" in status_code:
                        modified_files.append(filename)

            has_changes = bool(staged_files or unstaged_files or untracked_files)

            return GitStatus(
                staged_files=staged_files,
                unstaged_files=unstaged_files,
                untracked_files=untracked_files,
                deleted_files=deleted_files,
                modified_files=modified_files,
                has_changes=has_changes,
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            return GitStatus([], [], [], [], [], False)

    def validate_commit_completeness(self, git_status: GitStatus) -> CommitValidation:
        """Validate that commit is complete and ready"""
        issues = []
        warnings = []
        suggestions = []
        critical_files_missing = []

        # Check for critical file deletions
        for deleted_file in git_status.deleted_files:
            if deleted_file in self.critical_files:
                issues.append(
                    f"CRITICAL: {deleted_file} has been deleted - {self.critical_files[deleted_file]}"
                )
                critical_files_missing.append(deleted_file)

        # Check for unstaged changes
        if git_status.unstaged_files:
            issues.append(
                f"Unstaged changes detected in {len(git_status.unstaged_files)} files"
            )
            suggestions.append("Run 'git add -A' to stage all changes")

            # Check if unstaged changes are likely from formatters
            formatter_changes = [
                f
                for f in git_status.unstaged_files
                if any(
                    f.endswith(pattern.replace("*", ""))
                    for pattern in self.formatter_patterns
                )
            ]

            if formatter_changes:
                warnings.append(
                    f"Formatter-modified files detected: {formatter_changes}"
                )
                suggestions.append(
                    "These are likely from black/pre-commit hooks - stage them"
                )

        # Check for untracked files that should be committed
        important_untracked = [
            f
            for f in git_status.untracked_files
            if not f.startswith(".") and not f.endswith(".pyc")
        ]

        if important_untracked:
            warnings.append(
                f"Untracked files that may need committing: {important_untracked}"
            )
            suggestions.append("Review untracked files and add important ones")

        # Validate staged changes exist
        if not git_status.staged_files and git_status.has_changes:
            issues.append("No staged changes but modifications detected")
            suggestions.append("Stage your changes with 'git add' before committing")

        is_valid = len(issues) == 0 and len(critical_files_missing) == 0

        return CommitValidation(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            suggestions=suggestions,
            critical_files_missing=critical_files_missing,
        )

    def auto_fix_common_issues(
        self, git_status: GitStatus, validation: CommitValidation
    ) -> bool:
        """Automatically fix common issues where safe to do so"""
        fixes_applied = []

        # Auto-restore critical files if they were deleted
        for critical_file in validation.critical_files_missing:
            try:
                subprocess.run(
                    ["git", "checkout", "HEAD", "--", critical_file],
                    check=True,
                    capture_output=True,
                )
                fixes_applied.append(f"Restored {critical_file}")
                logger.info(f"Auto-restored critical file: {critical_file}")
            except subprocess.CalledProcessError:
                logger.warning(f"Could not auto-restore {critical_file}")

        # Auto-stage formatter changes if they look safe
        formatter_changes = [
            f
            for f in git_status.unstaged_files
            if f.endswith(".py") or f.endswith(".md")
        ]

        if formatter_changes and len(formatter_changes) <= 10:  # Safety limit
            try:
                subprocess.run(
                    ["git", "add"] + formatter_changes, check=True, capture_output=True
                )
                fixes_applied.append(f"Staged formatter changes: {formatter_changes}")
                logger.info(f"Auto-staged formatter changes: {formatter_changes}")
            except subprocess.CalledProcessError:
                logger.warning("Could not auto-stage formatter changes")

        if fixes_applied:
            logger.info(f"Applied {len(fixes_applied)} automatic fixes")
            return True

        return False

    def generate_commit_report(
        self, git_status: GitStatus, validation: CommitValidation
    ) -> str:
        """Generate comprehensive commit status report"""
        report_lines = [
            "🔍 SYSTEMATIC COMMIT VALIDATION REPORT",
            "=" * 50,
            f"Timestamp: {datetime.now().isoformat()}",
            f"Project Root: {self.project_root}",
            "",
            "📊 GIT STATUS SUMMARY:",
            f"  Staged Files: {len(git_status.staged_files)}",
            f"  Unstaged Files: {len(git_status.unstaged_files)}",
            f"  Untracked Files: {len(git_status.untracked_files)}",
            f"  Deleted Files: {len(git_status.deleted_files)}",
            f"  Modified Files: {len(git_status.modified_files)}",
            "",
        ]

        if git_status.staged_files:
            report_lines.extend(
                ["✅ STAGED FILES:", *[f"  + {f}" for f in git_status.staged_files], ""]
            )

        if git_status.unstaged_files:
            report_lines.extend(
                [
                    "⚠️  UNSTAGED FILES:",
                    *[f"  ! {f}" for f in git_status.unstaged_files],
                    "",
                ]
            )

        if validation.issues:
            report_lines.extend(
                [
                    "🚨 CRITICAL ISSUES:",
                    *[f"  ❌ {issue}" for issue in validation.issues],
                    "",
                ]
            )

        if validation.warnings:
            report_lines.extend(
                [
                    "⚠️  WARNINGS:",
                    *[f"  ⚠️  {warning}" for warning in validation.warnings],
                    "",
                ]
            )

        if validation.suggestions:
            report_lines.extend(
                [
                    "💡 SUGGESTIONS:",
                    *[f"  💡 {suggestion}" for suggestion in validation.suggestions],
                    "",
                ]
            )

        validation_status = (
            "✅ READY TO COMMIT" if validation.is_valid else "❌ NOT READY TO COMMIT"
        )
        report_lines.extend(["🎯 VALIDATION RESULT:", f"  {validation_status}", ""])

        return "\n".join(report_lines)

    def run_systematic_check(
        self, auto_fix: bool = True, verbose: bool = True
    ) -> Tuple[bool, str]:
        """Run complete systematic commit check"""
        logger.info("Starting systematic commit validation...")

        # Get git status
        git_status = self.get_git_status()

        # Validate commit completeness
        validation = self.validate_commit_completeness(git_status)

        # Apply auto-fixes if enabled and needed
        if auto_fix and not validation.is_valid:
            fixes_applied = self.auto_fix_common_issues(git_status, validation)

            if fixes_applied:
                # Re-check after fixes
                git_status = self.get_git_status()
                validation = self.validate_commit_completeness(git_status)

        # Generate report
        report = self.generate_commit_report(git_status, validation)

        if verbose:
            print(report)

        return validation.is_valid, report


def main():
    """Main entry point for systematic commit checker"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Systematic Commit Checker - Prevents Incomplete Commits"
    )
    parser.add_argument(
        "--no-auto-fix",
        action="store_true",
        help="Disable automatic fixes for common issues",
    )
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    checker = SystematicCommitChecker()
    is_valid, report = checker.run_systematic_check(
        auto_fix=not args.no_auto_fix, verbose=not args.quiet
    )

    if args.json:
        result = {
            "is_valid": is_valid,
            "report": report,
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
