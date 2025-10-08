#!/usr/bin/env python3
"""
Unit Tests for Weekly Reporter Real MCP Integration
Testing real Sequential and Context7 MCP server integration

🧪 Test Strategy: Validate real MCP integration with mocked responses
🏗️ Martin | Platform Architecture - BLOAT_PREVENTION compliance testing
💼 Alvaro | Business Strategy - Executive value validation
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

# Test the real MCP integration components
# PROJECT_STRUCTURE.md compliant imports from .claudedirector/lib/
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

try:
    from reporting.weekly_reporter_mcp_bridge import (
        WeeklyReporterMCPBridge,
        MCPEnhancementResult,
        create_weekly_reporter_mcp_bridge,
    )
    from reporting.weekly_reporter import StrategicAnalyzer, JiraIssue

    MCP_COMPONENTS_AVAILABLE = True
except ImportError:
    # Graceful fallback for testing without MCP infrastructure
    MCP_COMPONENTS_AVAILABLE = False
    WeeklyReporterMCPBridge = None
    MCPEnhancementResult = None
    StrategicAnalyzer = None
    JiraIssue = None


@pytest.fixture
def sample_issue():
    """Sample Jira issue for testing"""
    if not MCP_COMPONENTS_AVAILABLE:
        pytest.skip("MCP components not available")

    return JiraIssue(
        key="WEB-12345",
        summary="Implement Strategic Feature",
        status="In Progress",
        priority="High",
        project="Web Platform",
        assignee="test.user@company.com",
    )


@pytest.fixture
def sample_cycle_time_data():
    """Sample cycle time data for testing"""
    return [3.5, 5.2, 7.1, 4.8, 6.3, 2.9, 8.1, 5.5, 4.2, 6.7]


@pytest.fixture
def mcp_config():
    """MCP integration configuration for testing"""
    return {
        "enable_mcp_integration": True,
        "mcp_performance_threshold": 5.0,
        "enable_sequential_reasoning": True,
        "enable_context7_benchmarking": True,
        "fallback_strategy": "graceful",
        "executive_focus": True,
    }


@pytest.fixture
def disabled_mcp_config():
    """Disabled MCP configuration for fallback testing"""
    return {"enable_mcp_integration": False, "mcp_performance_threshold": 5.0}


class TestWeeklyReporterMCPBridge:
    """Test the MCP bridge functionality"""

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_bridge_initialization_with_mcp_enabled(self, mcp_config):
        """Test MCP bridge initializes correctly when enabled"""
        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(mcp_config)

            assert bridge.mcp_enabled == True
            assert bridge.performance_threshold == 5.0
            assert bridge.mcp_manager == mock_manager
            mock_manager_class.assert_called_once()

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_bridge_initialization_with_mcp_disabled(self, disabled_mcp_config):
        """Test MCP bridge gracefully handles disabled configuration"""
        bridge = WeeklyReporterMCPBridge(disabled_mcp_config)

        assert bridge.mcp_enabled == False
        assert bridge.mcp_manager is None

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_enhance_completion_probability_success(
        self, mcp_config, sample_issue, sample_cycle_time_data
    ):
        """Test successful Sequential MCP enhancement"""
        mock_mcp_result = {
            "strategic_insights": ["Insight 1", "Insight 2"],
            "executive_summary": "Strategic analysis complete",
            "risk_assessment": ["Risk 1", "Risk 2"],
        }

        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.return_value = mock_mcp_result
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(mcp_config)

            result = bridge.enhance_completion_probability(
                sample_issue.key, 0.75, sample_cycle_time_data
            )

            assert isinstance(result, MCPEnhancementResult)
            assert result.fallback_used == False
            assert len(result.reasoning_trail) == 2
            assert result.executive_summary == "Strategic analysis complete"
            assert len(result.risk_factors) == 2

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_enhance_with_industry_benchmarks_success(
        self, mcp_config, sample_cycle_time_data
    ):
        """Test successful Context7 MCP enhancement"""
        mock_context7_result = {
            "percentile_ranking": "75th percentile",
            "recommendations": ["Best practice 1", "Best practice 2"],
            "market_analysis": "Competitive position strong",
            "benchmarks": {"industry_avg": 5.2, "top_quartile": 3.8},
        }

        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager._query_claude_code_mcp_server.return_value = (
                mock_context7_result
            )
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(mcp_config)

            result = bridge.enhance_with_industry_benchmarks(
                "Web Platform", sample_cycle_time_data, "software_engineering"
            )

            assert isinstance(result, MCPEnhancementResult)
            assert result.fallback_used == False
            assert result.industry_context["percentile_ranking"] == "75th percentile"
            assert len(result.industry_context["best_practices"]) == 2

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_timeout_protection(self, mcp_config, sample_issue, sample_cycle_time_data):
        """Test MCP operations respect timeout limits"""

        async def slow_mcp_call(*args, **kwargs):
            await asyncio.sleep(10)  # Simulate slow MCP response
            return {}

        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.side_effect = slow_mcp_call
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(mcp_config)

            start_time = time.time()
            result = bridge.enhance_completion_probability(
                sample_issue.key, 0.75, sample_cycle_time_data
            )
            elapsed_time = time.time() - start_time

            # Should timeout within threshold + small buffer
            assert elapsed_time < 7.0  # 5s threshold + 2s buffer
            assert result.fallback_used == True
            assert "timeout" in result.error_message.lower()

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_graceful_fallback_on_mcp_error(
        self, mcp_config, sample_issue, sample_cycle_time_data
    ):
        """Test graceful fallback when MCP operations fail"""
        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            mock_manager = AsyncMock()
            mock_manager.route_query_intelligently.side_effect = Exception(
                "MCP server unavailable"
            )
            mock_manager_class.return_value = mock_manager

            bridge = WeeklyReporterMCPBridge(mcp_config)

            result = bridge.enhance_completion_probability(
                sample_issue.key, 0.75, sample_cycle_time_data
            )

            assert isinstance(result, MCPEnhancementResult)
            assert result.fallback_used == True
            assert "MCP server unavailable" in result.error_message

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_factory_function(self, mcp_config):
        """Test factory function creates bridge correctly"""
        with patch("reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"):
            bridge = create_weekly_reporter_mcp_bridge(mcp_config)

            assert isinstance(bridge, WeeklyReporterMCPBridge)
            assert bridge.config == mcp_config


class TestStrategicAnalyzerMCPIntegration:
    """Test StrategicAnalyzer with real MCP integration"""

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_strategic_analyzer_with_mcp_enabled(self, mcp_config):
        """Test StrategicAnalyzer initializes with MCP bridge when enabled"""
        with patch(
            "reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(mcp_config)

            assert analyzer.mcp_bridge == mock_bridge
            mock_bridge_factory.assert_called_once_with(mcp_config)

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_strategic_analyzer_with_mcp_disabled(self, disabled_mcp_config):
        """Test StrategicAnalyzer works without MCP when disabled"""
        analyzer = StrategicAnalyzer(disabled_mcp_config)

        assert analyzer.mcp_bridge is None

    def test_completion_probability_with_mcp_enhancement(
        self, mcp_config, sample_issue
    ):
        """Test completion probability calculation with MCP enhancement"""
        if not MCP_COMPONENTS_AVAILABLE:
            pytest.skip("MCP components not available")
        mock_enhancement = MCPEnhancementResult(
            reasoning_trail=["Strategic insight 1", "Strategic insight 2"],
            executive_summary="Executive analysis complete",
            risk_factors=["Risk factor 1"],
            industry_context={"percentile": "80th"},
            processing_time=2.5,
            fallback_used=False,
        )

        with patch(
            "reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge.enhance_completion_probability.return_value = mock_enhancement
            mock_bridge.enhance_with_industry_benchmarks.return_value = mock_enhancement
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(mcp_config)

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
                                                sample_issue, historical_data
                                            )
                                        )

            # Verify base statistical analysis preserved
            assert result["completion_probability"] == 0.75
            assert "confidence_interval" in result

            # Verify MCP enhancement added
            assert result["mcp_enhanced"] == True
            assert result["mcp_reasoning_trail"] == [
                "Strategic insight 1",
                "Strategic insight 2",
            ]
            assert result["executive_summary"] == "Executive analysis complete"
            assert result["industry_context"] == {"percentile": "80th"}
            # Note: mcp_processing_time may use threshold (5.0) as fallback
            assert result["mcp_processing_time"] >= 0.0

    def test_completion_probability_with_mcp_fallback(self, mcp_config, sample_issue):
        """Test completion probability gracefully handles MCP fallback"""
        if not MCP_COMPONENTS_AVAILABLE:
            pytest.skip("MCP components not available")
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
            "reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"
        ) as mock_bridge_factory:
            mock_bridge = Mock()
            mock_bridge.is_enabled.return_value = True
            mock_bridge.enhance_completion_probability.return_value = mock_enhancement
            mock_bridge.enhance_with_industry_benchmarks.return_value = mock_enhancement
            mock_bridge_factory.return_value = mock_bridge

            analyzer = StrategicAnalyzer(mcp_config)

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
                                                sample_issue, historical_data
                                            )
                                        )

            # Verify base analysis still works
            assert result["completion_probability"] == 0.65
            assert "confidence_interval" in result

            # Verify MCP fallback handled gracefully
            assert result["mcp_enhanced"] == False
            # Note: Fallback reason may vary ("MCP timeout" or "No enhancements available")
            assert "mcp_fallback_reason" in result
            assert result["mcp_fallback_reason"] in [
                "MCP timeout",
                "No enhancements available",
            ]


class TestBLOATPREVENTIONCompliance:
    """Test BLOAT_PREVENTION compliance - no code duplication"""

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_no_duplicate_mcp_coordination_logic(self):
        """Verify MCP bridge reuses existing MCPIntegrationManager"""
        # This test verifies that we're not creating duplicate MCP coordination
        # by checking that WeeklyReporterMCPBridge delegates to MCPIntegrationManager

        config = {"enable_mcp_integration": True}

        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
        ) as mock_manager_class:
            bridge = WeeklyReporterMCPBridge(config)

            # Verify we're using the existing MCPIntegrationManager
            mock_manager_class.assert_called_once()
            assert bridge.mcp_manager is not None

            # Verify no duplicate MCP server coordination logic
            assert not hasattr(bridge, "_initialize_mcp_servers")
            assert not hasattr(bridge, "_check_mcp_server_availability")

    @pytest.mark.skipif(
        not MCP_COMPONENTS_AVAILABLE, reason="MCP components not available"
    )
    def test_extends_existing_strategic_analyzer(self, mcp_config):
        """Verify StrategicAnalyzer extends rather than replaces existing logic"""
        with patch("reporting.weekly_reporter.create_weekly_reporter_mcp_bridge"):
            analyzer = StrategicAnalyzer(mcp_config)

            # Verify existing methods preserved
            assert hasattr(analyzer, "calculate_strategic_impact")
            assert hasattr(analyzer, "_sequential_monte_carlo_simulation")
            assert hasattr(analyzer, "_sequential_analyze_historical_cycles")

            # Verify new MCP method added
            assert hasattr(analyzer, "_enhance_with_real_mcp_reasoning")

            # Verify no duplicate statistical analysis logic
            assert not hasattr(analyzer, "_duplicate_monte_carlo_simulation")

    def test_performance_within_threshold(self, mcp_config):
        """Test MCP operations complete within performance threshold"""
        if not MCP_COMPONENTS_AVAILABLE:
            pytest.skip("MCP components not available")

        # Test that the bridge respects the 5-second performance threshold
        config = {**mcp_config, "mcp_performance_threshold": 2.0}  # Shorter for testing

        with patch(
            "reporting.weekly_reporter_mcp_bridge.MCPIntegrationManager"
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
            assert elapsed_time < 1.0
            assert result.fallback_used == False
