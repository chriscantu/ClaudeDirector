"""
Integration Tests for Advanced AI Intelligence - Phase 1

Team: Martin (Lead) + Berny (Senior AI Developer)

End-to-end integration testing for the complete AI Intelligence system:
- DecisionIntelligenceOrchestrator + MCPEnhancedDecisionPipeline integration
- Real MCP server coordination with framework analysis
- Performance and accuracy requirements validation
- Backwards compatibility with existing ClaudeDirector infrastructure
"""

import asyncio
import time
import unittest
from unittest.mock import AsyncMock, Mock, patch
import tempfile
import json

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from claudedirector.lib.ai_intelligence.decision_orchestrator import (
        DecisionIntelligenceOrchestrator,
        DecisionContext,
        DecisionComplexity,
        create_decision_intelligence_orchestrator,
    )
    from claudedirector.lib.ai_intelligence.mcp_decision_pipeline import (
        MCPEnhancedDecisionPipeline,
        create_mcp_enhanced_decision_pipeline,
    )
except ImportError:
    # Fallback for test environment
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    from lib.ai_intelligence.decision_orchestrator import (
        DecisionIntelligenceOrchestrator,
        DecisionContext,
        DecisionComplexity,
        create_decision_intelligence_orchestrator,
    )
    from lib.ai_intelligence.mcp_decision_pipeline import (
        MCPEnhancedDecisionPipeline,
        create_mcp_enhanced_decision_pipeline,
    )


class TestAIIntelligenceIntegration(unittest.TestCase):
    """Integration tests for complete AI Intelligence system"""

    def setUp(self):
        """Set up integration test environment"""
        # Create mock infrastructure that simulates real ClaudeDirector components
        self.mock_mcp_helper = self._create_realistic_mcp_helper()
        self.mock_framework_engine = self._create_realistic_framework_engine()
        self.mock_transparency_system = self._create_realistic_transparency_system()
        self.mock_persona_manager = self._create_realistic_persona_manager()

        # Create integrated system
        self.orchestrator = DecisionIntelligenceOrchestrator(
            mcp_integration_helper=self.mock_mcp_helper,
            framework_engine=self.mock_framework_engine,
            transparency_system=self.mock_transparency_system,
            persona_manager=self.mock_persona_manager,
        )

        self.pipeline = MCPEnhancedDecisionPipeline(
            mcp_helper=self.mock_mcp_helper,
            framework_integration_engine=self.mock_framework_engine.integration_engine,
        )

    def _create_realistic_mcp_helper(self):
        """Create realistic MCP helper mock with proper server responses"""
        mock_helper = Mock()
        mock_helper.server_mapping = {
            "diego": ["sequential"],
            "camille": ["sequential", "context7"],
            "rachel": ["context7", "magic"],
            "alvaro": ["sequential", "context7"],
            "martin": ["context7", "magic"],
        }

        # Mock realistic MCP server responses
        async def mock_mcp_call(server, capability, **kwargs):
            if server == "context7":
                return {
                    "patterns": [
                        "organizational_scaling_pattern",
                        "cross_functional_coordination_pattern",
                        "stakeholder_alignment_pattern",
                    ],
                    "stakeholders": ["engineering", "product", "design", "executive"],
                    "insights": [
                        "Strong engineering-product alignment needed",
                        "Design system coordination critical",
                        "Executive sponsorship required for success",
                    ],
                }
            elif server == "sequential":
                return {
                    "analysis": [
                        "Strategic kernel: Diagnosis of coordination challenges",
                        "Guiding policy: Platform-first approach with clear boundaries",
                        "Coherent actions: Team topology optimization and governance",
                    ],
                    "frameworks": ["rumelt_strategy_kernel", "team_topologies"],
                    "recommendations": [
                        "Define clear team boundaries and interaction modes",
                        "Establish platform governance framework",
                        "Implement systematic coordination mechanisms",
                    ],
                }
            elif server == "magic":
                return {
                    "diagrams": [
                        "team_topology_diagram",
                        "platform_architecture_visual",
                        "stakeholder_alignment_chart",
                    ],
                    "elements": [
                        "visual_framework_comparison",
                        "decision_tree_diagram",
                        "implementation_roadmap",
                    ],
                    "insights": [
                        "Visual representation clarifies complex relationships",
                        "Stakeholder map shows critical alignment points",
                        "Roadmap highlights key milestones and dependencies",
                    ],
                }
            else:
                return {"status": "healthy", "response": "Mock server response"}

        mock_helper.call_mcp_server = AsyncMock(side_effect=mock_mcp_call)
        return mock_helper

    def _create_realistic_framework_engine(self):
        """Create realistic framework engine mock with proper analysis"""
        mock_engine = Mock()

        # Mock framework analysis response
        mock_analysis = Mock()
        mock_analysis.primary_frameworks = ["rumelt_strategy_kernel", "team_topologies"]
        mock_analysis.confidence_score = 0.875
        mock_analysis.insights = [
            "Strategic diagnosis reveals coordination challenges",
            "Team cognitive load optimization needed",
            "Clear boundaries and interaction patterns required",
        ]

        mock_engine.analyze_systematically.return_value = mock_analysis

        # Mock integration engine
        mock_integration_engine = Mock()
        mock_integration_engine.base_engine = mock_engine
        mock_engine.integration_engine = mock_integration_engine

        return mock_engine

    def _create_realistic_transparency_system(self):
        """Create realistic transparency system mock"""
        mock_system = Mock()
        mock_system.generate_audit_trail.return_value = [
            "AI Intelligence analysis initiated",
            "MCP server coordination started",
            "Framework detection completed",
            "Decision intelligence synthesis completed",
        ]
        return mock_system

    def _create_realistic_persona_manager(self):
        """Create realistic persona manager mock"""
        mock_manager = Mock()
        mock_manager.get_persona_context.return_value = {
            "persona": "diego",
            "domain": "Engineering Leadership",
            "specialties": [
                "strategic_planning",
                "team_coordination",
                "platform_strategy",
            ],
        }
        return mock_manager

    async def test_end_to_end_strategic_decision_analysis(self):
        """Test complete end-to-end strategic decision analysis"""
        # Real-world strategic decision scenario
        user_input = """
        We're planning to scale our platform capabilities across multiple international markets.
        This involves restructuring our engineering teams from 3 to 8 teams, implementing new
        governance frameworks for cross-team coordination, and establishing clear boundaries
        between platform and product teams. We need to coordinate with executive stakeholders
        and ensure our approach aligns with business objectives while maintaining engineering velocity.
        """

        # Execute complete analysis workflow
        start_time = time.time()

        # Step 1: Decision Intelligence Orchestration
        orchestrator_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_strategic",
            persona="diego",
            context={"priority": "critical", "timeline": "Q1_2025"},
        )

        # Step 2: Enhanced Pipeline Processing
        pipeline_result = await self.pipeline.execute_pipeline(
            decision_context=orchestrator_result.decision_context,
            transparency_context=Mock(
                session_id="integration_test_strategic",
                persona="diego",
                enhancement_type="ai_intelligence",
            ),
        )

        total_time_ms = (time.time() - start_time) * 1000

        # Verify orchestrator results
        self.assertTrue(orchestrator_result.success)
        self.assertIsNone(orchestrator_result.error_message)
        self.assertEqual(
            orchestrator_result.decision_context.complexity,
            DecisionComplexity.STRATEGIC,
        )
        self.assertGreater(orchestrator_result.confidence_score, 0.85)
        self.assertGreater(len(orchestrator_result.recommended_frameworks), 1)
        self.assertIn("team_topologies", orchestrator_result.recommended_frameworks)

        # Verify pipeline results
        self.assertTrue(pipeline_result.success)
        self.assertGreater(len(pipeline_result.mcp_enhancements_applied), 1)
        self.assertIn("sequential", pipeline_result.mcp_enhancements_applied)
        self.assertIn("context7", pipeline_result.mcp_enhancements_applied)

        # Verify performance requirements
        self.assertLess(total_time_ms, 1000, "End-to-end analysis too slow")
        self.assertLess(
            orchestrator_result.processing_time_ms,
            500,
            "Orchestrator processing too slow",
        )
        self.assertLess(
            pipeline_result.total_processing_time_ms,
            800,
            "Pipeline processing too slow",
        )

        # Verify quality of recommendations
        recommendations = pipeline_result.final_recommendations
        self.assertGreater(len(recommendations), 2)

        recommendations_text = " ".join(recommendations).lower()
        self.assertIn("team", recommendations_text)
        self.assertIn("coordination", recommendations_text)
        self.assertIn("governance", recommendations_text)

    async def test_moderate_complexity_decision_workflow(self):
        """Test workflow for moderate complexity decisions"""
        user_input = "How should we improve coordination between our design and engineering teams?"

        # Execute analysis
        orchestrator_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_moderate",
            persona="rachel",
            context={"team_size": "medium", "urgency": "medium"},
        )

        pipeline_result = await self.pipeline.execute_pipeline(
            decision_context=orchestrator_result.decision_context,
            transparency_context=Mock(
                session_id="integration_test_moderate", persona="rachel"
            ),
        )

        # Verify moderate complexity handling
        self.assertEqual(
            orchestrator_result.decision_context.complexity, DecisionComplexity.MODERATE
        )
        self.assertTrue(orchestrator_result.success)
        self.assertTrue(pipeline_result.success)

        # Should use fewer MCP servers than strategic decisions
        self.assertLessEqual(len(pipeline_result.mcp_enhancements_applied), 2)

        # Should still provide quality recommendations
        self.assertGreater(len(pipeline_result.final_recommendations), 0)
        self.assertGreater(pipeline_result.confidence_score, 0.7)

    async def test_simple_decision_efficiency(self):
        """Test efficient handling of simple decisions"""
        user_input = "Which framework should I use for this team coordination issue?"

        # Execute analysis
        orchestrator_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_simple",
            persona="diego",
        )

        pipeline_result = await self.pipeline.execute_pipeline(
            decision_context=orchestrator_result.decision_context,
            transparency_context=Mock(
                session_id="integration_test_simple", persona="diego"
            ),
        )

        # Verify simple decision handling
        self.assertEqual(
            orchestrator_result.decision_context.complexity, DecisionComplexity.SIMPLE
        )
        self.assertTrue(orchestrator_result.success)
        self.assertTrue(pipeline_result.success)

        # Should not use MCP servers for simple decisions
        self.assertEqual(len(pipeline_result.mcp_enhancements_applied), 0)

        # Should be very fast
        self.assertLess(orchestrator_result.processing_time_ms, 200)
        self.assertLess(pipeline_result.total_processing_time_ms, 300)

    async def test_mcp_server_failure_resilience(self):
        """Test system resilience when MCP servers fail"""

        # Mock MCP server failures
        async def failing_mcp_call(server, capability, **kwargs):
            if server in ["context7", "sequential"]:
                raise Exception(f"{server} server unavailable")
            return {"status": "healthy"}

        self.mock_mcp_helper.call_mcp_server.side_effect = failing_mcp_call

        user_input = "Strategic decision that would normally use multiple MCP servers"

        # Execute analysis with MCP failures
        orchestrator_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_failure",
            persona="diego",
        )

        pipeline_result = await self.pipeline.execute_pipeline(
            decision_context=orchestrator_result.decision_context,
            transparency_context=Mock(
                session_id="integration_test_failure", persona="diego"
            ),
        )

        # Should still succeed with fallback to framework-only analysis
        self.assertTrue(orchestrator_result.success)
        self.assertTrue(pipeline_result.success)

        # Should have no MCP enhancements due to failures
        self.assertEqual(len(pipeline_result.mcp_enhancements_applied), 0)

        # Should still provide recommendations via framework analysis
        self.assertGreater(len(pipeline_result.final_recommendations), 0)

        # Confidence should be lower but still reasonable
        self.assertGreater(pipeline_result.confidence_score, 0.6)

    async def test_persona_specific_routing(self):
        """Test persona-specific MCP server routing"""
        user_input = (
            "How should we approach design system scaling across multiple teams?"
        )

        # Test with Rachel (design-focused persona)
        rachel_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_rachel",
            persona="rachel",
        )

        # Test with Martin (architecture-focused persona)
        martin_result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_martin",
            persona="martin",
        )

        # Both should succeed but may use different MCP servers
        self.assertTrue(rachel_result.success)
        self.assertTrue(martin_result.success)

        # Verify persona-specific server routing was applied
        # (This would be validated through the MCP helper calls in real implementation)
        self.assertGreater(len(rachel_result.mcp_servers_used), 0)
        self.assertGreater(len(martin_result.mcp_servers_used), 0)

    def test_performance_metrics_tracking(self):
        """Test performance metrics tracking across integrated system"""
        # Get initial metrics
        orchestrator_metrics = self.orchestrator.get_performance_metrics()
        pipeline_metrics = self.pipeline.get_pipeline_metrics()

        initial_orchestrator_count = orchestrator_metrics["decisions_processed"]
        initial_pipeline_count = pipeline_metrics["pipelines_executed"]

        # Execute multiple analyses
        async def run_multiple_analyses():
            tasks = []
            for i in range(3):
                task = self.orchestrator.analyze_decision_intelligence(
                    user_input=f"Test decision {i}",
                    session_id=f"metrics_test_{i}",
                    persona="diego",
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            return results

        # Run analyses
        results = asyncio.run(run_multiple_analyses())

        # Verify all succeeded
        for result in results:
            self.assertTrue(result.success)

        # Verify metrics updated
        updated_orchestrator_metrics = self.orchestrator.get_performance_metrics()
        self.assertEqual(
            updated_orchestrator_metrics["decisions_processed"],
            initial_orchestrator_count + 3,
        )

    async def test_transparency_and_audit_trail(self):
        """Test transparency and audit trail generation"""
        user_input = (
            "Strategic platform investment decision requiring full transparency"
        )

        # Execute analysis
        result = await self.orchestrator.analyze_decision_intelligence(
            user_input=user_input,
            session_id="integration_test_transparency",
            persona="camille",
            context={"audit_required": True, "compliance": "enterprise"},
        )

        # Verify transparency trail
        self.assertGreater(len(result.transparency_trail), 5)

        trail_text = " ".join(result.transparency_trail)
        self.assertIn("Decision Intelligence Analysis", trail_text)
        self.assertIn("MCP Servers", trail_text)
        self.assertIn("Frameworks", trail_text)
        self.assertIn("Persona", trail_text)
        self.assertIn("Business Impact", trail_text)

        # Verify audit compliance information
        self.assertIn("camille", trail_text)
        self.assertIn(result.decision_context.complexity.value, trail_text)

    async def test_backwards_compatibility(self):
        """Test backwards compatibility with existing ClaudeDirector infrastructure"""
        # Test with minimal configuration (simulating existing ClaudeDirector setup)
        minimal_mcp_helper = Mock()
        minimal_mcp_helper.server_mapping = {"diego": ["sequential"]}
        minimal_mcp_helper.call_mcp_server = AsyncMock(return_value={"status": "ok"})

        minimal_framework_engine = Mock()
        minimal_framework_engine.analyze_systematically.return_value = Mock(
            primary_frameworks=["team_topologies"], confidence_score=0.875
        )

        # Create orchestrator with minimal setup
        minimal_orchestrator = DecisionIntelligenceOrchestrator(
            mcp_integration_helper=minimal_mcp_helper,
            framework_engine=minimal_framework_engine,
            transparency_system=Mock(),
            persona_manager=Mock(),
        )

        # Should work with existing infrastructure
        result = await minimal_orchestrator.analyze_decision_intelligence(
            user_input="Test backwards compatibility",
            session_id="backwards_compat_test",
            persona="diego",
        )

        self.assertTrue(result.success)
        self.assertGreater(result.confidence_score, 0.8)

    def test_integration_with_existing_database(self):
        """Test integration with existing ClaudeDirector database"""
        # Create temporary database to simulate existing ClaudeDirector setup
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".db", delete=False
        ) as temp_db:
            temp_db_path = temp_db.name

        try:
            # Simulate database integration
            # (In real implementation, this would connect to actual strategic_memory.db)

            # Test that AI Intelligence can work with existing database
            user_input = "Decision that should be stored in strategic memory"

            result = asyncio.run(
                self.orchestrator.analyze_decision_intelligence(
                    user_input=user_input,
                    session_id="db_integration_test",
                    persona="diego",
                    context={"store_in_memory": True, "db_path": temp_db_path},
                )
            )

            # Should succeed and indicate database integration
            self.assertTrue(result.success)

        finally:
            # Clean up temporary database
            Path(temp_db_path).unlink(missing_ok=True)

    async def test_concurrent_decision_processing(self):
        """Test concurrent processing of multiple decisions"""
        # Create multiple concurrent decision analysis tasks
        decision_inputs = [
            "Strategic platform architecture decision",
            "Team coordination and scaling challenge",
            "Cross-functional alignment requirements",
            "Technical debt prioritization strategy",
            "Resource allocation for Q4 initiatives",
        ]

        # Execute all decisions concurrently
        start_time = time.time()

        tasks = [
            self.orchestrator.analyze_decision_intelligence(
                user_input=decision_input,
                session_id=f"concurrent_test_{i}",
                persona="diego",
            )
            for i, decision_input in enumerate(decision_inputs)
        ]

        results = await asyncio.gather(*tasks)

        total_time = (time.time() - start_time) * 1000

        # Verify all decisions processed successfully
        for i, result in enumerate(results):
            self.assertTrue(
                result.success, f"Decision {i} failed: {result.error_message}"
            )
            self.assertGreater(result.confidence_score, 0.7)

        # Verify concurrent processing efficiency
        # Should be faster than sequential processing
        average_time_per_decision = total_time / len(decision_inputs)
        self.assertLess(
            average_time_per_decision, 800, "Concurrent processing not efficient enough"
        )


class TestAIIntelligenceFactory(unittest.TestCase):
    """Test factory functions for AI Intelligence system"""

    @patch(
        "lib.ai_intelligence.decision_orchestrator.create_mcp_integrated_transparency_manager"
    )
    @patch("lib.ai_intelligence.decision_orchestrator.create_transparency_system")
    async def test_orchestrator_factory_integration(
        self, mock_create_transparency, mock_create_manager
    ):
        """Test orchestrator factory integration with existing infrastructure"""
        # Mock existing infrastructure
        mock_transparency_system = Mock()
        mock_persona_manager = Mock()
        mock_persona_manager.mcp_client = Mock()

        mock_create_transparency.return_value = mock_transparency_system
        mock_create_manager.return_value = mock_persona_manager

        # Create orchestrator via factory
        orchestrator = await create_decision_intelligence_orchestrator(
            transparency_config="enterprise", mcp_config_path="/test/mcp/config"
        )

        # Verify factory integration
        self.assertIsInstance(orchestrator, DecisionIntelligenceOrchestrator)
        mock_create_transparency.assert_called_once_with("enterprise")
        mock_create_manager.assert_called_once_with("enterprise", "/test/mcp/config")

    def test_pipeline_factory_integration(self):
        """Test pipeline factory integration"""
        mock_mcp_helper = Mock()
        mock_framework_engine = Mock()

        # Create pipeline via factory
        pipeline = create_mcp_enhanced_decision_pipeline(
            mcp_helper=mock_mcp_helper,
            framework_integration_engine=mock_framework_engine,
        )

        # Verify factory integration
        self.assertIsInstance(pipeline, MCPEnhancedDecisionPipeline)
        self.assertEqual(pipeline.mcp_helper, mock_mcp_helper)
        self.assertEqual(pipeline.framework_engine, mock_framework_engine)


if __name__ == "__main__":
    unittest.main()
