"""
Unit Tests for MCP Enhanced Decision Pipeline - Phase 1

Team: Martin (Lead) + Berny (Senior AI Developer)

Comprehensive test coverage for MCPEnhancedDecisionPipeline ensuring:
- Parallel and sequential MCP server execution
- Pipeline stage coordination and fallback strategies
- Performance requirements (<500ms for complex decisions)
- Integration with existing MCP infrastructure
- Error handling and graceful degradation
"""

import asyncio
import time
import unittest
from unittest.mock import AsyncMock, Mock, patch
from dataclasses import dataclass
from typing import Dict, Any, List

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from lib.ai_intelligence.mcp_decision_pipeline import (
        MCPEnhancedDecisionPipeline,
        MCPPipelineStage,
        PipelineExecutionResult,
        create_mcp_enhanced_decision_pipeline,
    )
    from lib.ai_intelligence.decision_orchestrator import (
        DecisionContext,
        DecisionComplexity,
    )
except ImportError:
    # Fallback for test environment
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    from lib.ai_intelligence.mcp_decision_pipeline import (
        MCPEnhancedDecisionPipeline,
        MCPPipelineStage,
        PipelineExecutionResult,
        create_mcp_enhanced_decision_pipeline,
    )
    from lib.ai_intelligence.decision_orchestrator import (
        DecisionContext,
        DecisionComplexity,
    )


class TestMCPEnhancedDecisionPipeline(unittest.TestCase):
    """Test suite for MCP Enhanced Decision Pipeline"""

    def setUp(self):
        """Set up test environment with mocked dependencies"""
        # Mock existing infrastructure components
        self.mock_mcp_helper = Mock()
        self.mock_framework_integration_engine = Mock()

        # Configure mock MCP helper for async calls
        self.mock_mcp_helper.call_mcp_server = AsyncMock()

        # Configure mock framework integration engine
        self.mock_framework_integration_engine.base_engine = Mock()
        self.mock_framework_integration_engine.base_engine.analyze_systematically.return_value = Mock(
            primary_frameworks=["rumelt_strategy_kernel", "team_topologies"],
            insights=["Strategic insight 1", "Strategic insight 2"],
            confidence_score=0.875,
        )

        # Create pipeline instance
        self.pipeline = MCPEnhancedDecisionPipeline(
            mcp_helper=self.mock_mcp_helper,
            framework_integration_engine=self.mock_framework_integration_engine,
        )

    def test_pipeline_initialization(self):
        """Test pipeline initializes correctly with existing infrastructure"""
        self.assertIsNotNone(self.pipeline)
        self.assertEqual(self.pipeline.pipeline_metrics["pipelines_executed"], 0)
        self.assertEqual(self.pipeline.pipeline_metrics["mcp_enhancement_rate"], 0.0)

        # Verify pipeline stages are configured for all complexity levels
        for complexity in DecisionComplexity:
            self.assertIn(complexity.value, self.pipeline.pipeline_stages)

        # Verify stage timeouts are configured
        expected_stages = [
            "context_analysis",
            "systematic_analysis",
            "visual_enhancement",
            "framework_analysis",
            "framework_integration",
            "synthesis",
        ]
        for stage in expected_stages:
            self.assertIn(stage, self.pipeline.stage_timeouts)

        # Verify fallback strategies are configured
        self.assertIn("context_analysis", self.pipeline.fallback_strategies)
        self.assertIn("systematic_analysis", self.pipeline.fallback_strategies)

    def test_pipeline_stage_configuration(self):
        """Test pipeline stage configuration for different complexity levels"""
        # Simple decisions - framework only
        simple_config = self.pipeline.pipeline_stages[DecisionComplexity.SIMPLE.value]
        self.assertEqual(simple_config["stages"], ["framework_analysis"])
        self.assertEqual(simple_config["mcp_servers"], [])
        self.assertFalse(simple_config["parallel_execution"])

        # Strategic decisions - full pipeline
        strategic_config = self.pipeline.pipeline_stages[
            DecisionComplexity.ENTERPRISE.value
        ]
        expected_stages = [
            "context_analysis",
            "systematic_analysis",
            "visual_enhancement",
            "framework_integration",
            "synthesis",
        ]
        self.assertEqual(strategic_config["stages"], expected_stages)
        self.assertEqual(
            strategic_config["mcp_servers"], ["context7", "sequential", "magic"]
        )
        self.assertTrue(strategic_config["parallel_execution"])

    async def test_single_stage_execution_context_analysis(self):
        """Test individual stage execution - Context7 MCP server"""
        # Mock Context7 MCP server response
        mock_response = {
            "patterns": ["organizational_pattern_1", "organizational_pattern_2"],
            "stakeholders": ["engineering", "product", "design"],
            "insights": ["Context insight 1", "Context insight 2"],
        }
        self.mock_mcp_helper.call_mcp_server.return_value = mock_response

        decision_context = DecisionContext(
            message="How should we restructure our teams for better collaboration?",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.COMPLEX,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering", "product"],
            time_sensitivity="medium_term",
            business_impact="high",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")
        input_data = {"user_input": decision_context.user_input}

        # Execute context analysis stage
        stage_result = await self.pipeline._execute_single_stage(
            "context_analysis", decision_context, transparency_context, input_data
        )

        # Verify stage execution
        self.assertTrue(stage_result.success)
        self.assertEqual(stage_result.stage_name, "context_analysis")
        self.assertEqual(stage_result.mcp_server, "context7")
        self.assertIsNotNone(stage_result.output_data)

        # Verify MCP server was called correctly
        self.mock_mcp_helper.call_mcp_server.assert_called_once_with(
            "context7",
            "pattern_recognition",
            query=decision_context.user_input,
            context=decision_context.stakeholder_scope,
            timeout=200,
        )

        # Verify output data structure
        output = stage_result.output_data
        self.assertIn("organizational_patterns", output)
        self.assertIn("stakeholder_analysis", output)
        self.assertIn("context_insights", output)

    async def test_single_stage_execution_systematic_analysis(self):
        """Test individual stage execution - Sequential MCP server"""
        # Mock Sequential MCP server response
        mock_response = {
            "analysis": ["Systematic analysis 1", "Systematic analysis 2"],
            "frameworks": ["rumelt_strategy_kernel", "team_topologies"],
            "recommendations": ["Recommendation 1", "Recommendation 2"],
        }
        self.mock_mcp_helper.call_mcp_server.return_value = mock_response

        decision_context = DecisionContext(
            message="Strategic platform investment decision",
            # session_id moved to metadata"test_session",
            persona="camille",
            complexity=DecisionComplexity.STRATEGIC,
            detected_frameworks=[
                "rumelt_strategy_kernel",
                "capital_allocation_framework",
            ],
            stakeholder_scope=["engineering", "executive"],
            time_sensitivity="long_term",
            business_impact="critical",
        )

        transparency_context = Mock(session_id="test_session", persona="camille")
        input_data = {"user_input": decision_context.user_input}

        # Execute systematic analysis stage
        stage_result = await self.pipeline._execute_single_stage(
            "systematic_analysis", decision_context, transparency_context, input_data
        )

        # Verify stage execution
        self.assertTrue(stage_result.success)
        self.assertEqual(stage_result.stage_name, "systematic_analysis")
        self.assertEqual(stage_result.mcp_server, "sequential")

        # Verify MCP server was called correctly
        self.mock_mcp_helper.call_mcp_server.assert_called_once_with(
            "sequential",
            "systematic_analysis",
            query=decision_context.user_input,
            frameworks=decision_context.detected_frameworks,
            timeout=300,
        )

    async def test_single_stage_execution_framework_analysis(self):
        """Test individual stage execution - Local framework analysis"""
        decision_context = DecisionContext(
            message="Framework analysis test",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.MEDIUM,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering"],
            time_sensitivity="short_term",
            business_impact="medium",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")
        input_data = {"user_input": decision_context.user_input}

        # Execute framework analysis stage
        stage_result = await self.pipeline._execute_single_stage(
            "framework_analysis", decision_context, transparency_context, input_data
        )

        # Verify stage execution
        self.assertTrue(stage_result.success)
        self.assertEqual(stage_result.stage_name, "framework_analysis")
        self.assertEqual(
            stage_result.mcp_server, ""
        )  # No MCP server for local analysis

        # Verify framework engine was called
        self.mock_framework_integration_engine.base_engine.analyze_systematically.assert_called_once()

        # Verify output data structure
        output = stage_result.output_data
        self.assertIn("primary_frameworks", output)
        self.assertIn("framework_insights", output)
        self.assertIn("confidence_score", output)

    async def test_sequential_stage_execution(self):
        """Test sequential pipeline execution for moderate complexity decisions"""
        # Mock MCP server responses
        context_response = {
            "patterns": ["pattern1"],
            "stakeholders": ["engineering"],
            "insights": ["insight1"],
        }
        self.mock_mcp_helper.call_mcp_server.return_value = context_response

        decision_context = DecisionContext(
            message="Moderate complexity decision requiring sequential processing",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.MEDIUM,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering"],
            time_sensitivity="medium_term",
            business_impact="medium",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")
        stages = ["context_analysis", "framework_analysis"]

        # Execute sequential stages
        executed_stages = await self.pipeline._execute_sequential_stages(
            decision_context, transparency_context, stages
        )

        # Verify both stages executed
        self.assertEqual(len(executed_stages), 2)
        self.assertEqual(executed_stages[0].stage_name, "context_analysis")
        self.assertEqual(executed_stages[1].stage_name, "framework_analysis")

        # Verify both stages succeeded
        for stage in executed_stages:
            self.assertTrue(stage.success)

    async def test_parallel_stage_execution(self):
        """Test parallel pipeline execution for strategic complexity decisions"""
        # Mock MCP server responses
        mcp_responses = {
            "context7": {
                "patterns": ["pattern1"],
                "stakeholders": ["engineering"],
                "insights": ["context_insight"],
            },
            "sequential": {
                "analysis": ["systematic_analysis"],
                "frameworks": ["rumelt_strategy_kernel"],
                "recommendations": ["recommendation1"],
            },
            "magic": {
                "diagrams": ["diagram1"],
                "elements": ["element1"],
                "insights": ["visual_insight"],
            },
        }

        async def mock_mcp_call(server, capability, **kwargs):
            return mcp_responses.get(server, {})

        self.mock_mcp_helper.call_mcp_server.side_effect = mock_mcp_call

        decision_context = DecisionContext(
            message="Strategic decision requiring parallel MCP processing",
            # session_id moved to metadata"test_session",
            persona="camille",
            complexity=DecisionComplexity.STRATEGIC,
            detected_frameworks=["rumelt_strategy_kernel", "team_topologies"],
            stakeholder_scope=["engineering", "executive"],
            time_sensitivity="long_term",
            business_impact="critical",
        )

        transparency_context = Mock(session_id="test_session", persona="camille")
        stages = [
            "context_analysis",
            "systematic_analysis",
            "visual_enhancement",
            "framework_integration",
        ]

        # Execute parallel stages
        executed_stages = await self.pipeline._execute_parallel_stages(
            decision_context, transparency_context, stages
        )

        # Verify all stages executed
        self.assertGreaterEqual(
            len(executed_stages), 3
        )  # At least MCP stages + framework stages

        # Verify MCP stages executed in parallel
        mcp_stage_names = [s.stage_name for s in executed_stages if s.mcp_server]
        self.assertIn("context_analysis", mcp_stage_names)
        self.assertIn("systematic_analysis", mcp_stage_names)

    async def test_pipeline_execution_with_fallback(self):
        """Test pipeline execution with MCP server failure and fallback"""

        # Mock MCP server failure for context analysis
        async def mock_mcp_call_with_failure(server, capability, **kwargs):
            if server == "context7":
                raise Exception("Context7 server unavailable")
            return {"analysis": ["fallback_analysis"]}

        self.mock_mcp_helper.call_mcp_server.side_effect = mock_mcp_call_with_failure

        decision_context = DecisionContext(
            message="Decision with MCP server failure",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.MEDIUM,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering"],
            time_sensitivity="medium_term",
            business_impact="medium",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")
        stages = ["context_analysis", "framework_analysis"]

        # Execute sequential stages with failure
        executed_stages = await self.pipeline._execute_sequential_stages(
            decision_context, transparency_context, stages
        )

        # Should have fallback to framework_analysis
        stage_names = [s.stage_name for s in executed_stages]
        self.assertIn("framework_analysis", stage_names)

        # At least one stage should have succeeded (the fallback)
        successful_stages = [s for s in executed_stages if s.success]
        self.assertGreater(len(successful_stages), 0)

    async def test_full_pipeline_execution_simple(self):
        """Test complete pipeline execution for simple decisions"""
        decision_context = DecisionContext(
            message="Simple decision requiring basic framework analysis",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.SIMPLE,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering"],
            time_sensitivity="short_term",
            business_impact="low",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")

        # Execute full pipeline
        result = await self.pipeline.execute_pipeline(
            decision_context, transparency_context
        )

        # Verify successful execution
        self.assertTrue(result.success)
        self.assertIsNone(result.error_message)
        self.assertEqual(result.decision_context, decision_context)

        # Simple decisions should not use MCP servers
        self.assertEqual(len(result.mcp_enhancements_applied), 0)

        # Should have framework analysis results
        self.assertGreater(len(result.final_recommendations), 0)
        self.assertGreater(result.confidence_score, 0.0)

    async def test_full_pipeline_execution_strategic(self):
        """Test complete pipeline execution for strategic decisions"""
        # Mock successful MCP responses
        mcp_responses = {
            "context7": {
                "patterns": ["pattern1"],
                "stakeholders": ["eng"],
                "insights": ["insight1"],
            },
            "sequential": {
                "analysis": ["analysis1"],
                "frameworks": ["framework1"],
                "recommendations": ["rec1"],
            },
            "magic": {
                "diagrams": ["diagram1"],
                "elements": ["element1"],
                "insights": ["visual1"],
            },
        }

        async def mock_mcp_call(server, capability, **kwargs):
            return mcp_responses.get(server, {})

        self.mock_mcp_helper.call_mcp_server.side_effect = mock_mcp_call

        decision_context = DecisionContext(
            message="Strategic decision requiring full MCP coordination",
            # session_id moved to metadata"test_session",
            persona="camille",
            complexity=DecisionComplexity.STRATEGIC,
            detected_frameworks=["rumelt_strategy_kernel", "team_topologies"],
            stakeholder_scope=["engineering", "executive"],
            time_sensitivity="long_term",
            business_impact="critical",
        )

        transparency_context = Mock(session_id="test_session", persona="camille")

        # Execute full pipeline
        result = await self.pipeline.execute_pipeline(
            decision_context, transparency_context
        )

        # Verify successful execution
        self.assertTrue(result.success)
        self.assertIsNone(result.error_message)

        # Strategic decisions should use multiple MCP servers
        self.assertGreater(len(result.mcp_enhancements_applied), 0)

        # Should have comprehensive results
        self.assertGreater(len(result.final_recommendations), 0)
        self.assertGreater(
            result.confidence_score, 0.8
        )  # High confidence for strategic decisions
        self.assertGreater(len(result.stages_executed), 2)  # Multiple stages

    async def test_pipeline_performance_requirements(self):
        """Test pipeline meets performance requirements"""
        # Mock fast MCP responses
        self.mock_mcp_helper.call_mcp_server.return_value = {"status": "success"}

        decision_context = DecisionContext(
            message="Performance test decision",
            # session_id moved to metadata"test_session",
            persona="diego",
            complexity=DecisionComplexity.COMPLEX,
            detected_frameworks=["team_topologies"],
            stakeholder_scope=["engineering"],
            time_sensitivity="medium_term",
            business_impact="medium",
        )

        transparency_context = Mock(session_id="test_session", persona="diego")

        # Execute pipeline and measure time
        start_time = time.time()
        result = await self.pipeline.execute_pipeline(
            decision_context, transparency_context
        )
        execution_time_ms = (time.time() - start_time) * 1000

        # Verify performance requirements
        self.assertTrue(result.success)
        self.assertLess(
            execution_time_ms, 500, "Pipeline execution too slow for complex decisions"
        )
        self.assertLess(
            result.total_processing_time_ms, 600, "Reported processing time too high"
        )

    def test_result_synthesis(self):
        """Test pipeline result synthesis from multiple stages"""
        # Create mock stages with different outputs
        stages = [
            MCPPipelineStage(
                stage_name="context_analysis",
                mcp_server="context7",
                capability="pattern_recognition",
                input_data={},
                output_data={
                    "context_insights": ["Context insight 1", "Context insight 2"],
                    "stakeholder_analysis": ["Stakeholder 1", "Stakeholder 2"],
                },
                processing_time_ms=150,
                success=True,
            ),
            MCPPipelineStage(
                stage_name="systematic_analysis",
                mcp_server="sequential",
                capability="systematic_analysis",
                input_data={},
                output_data={
                    "systematic_insights": ["Systematic insight 1"],
                    "strategic_recommendations": ["Strategic rec 1", "Strategic rec 2"],
                },
                processing_time_ms=200,
                success=True,
            ),
            MCPPipelineStage(
                stage_name="framework_analysis",
                mcp_server="",
                capability="framework_analysis",
                input_data={},
                output_data={
                    "primary_frameworks": ["rumelt_strategy_kernel"],
                    "confidence_score": 0.9,
                },
                processing_time_ms=100,
                success=True,
            ),
        ]

        decision_context = DecisionContext(
            message="Synthesis test",
            persona="diego",
            complexity=DecisionComplexity.COMPLEX,
            stakeholders=["engineering"],
            metadata={
                "detected_frameworks": ["rumelt_strategy_kernel"],
                "time_sensitivity": "medium_term",
                "business_impact": "medium",
                "session_id": "test_session",
            },
        )

        # Test synthesis
        recommendations, confidence, insights = asyncio.run(
            self.pipeline._synthesize_pipeline_results(decision_context, stages)
        )

        # Verify synthesis results
        self.assertGreater(len(recommendations), 0)
        self.assertGreater(
            confidence, 0.8
        )  # Should be high due to successful MCP stages
        self.assertIn("detected_frameworks", insights)

        # Should include recommendations from MCP stages
        recommendations_text = " ".join(recommendations)
        self.assertIn("Strategic rec", recommendations_text)

    def test_pipeline_metrics_tracking(self):
        """Test pipeline performance metrics tracking"""
        initial_count = self.pipeline.pipeline_metrics["pipelines_executed"]
        initial_avg = self.pipeline.pipeline_metrics["avg_processing_time_ms"]
        initial_enhancement_rate = self.pipeline.pipeline_metrics[
            "mcp_enhancement_rate"
        ]

        # Simulate successful pipeline execution with MCP enhancements
        self.pipeline._update_pipeline_metrics(300, 2, True)

        # Verify metrics updated
        self.assertEqual(
            self.pipeline.pipeline_metrics["pipelines_executed"], initial_count + 1
        )
        self.assertGreater(
            self.pipeline.pipeline_metrics["avg_processing_time_ms"], initial_avg
        )
        self.assertGreater(
            self.pipeline.pipeline_metrics["mcp_enhancement_rate"],
            initial_enhancement_rate,
        )

    def test_stage_timeout_configuration(self):
        """Test stage timeout configuration is appropriate"""
        timeouts = self.pipeline.stage_timeouts

        # Verify reasonable timeout values
        self.assertLessEqual(timeouts["context_analysis"], 300)
        self.assertLessEqual(timeouts["systematic_analysis"], 400)
        self.assertLessEqual(
            timeouts["framework_analysis"], 200
        )  # Local, should be fast

        # Verify all required stages have timeouts
        required_stages = [
            "context_analysis",
            "systematic_analysis",
            "visual_enhancement",
            "framework_analysis",
            "framework_integration",
            "synthesis",
        ]
        for stage in required_stages:
            self.assertIn(stage, timeouts)
            self.assertGreater(timeouts[stage], 0)

    def test_error_handling_and_recovery(self):
        """Test comprehensive error handling and recovery"""

        async def _async_test():
            return await self._test_error_handling_and_recovery()

        # Run async test
        asyncio.run(_async_test())

    async def _test_error_handling_and_recovery(self):
        # Mock complete MCP failure
        self.mock_mcp_helper.call_mcp_server.side_effect = Exception(
            "All MCP servers down"
        )

        decision_context = DecisionContext(
            message="Decision with complete MCP failure",
            persona="diego",
            complexity=DecisionComplexity.ENTERPRISE,  # Would normally use MCP
            stakeholders=["engineering"],
            metadata={
                "detected_frameworks": ["team_topologies"],
                "time_sensitivity": "medium_term",
                "business_impact": "high",
                "session_id": "test_session",
            },
        )

        transparency_context = Mock(session_id="test_session", persona="diego")

        # Execute pipeline (should handle failure gracefully)
        result = await self.pipeline.execute_pipeline(
            decision_context, transparency_context
        )

        # Should still provide some results via framework analysis
        self.assertTrue(result.success)  # Should succeed with fallback
        self.assertEqual(len(result.mcp_enhancements_applied), 0)  # No MCP enhancements
        self.assertGreater(
            len(result.final_recommendations), 0
        )  # Should have fallback recommendations


class TestMCPPipelineFactory(unittest.TestCase):
    """Test factory function for creating MCP pipeline"""

    def test_factory_function(self):
        """Test factory function creates pipeline correctly"""
        mock_mcp_helper = Mock()
        mock_framework_engine = Mock()

        # Create pipeline via factory
        pipeline = create_mcp_enhanced_decision_pipeline(
            mcp_helper=mock_mcp_helper,
            framework_integration_engine=mock_framework_engine,
        )

        # Verify pipeline created correctly
        self.assertIsInstance(pipeline, MCPEnhancedDecisionPipeline)
        self.assertEqual(pipeline.mcp_helper, mock_mcp_helper)
        self.assertEqual(pipeline.framework_engine, mock_framework_engine)


if __name__ == "__main__":
    unittest.main()
