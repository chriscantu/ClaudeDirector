#!/usr/bin/env python3
"""
P0 Mandatory Tests for ClaudeDirector Setup Feature
===================================================

CRITICAL: These tests are P0 and MUST pass for every commit.
Failure = Broken setup experience for new users = Product failure

Test Coverage:
- Setup command execution reliability
- Project root path detection accuracy
- Setup module import functionality
- Critical setup workflow completion
- Error recovery for setup failures
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil


class TestSetupP0(unittest.TestCase):
    """P0 Critical Setup Feature Tests - Zero tolerance for failure"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment with proper project root detection"""
        # Find project root by looking for bin/claudedirector
        current_dir = Path(__file__).parent
        project_root = None

        # Walk up the directory tree to find project root
        for parent in current_dir.parents:
            if (parent / "bin" / "claudedirector").exists():
                project_root = parent
                break

        if not project_root:
            raise RuntimeError(
                "Cannot find project root - bin/claudedirector not found"
            )

        cls.project_root = project_root
        cls.claudedirector_path = project_root / "bin" / "claudedirector"

        # Ensure claudedirector is executable
        if not os.access(cls.claudedirector_path, os.X_OK):
            os.chmod(cls.claudedirector_path, 0o755)

    def test_p0_claudedirector_executable_exists(self):
        """P0: claudedirector executable must exist and be executable"""
        self.assertTrue(
            self.claudedirector_path.exists(),
            f"CRITICAL: claudedirector executable not found at {self.claudedirector_path}",
        )

        self.assertTrue(
            os.access(self.claudedirector_path, os.X_OK),
            f"CRITICAL: claudedirector not executable at {self.claudedirector_path}",
        )

    def test_p0_setup_command_shows_deprecation(self):
        """P0: CLI must show deprecation notice (CLI deprecated in v3.0.0)"""
        try:
            result = subprocess.run(
                [str(self.claudedirector_path), "setup", "--help"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.project_root),
            )

            # CLI should exit with code 1 (deprecated)
            self.assertEqual(
                result.returncode,
                1,
                f"CRITICAL: CLI should exit with code 1 (deprecated). "
                f"Got code {result.returncode}. STDOUT: {result.stdout}. STDERR: {result.stderr}",
            )

            # Must contain deprecation information
            output = result.stdout + result.stderr
            self.assertTrue(
                any(
                    keyword in output.lower()
                    for keyword in ["deprecated", "cursor", "v3.0.0"]
                ),
                f"CRITICAL: CLI must show deprecation notice. Output: {output}",
            )

            # Must mention Cursor integration
            self.assertIn(
                "Cursor",
                output,
                f"CRITICAL: Deprecation notice must mention Cursor integration. Output: {output}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: CLI deprecation command timed out after 30 seconds")
        except Exception as e:
            self.fail(f"CRITICAL: CLI deprecation check failed with exception: {e}")

    def test_p0_alternative_setup_available(self):
        """P0: Alternative setup methods must be available (direct tools)"""
        # Since CLI is deprecated, test that direct setup tools exist
        setup_tools_dir = self.project_root / ".claudedirector" / "tools" / "setup"

        self.assertTrue(
            setup_tools_dir.exists(),
            f"CRITICAL: Setup tools directory not found at {setup_tools_dir}",
        )

        # Check for at least one setup script
        setup_scripts = list(setup_tools_dir.glob("setup_*.py"))
        self.assertGreater(
            len(setup_scripts),
            0,
            f"CRITICAL: No setup scripts found in {setup_tools_dir}",
        )

        # Test one of the setup scripts works
        setup_script = setup_scripts[0]  # Use the first available setup script
        try:
            result = subprocess.run(
                [sys.executable, str(setup_script)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.project_root),
            )

            # Should run without critical errors (0 = success, or other acceptable codes)
            self.assertNotEqual(
                result.returncode,
                126,  # Permission denied
                f"CRITICAL: Setup script not executable. "
                f"Exit code: {result.returncode}. STDOUT: {result.stdout}. STDERR: {result.stderr}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Setup script timed out")
        except Exception as e:
            self.fail(f"CRITICAL: Setup script execution failed: {e}")

    def test_p0_project_root_detection_accuracy(self):
        """P0: Project root detection must be accurate from various locations"""
        # Test from different subdirectories
        test_directories = [
            self.project_root,  # Project root
            self.project_root / ".claudedirector",  # Framework dir
            self.project_root / ".claudedirector" / "lib",  # Lib dir
            self.project_root / "leadership-workspace",  # Workspace dir
        ]

        for test_dir in test_directories:
            if not test_dir.exists():
                continue

            with self.subTest(directory=str(test_dir)):
                try:
                    result = subprocess.run(
                        [str(self.claudedirector_path), "status"],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        cwd=str(test_dir),
                    )

                    # Should not fail due to import errors
                    self.assertNotIn(
                        "ModuleNotFoundError",
                        result.stderr,
                        f"CRITICAL: Import error from {test_dir}\n"
                        f"STDERR: {result.stderr}",
                    )

                    self.assertNotIn(
                        "ImportError",
                        result.stderr,
                        f"CRITICAL: Import error from {test_dir}\n"
                        f"STDERR: {result.stderr}",
                    )

                except subprocess.TimeoutExpired:
                    self.fail(f"CRITICAL: status command timed out from {test_dir}")

    def test_p0_setup_modules_importable(self):
        """P0: All setup modules must be importable without errors"""
        setup_module_paths = [
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_meeting_intelligence.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_smart_git.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_stakeholder_management.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_task_tracking.py",
        ]

        for module_path in setup_module_paths:
            with self.subTest(module=module_path.name):
                # Test that modules can be executed directly
                try:
                    result = subprocess.run(
                        [sys.executable, str(module_path), "--help"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=str(self.project_root),
                    )

                    # Module should execute without import errors
                    self.assertNotIn(
                        "ModuleNotFoundError",
                        result.stderr,
                        f"CRITICAL: {module_path.name} has import errors:\n{result.stderr}",
                    )

                    self.assertNotIn(
                        "ImportError",
                        result.stderr,
                        f"CRITICAL: {module_path.name} has import errors:\n{result.stderr}",
                    )

                    # Should show help or setup information
                    self.assertTrue(
                        result.returncode in [0, 1, 2],  # Allow various help exit codes
                        f"CRITICAL: {module_path.name} failed to execute basic functionality",
                    )

                except subprocess.TimeoutExpired:
                    self.fail(f"CRITICAL: {module_path.name} execution timed out")
                except Exception as e:
                    self.fail(f"CRITICAL: {module_path.name} execution failed: {e}")

    def test_p0_setup_status_command_deprecated(self):
        """P0: Status command must show deprecation notice (CLI deprecated)"""
        try:
            result = subprocess.run(
                [str(self.claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(self.project_root),
            )

            # Status command should show deprecation (exit code 1)
            self.assertEqual(
                result.returncode,
                1,
                f"CRITICAL: status command should show deprecation (exit code 1)\n"
                f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}",
            )

            # Status output must contain deprecation information
            output = result.stdout + result.stderr
            self.assertIn(
                "deprecated",
                output.lower(),
                f"CRITICAL: Status command must show deprecation notice. Output: {output}",
            )

            # Must mention Cursor as alternative
            self.assertIn(
                "Cursor",
                output,
                f"CRITICAL: Must mention Cursor as alternative. Output: {output}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: status command timed out after 15 seconds")

    def test_p0_setup_directory_structure_integrity(self):
        """P0: Required setup directory structure must exist"""
        required_paths = [
            self.project_root / ".claudedirector",
            self.project_root / ".claudedirector" / "lib",
            self.project_root / ".claudedirector" / "tools",
            self.project_root / ".claudedirector" / "tools" / "setup",
            self.project_root / "data",
            self.project_root / "data" / "strategic",
        ]

        for required_path in required_paths:
            with self.subTest(path=str(required_path)):
                self.assertTrue(
                    required_path.exists(),
                    f"CRITICAL: Required setup directory missing: {required_path}",
                )

    def test_p0_setup_file_permissions(self):
        """P0: Setup scripts must have correct permissions"""
        setup_scripts = [
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_meeting_intelligence.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_smart_git.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_stakeholder_management.py",
            self.project_root
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_task_tracking.py",
        ]

        for script_path in setup_scripts:
            with self.subTest(script=script_path.name):
                self.assertTrue(
                    script_path.exists(),
                    f"CRITICAL: Setup script missing: {script_path}",
                )

                # Check readable
                self.assertTrue(
                    os.access(script_path, os.R_OK),
                    f"CRITICAL: Setup script not readable: {script_path}",
                )

    def test_p0_setup_commands_deprecated(self):
        """P0: All CLI commands must show deprecation notice (CLI deprecated)"""
        test_commands = ["setup", "status", "meetings", "stakeholders", "tasks"]

        for command in test_commands:
            with self.subTest(command=command):
                try:
                    result = subprocess.run(
                        [str(self.claudedirector_path), command, "--help"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=str(self.project_root),
                    )

                    # All commands should now show deprecation (exit code 1)
                    self.assertEqual(
                        result.returncode,
                        1,
                        f"CRITICAL: {command} should show deprecation notice (exit code 1)\n"
                        f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}",
                    )

                    # Must contain deprecation information
                    output = result.stdout + result.stderr
                    self.assertIn(
                        "deprecated",
                        output.lower(),
                        f"CRITICAL: {command} must show deprecation notice",
                    )

                except subprocess.TimeoutExpired:
                    self.fail(f"CRITICAL: {command} --help timed out")

    def test_p0_setup_error_recovery(self):
        """P0: Setup must handle common error conditions gracefully"""
        # Test with missing database directory
        with tempfile.TemporaryDirectory() as temp_dir:
            test_workspace = Path(temp_dir) / "test_workspace"
            test_workspace.mkdir()

            # Copy minimal claudedirector structure
            test_claudedirector = test_workspace / "bin" / "claudedirector"
            test_claudedirector.parent.mkdir(parents=True)
            shutil.copy2(self.claudedirector_path, test_claudedirector)

            try:
                result = subprocess.run(
                    [str(test_claudedirector), "status"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(test_workspace),
                )

                # Should not crash, even with missing components
                # Exit code may be non-zero, but should not crash
                self.assertNotIn(
                    "Traceback",
                    result.stderr,
                    f"CRITICAL: Setup crashed with traceback:\n{result.stderr}",
                )

            except subprocess.TimeoutExpired:
                self.fail("CRITICAL: Error recovery test timed out")

    def test_p0_setup_performance_requirements(self):
        """P0: Setup commands must meet performance requirements"""
        import time

        # Status command should complete within 5 seconds
        start_time = time.time()

        try:
            result = subprocess.run(
                [str(self.claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.project_root),
            )

            execution_time = time.time() - start_time

            self.assertLess(
                execution_time,
                5.0,
                f"CRITICAL: Status command too slow ({execution_time:.2f}s > 5.0s limit)\n"
                f"User experience requirement: <5s for status checks",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Status command exceeded timeout")

    def test_p0_setup_python_environment_compatibility(self):
        """P0: Setup must work with current Python environment"""
        # Test that setup works with current Python version and environment
        try:
            result = subprocess.run(
                [sys.executable, str(self.claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.project_root),
            )

            # Should work with current Python interpreter
            self.assertNotIn(
                "SyntaxError",
                result.stderr,
                f"CRITICAL: Python syntax compatibility issue:\n{result.stderr}",
            )

            self.assertNotIn(
                "version",
                result.stderr.lower(),
                f"CRITICAL: Python version compatibility issue:\n{result.stderr}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Python environment compatibility test timed out")


class TestSetupP0RegressionProtection(unittest.TestCase):
    """P0 Regression Protection for Setup Feature"""

    def test_p0_setup_regression_project_root_calculation(self):
        """P0 Regression: Project root calculation must be correct"""
        # This test specifically protects against the bug we just fixed

        # Simulate the bug condition by checking path calculation logic
        from pathlib import Path

        # Test the correct path calculation (what should happen)
        claudedirector_script = Path(__file__).parents[3] / "bin" / "claudedirector"
        if claudedirector_script.exists():
            # Read the script and verify project_root calculation
            with open(claudedirector_script, "r") as f:
                script_content = f.read()

            # Verify the fix is in place
            self.assertIn(
                "parent.parent",
                script_content,
                "CRITICAL REGRESSION: Project root calculation reverted to broken state!\n"
                "The bug fix for project_root = Path(__file__).parent.parent must be maintained",
            )

            # Verify old broken pattern is not present
            self.assertNotIn(
                "Path(__file__).parent\n",  # Single parent (the bug)
                script_content,
                "CRITICAL REGRESSION: Broken single parent path calculation detected!",
            )

    def test_p0_setup_regression_import_path_resolution(self):
        """P0 Regression: Import path resolution must work from setup modules"""
        # Test that the sys.path.insert fix is maintained in setup modules

        setup_module_paths = [
            Path(__file__).parents[3]
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_meeting_intelligence.py",
            Path(__file__).parents[3]
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_smart_git.py",
            Path(__file__).parents[3]
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_stakeholder_management.py",
            Path(__file__).parents[3]
            / ".claudedirector"
            / "tools"
            / "setup"
            / "setup_task_tracking.py",
        ]

        for module_path in setup_module_paths:
            if module_path.exists():
                with self.subTest(module=module_path.name):
                    with open(module_path, "r") as f:
                        module_content = f.read()

                    # Verify correct path calculation pattern exists
                    self.assertIn(
                        "parent.parent.parent.parent",
                        module_content,
                        f"CRITICAL REGRESSION: {module_path.name} missing correct path calculation!\n"
                        f"Must have: project_root = Path(__file__).parent.parent.parent.parent",
                    )

                    # Verify sys.path.insert for imports
                    self.assertIn(
                        "sys.path.insert(0, str(lib_path))",
                        module_content,
                        f"CRITICAL REGRESSION: {module_path.name} missing import path fix!",
                    )


if __name__ == "__main__":
    # Run P0 tests with immediate failure reporting
    unittest.main(verbosity=2, failfast=True)
