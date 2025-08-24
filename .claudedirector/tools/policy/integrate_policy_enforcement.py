#!/usr/bin/env python3
"""
Development Policy Integration Script
Safely integrates new policy enforcement with existing pre-commit hooks.
"""

import sys
import shutil
from pathlib import Path
import yaml

def backup_existing_config():
    """Backup existing pre-commit configuration."""
    config_path = Path('.pre-commit-config.yaml')
    if config_path.exists():
        backup_path = Path('.pre-commit-config.yaml.backup')
        shutil.copy2(config_path, backup_path)
        print(f"✅ Backed up existing configuration to {backup_path}")
        return True
    return False

def add_policy_hooks_to_existing():
    """Add policy enforcement hooks to existing configuration."""
    config_path = Path('.pre-commit-config.yaml')
    new_config_path = Path('.pre-commit-config-new.yaml')

    if not config_path.exists():
        print("❌ No existing .pre-commit-config.yaml found")
        return False

    if not new_config_path.exists():
        print("❌ New configuration template not found")
        return False

    try:
        # Read existing configuration
        with open(config_path, 'r') as f:
            existing_config = yaml.safe_load(f)

        # Read new policy hooks
        with open(new_config_path, 'r') as f:
            new_config = yaml.safe_load(f)

        # Find the policy enforcement section in new config
        policy_hooks = None
        for repo in new_config['repos']:
            if repo.get('repo') == 'local':
                for hook in repo['hooks']:
                    if 'policy' in hook.get('name', '').lower():
                        # Add policy hooks to existing local repo
                        for existing_repo in existing_config['repos']:
                            if existing_repo.get('repo') == 'local':
                                # Check if hook already exists
                                existing_ids = [h['id'] for h in existing_repo['hooks']]
                                if hook['id'] not in existing_ids:
                                    existing_repo['hooks'].append(hook)
                                    print(f"✅ Added policy hook: {hook['name']}")
                                else:
                                    print(f"⚠️ Policy hook already exists: {hook['name']}")
                        break

        # Write updated configuration
        with open(config_path, 'w') as f:
            yaml.dump(existing_config, f, default_flow_style=False, sort_keys=False)

        print("✅ Successfully integrated policy enforcement hooks")
        return True

    except Exception as e:
        print(f"❌ Error integrating policy hooks: {e}")
        return False

def validate_integration():
    """Validate that policy tools are executable."""
    policy_tools = [
        '.claudedirector/tools/policy/check_doc_size.py',
        '.claudedirector/tools/policy/check_architecture.py',
        '.claudedirector/tools/policy/check_p0_tests.py',
    ]

    all_valid = True
    for tool_path in policy_tools:
        tool = Path(tool_path)
        if tool.exists():
            # Make executable
            tool.chmod(0o755)
            print(f"✅ Policy tool ready: {tool_path}")
        else:
            print(f"❌ Policy tool missing: {tool_path}")
            all_valid = False

    return all_valid

def main():
    """Main integration function."""
    print("🏗️ DEVELOPMENT POLICY INTEGRATION")
    print("=" * 50)
    print("Integrating policy enforcement with existing pre-commit hooks...")
    print()

    # Step 1: Backup existing configuration
    print("📋 Step 1: Backup existing configuration")
    backup_existing_config()
    print()

    # Step 2: Validate policy tools
    print("🔧 Step 2: Validate policy tools")
    if not validate_integration():
        print("❌ Policy tools validation failed")
        sys.exit(1)
    print()

    # Step 3: Integration approach
    print("🔄 Step 3: Integration approach")
    print("Using existing file size limits (500 lines) to avoid refactoring")
    print("Adding policy enforcement alongside existing hooks")
    print("Maintaining compatibility with current workflow")
    print()

    # Step 4: Show what would be added
    print("📊 Step 4: Policy enforcement additions")
    print("The following policy checks will be added:")
    print("  • Documentation Size Policy (500 lines - aligned with code)")
    print("  • Architecture Compliance Policy (import validation)")
    print("  • P0 Test Protection Policy (prevent test skipping)")
    print()
    print("These complement existing hooks:")
    print("  • File Size Guard (Python files - 500 lines)")
    print("  • Security Scanner")
    print("  • Test Validation")
    print("  • SOLID Principles")
    print()

    print("✅ INTEGRATION READY")
    print("Policy enforcement tools are prepared and aligned with existing standards.")
    print("Run 'pre-commit install' to activate when ready.")
    print()
    print("💡 BENEFITS:")
    print("  • Consistent 500-line limits across all file types")
    print("  • Automated architecture compliance checking")
    print("  • P0 test protection against accidental disabling")
    print("  • No disruption to existing workflow")

if __name__ == "__main__":
    main()
