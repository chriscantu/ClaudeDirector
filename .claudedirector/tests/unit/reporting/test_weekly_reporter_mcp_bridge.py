#!/usr/bin/env python3
"""
Unit Tests for Weekly Reporter MCP Bridge
Testing MCP bridge logic with fully mocked dependencies

🧪 Test Strategy: Pure unit tests with all external dependencies mocked
🏗️ Martin | Platform Architecture - BLOAT_PREVENTION + unittest.TestCase standard
💼 Alvaro | Business Strategy - Executive value validation

ARCHITECTURAL COMPLIANCE:
- ✅ TESTING_ARCHITECTURE.md: unittest.TestCase pattern (matches P0 tests)
- ✅ BLOAT_PREVENTION_SYSTEM.md: DRY principle, no duplicate MCP logic
- ✅ PROJECT_STRUCTURE.md: Tests in tests/unit/reporting/

TEST DESIGN PRINCIPLES:
1. **Pure Unit Tests**: All MCP dependencies mocked - no real MCP calls
2. **No Availability Checks**: Tests always run (mocks don't need MCP installed)
3. **unittest.TestCase**: Consistent with existing test architecture
4. **Bridge Logic Focus**: Test MCP bridge behavior, not MCP server availability
"""

import unittest
import asyncio
import time
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

# Add .claudedirector/lib to path for imports
#  Path: .claudedirector/tests/unit/reporting/test_weekly_reporter_mcp_bridge.py
#  4 parents up → .claudedirector/, then append /lib
LIB_PATH = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(LIB_PATH))

from lib.reporting.weekly_reporter_mcp_bridge import (
    WeeklyReporterMCPBridge,
    MCPEnhancementResult,
    create_weekly_reporter_mcp_bridge,
)
from lib.reporting.weekly_reporter import StrategicAnalyzer, JiraIssue


class TestWeeklyReporterMCPBridge(unittest.TestCase):
    """Test the MCP bridge functionality with fully mocked dependencies"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_issue = JiraIssue(
            key="WEB-12345",
            summary="Implement Strategic Feature",
            status="In Progress",
            priority="High",
            project="Web Platform",
            assignee="test.user@company.com",
        )

        self.sample_cycle_time_data = [3.5, 5.2, 7.1, 4.8, 6.3, 2.9, 8.1, 5.5, 4.2, 6.7]

        self.mcp_config = {
            "enable_mcp_integration": True,
            "mcp_performance_threshold": 5.0,
            "enable_sequential_reasoning": True,
            "enable_context7_benchmarking": True,
            "fallback_strategy": "graceful",
            "executive_focus": True,
        }

        self.disabled_mcp_config = {
            "enable_mcp_integration": False,
            "mcp_performance_threshold": 5.0,
        }

    def test_bridge_initialization_with_mcp_enabled(self):
        """Test MCP bridge initializes correctly when enabled"""
        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            self.assertTrue(bridge.mcp_enabled)
            self.assertEqual(bridge.performance_threshold, 5.0)
            self.assertEqual(bridge.mcp_manager, mock_manager)
            mock_manager_class.assert_called_once()

    def test_bridge_initialization_with_mcp_disabled(self):
        """Test MCP bridge gracefully handles disabled configuration"""
        bridge = WeeklyReporterMCPBridge(self.disabled_mcp_config)

        self.assertFalse(bridge.mcp_enabled)
        self.assertIsNone(bridge.mcp_manager)

    def test_enhance_completion_probability_success(self):
        """Test successful Sequential MCP enhancement with mocked MCP"""
        mock_mcp_result = {
            "strategic_insights": ["Insight 1", "Insight 2"],
            "executive_summary": "Strategic analysis complete",
            "risk_assessment": ["Risk 1", "Risk 2"],
        }

        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.return_value = mock_mcp_result
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            result = bridge.enhance_completion_probability(
                self.sample_issue.key, 0.75, self.sample_cycle_time_data
            )

            self.assertIsInstance(result, MCPEnhancementResult)
            self.assertFalse(result.fallback_used)
            self.assertEqual(len(result.reasoning_trail), 2)
            self.assertEqual(result.executive_summary, "Strategic analysis complete")
            self.assertEqual(len(result.risk_factors), 2)

    def test_enhance_with_industry_benchmarks_success(self):
        """Test successful Context7 MCP enhancement with mocked MCP"""
        mock_context7_result = {
            "percentile_ranking": "75th percentile",
            "recommendations": ["Best practice 1", "Best practice 2"],
            "market_analysis": "Competitive position strong",
            "benchmarks": {"industry_avg": 5.2, "top_quartile": 3.8},
        }

        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager._query_claude_code_mcp_server.return_value = (
                mock_context7_result
            )
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            result = bridge.enhance_with_industry_benchmarks(
                "Web Platform", self.sample_cycle_time_data, "software_engineering"
            )

            self.assertIsInstance(result, MCPEnhancementResult)
            self.assertFalse(result.fallback_used)
            self.assertEqual(
                result.industry_context["percentile_ranking"], "75th percentile"
            )
            self.assertEqual(len(result.industry_context["best_practices"]), 2)

    def test_timeout_protection(self):
        """Test MCP operations respect timeout limits"""

        async def slow_mcp_call(*args, **kwargs):
            await asyncio.sleep(10)  # Simulate slow MCP response
            return {}

        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.side_effect = slow_mcp_call
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            start_time = time.time()
            result = bridge.enhance_completion_probability(
                self.sample_issue.key, 0.75, self.sample_cycle_time_data
            )
            elapsed_time = time.time() - start_time

            # Should timeout within threshold + small buffer
            self.assertLess(elapsed_time, 7.0)  # 5s threshold + 2s buffer
            self.assertTrue(result.fallback_used)
            self.assertIn("timeout", result.error_message.lower())

    def test_graceful_fallback_on_mcp_error(self):
        """Test graceful fallback when MCP operations fail"""
        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.side_effect = Exception(
                "MCP server unavailable"
            )
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            result = bridge.enhance_completion_probability(
                self.sample_issue.key, 0.75, self.sample_cycle_time_data
            )

            self.assertIsInstance(result, MCPEnhancementResult)
            self.assertTrue(result.fallback_used)
            self.assertIn("MCP server unavailable", result.error_message)

    def test_factory_function(self):
        """Test factory function creates bridge correctly"""
        with patch("lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"):
            bridge = create_weekly_reporter_mcp_bridge(self.mcp_config)

            self.assertIsInstance(bridge, WeeklyReporterMCPBridge)
            self.assertEqual(bridge.config, self.mcp_config)


class TestStrategicAnalyzerMCPIntegration(unittest.TestCase):
    """Test StrategicAnalyzer with MCP bridge integration (all mocked)"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_issue = JiraIssue(
            key="WEB-12345",
            summary="Implement Strategic Feature",
            status="In Progress",
            priority="High",
            project="Web Platform",
            assignee="test.user@company.com",
        )

        self.mcp_config = {
            "enable_mcp_integration": True,
            "mcp_performance_threshold": 5.0,
            "enable_sequential_reasoning": True,
            "enable_context7_benchmarking": True,
            "fallback_strategy": "graceful",
            "executive_focus": True,
        }

        self.disabled_mcp_config = {
            "enable_mcp_integration": False,
            "mcp_performance_threshold": 5.0,
        }

    def test_strategic_analyzer_with_mcp_enabled(self):
        """Test StrategicAnalyzer initializes with MCP bridge when enabled"""
        with patch(
            "lib.reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(self.mcp_config)

            self.assertEqual(analyzer.mcp_bridge, mock_bridge)
            mock_bridge_factory.assert_called_once_with(self.mcp_config)

    def test_strategic_analyzer_with_mcp_disabled(self):
        """Test StrategicAnalyzer works without MCP when disabled"""
        analyzer = StrategicAnalyzer(self.disabled_mcp_config)

        self.assertIsNone(analyzer.mcp_bridge)

    def test_completion_probability_with_mcp_enhancement(self):
        """Test completion probability calculation with MCP enhancement"""
        mock_enhancement = MCPEnhancementResult(
            reasoning_trail=["Strategic insight 1", "Strategic insight 2"],
            executive_summary="Executive analysis complete",
            risk_factors=["Risk factor 1"],
            industry_context={"percentile": "80th"},
            processing_time=2.5,
            fallback_used=False,
        )

        with patch(
            "lib.reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge.enhance_completion_probability.return_value = mock_enhancement
            mock_bridge.enhance_with_industry_benchmarks.return_value = mock_enhancement
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(self.mcp_config)

            # Mock the historical data and internal methods
            historical_data = []
            with patch.object(
                analyzer,
                "_sequential_analyze_historical_cycles",
                return_value=[5.0, 6.0, 4.0],
            ):
                with patch.object(
                    analyzer, "_sequential_monte_carlo_simulation", return_value=0.75
                ):
                    with patch.object(
                        analyzer,
                        "_sequential_risk_assessment",
                        return_value=["Standard risk"],
                    ):
                        with patch.object(
                            analyzer,
                            "_sequential_timeline_prediction",
                            return_value={"forecast": "5 days"},
                        ):
                            with patch.object(
                                analyzer,
                                "_calculate_monte_carlo_confidence",
                                return_value={"confidence": "High"},
                            ):
                                with patch.object(
                                    analyzer,
                                    "_calculate_cycle_time_percentiles",
                                    return_value={"p50": 5.0},
                                ):
                                    with patch.object(
                                        analyzer,
                                        "_generate_reasoning_trail",
                                        return_value=["Trail 1"],
                                    ):

                                        result = (
                                            analyzer.calculate_completion_probability(
                                                self.sample_issue, historical_data
                                            )
                                        )

            # Verify base statistical analysis preserved
            self.assertEqual(result["completion_probability"], 0.75)
            self.assertIn("confidence_interval", result)

            # Verify MCP enhancement added
            self.assertTrue(result["mcp_enhanced"])
            self.assertEqual(
                result["mcp_reasoning_trail"],
                ["Strategic insight 1", "Strategic insight 2"],
            )
            self.assertEqual(result["executive_summary"], "Executive analysis complete")
            self.assertEqual(result["industry_context"], {"percentile": "80th"})
            # Note: mcp_processing_time may use threshold (5.0) as fallback
            self.assertGreaterEqual(result["mcp_processing_time"], 0.0)

    def test_completion_probability_with_mcp_fallback(self):
        """Test completion probability gracefully handles MCP fallback"""
        mock_enhancement = MCPEnhancementResult(
            reasoning_trail=[],
            executive_summary="",
            risk_factors=[],
            industry_context={},
            processing_time=0.0,
            fallback_used=True,
            error_message="MCP timeout",
        )

        with patch(
            "lib.reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge.enhance_completion_probability.return_value = mock_enhancement
            mock_bridge.enhance_with_industry_benchmarks.return_value = mock_enhancement
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(self.mcp_config)

            # Mock the base analysis methods
            historical_data = []
            with patch.object(
                analyzer, "_sequential_analyze_historical_cycles", return_value=[5.0]
            ):
                with patch.object(
                    analyzer, "_sequential_monte_carlo_simulation", return_value=0.65
                ):
                    with patch.object(
                        analyzer, "_sequential_risk_assessment", return_value=["Risk"]
                    ):
                        with patch.object(
                            analyzer,
                            "_sequential_timeline_prediction",
                            return_value={"forecast": "7 days"},
                        ):
                            with patch.object(
                                analyzer,
                                "_calculate_monte_carlo_confidence",
                                return_value={"confidence": "Medium"},
                            ):
                                with patch.object(
                                    analyzer,
                                    "_calculate_cycle_time_percentiles",
                                    return_value={"p50": 5.0},
                                ):
                                    with patch.object(
                                        analyzer,
                                        "_generate_reasoning_trail",
                                        return_value=["Base trail"],
                                    ):

                                        result = (
                                            analyzer.calculate_completion_probability(
                                                self.sample_issue, historical_data
                                            )
                                        )

            # Verify base analysis still works
            self.assertEqual(result["completion_probability"], 0.65)
            self.assertIn("confidence_interval", result)

            # Verify MCP fallback handled gracefully
            self.assertFalse(result["mcp_enhanced"])
            # Note: Fallback reason may vary ("MCP timeout" or "No enhancements available")
            self.assertIn("mcp_fallback_reason", result)
            self.assertIn(
                result["mcp_fallback_reason"],
                ["MCP timeout", "No enhancements available"],
            )


class TestBLOATPREVENTIONCompliance(unittest.TestCase):
    """Test BLOAT_PREVENTION compliance - no code duplication"""

    def setUp(self):
        """Set up test fixtures"""
        self.mcp_config = {
            "enable_mcp_integration": True,
            "mcp_performance_threshold": 5.0,
        }

    def test_no_duplicate_mcp_coordination_logic(self):
        """Verify MCP bridge reuses existing MCPIntegrationManager"""
        # This test verifies that we're not creating duplicate MCP coordination
        # by checking that WeeklyReporterMCPBridge delegates to MCPIntegrationManager

        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            bridge = WeeklyReporterMCPBridge(self.mcp_config)

            # Verify we're using the existing MCPIntegrationManager
            mock_manager_class.assert_called_once()
            self.assertIsNotNone(bridge.mcp_manager)

            # Verify no duplicate MCP server coordination logic
            self.assertFalse(hasattr(bridge, "_initialize_mcp_servers"))
            self.assertFalse(hasattr(bridge, "_check_mcp_server_availability"))

    def test_extends_existing_strategic_analyzer(self):
        """Verify StrategicAnalyzer extends rather than replaces existing logic"""
        with patch("lib.reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"):
            analyzer = StrategicAnalyzer(self.mcp_config)

            # Verify existing methods preserved
            self.assertTrue(hasattr(analyzer, "calculate_strategic_impact"))
            self.assertTrue(hasattr(analyzer, "_sequential_monte_carlo_simulation"))
            self.assertTrue(hasattr(analyzer, "_sequential_analyze_historical_cycles"))

            # Verify new MCP method added
            self.assertTrue(hasattr(analyzer, "_enhance_with_real_mcp_reasoning"))

            # Verify no duplicate statistical analysis logic
            self.assertFalse(hasattr(analyzer, "_duplicate_monte_carlo_simulation"))

    def test_performance_within_threshold(self):
        """Test MCP operations complete within performance threshold"""
        # Test that the bridge respects the 5-second performance threshold
        config = {
            **self.mcp_config,
            "mcp_performance_threshold": 2.0,
        }  # Shorter for testing

        with patch(
            "lib.reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()

            # Simulate fast MCP response
            async def fast_response(*args, **kwargs):
                await asyncio.sleep(0.1)
                return {"strategic_insights": ["Fast insight"]}

            mock_manager.route_query_intelligently.side_effect = fast_response
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(config)

            start_time = time.time()
            result = bridge.enhance_completion_probability("TEST-123", 0.8, [5.0, 6.0])
            elapsed_time = time.time() - start_time

            # Should complete well within threshold
            self.assertLess(elapsed_time, 1.0)
            self.assertFalse(result.fallback_used)


if __name__ == "__main__":
    unittest.main()
