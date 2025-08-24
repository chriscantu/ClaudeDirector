"""
Unit tests for Dynamic Persona Activation Engine - Phase 2.1

Tests the core components of intelligent persona activation including
context analysis, persona selection, and conversation state management.
"""

import unittest
from unittest.mock import Mock
import time

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from lib.core.persona_activation_engine import (
    ContextAnalysisEngine,
    PersonaSelectionEngine,
    ConversationStateEngine,
    ContextResult,
    PersonaSelection,
    ConfidenceLevel,
)

from lib.core.template_engine import (
    TemplateDiscoveryEngine,
    DirectorTemplate,
    TemplatePersonaConfig,
    TemplateActivationKeywords,
)


class TestContextResult(unittest.TestCase):
    """Test ContextResult data structure and confidence level determination"""

    def test_confidence_level_high(self):
        """Test high confidence level assignment"""
        context = ContextResult(confidence=0.85)
        self.assertEqual(context.confidence_level, ConfidenceLevel.HIGH)

    def test_confidence_level_medium(self):
        """Test medium confidence level assignment"""
        context = ContextResult(confidence=0.65)
        self.assertEqual(context.confidence_level, ConfidenceLevel.MEDIUM)

    def test_confidence_level_low(self):
        """Test low confidence level assignment"""
        context = ContextResult(confidence=0.45)
        self.assertEqual(context.confidence_level, ConfidenceLevel.LOW)

    def test_confidence_level_none(self):
        """Test none confidence level assignment"""
        context = ContextResult(confidence=0.25)
        self.assertEqual(context.confidence_level, ConfidenceLevel.NONE)

    def test_to_dict_conversion(self):
        """Test conversion to dictionary"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.9,
            suggested_template="mobile_director",
            keywords=["mobile app", "ios"],
            detected_industry="fintech",
            detected_team_size="startup",
            analysis_time_ms=250,
        )

        result_dict = context.to_dict()

        self.assertEqual(result_dict["domain"], "mobile_platforms")
        self.assertEqual(result_dict["confidence"], 0.9)
        self.assertEqual(result_dict["suggested_template"], "mobile_director")
        self.assertEqual(result_dict["keywords"], ["mobile app", "ios"])
        self.assertEqual(result_dict["detected_industry"], "fintech")
        self.assertEqual(result_dict["detected_team_size"], "startup")
        self.assertEqual(result_dict["analysis_time_ms"], 250)
        self.assertEqual(result_dict["confidence_level"], "high")


class TestPersonaSelection(unittest.TestCase):
    """Test PersonaSelection data structure"""

    def test_persona_selection_creation(self):
        """Test persona selection creation with all fields"""
        selection = PersonaSelection(
            primary="alvaro",
            template_id="product_engineering_director",
            confidence=0.85,
            contextual=["rachel", "diego"],
            fallback="camille",
            rationale="High confidence product strategy match",
            selection_method="automatic_high_confidence",
            selection_time_ms=150,
            alternatives_considered=["alvaro", "rachel", "diego", "camille"],
        )

        self.assertEqual(selection.primary, "alvaro")
        self.assertEqual(selection.template_id, "product_engineering_director")
        self.assertEqual(selection.confidence, 0.85)
        self.assertEqual(selection.contextual, ["rachel", "diego"])
        self.assertEqual(selection.fallback, "camille")
        self.assertIn("High confidence", selection.rationale)

    def test_to_dict_conversion(self):
        """Test conversion to dictionary"""
        selection = PersonaSelection(
            primary="marcus", template_id="mobile_director", confidence=0.75
        )

        result_dict = selection.to_dict()

        self.assertEqual(result_dict["primary"], "marcus")
        self.assertEqual(result_dict["template_id"], "mobile_director")
        self.assertEqual(result_dict["confidence"], 0.75)
        self.assertIn("contextual", result_dict)
        self.assertIn("fallback", result_dict)


class TestContextAnalysisEngine(unittest.TestCase):
    """Test Context Analysis Engine functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create mock template discovery engine
        self.mock_template_discovery = Mock(spec=TemplateDiscoveryEngine)

        # Create test templates
        self.mobile_template = DirectorTemplate(
            template_id="mobile_director",
            domain="mobile_platforms",
            display_name="Mobile Engineering Director",
            description="iOS/Android platform strategy",
            personas=TemplatePersonaConfig(
                primary=["marcus", "sofia"], contextual=["diego"], fallback=["camille"]
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={
                    "mobile app": 0.9,
                    "ios development": 0.95,
                    "android platform": 0.9,
                }
            ),
        )

        self.product_template = DirectorTemplate(
            template_id="product_engineering_director",
            domain="product_engineering",
            display_name="Product Engineering Director",
            description="Product strategy execution",
            personas=TemplatePersonaConfig(
                primary=["alvaro", "rachel"], contextual=["diego"], fallback=["camille"]
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={
                    "product strategy": 0.95,
                    "user experience": 0.9,
                    "feature delivery": 0.85,
                }
            ),
        )

        # Configure mock
        self.mock_template_discovery.list_templates.return_value = [
            self.mobile_template,
            self.product_template,
        ]

        # Create engine
        self.engine = ContextAnalysisEngine(self.mock_template_discovery)

    def test_analyze_context_mobile_high_confidence(self):
        """Test context analysis for mobile domain with high confidence"""
        # Configure mock for template discovery
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.mobile_template, 0.9)
        ]

        result = self.engine.analyze_context("Our iOS app performance is declining")

        self.assertIsNotNone(result.domain)
        self.assertGreater(result.confidence, 0.8)
        self.assertEqual(result.suggested_template, "mobile_director")
        self.assertIn("ios", [k.lower() for k in result.keywords])
        self.assertLess(result.analysis_time_ms, 1000)  # Should be fast

    def test_analyze_context_product_strategy(self):
        """Test context analysis for product strategy domain"""
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.product_template, 0.95)
        ]

        result = self.engine.analyze_context(
            "We need to improve our product strategy and user experience"
        )

        self.assertGreater(result.confidence, 0.8)
        self.assertEqual(result.suggested_template, "product_engineering_director")
        self.assertIn("product strategy", result.keywords)

    def test_analyze_context_with_industry_detection(self):
        """Test context analysis with industry detection"""
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.mobile_template, 0.8)
        ]

        result = self.engine.analyze_context(
            "Our fintech mobile app needs better security compliance"
        )

        self.assertEqual(result.detected_industry, "fintech")
        self.assertIsNotNone(result.suggested_template)

    def test_analyze_context_with_team_size_detection(self):
        """Test context analysis with team size detection"""
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.product_template, 0.7)
        ]

        result = self.engine.analyze_context(
            "Our startup team of 8 engineers is struggling with product delivery"
        )

        self.assertEqual(result.detected_team_size, "startup")
        self.assertIsNotNone(result.suggested_template)

    def test_analyze_context_no_match(self):
        """Test context analysis when no clear match is found"""
        self.mock_template_discovery.discover_templates_by_context.return_value = []

        result = self.engine.analyze_context(
            "Random unrelated text about cooking recipes"
        )

        self.assertLess(result.confidence, 0.4)
        self.assertIsNone(result.suggested_template)
        self.assertEqual(result.confidence_level, ConfidenceLevel.NONE)

    def test_analyze_context_performance(self):
        """Test that context analysis meets performance requirements"""
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.mobile_template, 0.8)
        ]

        start_time = time.time()
        result = self.engine.analyze_context("Mobile app development challenges")
        analysis_time = (time.time() - start_time) * 1000

        # Should meet <500ms requirement
        self.assertLess(analysis_time, 500)
        self.assertLess(result.analysis_time_ms, 500)

    def test_industry_detection_patterns(self):
        """Test various industry detection patterns"""
        test_cases = [
            ("fintech mobile payment app", "fintech"),
            ("healthcare patient management system", "healthcare"),
            ("SaaS subscription platform", "saas"),
            ("ecommerce shopping cart optimization", "ecommerce"),
            ("gaming real-time multiplayer", "gaming"),
            ("corporate business application", None),  # No clear industry
        ]

        for text, expected_industry in test_cases:
            result = self.engine._detect_industry(text)
            self.assertEqual(result, expected_industry, f"Failed for: {text}")

    def test_team_size_detection_patterns(self):
        """Test various team size detection patterns"""
        test_cases = [
            ("our small startup team of 5 engineers", "startup"),
            ("scaling team with 25 developers", "scale"),
            ("enterprise team of 200 engineers", "enterprise"),
            ("we have some developers", None),  # No specific size
        ]

        for text, expected_size in test_cases:
            result = self.engine._detect_team_size(text)
            self.assertEqual(result, expected_size, f"Failed for: {text}")

    def test_error_handling(self):
        """Test error handling in context analysis"""
        # Configure mock to raise exception
        self.mock_template_discovery.discover_templates_by_context.side_effect = (
            Exception("Test error")
        )

        result = self.engine.analyze_context("test input")

        # Should return low-confidence result, not crash
        self.assertIsInstance(result, ContextResult)
        self.assertEqual(result.confidence, 0.0)
        self.assertIsNotNone(result.analysis_time_ms)


class TestPersonaSelectionEngine(unittest.TestCase):
    """Test Persona Selection Engine functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_template_discovery = Mock(spec=TemplateDiscoveryEngine)

        # Create test template
        self.test_template = DirectorTemplate(
            template_id="mobile_director",
            domain="mobile_platforms",
            display_name="Mobile Engineering Director",
            description="Test template",
            personas=TemplatePersonaConfig(
                primary=["marcus", "sofia"],
                contextual=["diego", "martin"],
                fallback=["camille"],
            ),
            activation_keywords=TemplateActivationKeywords(keywords={"mobile": 0.9}),
        )

        self.mock_template_discovery.get_template.return_value = self.test_template

        self.engine = PersonaSelectionEngine(self.mock_template_discovery)

    def test_select_persona_high_confidence(self):
        """Test persona selection with high confidence"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.85,
            suggested_template="mobile_director",
        )

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.primary, "marcus")  # First primary persona
        self.assertEqual(selection.template_id, "mobile_director")
        self.assertEqual(selection.confidence, 0.85)
        self.assertEqual(selection.selection_method, "automatic_high_confidence")
        self.assertIn("High confidence", selection.rationale)

    def test_select_persona_medium_confidence(self):
        """Test persona selection with medium confidence"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.65,
            suggested_template="mobile_director",
        )

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.primary, "diego")  # First contextual persona
        self.assertEqual(selection.selection_method, "automatic_medium_confidence")
        self.assertIn("Medium confidence", selection.rationale)

    def test_select_persona_low_confidence(self):
        """Test persona selection with low confidence"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.35,
            suggested_template="mobile_director",
        )

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.primary, "camille")  # Fallback persona
        self.assertEqual(selection.selection_method, "fallback_low_confidence")
        self.assertIn("Low confidence", selection.rationale)

    def test_select_persona_no_template(self):
        """Test persona selection when no template is suggested"""
        context = ContextResult(domain=None, confidence=0.2, suggested_template=None)

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.primary, "camille")  # Global fallback
        self.assertEqual(selection.template_id, "fallback")
        self.assertEqual(selection.selection_method, "global_fallback")

    def test_select_persona_template_not_found(self):
        """Test persona selection when template is not found"""
        self.mock_template_discovery.get_template.return_value = None

        context = ContextResult(
            domain="unknown_domain",
            confidence=0.8,
            suggested_template="nonexistent_template",
        )

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.primary, "camille")
        self.assertEqual(selection.selection_method, "global_fallback")

    def test_select_persona_with_override(self):
        """Test persona selection with template override"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.9,
            suggested_template="product_engineering_director",  # Different template
        )

        selection = self.engine.select_persona(
            context, override_template="mobile_director"
        )

        self.assertEqual(
            selection.template_id, "mobile_director"
        )  # Should use override
        self.assertEqual(selection.primary, "marcus")

    def test_select_persona_performance(self):
        """Test that persona selection meets performance requirements"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.8,
            suggested_template="mobile_director",
        )

        start_time = time.time()
        selection = self.engine.select_persona(context)
        selection_time = (time.time() - start_time) * 1000

        # Should meet <300ms requirement
        self.assertLess(selection_time, 300)
        self.assertLess(selection.selection_time_ms, 300)

    def test_contextual_personas_inclusion(self):
        """Test that contextual personas are included in selection"""
        context = ContextResult(
            domain="mobile_platforms",
            confidence=0.8,
            suggested_template="mobile_director",
        )

        selection = self.engine.select_persona(context)

        self.assertEqual(selection.contextual, ["diego", "martin"])
        self.assertEqual(selection.fallback, "camille")
        self.assertIn("marcus", selection.alternatives_considered)
        self.assertIn("diego", selection.alternatives_considered)


class TestConversationStateEngine(unittest.TestCase):
    """Test Conversation State Engine functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.engine = ConversationStateEngine()

        # Create test data
        self.test_context = ContextResult(
            domain="mobile_platforms",
            confidence=0.85,
            suggested_template="mobile_director",
            keywords=["mobile app"],
            analysis_time_ms=200,
        )

        self.test_selection = PersonaSelection(
            primary="marcus",
            template_id="mobile_director",
            confidence=0.85,
            contextual=["diego"],
            fallback="camille",
            rationale="High confidence mobile match",
            selection_method="automatic_high_confidence",
            selection_time_ms=150,
        )

    def test_initial_state(self):
        """Test initial conversation state"""
        state = self.engine.get_current_state()

        self.assertIsNone(state["active_persona"])
        self.assertIsNone(state["current_template_id"])
        self.assertEqual(state["total_activations"], 0)
        self.assertEqual(state["persona_usage_count"], {})

    def test_update_state(self):
        """Test state update with persona activation"""
        self.engine.update_state(
            self.test_selection,
            self.test_context,
            "Our mobile app needs performance optimization",
        )

        state = self.engine.get_current_state()

        self.assertEqual(state["active_persona"], "marcus")
        self.assertEqual(state["current_template_id"], "mobile_director")
        self.assertEqual(state["total_activations"], 1)
        self.assertEqual(state["persona_usage_count"]["marcus"], 1)
        self.assertIsNotNone(state["last_activation_time"])

    def test_multiple_activations(self):
        """Test state tracking with multiple activations"""
        # First activation
        self.engine.update_state(self.test_selection, self.test_context, "test input 1")

        # Second activation with different persona
        selection2 = PersonaSelection(
            primary="alvaro", template_id="product_engineering_director", confidence=0.7
        )
        context2 = ContextResult(domain="product_engineering", confidence=0.7)

        self.engine.update_state(selection2, context2, "test input 2")

        state = self.engine.get_current_state()

        self.assertEqual(state["active_persona"], "alvaro")  # Latest activation
        self.assertEqual(state["total_activations"], 2)
        self.assertEqual(state["persona_usage_count"]["marcus"], 1)
        self.assertEqual(state["persona_usage_count"]["alvaro"], 1)

    def test_activation_history(self):
        """Test activation history tracking"""
        self.engine.update_state(self.test_selection, self.test_context, "test input")

        history = self.engine.get_activation_history()

        self.assertEqual(len(history), 1)
        activation = history[0]
        self.assertEqual(activation["persona"], "marcus")
        self.assertEqual(activation["template_id"], "mobile_director")
        self.assertEqual(activation["user_input"], "test input")
        self.assertIn("context", activation)
        self.assertIn("timestamp", activation)

    def test_activation_history_limit(self):
        """Test activation history with limit"""
        # Add multiple activations
        for i in range(15):
            selection = PersonaSelection(
                primary=f"persona_{i}", template_id="test", confidence=0.5
            )
            context = ContextResult(confidence=0.5)
            self.engine.update_state(selection, context, f"input {i}")

        # Get limited history
        history = self.engine.get_activation_history(limit=5)

        self.assertEqual(len(history), 5)
        # Should get most recent activations
        self.assertEqual(history[-1]["persona"], "persona_14")
        self.assertEqual(history[0]["persona"], "persona_10")

    def test_suggest_persona_switch(self):
        """Test persona switch suggestion"""
        # Set initial state
        self.engine.update_state(self.test_selection, self.test_context)

        # Create context suggesting different template
        new_context = ContextResult(
            domain="product_engineering",
            confidence=0.8,
            suggested_template="product_engineering_director",
        )

        suggestion = self.engine.suggest_persona_switch(new_context)

        self.assertEqual(suggestion, "product_engineering_director")

    def test_suggest_persona_switch_no_change(self):
        """Test persona switch suggestion when no change needed"""
        self.engine.update_state(self.test_selection, self.test_context)

        # Context suggesting same template
        same_context = ContextResult(
            domain="mobile_platforms",
            confidence=0.8,
            suggested_template="mobile_director",
        )

        suggestion = self.engine.suggest_persona_switch(same_context)

        self.assertIsNone(suggestion)

    def test_suggest_persona_switch_low_confidence(self):
        """Test persona switch suggestion with low confidence"""
        self.engine.update_state(self.test_selection, self.test_context)

        # Low confidence context
        low_confidence_context = ContextResult(
            domain="product_engineering",
            confidence=0.5,  # Below 0.7 threshold
            suggested_template="product_engineering_director",
        )

        suggestion = self.engine.suggest_persona_switch(low_confidence_context)

        self.assertIsNone(suggestion)  # Should not suggest switch

    def test_reset_session(self):
        """Test session reset functionality"""
        # Set some state
        self.engine.update_state(self.test_selection, self.test_context)

        # Verify state exists
        state_before = self.engine.get_current_state()
        self.assertIsNotNone(state_before["active_persona"])
        self.assertGreater(state_before["total_activations"], 0)

        # Reset session
        self.engine.reset_session()

        # Verify state is cleared
        state_after = self.engine.get_current_state()
        self.assertIsNone(state_after["active_persona"])
        self.assertIsNone(state_after["current_template_id"])
        self.assertEqual(state_after["total_activations"], 0)
        self.assertEqual(state_after["persona_usage_count"], {})

        history = self.engine.get_activation_history()
        self.assertEqual(len(history), 0)

    def test_session_duration_tracking(self):
        """Test session duration tracking"""
        # Let some time pass
        time.sleep(0.1)

        state = self.engine.get_current_state()

        self.assertGreater(state["session_duration_minutes"], 0)
        self.assertLess(state["session_duration_minutes"], 1)  # Should be very small


class TestPersonaActivationIntegration(unittest.TestCase):
    """Integration tests for persona activation components"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_template_discovery = Mock(spec=TemplateDiscoveryEngine)

        # Create test template
        self.test_template = DirectorTemplate(
            template_id="mobile_director",
            domain="mobile_platforms",
            display_name="Mobile Engineering Director",
            description="Test template",
            personas=TemplatePersonaConfig(
                primary=["marcus", "sofia"], contextual=["diego"], fallback=["camille"]
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={"mobile app": 0.9, "ios": 0.95}
            ),
        )

        self.mock_template_discovery.list_templates.return_value = [self.test_template]
        self.mock_template_discovery.get_template.return_value = self.test_template
        self.mock_template_discovery.discover_templates_by_context.return_value = [
            (self.test_template, 0.9)
        ]

        # Create engines
        self.context_engine = ContextAnalysisEngine(self.mock_template_discovery)
        self.persona_engine = PersonaSelectionEngine(self.mock_template_discovery)
        self.state_engine = ConversationStateEngine()

    def test_full_activation_workflow(self):
        """Test complete persona activation workflow"""
        user_input = "Our iOS mobile app performance is really bad"

        # Step 1: Analyze context
        context = self.context_engine.analyze_context(user_input)

        self.assertGreater(context.confidence, 0.6)  # Medium confidence is expected
        self.assertEqual(context.suggested_template, "mobile_director")

        # Step 2: Select persona
        selection = self.persona_engine.select_persona(context)

        # With medium confidence, should select contextual persona
        self.assertEqual(selection.primary, "diego")
        self.assertEqual(selection.template_id, "mobile_director")
        self.assertEqual(selection.selection_method, "automatic_medium_confidence")

        # Step 3: Update state
        self.state_engine.update_state(selection, context, user_input)

        state = self.state_engine.get_current_state()
        self.assertEqual(state["active_persona"], "diego")
        self.assertEqual(state["total_activations"], 1)

        # Step 4: Check history
        history = self.state_engine.get_activation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_input"], user_input)

    def test_persona_switch_workflow(self):
        """Test workflow when persona should switch based on new context"""
        # Initial activation
        mobile_input = "iOS app performance issues"
        context1 = self.context_engine.analyze_context(mobile_input)
        selection1 = self.persona_engine.select_persona(context1)
        self.state_engine.update_state(selection1, context1, mobile_input)

        # New context suggesting different domain
        product_template = DirectorTemplate(
            template_id="product_engineering_director",
            domain="product_engineering",
            display_name="Product Engineering Director",
            description="Product strategy",
            personas=TemplatePersonaConfig(
                primary=["alvaro"], contextual=["rachel"], fallback=["camille"]
            ),
            activation_keywords=TemplateActivationKeywords(
                keywords={"product strategy": 0.95}
            ),
        )

        # Update mock to return product template for product context
        def mock_discover_side_effect(text, threshold):
            if "product strategy" in text.lower():
                return [(product_template, 0.95)]
            return [(self.test_template, 0.9)]

        self.mock_template_discovery.discover_templates_by_context.side_effect = (
            mock_discover_side_effect
        )

        def mock_get_template_side_effect(template_id):
            if template_id == "product_engineering_director":
                return product_template
            return self.test_template

        self.mock_template_discovery.get_template.side_effect = (
            mock_get_template_side_effect
        )

        # Analyze new context
        product_input = (
            "We need to improve our product strategy and user feedback loops"
        )
        context2 = self.context_engine.analyze_context(product_input)

        # Check if switch is suggested
        suggestion = self.state_engine.suggest_persona_switch(context2)
        self.assertEqual(suggestion, "product_engineering_director")

        # Perform switch
        selection2 = self.persona_engine.select_persona(context2)
        self.state_engine.update_state(selection2, context2, product_input)

        # Verify new state
        state = self.state_engine.get_current_state()
        self.assertEqual(state["active_persona"], "alvaro")
        self.assertEqual(state["current_template_id"], "product_engineering_director")
        self.assertEqual(state["total_activations"], 2)

    def test_performance_requirements(self):
        """Test that full workflow meets performance requirements"""
        user_input = "Mobile app development challenges with iOS performance"

        start_time = time.time()

        # Full workflow
        context = self.context_engine.analyze_context(user_input)
        selection = self.persona_engine.select_persona(context)
        self.state_engine.update_state(selection, context, user_input)

        total_time = (time.time() - start_time) * 1000

        # Total should be under 2 seconds (2000ms) as per ADR
        self.assertLess(total_time, 2000)

        # Individual components should meet their targets
        self.assertLess(context.analysis_time_ms, 500)  # Context analysis <500ms
        self.assertLess(selection.selection_time_ms, 300)  # Persona selection <300ms


if __name__ == "__main__":
    unittest.main()
