#!/usr/bin/env python3
"""
Functional tests for P1 Organizational Intelligence
End-to-end workflow testing for director profile management
"""

import pytest
import tempfile
import yaml
import subprocess
import os
from pathlib import Path
from click.testing import CliRunner

# Import the modules under test
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from lib.claudedirector.p1_features.organizational_intelligence import DirectorProfileManager
from lib.claudedirector.p1_features.organizational_intelligence.cli_customization import org_intelligence


class TestDirectorProfileWorkflows:
    """Test complete director profile management workflows"""

    @pytest.fixture
    def clean_test_environment(self):
        """Set up clean test environment"""
        # Create temporary directory for test
        test_dir = Path(tempfile.mkdtemp())
        original_cwd = os.getcwd()

        # Change to test directory
        os.chdir(test_dir)

        # Create config directory
        config_dir = test_dir / "config"
        config_dir.mkdir()

        yield test_dir

        # Cleanup
        os.chdir(original_cwd)

        # Remove test directory and contents
        import shutil
        shutil.rmtree(test_dir)

    def test_complete_platform_director_setup_workflow(self, clean_test_environment):
        """Test complete setup workflow for platform director"""

        # Step 1: Create initial configuration
        config_path = clean_test_environment / "config" / "p1_organizational_intelligence.yaml"
        initial_config = {
            "director_profile": {
                "profile_type": "custom",
                "custom_profile": {
                    "role_title": "Director of Engineering - UI Foundation",
                    "primary_focus": "Web platform, design system, internationalization",
                    "strategic_priorities": [
                        "Platform scalability and developer experience",
                        "Design system adoption and consistency",
                        "International expansion support"
                    ],
                    "success_metrics": [
                        "Platform adoption rates",
                        "Developer satisfaction scores",
                        "Design system component usage"
                    ]
                }
            },
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {
                            "enabled": True,
                            "weight": 0.35,
                            "metrics": ["component_usage_consistency", "design_debt_reduction"],
                            "targets": {
                                "component_usage_consistency": 0.85,
                                "design_debt_reduction": 0.15
                            }
                        },
                        "platform_adoption": {
                            "enabled": True,
                            "weight": 0.30,
                            "metrics": ["adoption_rate_percentage", "developer_satisfaction_score"],
                            "targets": {
                                "adoption_rate_percentage": 0.80,
                                "developer_satisfaction_score": 4.5
                            }
                        },
                        "developer_experience": {
                            "enabled": True,
                            "weight": 0.25,
                            "metrics": ["onboarding_efficiency", "productivity_metrics"],
                            "targets": {
                                "onboarding_efficiency": 0.60,
                                "productivity_metrics": 0.75
                            }
                        },
                        "knowledge_sharing": {
                            "enabled": True,
                            "weight": 0.10,
                            "metrics": ["cross_team_learning_index"],
                            "targets": {
                                "cross_team_learning_index": 0.70
                            }
                        }
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
                                {"metric": "component_adoption_rate", "target": 0.85, "weight": 0.6}
                            ]
                        },
                        "platform_infrastructure": {
                            "enabled": True,
                            "priority_weight": 0.30,
                            "roi_calculation_method": "operational_efficiency",
                            "measurement_period_months": 12,
                            "success_criteria": [
                                {"metric": "deployment_frequency", "target": 2.0, "weight": 0.5}
                            ]
                        }
                    }
                }
            },
            "dashboard": {
                "layout": "platform_director"
            },
            "integrations": {
                "design_tools": {
                    "figma": {"enabled": False},
                    "sketch": {"enabled": False}
                },
                "development_tools": {
                    "github": {"enabled": True},
                    "jira": {"enabled": True}
                }
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(initial_config, f)

        # Step 2: Initialize DirectorProfileManager
        manager = DirectorProfileManager(str(config_path))

        # Step 3: Verify initial profile
        profile = manager.current_profile
        assert profile.role_title == "Director of Engineering - UI Foundation"
        assert len(profile.enabled_domains) == 4
        assert "design_system_leverage" in profile.enabled_domains
        assert len(profile.investment_categories) == 2

        # Step 4: Test customization
        manager.customize_profile(
            update_weights={
                "design_system_leverage": 0.40,  # Increase design system focus
                "platform_adoption": 0.30,
                "developer_experience": 0.20,
                "knowledge_sharing": 0.10
            },
            update_targets={
                "design_system_leverage": 0.90,  # Increase design consistency target
                "platform_adoption": 0.85       # Increase adoption target
            }
        )

        # Step 5: Verify customizations
        design_metrics = profile.enabled_domains["design_system_leverage"]
        platform_metrics = profile.enabled_domains["platform_adoption"]

        assert design_metrics[0].weight == 0.40
        assert design_metrics[0].target_value == 0.90
        assert platform_metrics[0].target_value == 0.85

        # Step 6: Test business value calculation
        current_metrics = {
            "component_usage_consistency": 0.75,  # 75% actual vs 90% target
            "design_debt_reduction": 0.12,        # 12% actual vs 15% target
            "adoption_rate_percentage": 0.78,     # 78% actual vs 85% target
            "developer_satisfaction_score": 4.3,  # 4.3 actual vs 4.5 target
            "onboarding_efficiency": 0.55,        # 55% actual vs 60% target
            "cross_team_learning_index": 0.68     # 68% actual vs 70% target
        }

        impact_score = manager.calculate_organizational_impact_score(current_metrics)

        # Should be a weighted score based on achievement ratios
        assert 0.0 <= impact_score <= 1.0
        assert impact_score > 0.70  # Should be reasonably high

        # Step 7: Generate executive summary
        summary = manager.generate_executive_summary()

        assert summary["director_profile"]["role"] == "Director of Engineering - UI Foundation"
        assert len(summary["enabled_domains"]) == 4
        assert len(summary["investment_priorities"]) == 2
        assert "Platform scalability and developer experience" in summary["director_profile"]["strategic_priorities"]

    def test_backend_director_workflow(self, clean_test_environment):
        """Test workflow for backend engineering director"""

        config_path = clean_test_environment / "config" / "p1_organizational_intelligence.yaml"

        # Backend director focused configuration
        backend_config = {
            "director_profile": {
                "profile_type": "custom",
                "custom_profile": {
                    "role_title": "Director of Backend Engineering",
                    "primary_focus": "Service architecture, API design, system scalability",
                    "strategic_priorities": [
                        "Service reliability and performance",
                        "API design and integration quality",
                        "System scalability and efficiency"
                    ],
                    "success_metrics": [
                        "API response times",
                        "Service uptime",
                        "Integration success rates"
                    ]
                }
            },
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "api_service_efficiency": {
                            "enabled": True,
                            "weight": 0.40,
                            "metrics": ["api_response_times", "service_uptime"],
                            "targets": {
                                "api_response_times": 200,  # 200ms target
                                "service_uptime": 0.999     # 99.9% uptime target
                            }
                        },
                        "feature_delivery_impact": {
                            "enabled": True,
                            "weight": 0.35,
                            "metrics": ["delivery_velocity", "integration_success"],
                            "targets": {
                                "delivery_velocity": 0.80,
                                "integration_success": 0.95
                            }
                        },
                        "knowledge_sharing": {
                            "enabled": True,
                            "weight": 0.25,
                            "metrics": ["cross_team_coordination"],
                            "targets": {
                                "cross_team_coordination": 0.75
                            }
                        },
                        # Design system should be disabled for backend director
                        "design_system_leverage": {
                            "enabled": False,
                            "weight": 0.0,
                            "metrics": [],
                            "targets": {}
                        }
                    }
                },
                "investment_intelligence": {
                    "investment_categories": {
                        "platform_infrastructure": {
                            "enabled": True,
                            "priority_weight": 0.50,
                            "roi_calculation_method": "operational_efficiency",
                            "measurement_period_months": 9,
                            "success_criteria": [
                                {"metric": "service_reliability", "target": 0.999, "weight": 0.6}
                            ]
                        },
                        "cross_team_tooling": {
                            "enabled": True,
                            "priority_weight": 0.50,
                            "roi_calculation_method": "coordination_efficiency",
                            "measurement_period_months": 6,
                            "success_criteria": [
                                {"metric": "integration_time_reduction", "target": 0.30, "weight": 0.7}
                            ]
                        }
                    }
                }
            },
            "dashboard": {
                "layout": "backend_focused"
            },
            "integrations": {
                "development_tools": {
                    "github": {"enabled": True},
                    "jira": {"enabled": True}
                },
                "analytics": {
                    "datadog": {"enabled": True}
                }
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(backend_config, f)

        # Initialize and test backend director profile
        manager = DirectorProfileManager(str(config_path))
        profile = manager.current_profile

        # Verify backend-specific configuration
        assert profile.role_title == "Director of Backend Engineering"
        assert "Service architecture" in profile.primary_focus

        # Should have backend-focused domains enabled
        assert "api_service_efficiency" in profile.enabled_domains
        assert "feature_delivery_impact" in profile.enabled_domains

        # Design system should NOT be enabled for backend director
        assert "design_system_leverage" not in profile.enabled_domains

        # Test API service efficiency metrics
        api_metrics = profile.enabled_domains["api_service_efficiency"]
        assert api_metrics[0].weight == 0.40  # Highest weight for backend director

        # Test business value calculation with backend-specific metrics
        backend_current_metrics = {
            "api_response_times": 180,           # 180ms actual vs 200ms target (good)
            "service_uptime": 0.9995,           # 99.95% actual vs 99.9% target (excellent)
            "delivery_velocity": 0.75,          # 75% actual vs 80% target (good)
            "integration_success": 0.97,        # 97% actual vs 95% target (excellent)
            "cross_team_coordination": 0.70     # 70% actual vs 75% target (good)
        }

        impact_score = manager.calculate_organizational_impact_score(backend_current_metrics)
        assert impact_score > 0.85  # Should be high for good backend performance

    def test_profile_migration_workflow(self, clean_test_environment):
        """Test migrating from one director profile to another"""

        config_path = clean_test_environment / "config" / "p1_organizational_intelligence.yaml"

        # Start as product director
        initial_config = {
            "director_profile": {
                "profile_type": "custom",
                "custom_profile": {
                    "role_title": "Director of Product Engineering",
                    "primary_focus": "Feature delivery, user experience",
                    "strategic_priorities": ["Feature velocity", "User satisfaction"],
                    "success_metrics": ["Delivery metrics", "User feedback"]
                }
            },
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "feature_delivery_impact": {
                            "enabled": True,
                            "weight": 0.60,
                            "metrics": ["feature_velocity"],
                            "targets": {"feature_velocity": 0.80}
                        },
                        "developer_experience": {
                            "enabled": True,
                            "weight": 0.40,
                            "metrics": ["team_satisfaction"],
                            "targets": {"team_satisfaction": 4.0}
                        }
                    }
                },
                "investment_intelligence": {
                    "investment_categories": {
                        "feature_tooling": {
                            "enabled": True,
                            "priority_weight": 1.0,
                            "roi_calculation_method": "feature_delivery",
                            "measurement_period_months": 3,
                            "success_criteria": []
                        }
                    }
                }
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(initial_config, f)

        # Initialize as product director
        manager = DirectorProfileManager(str(config_path))
        initial_profile = manager.current_profile

        assert initial_profile.role_title == "Director of Product Engineering"
        assert len(initial_profile.enabled_domains) == 2

        # Migrate to platform director role (simulate role change)
        manager.customize_profile(
            role_title="Director of Platform Engineering",
            enable_domains=["design_system_leverage", "platform_adoption"],
            disable_domains=["feature_delivery_impact"],
            update_weights={
                "design_system_leverage": 0.40,
                "platform_adoption": 0.35,
                "developer_experience": 0.25
            }
        )

        # Verify migration
        migrated_profile = manager.current_profile
        assert migrated_profile.role_title == "Director of Platform Engineering"
        assert "design_system_leverage" in migrated_profile.enabled_domains
        assert "platform_adoption" in migrated_profile.enabled_domains
        assert "feature_delivery_impact" not in migrated_profile.enabled_domains

        # Verify weights were updated
        design_weight = migrated_profile.enabled_domains["design_system_leverage"][0].weight
        platform_weight = migrated_profile.enabled_domains["platform_adoption"][0].weight

        assert design_weight == 0.40
        assert platform_weight == 0.35


class TestCLIFunctionalWorkflows:
    """Test CLI functional workflows"""

    @pytest.fixture
    def cli_test_environment(self):
        """Set up CLI test environment"""
        test_dir = Path(tempfile.mkdtemp())
        original_cwd = os.getcwd()

        os.chdir(test_dir)
        config_dir = test_dir / "config"
        config_dir.mkdir()

        # Create minimal config
        config_path = config_dir / "p1_organizational_intelligence.yaml"
        minimal_config = {
            "director_profile": {"profile_type": "platform_director"},
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {
                        "design_system_leverage": {"enabled": False, "weight": 0.0},
                        "platform_adoption": {"enabled": False, "weight": 0.0},
                        "developer_experience": {"enabled": False, "weight": 0.0}
                    }
                }
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(minimal_config, f)

        yield test_dir, config_path

        # Cleanup
        os.chdir(original_cwd)
        import shutil
        shutil.rmtree(test_dir)

    def test_complete_cli_setup_workflow(self, cli_test_environment):
        """Test complete CLI setup workflow"""
        test_dir, config_path = cli_test_environment

        runner = CliRunner()

        # Step 1: Quick setup with design system template
        result = runner.invoke(org_intelligence, [
            'quick-setup', '--template', 'design_system'
        ])

        assert result.exit_code == 0
        assert "Quick setup complete" in result.output

        # Step 2: Verify configuration was updated
        with open(config_path, 'r') as f:
            updated_config = yaml.safe_load(f)

        profile_config = updated_config["director_profile"]["custom_profile"]
        assert "UI Foundation" in profile_config["role_title"]

        domains = updated_config["organizational_intelligence"]["velocity_tracking"]["measurement_domains"]
        assert domains["design_system_leverage"]["enabled"] is True
        assert domains["platform_adoption"]["enabled"] is True

        # Step 3: Check status
        with patch('lib.claudedirector.p1_features.organizational_intelligence.cli_customization.DirectorProfileManager') as mock_manager:
            mock_profile = MagicMock()
            mock_profile.role_title = "Director of Engineering - UI Foundation"
            mock_profile.primary_focus = "Web platform, design system"
            mock_profile.enabled_domains = {"design_system_leverage": [MagicMock(weight=0.35)]}
            mock_profile.investment_categories = {}
            mock_profile.strategic_priorities = []
            mock_profile.success_metrics = []
            mock_profile.integration_preferences = {}

            mock_manager.return_value.current_profile = mock_profile

            status_result = runner.invoke(org_intelligence, ['status'])

            assert status_result.exit_code == 0
            assert "UI Foundation" in status_result.output


class TestPerformanceAndScalability:
    """Test performance and scalability of organizational intelligence"""

    def test_large_configuration_performance(self, clean_test_environment):
        """Test performance with large configuration"""

        config_path = clean_test_environment / "config" / "p1_organizational_intelligence.yaml"

        # Create large configuration with many domains and metrics
        large_config = {
            "director_profile": {
                "profile_type": "custom",
                "custom_profile": {
                    "role_title": "Enterprise Director",
                    "primary_focus": "Large scale operations",
                    "strategic_priorities": [f"Priority {i}" for i in range(20)],
                    "success_metrics": [f"Metric {i}" for i in range(50)]
                }
            },
            "organizational_intelligence": {
                "velocity_tracking": {
                    "measurement_domains": {}
                },
                "investment_intelligence": {
                    "investment_categories": {}
                }
            }
        }

        # Add many measurement domains
        for i in range(10):
            domain_name = f"domain_{i}"
            large_config["organizational_intelligence"]["velocity_tracking"]["measurement_domains"][domain_name] = {
                "enabled": True,
                "weight": 0.1,
                "metrics": [f"metric_{j}" for j in range(10)],
                "targets": {f"metric_{j}": 0.8 for j in range(10)}
            }

        # Add many investment categories
        for i in range(10):
            category_name = f"investment_{i}"
            large_config["organizational_intelligence"]["investment_intelligence"]["investment_categories"][category_name] = {
                "enabled": True,
                "priority_weight": 0.1,
                "roi_calculation_method": "test_method",
                "measurement_period_months": 6,
                "success_criteria": [{"metric": f"metric_{j}", "target": 0.8} for j in range(5)]
            }

        with open(config_path, 'w') as f:
            yaml.dump(large_config, f)

        # Test initialization performance
        import time

        start_time = time.time()
        manager = DirectorProfileManager(str(config_path))
        init_time = time.time() - start_time

        # Should initialize quickly even with large config
        assert init_time < 1.0  # Less than 1 second

        profile = manager.current_profile
        assert len(profile.enabled_domains) == 10
        assert len(profile.investment_categories) == 10

        # Test calculation performance with many metrics
        large_current_metrics = {}
        for domain_i in range(10):
            for metric_j in range(10):
                large_current_metrics[f"metric_{metric_j}"] = 0.75

        start_time = time.time()
        impact_score = manager.calculate_organizational_impact_score(large_current_metrics)
        calc_time = time.time() - start_time

        # Should calculate quickly even with many metrics
        assert calc_time < 0.1  # Less than 100ms
        assert 0.0 <= impact_score <= 1.0

    def test_concurrent_access_safety(self, clean_test_environment):
        """Test thread safety of DirectorProfileManager"""

        config_path = clean_test_environment / "config" / "p1_organizational_intelligence.yaml"

        # Create basic config
        config = {
            "director_profile": {"profile_type": "custom", "custom_profile": {"role_title": "Test"}},
            "organizational_intelligence": {
                "velocity_tracking": {"measurement_domains": {
                    "test_domain": {
                        "enabled": True, "weight": 1.0, "metrics": ["test_metric"], "targets": {"test_metric": 0.8}
                    }
                }}
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(config, f)

        # Test multiple managers accessing same config
        managers = []
        for i in range(5):
            manager = DirectorProfileManager(str(config_path))
            managers.append(manager)

        # All should have same configuration
        for manager in managers:
            assert manager.current_profile.role_title == "Test"
            assert len(manager.current_profile.enabled_domains) == 1

        # Test concurrent calculations
        import threading
        import time

        results = []

        def calculate_score(manager):
            score = manager.calculate_organizational_impact_score({"test_metric": 0.7})
            results.append(score)

        threads = []
        for manager in managers:
            thread = threading.Thread(target=calculate_score, args=(manager,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # All calculations should produce same result
        assert len(results) == 5
        assert all(abs(score - results[0]) < 0.001 for score in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])
