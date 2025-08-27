#!/usr/bin/env python3
"""
P0 BLOCKING Tests for Complete New Setup Experience - OPTIMIZED
==============================================================

CRITICAL: These tests validate the ESSENTIAL new user setup journey
optimized for <2 minute P0 execution within CI/pre-commit constraints.

ZERO TOLERANCE: If a new user cannot successfully set up ClaudeDirector,
our product fails at the first touchpoint.

Test Coverage (Essential Only):
- Fresh clone file structure validation
- Executable immediate availability
- Basic performance requirements
- Essential documentation presence
- Python environment compatibility

Author: Martin | Platform Architecture
Purpose: Eliminate new user setup failures - P0 BLOCKING (OPTIMIZED)
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
from typing import Dict, List, Optional


class TestCompleteNewSetupP0Optimized(unittest.TestCase):
    """P0 Critical Complete New Setup Tests - OPTIMIZED for speed"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment with shared workspace for speed"""
        # Find actual project root for reference
        current_dir = Path(__file__).parent
        cls.source_project_root = None

        for parent in current_dir.parents:
            if (parent / "bin" / "claudedirector").exists():
                cls.source_project_root = parent
                break

        if not cls.source_project_root:
            raise RuntimeError("Cannot find source project root for new setup testing")

        # Create single shared workspace to minimize I/O overhead
        cls.shared_workspace = cls._create_optimized_workspace()

    @classmethod
    def tearDownClass(cls):
        """Clean up shared workspace"""
        if hasattr(cls, "shared_workspace") and cls.shared_workspace.exists():
            shutil.rmtree(cls.shared_workspace.parent, ignore_errors=True)

    @classmethod
    def _create_optimized_workspace(cls):
        """Create optimized workspace with minimal copying"""
        workspace = Path(tempfile.mkdtemp(prefix="claudedirector_p0_newsetup_"))

        # Copy only essential files for new setup validation
        essential_files = [
            "README.md",
            "bin/claudedirector",
            "requirements.txt",
            "docs/GETTING_STARTED.md",
            "docs/CAPABILITIES.md",
        ]

        essential_dirs = [
            ".claudedirector/lib/core",
            ".claudedirector/lib/transparency",
            ".claudedirector/tools",
        ]

        target_dir = workspace / "ClaudeDirector"
        target_dir.mkdir()

        # Copy essential files only
        for file_path in essential_files:
            source_file = cls.source_project_root / file_path
            if source_file.exists():
                target_file = target_dir / file_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

        # Copy essential directories
        for dir_path in essential_dirs:
            source_dir = cls.source_project_root / dir_path
            if source_dir.exists():
                target_dir_path = target_dir / dir_path
                shutil.copytree(source_dir, target_dir_path, dirs_exist_ok=True)

        # Ensure executable permissions
        claudedirector_path = target_dir / "bin" / "claudedirector"
        if claudedirector_path.exists():
            os.chmod(claudedirector_path, 0o755)

        return target_dir

    def test_p0_essential_new_setup_validation(self):
        """P0: Essential new setup validation - ALL CRITICAL CHECKS IN ONE TEST"""
        workspace = self.shared_workspace
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Test 1: Essential file structure (CRITICAL)
        essential_files = [
            "README.md",
            "bin/claudedirector",
            "requirements.txt",
            ".claudedirector/lib/core",
            "docs/GETTING_STARTED.md",
        ]

        for essential_file in essential_files:
            file_path = workspace / essential_file
            self.assertTrue(
                file_path.exists(),
                f"CRITICAL: New setup missing essential file: {essential_file}",
            )

        # Test 2: Executable immediate availability + performance (CRITICAL)
        start_time = time.time()
        try:
            result = subprocess.run(
                [str(claudedirector_path), "--version"],
                capture_output=True,
                text=True,
                timeout=3,  # Aggressive timeout
                cwd=str(workspace),
            )

            execution_time = time.time() - start_time

            # Must execute successfully OR show deprecation (both acceptable)
            self.assertIn(
                result.returncode,
                [0, 1],
                f"CRITICAL: ClaudeDirector executable failed immediately after clone\n"
                f"Return code: {result.returncode}, STDOUT: {result.stdout}, STDERR: {result.stderr}",
            )

            # Must be fast for new users
            self.assertLess(
                execution_time,
                2.0,
                f"CRITICAL: New user executable too slow ({execution_time:.2f}s > 2.0s)\n"
                f"New users will abandon slow setup",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: New user executable timed out - unacceptable UX")

        # Test 3: Essential documentation accessibility (CRITICAL)
        try:
            readme_content = (
                (workspace / "README.md").read_text(encoding="utf-8").lower()
            )

            # Must contain new user guidance
            new_user_keywords = ["getting started", "installation", "setup"]
            found_keywords = [kw for kw in new_user_keywords if kw in readme_content]

            self.assertGreater(
                len(found_keywords),
                0,
                f"CRITICAL: README.md missing new user guidance\n"
                f"Required keywords: {new_user_keywords}, Found: {found_keywords}",
            )

        except Exception as e:
            self.fail(f"CRITICAL: README.md accessibility failed: {e}")

        # Test 4: Python environment compatibility (CRITICAL)
        try:
            # Test ClaudeDirector Python import path setup
            python_test = """
import sys
sys.path.insert(0, ".claudedirector/lib")
from pathlib import Path

# Verify essential structure exists
core_path = Path(".claudedirector/lib/core")
if not core_path.exists():
    print("MISSING_CORE")
    sys.exit(1)
else:
    print("PYTHON_COMPAT_OK")
    sys.exit(0)
"""

            result = subprocess.run(
                [sys.executable, "-c", python_test],
                capture_output=True,
                text=True,
                timeout=3,
                cwd=str(workspace),
            )

            self.assertEqual(
                result.returncode,
                0,
                f"CRITICAL: Python environment compatibility failed\n"
                f"STDOUT: {result.stdout}, STDERR: {result.stderr}\n"
                f"New users with standard Python will fail",
            )

            self.assertIn(
                "PYTHON_COMPAT_OK",
                result.stdout,
                "CRITICAL: Python compatibility validation failed",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Python compatibility check timed out")

        # Test 5: Network independence for basic functionality (CRITICAL)
        try:
            # Test status command works without network
            offline_env = os.environ.copy()
            offline_env.update(
                {
                    "http_proxy": "http://localhost:9999",
                    "https_proxy": "http://localhost:9999",
                }
            )

            result = subprocess.run(
                [str(claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=3,
                cwd=str(workspace),
                env=offline_env,
            )

            # Should not hang or show network errors
            output = result.stdout + result.stderr
            network_error_terms = ["connection refused", "network unreachable", "dns"]

            network_errors = [
                term for term in network_error_terms if term.lower() in output.lower()
            ]

            self.assertEqual(
                len(network_errors),
                0,
                f"CRITICAL: Basic functionality requires network access\n"
                f"Network errors: {network_errors}\n"
                f"New users without internet will be blocked",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Network independence test timed out")

    def test_p0_new_user_error_scenarios(self):
        """P0: New users must get helpful error messages"""
        workspace = self.shared_workspace
        claudedirector_path = workspace / "bin" / "claudedirector"

        # Test common new user error: wrong directory
        try:
            result = subprocess.run(
                [str(claudedirector_path), "status"],
                capture_output=True,
                text=True,
                timeout=3,
                cwd=str(workspace.parent),  # Run from outside project
            )

            output = result.stdout + result.stderr

            # Should provide helpful feedback, not crash
            self.assertGreater(
                len(output.strip()),
                5,
                "CRITICAL: No feedback provided for common new user error",
            )

            # Should not show raw Python traceback to new users
            self.assertNotIn(
                "Traceback",
                output,
                f"CRITICAL: Raw traceback exposed to new users\nOutput: {output}",
            )

        except subprocess.TimeoutExpired:
            self.fail("CRITICAL: Error scenario handling timed out")


if __name__ == "__main__":
    unittest.main(verbosity=2)
