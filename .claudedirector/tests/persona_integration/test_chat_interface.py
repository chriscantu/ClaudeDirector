"""
Test Chat Interface

Tests for the persona chat interface and P2.1 integration.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from lib.claudedirector.persona_integration.chat_interface import (
    PersonaChatInterface, ChatRequest, ChatResponse, PersonaType
)
from lib.claudedirector.p2_communication.interfaces.report_interface import StakeholderType


class TestPersonaChatInterface(unittest.TestCase):
    """Test persona chat interface functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.interface = PersonaChatInterface()

    def test_chat_request_parsing_executive_summary(self):
        """Test parsing executive summary requests."""
        request = self.interface._parse_chat_request(
            "diego",
            "Can you give me an executive summary?"
        )

        self.assertEqual(request.persona, PersonaType.DIEGO)
        self.assertEqual(request.request_type, "executive_summary")
        self.assertEqual(request.time_period, "current_week")  # default

    def test_chat_request_parsing_alerts(self):
        """Test parsing alert requests."""
        request = self.interface._parse_chat_request(
            "camille",
            "What critical alerts should I know about?"
        )

        self.assertEqual(request.persona, PersonaType.CAMILLE)
        self.assertEqual(request.request_type, "alerts")

    def test_chat_request_parsing_team_health(self):
        """Test parsing team health requests."""
        request = self.interface._parse_chat_request(
            "rachel",
            "How is team health looking this week?"
        )

        self.assertEqual(request.persona, PersonaType.RACHEL)
        self.assertEqual(request.request_type, "team_health")
        self.assertEqual(request.time_period, "current_week")

    def test_chat_request_parsing_time_periods(self):
        """Test time period extraction from requests."""
        # Test daily
        request = self.interface._parse_chat_request(
            "diego", "Give me today's status"
        )
        self.assertEqual(request.time_period, "today")

        # Test monthly
        request = self.interface._parse_chat_request(
            "diego", "Show me this month's summary"
        )
        self.assertEqual(request.time_period, "current_month")

        # Test quarterly
        request = self.interface._parse_chat_request(
            "diego", "What's our quarterly performance?"
        )
        self.assertEqual(request.time_period, "current_quarter")

    def test_persona_stakeholder_mapping(self):
        """Test persona to stakeholder mapping."""
        mappings = [
            (PersonaType.DIEGO, "vp_engineering"),
            (PersonaType.CAMILLE, "ceo"),
            (PersonaType.RACHEL, "product_team"),
            (PersonaType.ALVARO, "ceo"),
            (PersonaType.MARTIN, "vp_engineering")
        ]

        for persona_type, expected_stakeholder in mappings:
            stakeholder = self.interface.persona_stakeholder_map[persona_type]
            # Convert enum to string for comparison
            stakeholder_str = stakeholder.value if hasattr(stakeholder, 'value') else str(stakeholder).split('.')[-1].lower()
            self.assertEqual(stakeholder_str, expected_stakeholder)

    @patch('lib.claudedirector.persona_integration.chat_interface.ExecutiveSummaryGenerator')
    def test_handle_executive_summary_request(self, mock_generator):
        """Test executive summary request handling."""
        # Mock report
        mock_report = Mock()
        mock_report.sections = [
            Mock(title="Executive Summary", content="• Key insight 1\n• Key insight 2"),
            Mock(title="Risks & Opportunities", content="⚠️ Risk 1\n✅ Opportunity 1")
        ]
        mock_report.data_sources = ["jira", "claudedirector"]
        mock_report.confidence_score = 0.95
        mock_report.generated_at = "2025-01-15T10:00:00Z"

        mock_instance = mock_generator.return_value
        mock_instance.generate_report.return_value = mock_report

        # Create request
        request = ChatRequest(
            persona=PersonaType.DIEGO,
            request_type="executive_summary",
            stakeholder_context=StakeholderType.VP_ENGINEERING,
            time_period="current_week",
            additional_context={},
            raw_message="Give me an executive summary"
        )

        # Handle request
        response = self.interface._handle_executive_summary_request(request)

        # Verify response
        self.assertIsInstance(response, ChatResponse)
        self.assertIn("Executive Summary", response.response_text)
        self.assertIn("Key Highlights", response.response_text)
        self.assertEqual(response.confidence_score, 0.95)
        self.assertEqual(response.data_sources, ["jira", "claudedirector"])

    def test_handle_alerts_request_with_no_alerts(self):
        """Test alerts request when no alerts exist."""
        # Mock empty alerts
        with patch.object(self.interface.alert_system, 'get_stakeholder_alerts', return_value=[]):
            request = ChatRequest(
                persona=PersonaType.DIEGO,
                request_type="alerts",
                stakeholder_context=StakeholderType.VP_ENGINEERING,
                time_period="current_week",
                additional_context={},
                raw_message="Any alerts?"
            )

            response = self.interface._handle_alerts_request(request)

            self.assertIn("Good news", response.response_text)
            self.assertEqual(response.confidence_score, 1.0)

    def test_handle_alerts_request_with_critical_alerts(self):
        """Test alerts request with critical alerts."""
        # Mock critical alerts
        mock_alert = Mock()
        mock_alert.title = "Critical Issue"
        mock_alert.message = "System down"
        mock_alert.severity.value = "critical"
        mock_alert.actionable_items = ["Restart service"]

        with patch.object(self.interface.alert_system, 'get_stakeholder_alerts', return_value=[mock_alert]):
            request = ChatRequest(
                persona=PersonaType.DIEGO,
                request_type="alerts",
                stakeholder_context=StakeholderType.VP_ENGINEERING,
                time_period="current_week",
                additional_context={},
                raw_message="Any critical alerts?"
            )

            response = self.interface._handle_alerts_request(request)

            self.assertIn("Alert Summary", response.response_text)
            self.assertIn("Critical Issue", response.response_text)
            self.assertIn("Critical Issues", response.response_text)
            self.assertEqual(response.confidence_score, 0.95)

    def test_handle_team_health_request(self):
        """Test team health request handling."""
        # Mock health data
        mock_data = {
            "team_health": {
                "overall_score": 85,
                "collaboration_score": 80,
                "quality_metrics": 90
            },
            "team_velocity": {
                "current_sprint": 45,
                "trend": "increasing"
            }
        }

        with patch.object(self.interface.data_source, 'get_data', return_value=mock_data):
            request = ChatRequest(
                persona=PersonaType.RACHEL,
                request_type="team_health",
                stakeholder_context=StakeholderType.PRODUCT_TEAM,
                time_period="current_week",
                additional_context={},
                raw_message="How is team health?"
            )

            response = self.interface._handle_team_health_request(request)

            self.assertIn("Team Health", response.response_text)
            self.assertIn("85%", response.response_text)
            self.assertIn("45 points", response.response_text)
            self.assertEqual(response.confidence_score, 0.90)

    def test_handle_general_request(self):
        """Test general request handling."""
        request = ChatRequest(
            persona=PersonaType.MARTIN,
            request_type="general",
            stakeholder_context=StakeholderType.VP_ENGINEERING,
            time_period="current_week",
            additional_context={},
            raw_message="What's going on?"
        )

        response = self.interface._handle_general_request(request)

        self.assertIsInstance(response, ChatResponse)
        self.assertIn("status", response.response_text.lower())
        self.assertEqual(response.confidence_score, 0.80)
        self.assertIn("Ask for a detailed executive summary", response.follow_up_suggestions)

    def test_format_executive_summary_for_conversation_diego(self):
        """Test executive summary formatting for Diego."""
        # Mock report
        mock_report = Mock()
        mock_report.sections = [
            Mock(title="Executive Summary", content="• Platform is healthy\n• Cross-team coordination strong"),
            Mock(title="Risks & Opportunities", content="⚠️ Minor technical debt\n✅ Scaling opportunity")
        ]
        mock_report.confidence_score = 0.90
        mock_report.generated_at = "2025-01-15T14:30:00Z"

        result = self.interface._format_executive_summary_for_conversation(
            mock_report, PersonaType.DIEGO
        )

        self.assertIn("Engineering Leadership Perspective", result)
        self.assertIn("Platform is healthy", result)
        self.assertIn("Cross-team coordination", result)
        self.assertIn("90%", result)  # Confidence
        self.assertIn("2025-01-15", result)  # Date

    def test_format_alerts_for_conversation_no_alerts(self):
        """Test alert formatting when no alerts exist."""
        result = self.interface._format_alerts_for_conversation([], PersonaType.DIEGO)

        self.assertIn("Good news", result)
        self.assertIn("No critical alerts", result)

    def test_format_alerts_for_conversation_with_alerts(self):
        """Test alert formatting with various alert types."""
        # Mock alerts
        critical_alert = Mock()
        critical_alert.title = "System Down"
        critical_alert.message = "Database offline"
        critical_alert.severity.value = "critical"
        critical_alert.actionable_items = ["Check database connection"]

        high_alert = Mock()
        high_alert.title = "Performance Issue"
        high_alert.message = "Response times elevated"
        high_alert.severity.value = "high"
        high_alert.actionable_items = []

        medium_alert = Mock()
        medium_alert.title = "Minor Issue"
        medium_alert.message = "Log rotation needed"
        medium_alert.severity.value = "medium"
        medium_alert.actionable_items = []

        alerts = [critical_alert, high_alert, medium_alert]

        result = self.interface._format_alerts_for_conversation(alerts, PersonaType.DIEGO)

        self.assertIn("3 items require attention", result)
        self.assertIn("Critical Issues", result)
        self.assertIn("System Down", result)
        self.assertIn("High Priority", result)
        self.assertIn("Performance Issue", result)
        self.assertIn("Medium Priority", result)

    def test_persona_specific_insights(self):
        """Test persona-specific insight generation."""
        mock_report = Mock()

        # Test different personas
        personas_and_keywords = [
            (PersonaType.DIEGO, "Platform Engineering"),
            (PersonaType.RACHEL, "UX Impact"),
            (PersonaType.ALVARO, "Business Impact"),
            (PersonaType.CAMILLE, "Strategic Technology"),
            (PersonaType.MARTIN, "Architecture Health")
        ]

        for persona, expected_keyword in personas_and_keywords:
            insight = self.interface._add_persona_specific_insights(persona, mock_report)
            self.assertIn(expected_keyword, insight)

    def test_follow_up_suggestions_generation(self):
        """Test follow-up suggestion generation."""
        suggestions = self.interface._generate_follow_up_suggestions(
            PersonaType.DIEGO, "executive_summary"
        )

        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)

        # Should be relevant to executive summary
        suggestion_text = " ".join(suggestions).lower()
        self.assertTrue(
            any(keyword in suggestion_text for keyword in ["team", "risk", "performance", "metric"])
        )

    def test_unknown_persona_fallback(self):
        """Test handling of unknown persona types."""
        request = self.interface._parse_chat_request(
            "unknown_persona",
            "Give me a status update"
        )

        # Should fallback to DIEGO
        self.assertEqual(request.persona, PersonaType.DIEGO)

    def test_handle_chat_request_error_handling(self):
        """Test error handling in main chat request handler."""
        # Mock an exception in request parsing
        with patch.object(self.interface, '_parse_chat_request', side_effect=Exception("Test error")):
            response = self.interface.handle_chat_request("diego", "test message")

            self.assertIsInstance(response, ChatResponse)
            self.assertIn("encountered an issue", response.response_text)
            self.assertEqual(response.confidence_score, 0.5)
            self.assertEqual(response.data_sources, ["error_handling"])
            self.assertIn("error", response.technical_details)


if __name__ == "__main__":
    unittest.main()
