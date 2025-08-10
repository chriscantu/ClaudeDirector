"""
Functional tests for Template System Integration

Tests the end-to-end functionality of the template system including
CLI integration, template discovery workflows, and real configuration loading.
"""

import unittest
import tempfile
import os
import yaml
from pathlib import Path
import subprocess
import json

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from claudedirector.core.template_engine import TemplateDiscoveryEngine
from claudedirector.p1_features.template_commands import TemplateCommands


class TestTemplateSystemIntegration(unittest.TestCase):
    """Functional tests for complete template system integration"""

    def setUp(self):
        """Set up test environment with temporary config file"""
        # Create temporary directory and config file
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / "test_director_templates.yaml"

        # Create test configuration
        self.test_config = {
            "schema_version": "1.0.0",
            "metadata": {
                "generated_at": "2025-01-15T12:00:00Z",
                "generated_by": "Test Suite",
                "total_templates": 3,
                "supported_domains": ["mobile_platforms", "product_engineering", "infrastructure_devops"]
            },
            "templates": {
                "mobile_director": {
                    "domain": "mobile_platforms",
                    "display_name": "Mobile Engineering Director",
                    "description": "iOS/Android platform strategy, mobile DevOps, and app performance optimization",
                    "industry_modifiers": {
                        "fintech": {
                            "priorities": ["security_compliance", "payment_processing"],
                            "metrics": ["transaction_security", "compliance_audit_score"]
                        },
                        "consumer": {
                            "priorities": ["user_experience", "app_store_optimization"],
                            "metrics": ["app_store_rating", "user_retention"]
                        }
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["mvp_velocity", "platform_foundation"],
                            "challenges": ["resource_constraints", "technical_debt"]
                        },
                        "scale": {
                            "focus": ["platform_unification", "team_coordination"],
                            "challenges": ["cross_platform_consistency", "team_scaling"]
                        }
                    },
                    "personas": {
                        "primary": ["marcus", "sofia", "elena"],
                        "contextual": ["diego", "martin", "security"],
                        "fallback": ["camille", "rachel"]
                    },
                    "activation_keywords": {
                        "mobile app": 0.9,
                        "ios development": 0.95,
                        "android platform": 0.9,
                        "app store": 0.8,
                        "mobile performance": 0.85
                    },
                    "strategic_priorities": [
                        "platform_unification",
                        "developer_experience",
                        "market_speed",
                        "performance_optimization",
                        "security_compliance"
                    ],
                    "metrics_focus": [
                        "app_performance",
                        "release_velocity",
                        "user_adoption",
                        "platform_consistency",
                        "developer_productivity"
                    ]
                },
                "product_engineering_director": {
                    "domain": "product_engineering",
                    "display_name": "Product Engineering Director",
                    "description": "Product strategy execution, user experience optimization, and customer-driven engineering delivery",
                    "industry_modifiers": {
                        "saas": {
                            "priorities": ["customer_retention_engineering", "product_analytics"],
                            "metrics": ["monthly_active_users", "feature_adoption_rate"]
                        }
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["mvp_product_fit", "user_feedback_loops"],
                            "challenges": ["feature_prioritization", "technical_debt_vs_features"]
                        }
                    },
                    "personas": {
                        "primary": ["alvaro", "rachel", "camille"],
                        "contextual": ["diego", "marcus", "data"],
                        "fallback": ["martin", "security"]
                    },
                    "activation_keywords": {
                        "product strategy": 0.95,
                        "user experience": 0.9,
                        "product roadmap": 0.9,
                        "customer feedback": 0.85,
                        "feature delivery": 0.85
                    },
                    "strategic_priorities": [
                        "product_market_fit_engineering",
                        "user_experience_optimization",
                        "feature_delivery_velocity",
                        "data_driven_development",
                        "customer_feedback_integration"
                    ],
                    "metrics_focus": [
                        "feature_adoption_rate",
                        "user_satisfaction_scores",
                        "product_velocity_metrics",
                        "customer_conversion_impact",
                        "technical_debt_vs_feature_ratio"
                    ]
                },
                "infrastructure_director": {
                    "domain": "infrastructure_devops",
                    "display_name": "Infrastructure & DevOps Director",
                    "description": "Cloud platforms, reliability engineering, and DevOps transformation",
                    "industry_modifiers": {
                        "fintech": {
                            "priorities": ["regulatory_compliance", "financial_security"],
                            "metrics": ["compliance_coverage", "security_incidents"]
                        }
                    },
                    "team_size_contexts": {
                        "enterprise": {
                            "focus": ["enterprise_governance", "compliance_frameworks"],
                            "challenges": ["legacy_migration", "regulatory_requirements"]
                        }
                    },
                    "personas": {
                        "primary": ["martin", "security", "david"],
                        "contextual": ["diego", "camille", "sofia"],
                        "fallback": ["alvaro", "elena"]
                    },
                    "activation_keywords": {
                        "infrastructure": 0.95,
                        "devops": 0.9,
                        "cloud platform": 0.9,
                        "kubernetes": 0.85,
                        "reliability": 0.85
                    },
                    "strategic_priorities": [
                        "platform_reliability",
                        "cost_optimization",
                        "security_posture",
                        "operational_excellence",
                        "scalability_planning"
                    ],
                    "metrics_focus": [
                        "system_reliability",
                        "cost_efficiency",
                        "deployment_velocity",
                        "security_posture",
                        "operational_efficiency"
                    ]
                }
            },
            "global_settings": {
                "default_fallback_personas": ["camille", "diego", "alvaro"],
                "activation_thresholds": {
                    "high_confidence": 0.8,
                    "medium_confidence": 0.6,
                    "low_confidence": 0.4
                },
                "selection_weights": {
                    "domain_match": 0.4,
                    "industry_match": 0.3,
                    "team_size_match": 0.2,
                    "keyword_confidence": 0.1
                }
            }
        }

        # Write config to file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config, f)

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_template_engine_loads_config_successfully(self):
        """Test that template engine loads configuration correctly"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Verify templates were loaded
        self.assertEqual(len(engine.templates), 3)
        self.assertIn("mobile_director", engine.templates)
        self.assertIn("product_engineering_director", engine.templates)
        self.assertIn("infrastructure_director", engine.templates)

        # Verify global settings were loaded
        self.assertIn("activation_thresholds", engine.global_settings)
        self.assertEqual(engine.global_settings["activation_thresholds"]["high_confidence"], 0.8)

    def test_template_discovery_workflow(self):
        """Test complete template discovery workflow"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Test mobile context discovery
        mobile_results = engine.discover_templates_by_context("mobile app performance issues", threshold=0.7)
        self.assertEqual(len(mobile_results), 1)
        template, confidence = mobile_results[0]
        self.assertEqual(template.template_id, "mobile_director")
        self.assertGreater(confidence, 0.8)

        # Test product context discovery
        product_results = engine.discover_templates_by_context("product strategy and user experience", threshold=0.7)
        self.assertEqual(len(product_results), 1)
        template, confidence = product_results[0]
        self.assertEqual(template.template_id, "product_engineering_director")
        self.assertGreater(confidence, 0.9)

        # Test infrastructure context discovery
        infra_results = engine.discover_templates_by_context("kubernetes infrastructure and devops", threshold=0.7)
        self.assertEqual(len(infra_results), 1)
        template, confidence = infra_results[0]
        self.assertEqual(template.template_id, "infrastructure_director")
        self.assertGreater(confidence, 0.8)

    def test_template_validation_workflow(self):
        """Test template validation with different contexts"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Test valid template with supported modifiers
        result = engine.validate_template_selection("mobile_director", "fintech", "startup")
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["warnings"]), 0)

        # Test valid template with unsupported modifiers
        result = engine.validate_template_selection("mobile_director", "unsupported_industry", "unsupported_size")
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["warnings"]), 2)

        # Test invalid template
        result = engine.validate_template_selection("nonexistent_template")
        self.assertFalse(result["valid"])
        self.assertIn("Template not found", result["error"])

    def test_template_summary_generation_workflow(self):
        """Test template summary generation with different contexts"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Test mobile director summary with fintech + startup context
        summary = engine.generate_template_summary("mobile_director", "fintech", "startup")

        self.assertEqual(summary["template_id"], "mobile_director")
        self.assertEqual(summary["display_name"], "Mobile Engineering Director")
        self.assertIn("industry_enhancements", summary)
        self.assertIn("team_size_context", summary)

        # Verify industry enhancements
        enhancements = summary["industry_enhancements"]
        self.assertIn("security_compliance", enhancements["enhanced_priorities"])
        self.assertIn("transaction_security", enhancements["enhanced_metrics"])

        # Verify team size context
        team_context = summary["team_size_context"]
        self.assertIn("mvp_velocity", team_context["focus_areas"])
        self.assertIn("resource_constraints", team_context["key_challenges"])

    def test_template_comparison_workflow(self):
        """Test template comparison functionality"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Compare mobile and product templates
        comparison = engine.get_template_comparison(["mobile_director", "product_engineering_director"])

        self.assertIn("templates", comparison)
        self.assertEqual(len(comparison["templates"]), 2)

        # Verify mobile template data
        mobile_data = comparison["templates"]["mobile_director"]
        self.assertEqual(mobile_data["display_name"], "Mobile Engineering Director")
        self.assertEqual(mobile_data["domain"], "mobile_platforms")
        self.assertIn("marcus", mobile_data["primary_personas"])

        # Verify product template data
        product_data = comparison["templates"]["product_engineering_director"]
        self.assertEqual(product_data["display_name"], "Product Engineering Director")
        self.assertEqual(product_data["domain"], "product_engineering")
        self.assertIn("alvaro", product_data["primary_personas"])

    def test_template_commands_integration(self):
        """Test template commands integration with real engine"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)
        commands = TemplateCommands(template_engine=engine)

        # Test list command
        result = commands.list_templates()
        self.assertIn("Available Director Templates", result)
        self.assertIn("mobile_director", result)
        self.assertIn("product_engineering_director", result)
        self.assertIn("infrastructure_director", result)

        # Test discover command
        result = commands.discover_by_context("mobile app development")
        self.assertIn("Mobile Engineering Director", result)
        self.assertIn("90% match", result)  # Should be high confidence

        # Test show command
        result = commands.get_template_details("mobile_director")
        self.assertIn("Mobile Engineering Director", result)
        self.assertIn("mobile_platforms", result)
        self.assertIn("marcus, sofia, elena", result)

        # Test summary command
        result = commands.generate_summary("mobile_director", "fintech", "startup")
        self.assertIn("Mobile Engineering Director - Configuration Summary", result)
        self.assertIn("Industry-Specific Enhancements", result)
        self.assertIn("Team Size Context", result)

        # Test compare command
        result = commands.compare_templates(["mobile_director", "product_engineering_director"])
        self.assertIn("Template Comparison", result)
        self.assertIn("Mobile Engineering Director", result)
        self.assertIn("Product Engineering Director", result)

        # Test domains command
        result = commands.list_domains()
        self.assertIn("mobile_platforms", result)
        self.assertIn("product_engineering", result)
        self.assertIn("infrastructure_devops", result)

    def test_multi_keyword_activation_confidence(self):
        """Test activation confidence with multiple keywords"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Test text with multiple mobile keywords
        mobile_template = engine.get_template("mobile_director")
        confidence = mobile_template.get_activation_confidence("Our iOS development team needs better mobile app performance")
        self.assertGreater(confidence, 0.9)  # Should get ios development confidence (0.95)

        # Test text with single keyword
        confidence = mobile_template.get_activation_confidence("We need better app store optimization")
        self.assertAlmostEqual(confidence, 0.8, places=1)  # Should get app store confidence

        # Test text with no matching keywords
        confidence = mobile_template.get_activation_confidence("Database optimization and backend scaling")
        self.assertEqual(confidence, 0.0)

    def test_template_domain_filtering(self):
        """Test template listing with domain filtering"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        # Test mobile domain filtering
        mobile_templates = engine.list_templates(domain_filter="mobile_platforms")
        self.assertEqual(len(mobile_templates), 1)
        self.assertEqual(mobile_templates[0].template_id, "mobile_director")

        # Test product domain filtering
        product_templates = engine.list_templates(domain_filter="product_engineering")
        self.assertEqual(len(product_templates), 1)
        self.assertEqual(product_templates[0].template_id, "product_engineering_director")

        # Test non-existent domain filtering
        empty_templates = engine.list_templates(domain_filter="nonexistent_domain")
        self.assertEqual(len(empty_templates), 0)

        # Test no filtering (all templates)
        all_templates = engine.list_templates()
        self.assertEqual(len(all_templates), 3)

    def test_persona_hierarchy_validation(self):
        """Test that persona hierarchies are correctly parsed and accessible"""
        engine = TemplateDiscoveryEngine(templates_config_path=self.config_path)

        mobile_template = engine.get_template("mobile_director")

        # Test persona hierarchy
        self.assertEqual(mobile_template.personas.primary, ["marcus", "sofia", "elena"])
        self.assertEqual(mobile_template.personas.contextual, ["diego", "martin", "security"])
        self.assertEqual(mobile_template.personas.fallback, ["camille", "rachel"])

        # Test all personas method
        all_personas = mobile_template.personas.get_all_personas()
        expected = ["marcus", "sofia", "elena", "diego", "martin", "security", "camille", "rachel"]
        self.assertEqual(all_personas, expected)

        # Test primary persona selection
        primary = mobile_template.personas.get_primary_persona()
        self.assertEqual(primary, "marcus")

    def test_error_handling_robustness(self):
        """Test error handling for various edge cases"""
        # Test with invalid config path
        engine = TemplateDiscoveryEngine(templates_config_path=Path("/nonexistent/path/config.yaml"))
        self.assertEqual(len(engine.templates), 0)

        # Test commands with empty engine
        commands = TemplateCommands(template_engine=engine)

        result = commands.list_templates()
        self.assertIn("No templates found", result)

        result = commands.get_template_details("nonexistent")
        self.assertIn("Template not found", result)

        result = commands.discover_by_context("any context")
        self.assertIn("No templates found", result)

        result = commands.list_domains()
        self.assertIn("No template domains found", result)


class TestTemplateSystemCLIIntegration(unittest.TestCase):
    """Test CLI integration with template system (requires claudedirector CLI)"""

    def setUp(self):
        """Set up for CLI testing"""
        # Check if claudedirector CLI is available
        self.cli_available = os.path.exists("./claudedirector")
        if not self.cli_available:
            self.skipTest("claudedirector CLI not available for testing")

    def test_cli_templates_list_command(self):
        """Test templates list command via CLI"""
        if not self.cli_available:
            self.skipTest("CLI not available")

        result = subprocess.run(
            ["./claudedirector", "templates", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should not error out
        self.assertEqual(result.returncode, 0)
        self.assertIn("Director Template Management", result.stdout)

    def test_cli_templates_domains_command(self):
        """Test templates domains command via CLI"""
        if not self.cli_available:
            self.skipTest("CLI not available")

        result = subprocess.run(
            ["./claudedirector", "templates", "domains"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should not error out
        self.assertEqual(result.returncode, 0)
        self.assertIn("Director Template Management", result.stdout)

    def test_cli_templates_help_command(self):
        """Test templates help command via CLI"""
        if not self.cli_available:
            self.skipTest("CLI not available")

        result = subprocess.run(
            ["./claudedirector", "templates", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should show help
        self.assertEqual(result.returncode, 0)
        self.assertIn("template management", result.stdout.lower())


if __name__ == '__main__':
    unittest.main()
