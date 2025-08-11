"""
Test Persona Bridge

Comprehensive tests for persona framework integration with P2.1 system.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from lib.claudedirector.persona_integration.persona_bridge import PersonaP2Bridge, PersonaRequest, PersonaResponse


class TestPersonaP2Bridge(unittest.TestCase):
    """Test persona bridge functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.bridge = PersonaP2Bridge()

    def test_should_route_to_p2_with_executive_summary_request(self):
        """Test routing decision for executive summary requests."""
        # Should route to P2.1
        should_route = self.bridge._should_route_to_p2(
            "Give me an executive summary",
            "diego"
        )
        self.assertTrue(should_route)

    def test_should_route_to_p2_with_alerts_request(self):
        """Test routing decision for alerts requests."""
        should_route = self.bridge._should_route_to_p2(
            "What critical alerts should I know about?",
            "camille"
        )
        self.assertTrue(should_route)

    def test_should_route_to_p2_with_team_health_request(self):
        """Test routing decision for team health requests."""
        should_route = self.bridge._should_route_to_p2(
            "How is team health looking?",
            "rachel"
        )
        self.assertTrue(should_route)

    def test_should_not_route_general_questions(self):
        """Test that general questions don't route to P2.1."""
        should_route = self.bridge._should_route_to_p2(
            "What is your opinion on microservices?",
            "martin"
        )
        self.assertFalse(should_route)

    def test_persona_specific_keyword_routing(self):
        """Test routing based on persona-specific keywords."""
        # Diego + platform keywords + status request
        should_route = self.bridge._should_route_to_p2(
            "What's the status of platform engineering coordination?",
            "diego"
        )
        self.assertTrue(should_route)

        # Rachel + design keywords + overview request
        should_route = self.bridge._should_route_to_p2(
            "Give me an overview of design system accessibility",
            "rachel"
        )
        self.assertTrue(should_route)

    def test_handle_p2_request_success(self):
        """Test successful P2.1 request handling."""
        # Mock chat interface response
        mock_response = Mock()
        mock_response.response_text = "Test executive summary"
        mock_response.confidence_score = 0.95
        mock_response.data_sources = ["jira", "claudedirector"]
        mock_response.follow_up_suggestions = ["Check alerts"]
        mock_response.technical_details = {"sections": 3}

        # Mock the chat interface directly
        with patch.object(self.bridge.chat_interface, 'handle_chat_request', return_value=mock_response):
            # Test the request
            response = self.bridge._handle_p2_request(
                "diego",
                "Give me an executive summary",
                {}
            )

            # Verify response structure
            self.assertIsInstance(response, PersonaResponse)
            self.assertEqual(response.response_text, "Test executive summary")
            self.assertEqual(response.confidence_score, 0.95)
            self.assertEqual(response.data_sources, ["jira", "claudedirector"])
            self.assertTrue(response.metadata["used_p2_system"])
            self.assertEqual(response.metadata["persona"], "diego")

    def test_handle_general_persona_request(self):
        """Test general persona request handling."""
        response = self.bridge._handle_general_persona_request(
            "diego",
            "What do you think about microservices?",
            {}
        )

        # Verify response structure
        self.assertIsInstance(response, PersonaResponse)
        self.assertIn("platform engineering", response.response_text.lower())
        self.assertEqual(response.confidence_score, 0.7)
        self.assertEqual(response.data_sources, ["persona_knowledge"])
        self.assertFalse(response.metadata["used_p2_system"])

    def test_get_available_personas(self):
        """Test getting available personas list."""
        personas = self.bridge.get_available_personas()

        # Should return list of persona dictionaries
        self.assertIsInstance(personas, list)
        self.assertGreater(len(personas), 0)

        # Check structure of first persona
        first_persona = personas[0]
        required_keys = ["name", "title", "focus", "capabilities"]
        for key in required_keys:
            self.assertIn(key, first_persona)

        # Verify expected personas are present
        persona_names = [p["name"] for p in personas]
        expected_personas = ["diego", "camille", "rachel", "alvaro", "martin"]
        for expected in expected_personas:
            self.assertIn(expected, persona_names)

    def test_get_persona_capabilities(self):
        """Test getting specific persona capabilities."""
        # Test known persona
        caps = self.bridge.get_persona_capabilities("diego")

        required_keys = [
            "primary_focus", "data_sources", "report_types",
            "alert_types", "stakeholder_perspective"
        ]
        for key in required_keys:
            self.assertIn(key, caps)

        self.assertIn("platform engineering", caps["primary_focus"].lower())
        self.assertEqual(caps["stakeholder_perspective"], "VP Engineering")

        # Test unknown persona (should return default)
        caps = self.bridge.get_persona_capabilities("unknown")
        self.assertEqual(caps["stakeholder_perspective"], "General")

    def test_format_persona_help(self):
        """Test persona help formatting."""
        help_text = self.bridge.format_persona_help("diego")

        # Should contain key information
        self.assertIn("Diego", help_text)
        self.assertIn("Primary Focus", help_text)
        self.assertIn("Example Requests", help_text)
        self.assertIn("Data Sources", help_text)

        # Should be properly formatted
        self.assertIn("**", help_text)  # Markdown formatting

    def test_quick_status_check(self):
        """Test quick status check functionality."""
        # Mock chat interface response
        mock_response = Mock()
        mock_response.response_text = "Quick status overview"
        mock_response.confidence_score = 0.85
        mock_response.data_sources = ["jira"]

        with patch.object(self.bridge.chat_interface, 'handle_chat_request', return_value=mock_response):
            # Test quick status
            response = self.bridge.quick_status_check("diego")

            # Verify response
            self.assertIsInstance(response, PersonaResponse)
            self.assertIn("Quick Status for Diego", response.response_text)
            self.assertEqual(response.metadata["response_type"], "quick_status")
            self.assertTrue(response.metadata["used_p2_system"])

    def test_handle_persona_request_with_error(self):
        """Test error handling in persona request."""
        # Mock chat interface to raise exception
        with patch.object(self.bridge.chat_interface, 'handle_chat_request', side_effect=Exception("Test error")):
            # Test request with error
            response = self.bridge.handle_persona_request(
                "diego",
                "Give me an executive summary"
            )

            # Should return error response
            self.assertIsInstance(response, PersonaResponse)
            self.assertIn("encountered an issue", response.response_text)
            self.assertEqual(response.confidence_score, 0.5)
            self.assertEqual(response.data_sources, ["error_handling"])
            self.assertIn("error", response.metadata)
            self.assertTrue(response.metadata["fallback"])

    def test_persona_keyword_mapping(self):
        """Test persona keyword mapping completeness."""
        # All personas should have keyword mappings
        expected_personas = ["diego", "camille", "rachel", "alvaro", "martin",
                           "sofia", "elena", "marcus", "david", "security", "data"]

        for persona in expected_personas:
            self.assertIn(persona, self.bridge.persona_keywords)
            keywords = self.bridge.persona_keywords[persona]
            self.assertIsInstance(keywords, list)
            self.assertGreater(len(keywords), 0)

    def test_p2_trigger_patterns(self):
        """Test P2.1 trigger patterns are comprehensive."""
        patterns = self.bridge.p2_trigger_patterns

        # Should include common request types
        expected_patterns = [
            "executive summary", "status update", "alerts", "team health",
            "velocity", "risks", "initiatives"
        ]

        pattern_text = " ".join(patterns)
        for expected in expected_patterns:
            # Check if pattern exists (allowing for regex syntax)
            found = any(expected.replace("?", "") in pattern for pattern in patterns)
            self.assertTrue(found, f"Expected pattern '{expected}' not found")


if __name__ == "__main__":
    unittest.main()
