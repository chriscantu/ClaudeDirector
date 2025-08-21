#!/usr/bin/env python3
"""
Pytest configuration for P1 Organizational Intelligence tests
Shared fixtures and test utilities
"""

import pytest
import tempfile
import yaml
import os
from pathlib import Path
from unittest.mock import MagicMock

# Test fixtures for P1 features


@pytest.fixture
def sample_director_config():
    """Standard director configuration for testing"""
    return {
        "director_profile": {
            "profile_type": "custom",
            "custom_profile": {
                "role_title": "Test Director of Engineering",
                "primary_focus": "Platform development and team enablement",
                "strategic_priorities": [
                    "Platform scalability and developer experience",
                    "Design system adoption and consistency",
                    "Cross-team collaboration and knowledge sharing",
                ],
                "success_metrics": [
                    "Platform adoption rates",
                    "Developer satisfaction scores",
                    "Design system component usage",
                    "Cross-team velocity improvements",
                ],
            },
        },
        "organizational_intelligence": {
            "velocity_tracking": {
                "measurement_domains": {
                    "design_system_leverage": {
                        "enabled": True,
                        "weight": 0.35,
                        "metrics": [
                            "component_usage_consistency",
                            "design_debt_reduction",
                            "cross_team_design_velocity",
                        ],
                        "targets": {
                            "component_usage_consistency": 0.85,
                            "design_debt_reduction": 0.15,
                            "cross_team_design_velocity": 0.20,
                        },
                    },
                    "platform_adoption": {
                        "enabled": True,
                        "weight": 0.30,
                        "metrics": [
                            "adoption_rate_percentage",
                            "developer_satisfaction_score",
                            "time_to_onboard_new_teams",
                        ],
                        "targets": {
                            "adoption_rate_percentage": 0.80,
                            "developer_satisfaction_score": 4.5,
                            "time_to_onboard_new_teams": 3.0,
                        },
                    },
                    "developer_experience": {
                        "enabled": True,
                        "weight": 0.25,
                        "metrics": [
                            "onboarding_efficiency",
                            "productivity_metrics",
                            "tool_satisfaction",
                        ],
                        "targets": {
                            "onboarding_efficiency": 0.60,
                            "productivity_metrics": 0.75,
                            "tool_satisfaction": 4.2,
                        },
                    },
                    "knowledge_sharing": {
                        "enabled": True,
                        "weight": 0.10,
                        "metrics": [
                            "cross_team_learning_index",
                            "best_practice_adoption",
                            "documentation_quality",
                        ],
                        "targets": {
                            "cross_team_learning_index": 0.70,
                            "best_practice_adoption": 0.65,
                            "documentation_quality": 0.80,
                        },
                    },
                    # Disabled domain for testing
                    "api_service_efficiency": {
                        "enabled": False,
                        "weight": 0.0,
                        "metrics": ["api_response_times", "service_dependency_health"],
                        "targets": {
                            "api_response_times": 200,
                            "service_dependency_health": 0.95,
                        },
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
                            {
                                "metric": "component_adoption_rate",
                                "target": 0.85,
                                "weight": 0.4,
                            },
                            {
                                "metric": "development_velocity_improvement",
                                "target": 0.25,
                                "weight": 0.6,
                            },
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
                            },
                            {
                                "metric": "mean_time_to_recovery",
                                "target": 0.5,
                                "weight": 0.5,
                            },
                        ],
                    },
                    "developer_experience": {
                        "enabled": True,
                        "priority_weight": 0.25,
                        "roi_calculation_method": "productivity_and_satisfaction",
                        "measurement_period_months": 3,
                        "success_criteria": [
                            {
                                "metric": "developer_satisfaction",
                                "target": 4.5,
                                "weight": 0.6,
                            },
                            {
                                "metric": "onboarding_efficiency",
                                "target": 0.6,
                                "weight": 0.4,
                            },
                        ],
                    },
                    "cross_team_tooling": {
                        "enabled": True,
                        "priority_weight": 0.10,
                        "roi_calculation_method": "coordination_efficiency",
                        "measurement_period_months": 9,
                        "success_criteria": [
                            {
                                "metric": "cross_team_communication_efficiency",
                                "target": 0.3,
                                "weight": 1.0,
                            }
                        ],
                    },
                }
            },
        },
        "business_value": {
            "value_drivers": {
                "developer_productivity": {
                    "enabled": True,
                    "annual_value_per_percent": 15000,
                    "measurement_method": "velocity_and_satisfaction",
                },
                "design_consistency": {
                    "enabled": True,
                    "annual_value_per_percent": 8000,
                    "measurement_method": "brand_and_ux_metrics",
                },
                "platform_adoption": {
                    "enabled": True,
                    "annual_value_per_percent": 12000,
                    "measurement_method": "team_onboarding_and_usage",
                },
                "cross_team_velocity": {
                    "enabled": True,
                    "annual_value_per_percent": 20000,
                    "measurement_method": "coordination_and_delivery",
                },
            }
        },
        "dashboard": {
            "layout": "platform_director",
            "custom_widgets": [
                {
                    "type": "design_system_health",
                    "position": "top_left",
                    "enabled": True,
                    "refresh_rate": "hourly",
                },
                {
                    "type": "platform_adoption_trends",
                    "position": "top_right",
                    "enabled": True,
                    "refresh_rate": "daily",
                },
                {
                    "type": "investment_roi_tracking",
                    "position": "middle_right",
                    "enabled": True,
                    "refresh_rate": "weekly",
                },
            ],
        },
        "integrations": {
            "design_tools": {
                "figma": {"enabled": False, "api_key_env": "FIGMA_API_KEY"},
                "sketch": {"enabled": False, "api_key_env": "SKETCH_API_KEY"},
            },
            "development_tools": {
                "github": {"enabled": True, "api_key_env": "GITHUB_API_KEY"},
                "jira": {"enabled": True, "api_key_env": "JIRA_API_KEY"},
            },
            "analytics": {
                "datadog": {"enabled": False, "api_key_env": "DATADOG_API_KEY"}
            },
        },
        "preset_profiles": {
            "platform_director": {
                "focus_areas": [
                    "design_system_leverage",
                    "platform_adoption",
                    "developer_experience",
                ],
                "key_metrics": [
                    "adoption_rate",
                    "developer_satisfaction",
                    "design_consistency",
                ],
                "dashboard_layout": "platform_focused",
            },
            "backend_director": {
                "focus_areas": [
                    "api_service_efficiency",
                    "system_reliability",
                    "cross_team_coordination",
                ],
                "key_metrics": [
                    "api_performance",
                    "service_uptime",
                    "integration_health",
                ],
                "dashboard_layout": "services_focused",
            },
        },
    }


@pytest.fixture
def temp_config_file(sample_director_config):
    """Create temporary configuration file for testing"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(sample_director_config, f)
        yield f.name

    # Cleanup
    Path(f.name).unlink()


@pytest.fixture
def mock_director_profile():
    """Mock DirectorProfile for testing"""
    profile = MagicMock()

    # Mock basic attributes
    profile.role_title = "Mock Director of Engineering"
    profile.primary_focus = "Mock platform development"
    profile.strategic_priorities = ["Mock Priority 1", "Mock Priority 2"]
    profile.success_metrics = ["Mock Metric 1", "Mock Metric 2"]

    # Mock enabled domains with metrics
    mock_metric_1 = MagicMock()
    mock_metric_1.name = "mock_metric_1"
    mock_metric_1.weight = 0.5
    mock_metric_1.target_value = 0.8
    mock_metric_1.enabled = True

    mock_metric_2 = MagicMock()
    mock_metric_2.name = "mock_metric_2"
    mock_metric_2.weight = 0.5
    mock_metric_2.target_value = 0.9
    mock_metric_2.enabled = True

    profile.enabled_domains = {
        "mock_domain_1": [mock_metric_1],
        "mock_domain_2": [mock_metric_2],
    }

    # Mock investment categories
    mock_investment = MagicMock()
    mock_investment.name = "mock_investment"
    mock_investment.priority_weight = 0.7
    mock_investment.measurement_period_months = 6

    profile.investment_categories = {"mock_investment": mock_investment}

    # Mock dashboard and integration preferences
    profile.dashboard_config = {"layout": "mock_layout"}
    profile.integration_preferences = {"mock_tool": True}

    return profile


@pytest.fixture
def sample_current_metrics():
    """Sample current metrics for testing calculations"""
    return {
        "component_usage_consistency": 0.78,
        "design_debt_reduction": 0.12,
        "cross_team_design_velocity": 0.18,
        "adoption_rate_percentage": 0.75,
        "developer_satisfaction_score": 4.3,
        "time_to_onboard_new_teams": 3.5,
        "onboarding_efficiency": 0.55,
        "productivity_metrics": 0.72,
        "tool_satisfaction": 4.1,
        "cross_team_learning_index": 0.68,
        "best_practice_adoption": 0.60,
        "documentation_quality": 0.75,
    }


@pytest.fixture
def clean_test_config_directory():
    """Create clean test configuration directory"""
    test_dir = Path(tempfile.mkdtemp())
    config_dir = test_dir / "config"
    config_dir.mkdir()

    original_cwd = os.getcwd()
    os.chdir(test_dir)

    yield test_dir, config_dir

    # Cleanup
    os.chdir(original_cwd)
    import shutil

    shutil.rmtree(test_dir)


@pytest.fixture
def backend_director_config():
    """Configuration for backend director testing"""
    return {
        "director_profile": {
            "profile_type": "custom",
            "custom_profile": {
                "role_title": "Director of Backend Engineering",
                "primary_focus": "Service architecture, API design, system scalability",
                "strategic_priorities": [
                    "Service reliability and performance",
                    "API design and integration quality",
                    "System scalability and efficiency",
                    "Cross-team service coordination",
                ],
                "success_metrics": [
                    "API response times",
                    "Service uptime",
                    "Integration success rates",
                    "System throughput",
                ],
            },
        },
        "organizational_intelligence": {
            "velocity_tracking": {
                "measurement_domains": {
                    "api_service_efficiency": {
                        "enabled": True,
                        "weight": 0.40,
                        "metrics": [
                            "api_response_times",
                            "service_uptime",
                            "throughput",
                        ],
                        "targets": {
                            "api_response_times": 200,
                            "service_uptime": 0.999,
                            "throughput": 1000,
                        },
                    },
                    "feature_delivery_impact": {
                        "enabled": True,
                        "weight": 0.35,
                        "metrics": ["delivery_velocity", "integration_success"],
                        "targets": {
                            "delivery_velocity": 0.80,
                            "integration_success": 0.95,
                        },
                    },
                    "knowledge_sharing": {
                        "enabled": True,
                        "weight": 0.25,
                        "metrics": ["cross_team_coordination"],
                        "targets": {"cross_team_coordination": 0.75},
                    },
                }
            }
        },
    }


@pytest.fixture
def product_director_config():
    """Configuration for product director testing"""
    return {
        "director_profile": {
            "profile_type": "custom",
            "custom_profile": {
                "role_title": "Director of Product Engineering",
                "primary_focus": "Feature delivery, user experience, product quality",
                "strategic_priorities": [
                    "Feature delivery velocity and quality",
                    "User experience and product outcomes",
                    "Cross-functional team coordination",
                    "Product-engineering alignment",
                ],
                "success_metrics": [
                    "Feature delivery metrics",
                    "User satisfaction scores",
                    "Product quality indicators",
                    "Cross-functional efficiency",
                ],
            },
        },
        "organizational_intelligence": {
            "velocity_tracking": {
                "measurement_domains": {
                    "feature_delivery_impact": {
                        "enabled": True,
                        "weight": 0.40,
                        "metrics": ["feature_velocity", "quality_score"],
                        "targets": {"feature_velocity": 0.85, "quality_score": 0.90},
                    },
                    "developer_experience": {
                        "enabled": True,
                        "weight": 0.30,
                        "metrics": ["team_satisfaction", "productivity"],
                        "targets": {"team_satisfaction": 4.5, "productivity": 0.80},
                    },
                    "knowledge_sharing": {
                        "enabled": True,
                        "weight": 0.30,
                        "metrics": ["cross_functional_alignment"],
                        "targets": {"cross_functional_alignment": 0.75},
                    },
                }
            }
        },
    }


# Test utilities


def assert_metric_definition(
    metric,
    expected_name,
    expected_enabled=True,
    expected_weight=None,
    expected_target=None,
):
    """Utility to assert MetricDefinition properties"""
    assert metric.name == expected_name
    assert metric.enabled == expected_enabled

    if expected_weight is not None:
        assert abs(metric.weight - expected_weight) < 0.001

    if expected_target is not None:
        assert abs(metric.target_value - expected_target) < 0.001


def assert_investment_category(
    investment,
    expected_name,
    expected_enabled=True,
    expected_priority=None,
    expected_period=None,
):
    """Utility to assert InvestmentCategory properties"""
    assert investment.name == expected_name
    assert investment.enabled == expected_enabled

    if expected_priority is not None:
        assert abs(investment.priority_weight - expected_priority) < 0.001

    if expected_period is not None:
        assert investment.measurement_period_months == expected_period


def create_test_config_file(config_dict, file_path):
    """Utility to create test configuration file"""
    with open(file_path, "w") as f:
        yaml.dump(config_dict, f, indent=2)


def load_test_config_file(file_path):
    """Utility to load test configuration file"""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


# Performance testing utilities


def measure_execution_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    import time

    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def assert_performance_threshold(
    execution_time, threshold_seconds, operation_name="Operation"
):
    """Assert that execution time is below threshold"""
    assert (
        execution_time < threshold_seconds
    ), f"{operation_name} took {execution_time:.3f}s, expected < {threshold_seconds}s"


# Coverage utilities


def get_test_coverage_report():
    """Generate test coverage report for P1 features"""
    try:
        import coverage

        cov = coverage.Coverage()
        cov.start()
        # Test execution would happen here
        cov.stop()
        cov.save()
        return cov.report()
    except ImportError:
        return "Coverage module not available"


# Test markers for categorizing tests


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "functional: Functional tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "cli: CLI tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Custom pytest hooks


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "functional" in str(item.fspath):
            item.add_marker(pytest.mark.functional)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Add CLI marker for CLI-related tests
        if "cli" in item.name.lower() or "cli" in str(item.fspath):
            item.add_marker(pytest.mark.cli)

        # Add performance marker for performance tests
        if "performance" in item.name.lower():
            item.add_marker(pytest.mark.performance)

        # Add slow marker for tests that take longer
        if "large" in item.name.lower() or "concurrent" in item.name.lower():
            item.add_marker(pytest.mark.slow)
