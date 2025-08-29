#!/usr/bin/env python3
"""
Phase 9 Architecture Cleanup: Legacy Directory Migration Tool

This tool implements the systematic migration plan from PHASE9_ARCHITECTURE_CLEANUP_PLAN.md
to eliminate legacy technical debt and achieve single source of truth architecture.

Author: Martin | Platform Architecture
Status: Phase 9 Implementation
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Set
import ast
import json
from dataclasses import dataclass

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))


@dataclass
class MigrationMapping:
    """Defines migration from legacy to target location"""

    source_file: str
    target_file: str
    migration_type: str  # 'MOVE', 'MERGE', 'DELETE'
    notes: str = ""


class LegacyMigrationTool:
    """Systematic legacy directory migration following Phase 9 plan"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.lib_path = PROJECT_ROOT / ".claudedirector/lib"
        self.migration_mappings: List[MigrationMapping] = []
        self.import_updates: Dict[str, str] = {}

        # Legacy directories to clean up (from Phase 9 plan)
        self.legacy_dirs = [
            "clarity",
            "intelligence",
            "memory",
            "persona_integration",
            "integrations",
            "bridges",
        ]

        self._initialize_migration_mappings()

    def _initialize_migration_mappings(self):
        """Initialize migration mappings based on Phase 9 plan"""

        # Stakeholder Intelligence Consolidation (CRITICAL PRIORITY)
        self.migration_mappings.extend(
            [
                MigrationMapping(
                    "memory/intelligent_stakeholder_detector.py",
                    "context_engineering/stakeholder_layer.py",
                    "MERGE",
                    "Consolidate stakeholder detection logic",
                ),
                MigrationMapping(
                    "memory/stakeholder_engagement_engine.py",
                    "context_engineering/stakeholder_layer.py",
                    "MERGE",
                    "Consolidate stakeholder engagement logic",
                ),
                MigrationMapping(
                    "intelligence/stakeholder.py",
                    "context_engineering/stakeholder_layer.py",
                    "MERGE",
                    "Move intelligence stakeholder to context layer",
                ),
            ]
        )

        # Memory System Consolidation
        self.migration_mappings.extend(
            [
                MigrationMapping(
                    "memory/memory_manager.py",
                    "context_engineering/advanced_context_engine.py",
                    "MERGE",
                    "Consolidate memory management",
                ),
                MigrationMapping(
                    "memory/session_context_manager.py",
                    "context_engineering/conversation_layer.py",
                    "MERGE",
                    "Move session context to conversation layer",
                ),
                MigrationMapping(
                    "memory/workspace_monitor.py",
                    "context_engineering/workspace_integration.py",
                    "MERGE",
                    "Consolidate workspace monitoring",
                ),
                MigrationMapping(
                    "memory/architecture_health_monitor.py",
                    "",
                    "DELETE",
                    "Superseded by performance/ module",
                ),
            ]
        )

        # Intelligence Layer Migration
        self.migration_mappings.extend(
            [
                MigrationMapping(
                    "intelligence/meeting.py",
                    "ai_intelligence/context/meeting_intelligence.py",
                    "MOVE",
                    "Move meeting intelligence to ai_intelligence",
                ),
                MigrationMapping(
                    "intelligence/task.py",
                    "ai_intelligence/context/task_intelligence.py",
                    "MOVE",
                    "Move task intelligence to ai_intelligence",
                ),
            ]
        )

        # Integration Layer Cleanup
        self.migration_mappings.extend(
            [
                MigrationMapping(
                    "integrations/mcp_use_client.py",
                    "integration/unified_bridge.py",
                    "MERGE",
                    "Consolidate MCP client into unified bridge",
                ),
                MigrationMapping(
                    "bridges/cli_context_bridge.py",
                    "integration/unified_bridge.py",
                    "MERGE",
                    "Consolidate CLI bridge into unified bridge",
                ),
            ]
        )

    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """Analyze import dependencies for legacy directories"""
        dependencies = {}

        print("🔍 Analyzing import dependencies in legacy directories...")

        for legacy_dir in self.legacy_dirs:
            legacy_path = self.lib_path / legacy_dir
            if not legacy_path.exists():
                print(f"⚠️  Legacy directory not found: {legacy_dir}")
                continue

            dependencies[legacy_dir] = []

            # Find all Python files in legacy directory
            for py_file in legacy_path.glob("**/*.py"):
                if py_file.name == "__init__.py":
                    continue

                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Parse AST to find imports
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                dependencies[legacy_dir].append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                dependencies[legacy_dir].append(node.module)

                except Exception as e:
                    print(f"⚠️  Error analyzing {py_file}: {e}")

        # Save dependency analysis
        deps_file = PROJECT_ROOT / "dependency_analysis.json"
        with open(deps_file, "w") as f:
            json.dump(dependencies, f, indent=2)

        print(f"✅ Dependency analysis saved to {deps_file}")
        return dependencies

    def validate_migration_safety(self) -> bool:
        """Validate that migration can be performed safely"""
        print("🛡️  Validating migration safety...")

        # Check that target directories exist
        for mapping in self.migration_mappings:
            if mapping.migration_type in ["MOVE", "MERGE"] and mapping.target_file:
                target_path = self.lib_path / mapping.target_file
                target_dir = target_path.parent

                if not target_dir.exists():
                    print(f"❌ Target directory does not exist: {target_dir}")
                    return False

        # Check that source files exist
        missing_sources = []
        for mapping in self.migration_mappings:
            source_path = self.lib_path / mapping.source_file
            if not source_path.exists():
                missing_sources.append(mapping.source_file)

        if missing_sources:
            print("⚠️  Some source files not found (may already be migrated):")
            for source in missing_sources:
                print(f"   - {source}")

        print("✅ Migration safety validation completed")
        return True

    def execute_migration(self) -> bool:
        """Execute the migration plan"""
        if self.dry_run:
            print("🧪 DRY RUN MODE - No actual file changes will be made")

        print("🚀 Executing Phase 9 architecture cleanup migration...")

        for mapping in self.migration_mappings:
            source_path = self.lib_path / mapping.source_file

            if not source_path.exists():
                print(f"⚠️  Source not found: {mapping.source_file} (skipping)")
                continue

            if mapping.migration_type == "DELETE":
                print(f"🗑️  DELETE: {mapping.source_file}")
                if not self.dry_run:
                    if source_path.is_file():
                        source_path.unlink()
                    elif source_path.is_dir():
                        shutil.rmtree(source_path)

            elif mapping.migration_type == "MOVE":
                target_path = self.lib_path / mapping.target_file
                print(f"📁 MOVE: {mapping.source_file} → {mapping.target_file}")

                if not self.dry_run:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(target_path))

            elif mapping.migration_type == "MERGE":
                print(f"🔄 MERGE: {mapping.source_file} → {mapping.target_file}")
                if not self.dry_run:
                    # For MERGE operations, we need manual intervention
                    print(
                        f"   ⚠️  MERGE requires manual intervention for {mapping.source_file}"
                    )
                    print(f"   📝 Notes: {mapping.notes}")

        return True

    def remove_legacy_directories(self) -> bool:
        """Remove empty legacy directories after migration"""
        print("🧹 Removing empty legacy directories...")

        for legacy_dir in self.legacy_dirs:
            legacy_path = self.lib_path / legacy_dir

            if legacy_path.exists():
                # Check if directory is empty or only contains __pycache__
                contents = list(legacy_path.glob("*"))
                pycache_only = all(item.name == "__pycache__" for item in contents)

                if not contents or pycache_only:
                    print(f"🗑️  Removing empty legacy directory: {legacy_dir}")
                    if not self.dry_run:
                        shutil.rmtree(legacy_path)
                else:
                    print(f"⚠️  Legacy directory not empty: {legacy_dir}")
                    for item in contents:
                        if item.name != "__pycache__":
                            print(f"   - {item.name}")

        return True

    def generate_import_update_script(self) -> str:
        """Generate script to update import statements"""
        script_lines = [
            "#!/usr/bin/env python3",
            "# Generated import update script for Phase 9 cleanup",
            "",
            "import os",
            "import re",
            "from pathlib import Path",
            "",
            "def update_imports():",
            "    lib_path = Path('.claudedirector/lib')",
            "    ",
            "    # Import mappings from legacy to new locations",
            "    import_mappings = {",
        ]

        # Add import mappings based on migration plan
        for mapping in self.migration_mappings:
            if mapping.migration_type in ["MOVE", "MERGE"] and mapping.target_file:
                old_import = mapping.source_file.replace("/", ".").replace(".py", "")
                new_import = mapping.target_file.replace("/", ".").replace(".py", "")
                script_lines.append(f'        "{old_import}": "{new_import}",')

        script_lines.extend(
            [
                "    }",
                "",
                "    # Update all Python files",
                "    for py_file in lib_path.glob('**/*.py'):",
                "        try:",
                "            with open(py_file, 'r') as f:",
                "                content = f.read()",
                "            ",
                "            updated = content",
                "            for old_import, new_import in import_mappings.items():",
                "                updated = re.sub(",
                "                    rf'from {re.escape(old_import)}',",
                "                    f'from {new_import}',",
                "                    updated",
                "                )",
                "                updated = re.sub(",
                "                    rf'import {re.escape(old_import)}',",
                "                    f'import {new_import}',",
                "                    updated",
                "                )",
                "            ",
                "            if updated != content:",
                "                print(f'Updated imports in {py_file}')",
                "                with open(py_file, 'w') as f:",
                "                    f.write(updated)",
                "        except Exception as e:",
                "            print(f'Error updating {py_file}: {e}')",
                "",
                "if __name__ == '__main__':",
                "    update_imports()",
                "    print('Import update completed')",
            ]
        )

        return "\n".join(script_lines)


def main():
    parser = argparse.ArgumentParser(description="Phase 9 Legacy Migration Tool")
    parser.add_argument(
        "--dry-run", action="store_true", help="Run in dry-run mode (no file changes)"
    )
    parser.add_argument("--execute", action="store_true", help="Execute the migration")
    parser.add_argument(
        "--analyze-deps", action="store_true", help="Analyze dependencies only"
    )

    args = parser.parse_args()

    if not any([args.execute, args.analyze_deps]):
        args.dry_run = True
        args.execute = True
        print("No specific action specified, running in dry-run mode")

    tool = LegacyMigrationTool(dry_run=args.dry_run)

    if args.analyze_deps:
        dependencies = tool.analyze_dependencies()
        print("\n📊 Dependency Analysis Results:")
        for legacy_dir, deps in dependencies.items():
            print(f"\n{legacy_dir}:")
            for dep in sorted(set(deps)):
                print(f"  - {dep}")

    if args.execute:
        if not tool.validate_migration_safety():
            print("❌ Migration safety validation failed")
            return 1

        if not tool.execute_migration():
            print("❌ Migration execution failed")
            return 1

        # Generate import update script
        import_script = tool.generate_import_update_script()
        script_path = PROJECT_ROOT / "update_imports.py"
        with open(script_path, "w") as f:
            f.write(import_script)
        print(f"📝 Import update script generated: {script_path}")

        if not args.dry_run:
            tool.remove_legacy_directories()

    print("✅ Phase 9 legacy migration tool completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
