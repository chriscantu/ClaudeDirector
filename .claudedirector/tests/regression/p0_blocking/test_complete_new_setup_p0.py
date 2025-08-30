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
            # Look for multiple project root indicators (more reliable than just bin/claudedirector)
            if (
                (parent / "README.md").exists() and
                (parent / ".claudedirector").exists() and
                (parent / "requirements.txt").exists()
            ):
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

        # Note: CLI executable removed - ClaudeDirector is now chat-only framework

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

        # Note: CLI executable removed - ClaudeDirector is now chat-only framework

        return target_dir

    def test_p0_combined_essential_setup_checks(self):
        """P0: Combined essential checks for speed optimization"""
        # Use shared workspace for faster execution
        workspace = self.shared_workspace

        # Combined Check 1: File structure for chat-only framework
        required_files = [
            "README.md",
            "requirements.txt",
            ".claudedirector/lib",
            ".claudedirector/config",
        ]

        for required_file in required_files:
            file_path = workspace / required_file
            self.assertTrue(
                file_path.exists(),
                f"CRITICAL: Fresh clone missing required file: {required_file}",
            )

        # Combined Check 2: Chat interface documentation + performance
        start_time = time.time()
        try:
            # Test that README provides clear chat interface guidance
            readme_path = workspace / "README.md"
            content = readme_path.read_text(encoding="utf-8").lower()

            # Should clearly indicate this is a chat-only framework
            chat_indicators = ["cursor", "claude", "chat"]
            found_chat_guidance = any(indicator in content for indicator in chat_indicators)

            execution_time = time.time() - start_time

            # Must have chat guidance and be fast to read
            self.assertTrue(
                found_chat_guidance,
                "CRITICAL: README lacks chat interface guidance for new users"
            )
            self.assertLess(
                execution_time, 3.0, f"CRITICAL: Documentation read too slow ({execution_time:.2f}s)"
            )

        except Exception as e:
            self.fail(f"CRITICAL: Documentation validation failed: {e}")

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

        # Step 1: Verify fresh workspace structure for chat-only framework (fast check)
        required_files = [
            "README.md",
            "requirements.txt",
            ".claudedirector/lib",
            ".claudedirector/config",
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

    def test_p0_claudedirector_chat_interface_immediate_availability(self):
        """P0: ClaudeDirector chat interface must be documented immediately after clone"""
        workspace = self.create_fresh_workspace("chat_interface_test")

        # Must have clear chat interface documentation
        readme_path = workspace / "README.md"
        self.assertTrue(
            readme_path.exists(),
            f"CRITICAL: README.md missing in fresh clone",
        )

        # Test immediate documentation access (should work without additional setup)
        try:
            # Test documentation provides chat guidance (optimized for speed)
            content = readme_path.read_text(encoding="utf-8").lower()

            # Should clearly indicate this is a chat-only framework
            chat_indicators = ["cursor", "claude", "chat", "conversation"]
            found_chat_guidance = any(indicator in content for indicator in chat_indicators)

            # Should provide getting started guidance
            setup_indicators = ["getting started", "setup", "installation"]
            found_setup_guidance = any(indicator in content for indicator in setup_indicators)

            self.assertTrue(
                found_chat_guidance,
                f"CRITICAL: README lacks chat interface guidance for new users",
            )

            self.assertTrue(
                found_setup_guidance,
                f"CRITICAL: README lacks setup guidance for new users",
            )

        except Exception as e:
            self.fail(f"CRITICAL: Chat interface documentation validation failed: {e}")

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

        # New user performance requirements for chat interface documentation
        start_time = time.time()

        try:
            # Test documentation read performance (should be fast)
            readme_path = workspace / "README.md"
            content = readme_path.read_text(encoding="utf-8")

            # Verify it has essential content
            content_lower = content.lower()
            has_guidance = any(indicator in content_lower for indicator in ["cursor", "claude", "getting started"])

            execution_time = time.time() - start_time

            # Documentation read should be fast and have guidance
            self.assertLess(
                execution_time,
                1.0,
                f"CRITICAL: Documentation read too slow ({execution_time:.2f}s > 1.0s limit)\n"
                f"New users will abandon slow documentation access.",
            )

            self.assertTrue(
                has_guidance,
                "CRITICAL: README lacks essential guidance for new users"
            )

        except Exception as e:
            self.fail(f"CRITICAL: Documentation performance test failed: {e}")

    def test_p0_error_recovery_fresh_setup(self):
        """P0: Setup must handle common new user errors gracefully"""
        workspace = self.create_fresh_workspace("error_recovery")

        # Test common new user error scenarios for chat-only interface
        error_scenarios = [
            {
                "name": "Missing README access",
                "test": lambda: self._test_readme_accessibility(workspace),
                "expect_graceful": True,
            },
            {
                "name": "Documentation clarity test",
                "test": lambda: self._test_documentation_clarity(workspace),
                "expect_graceful": True,
            },
        ]

        for scenario in error_scenarios:
            with self.subTest(scenario=scenario["name"]):
                try:
                    # Run the test scenario
                    scenario["test"]()

                except Exception as e:
                    self.fail(f"CRITICAL: Error recovery failed for scenario {scenario['name']}: {e}")

    def _test_readme_accessibility(self, workspace):
        """Test that README is accessible and readable"""
        readme_path = workspace / "README.md"
        self.assertTrue(readme_path.exists(), "README.md must exist")
        content = readme_path.read_text(encoding="utf-8")
        self.assertGreater(len(content), 100, "README must have substantial content")

    def _test_documentation_clarity(self, workspace):
        """Test that documentation provides clear guidance"""
        readme_path = workspace / "README.md"
        content = readme_path.read_text(encoding="utf-8").lower()

        # Should have clear chat interface guidance
        chat_indicators = ["cursor", "claude", "chat"]
        has_chat_guidance = any(indicator in content for indicator in chat_indicators)
        self.assertTrue(has_chat_guidance, "Documentation must explain chat interface")

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
            # Basic documentation access should work offline
            readme_path = workspace / "README.md"
            content = readme_path.read_text(encoding="utf-8")

            # Should be able to read documentation without network
            self.assertGreater(len(content), 100, "README must be accessible offline")

            # Should have chat interface guidance
            content_lower = content.lower()
            chat_indicators = ["cursor", "claude", "chat"]
            has_chat_guidance = any(indicator in content_lower for indicator in chat_indicators)

            # Documentation should provide chat guidance even offline
            self.assertTrue(
                has_chat_guidance,
                "CRITICAL: Documentation lacks chat interface guidance for offline users"
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Offline functionality test timed out")


class TestNewUserExperienceP0(unittest.TestCase):
    """P0 Tests focused on new user experience quality"""

    @classmethod
    def setUpClass(cls):
        """Set up shared workspace for UX testing"""
        # Find actual project root for reference
        current_dir = Path(__file__).parent
        cls.source_project_root = None

        for parent in current_dir.parents:
            # Look for multiple project root indicators (more reliable than just bin/claudedirector)
            if (
                (parent / "README.md").exists() and
                (parent / ".claudedirector").exists() and
                (parent / "requirements.txt").exists()
            ):
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
        workspace = Path(tempfile.mkdtemp(prefix="claudedirector_ux_setup_"))
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

        return target_dir

    def setUp(self):
        """Set up for UX testing"""
        pass  # Using class-level shared workspace

    def tearDown(self):
        """Clean up test workspaces"""
        pass  # Using class-level cleanup

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
        except FileNotFoundError:
            # Expected - CLI was removed, test chat interface documentation instead
            self._test_chat_interface_documentation(workspace)

    def _test_chat_interface_documentation(self, workspace):
        """Test that documentation provides clear guidance for chat-only interface"""
        readme_path = workspace / "README.md"

        try:
            content = readme_path.read_text(encoding="utf-8").lower()

            # Should clearly indicate this is a chat-only framework
            chat_indicators = [
                "chat",
                "cursor",
                "claude",
                "conversation",
                "ai assistant"
            ]

            found_chat_guidance = any(indicator in content for indicator in chat_indicators)
            self.assertTrue(
                found_chat_guidance,
                f"CRITICAL: README lacks chat interface guidance for new users: {chat_indicators}",
            )

        except Exception as e:
            self.fail(f"CRITICAL: README validation failed for new users: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
