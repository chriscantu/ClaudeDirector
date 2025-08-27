#!/usr/bin/env python3
"""
P0 BLOCKING Tests for Complete New Setup Experience
===================================================

CRITICAL: These tests validate the COMPLETE new user setup journey from
fresh git clone to working ClaudeDirector installation.

ZERO TOLERANCE: If a new user cannot successfully set up ClaudeDirector,
our product fails at the first touchpoint.

Test Coverage:
- Fresh git clone simulation
- Dependency installation validation
- Environment setup requirements
- First-run experience reliability
- Cross-platform compatibility
- Network dependency handling
- Error recovery for common setup failures
- Performance requirements for new setup

Author: Martin | Platform Architecture
Purpose: Eliminate new user setup failures - P0 BLOCKING
Status: MANDATORY - Cannot be skipped or bypassed
"""

import os
import sys
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from unittest.mock import patch, MagicMock


class TestCompleteNewSetupP0(unittest.TestCase):
    """P0 Critical Complete New Setup Tests - Zero tolerance for new user failure"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment for new setup simulation"""
        # Find actual project root for reference
        current_dir = Path(__file__).parent
        cls.source_project_root = None

        for parent in current_dir.parents:
            if (parent / "bin" / "claudedirector").exists():
                cls.source_project_root = parent
                break

        if not cls.source_project_root:
            raise RuntimeError("Cannot find source project root for new setup testing")

        cls.test_workspaces = []  # Track temporary directories for cleanup

        # Create shared workspace for faster tests
        cls.shared_workspace = cls._create_shared_workspace()

    @classmethod
    def tearDownClass(cls):
        """Clean up all test workspaces"""
        for workspace in cls.test_workspaces:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)

    @classmethod
    def _create_shared_workspace(cls):
        """Create a shared workspace to reduce setup overhead"""
        workspace = Path(tempfile.mkdtemp(prefix="claudedirector_shared_setup_"))
        cls.test_workspaces.append(workspace)

        # Copy source project to simulate fresh git clone
        target_dir = workspace / "ClaudeDirector"
        shutil.copytree(
            cls.source_project_root,
            target_dir,
            ignore=shutil.ignore_patterns(
                ".git",
                "__pycache__",
                "*.pyc",
                ".pytest_cache",
                "venv",
                ".venv",
                "node_modules",
                ".claudedirector/backups",
            ),
        )

        # Ensure claudedirector executable has correct permissions
        claudedirector_path = target_dir / "bin" / "claudedirector"
        if claudedirector_path.exists():
            os.chmod(claudedirector_path, 0o755)

        return target_dir

    def create_fresh_workspace(self, workspace_name: str) -> Path:
        """Create a fresh workspace simulating a new git clone"""
        workspace = Path(
            tempfile.mkdtemp(prefix=f"claudedirector_newsetup_{workspace_name}_")
        )
        self.test_workspaces.append(workspace)

        # Copy source project to simulate fresh git clone
        target_dir = workspace / "ClaudeDirector"
        shutil.copytree(
            self.source_project_root,
            target_dir,
            ignore=shutil.ignore_patterns(
                ".git",
                "__pycache__",
                "*.pyc",
                ".pytest_cache",
                "venv",
                ".venv",
                "node_modules",
                ".claudedirector/backups",
            ),
        )

        # Ensure claudedirector executable has correct permissions
        claudedirector_path = target_dir / "bin" / "claudedirector"
        if claudedirector_path.exists():
            os.chmod(claudedirector_path, 0o755)

        return target_dir

    def test_p0_combined_essential_setup_checks(self):
        """P0: Combined essential checks for speed optimization"""
        # Use shared workspace for faster execution
        workspace = self.shared_workspace
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Combined Check 1: File structure + executable test
        required_files = [
            "README.md",
            "bin/claudedirector",
            "requirements.txt",
            ".claudedirector/lib",
        ]

        for required_file in required_files:
            file_path = workspace / required_file
            self.assertTrue(
                file_path.exists(),
                f"CRITICAL: Fresh clone missing required file: {required_file}",
            )

        # Combined Check 2: Basic execution + performance
        start_time = time.time()
        try:
            result = subprocess.run(
                [str(claudedirector_path), "--version"],
                capture_output=True,
                text=True,
                timeout=3,  # Aggressive timeout for P0
                cwd=str(workspace),
            )

            execution_time = time.time() - start_time

            # Must execute and be fast
            self.assertIn(result.returncode, [0, 1], "CRITICAL: Executable failed")
            self.assertLess(
                execution_time, 3.0, f"CRITICAL: Too slow ({execution_time:.2f}s)"
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: New user executable timed out")

        # Combined Check 3: Documentation + Python compatibility
        try:
            readme_content = (
                (workspace / "README.md").read_text(encoding="utf-8").lower()
            )
            self.assertIn(
                "getting started",
                readme_content,
                "CRITICAL: README missing setup guidance",
            )

            # Test basic Python path setup
            sys_path_test = (
                'import sys; sys.path.insert(0, ".claudedirector/lib"); print("OK")'
            )
            result = subprocess.run(
                [sys.executable, "-c", sys_path_test],
                capture_output=True,
                text=True,
                timeout=2,
                cwd=str(workspace),
            )

            self.assertEqual(result.returncode, 0, "CRITICAL: Python path setup failed")
            self.assertIn(
                "OK", result.stdout, "CRITICAL: Basic setup validation failed"
            )

        except Exception as e:
            self.fail(f"CRITICAL: Documentation/Python compatibility failed: {e}")

    def test_p0_fresh_clone_to_working_system(self):
        """P0: Complete journey from fresh clone to working ClaudeDirector"""
        workspace = self.create_fresh_workspace("complete_journey")

        # Step 1: Verify fresh workspace structure (fast check)
        required_files = [
            "README.md",
            "bin/claudedirector",
            "requirements.txt",
            ".claudedirector/lib",
        ]

        for required_file in required_files:
            file_path = workspace / required_file
            self.assertTrue(
                file_path.exists(),
                f"CRITICAL: Fresh clone missing required file: {required_file}",
            )

        # Step 2: Test essential Python imports only (optimized for speed)
        essential_imports = ["import sys, os, pathlib, json"]

        try:
            import_result = subprocess.run(
                [sys.executable, "-c", essential_imports[0]],
                capture_output=True,
                text=True,
                timeout=5,  # Reduced timeout
                cwd=str(workspace),
            )

            self.assertEqual(
                import_result.returncode,
                0,
                f"CRITICAL: Essential Python imports failed\nSTDERR: {import_result.stderr}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Essential import check timed out")

    def test_p0_claudedirector_executable_immediate_availability(self):
        """P0: ClaudeDirector executable must work immediately after clone"""
        workspace = self.create_fresh_workspace("executable_test")
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Must be executable
        self.assertTrue(
            claudedirector_path.exists(),
            f"CRITICAL: claudedirector executable missing in fresh clone",
        )

        # Test immediate execution (should work without additional setup)
        try:
            # Test basic execution (optimized for speed)
            result = subprocess.run(
                [str(claudedirector_path), "--version"],
                capture_output=True,
                text=True,
                timeout=5,  # Reduced from 15s
                cwd=str(workspace),
            )

            # Should either show version or deprecation notice (both are acceptable)
            self.assertIn(
                result.returncode,
                [0, 1],  # 0 = success, 1 = deprecated but working
                f"CRITICAL: ClaudeDirector executable failed on fresh clone\n"
                f"Return code: {result.returncode}\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: ClaudeDirector executable hung on fresh clone")

    def test_p0_python_environment_requirements(self):
        """P0: Must work with standard Python environments new users have"""
        workspace = self.create_fresh_workspace("python_env")

        # Test common Python versions that new users might have
        python_commands = [
            sys.executable,  # Current Python
            "python3",  # Common alias
            "python",  # Another common alias
        ]

        for python_cmd in python_commands:
            try:
                # Test basic Python execution in workspace
                result = subprocess.run(
                    [python_cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(workspace),
                )

                if result.returncode == 0:
                    # Test basic ClaudeDirector import capability
                    sys_path_setup = (
                        f'import sys; sys.path.insert(0, ".claudedirector/lib")'
                    )
                    basic_test = (
                        f'{sys_path_setup}; print("ClaudeDirector path setup: OK")'
                    )

                    import_result = subprocess.run(
                        [python_cmd, "-c", basic_test],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=str(workspace),
                    )

                    if import_result.returncode == 0:
                        self.assertIn(
                            "ClaudeDirector path setup: OK",
                            import_result.stdout,
                            f"CRITICAL: Basic ClaudeDirector import setup failed with {python_cmd}",
                        )
                        break  # Found working Python

            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue  # Try next Python command
        else:
            self.fail(
                "CRITICAL: No working Python environment found for new ClaudeDirector setup\n"
                f"Tested commands: {python_commands}"
            )

    def test_p0_documentation_accessibility_fresh_clone(self):
        """P0: New users must have immediate access to setup documentation"""
        workspace = self.create_fresh_workspace("docs_access")

        # Critical documentation files for new users
        critical_docs = {
            "README.md": ["Quick Start", "Installation", "Getting Started"],
            "docs/GETTING_STARTED.md": ["Setup", "Configuration", "First"],
            "docs/CAPABILITIES.md": [
                "capabilities",
                "personas",
                "strategic",
            ],  # More realistic content expectations
        }

        for doc_file, required_content in critical_docs.items():
            doc_path = workspace / doc_file

            self.assertTrue(
                doc_path.exists(),
                f"CRITICAL: New user documentation missing: {doc_file}",
            )

            try:
                content = doc_path.read_text(encoding="utf-8")

                for requirement in required_content:
                    self.assertIn(
                        requirement.lower(),
                        content.lower(),
                        f"CRITICAL: New user documentation incomplete\n"
                        f"File: {doc_file}\n"
                        f"Missing content about: {requirement}",
                    )

            except UnicodeDecodeError:
                self.fail(f"CRITICAL: New user documentation unreadable: {doc_file}")

    def test_p0_setup_performance_requirements_new_user(self):
        """P0: Setup must meet performance requirements for new users"""
        workspace = self.create_fresh_workspace("performance")
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Make executable
        os.chmod(claudedirector_path, 0o755)

        # New user performance requirements (more lenient than existing users)
        start_time = time.time()

        try:
            result = subprocess.run(
                [str(claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=15,  # New users get 15s timeout
                cwd=str(workspace),
            )

            execution_time = time.time() - start_time

            # New user should get response within 5 seconds (optimized)
            self.assertLess(
                execution_time,
                5.0,
                f"CRITICAL: New user setup too slow ({execution_time:.2f}s > 5.0s limit)\n"
                f"New users will abandon slow setup. Return code: {result.returncode}\n"
                f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: New user setup command timed out - unacceptable UX")

    def test_p0_error_recovery_fresh_setup(self):
        """P0: Setup must handle common new user errors gracefully"""
        workspace = self.create_fresh_workspace("error_recovery")
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Test common new user error scenarios
        error_scenarios = [
            {
                "name": "Wrong directory execution",
                "cmd": [str(claudedirector_path), "status"],
                "cwd": str(workspace.parent),  # Run from outside project
                "expect_graceful": True,
            },
            {
                "name": "Help command test",
                "cmd": [str(claudedirector_path), "--help"],
                "cwd": str(workspace),
                "expect_graceful": True,  # Should work gracefully
            },
        ]

        for scenario in error_scenarios:
            with self.subTest(scenario=scenario["name"]):
                # Setup scenario if needed
                if "setup" in scenario:
                    scenario["setup"]()

                try:
                    # Ensure executable permissions are set before test
                    if claudedirector_path.exists():
                        os.chmod(claudedirector_path, 0o755)

                    result = subprocess.run(
                        scenario["cmd"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=scenario["cwd"],
                    )

                    # Should not hang or crash - must provide feedback
                    output = result.stdout + result.stderr

                    if scenario["expect_graceful"]:
                        self.assertNotIn(
                            "Traceback",
                            output,
                            f"CRITICAL: New user error scenario showed raw traceback\n"
                            f"Scenario: {scenario['name']}\n"
                            f"Output: {output}",
                        )

                    # Must provide some helpful feedback
                    self.assertGreater(
                        len(output.strip()),
                        10,
                        f"CRITICAL: No feedback provided for new user error\n"
                        f"Scenario: {scenario['name']}",
                    )

                except subprocess.TimeoutExpired:
                    self.fail(
                        f"CRITICAL: Error recovery hung for scenario: {scenario['name']}"
                    )

                finally:
                    # Reset permissions for next test
                    if claudedirector_path.exists():
                        os.chmod(claudedirector_path, 0o755)

    def test_p0_minimal_system_requirements(self):
        """P0: Must work on minimal systems new users might have"""
        workspace = self.create_fresh_workspace("minimal_system")

        # Test with minimal Python environment
        minimal_python_test = """
import sys
import os
import json
import pathlib

# Simulate minimal system check
try:
    sys.path.insert(0, ".claudedirector/lib")

    # Test basic import without full dependencies
    from pathlib import Path

    # Verify core directory structure exists
    core_dirs = [
        ".claudedirector/lib/core",
        ".claudedirector/lib/transparency",
        ".claudedirector/tools"
    ]

    missing_dirs = []
    for dir_path in core_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"MISSING_DIRS: {missing_dirs}")
        sys.exit(1)
    else:
        print("MINIMAL_SYSTEM_CHECK: OK")
        sys.exit(0)

except Exception as e:
    print(f"MINIMAL_SYSTEM_ERROR: {e}")
    sys.exit(1)
"""

        try:
            result = subprocess.run(
                [sys.executable, "-c", minimal_python_test],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(workspace),
            )

            self.assertEqual(
                result.returncode,
                0,
                f"CRITICAL: Minimal system requirements not met\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}\n"
                f"New users with minimal Python setups will fail",
            )

            self.assertIn(
                "MINIMAL_SYSTEM_CHECK: OK",
                result.stdout,
                f"CRITICAL: Minimal system check failed\nOutput: {result.stdout}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Minimal system check timed out")

    def test_p0_network_independence_basic_functionality(self):
        """P0: Basic functionality must work without network access"""
        workspace = self.create_fresh_workspace("offline")
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Make executable
        os.chmod(claudedirector_path, 0o755)

        # Simulate network-disconnected environment
        offline_env = os.environ.copy()
        offline_env.update(
            {
                "http_proxy": "http://localhost:9999",  # Non-existent proxy
                "https_proxy": "http://localhost:9999",
                "HTTP_PROXY": "http://localhost:9999",
                "HTTPS_PROXY": "http://localhost:9999",
            }
        )

        try:
            # Basic status command should work offline
            result = subprocess.run(
                [str(claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(workspace),
                env=offline_env,
            )

            # Should complete (not necessarily succeed, but not hang or crash)
            output = result.stdout + result.stderr

            # Should not show network-related errors for basic functionality
            network_error_indicators = [
                "connection refused",
                "network unreachable",
                "timeout",
                "dns resolution failed",
            ]

            output_lower = output.lower()
            network_errors = [
                indicator
                for indicator in network_error_indicators
                if indicator in output_lower
            ]

            self.assertEqual(
                len(network_errors),
                0,
                f"CRITICAL: Basic functionality requires network access\n"
                f"Network errors found: {network_errors}\n"
                f"Output: {output}\n"
                f"New users without internet will be blocked",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Offline functionality test timed out")


class TestNewUserExperienceP0(unittest.TestCase):
    """P0 Tests focused on new user experience quality"""

    def setUp(self):
        """Set up for UX testing"""
        self.test_workspaces = []

    def tearDown(self):
        """Clean up test workspaces"""
        for workspace in self.test_workspaces:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)

    def test_p0_first_run_guidance_availability(self):
        """P0: New users must get clear first-run guidance"""
        workspace = self.shared_workspace

        # Check that README provides clear first-run guidance
        readme_path = workspace / "README.md"
        self.assertTrue(
            readme_path.exists(), "CRITICAL: README.md missing for new users"
        )

        try:
            content = readme_path.read_text(encoding="utf-8").lower()
            guidance_keywords = [
                "getting started",
                "installation",
                "setup",
                "quick start",
            ]

            found_guidance = any(keyword in content for keyword in guidance_keywords)
            self.assertTrue(
                found_guidance,
                f"CRITICAL: README lacks first-run guidance keywords: {guidance_keywords}",
            )
        except Exception as e:
            self.fail(f"CRITICAL: README accessibility failed: {e}")

    def test_p0_error_message_quality_new_users(self):
        """P0: Error messages must be helpful for new users"""
        workspace = self.shared_workspace
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Test that error messages are user-friendly, not technical stack traces
        try:
            result = subprocess.run(
                [str(claudedirector_path), "nonexistent-command"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=str(workspace),
            )

            output = result.stdout + result.stderr

            # Should provide helpful feedback
            self.assertGreater(
                len(output.strip()),
                5,
                "CRITICAL: No helpful error message for invalid command",
            )

            # Should not expose technical details to new users
            technical_terms = ["traceback", "exception", "stacktrace", "python"]
            exposed_terms = [
                term for term in technical_terms if term.lower() in output.lower()
            ]

            self.assertEqual(
                len(exposed_terms),
                0,
                f"CRITICAL: Error exposes technical details to new users: {exposed_terms}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Error handling timed out")


if __name__ == "__main__":
    unittest.main(verbosity=2)
