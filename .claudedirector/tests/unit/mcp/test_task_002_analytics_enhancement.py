#!/usr/bin/env python3
"""
Test Suite for Task 002: Context Engineering Analytics Enhancement
Tests MCP session pattern analysis functionality
"""

import unittest
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from context_engineering.analytics_engine import AnalyticsEngine, SessionInsights


class TestMCPAnalyticsEnhancement(unittest.TestCase):
    """Test suite for MCP analytics enhancement functionality - Task 002"""

    def setUp(self):
        """Set up test fixtures"""
        self.analytics_engine = AnalyticsEngine()

    def test_mcp_session_pattern_analysis(self):
        """Test MCP session pattern analysis functionality"""

        # Test session data with various query types
        session_data = [
            {"query": "What is our strategic roadmap for next quarter?"},
            {"query": "Analyze team performance and ROI"},
            {"query": "Show me the documentation for this API"},
            {"query": "Create a button component with modern design"},
            {"query": "Set up browser automation testing"},
        ]

        # Analyze session patterns
        insights = self.analytics_engine.analyze_mcp_session_patterns(session_data)

        # Verify SessionInsights structure
        self.assertIsInstance(insights, SessionInsights)
        self.assertIsInstance(insights.patterns, dict)
        self.assertIsInstance(insights.trends, dict)
        self.assertIsInstance(insights.recommendations, list)
        self.assertIsInstance(insights.confidence, float)

        # Verify pattern detection
        self.assertIn("strategic_analysis", insights.patterns)
        self.assertIn("technical_documentation", insights.patterns)
        self.assertIn("ui_design", insights.patterns)
        self.assertIn("testing_automation", insights.patterns)

        # Verify confidence is reasonable
        self.assertGreater(insights.confidence, 0.0)
        self.assertLessEqual(insights.confidence, 1.0)

    def test_empty_session_data_handling(self):
        """Test handling of empty session data"""

        insights = self.analytics_engine.analyze_mcp_session_patterns([])

        # Should handle gracefully
        self.assertIsInstance(insights, SessionInsights)
        self.assertGreater(len(insights.patterns), 0)  # Should have fallback patterns
        self.assertGreater(
            len(insights.recommendations), 0
        )  # Should have default recommendations

    def test_strategic_query_classification(self):
        """Test strategic query classification accuracy"""

        session_data = [
            {"query": "strategic planning for business growth"},
            {"query": "roadmap development for platform strategy"},
            {"query": "ROI analysis for investment decisions"},
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(session_data)

        # Should detect high strategic analysis pattern
        self.assertGreater(insights.patterns.get("strategic_analysis", 0), 0.8)

    def test_ui_design_query_classification(self):
        """Test UI design query classification"""

        session_data = [
            {"query": "create a form component with validation"},
            {"query": "design a responsive layout interface"},
            {"query": "build button components for the UI"},
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(session_data)

        # Should detect high UI design pattern
        self.assertGreater(insights.patterns.get("ui_design", 0), 0.8)

    def test_recommendation_generation(self):
        """Test recommendation generation for different patterns"""

        # Strategic analysis heavy session
        strategic_session = [
            {"query": "strategic planning initiative"},
            {"query": "business strategy analysis"},
            {"query": "strategic roadmap development"},
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(strategic_session)

        # Should recommend Sequential MCP server for strategic analysis
        recommendations_text = " ".join(insights.recommendations)
        self.assertIn("Sequential", recommendations_text)

    def test_session_flow_coherence(self):
        """Test session flow coherence detection"""

        # Coherent session (all strategic)
        coherent_session = [
            {"query": "strategic analysis needed"},
            {"query": "strategic planning approach"},
            {"query": "strategic implementation roadmap"},
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(coherent_session)

        # Should detect high flow coherence
        self.assertIn("flow_coherence", insights.patterns)
        self.assertGreater(insights.patterns["flow_coherence"], 0.8)

    def test_complexity_trend_analysis(self):
        """Test complexity trend analysis within session"""

        # Session with increasing complexity
        increasing_complexity_session = [
            {"query": "help"},
            {"query": "analyze team performance"},
            {
                "query": "comprehensive strategic analysis with stakeholder alignment and implementation roadmap"
            },
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(
            increasing_complexity_session
        )

        # Should detect increasing complexity trend
        self.assertEqual(insights.trends.get("complexity_trend"), "increasing")

    def test_mixed_focus_session(self):
        """Test mixed focus session detection"""

        mixed_session = [
            {"query": "strategic planning"},
            {"query": "create UI component"},
            {"query": "API documentation"},
            {"query": "test automation setup"},
        ]

        insights = self.analytics_engine.analyze_mcp_session_patterns(mixed_session)

        # Should detect mixed focus
        self.assertEqual(insights.trends.get("session_focus"), "mixed_focus")

    def test_enhancement_backward_compatibility(self):
        """Test that enhancement doesn't break existing functionality"""

        # Test existing methods still work
        context = "strategic planning for team organization"
        recommendations = self.analytics_engine.get_strategic_recommendations(context)

        # Should return valid recommendations
        self.assertIsInstance(recommendations, dict)
        self.assertIn("framework_recommendation", recommendations)

        # Performance summary should work
        performance = self.analytics_engine.get_performance_summary()
        self.assertIsInstance(performance, dict)

    def test_integration_with_existing_ml_patterns(self):
        """Test integration with existing ML pattern infrastructure"""

        session_data = [
            {"query": "team collaboration analysis"},
            {"query": "stakeholder engagement assessment"},
        ]

        # Should not error when trying to use ML pattern engine
        insights = self.analytics_engine.analyze_mcp_session_patterns(session_data)

        # Should return valid insights even if ML components not fully available
        self.assertIsInstance(insights, SessionInsights)
        self.assertGreater(insights.confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
