#!/usr/bin/env python3
"""
Sequential Thinking Validator - MANDATORY ENFORCEMENT TOOL

🚨 CRITICAL REQUIREMENT: Validates ALL commits for Sequential Thinking compliance
🎯 ZERO TOLERANCE POLICY: No commits allowed without Sequential Thinking methodology

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import os
import sys
import re
import subprocess
from typing import List, Dict, Tuple, Set
from pathlib import Path
import json
from datetime import datetime


class SequentialThinkingValidator:
    """
    🏗️ SEQUENTIAL THINKING VALIDATION ENGINE

    MANDATORY ENFORCEMENT:
    - Validates all staged files for Sequential Thinking compliance
    - Blocks commits that don't demonstrate Sequential Thinking methodology
    - Ensures 100% compliance with Sequential Thinking requirements

    VALIDATION CRITERIA:
    - Sequential Thinking documentation in file headers
    - Systematic approach documentation
    - Step-by-step methodology evidence
    - Problem-solution mapping clarity
    """

    def __init__(self):
        self.project_root = self._find_project_root()
        self.validation_results = {
            "compliant_files": [],
            "non_compliant_files": [],
            "validation_errors": [],
            "total_files_checked": 0,
            "compliance_rate": 0.0,
        }

        # Sequential Thinking compliance patterns
        self.required_patterns = [
            r"Sequential Thinking",
            r"🏗️.*Sequential Thinking",
            r"Sequential.*methodology",
            r"Systematic.*approach",
            r"Step-by-step",
        ]

        # File types that require Sequential Thinking documentation
        self.python_extensions = {".py"}
        self.doc_extensions = {".md", ".rst", ".txt"}
        self.required_extensions = self.python_extensions.union(self.doc_extensions)

    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claudedirector").exists():
                return current
            current = current.parent
        return Path.cwd()

    def get_staged_files(self) -> List[str]:
        """Get list of staged files for commit"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                self.validation_results["validation_errors"].append(
                    f"Failed to get staged files: {result.stderr}"
                )
                return []

            staged_files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
            return [f for f in staged_files if self._should_validate_file(f)]

        except Exception as e:
            self.validation_results["validation_errors"].append(
                f"Error getting staged files: {str(e)}"
            )
            return []

    def _should_validate_file(self, file_path: str) -> bool:
        """Check if file should be validated for Sequential Thinking"""
        path = Path(file_path)

        # Skip deleted files
        if not (self.project_root / file_path).exists():
            return False

        # Only validate specific file types
        if path.suffix not in self.required_extensions:
            return False

        # Skip test files (they inherit methodology from implementation)
        if "test_" in path.name or path.name.startswith("test"):
            return False

        # Skip configuration files
        if path.name in ["__init__.py", "setup.py", "conftest.py"]:
            return False

        return True

    def validate_file_content(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate a single file for Sequential Thinking compliance"""
        try:
            full_path = self.project_root / file_path
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            issues = []

            # Check for Sequential Thinking documentation
            has_sequential_thinking = any(
                re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                for pattern in self.required_patterns
            )

            if not has_sequential_thinking:
                issues.append("Missing Sequential Thinking methodology documentation")

            # For Python files, check for proper docstring structure
            if file_path.endswith(".py"):
                docstring_issues = self._validate_python_docstring(content)
                issues.extend(docstring_issues)

            # For documentation files, check for methodology sections
            if file_path.endswith(".md"):
                doc_issues = self._validate_documentation_structure(content)
                issues.extend(doc_issues)

            return len(issues) == 0, issues

        except Exception as e:
            return False, [f"Error reading file: {str(e)}"]

    def _validate_python_docstring(self, content: str) -> List[str]:
        """Validate Python file docstring for Sequential Thinking compliance"""
        issues = []

        # Check for module docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if not docstring_match:
            issues.append("Missing module docstring")
            return issues

        docstring = docstring_match.group(1)

        # Check for required Sequential Thinking elements
        required_elements = [
            (r"Sequential Thinking", "Sequential Thinking methodology reference"),
            (r"🏗️", "Sequential Thinking emoji indicator"),
            (
                r"Author:.*Sequential Thinking",
                "Author attribution with Sequential Thinking methodology",
            ),
        ]

        for pattern, description in required_elements:
            if not re.search(pattern, docstring, re.IGNORECASE | re.MULTILINE):
                issues.append(f"Missing {description} in docstring")

        return issues

    def _validate_documentation_structure(self, content: str) -> List[str]:
        """Validate documentation file for Sequential Thinking methodology"""
        issues = []

        # Check for Sequential Thinking methodology sections
        methodology_patterns = [
            r"Sequential Thinking",
            r"Systematic.*approach",
            r"Step-by-step",
            r"Methodology",
        ]

        has_methodology_section = any(
            re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            for pattern in methodology_patterns
        )

        if not has_methodology_section:
            issues.append("Missing Sequential Thinking methodology documentation")

        return issues

    def validate_commit_message(self) -> Tuple[bool, List[str]]:
        """Validate commit message for Sequential Thinking compliance"""
        try:
            # Get the commit message from git
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=%B"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                return False, ["Could not retrieve commit message"]

            commit_message = result.stdout.strip()
            issues = []

            # Check for Sequential Thinking indicators in commit message
            sequential_indicators = [
                r"Sequential Thinking",
                r"systematic.*approach",
                r"step-by-step",
                r"methodology",
                r"TS-\d+",  # Technical Story pattern
            ]

            has_sequential_indicator = any(
                re.search(indicator, commit_message, re.IGNORECASE)
                for indicator in sequential_indicators
            )

            if not has_sequential_indicator:
                issues.append(
                    "Commit message should reference Sequential Thinking methodology or systematic approach"
                )

            return len(issues) == 0, issues

        except Exception as e:
            return False, [f"Error validating commit message: {str(e)}"]

    def run_validation(self) -> bool:
        """Run complete Sequential Thinking validation"""
        print("🏗️ SEQUENTIAL THINKING VALIDATOR")
        print("=" * 60)
        print("🚨 MANDATORY: Validating Sequential Thinking compliance")
        print(
            "🎯 ZERO TOLERANCE: All files must demonstrate Sequential Thinking methodology"
        )
        print()

        # Get staged files
        staged_files = self.get_staged_files()
        self.validation_results["total_files_checked"] = len(staged_files)

        if not staged_files:
            print("✅ No files require Sequential Thinking validation")
            return True

        print(
            f"📋 Validating {len(staged_files)} files for Sequential Thinking compliance:"
        )
        print()

        all_compliant = True

        # Validate each file
        for file_path in staged_files:
            is_compliant, issues = self.validate_file_content(file_path)

            if is_compliant:
                self.validation_results["compliant_files"].append(file_path)
                print(f"✅ {file_path}")
            else:
                self.validation_results["non_compliant_files"].append(
                    {"file": file_path, "issues": issues}
                )
                print(f"❌ {file_path}")
                for issue in issues:
                    print(f"   - {issue}")
                all_compliant = False

        print()

        # Validate commit message
        commit_compliant, commit_issues = self.validate_commit_message()
        if not commit_compliant:
            print("❌ COMMIT MESSAGE VALIDATION FAILED:")
            for issue in commit_issues:
                print(f"   - {issue}")
            all_compliant = False
        else:
            print("✅ Commit message demonstrates Sequential Thinking methodology")

        # Calculate compliance rate
        if self.validation_results["total_files_checked"] > 0:
            self.validation_results["compliance_rate"] = (
                len(self.validation_results["compliant_files"])
                / self.validation_results["total_files_checked"]
                * 100
            )

        print()
        print("=" * 60)
        print("📊 SEQUENTIAL THINKING VALIDATION RESULTS")
        print("=" * 60)
        print(f"Total Files Checked: {self.validation_results['total_files_checked']}")
        print(f"Compliant Files: {len(self.validation_results['compliant_files'])}")
        print(
            f"Non-Compliant Files: {len(self.validation_results['non_compliant_files'])}"
        )
        print(f"Compliance Rate: {self.validation_results['compliance_rate']:.1f}%")

        if all_compliant and commit_compliant:
            print()
            print("🎉 ALL VALIDATIONS PASSED")
            print("✅ Sequential Thinking methodology compliance verified")
            print("✅ Commit allowed to proceed")
            return True
        else:
            print()
            print("🚨 VALIDATION FAILURES DETECTED")
            print("❌ Sequential Thinking methodology compliance failed")
            print("❌ COMMIT BLOCKED")
            print()
            print("📚 REQUIRED ACTIONS:")
            print("1. Add Sequential Thinking documentation to all non-compliant files")
            print("2. Include systematic approach documentation in file headers")
            print("3. Reference Sequential Thinking methodology in commit message")
            print("4. Follow Sequential Thinking Enforcement Protocol:")
            print("   .claudedirector/docs/SEQUENTIAL_THINKING_ENFORCEMENT.md")
            return False

    def save_validation_results(self):
        """Save validation results for monitoring and reporting"""
        results_dir = self.project_root / ".claudedirector" / "validation_results"
        results_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"sequential_thinking_validation_{timestamp}.json"

        self.validation_results["timestamp"] = timestamp
        self.validation_results["validation_date"] = datetime.now().isoformat()

        with open(results_file, "w") as f:
            json.dump(self.validation_results, f, indent=2)


def main():
    """Main execution function"""
    validator = SequentialThinkingValidator()

    try:
        is_valid = validator.run_validation()
        validator.save_validation_results()

        # Exit with appropriate code
        sys.exit(0 if is_valid else 1)

    except Exception as e:
        print(f"🚨 VALIDATION ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
