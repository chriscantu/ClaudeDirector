"""
Unit tests for Template Commands CLI Interface

Tests the CLI command implementations for template management including
listing, discovery, validation, and comparison operations.
"""

import unittest
from unittest.mock import Mock, patch
import json

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from lib.p1_features.template_commands import (
    TemplateCommands,
    DEFAULT_CONFIDENCE_THRESHOLD,
)
from lib.core.template_engine import (
    TemplateDiscoveryEngine,
    DirectorTemplate,
    TemplatePersonaConfig,
    TemplateActivationKeywords,
)


class TestTemplateCommands(unittest.TestCase):
    """Test TemplateCommands CLI interface"""

    def setUp(self):
        """Set up test fixtures"""
        # Create mock template engine
        self.mock_engine = Mock(spec=TemplateDiscoveryEngine)
        self.template_commands = TemplateCommands(template_engine=self.mock_engine)

        # Create test template objects
        self.mobile_template = DirectorTemplate(
            template_id="mobile_director",
            domain="mobile_platforms",
            display_name="Mobile Engineering Director",
            description="iOS/Android platform strategy and mobile DevOps",
            personas=TemplatePersonaConfig(
                primary=["marcus", "sofia"],
                contextual=["diego", "martin"],
                fallback=["camille"],
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={"mobile app": 0.9}
            ),
            strategic_priorities=["platform_unification", "developer_experience"],
            metrics_focus=["app_performance", "release_velocity"],
        )

        self.product_template = DirectorTemplate(
            template_id="product_engineering_director",
            domain="product_engineering",
            display_name="Product Engineering Director",
            description="Product strategy execution and customer-driven engineering",
            personas=TemplatePersonaConfig(
                primary=["alvaro", "rachel"],
                contextual=["diego", "data"],
                fallback=["camille"],
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={"product strategy": 0.95}
            ),
            strategic_priorities=["product_market_fit_engineering"],
            metrics_focus=["feature_adoption_rate"],
        )

    def test_list_templates_table_format(self):
        """Test listing templates in table format"""
        self.mock_engine.list_templates.return_value = [
            self.mobile_template,
            self.product_template,
        ]

        result = self.template_commands.list_templates(format_type="table")

        self.assertIn("Available Director Templates", result)
        self.assertIn("mobile_director", result)
        self.assertIn("Mobile Engineering Director", result)
        self.assertIn("product_engineering_director", result)
        self.assertIn("Product Engineering Director", result)
        self.mock_engine.list_templates.assert_called_once_with(domain_filter=None)

    def test_list_templates_json_format(self):
        """Test listing templates in JSON format"""
        self.mock_engine.list_templates.return_value = [self.mobile_template]

        result = self.template_commands.list_templates(format_type="json")

        # Should be valid JSON
        data = json.loads(result)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "mobile_director")
        self.assertEqual(data[0]["name"], "Mobile Engineering Director")
        self.assertEqual(data[0]["domain"], "mobile_platforms")

    def test_list_templates_with_domain_filter(self):
        """Test listing templates with domain filter"""
        self.mock_engine.list_templates.return_value = [self.mobile_template]

        result = self.template_commands.list_templates(domain="mobile_platforms")

        self.mock_engine.list_templates.assert_called_once_with(
            domain_filter="mobile_platforms"
        )
        self.assertIn("mobile_director", result)

    def test_list_templates_empty(self):
        """Test listing templates when no templates are found"""
        self.mock_engine.list_templates.return_value = []

        result = self.template_commands.list_templates()

        self.assertIn("No templates found", result)
        self.assertIn("⚠️", result)  # Warning icon

    def test_list_templates_error(self):
        """Test error handling in list_templates"""
        self.mock_engine.list_templates.side_effect = Exception("Test error")

        result = self.template_commands.list_templates()

        self.assertIn("Failed to list templates", result)
        self.assertIn("❌", result)  # Error icon

    def test_get_template_details_yaml_format(self):
        """Test getting template details in YAML format"""
        self.mock_engine.get_template.return_value = self.mobile_template

        result = self.template_commands.get_template_details(
            "mobile_director", format_type="yaml"
        )

        self.assertIn("# Mobile Engineering Director", result)
        self.assertIn("**Template ID**: mobile_director", result)
        self.assertIn("**Domain**: mobile_platforms", result)
        self.assertIn("**Primary**: marcus, sofia", result)
        self.assertIn("• platform_unification", result)
        self.mock_engine.get_template.assert_called_once_with("mobile_director")

    def test_get_template_details_json_format(self):
        """Test getting template details in JSON format"""
        self.mock_engine.get_template.return_value = self.mobile_template

        result = self.template_commands.get_template_details(
            "mobile_director", format_type="json"
        )

        # Should be valid JSON
        data = json.loads(result)
        self.assertEqual(data["template_id"], "mobile_director")
        self.assertEqual(data["display_name"], "Mobile Engineering Director")
        self.assertEqual(data["domain"], "mobile_platforms")
        self.assertEqual(data["personas"]["primary"], ["marcus", "sofia"])

    def test_get_template_details_not_found(self):
        """Test getting details for non-existent template"""
        self.mock_engine.get_template.return_value = None

        result = self.template_commands.get_template_details("nonexistent")

        self.assertIn("Template not found: nonexistent", result)
        self.assertIn("❌", result)

    def test_discover_by_context_success(self):
        """Test successful template discovery by context"""
        self.mock_engine.discover_templates_by_context.return_value = [
            (self.mobile_template, 0.9)
        ]

        result = self.template_commands.discover_by_context("mobile app development")

        self.assertIn(
            "**Template Discovery Results for**: 'mobile app development'", result
        )
        self.assertIn("**1. Mobile Engineering Director** (90% match)", result)
        self.assertIn("**Domain**: mobile_platforms", result)
        self.assertIn("**Primary Personas**: marcus, sofia", result)
        self.mock_engine.discover_templates_by_context.assert_called_once_with(
            "mobile app development", DEFAULT_CONFIDENCE_THRESHOLD
        )

    def test_discover_by_context_custom_threshold(self):
        """Test template discovery with custom threshold"""
        self.mock_engine.discover_templates_by_context.return_value = []

        self.template_commands.discover_by_context("test context", threshold=0.8)

        self.mock_engine.discover_templates_by_context.assert_called_once_with(
            "test context", 0.8
        )

    def test_discover_by_context_no_results(self):
        """Test template discovery when no results found"""
        self.mock_engine.discover_templates_by_context.return_value = []

        result = self.template_commands.discover_by_context("unrelated context")

        self.assertIn("No templates found for context: 'unrelated context'", result)
        self.assertIn("⚠️", result)

    def test_discover_by_context_many_results(self):
        """Test template discovery with many results (should limit to 5)"""
        results = [(self.mobile_template, 0.9 - i * 0.1) for i in range(7)]  # 7 results
        self.mock_engine.discover_templates_by_context.return_value = results

        result = self.template_commands.discover_by_context("test context")

        # Should show top 5 results plus "... and X more results"
        self.assertIn("... and 2 more results", result)

    def test_validate_selection_valid(self):
        """Test template selection validation for valid selection"""
        self.mock_engine.validate_template_selection.return_value = {
            "valid": True,
            "template": self.mobile_template,
            "warnings": [],
        }

        result = self.template_commands.validate_selection(
            "mobile_director", "fintech", "startup"
        )

        self.assertIn(
            "✅ Template selection valid: Mobile Engineering Director", result
        )
        self.mock_engine.validate_template_selection.assert_called_once_with(
            "mobile_director", "fintech", "startup"
        )

    def test_validate_selection_with_warnings(self):
        """Test template selection validation with warnings"""
        self.mock_engine.validate_template_selection.return_value = {
            "valid": True,
            "template": self.mobile_template,
            "warnings": ["Industry 'unknown' not specifically supported"],
        }

        result = self.template_commands.validate_selection(
            "mobile_director", "unknown", None
        )

        self.assertIn("✅ Template selection valid", result)
        self.assertIn("**Warnings:**", result)
        self.assertIn("⚠️  Industry 'unknown' not specifically supported", result)

    def test_validate_selection_invalid(self):
        """Test template selection validation for invalid selection"""
        self.mock_engine.validate_template_selection.return_value = {
            "valid": False,
            "error": "Template not found: nonexistent",
        }

        result = self.template_commands.validate_selection("nonexistent")

        self.assertIn("Template not found: nonexistent", result)
        self.assertIn("❌", result)

    def test_generate_summary_success(self):
        """Test successful template summary generation"""
        summary_data = {
            "template_id": "mobile_director",
            "display_name": "Mobile Engineering Director",
            "domain": "mobile_platforms",
            "description": "iOS/Android platform strategy",
            "primary_personas": ["marcus", "sofia"],
            "strategic_priorities": ["platform_unification"],
            "metrics_focus": ["app_performance"],
            "industry_enhancements": {
                "enhanced_priorities": ["security_compliance"],
                "enhanced_metrics": ["transaction_security"],
            },
            "team_size_context": {
                "focus_areas": ["mvp_velocity"],
                "key_challenges": ["resource_constraints"],
            },
        }
        self.mock_engine.generate_template_summary.return_value = summary_data

        result = self.template_commands.generate_summary(
            "mobile_director", "fintech", "startup"
        )

        self.assertIn("# Mobile Engineering Director - Configuration Summary", result)
        self.assertIn("**Template ID**: mobile_director", result)
        self.assertIn("## Primary Personas", result)
        self.assertIn("• marcus", result)
        self.assertIn("## Industry-Specific Enhancements", result)
        self.assertIn("**Enhanced Priorities**: • security_compliance", result)
        self.assertIn("## Team Size Context", result)
        self.assertIn("**Focus Areas**: • mvp_velocity", result)
        self.mock_engine.generate_template_summary.assert_called_once_with(
            "mobile_director", "fintech", "startup"
        )

    def test_generate_summary_template_not_found(self):
        """Test summary generation for non-existent template"""
        self.mock_engine.generate_template_summary.return_value = {
            "error": "Template not found: nonexistent"
        }

        result = self.template_commands.generate_summary("nonexistent")

        self.assertIn("Template not found: nonexistent", result)
        self.assertIn("❌", result)

    def test_compare_templates_success(self):
        """Test successful template comparison"""
        comparison_data = {
            "templates": {
                "mobile_director": {
                    "display_name": "Mobile Engineering Director",
                    "description": "iOS/Android platform strategy",
                    "domain": "mobile_platforms",
                    "primary_personas": ["marcus", "sofia"],
                    "strategic_priorities": [
                        "platform_unification",
                        "developer_experience",
                    ],
                    "metrics_focus": ["app_performance", "release_velocity"],
                },
                "product_engineering_director": {
                    "display_name": "Product Engineering Director",
                    "description": "Product strategy execution",
                    "domain": "product_engineering",
                    "primary_personas": ["alvaro", "rachel"],
                    "strategic_priorities": ["product_market_fit_engineering"],
                    "metrics_focus": ["feature_adoption_rate"],
                },
            }
        }
        self.mock_engine.get_template_comparison.return_value = comparison_data

        result = self.template_commands.compare_templates(
            ["mobile_director", "product_engineering_director"]
        )

        self.assertIn("# Template Comparison", result)
        self.assertIn("Mobile Engineering Director", result)
        self.assertIn("Product Engineering Director", result)
        self.assertIn("mobile_platforms", result)
        self.assertIn("product_engineering", result)
        self.mock_engine.get_template_comparison.assert_called_once_with(
            ["mobile_director", "product_engineering_director"]
        )

    def test_compare_templates_error(self):
        """Test template comparison with error"""
        self.mock_engine.get_template_comparison.return_value = {
            "error": "Cannot compare more than 4 templates at once"
        }

        result = self.template_commands.compare_templates(
            ["t1", "t2", "t3", "t4", "t5"]
        )

        self.assertIn("Cannot compare more than 4 templates at once", result)
        self.assertIn("❌", result)

    def test_compare_templates_no_valid_templates(self):
        """Test template comparison with no valid templates"""
        comparison_data = {"templates": {}}
        self.mock_engine.get_template_comparison.return_value = comparison_data

        result = self.template_commands.compare_templates(
            ["nonexistent1", "nonexistent2"]
        )

        self.assertIn("No valid templates found for comparison", result)
        self.assertIn("⚠️", result)

    def test_list_domains_success(self):
        """Test successful domain listing"""
        self.mock_engine.get_domains.return_value = [
            "mobile_platforms",
            "product_engineering",
        ]
        self.mock_engine.list_templates.side_effect = [
            [self.mobile_template],  # 1 template for mobile_platforms
            [self.product_template],  # 1 template for product_engineering
        ]

        result = self.template_commands.list_domains()

        self.assertIn("**Available Template Domains:**", result)
        self.assertIn("- **mobile_platforms** (1 template)", result)
        self.assertIn("- **product_engineering** (1 template)", result)

    def test_list_domains_empty(self):
        """Test domain listing when no domains found"""
        self.mock_engine.get_domains.return_value = []

        result = self.template_commands.list_domains()

        self.assertIn("No template domains found", result)
        self.assertIn("⚠️", result)

    def test_default_confidence_threshold(self):
        """Test that default confidence threshold is used correctly"""
        self.assertEqual(DEFAULT_CONFIDENCE_THRESHOLD, 0.6)

        # Test that it's used in discover_by_context when no threshold provided
        self.mock_engine.discover_templates_by_context.return_value = []
        self.template_commands.discover_by_context("test context")

        self.mock_engine.discover_templates_by_context.assert_called_with(
            "test context", DEFAULT_CONFIDENCE_THRESHOLD
        )


class TestTemplateCommandsIntegration(unittest.TestCase):
    """Integration tests for TemplateCommands with real TemplateDiscoveryEngine"""

    def setUp(self):
        """Set up test fixtures with real template engine"""
        # Use real engine but with mock config loading
        with patch("pathlib.Path.exists", return_value=False):
            self.template_commands = TemplateCommands()

    def test_commands_with_empty_engine(self):
        """Test that commands handle empty template engine gracefully"""
        result = self.template_commands.list_templates()
        self.assertIn("No templates found", result)

        result = self.template_commands.get_template_details("nonexistent")
        self.assertIn("Template not found", result)

        result = self.template_commands.discover_by_context("test context")
        self.assertIn("No templates found", result)

        result = self.template_commands.list_domains()
        self.assertIn("No template domains found", result)

    def test_dependency_injection(self):
        """Test that dependency injection works correctly"""
        mock_engine = Mock(spec=TemplateDiscoveryEngine)
        commands = TemplateCommands(template_engine=mock_engine)

        self.assertIs(commands.template_engine, mock_engine)

    def test_default_engine_creation(self):
        """Test that default engine is created when none provided"""
        with patch(
            "claudedirector.p1_features.template_commands.TemplateDiscoveryEngine"
        ) as mock_engine_class:
            mock_instance = Mock()
            mock_engine_class.return_value = mock_instance

            commands = TemplateCommands()

            mock_engine_class.assert_called_once()
            self.assertIs(commands.template_engine, mock_instance)


if __name__ == "__main__":
    unittest.main()
