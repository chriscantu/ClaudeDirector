#!/usr/bin/env python3
"""
File Size Guard - Prevent Monolithic Files

Prevents large Python files that violate Single Responsibility Principle.
This tool enforces file size limits to maintain SOLID architecture.

Author: Martin (SOLID Architecture Enforcement)
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import argparse


class FileSizeGuard:
    """Guard against monolithic files that violate SOLID principles"""

    def __init__(self):
        # File size limits (lines)
        self.limits = {
            "python": {
                "warning": 300,    # Warn at 300 lines
                "error": 500,      # Block at 500 lines
                "critical": 1000   # Critical violation at 1000+ lines
            },
            "typescript": {
                "warning": 400,
                "error": 600,
                "critical": 1200
            },
            "javascript": {
                "warning": 400,
                "error": 600,
                "critical": 1200
            }
        }

        # Exceptions for specific files that are allowed to be larger
        self.exceptions = {
            "test_": 800,      # Test files can be larger
            "_test.py": 800,
            "migration": 1000,  # Database migrations
            "schema": 600,     # Schema definitions
            "config": 400      # Configuration files
        }

        # Directories to check
        self.check_dirs = [
            ".claudedirector/lib/",
            ".claudedirector/tools/",
            "src/",
            "lib/"
        ]

    def get_file_type(self, filepath: Path) -> str:
        """Determine file type from extension"""
        suffix = filepath.suffix.lower()
        type_mapping = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript"
        }
        return type_mapping.get(suffix, "unknown")

    def get_exception_limit(self, filepath: Path) -> int:
        """Check if file has exception for size limit"""
        filename = filepath.name.lower()

        for pattern, limit in self.exceptions.items():
            if pattern in filename:
                return limit

        return None

    def count_lines(self, filepath: Path) -> int:
        """Count lines in file, excluding empty lines and comments"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Count non-empty, non-comment lines for more accurate measurement
            significant_lines = 0
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                    significant_lines += 1

            return significant_lines
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return 0

    def check_file(self, filepath: Path) -> Dict[str, any]:
        """Check a single file for size violations"""
        file_type = self.get_file_type(filepath)

        if file_type == "unknown":
            return None

        line_count = self.count_lines(filepath)
        limits = self.limits.get(file_type, self.limits["python"])

        # Check for exceptions
        exception_limit = self.get_exception_limit(filepath)
        if exception_limit:
            limits = {
                "warning": exception_limit,
                "error": exception_limit + 200,
                "critical": exception_limit + 500
            }

        # Determine violation level
        violation_level = None
        if line_count >= limits["critical"]:
            violation_level = "critical"
        elif line_count >= limits["error"]:
            violation_level = "error"
        elif line_count >= limits["warning"]:
            violation_level = "warning"

        return {
            "filepath": filepath,
            "file_type": file_type,
            "line_count": line_count,
            "limits": limits,
            "violation_level": violation_level,
            "exception_applied": exception_limit is not None
        }

    def scan_directory(self, directory: Path) -> List[Dict]:
        """Scan directory for large files"""
        violations = []

        if not directory.exists():
            return violations

        for filepath in directory.rglob("*"):
            if filepath.is_file():
                result = self.check_file(filepath)
                if result and result["violation_level"]:
                    violations.append(result)

        return violations

    def run_check(self, target_paths: List[str] = None) -> Tuple[List[Dict], bool]:
        """Run file size check on specified paths or default directories"""
        all_violations = []
        has_blocking_violations = False

        # Use provided paths or default check directories
        paths_to_check = target_paths or self.check_dirs

        for path_str in paths_to_check:
            path = Path(path_str)
            if path.exists():
                violations = self.scan_directory(path)
                all_violations.extend(violations)

        # Check for blocking violations
        for violation in all_violations:
            if violation["violation_level"] in ["error", "critical"]:
                has_blocking_violations = True
                break

        return all_violations, has_blocking_violations

    def format_report(self, violations: List[Dict]) -> str:
        """Format violations report"""
        if not violations:
            return "✅ No file size violations detected"

        report = []
        report.append("🚨 FILE SIZE VIOLATIONS DETECTED")
        report.append("=" * 50)

        # Group by violation level
        by_level = {"critical": [], "error": [], "warning": []}
        for violation in violations:
            level = violation["violation_level"]
            by_level[level].append(violation)

        # Report critical violations first
        for level in ["critical", "error", "warning"]:
            if by_level[level]:
                level_emoji = {"critical": "🔥", "error": "❌", "warning": "⚠️"}
                report.append(f"\n{level_emoji[level]} {level.upper()} VIOLATIONS:")

                for v in by_level[level]:
                    filepath = v["filepath"]
                    line_count = v["line_count"]
                    limits = v["limits"]
                    exception = " (exception applied)" if v["exception_applied"] else ""

                    report.append(f"  • {filepath}")
                    report.append(f"    Lines: {line_count} (limit: {limits[level]}){exception}")

                    if level == "critical":
                        report.append(f"    💡 REFACTOR: This file violates Single Responsibility Principle")
                        report.append(f"    🔧 ACTION: Break into smaller, focused modules")

        # Add summary
        report.append(f"\n📊 SUMMARY:")
        report.append(f"  • Total violations: {len(violations)}")
        report.append(f"  • Critical: {len(by_level['critical'])}")
        report.append(f"  • Errors: {len(by_level['error'])}")
        report.append(f"  • Warnings: {len(by_level['warning'])}")

        return "\n".join(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="File Size Guard - Prevent Monolithic Files")
    parser.add_argument("paths", nargs="*", help="Paths to check (default: standard directories)")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--report-only", action="store_true", help="Report only, don't exit with error")

    args = parser.parse_args()

    guard = FileSizeGuard()
    violations, has_blocking = guard.run_check(args.paths)

    # Print report
    report = guard.format_report(violations)
    print(report)

    # Determine exit code
    exit_code = 0
    if has_blocking and not args.report_only:
        exit_code = 1
        print("\n🚨 BLOCKING VIOLATIONS DETECTED - Commit blocked")
        print("🔧 Refactor large files into smaller, focused modules")
    elif args.strict and violations and not args.report_only:
        exit_code = 1
        print("\n⚠️ STRICT MODE - Warnings treated as errors")
    elif violations:
        print("\n💡 Consider refactoring large files to improve maintainability")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
