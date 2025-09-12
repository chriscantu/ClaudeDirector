#!/usr/bin/env python3
"""
🚨 HARD ENFORCEMENT INSTALLATION SCRIPT
MANDATORY INSTALLATION - ZERO BYPASS - ZERO EXCEPTIONS

🧠 SEQUENTIAL THINKING METHODOLOGY APPLIED:

🎯 Problem Definition:
Need installation script that sets up complete hard enforcement system across
Git hooks, Cursor IDE integration, and CI/CD pipeline for mandatory compliance.

🔍 Root Cause Analysis:
Without systematic installation, enforcement components remain disconnected,
allowing bypass through different development paths (Git, IDE, CI).

🏗️ Solution Architecture:
Comprehensive installation script that configures Git hooks, Cursor integration,
CI/CD enforcement, and all required dependencies for complete coverage.

⚡ Implementation Strategy:
1. Install Git hooks with zero-bypass design
2. Configure Cursor IDE integration for real-time enforcement
3. Set up CI/CD pipeline enforcement
4. Install all required dependencies and configurations
5. Validate complete system installation

📈 Strategic Enhancement:
Installation system ensures complete enforcement coverage across all development
paths, eliminating all bypass opportunities through systematic setup.

📊 Success Metrics:
- 100% enforcement coverage across Git, IDE, and CI
- Zero bypass opportunities after installation
- Complete system validation and health checks

Installs HARD enforcement system that FORCES compliance with:
- Spec-kit format for all specifications
- Sequential Thinking methodology for all development
- Context7 enhancement for strategic work
- DRY and SOLID principles for all code
- PROJECT_STRUCTURE.md compliance for file placement
- BLOAT_PREVENTION_SYSTEM.md integration

🔧 Context7 MCP Integration:
Utilizes Context7 systematic installation patterns for enterprise deployment
and comprehensive enforcement system setup.

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class HardEnforcementInstaller:
    """
    🚨 HARD ENFORCEMENT SYSTEM INSTALLER

    Installs enforcement system with ZERO bypass options.
    Makes compliance MANDATORY and UNAVOIDABLE.
    """

    def __init__(self):
        self.project_root = Path.cwd()
        self.git_hooks_dir = self.project_root / ".git" / "hooks"
        self.enforcement_dir = (
            self.project_root / ".claudedirector" / "tools" / "enforcement"
        )

    def install_hard_enforcement(self) -> bool:
        """
        🚨 INSTALL HARD ENFORCEMENT SYSTEM

        Makes compliance MANDATORY across all development tools.
        """
        print("🚨 INSTALLING HARD ENFORCEMENT SYSTEM")
        print("=" * 60)
        print("ZERO TOLERANCE - ZERO BYPASS - ZERO EXCEPTIONS")
        print("=" * 60)

        success = True

        # Install Git hooks
        if not self._install_git_hooks():
            success = False

        # Install Cursor integration
        if not self._install_cursor_integration():
            success = False

        # Install CI/CD enforcement
        if not self._install_cicd_enforcement():
            success = False

        # Create enforcement configuration
        if not self._create_enforcement_config():
            success = False

        # Validate installation
        if not self._validate_installation():
            success = False

        if success:
            self._display_success_message()
        else:
            self._display_failure_message()

        return success

    def _install_git_hooks(self) -> bool:
        """Install Git hooks that BLOCK non-compliant commits"""
        print("📦 Installing Git Hooks...")

        try:
            # Ensure .git/hooks directory exists
            self.git_hooks_dir.mkdir(parents=True, exist_ok=True)

            # Install pre-commit hook
            pre_commit_source = (
                self.enforcement_dir.parent
                / "git-hooks"
                / "pre-commit-hard-enforcement"
            )
            pre_commit_target = self.git_hooks_dir / "pre-commit"

            if pre_commit_source.exists():
                shutil.copy2(pre_commit_source, pre_commit_target)
                os.chmod(pre_commit_target, 0o755)  # Make executable
                print("   ✅ Pre-commit hook installed")
            else:
                print("   ❌ Pre-commit hook source not found")
                return False

            # Install pre-push hook (if exists)
            pre_push_source = (
                self.enforcement_dir.parent / "git-hooks" / "pre-push-hard-enforcement"
            )
            pre_push_target = self.git_hooks_dir / "pre-push"

            if pre_push_source.exists():
                shutil.copy2(pre_push_source, pre_push_target)
                os.chmod(pre_push_target, 0o755)  # Make executable
                print("   ✅ Pre-push hook installed")

            return True

        except Exception as e:
            print(f"   ❌ Git hooks installation failed: {e}")
            return False

    def _install_cursor_integration(self) -> bool:
        """Install Cursor IDE integration"""
        print("🖥️  Installing Cursor Integration...")

        try:
            # Check if Cursor integration exists
            cursor_integration = self.enforcement_dir / "cursor_integration.py"

            if cursor_integration.exists():
                print("   ✅ Cursor integration available")

                # Create startup script
                startup_script = self.project_root / "start_cursor_enforcement.py"
                startup_content = f"""#!/usr/bin/env python3
\"\"\"
🚨 CURSOR HARD ENFORCEMENT STARTUP SCRIPT
Run this script to enable Cursor IDE enforcement.
\"\"\"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / ".claudedirector" / "tools" / "enforcement"))

from cursor_integration import CursorIntegrationServer

if __name__ == '__main__':
    server = CursorIntegrationServer()
    print("🚨 Starting Cursor Hard Enforcement...")
    print("Press Ctrl+C to stop")
    server.start_enforcement()
"""

                with open(startup_script, "w") as f:
                    f.write(startup_content)
                os.chmod(startup_script, 0o755)

                print("   ✅ Cursor startup script created")
                return True
            else:
                print("   ❌ Cursor integration not found")
                return False

        except Exception as e:
            print(f"   ❌ Cursor integration installation failed: {e}")
            return False

    def _install_cicd_enforcement(self) -> bool:
        """Install CI/CD enforcement"""
        print("🚀 Installing CI/CD Enforcement...")

        try:
            # Check if GitHub workflows directory exists
            workflows_dir = self.project_root / ".github" / "workflows"

            if workflows_dir.exists():
                # Create hard enforcement workflow
                enforcement_workflow = workflows_dir / "hard-enforcement.yml"
                workflow_content = """name: Hard Enforcement Validation

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main, develop ]

jobs:
  hard-enforcement:
    name: "🚨 Hard Compliance Enforcement"
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Hard Enforcement Validation
      run: |
        echo "🚨 HARD ENFORCEMENT VALIDATION"
        echo "ZERO TOLERANCE - ZERO BYPASS - ZERO EXCEPTIONS"
        python .claudedirector/tools/enforcement/cursor_claude_enforcer.py "ci-cd-validation" --files $(git diff --name-only HEAD~1) --description "CI/CD validation"
"""

                with open(enforcement_workflow, "w") as f:
                    f.write(workflow_content)

                print("   ✅ GitHub Actions enforcement workflow created")
            else:
                print("   ⚠️  No .github/workflows directory found")

            return True

        except Exception as e:
            print(f"   ❌ CI/CD enforcement installation failed: {e}")
            return False

    def _create_enforcement_config(self) -> bool:
        """Create enforcement configuration"""
        print("⚙️  Creating Enforcement Configuration...")

        try:
            config_dir = self.project_root / ".claudedirector" / "config"
            config_dir.mkdir(parents=True, exist_ok=True)

            config_file = config_dir / "hard_enforcement_config.yaml"
            config_content = """# 🚨 HARD ENFORCEMENT CONFIGURATION
# ZERO TOLERANCE - ZERO BYPASS - ZERO EXCEPTIONS

enforcement_rules:
  spec_kit_format:
    enabled: true
    level: MANDATORY
    description: "All specifications must use spec-kit format"

  sequential_thinking:
    enabled: true
    level: MANDATORY
    description: "All development must use Sequential Thinking methodology"

  context7_enhancement:
    enabled: true
    level: MANDATORY
    description: "Strategic work must use Context7 enhancement"

  solid_principles:
    enabled: true
    level: MANDATORY
    description: "All code must follow SOLID principles"
    max_class_lines: 200

  dry_principle:
    enabled: true
    level: MANDATORY
    description: "All code must follow DRY principle"
    max_string_duplicates: 2

  project_structure:
    enabled: true
    level: MANDATORY
    description: "All files must comply with PROJECT_STRUCTURE.md"

  bloat_prevention:
    enabled: true
    level: MANDATORY
    description: "Must integrate with BLOAT_PREVENTION_SYSTEM.md"

  p0_protection:
    enabled: true
    level: MANDATORY
    description: "P0 tests must remain at 39/39 passing"

performance_targets:
  max_validation_time_seconds: 5
  max_alert_time_seconds: 1
  max_completion_time_seconds: 10

bypass_options:
  emergency_bypass: false
  developer_override: false
  admin_override: false

audit_logging:
  enabled: true
  log_file: ".claudedirector/logs/enforcement.log"
  include_context: true
  retention_days: 90
"""

            with open(config_file, "w") as f:
                f.write(config_content)

            print("   ✅ Enforcement configuration created")
            return True

        except Exception as e:
            print(f"   ❌ Configuration creation failed: {e}")
            return False

    def _validate_installation(self) -> bool:
        """Validate enforcement installation"""
        print("🔍 Validating Installation...")

        validation_results = []

        # Check Git hooks
        pre_commit_hook = self.git_hooks_dir / "pre-commit"
        validation_results.append(
            (
                "Pre-commit hook",
                pre_commit_hook.exists() and os.access(pre_commit_hook, os.X_OK),
            )
        )

        # Check enforcement tools
        enforcer_tool = self.enforcement_dir / "cursor_claude_enforcer.py"
        validation_results.append(("Enforcement tool", enforcer_tool.exists()))

        # Check configuration
        config_file = (
            self.project_root
            / ".claudedirector"
            / "config"
            / "hard_enforcement_config.yaml"
        )
        validation_results.append(("Configuration file", config_file.exists()))

        # Display results
        all_passed = True
        for check_name, passed in validation_results:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False

        return all_passed

    def _display_success_message(self):
        """Display successful installation message"""
        print("\n" + "=" * 60)
        print("🎉 HARD ENFORCEMENT SYSTEM INSTALLED SUCCESSFULLY")
        print("=" * 60)
        print("✅ Git hooks installed and active")
        print("✅ Cursor integration available")
        print("✅ CI/CD enforcement configured")
        print("✅ Configuration files created")
        print("\n🚨 ENFORCEMENT NOW ACTIVE:")
        print("   • All commits will be validated")
        print("   • All file operations will be monitored")
        print("   • All CI/CD builds will be enforced")
        print("   • NO BYPASS OPTIONS AVAILABLE")
        print("\n📋 COMPLIANCE REQUIREMENTS:")
        print("   ✅ Spec-kit format for specifications")
        print("   ✅ Sequential Thinking for development")
        print("   ✅ Context7 enhancement for strategic work")
        print("   ✅ SOLID and DRY principles for code")
        print("   ✅ PROJECT_STRUCTURE.md compliance")
        print("   ✅ BLOAT_PREVENTION_SYSTEM.md integration")
        print("   ✅ P0 test protection (39/39 passing)")
        print("\n🚀 NEXT STEPS:")
        print("   1. Test enforcement with a commit")
        print("   2. Start Cursor integration: python start_cursor_enforcement.py")
        print("   3. Ensure all team members understand requirements")
        print("=" * 60)

    def _display_failure_message(self):
        """Display installation failure message"""
        print("\n" + "=" * 60)
        print("❌ HARD ENFORCEMENT INSTALLATION FAILED")
        print("=" * 60)
        print("🚨 CRITICAL: Enforcement system not properly installed")
        print("📋 REQUIRED ACTIONS:")
        print("   1. Review error messages above")
        print("   2. Fix installation issues")
        print("   3. Re-run installation script")
        print("   4. Validate all components are working")
        print("\n⚠️  COMPLIANCE NOT ENFORCED UNTIL INSTALLATION SUCCEEDS")
        print("=" * 60)


def main():
    """CLI entry point for hard enforcement installation"""
    import argparse

    parser = argparse.ArgumentParser(description="Hard Enforcement System Installer")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force installation even if already installed",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing installation",
    )

    args = parser.parse_args()

    installer = HardEnforcementInstaller()

    if args.validate_only:
        print("🔍 VALIDATING EXISTING INSTALLATION")
        success = installer._validate_installation()
        sys.exit(0 if success else 1)
    else:
        success = installer.install_hard_enforcement()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
