#!/usr/bin/env python3
"""
Stakeholder Management CLI
Lightweight interface to lib/automation/stakeholder/manager.py business logic
Replaces both stakeholder_manager.py and stakeholder_ai_manager.py
"""

import sys
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent.parent.parent / ".claudedirector" / "lib"
sys.path.insert(0, str(lib_path))

from automation.stakeholder.manager import ConsolidatedStakeholderManager


def main():
    """Lightweight CLI interface to Consolidated Stakeholder Manager"""
    try:
        manager = ConsolidatedStakeholderManager()

        if len(sys.argv) < 2:
            print("Usage: stakeholder_cli.py <command> [args]")
            print("Commands:")
            print("  add - Add stakeholder interactively")
            print("  list - List all stakeholders")
            print("  scan - AI-powered workspace scanning")
            print("  report - Generate stakeholder report")
            print("  recommendations - Get AI recommendations")
            return

        command = sys.argv[1]

        if command == "add":
            manager.add_stakeholder_interactive()

        elif command == "list":
            stakeholders = manager.list_stakeholders()
            print(f"\n📋 Found {len(stakeholders)} stakeholders:")
            for stakeholder in stakeholders:
                print(
                    f"  • {stakeholder.get('name', 'Unknown')} ({stakeholder.get('role', 'Unknown role')})"
                )

        elif command == "scan":
            print("🧠 Scanning workspace for stakeholder mentions...")
            result = manager.process_workspace_automatically()
            if result["status"] == "success":
                print(f"✅ Detected {result['detected_count']} potential stakeholders")
            else:
                print(f"❌ Error: {result['message']}")

        elif command == "report":
            print("📊 Generating stakeholder report...")
            report = manager.generate_stakeholder_report()
            if "error" not in report:
                print(f"Total stakeholders: {report['total_stakeholders']}")
                print(f"High priority: {len(report['high_priority_stakeholders'])}")
                print(f"Roles: {list(report['stakeholders_by_role'].keys())}")
            else:
                print(f"Error: {report['error']}")

        elif command == "recommendations":
            recommendations = manager.get_recommendations()
            print(f"📈 Found {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"  {i}. {rec.get('title', 'No title')}")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
