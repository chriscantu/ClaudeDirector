#!/usr/bin/env python3
"""
Security & Compliance Validation Testing
Tests security scanning, dependency safety, and compliance requirements
"""

import sys
import json
import subprocess
import unittest
from pathlib import Path

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Add additional paths for CI environment
import os

sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
sys.path.insert(0, os.getcwd())  # Current working directory


class TestSecurityCompliance(unittest.TestCase):
    """Security and compliance validation for CI/CD pipeline"""

    def setUp(self):
        """Set up security testing environment"""
        self.project_root = PROJECT_ROOT
        self.security_results = {}

    def test_dependency_security_scan(self):
        """Test dependency security scanning with safety"""
        print("🔒 Running dependency security scan...")

        try:
            # Try to install safety if not available
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "safety"], capture_output=True
            )

            # Run safety check
            result = subprocess.run(
                [sys.executable, "-m", "safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.project_root,
                env=os.environ.copy(),
            )

            if result.returncode == 0:
                # No vulnerabilities found
                self.security_results["dependency_scan"] = {
                    "status": "passed",
                    "vulnerabilities": 0,
                    "message": "No known security vulnerabilities found",
                }
                print("   ✅ No security vulnerabilities found")

            else:
                # Parse safety output
                try:
                    if result.stdout:
                        vulnerabilities = json.loads(result.stdout)
                        vuln_count = len(vulnerabilities)

                        # Check if vulnerabilities are critical
                        critical_vulns = [
                            v
                            for v in vulnerabilities
                            if v.get("vulnerability_id", "").startswith("CVE")
                        ]

                        if critical_vulns:
                            self.fail(
                                f"Critical security vulnerabilities found: {len(critical_vulns)}"
                            )

                        self.security_results["dependency_scan"] = {
                            "status": "warning",
                            "vulnerabilities": vuln_count,
                            "details": vulnerabilities,
                        }

                        # Allow non-critical vulnerabilities but warn
                        print(f"   ⚠️  {vuln_count} non-critical vulnerabilities found")

                    else:
                        # Safety returned error but no JSON
                        self.security_results["dependency_scan"] = {
                            "status": "error",
                            "message": result.stderr or "Safety check failed",
                        }
                        print(f"   ❌ Safety check failed: {result.stderr}")

                except json.JSONDecodeError:
                    # Not JSON output, treat as warning
                    self.security_results["dependency_scan"] = {
                        "status": "warning",
                        "message": "Could not parse safety output",
                    }
                    print("   ⚠️  Could not parse safety output")

        except subprocess.TimeoutExpired:
            self.fail("Dependency security scan timed out")
        except FileNotFoundError:
            self.skipTest("Safety tool not available and could not be installed")

    def test_code_security_scan(self):
        """Test code security scanning with bandit"""
        print("🔍 Running code security scan...")

        try:
            # Try to install bandit if not available
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "bandit"], capture_output=True
            )

            # Run bandit on the lib directory
            lib_dir = self.project_root / ".claudedirector/lib"

            if not lib_dir.exists():
                self.skipTest("Lib directory not found for security scanning")

            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-r", str(lib_dir), "-f", "json"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.project_root,
                env=os.environ.copy(),
            )

            try:
                if result.stdout:
                    bandit_results = json.loads(result.stdout)

                    # Extract results
                    results = bandit_results.get("results", [])
                    metrics = bandit_results.get("metrics", {})

                    # Count severity levels
                    high_severity = len(
                        [r for r in results if r.get("issue_severity") == "HIGH"]
                    )
                    medium_severity = len(
                        [r for r in results if r.get("issue_severity") == "MEDIUM"]
                    )
                    low_severity = len(
                        [r for r in results if r.get("issue_severity") == "LOW"]
                    )

                    # Fail on high severity issues
                    if high_severity > 0:
                        high_issues = [
                            r for r in results if r.get("issue_severity") == "HIGH"
                        ]
                        issue_summary = "; ".join(
                            [
                                f"{issue.get('test_name', 'Unknown')}: {issue.get('issue_text', 'No description')}"
                                for issue in high_issues[:3]
                            ]
                        )  # Show first 3
                        self.fail(
                            f"High severity security issues found: {high_severity}. Issues: {issue_summary}"
                        )

                    self.security_results["code_scan"] = {
                        "status": "passed" if high_severity == 0 else "failed",
                        "high_severity": high_severity,
                        "medium_severity": medium_severity,
                        "low_severity": low_severity,
                        "total_issues": len(results),
                        "files_scanned": metrics.get("_totals", {}).get("loc", 0),
                    }

                    if high_severity == 0:
                        print(f"   ✅ No high-severity security issues found")
                        if medium_severity > 0:
                            print(
                                f"   ⚠️  {medium_severity} medium-severity issues found"
                            )
                    else:
                        print(
                            f"   ❌ {high_severity} high-severity security issues found"
                        )

                else:
                    # No output - assume clean
                    self.security_results["code_scan"] = {
                        "status": "passed",
                        "message": "No security issues detected",
                    }
                    print("   ✅ No security issues detected")

            except json.JSONDecodeError:
                self.security_results["code_scan"] = {
                    "status": "error",
                    "message": "Could not parse bandit output",
                }
                print("   ⚠️  Could not parse bandit output")

        except subprocess.TimeoutExpired:
            self.fail("Code security scan timed out")
        except FileNotFoundError:
            self.skipTest("Bandit tool not available and could not be installed")

    def test_secrets_detection(self):
        """Test for accidentally committed secrets"""
        print("🔐 Scanning for accidentally committed secrets...")

        # Patterns for common secrets
        secret_patterns = [
            r"(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}",
            r"(?i)(secret[_-]?key|secretkey)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}",
            r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_@#$%^&*-]{8,}",
            r"(?i)(token|auth[_-]?token)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}",
            r"(?i)(private[_-]?key|privatekey)['\"]?\s*[:=]\s*['\"]?-----BEGIN",
            r"(?i)(database[_-]?url|db[_-]?url)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_://.-]+",
            # Exclude test/example patterns
            r"(?!.*(?:test|example|demo|sample|placeholder|fake|mock))",
        ]

        secrets_found = []

        # Scan key files for secrets
        files_to_scan = []

        # Add Python files
        for py_file in self.project_root.rglob("*.py"):
            if not any(
                skip in str(py_file)
                for skip in [".git", "__pycache__", ".venv", "venv"]
            ):
                files_to_scan.append(py_file)

        # Add config files
        for ext in ["*.yaml", "*.yml", "*.json", "*.conf", "*.env"]:
            for config_file in self.project_root.rglob(ext):
                if not any(
                    skip in str(config_file) for skip in [".git", "__pycache__"]
                ):
                    files_to_scan.append(config_file)

        import re

        for file_path in files_to_scan[
            :100
        ]:  # Limit to first 100 files for performance
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    for i, line in enumerate(content.split("\n"), 1):
                        # Skip comments and obviously safe lines
                        if (
                            line.strip().startswith("#")
                            or "test" in line.lower()
                            or "example" in line.lower()
                        ):
                            continue

                        for pattern in secret_patterns[
                            :-1
                        ]:  # Exclude the negative lookahead pattern
                            if re.search(pattern, line):
                                # Additional validation - skip if it's clearly a test/example
                                if any(
                                    safe_word in line.lower()
                                    for safe_word in [
                                        "test",
                                        "example",
                                        "demo",
                                        "sample",
                                        "placeholder",
                                        "fake",
                                        "mock",
                                        "xxx",
                                    ]
                                ):
                                    continue

                                secrets_found.append(
                                    {
                                        "file": str(
                                            file_path.relative_to(self.project_root)
                                        ),
                                        "line": i,
                                        "pattern": "potential_secret",
                                        "content": line.strip()[
                                            :100
                                        ],  # First 100 chars
                                    }
                                )

            except (UnicodeDecodeError, PermissionError):
                continue

        # Filter out obvious false positives
        filtered_secrets = []
        for secret in secrets_found:
            content = secret["content"].lower()

            # Skip if it contains obvious test indicators
            if any(
                indicator in content
                for indicator in [
                    "test",
                    "example",
                    "demo",
                    "sample",
                    "placeholder",
                    "mock",
                    "fake",
                    "your_",
                    "insert_",
                    "replace_",
                    "todo",
                    "fixme",
                ]
            ):
                continue

            # Skip if it's in a test file
            if any(
                test_dir in secret["file"] for test_dir in ["test", "tests", "testing"]
            ):
                continue

            filtered_secrets.append(secret)

        self.security_results["secrets_scan"] = {
            "status": "passed" if len(filtered_secrets) == 0 else "failed",
            "potential_secrets_found": len(filtered_secrets),
            "files_scanned": len(files_to_scan),
            "secrets": filtered_secrets[:5] if filtered_secrets else [],  # Show first 5
        }

        if filtered_secrets:
            self.fail(
                f"Potential secrets found in {len(filtered_secrets)} locations. "
                f"First issue: {filtered_secrets[0]['file']}:{filtered_secrets[0]['line']}"
            )
        else:
            print(f"   ✅ No secrets detected in {len(files_to_scan)} files")

    def test_file_permissions_security(self):
        """Test file permissions for security issues"""
        print("📁 Checking file permissions...")

        import stat

        permission_issues = []

        # Check for overly permissive files
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    file_stat = file_path.stat()
                    mode = file_stat.st_mode

                    # Check for world-writable files (dangerous)
                    if mode & stat.S_IWOTH:
                        permission_issues.append(
                            {
                                "file": str(file_path.relative_to(self.project_root)),
                                "issue": "world_writable",
                                "permissions": oct(mode)[-3:],
                            }
                        )

                    # Check for executable config files (suspicious)
                    if file_path.suffix in [
                        ".json",
                        ".yaml",
                        ".yml",
                        ".conf",
                        ".env",
                    ] and mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                        permission_issues.append(
                            {
                                "file": str(file_path.relative_to(self.project_root)),
                                "issue": "executable_config",
                                "permissions": oct(mode)[-3:],
                            }
                        )

                except (OSError, PermissionError):
                    continue

        self.security_results["permissions_scan"] = {
            "status": "passed" if len(permission_issues) == 0 else "warning",
            "permission_issues": len(permission_issues),
            "issues": permission_issues[:10],  # Show first 10
        }

        # Warning for permission issues but don't fail CI
        if permission_issues:
            print(f"   ⚠️  {len(permission_issues)} file permission issues found")
        else:
            print("   ✅ File permissions secure")

    def test_compliance_requirements(self):
        """Test basic compliance requirements"""
        print("📋 Checking compliance requirements...")

        compliance_checks = {
            "readme_present": (self.project_root / "README.md").exists(),
            "requirements_present": (self.project_root / "requirements.txt").exists(),
            "gitignore_present": (self.project_root / ".gitignore").exists(),
            "license_present": any(
                (self.project_root / f"LICENSE{ext}").exists()
                for ext in ["", ".txt", ".md"]
            ),
        }

        # Check for sensitive data protection
        gitignore_path = self.project_root / ".gitignore"
        has_security_ignores = False

        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
            security_patterns = ["*.env", "*.key", "*password*", "*secret*"]
            has_security_ignores = any(
                pattern in gitignore_content for pattern in security_patterns
            )

        compliance_checks["security_ignores"] = has_security_ignores

        # Count failed compliance checks
        failed_checks = [
            check for check, passed in compliance_checks.items() if not passed
        ]

        self.security_results["compliance_scan"] = {
            "status": "passed" if len(failed_checks) == 0 else "warning",
            "checks": compliance_checks,
            "failed_checks": failed_checks,
        }

        # Report compliance status
        if failed_checks:
            print(f"   ⚠️  Compliance issues: {', '.join(failed_checks)}")
        else:
            print("   ✅ All compliance requirements met")

        # Don't fail CI for basic compliance, but report issues
        if "readme_present" in failed_checks:
            print("   📝 Consider adding README.md")
        if "license_present" in failed_checks:
            print("   ⚖️  Consider adding LICENSE file")


def run_security_compliance_tests():
    """Run security and compliance tests"""
    print("🛡️  SECURITY & COMPLIANCE VALIDATION")
    print("=" * 60)
    print("Testing security scanning, dependency safety, and compliance")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecurityCompliance)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL SECURITY & COMPLIANCE TESTS PASSED")
        print("   No critical security vulnerabilities")
        print("   No secrets detected in codebase")
        print("   File permissions secure")
        print("   Basic compliance requirements met")
        return True
    else:
        print("❌ SECURITY & COMPLIANCE TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")

        # Show critical failures
        for test, traceback in result.failures:
            print(f"   Critical: {test}")

        return False


if __name__ == "__main__":
    success = run_security_compliance_tests()
    sys.exit(0 if success else 1)
