#!/usr/bin/env python3
"""
Strategic Task Management CLI
Lightweight interface to lib/automation/task_manager.py business logic
"""

import sys
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent.parent.parent / ".claudedirector" / "lib"
sys.path.insert(0, str(lib_path))

from automation.task_manager import StrategicTaskManager


def main():
    """Lightweight CLI interface to Strategic Task Manager business logic"""
    try:
        manager = StrategicTaskManager()

        if len(sys.argv) < 2:
            print("Usage: strategic_task_cli.py <command> [args]")
            print("Commands: scan, create, list, update, delete")
            return

        command = sys.argv[1]

        if command == "scan":
            results = manager.scan_workspace_for_tasks()
            print(f"Scanned workspace, found {len(results)} potential tasks")

        elif command == "list":
            tasks = manager.list_tasks()
            for task in tasks:
                print(f"- {task['title']} ({task['status']})")

        else:
            print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
