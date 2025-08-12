#!/usr/bin/env python3
"""
ClaudeDirector Workspace Migration Utility
Migrates from engineering-director-workspace to leadership-workspace
"""

import os
import shutil
from pathlib import Path
import argparse

class WorkspaceMigrator:
    """Handles migration from old to new workspace naming"""

    def __init__(self):
        self.home_path = Path.home()
        self.legacy_workspace = self.home_path / "engineering-director-workspace"
        self.new_workspace = self.home_path / "leadership-workspace"

    def check_migration_needed(self) -> bool:
        """Check if migration is needed"""
        return self.legacy_workspace.exists() and not self.new_workspace.exists()

    def analyze_workspace(self):
        """Analyze current workspace situation"""
        print("🔍 **Workspace Analysis**\n")

        if self.legacy_workspace.exists():
            size_mb = self._get_directory_size(self.legacy_workspace)
            file_count = self._count_files(self.legacy_workspace)
            print(f"📁 Legacy workspace found: {self.legacy_workspace}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"   Files: {file_count} items")
        else:
            print(f"❌ No legacy workspace found at: {self.legacy_workspace}")

        if self.new_workspace.exists():
            size_mb = self._get_directory_size(self.new_workspace)
            file_count = self._count_files(self.new_workspace)
            print(f"📁 New workspace found: {self.new_workspace}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"   Files: {file_count} items")
        else:
            print(f"📁 New workspace location available: {self.new_workspace}")

        # Check environment variable
        env_workspace = os.environ.get('CLAUDEDIRECTOR_WORKSPACE')
        if env_workspace:
            print(f"🔧 Environment variable set: {env_workspace}")
        else:
            print(f"🔧 No CLAUDEDIRECTOR_WORKSPACE environment variable set")

    def _get_directory_size(self, path: Path) -> float:
        """Get directory size in MB"""
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except (OSError, PermissionError):
            pass
        return total_size / (1024 * 1024)  # Convert to MB

    def _count_files(self, path: Path) -> int:
        """Count files and directories"""
        try:
            return len(list(path.rglob('*')))
        except (OSError, PermissionError):
            return 0

    def migrate_workspace(self, mode: str = "move"):
        """Migrate workspace from old to new location"""

        if not self.check_migration_needed():
            print("❌ Migration not needed or not possible:")
            if not self.legacy_workspace.exists():
                print(f"   Legacy workspace not found: {self.legacy_workspace}")
            if self.new_workspace.exists():
                print(f"   New workspace already exists: {self.new_workspace}")
            return False

        print(f"🚀 **Starting Workspace Migration**")
        print(f"From: {self.legacy_workspace}")
        print(f"To: {self.new_workspace}")
        print(f"Mode: {mode}\n")

        try:
            if mode == "move":
                print("📦 Moving workspace...")
                shutil.move(str(self.legacy_workspace), str(self.new_workspace))
                print("✅ Workspace moved successfully")

            elif mode == "copy":
                print("📦 Copying workspace...")
                shutil.copytree(str(self.legacy_workspace), str(self.new_workspace))
                print("✅ Workspace copied successfully")
                print(f"ℹ️  Legacy workspace preserved at: {self.legacy_workspace}")

            elif mode == "symlink":
                print("🔗 Creating symbolic link...")
                self.new_workspace.symlink_to(self.legacy_workspace)
                print("✅ Symbolic link created successfully")
                print(f"ℹ️  Legacy workspace remains at: {self.legacy_workspace}")

            # Update environment variable recommendation
            self._suggest_environment_update()

            return True

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False

    def _suggest_environment_update(self):
        """Suggest environment variable update"""
        env_workspace = os.environ.get('CLAUDEDIRECTOR_WORKSPACE')

        if env_workspace and "engineering-director-workspace" in env_workspace:
            new_env_value = env_workspace.replace("engineering-director-workspace", "leadership-workspace")

            print(f"\n💡 **Environment Variable Update Needed**")
            print(f"Current: CLAUDEDIRECTOR_WORKSPACE={env_workspace}")
            print(f"Update to: CLAUDEDIRECTOR_WORKSPACE={new_env_value}")
            print(f"\nAdd this to your shell configuration:")
            print(f'export CLAUDEDIRECTOR_WORKSPACE="{new_env_value}"')

    def interactive_migration(self):
        """Interactive migration with user prompts"""
        print("🎯 **ClaudeDirector Workspace Migration**\n")

        self.analyze_workspace()

        if not self.check_migration_needed():
            print("\n✅ No migration needed!")
            return

        print(f"\n📋 **Migration Options:**")
        print(f"1. **Move** - Rename directory (recommended)")
        print(f"2. **Copy** - Create copy, keep original")
        print(f"3. **Symlink** - Create link, keep original location")
        print(f"4. **Cancel** - Skip migration")

        while True:
            choice = input("\nChoice [1-4]: ").strip()

            if choice == "1":
                self.migrate_workspace("move")
                break
            elif choice == "2":
                self.migrate_workspace("copy")
                break
            elif choice == "3":
                self.migrate_workspace("symlink")
                break
            elif choice == "4":
                print("Migration cancelled")
                break
            else:
                print("Invalid choice. Please enter 1-4.")


def main():
    parser = argparse.ArgumentParser(description="Migrate ClaudeDirector workspace naming")
    parser.add_argument("--mode", choices=["move", "copy", "symlink", "interactive"],
                       default="interactive", help="Migration mode")
    parser.add_argument("--analyze-only", action="store_true",
                       help="Only analyze current workspace situation")

    args = parser.parse_args()

    migrator = WorkspaceMigrator()

    if args.analyze_only:
        migrator.analyze_workspace()
    elif args.mode == "interactive":
        migrator.interactive_migration()
    else:
        migrator.migrate_workspace(args.mode)


if __name__ == "__main__":
    main()
