#!/usr/bin/env python3
"""
P0 Enforcement CLI
Lightweight interface to lib/core/validation/p0_enforcer.py business logic
"""

import sys
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent.parent.parent / ".claudedirector" / "lib"
sys.path.insert(0, str(lib_path))

from core.validation.p0_enforcer import P0EnforcementSuite


def main():
    """Lightweight CLI interface to P0 Enforcement Suite"""
    try:
        enforcer = P0EnforcementSuite()

        if len(sys.argv) < 2:
            print("Usage: p0_enforcement_cli.py <command> [args]")
            print("Commands: validate, report, check")
            return

        command = sys.argv[1]

        if command == "validate":
            print("🚨 Running P0 validation...")
            result = enforcer.validate_all_p0_features()
            if result.get("all_passed", False):
                print("✅ All P0 features validated successfully")
            else:
                print("❌ P0 validation failures detected")
                sys.exit(1)

        elif command == "report":
            print("📊 Generating P0 compliance report...")
            report = enforcer.generate_compliance_report()
            print(f"P0 Features: {report.get('total_features', 0)}")
            print(f"Passing: {report.get('passing_features', 0)}")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
