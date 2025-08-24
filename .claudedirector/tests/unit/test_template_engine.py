"""
Unit tests for Template Discovery Engine

Tests the core template discovery functionality including template loading,
validation, discovery by context, and template management operations.
"""

import unittest
from unittest.mock import patch, mock_open
import yaml

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from claudedirector.core.template_engine import (
    TemplateDiscoveryEngine,
    DirectorTemplate,
    TemplatePersonaConfig,
    TemplateActivationKeywords,
    IndustryModifier,
    TeamSizeContext,
    TemplateValidationError,
)


class TestTemplateActivationKeywords(unittest.TestCase):
    """Test TemplateActivationKeywords functionality"""

    def setUp(self):
        self.keywords = TemplateActivationKeywords(
            keywords={
                "mobile app": 0.9,
                "ios development": 0.95,
                "android platform": 0.9,
                "platform engineering": 0.8,
            }
        )

    def test_get_confidence_exact_match(self):
        """Test confidence scoring for exact keyword matches"""
        confidence = self.keywords.get_confidence("Our mobile app needs improvement")
        self.assertAlmostEqual(confidence, 0.9, places=2)

    def test_get_confidence_case_insensitive(self):
        """Test that confidence detection is case insensitive"""
        confidence = self.keywords.get_confidence("MOBILE APP performance")
        self.assertAlmostEqual(confidence, 0.9, places=2)

    def test_get_confidence_multiple_keywords(self):
        """Test that highest confidence is returned when multiple keywords match"""
        confidence = self.keywords.get_confidence("iOS development for mobile app")
        self.assertAlmostEqual(
            confidence, 0.95, places=2
        )  # ios development has higher confidence

    def test_get_confidence_no_match(self):
        """Test that zero confidence is returned when no keywords match"""
        confidence = self.keywords.get_confidence("database optimization strategies")
        self.assertEqual(confidence, 0.0)

    def test_get_confidence_partial_match(self):
        """Test confidence scoring for partial keyword matches"""
        confidence = self.keywords.get_confidence("We need platform solutions")
        self.assertEqual(
            confidence, 0.0
        )  # "platform" alone doesn't match "platform engineering"


class TestTemplatePersonaConfig(unittest.TestCase):
    """Test TemplatePersonaConfig functionality"""

    def setUp(self):
        self.personas = TemplatePersonaConfig(
            primary=["alvaro", "rachel"],
            contextual=["diego", "martin"],
            fallback=["camille"],
        )

    def test_get_all_personas(self):
        """Test that all personas are returned in correct order"""
        all_personas = self.personas.get_all_personas()
        expected = ["alvaro", "rachel", "diego", "martin", "camille"]
        self.assertEqual(all_personas, expected)

    def test_get_primary_persona(self):
        """Test that first primary persona is returned"""
        primary = self.personas.get_primary_persona()
        self.assertEqual(primary, "alvaro")

    def test_get_primary_persona_empty(self):
        """Test that None is returned when no primary personas exist"""
        empty_personas = TemplatePersonaConfig(
            primary=[], contextual=["diego"], fallback=["camille"]
        )
        primary = empty_personas.get_primary_persona()
        self.assertIsNone(primary)


class TestDirectorTemplate(unittest.TestCase):
    """Test DirectorTemplate validation and functionality"""

    def setUp(self):
        self.valid_template_data = {
            "template_id": "test_director",
            "domain": "product_engineering",
            "display_name": "Test Director",
            "description": "Test template for unit testing",
            "personas": TemplatePersonaConfig(
                primary=["alvaro"], contextual=["rachel"], fallback=["camille"]
            ),
            "activation_keywords": TemplateActivationKeywords(keywords={"test": 0.9}),
            "strategic_priorities": ["test_priority"],
            "metrics_focus": ["test_metric"],
        }

    def test_valid_template_creation(self):
        """Test that valid template can be created successfully"""
        template = DirectorTemplate(**self.valid_template_data)
        self.assertEqual(template.template_id, "test_director")
        self.assertEqual(template.domain, "product_engineering")
        self.assertEqual(template.display_name, "Test Director")

    def test_template_validation_missing_id(self):
        """Test that template validation fails when ID is missing"""
        invalid_data = self.valid_template_data.copy()
        invalid_data["template_id"] = ""

        with self.assertRaises(TemplateValidationError) as context:
            DirectorTemplate(**invalid_data)
        self.assertIn("Template ID is required", str(context.exception))

    def test_template_validation_missing_domain(self):
        """Test that template validation fails when domain is missing"""
        invalid_data = self.valid_template_data.copy()
        invalid_data["domain"] = ""

        with self.assertRaises(TemplateValidationError) as context:
            DirectorTemplate(**invalid_data)
        self.assertIn("Template domain is required", str(context.exception))

    def test_template_validation_no_primary_personas(self):
        """Test that template validation fails when no primary personas exist"""
        invalid_data = self.valid_template_data.copy()
        invalid_data["personas"] = TemplatePersonaConfig(
            primary=[], contextual=["rachel"], fallback=["camille"]
        )

        with self.assertRaises(TemplateValidationError) as context:
            DirectorTemplate(**invalid_data)
        self.assertIn(
            "At least one primary persona is required", str(context.exception)
        )

    def test_template_validation_invalid_domain(self):
        """Test that template validation fails for unsupported domain"""
        invalid_data = self.valid_template_data.copy()
        invalid_data["domain"] = "invalid_domain"

        with self.assertRaises(TemplateValidationError) as context:
            DirectorTemplate(**invalid_data)
        self.assertIn("Unsupported template domain", str(context.exception))

    def test_get_activation_confidence(self):
        """Test activation confidence calculation"""
        template = DirectorTemplate(**self.valid_template_data)
        confidence = template.get_activation_confidence("This is a test context")
        self.assertAlmostEqual(confidence, 0.9, places=2)

    def test_get_optimal_persona(self):
        """Test optimal persona selection"""
        template = DirectorTemplate(**self.valid_template_data)
        persona = template.get_optimal_persona("test context")
        self.assertEqual(persona, "alvaro")  # Should return primary persona

    def test_apply_industry_modifier(self):
        """Test application of industry modifiers"""
        template_data = self.valid_template_data.copy()
        template_data["industry_modifiers"] = {
            "fintech": IndustryModifier(
                priorities=["security", "compliance"], metrics=["regulatory_score"]
            )
        }
        template = DirectorTemplate(**template_data)

        result = template.apply_industry_modifier("fintech")
        self.assertIn("enhanced_priorities", result)
        self.assertIn("enhanced_metrics", result)
        self.assertIn("security", result["enhanced_priorities"])
        self.assertIn("regulatory_score", result["enhanced_metrics"])

    def test_apply_industry_modifier_not_supported(self):
        """Test that empty dict is returned for unsupported industry"""
        template = DirectorTemplate(**self.valid_template_data)
        result = template.apply_industry_modifier("unsupported_industry")
        self.assertEqual(result, {})

    def test_apply_team_size_context(self):
        """Test application of team size contexts"""
        template_data = self.valid_template_data.copy()
        template_data["team_size_contexts"] = {
            "startup": TeamSizeContext(
                focus=["mvp", "rapid_iteration"], challenges=["resource_constraints"]
            )
        }
        template = DirectorTemplate(**template_data)

        result = template.apply_team_size_context("startup")
        self.assertIn("focus_areas", result)
        self.assertIn("key_challenges", result)
        self.assertIn("mvp", result["focus_areas"])
        self.assertIn("resource_constraints", result["key_challenges"])


class TestTemplateDiscoveryEngine(unittest.TestCase):
    """Test TemplateDiscoveryEngine functionality"""

    def setUp(self):
        # Create test template configuration
        self.test_config = {
            "global_settings": {
                "default_fallback_personas": ["camille", "diego", "alvaro"],
                "activation_thresholds": {
                    "high_confidence": 0.8,
                    "medium_confidence": 0.6,
                    "low_confidence": 0.4,
                },
            },
            "templates": {
                "mobile_director": {
                    "domain": "mobile_platforms",
                    "display_name": "Mobile Engineering Director",
                    "description": "iOS/Android platform strategy and mobile DevOps",
                    "personas": {
                        "primary": ["marcus", "sofia"],
                        "contextual": ["diego", "martin"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "mobile app": 0.9,
                        "ios development": 0.95,
                        "android platform": 0.9,
                    },
                    "strategic_priorities": [
                        "platform_unification",
                        "developer_experience",
                    ],
                    "metrics_focus": ["app_performance", "release_velocity"],
                    "industry_modifiers": {
                        "fintech": {
                            "priorities": ["security_compliance"],
                            "metrics": ["transaction_security"],
                        }
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["mvp_velocity"],
                            "challenges": ["resource_constraints"],
                        }
                    },
                },
                "product_engineering_director": {
                    "domain": "product_engineering",
                    "display_name": "Product Engineering Director",
                    "description": "Product strategy execution and customer-driven engineering",
                    "personas": {
                        "primary": ["alvaro", "rachel"],
                        "contextual": ["diego", "data"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "product strategy": 0.95,
                        "user experience": 0.9,
                        "feature delivery": 0.85,
                    },
                    "strategic_priorities": ["product_market_fit_engineering"],
                    "metrics_focus": ["feature_adoption_rate"],
                    "industry_modifiers": {},
                    "team_size_contexts": {},
                },
            },
        }

        # Create mock config file
        self.config_yaml = yaml.dump(self.test_config)

    @patch("pathlib.Path.exists")
    def test_load_templates_success(self, mock_exists):
        """Test successful template loading from configuration file"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()

        self.assertEqual(len(engine.templates), 2)
        self.assertIn("mobile_director", engine.templates)
        self.assertIn("product_engineering_director", engine.templates)

    @patch("pathlib.Path.exists")
    def test_load_templates_file_not_found(self, mock_exists):
        """Test graceful handling when config file doesn't exist"""
        mock_exists.return_value = False

        with patch("claudedirector.core.template_engine.logger") as mock_logger:
            engine = TemplateDiscoveryEngine()
            mock_logger.warning.assert_called_once()
            self.assertEqual(len(engine.templates), 0)

    @patch("pathlib.Path.exists")
    def test_list_templates(self, mock_exists):
        """Test template listing functionality"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        templates = engine.list_templates()

        self.assertEqual(len(templates), 2)
        # Should be sorted by display name
        self.assertEqual(templates[0].display_name, "Mobile Engineering Director")
        self.assertEqual(templates[1].display_name, "Product Engineering Director")

    @patch("pathlib.Path.exists")
    def test_list_templates_with_domain_filter(self, mock_exists):
        """Test template listing with domain filtering"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        templates = engine.list_templates(domain_filter="mobile_platforms")

        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].template_id, "mobile_director")

    @patch("pathlib.Path.exists")
    def test_get_template(self, mock_exists):
        """Test template retrieval by ID"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        template = engine.get_template("mobile_director")

        self.assertIsNotNone(template)
        self.assertEqual(template.template_id, "mobile_director")
        self.assertEqual(template.domain, "mobile_platforms")

    @patch("pathlib.Path.exists")
    def test_get_template_not_found(self, mock_exists):
        """Test template retrieval for non-existent template"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        template = engine.get_template("nonexistent_template")

        self.assertIsNone(template)

    @patch("pathlib.Path.exists")
    def test_discover_templates_by_context(self, mock_exists):
        """Test template discovery by context"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
            results = engine.discover_templates_by_context(
                "mobile app development", threshold=0.8
            )

        self.assertEqual(len(results), 1)
        template, confidence = results[0]
        self.assertEqual(template.template_id, "mobile_director")
        self.assertGreaterEqual(confidence, 0.8)

    @patch("pathlib.Path.exists")
    def test_discover_templates_no_match(self, mock_exists):
        """Test template discovery when no templates match threshold"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
            results = engine.discover_templates_by_context(
                "database optimization", threshold=0.8
            )

        self.assertEqual(len(results), 0)

    @patch("pathlib.Path.exists")
    def test_get_domains(self, mock_exists):
        """Test getting available template domains"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        domains = engine.get_domains()

        self.assertEqual(len(domains), 2)
        self.assertIn("mobile_platforms", domains)
        self.assertIn("product_engineering", domains)
        self.assertEqual(domains, sorted(domains))  # Should be sorted

    @patch("pathlib.Path.exists")
    def test_validate_template_selection_valid(self, mock_exists):
        """Test template selection validation for valid selection"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        result = engine.validate_template_selection(
            "mobile_director", "fintech", "startup"
        )

        self.assertTrue(result["valid"])
        self.assertIn("template", result)
        self.assertEqual(len(result["warnings"]), 0)

    @patch("pathlib.Path.exists")
    def test_validate_template_selection_invalid_template(self, mock_exists):
        """Test template selection validation for invalid template"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        result = engine.validate_template_selection("nonexistent_template")

        self.assertFalse(result["valid"])
        self.assertIn("error", result)
        self.assertIn("Template not found", result["error"])

    @patch("pathlib.Path.exists")
    def test_validate_template_selection_unsupported_modifiers(self, mock_exists):
        """Test template selection validation with unsupported modifiers"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        result = engine.validate_template_selection(
            "mobile_director", "unsupported_industry", "unsupported_size"
        )

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["warnings"]), 2)
        self.assertIn(
            "Industry 'unsupported_industry' not specifically supported",
            result["warnings"][0],
        )
        self.assertIn(
            "Team size 'unsupported_size' not specifically supported",
            result["warnings"][1],
        )

    @patch("pathlib.Path.exists")
    def test_generate_template_summary(self, mock_exists):
        """Test template summary generation"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        summary = engine.generate_template_summary(
            "mobile_director", "fintech", "startup"
        )

        self.assertEqual(summary["template_id"], "mobile_director")
        self.assertEqual(summary["display_name"], "Mobile Engineering Director")
        self.assertIn("industry_enhancements", summary)
        self.assertIn("team_size_context", summary)

    @patch("pathlib.Path.exists")
    def test_get_template_comparison(self, mock_exists):
        """Test template comparison functionality"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        comparison = engine.get_template_comparison(
            ["mobile_director", "product_engineering_director"]
        )

        self.assertIn("templates", comparison)
        self.assertEqual(len(comparison["templates"]), 2)
        self.assertIn("mobile_director", comparison["templates"])
        self.assertIn("product_engineering_director", comparison["templates"])

    @patch("pathlib.Path.exists")
    def test_get_template_comparison_too_many(self, mock_exists):
        """Test template comparison with too many templates"""
        mock_exists.return_value = True

        with patch("builtins.open", mock_open(read_data=self.config_yaml)):
            engine = TemplateDiscoveryEngine()
        comparison = engine.get_template_comparison(["t1", "t2", "t3", "t4", "t5"])

        self.assertIn("error", comparison)
        self.assertIn("Cannot compare more than 4 templates", comparison["error"])


if __name__ == "__main__":
    unittest.main()
