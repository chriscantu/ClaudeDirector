#!/usr/bin/env python3
"""
Unit tests for CLI Customization
Testing P1 Organizational Intelligence CLI interface
"""

import pytest
import yaml
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

# Import the modules under test
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from lib.claudedirector.p1_features.organizational_intelligence.cli_customization import (
    org_intelligence,
    setup,
    customize,
    configure_domain,
    status,
    quick_setup,
)


class TestOrgIntelligenceCLI:
    """Test main CLI group"""

    def test_org_intelligence_group_exists(self):
        """Test that the main CLI group exists and is callable"""
        runner = CliRunner()
        result = runner.invoke(org_intelligence, ["--help"])
        assert result.exit_code == 0
        assert (
            "Organizational Leverage Intelligence configuration commands"
            in result.output
        )


class TestSetupCommand:
    """Test setup command functionality"""

    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing"""
        return {
            "director_profile": {"profile_type": "platform_director"},
            "organizational_intelligence": {
                "velocity_tracking": {"measurement_domains": {}}
            },
        }

    @pytest.fixture
    def temp_config_file(self, sample_config):
        """Create temporary config file"""
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)

        config_path = config_dir / "p1_organizational_intelligence.yaml"
        with open(config_path, "w") as f:
            yaml.dump(sample_config, f)

        yield str(config_path)

        # Cleanup
        if config_path.exists():
            config_path.unlink()

    def test_setup_platform_director_preset(self, temp_config_file):
        """Test setup with platform director preset"""
        runner = CliRunner()

        result = runner.invoke(
            setup,
            [
                "--profile-type",
                "platform_director",
                "--role-title",
                "Test Director",
                "--primary-focus",
                "Test Focus",
            ],
        )

        assert result.exit_code == 0
        assert (
            "Setting up Organizational Intelligence for Test Director" in result.output
        )
        assert "Profile setup complete" in result.output

    def test_setup_custom_profile_non_interactive(self, temp_config_file):
        """Test setup with custom profile (non-interactive)"""
        runner = CliRunner()

        # Mock the interactive input for custom profile
        inputs = "\n\n\n\n"  # Empty inputs to exit loops

        result = runner.invoke(
            setup,
            [
                "--profile-type",
                "custom",
                "--role-title",
                "Custom Director",
                "--primary-focus",
                "Custom Focus",
            ],
            input=inputs,
        )

        assert result.exit_code == 0
        assert "Custom Profile Setup" in result.output

    def test_setup_backend_director_preset(self, temp_config_file):
        """Test setup with backend director preset"""
        runner = CliRunner()

        result = runner.invoke(
            setup,
            [
                "--profile-type",
                "backend_director",
                "--role-title",
                "Backend Director",
                "--primary-focus",
                "Backend Services",
            ],
        )

        assert result.exit_code == 0
        assert (
            "Setting up Organizational Intelligence for Backend Director"
            in result.output
        )

    def test_setup_updates_config_file(self, temp_config_file):
        """Test that setup actually updates the configuration file"""
        runner = CliRunner()

        # Run setup
        result = runner.invoke(
            setup,
            ["--profile-type", "product_director", "--role-title", "Product Director"],
        )

        assert result.exit_code == 0

        # Check that config file was updated
        with open(temp_config_file, "r") as f:
            updated_config = yaml.safe_load(f)

        assert updated_config["director_profile"]["profile_type"] == "product_director"


class TestStatusCommand:
    """Test status command functionality"""

    @pytest.fixture
    def mock_director_profile_manager(self):
        """Mock DirectorProfileManager for testing"""
        mock_manager = MagicMock()
        mock_profile = MagicMock()

        mock_profile.role_title = "Test Director"
        mock_profile.primary_focus = "Test Focus"
        mock_profile.enabled_domains = {
            "design_system_leverage": [MagicMock(weight=0.35)],
            "platform_adoption": [MagicMock(weight=0.30)],
        }
        mock_profile.investment_categories = {
            "design_enhancement": MagicMock(priority_weight=0.4),
            "platform_infra": MagicMock(priority_weight=0.6),
        }
        mock_profile.strategic_priorities = ["Priority 1", "Priority 2"]
        mock_profile.success_metrics = ["Metric 1", "Metric 2"]
        mock_profile.integration_preferences = {"github": True, "figma": False}

        mock_manager.current_profile = mock_profile
        return mock_manager

    @patch(
        "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
    )
    def test_status_command_output(
        self, mock_manager_class, mock_director_profile_manager
    ):
        """Test status command output format"""
        mock_manager_class.return_value = mock_director_profile_manager

        runner = CliRunner()
        result = runner.invoke(status)

        assert result.exit_code == 0
        assert "Organizational Intelligence Status" in result.output
        assert "Test Director" in result.output
        assert "Test Focus" in result.output
        assert "Enabled Measurement Domains (2)" in result.output
        assert "Investment Categories (2)" in result.output
        assert "Strategic Priorities" in result.output
        assert "Success Metrics" in result.output
        assert "Active Integrations (1)" in result.output


class TestCustomizeCommand:
    """Test customize command functionality"""

    @pytest.fixture
    def sample_config_with_domains(self):
        """Configuration with multiple domains for customization testing"""
        return {
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {
                            "enabled": True,
                            "weight": 0.35,
                            "metrics": ["component_usage"],
                            "targets": {"component": 0.8},
                        },
                        "api_service_efficiency": {
                            "enabled": False,
                            "weight": 0.0,
                            "metrics": ["response_time"],
                            "targets": {"response": 200},
                        },
                        "platform_adoption": {
                            "enabled": True,
                            "weight": 0.30,
                            "metrics": ["adoption_rate"],
                            "targets": {"adoption": 0.75},
                        },
                    }
                }
            }
        }

    @pytest.fixture
    def temp_config_for_customize(self, sample_config_with_domains):
        """Create temporary config file for customize testing"""
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)

        config_path = config_dir / "p1_organizational_intelligence.yaml"
        with open(config_path, "w") as f:
            yaml.dump(sample_config_with_domains, f)

        yield str(config_path)

        # Cleanup
        if config_path.exists():
            config_path.unlink()

    @patch(
        "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
    )
    def test_customize_command_basic_flow(
        self, mock_manager_class, temp_config_for_customize
    ):
        """Test customize command basic flow"""
        mock_manager = MagicMock()
        mock_profile = MagicMock()

        mock_profile.role_title = "Test Director"
        mock_profile.primary_focus = "Test Focus"
        mock_profile.enabled_domains = {"design_system_leverage": []}

        mock_manager.current_profile = mock_profile
        mock_manager.generate_executive_summary.return_value = {
            "director_profile": {"role": "Test Director"},
            "enabled_domains": ["design_system_leverage"],
        }

        mock_manager_class.return_value = mock_manager

        runner = CliRunner()

        # Simulate user saying no to all customizations
        inputs = "n\nn\n"

        result = runner.invoke(customize, input=inputs)

        assert result.exit_code == 0
        assert "Customizing profile for: Test Director" in result.output
        assert "Currently enabled measurement domains" in result.output


class TestConfigureDomainCommand:
    """Test configure domain command functionality"""

    @pytest.fixture
    def temp_config_for_domain_config(self):
        """Create config with domain configuration"""
        config = {
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {
                            "enabled": True,
                            "targets": {"consistency": 0.85, "adoption": 0.80},
                        }
                    }
                }
            }
        }

        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)

        config_path = config_dir / "p1_organizational_intelligence.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        yield str(config_path)

        # Cleanup
        if config_path.exists():
            config_path.unlink()

    @patch(
        "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
    )
    def test_configure_domain_specific(
        self, mock_manager_class, temp_config_for_domain_config
    ):
        """Test configuring a specific domain"""
        mock_manager = MagicMock()
        mock_profile = MagicMock()
        mock_profile.enabled_domains = {"design_system_leverage": []}
        mock_manager.current_profile = mock_profile
        mock_manager_class.return_value = mock_manager

        runner = CliRunner()

        # Simulate user saying no to updates
        inputs = "n\n"

        result = runner.invoke(
            configure_domain, ["--domain", "design_system_leverage"], input=inputs
        )

        assert result.exit_code == 0
        assert "Configuring design_system_leverage" in result.output
        assert "Current targets for design_system_leverage" in result.output

    @patch(
        "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
    )
    def test_configure_domain_not_enabled(
        self, mock_manager_class, temp_config_for_domain_config
    ):
        """Test configuring a domain that's not enabled"""
        mock_manager = MagicMock()
        mock_profile = MagicMock()
        mock_profile.enabled_domains = {}  # Empty - no domains enabled
        mock_manager.current_profile = mock_profile
        mock_manager_class.return_value = mock_manager

        runner = CliRunner()

        result = runner.invoke(configure_domain, ["--domain", "nonexistent_domain"])

        assert result.exit_code == 0
        assert "Domain nonexistent_domain is not enabled" in result.output


class TestQuickSetupCommand:
    """Test quick setup command functionality"""

    @pytest.fixture
    def temp_config_for_quick_setup(self):
        """Create config for quick setup testing"""
        config = {
            "director_profile": {"profile_type": "custom"},
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {"enabled": False, "weight": 0.0},
                        "platform_adoption": {"enabled": False, "weight": 0.0},
                        "developer_experience": {"enabled": False, "weight": 0.0},
                        "api_service_efficiency": {"enabled": False, "weight": 0.0},
                    }
                }
            },
        }

        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)

        config_path = config_dir / "p1_organizational_intelligence.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        yield str(config_path)

        # Cleanup
        if config_path.exists():
            config_path.unlink()

    def test_quick_setup_design_system_template(self, temp_config_for_quick_setup):
        """Test quick setup with design system template"""
        runner = CliRunner()

        result = runner.invoke(quick_setup, ["--template", "design_system"])

        assert result.exit_code == 0
        assert "Setting up with design_system template" in result.output
        assert "Director of Engineering - UI Foundation" in result.output
        assert "Quick setup complete" in result.output

        # Verify config was updated
        with open(temp_config_for_quick_setup, "r") as f:
            updated_config = yaml.safe_load(f)

        profile_config = updated_config["director_profile"]["custom_profile"]
        assert "UI Foundation" in profile_config["role_title"]
        assert "design system" in profile_config["primary_focus"]

    def test_quick_setup_backend_services_template(self, temp_config_for_quick_setup):
        """Test quick setup with backend services template"""
        runner = CliRunner()

        result = runner.invoke(quick_setup, ["--template", "backend_services"])

        assert result.exit_code == 0
        assert "Setting up with backend_services template" in result.output
        assert "Director of Backend Engineering" in result.output

    def test_quick_setup_interactive_template_selection(
        self, temp_config_for_quick_setup
    ):
        """Test quick setup with interactive template selection"""
        runner = CliRunner()

        # Simulate user selecting design_system template
        inputs = "design_system\n"

        result = runner.invoke(quick_setup, input=inputs)

        assert result.exit_code == 0
        assert "Available quick setup templates" in result.output
        assert "design_system:" in result.output

    def test_quick_setup_updates_domain_weights(self, temp_config_for_quick_setup):
        """Test that quick setup properly updates domain weights"""
        runner = CliRunner()

        result = runner.invoke(quick_setup, ["--template", "design_system"])

        assert result.exit_code == 0

        # Check that domains were enabled and weighted correctly
        with open(temp_config_for_quick_setup, "r") as f:
            updated_config = yaml.safe_load(f)

        domains = updated_config["organizational_intelligence"]["velocity_tracking"][
            "measurement_domains"
        ]

        # Design system template should enable these domains
        assert domains["design_system_leverage"]["enabled"] is True
        assert domains["platform_adoption"]["enabled"] is True
        assert domains["developer_experience"]["enabled"] is True

        # And disable others
        assert domains["api_service_efficiency"]["enabled"] is False

        # Check weights
        assert domains["design_system_leverage"]["weight"] == 0.35
        assert domains["platform_adoption"]["weight"] == 0.30


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases"""

    def test_setup_with_invalid_profile_type(self):
        """Test setup with invalid profile type"""
        runner = CliRunner()

        result = runner.invoke(setup, ["--profile-type", "invalid_type"])

        # Should fail due to Click choice validation
        assert result.exit_code != 0

    def test_quick_setup_with_invalid_template(self):
        """Test quick setup with invalid template"""
        runner = CliRunner()

        result = runner.invoke(quick_setup, ["--template", "invalid_template"])

        # Should fail due to Click choice validation
        assert result.exit_code != 0

    @patch(
        "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
    )
    def test_status_with_manager_error(self, mock_manager_class):
        """Test status command when manager initialization fails"""
        mock_manager_class.side_effect = Exception("Configuration error")

        runner = CliRunner()
        result = runner.invoke(status)

        # Should handle the error gracefully
        assert result.exit_code != 0


class TestCLIIntegration:
    """Integration tests for CLI commands"""

    def test_setup_then_status_workflow(self):
        """Test complete workflow: setup then status"""
        # Create temporary config directory
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)

        config_path = config_dir / "p1_organizational_intelligence.yaml"

        # Initial minimal config
        initial_config = {
            "director_profile": {"profile_type": "platform_director"},
            "organizational_intelligence": {
                "velocity_tracking": {"measurement_domains": {}}
            },
        }

        with open(config_path, "w") as f:
            yaml.dump(initial_config, f)

        runner = CliRunner()

        try:
            # Run setup
            setup_result = runner.invoke(
                setup,
                [
                    "--profile-type",
                    "platform_director",
                    "--role-title",
                    "Integration Test Director",
                ],
            )

            assert setup_result.exit_code == 0

            # Then run status to verify
            with patch(
                "lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager"
            ) as mock_manager:
                mock_profile = MagicMock()
                mock_profile.role_title = "Integration Test Director"
                mock_profile.primary_focus = "Test"
                mock_profile.enabled_domains = {}
                mock_profile.investment_categories = {}
                mock_profile.strategic_priorities = []
                mock_profile.success_metrics = []
                mock_profile.integration_preferences = {}

                mock_manager.return_value.current_profile = mock_profile

                status_result = runner.invoke(status)
                assert status_result.exit_code == 0
                assert "Integration Test Director" in status_result.output

        finally:
            # Cleanup
            if config_path.exists():
                config_path.unlink()
            if config_dir.exists():
                config_dir.rmdir()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
