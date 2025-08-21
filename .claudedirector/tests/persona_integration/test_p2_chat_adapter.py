"""
Test P2 Chat Adapter

Tests for the convenience adapter functions for P2.1 integration.
"""

import unittest
from unittest.mock import Mock, patch
from lib.claudedirector.persona_integration.p2_chat_adapter import (
    P2ChatAdapter,
    executive_summary,
    current_alerts,
    team_health,
    risk_analysis,
    initiative_status,
    ask_persona,
    get_capabilities,
    list_personas,
)


class TestP2ChatAdapter(unittest.TestCase):
    """Test P2 chat adapter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.adapter = P2ChatAdapter()

    def test_get_executive_summary_auto_stakeholder(self):
        """Test executive summary with auto stakeholder detection."""
        mock_response = Mock()
        mock_response.response_text = "Executive summary for Diego"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_executive_summary("diego")

            # Should auto-detect stakeholder for Diego as vp_engineering
            mock_handler.assert_called_once()
            call_args = mock_handler.call_args
            self.assertEqual(call_args[0][0], "diego")
            self.assertIn("vp_engineering", call_args[0][1])

            self.assertEqual(result, "Executive summary for Diego")

    def test_get_executive_summary_specific_stakeholder(self):
        """Test executive summary with specific stakeholder."""
        mock_response = Mock()
        mock_response.response_text = "CEO-focused summary"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_executive_summary(
                "camille", stakeholder="ceo", period="current_month"
            )

            # Should use specified stakeholder
            call_args = mock_handler.call_args
            self.assertIn("ceo", call_args[0][1])
            self.assertIn("current_month", call_args[0][1])

            self.assertEqual(result, "CEO-focused summary")

    def test_get_current_alerts(self):
        """Test current alerts retrieval."""
        mock_response = Mock()
        mock_response.response_text = "Current critical alerts"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_current_alerts("rachel", severity="critical")

            call_args = mock_handler.call_args
            self.assertEqual(call_args[0][0], "rachel")
            self.assertIn("critical", call_args[0][1])

            self.assertEqual(result, "Current critical alerts")

    def test_get_team_health(self):
        """Test team health retrieval."""
        mock_response = Mock()
        mock_response.response_text = "Team health status"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_team_health("martin")

            call_args = mock_handler.call_args
            self.assertEqual(call_args[0][0], "martin")
            self.assertIn("team health", call_args[0][1].lower())

            self.assertEqual(result, "Team health status")

    def test_get_risk_analysis(self):
        """Test risk analysis retrieval."""
        mock_response = Mock()
        mock_response.response_text = "Risk analysis report"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_risk_analysis("alvaro")

            call_args = mock_handler.call_args
            self.assertEqual(call_args[0][0], "alvaro")
            self.assertIn("risk", call_args[0][1].lower())

            self.assertEqual(result, "Risk analysis report")

    def test_get_initiative_status(self):
        """Test initiative status retrieval."""
        mock_response = Mock()
        mock_response.response_text = "Initiative status report"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            result = self.adapter.get_initiative_status("diego")

            call_args = mock_handler.call_args
            self.assertEqual(call_args[0][0], "diego")
            self.assertIn("initiative", call_args[0][1].lower())

            self.assertEqual(result, "Initiative status report")

    def test_handle_natural_request(self):
        """Test natural language request handling."""
        mock_response = Mock()
        mock_response.response_text = "Natural response"
        mock_response.confidence_score = 0.85
        mock_response.data_sources = ["jira", "test"]
        mock_response.follow_up_suggestions = ["Follow up 1", "Follow up 2"]
        mock_response.metadata = {"test": "data"}

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ):
            result = self.adapter.handle_natural_request(
                "sofia", "How are things going?"
            )

            # Should return complete response dictionary
            self.assertIsInstance(result, dict)
            self.assertEqual(result["response"], "Natural response")
            self.assertEqual(result["confidence"], 0.85)
            self.assertEqual(result["data_sources"], ["jira", "test"])
            self.assertEqual(result["suggestions"], ["Follow up 1", "Follow up 2"])
            self.assertEqual(result["metadata"], {"test": "data"})
            self.assertIn("timestamp", result)

    def test_stakeholder_auto_detection_mapping(self):
        """Test stakeholder auto-detection for all personas."""
        test_cases = [
            ("diego", "vp_engineering"),
            ("camille", "ceo"),
            ("rachel", "product_team"),
            ("alvaro", "ceo"),
            ("martin", "vp_engineering"),
            ("unknown", "vp_engineering"),  # Default fallback
        ]

        mock_response = Mock()
        mock_response.response_text = "Test response"

        with patch.object(
            self.adapter.bridge, "handle_persona_request", return_value=mock_response
        ) as mock_handler:
            for persona, expected_stakeholder in test_cases:
                mock_handler.reset_mock()  # Reset for each test
                self.adapter.get_executive_summary(persona)

                call_args = mock_handler.call_args
                self.assertIn(expected_stakeholder, call_args[0][1])

    def test_get_persona_capabilities(self):
        """Test persona capabilities retrieval."""
        mock_caps = {"primary_focus": "test focus", "data_sources": ["test"]}

        with patch.object(
            self.adapter.bridge, "get_persona_capabilities", return_value=mock_caps
        ) as mock_handler:
            result = self.adapter.get_persona_capabilities("elena")

            mock_handler.assert_called_once_with("elena")
            self.assertEqual(result, mock_caps)

    def test_list_available_personas(self):
        """Test listing available personas."""
        mock_personas = [
            {"name": "diego", "title": "Test Title"},
            {"name": "camille", "title": "Test Title 2"},
        ]

        with patch.object(
            self.adapter.bridge, "get_available_personas", return_value=mock_personas
        ) as mock_handler:
            result = self.adapter.list_available_personas()

            mock_handler.assert_called_once()
            self.assertEqual(result, mock_personas)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for direct use."""

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_executive_summary_function(self, mock_adapter):
        """Test executive_summary convenience function."""
        mock_adapter.get_executive_summary.return_value = "Test summary"

        result = executive_summary("diego", stakeholder="ceo")

        mock_adapter.get_executive_summary.assert_called_once_with(
            "diego", stakeholder="ceo"
        )
        self.assertEqual(result, "Test summary")

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_current_alerts_function(self, mock_adapter):
        """Test current_alerts convenience function."""
        mock_adapter.get_current_alerts.return_value = "Test alerts"

        result = current_alerts("rachel", severity="high")

        mock_adapter.get_current_alerts.assert_called_once_with(
            "rachel", severity="high"
        )
        self.assertEqual(result, "Test alerts")

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_team_health_function(self, mock_adapter):
        """Test team_health convenience function."""
        mock_adapter.get_team_health.return_value = "Test health"

        result = team_health("martin")

        mock_adapter.get_team_health.assert_called_once_with("martin")
        self.assertEqual(result, "Test health")

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_risk_analysis_function(self, mock_adapter):
        """Test risk_analysis convenience function."""
        mock_adapter.get_risk_analysis.return_value = "Test risks"

        result = risk_analysis("alvaro")

        mock_adapter.get_risk_analysis.assert_called_once_with("alvaro")
        self.assertEqual(result, "Test risks")

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_initiative_status_function(self, mock_adapter):
        """Test initiative_status convenience function."""
        mock_adapter.get_initiative_status.return_value = "Test initiatives"

        result = initiative_status("diego")

        mock_adapter.get_initiative_status.assert_called_once_with("diego")
        self.assertEqual(result, "Test initiatives")

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_ask_persona_function(self, mock_adapter):
        """Test ask_persona convenience function."""
        mock_adapter.handle_natural_request.return_value = {"response": "Test response"}

        result = ask_persona("sofia", "How are things?")

        mock_adapter.handle_natural_request.assert_called_once_with(
            "sofia", "How are things?"
        )
        self.assertEqual(result, {"response": "Test response"})

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_get_capabilities_function(self, mock_adapter):
        """Test get_capabilities convenience function."""
        mock_adapter.get_persona_capabilities.return_value = {"test": "caps"}

        result = get_capabilities("elena")

        mock_adapter.get_persona_capabilities.assert_called_once_with("elena")
        self.assertEqual(result, {"test": "caps"})

    @patch("lib.claudedirector.persona_integration.p2_chat_adapter.p2_chat")
    def test_list_personas_function(self, mock_adapter):
        """Test list_personas convenience function."""
        mock_adapter.list_available_personas.return_value = [{"name": "test"}]

        result = list_personas()

        mock_adapter.list_available_personas.assert_called_once()
        self.assertEqual(result, [{"name": "test"}])


if __name__ == "__main__":
    unittest.main()
