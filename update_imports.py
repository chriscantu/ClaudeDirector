#!/usr/bin/env python3
# Generated import update script for Phase 9 cleanup

import os
import re
from pathlib import Path


def update_imports():
    lib_path = Path(".claudedirector/lib")

    # Import mappings from legacy to new locations
    import_mappings = {
        "memory.intelligent_stakeholder_detector": "context_engineering.stakeholder_layer",
        "memory.stakeholder_engagement_engine": "context_engineering.stakeholder_layer",
        "intelligence.stakeholder": "context_engineering.stakeholder_layer",
        "memory.memory_manager": "context_engineering.advanced_context_engine",
        "memory.session_context_manager": "context_engineering.conversation_layer",
        "memory.workspace_monitor": "context_engineering.workspace_integration",
        "intelligence.meeting": "ai_intelligence.context.meeting_intelligence",
        "intelligence.task": "ai_intelligence.context.task_intelligence",
        "integrations.mcp_use_client": "integration.unified_bridge",
        "bridges.cli_context_bridge": "integration.unified_bridge",
    }

    # Update all Python files
    for py_file in lib_path.glob("**/*.py"):
        try:
            with open(py_file, "r") as f:
                content = f.read()

            updated = content
            for old_import, new_import in import_mappings.items():
                updated = re.sub(
                    rf"from {re.escape(old_import)}", f"from {new_import}", updated
                )
                updated = re.sub(
                    rf"import {re.escape(old_import)}", f"import {new_import}", updated
                )

            if updated != content:
                print(f"Updated imports in {py_file}")
                with open(py_file, "w") as f:
                    f.write(updated)
        except Exception as e:
            print(f"Error updating {py_file}: {e}")


if __name__ == "__main__":
    update_imports()
    print("Import update completed")
