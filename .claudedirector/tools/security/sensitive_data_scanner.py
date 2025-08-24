#!/usr/bin/env python3
"""
CRITICAL SECURITY: Sensitive Data Scanner
Prevents sensitive files from being committed to git
--persona-martin: Zero-tolerance security enforcement
"""

import os
import sys
import subprocess
import re
from typing import List, Dict


class SensitiveDataScanner:
    """
    Pre-commit scanner to prevent sensitive data from entering git
    ZERO TOLERANCE for security violations
    """

    def __init__(self):
        self.sensitive_patterns = [
            # Database files
            r".*\.db$",
            r".*\.sqlite$",
            r".*\.sqlite3$",
            # Credentials and secrets
            r".*\.key$",
            r".*\.pem$",
            r".*\.p12$",
            r".*\.pfx$",
            r".*password.*",
            r".*credential.*",
            r".*secret.*",
            r".*\.env$",
            # Strategic data
            r".*strategic_memory\..*",
            r".*stakeholder.*\.db",
            r".*meeting.*\.db",
            # Backup and temporary files
            r".*\.bak$",
            r".*\.backup$",
            r".*\.tmp$",
            r".*\.temp$",
            r".*~$",
            # OS artifacts
            r"\.DS_Store$",
            r"Thumbs\.db$",
            r"desktop\.ini$",
        ]

        self.content_patterns = [
            # API keys and tokens
            r'(?i)(api[_-]?key|token|secret)["\']?\s*[:=]\s*["\'][a-zA-Z0-9+/=]{20,}["\']',
            r'(?i)(password|passwd)["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
            r'(?i)(access[_-]?token)["\']?\s*[:=]\s*["\'][a-zA-Z0-9+/=]{20,}["\']',
            # Database connection strings
            r'(?i)(connection[_-]?string|database[_-]?url)["\']?\s*[:=]\s*["\'][^"\']+["\']',
            # Strategic data markers
            r"(?i)(stakeholder[_-]?data|strategic[_-]?intelligence)",
            r"(?i)(confidential|proprietary|internal[_-]?only)",
        ]

    def scan_staged_files(self) -> List[Dict[str, str]]:
        """Scan all staged files for sensitive content"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            staged_files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
        except subprocess.CalledProcessError:
            return []

        violations = []

        for file_path in staged_files:
            if not os.path.exists(file_path):
                continue

            # Check filename patterns
            filename_violations = self._check_filename(file_path)
            violations.extend(filename_violations)

            # Check file content
            content_violations = self._check_content(file_path)
            violations.extend(content_violations)

        return violations

    def _check_filename(self, file_path: str) -> List[Dict[str, str]]:
        """Check if filename matches sensitive patterns"""
        violations = []

        for pattern in self.sensitive_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                violations.append(
                    {
                        "type": "FILENAME",
                        "severity": "CRITICAL",
                        "file": file_path,
                        "pattern": pattern,
                        "message": f"Sensitive filename pattern detected: {pattern}",
                    }
                )

        return violations

    def _check_content(self, file_path: str) -> List[Dict[str, str]]:
        """Check file content for sensitive patterns"""
        violations = []

        # Skip binary files
        if self._is_binary_file(file_path):
            return violations

        # Skip security-related files (to avoid false positives)
        if any(
            path in file_path
            for path in ["SECURITY.md", "sensitive_data_scanner.py", "security/"]
        ):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for i, line in enumerate(content.split("\n"), 1):
                for pattern in self.content_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append(
                            {
                                "type": "CONTENT",
                                "severity": "CRITICAL",
                                "file": file_path,
                                "line": i,
                                "pattern": pattern,
                                "message": f"Sensitive content detected on line {i}",
                            }
                        )

        except Exception as e:
            # If we can't read the file, be conservative and flag it
            violations.append(
                {
                    "type": "ERROR",
                    "severity": "WARNING",
                    "file": file_path,
                    "message": f"Could not scan file: {e}",
                }
            )

        return violations

    def _is_binary_file(self, file_path: str) -> bool:
        """Check if file is binary"""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(8192)
            return b"\0" in chunk
        except:
            return True


def main():
    """Pre-commit hook entry point"""
    scanner = SensitiveDataScanner()
    violations = scanner.scan_staged_files()

    if violations:
        print("🚨 CRITICAL SECURITY VIOLATION DETECTED 🚨")
        print("=" * 60)
        print("SENSITIVE DATA FOUND IN STAGED FILES!")
        print("COMMIT BLOCKED FOR SECURITY")
        print("=" * 60)

        for violation in violations:
            print(f"\n❌ {violation['severity']}: {violation['type']}")
            print(f"   File: {violation['file']}")
            if "line" in violation:
                print(f"   Line: {violation['line']}")
            print(f"   Issue: {violation['message']}")
            if "pattern" in violation:
                print(f"   Pattern: {violation['pattern']}")

        print("\n🛡️ SECURITY ENFORCEMENT:")
        print("1. Remove sensitive files from staging: git reset HEAD <file>")
        print("2. Add files to .gitignore")
        print("3. Use environment variables for secrets")
        print("4. Store databases outside repository")
        print("5. Re-attempt commit after cleanup")

        print("\n⚠️  MARTIN'S SECURITY MANDATE:")
        print("ZERO TOLERANCE for sensitive data in version control")
        print("All violations must be resolved before commit")

        sys.exit(1)

    print("✅ Security scan passed - no sensitive data detected")
    sys.exit(0)


if __name__ == "__main__":
    main()
