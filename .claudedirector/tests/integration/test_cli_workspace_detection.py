"""
Integration tests for CLI workspace detection
Tests the critical fix for dynamic workspace path resolution
"""

import pytest
import tempfile
import os
import subprocess
import sys
from pathlib import Path


class TestCLIWorkspaceDetection:
    """Test CLI workspace detection functionality"""

    def test_cli_workspace_detection_with_env_var(self):
        """Test CLI respects CLAUDEDIRECTOR_WORKSPACE environment variable"""

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "test-workspace"
            workspace_path.mkdir()
            reports_dir = workspace_path / "reports"
            reports_dir.mkdir()

            # Set environment variable
            env = os.environ.copy()
            env["CLAUDEDIRECTOR_WORKSPACE"] = str(workspace_path)

            # Run CLI command
            result = subprocess.run(
                [sys.executable, "./claudedirector", "reports", "weekly", "--dry-run"],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path.cwd()),
            )

            # Should not error and should reference correct workspace
            assert result.returncode == 0, f"CLI failed: {result.stderr}"
            assert "test-workspace/reports" in result.stdout

    def test_cli_detects_leadership_workspace(self):
        """Test CLI detects leadership-workspace when it exists"""

        # Create leadership-workspace in home directory
        leadership_workspace = Path.home() / "leadership-workspace"
        reports_dir = leadership_workspace / "reports"

        # Clean up any existing test artifacts
        if leadership_workspace.exists():
            import shutil

            shutil.rmtree(leadership_workspace, ignore_errors=True)

        try:
            leadership_workspace.mkdir(exist_ok=True)
            reports_dir.mkdir(exist_ok=True)

            # Run CLI without environment variable
            env = os.environ.copy()
            env.pop("CLAUDEDIRECTOR_WORKSPACE", None)

            result = subprocess.run(
                [sys.executable, "./claudedirector", "reports", "weekly", "--dry-run"],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path.cwd()),
            )

            # Should detect leadership-workspace
            assert result.returncode == 0, f"CLI failed: {result.stderr}"
            assert "leadership-workspace/reports" in result.stdout

        finally:
            # Clean up test workspace
            if leadership_workspace.exists():
                import shutil

                shutil.rmtree(leadership_workspace, ignore_errors=True)

    def test_cli_detects_legacy_workspace(self):
        """Test CLI detects leadership-workspace (legacy support)"""

        # Ensure leadership-workspace doesn't exist for this test
        leadership_workspace = Path.home() / "leadership-workspace"
        if leadership_workspace.exists():
            import shutil

            shutil.rmtree(leadership_workspace, ignore_errors=True)

        # Create legacy workspace
        legacy_workspace = Path.home() / "leadership-workspace"
        reports_dir = legacy_workspace / "reports"

        try:
            legacy_workspace.mkdir(exist_ok=True)
            reports_dir.mkdir(exist_ok=True)

            # Run CLI without environment variable
            env = os.environ.copy()
            env.pop("CLAUDEDIRECTOR_WORKSPACE", None)

            result = subprocess.run(
                [sys.executable, "./claudedirector", "reports", "weekly", "--dry-run"],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path.cwd()),
            )

            # Should detect legacy workspace
            assert result.returncode == 0, f"CLI failed: {result.stderr}"
            assert "leadership-workspace/reports" in result.stdout

        finally:
            # Clean up test workspace
            if legacy_workspace.exists():
                import shutil

                shutil.rmtree(legacy_workspace, ignore_errors=True)

    def test_cli_no_hardcoded_paths(self):
        """Test CLI doesn't contain hardcoded workspace paths"""

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a uniquely named workspace
            unique_workspace = Path(temp_dir) / "unique-test-workspace-12345"
            unique_workspace.mkdir()
            reports_dir = unique_workspace / "reports"
            reports_dir.mkdir()

            # Set environment variable to unique workspace
            env = os.environ.copy()
            env["CLAUDEDIRECTOR_WORKSPACE"] = str(unique_workspace)

            # Run CLI command
            result = subprocess.run(
                [sys.executable, "./claudedirector", "reports", "weekly", "--dry-run"],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(Path.cwd()),
            )

            # Should reference the unique workspace name, not hardcoded paths
            assert result.returncode == 0, f"CLI failed: {result.stderr}"
            assert "unique-test-workspace-12345/reports" in result.stdout

            # Should NOT contain hardcoded references
            assert (
                "leadership-workspace/reports" not in result.stdout
                or env["CLAUDEDIRECTOR_WORKSPACE"] in result.stdout
            )

    def test_workspace_file_handler_integration(self):
        """Test WorkspaceFileHandler integrates with CLI properly"""

        import sys

        sys.path.insert(0, ".claudedirector/lib")

        from lib.core.workspace_file_handler import WorkspaceFileHandler

        # Test workspace detection
        handler = WorkspaceFileHandler()

        # Should detect a workspace path
        assert handler.workspace_path is not None
        assert Path(handler.workspace_path).exists()

        # Should have integrated lifecycle manager
        assert hasattr(handler, "lifecycle_manager")
        assert handler.lifecycle_manager is not None

        # Should have integrated smart organizer
        assert hasattr(handler, "smart_organizer")
        assert handler.smart_organizer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
