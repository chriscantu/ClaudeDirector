#!/usr/bin/env python3
"""
Weekly Report Generator CLI
Lightweight interface to lib/reporting/weekly_reporter.py business logic
"""

import sys
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent.parent.parent / ".claudedirector" / "lib"
sys.path.insert(0, str(lib_path))

from reporting.weekly_reporter import WeeklyReportGenerator


def main():
    """Lightweight CLI interface to Weekly Report Generator business logic"""
    try:
        generator = WeeklyReportGenerator()

        if len(sys.argv) < 2:
            print("Usage: weekly_report_cli.py <command> [args]")
            print("Commands: generate, validate, config")
            return

        command = sys.argv[1]

        if command == "generate":
            print("Generating weekly report...")
            result = generator.generate_report()
            print(f"Report generated: {result}")

        elif command == "validate":
            print("Validating configuration...")
            is_valid = generator.validate_config()
            print(f"Configuration valid: {is_valid}")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
