#!/usr/bin/env python3
"""
Unit tests for Director Profile Manager
Comprehensive testing of P1 Organizational Intelligence core functionality
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open
from typing import Dict, Any

# Import the modules under test
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from lib.claudedirector.p1_features.organizational_intelligence.director_profile_manager import (
    DirectorProfileManager,
    DirectorProfile,
    MetricDefinition,
    InvestmentCategory,
    DirectorRole,
)


class TestMetricDefinition:
    """Test MetricDefinition dataclass"""

    def test_metric_definition_creation(self):
        """Test basic MetricDefinition creation"""
        metric = MetricDefinition(
            name="test_metric",
            enabled=True,
            weight=0.5,
            target_value=0.8,
            measurement_method="test_method",
        )

        assert metric.name == "test_metric"
        assert metric.enabled is True
        assert metric.weight == 0.5
        assert metric.target_value == 0.8
        assert metric.measurement_method == "test_method"
        assert metric.annual_value_per_percent is None

    def test_metric_definition_with_annual_value(self):
        """Test MetricDefinition with annual value"""
        metric = MetricDefinition(
            name="business_metric",
            enabled=True,
            weight=0.3,
            target_value=0.9,
            measurement_method="business_analysis",
            annual_value_per_percent=15000.0,
        )

        assert metric.annual_value_per_percent == 15000.0


class TestInvestmentCategory:
    """Test InvestmentCategory dataclass"""

    def test_investment_category_creation(self):
        """Test basic InvestmentCategory creation"""
        investment = InvestmentCategory(
            name="test_investment",
            enabled=True,
            priority_weight=0.4,
            roi_calculation_method="productivity_gains",
            measurement_period_months=6,
            success_criteria=[{"metric": "adoption", "target": 0.8}],
        )

        assert investment.name == "test_investment"
        assert investment.enabled is True
        assert investment.priority_weight == 0.4
        assert investment.roi_calculation_method == "productivity_gains"
        assert investment.measurement_period_months == 6
        assert len(investment.success_criteria) == 1


class TestDirectorProfile:
    """Test DirectorProfile dataclass"""

    def test_director_profile_creation(self):
        """Test DirectorProfile creation with all fields"""
        metrics = [MetricDefinition("test", True, 0.5, 0.8, "method")]
        investment = InvestmentCategory("invest", True, 0.3, "method", 6, [])

        profile = DirectorProfile(
            role_title="Test Director",
            primary_focus="Testing",
            strategic_priorities=["Priority 1", "Priority 2"],
            success_metrics=["Metric 1"],
            enabled_domains={"domain1": metrics},
            investment_categories={"invest1": investment},
            dashboard_config={"layout": "test"},
            integration_preferences={"tool1": True},
        )

        assert profile.role_title == "Test Director"
        assert profile.primary_focus == "Testing"
        assert len(profile.strategic_priorities) == 2
        assert len(profile.success_metrics) == 1
        assert "domain1" in profile.enabled_domains
        assert "invest1" in profile.investment_categories


class TestDirectorProfileManager:
    """Test DirectorProfileManager main functionality"""

    @pytest.fixture
    def sample_config(self) -> Dict[str, Any]:
        """Sample configuration for testing"""
        return {
            "director_profile": {
                "profile_type": "custom",
                "custom_profile": {
                    "role_title": "Test Director",
                    "primary_focus": "Test Focus",
                    "strategic_priorities": ["Priority 1", "Priority 2"],
                    "success_metrics": ["Metric 1", "Metric 2"],
                },
            },
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {
                            "enabled": True,
                            "weight": 0.35,
                            "metrics": ["component_usage", "design_consistency"],
                            "targets": {"component": 0.8, "design": 0.85},
                        },
                        "platform_adoption": {
                            "enabled": True,
                            "weight": 0.30,
                            "metrics": ["adoption_rate", "satisfaction"],
                            "targets": {"adoption": 0.75, "satisfaction": 4.5},
                        },
                        "api_service_efficiency": {
                            "enabled": False,
                            "weight": 0.0,
                            "metrics": ["response_time", "uptime"],
                            "targets": {"response": 200, "uptime": 0.99},
                        },
                    }
                },
                "investment_intelligence": {
                    "investment_categories": {
                        "design_system_enhancement": {
                            "enabled": True,
                            "priority_weight": 0.35,
                            "roi_calculation_method": "developer_velocity_improvement",
                            "measurement_period_months": 6,
                            "success_criteria": [
                                {"metric": "adoption", "target": 0.85, "weight": 0.6}
                            ],
                        },
                        "platform_infrastructure": {
                            "enabled": True,
                            "priority_weight": 0.30,
                            "roi_calculation_method": "operational_efficiency",
                            "measurement_period_months": 12,
                            "success_criteria": [
                                {
                                    "metric": "deployment_frequency",
                                    "target": 2.0,
                                    "weight": 0.5,
                                }
                            ],
                        },
                    }
                },
            },
            "dashboard": {"layout": "platform_director"},
            "integrations": {
                "design_tools": {
                    "figma": {"enabled": False},
                    "sketch": {"enabled": False},
                },
                "development_tools": {
                    "github": {"enabled": True},
                    "jira": {"enabled": True},
                },
            },
            "preset_profiles": {
                "platform_director": {
                    "focus_areas": ["design_system_leverage", "platform_adoption"],
                    "key_metrics": ["adoption_rate", "design_consistency"],
                    "dashboard_layout": "platform_focused",
                }
            },
        }

    @pytest.fixture
    def temp_config_file(self, sample_config):
        """Create temporary config file for testing"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config, f)
            return f.name

    def test_init_with_valid_config(self, temp_config_file):
        """Test DirectorProfileManager initialization with valid config"""
        manager = DirectorProfileManager(temp_config_file)

        assert manager.config is not None
        assert manager.current_profile is not None
        assert manager.current_profile.role_title == "Test Director"

        # Cleanup
        Path(temp_config_file).unlink()

    def test_init_with_missing_config_file(self):
        """Test initialization with missing config file"""
        with pytest.raises(Exception, match="Configuration file not found"):
            DirectorProfileManager("nonexistent_file.yaml")

    def test_load_configuration_valid_yaml(self, temp_config_file, sample_config):
        """Test loading valid YAML configuration"""
        manager = DirectorProfileManager(temp_config_file)
        config = manager._load_configuration()

        assert config["director_profile"]["profile_type"] == "custom"
        assert config["organizational_intelligence"] is not None

        # Cleanup
        Path(temp_config_file).unlink()

    def test_create_custom_profile(self, temp_config_file):
        """Test creating custom profile from configuration"""
        manager = DirectorProfileManager(temp_config_file)
        profile = manager.current_profile

        assert profile.role_title == "Test Director"
        assert profile.primary_focus == "Test Focus"
        assert len(profile.strategic_priorities) == 2
        assert len(profile.enabled_domains) == 2  # Only enabled domains
        assert "design_system_leverage" in profile.enabled_domains
        assert "platform_adoption" in profile.enabled_domains
        assert "api_service_efficiency" not in profile.enabled_domains  # Disabled

        # Cleanup
        Path(temp_config_file).unlink()

    def test_create_preset_profile(self, temp_config_file, sample_config):
        """Test creating preset profile"""
        # Modify config to use preset
        sample_config["director_profile"]["profile_type"] = "platform_director"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config, f)
            preset_config_file = f.name

        manager = DirectorProfileManager(preset_config_file)
        profile = manager.current_profile

        assert "Platform Director" in profile.role_title
        assert "design_system_leverage, platform_adoption" in profile.primary_focus

        # Cleanup
        Path(preset_config_file).unlink()
        Path(temp_config_file).unlink()

    def test_customize_profile_enable_domains(self, temp_config_file):
        """Test enabling additional domains"""
        manager = DirectorProfileManager(temp_config_file)

        initial_count = len(manager.current_profile.enabled_domains)

        # Enable previously disabled domain
        manager.customize_profile(enable_domains=["api_service_efficiency"])

        assert len(manager.current_profile.enabled_domains) == initial_count + 1
        assert "api_service_efficiency" in manager.current_profile.enabled_domains

        # Cleanup
        Path(temp_config_file).unlink()

    def test_customize_profile_disable_domains(self, temp_config_file):
        """Test disabling domains"""
        manager = DirectorProfileManager(temp_config_file)

        initial_count = len(manager.current_profile.enabled_domains)

        # Disable existing domain
        manager.customize_profile(disable_domains=["design_system_leverage"])

        assert len(manager.current_profile.enabled_domains) == initial_count - 1
        assert "design_system_leverage" not in manager.current_profile.enabled_domains

        # Cleanup
        Path(temp_config_file).unlink()

    def test_customize_profile_update_weights(self, temp_config_file):
        """Test updating domain weights"""
        manager = DirectorProfileManager(temp_config_file)

        # Update weights
        new_weights = {"design_system_leverage": 0.5, "platform_adoption": 0.5}
        manager.customize_profile(update_weights=new_weights)

        # Check updated weights
        design_metrics = manager.current_profile.enabled_domains[
            "design_system_leverage"
        ]
        platform_metrics = manager.current_profile.enabled_domains["platform_adoption"]

        assert design_metrics[0].weight == 0.5
        assert platform_metrics[0].weight == 0.5

        # Cleanup
        Path(temp_config_file).unlink()

    def test_customize_profile_update_targets(self, temp_config_file):
        """Test updating target values"""
        manager = DirectorProfileManager(temp_config_file)

        # Update targets
        new_targets = {"design_system_leverage": 0.9, "platform_adoption": 0.8}
        manager.customize_profile(update_targets=new_targets)

        # Check updated targets
        design_metrics = manager.current_profile.enabled_domains[
            "design_system_leverage"
        ]
        platform_metrics = manager.current_profile.enabled_domains["platform_adoption"]

        assert design_metrics[0].target_value == 0.9
        assert platform_metrics[0].target_value == 0.8

        # Cleanup
        Path(temp_config_file).unlink()

    def test_calculate_organizational_impact_score(self, temp_config_file):
        """Test organizational impact score calculation"""
        manager = DirectorProfileManager(temp_config_file)

        # Mock current metrics
        current_metrics = {
            "component_usage": 0.7,  # 70% of 80% target = 87.5% achievement
            "design_consistency": 0.8,  # 80% of 85% target = 94.1% achievement
            "adoption_rate": 0.6,  # 60% of 75% target = 80% achievement
            "satisfaction": 4.0,  # 4.0 of 4.5 target = 88.9% achievement
        }

        impact_score = manager.calculate_organizational_impact_score(current_metrics)

        # Should be weighted average of achievements
        assert 0.0 <= impact_score <= 1.0
        assert impact_score > 0.8  # Should be high given good performance

        # Cleanup
        Path(temp_config_file).unlink()

    def test_calculate_impact_score_no_metrics(self, temp_config_file):
        """Test impact score calculation with no matching metrics"""
        manager = DirectorProfileManager(temp_config_file)

        # Empty metrics
        current_metrics = {}

        impact_score = manager.calculate_organizational_impact_score(current_metrics)

        assert impact_score == 0.0

        # Cleanup
        Path(temp_config_file).unlink()

    def test_generate_executive_summary(self, temp_config_file):
        """Test executive summary generation"""
        manager = DirectorProfileManager(temp_config_file)

        summary = manager.generate_executive_summary()

        assert "director_profile" in summary
        assert "enabled_domains" in summary
        assert "investment_priorities" in summary
        assert "success_metrics" in summary

        assert summary["director_profile"]["role"] == "Test Director"
        assert len(summary["enabled_domains"]) == 2
        assert len(summary["investment_priorities"]) == 2

        # Cleanup
        Path(temp_config_file).unlink()

    def test_get_dashboard_config(self, temp_config_file):
        """Test dashboard configuration retrieval"""
        manager = DirectorProfileManager(temp_config_file)

        dashboard_config = manager.get_dashboard_config()

        assert dashboard_config["layout"] == "platform_director"

    def test_get_enabled_metrics(self, temp_config_file):
        """Test enabled metrics retrieval"""
        manager = DirectorProfileManager(temp_config_file)

        enabled_metrics = manager.get_enabled_metrics()

        assert len(enabled_metrics) == 2
        assert "design_system_leverage" in enabled_metrics
        assert "platform_adoption" in enabled_metrics

        # Cleanup
        Path(temp_config_file).unlink()

    def test_get_investment_priorities(self, temp_config_file):
        """Test investment priorities retrieval"""
        manager = DirectorProfileManager(temp_config_file)

        investments = manager.get_investment_priorities()

        assert len(investments) == 2
        assert "design_system_enhancement" in investments
        assert "platform_infrastructure" in investments

        # Cleanup
        Path(temp_config_file).unlink()


class TestDirectorRole:
    """Test DirectorRole enum"""

    def test_director_role_values(self):
        """Test DirectorRole enum values"""
        assert DirectorRole.PLATFORM_DIRECTOR.value == "platform_director"
        assert DirectorRole.BACKEND_DIRECTOR.value == "backend_director"
        assert DirectorRole.PRODUCT_DIRECTOR.value == "product_director"
        assert DirectorRole.DESIGN_DIRECTOR.value == "design_director"
        assert DirectorRole.CUSTOM.value == "custom"


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_unknown_preset_profile(self, sample_config):
        """Test handling of unknown preset profile"""
        sample_config["director_profile"]["profile_type"] = "unknown_profile"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config, f)
            config_file = f.name

        with pytest.raises(ValueError, match="Unknown preset profile type"):
            DirectorProfileManager(config_file)

        # Cleanup
        Path(config_file).unlink()

    def test_malformed_yaml_config(self):
        """Test handling of malformed YAML"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [unclosed bracket")
            config_file = f.name

        with pytest.raises(yaml.YAMLError):
            DirectorProfileManager(config_file)

        # Cleanup
        Path(config_file).unlink()

    def test_missing_required_config_sections(self):
        """Test handling of missing required configuration sections"""
        minimal_config = {"director_profile": {"profile_type": "custom"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(minimal_config, f)
            config_file = f.name

        # Should handle gracefully with defaults
        manager = DirectorProfileManager(config_file)
        assert manager.current_profile is not None

        # Cleanup
        Path(config_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
