#!/usr/bin/env python3
"""
Install Systematic Commit Hooks

Installs Git hooks that automatically run systematic commit validation
to prevent the recurring issue of incomplete commits.

Author: Martin | Platform Architecture
Created: January 2025
Purpose: Systematic prevention of uncommitted changes workflow issue
"""

import os
import stat
import subprocess
from pathlib import Path
from typing import Optional


def install_pre_commit_hook(project_root: Optional[Path] = None) -> bool:
    """Install pre-commit hook that runs systematic commit checker"""

    if project_root is None:
        project_root = Path.cwd()

    git_hooks_dir = project_root / ".git" / "hooks"
    pre_commit_hook = git_hooks_dir / "pre-commit-systematic"

    # Ensure hooks directory exists
    git_hooks_dir.mkdir(exist_ok=True)

    # Create the hook script
    hook_content = """#!/bin/bash
# Systematic Commit Checker - Pre-commit Hook
# Prevents incomplete commits by validating all changes

echo "🔍 Running systematic commit validation..."

# Run the systematic commit checker
python .claudedirector/tools/development/systematic_commit_checker.py --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ COMMIT BLOCKED: Systematic validation failed"
    echo ""
    echo "💡 To see detailed report, run:"
    echo "   python .claudedirector/tools/development/systematic_commit_checker.py"
    echo ""
    echo "💡 To auto-fix common issues, run:"
    echo "   python .claudedirector/tools/development/systematic_commit_checker.py"
    echo ""
    echo "💡 To bypass this check (NOT RECOMMENDED), run:"
    echo "   git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ Systematic validation passed - commit allowed"
"""

    try:
        # Write the hook
        with open(pre_commit_hook, "w") as f:
            f.write(hook_content)

        # Make it executable
        st = os.stat(pre_commit_hook)
        os.chmod(pre_commit_hook, st.st_mode | stat.S_IEXEC)

        print(f"✅ Installed systematic pre-commit hook: {pre_commit_hook}")
        return True

    except Exception as e:
        print(f"❌ Failed to install pre-commit hook: {e}")
        return False


def install_pre_push_hook(project_root: Optional[Path] = None) -> bool:
    """Install pre-push hook for final validation"""

    if project_root is None:
        project_root = Path.cwd()

    git_hooks_dir = project_root / ".git" / "hooks"
    pre_push_hook = git_hooks_dir / "pre-push-systematic"

    # Create the hook script
    hook_content = """#!/bin/bash
# Systematic Commit Checker - Pre-push Hook
# Final validation before push to ensure complete changesets

echo "🚀 Running final systematic validation before push..."

# Check for any uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "❌ PUSH BLOCKED: Uncommitted changes detected"
    echo ""
    echo "💡 Run systematic commit checker:"
    echo "   python .claudedirector/tools/development/systematic_commit_checker.py"
    echo ""
    exit 1
fi

echo "✅ Final systematic validation passed - push allowed"
"""

    try:
        # Write the hook
        with open(pre_push_hook, "w") as f:
            f.write(hook_content)

        # Make it executable
        st = os.stat(pre_push_hook)
        os.chmod(pre_push_hook, st.st_mode | stat.S_IEXEC)

        print(f"✅ Installed systematic pre-push hook: {pre_push_hook}")
        return True

    except Exception as e:
        print(f"❌ Failed to install pre-push hook: {e}")
        return False


def create_commit_helper_script(project_root: Optional[Path] = None) -> bool:
    """Create helper script for systematic commits"""

    if project_root is None:
        project_root = Path.cwd()

    helper_script = (
        project_root
        / ".claudedirector"
        / "tools"
        / "development"
        / "systematic_commit.py"
    )

    script_content = '''#!/usr/bin/env python3
"""
Systematic Commit Helper

Wrapper script that ensures complete commits by running systematic validation
and auto-fixing common issues before committing.

Usage:
    python .claudedirector/tools/development/systematic_commit.py "commit message"
"""

import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python systematic_commit.py 'commit message'")
        sys.exit(1)

    commit_message = sys.argv[1]

    # Run systematic validation with auto-fix
    print("🔍 Running systematic commit validation...")
    result = subprocess.run([
        'python', '.claudedirector/tools/development/systematic_commit_checker.py'
    ])

    if result.returncode != 0:
        print("❌ Systematic validation failed - commit aborted")
        sys.exit(1)

    # If validation passes, commit
    print("✅ Validation passed - proceeding with commit...")
    commit_result = subprocess.run(['git', 'commit', '-m', commit_message])

    if commit_result.returncode == 0:
        print("🎉 Systematic commit completed successfully!")
    else:
        print("❌ Commit failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''

    try:
        with open(helper_script, "w") as f:
            f.write(script_content)

        # Make it executable
        st = os.stat(helper_script)
        os.chmod(helper_script, st.st_mode | stat.S_IEXEC)

        print(f"✅ Created systematic commit helper: {helper_script}")
        return True

    except Exception as e:
        print(f"❌ Failed to create commit helper: {e}")
        return False


def main():
    """Install all systematic commit tools"""
    print("🔧 Installing Systematic Commit Validation Tools...")
    print("=" * 50)

    success_count = 0

    # Install hooks
    if install_pre_commit_hook():
        success_count += 1

    if install_pre_push_hook():
        success_count += 1

    # Create helper script
    if create_commit_helper_script():
        success_count += 1

    print("\n" + "=" * 50)
    print(f"✅ Installation complete: {success_count}/3 tools installed")

    if success_count == 3:
        print("\n🎯 SYSTEMATIC COMMIT PREVENTION ACTIVE!")
        print("\n💡 Usage:")
        print("  • Normal commits now include automatic validation")
        print(
            "  • Use: python .claudedirector/tools/development/systematic_commit.py 'message'"
        )
        print(
            "  • Manual check: python .claudedirector/tools/development/systematic_commit_checker.py"
        )
        print("\n🛡️ This will prevent future uncommitted changes issues!")
    else:
        print("\n⚠️ Some tools failed to install - check permissions and try again")


if __name__ == "__main__":
    main()
