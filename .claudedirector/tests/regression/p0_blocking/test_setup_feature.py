#!/usr/bin/env python3
"""
P0 Mandatory Tests for ClaudeDirector Setup Feature - CURSOR-FIRST ARCHITECTURE
==============================================================================

CRITICAL: These tests are P0 and MUST pass for every commit.
Failure = Broken setup experience for new users = Product failure

Test Coverage (Cursor-First):
- Setup database tool execution reliability
- ClaudeDirector module import functionality
- Core configuration system setup
- Cursor integration readiness validation
- Error recovery for setup failures

Architecture: Tests reflect actual user experience (Cursor-first, not CLI)
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
    """P0 Critical Setup Feature Tests - Cursor-First Architecture"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment with proper project root detection"""
        # Find project root by looking for .claudedirector directory with expected structure
        current_dir = Path(__file__).parent
        project_root = None

        for parent in current_dir.parents:
            claudedir = parent / ".claudedirector"
            # Check if this is the real project root by verifying expected structure
            if (
                claudedir.is_dir()
                and (claudedir / "lib").is_dir()
                and (claudedir / "tools").is_dir()
            ):
                project_root = parent
                break

        if not project_root:
            raise RuntimeError(
                "Cannot find project root - .claudedirector directory with lib and tools not found"
            )

        cls.project_root = project_root
        cls.setup_database_path = (
            project_root / ".claudedirector" / "tools" / "ci" / "init-database.py"
        )

    def test_p0_setup_database_tool_exists(self):
        """P0: init-database.py must exist and be executable"""
        self.assertTrue(
            self.setup_database_path.exists(),
            f"CRITICAL: init-database.py not found at {self.setup_database_path}",
        )

        # Verify it's a Python file
        self.assertTrue(
            self.setup_database_path.suffix == ".py",
            f"CRITICAL: init-database.py is not a Python file",
        )

    def test_p0_setup_database_help_execution(self):
        """P0: init-database.py must show help without errors"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.setup_database_path), "--help"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.project_root),
            )

            # Should execute successfully
            self.assertEqual(
                result.returncode,
                0,
                f"CRITICAL: init-database.py --help failed. STDERR: {result.stderr}",
            )

            # Should show database initialization message
            self.assertIn(
                "database",
                result.stdout.lower(),
                "CRITICAL: init-database.py doesn't show database initialization",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: init-database.py --help timed out")

    def test_p0_claudedirector_core_imports(self):
        """P0: Core ClaudeDirector modules must be importable for Cursor integration"""
        # Add project lib to path temporarily
        lib_path = str(self.project_root / ".claudedirector" / "lib")
        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)

        try:
            # Test critical imports that Cursor integration requires
            from core.config import ClaudeDirectorConfig

            # Basic instantiation test
            config = ClaudeDirectorConfig()
            self.assertIsNotNone(
                config, "CRITICAL: ClaudeDirectorConfig instantiation failed"
            )

        except ImportError as e:
            self.fail(
                f"CRITICAL: Core module import failed - breaks Cursor integration: {e}"
            )
        finally:
            # Clean up sys.path
            if lib_path in sys.path:
                sys.path.remove(lib_path)

    def test_p0_project_structure_integrity(self):
        """P0: Essential project structure must exist for setup"""
        critical_paths = [
            self.project_root / ".claudedirector",
            self.project_root / ".claudedirector" / "lib",
            self.project_root / ".claudedirector" / "tools",
            self.project_root / ".claudedirector" / "tools" / "setup",
        ]

        for path in critical_paths:
            self.assertTrue(
                path.exists(), f"CRITICAL: Essential directory missing: {path}"
            )

    def test_p0_configuration_system_readiness(self):
        """P0: Configuration system must be ready for Cursor integration"""
        lib_path = str(self.project_root / ".claudedirector" / "lib")
        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)

        try:
            from core.config import ClaudeDirectorConfig

            # Test configuration instantiation
            config = ClaudeDirectorConfig()

            # Test basic configuration methods exist
            self.assertTrue(
                hasattr(config, "get"),
                "CRITICAL: Configuration system missing get method",
            )

        except Exception as e:
            self.fail(
                f"CRITICAL: Configuration system not ready for Cursor integration: {e}"
            )
        finally:
            if lib_path in sys.path:
                sys.path.remove(lib_path)

    def test_p0_python_environment_compatibility(self):
        """P0: Current Python environment must support ClaudeDirector"""
        # Test Python version compatibility
        self.assertGreaterEqual(
            sys.version_info[:2],
            (3, 8),
            "CRITICAL: Python 3.8+ required for ClaudeDirector",
        )

        # Test essential modules are available
        essential_modules = ["pathlib", "subprocess", "json", "yaml"]
        for module in essential_modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"CRITICAL: Essential module not available: {module}")


if __name__ == "__main__":
    unittest.main()
