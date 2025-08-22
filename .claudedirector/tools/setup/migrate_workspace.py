#!/usr/bin/env python3
"""
ClaudeDirector Workspace Migration Tool
Helps migrate from old workspace structure to new clean separation
"""

import os
import shutil
import sys
from pathlib import Path


class WorkspaceMigrator:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.old_workspace_locations = [
            "../platform-eng-leader-claude-config/workspace",
            "../strategic_integration_service_backup/workspace",
            "./workspace_backup_20250810",
            "./workspace",
        ]
        self.recommended_workspace = Path.home() / "engineering-director-workspace"

    def print_header(self):
        print("🔄 ClaudeDirector Workspace Migration")
        print("=" * 50)
        print("Migrating from old workspace structure to new clean separation")
        print()

    def find_existing_workspaces(self):
        """Find existing workspace directories with data."""
        found_workspaces = []

        for location in self.old_workspace_locations:
            workspace_path = Path(location)
            if workspace_path.exists() and workspace_path.is_dir():
                # Check if it has actual content
                contents = list(workspace_path.iterdir())
                if contents:
                    found_workspaces.append(workspace_path.resolve())

        return found_workspaces

    def analyze_workspace(self, workspace_path):
        """Analyze workspace contents."""
        print(f"📂 Found workspace: {workspace_path}")
        contents = []
        total_size = 0

        for item in workspace_path.rglob("*"):
            if item.is_file():
                size = item.stat().st_size
                total_size += size
                contents.append((item.relative_to(workspace_path), size))

        print(f"   📊 {len(contents)} files, {self.format_size(total_size)} total")

        # Show key directories
        dirs = [item for item in workspace_path.iterdir() if item.is_dir()]
        if dirs:
            print(f"   📁 Key directories: {', '.join([d.name for d in dirs[:5]])}")
            if len(dirs) > 5:
                print(f"      ... and {len(dirs) - 5} more")
        print()

        return contents, total_size

    def format_size(self, size_bytes):
        """Format file size in human readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def migrate_workspace(self, source_path, dest_path):
        """Migrate workspace from source to destination."""
        print(f"🚀 Migrating workspace...")
        print(f"   From: {source_path}")
        print(f"   To:   {dest_path}")

        # Create destination if it doesn't exist
        dest_path.mkdir(parents=True, exist_ok=True)

        # Copy contents
        for item in source_path.iterdir():
            dest_item = dest_path / item.name

            try:
                if item.is_dir():
                    if dest_item.exists():
                        print(f"   📁 Merging directory: {item.name}")
                        shutil.copytree(item, dest_item, dirs_exist_ok=True)
                    else:
                        print(f"   📁 Copying directory: {item.name}")
                        shutil.copytree(item, dest_item)
                else:
                    print(f"   📄 Copying file: {item.name}")
                    shutil.copy2(item, dest_item)

            except Exception as e:
                print(f"   ❌ Error copying {item.name}: {e}")
                return False

        print("   ✅ Migration completed successfully!")
        return True

    def setup_environment(self):
        """Help user set up environment variables."""
        print("\n🔧 Setting up environment variables...")

        shell_configs = {
            "bash": Path.home() / ".bashrc",
            "zsh": Path.home() / ".zshrc",
            "fish": Path.home() / ".config" / "fish" / "config.fish",
        }

        env_var = f'export CLAUDEDIRECTOR_WORKSPACE="{self.recommended_workspace}"'
        fish_var = f'set -gx CLAUDEDIRECTOR_WORKSPACE "{self.recommended_workspace}"'

        print(f"\n📝 Add this to your shell configuration:")
        print(f"   Bash/Zsh: {env_var}")
        print(f"   Fish:      {fish_var}")

        # Try to detect current shell and offer to add automatically
        current_shell = os.environ.get("SHELL", "").split("/")[-1]
        if current_shell in shell_configs:
            config_file = shell_configs[current_shell]

            response = input(f"\n❓ Add to {config_file}? (y/N): ").strip().lower()
            if response == "y":
                try:
                    config_file.parent.mkdir(parents=True, exist_ok=True)
                    with config_file.open("a") as f:
                        f.write(f"\n# ClaudeDirector workspace\n")
                        if current_shell == "fish":
                            f.write(f"{fish_var}\n")
                        else:
                            f.write(f"{env_var}\n")
                    print(f"   ✅ Added to {config_file}")
                    print(f"   🔄 Run 'source {config_file}' or restart your terminal")
                except Exception as e:
                    print(f"   ❌ Error writing to {config_file}: {e}")

    def create_workspace_readme(self):
        """Create README for new workspace."""
        readme_path = self.recommended_workspace / "README.md"

        readme_content = f"""# Engineering Director Workspace

Your personal workspace for engineering leadership activities.

## Organization

- `current-initiatives/` - Active projects and initiatives
- `meeting-prep/` - Meeting preparation and materials
- `stakeholder-analysis/` - Team and stakeholder management
- `platform-strategy/` - Strategic planning and documentation
- `budget-planning/` - Financial planning and ROI analysis
- `data/` - Working data and analysis
- `templates/` - Your custom templates

## ClaudeDirector Integration

This workspace is automatically detected by ClaudeDirector when the
`CLAUDEDIRECTOR_WORKSPACE` environment variable is set to:
```
{self.recommended_workspace}
```

## Usage

```bash
# Analyze current initiatives
claudedirector analyze initiatives

# Prepare for meetings
claudedirector meeting prep --type weekly-leadership

# Strategic planning assistance
claudedirector strategy --persona martin platform-architecture
```

---

*Generated by ClaudeDirector Workspace Migration Tool*
*Framework location: {self.current_dir}*
"""

        try:
            with readme_path.open("w") as f:
                f.write(readme_content)
            print(f"   ✅ Created workspace README: {readme_path}")
        except Exception as e:
            print(f"   ❌ Error creating README: {e}")

    def run(self):
        """Run the migration process."""
        self.print_header()

        # Find existing workspaces
        workspaces = self.find_existing_workspaces()

        if not workspaces:
            print("❌ No existing workspaces found in expected locations:")
            for location in self.old_workspace_locations:
                print(f"   - {location}")
            print("\n💡 If your workspace is elsewhere, you can:")
            print(f"   1. Copy it manually to: {self.recommended_workspace}")
            print(f"   2. Create a symbolic link")
            print(f"   3. Set CLAUDEDIRECTOR_WORKSPACE to your current location")
            return

        if len(workspaces) == 1:
            source_workspace = workspaces[0]
            print(f"🎯 Found one workspace to migrate:")
        else:
            print(f"🎯 Found {len(workspaces)} workspaces:")
            for i, workspace in enumerate(workspaces, 1):
                print(f"   {i}. {workspace}")

            choice = input(
                f"\n❓ Which workspace to migrate? (1-{len(workspaces)}): "
            ).strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(workspaces):
                    source_workspace = workspaces[choice_idx]
                else:
                    print("❌ Invalid choice")
                    return
            except ValueError:
                print("❌ Invalid choice")
                return

        # Analyze source workspace
        contents, total_size = self.analyze_workspace(source_workspace)

        if not contents:
            print("❌ Source workspace appears to be empty")
            return

        # Check if destination exists
        if self.recommended_workspace.exists():
            print(f"⚠️  Destination already exists: {self.recommended_workspace}")
            response = (
                input("❓ Merge with existing workspace? (y/N): ").strip().lower()
            )
            if response != "y":
                print("❌ Migration cancelled")
                return
        else:
            print(f"🎯 Will create new workspace: {self.recommended_workspace}")

        # Confirm migration
        response = input(f"\n❓ Proceed with migration? (y/N): ").strip().lower()
        if response != "y":
            print("❌ Migration cancelled")
            return

        # Perform migration
        if self.migrate_workspace(source_workspace, self.recommended_workspace):
            self.create_workspace_readme()
            self.setup_environment()

            print(f"\n🎉 Migration completed successfully!")
            print(f"📂 Your workspace is now at: {self.recommended_workspace}")
            print(f"📚 See docs/WORKSPACE_GUIDE.md for detailed usage information")

            print(f"\n🚀 Next steps:")
            print(f"   1. Restart your terminal or source your shell config")
            print(f"   2. Test: claudedirector workspace status")
            print(f"   3. Start using: claudedirector analyze --help")
        else:
            print("❌ Migration failed")


if __name__ == "__main__":
    migrator = WorkspaceMigrator()
    migrator.run()
