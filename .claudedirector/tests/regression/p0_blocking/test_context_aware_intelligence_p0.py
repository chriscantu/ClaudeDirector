"""
P0 Tests for Refactored Context-Aware Intelligence

Critical performance and functionality tests for modular context intelligence.
"""

import unittest
import asyncio
import time
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

# Import components to test
try:
    from claudedirector.lib.ai_intelligence.context_aware_intelligence import ContextAwareIntelligence
    from claudedirector.lib.ai_intelligence.context.context_analyzer import (
        ContextComplexity,
        SituationalContext,
    )
    from claudedirector.lib.ai_intelligence.context.framework_selector import ContextualFrameworkRecommendation
    from claudedirector.lib.ai_intelligence.context.persona_selector import PersonaActivationRecommendation
except ImportError:
    from lib.ai_intelligence.context_aware_intelligence import ContextAwareIntelligence
    from lib.ai_intelligence.context.context_analyzer import (
        ContextComplexity,
        SituationalContext,
    )
    from lib.ai_intelligence.context.framework_selector import ContextualFrameworkRecommendation
    from lib.ai_intelligence.context.persona_selector import PersonaActivationRecommendation


class TestContextAwareIntelligenceV2P0(unittest.TestCase):
    """P0 test suite for refactored Context-Aware Intelligence"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_context_engine = Mock()
        self.mock_framework_detector = Mock()
        self.mock_mcp_pipeline = Mock()
        self.mock_predictive_engine = Mock()

        # Mock context engine layers
        self.mock_context_engine.conversation_layer = Mock()
        self.mock_context_engine.strategic_layer = Mock()
        self.mock_context_engine.stakeholder_layer = Mock()
        self.mock_context_engine.learning_layer = Mock()
        self.mock_context_engine.organizational_layer = Mock()
        self.mock_context_engine.team_dynamics_engine = Mock()

        self.config = {
            "response_time_target_ms": 200,
            "relevance_threshold": 0.8,
            "cache_duration": 15,
        }

        self.intelligence = ContextAwareIntelligence(
            context_engine=self.mock_context_engine,
            framework_detector=self.mock_framework_detector,
            mcp_pipeline=self.mock_mcp_pipeline,
            predictive_engine=self.mock_predictive_engine,
            config=self.config,
        )

    def test_p0_initialization_performance(self):
        """P0: Intelligence initialization must complete within performance targets"""
        start_time = time.time()

        intelligence = ContextAwareIntelligence(
            context_engine=self.mock_context_engine,
            framework_detector=self.mock_framework_detector,
            config=self.config,
        )

        initialization_time = (time.time() - start_time) * 1000

        # P0 CRITICAL: Initialization must be under 100ms
        self.assertLess(
            initialization_time,
            100,
            f"Initialization took {initialization_time:.1f}ms, must be <100ms",
        )

        # Verify all components are initialized
        self.assertIsNotNone(intelligence.context_analyzer)
        self.assertIsNotNone(intelligence.framework_selector)
        self.assertIsNotNone(intelligence.persona_selector)

    def test_p0_context_analysis_performance(self):
        """P0: Context analysis must meet response time targets"""

        async def run_analysis_test():
            start_time = time.time()

            context_analysis = await self.intelligence.analyze_strategic_context(
                "How should we restructure our engineering teams?"
            )

            analysis_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Context analysis must be under 200ms
            self.assertLess(
                analysis_time,
                200,
                f"Context analysis took {analysis_time:.1f}ms, must be <200ms",
            )

            # Verify analysis structure
            self.assertIn("situational_context", context_analysis)
            self.assertIn("complexity_level", context_analysis)
            self.assertIn("stakeholder_analysis", context_analysis)
            self.assertIn("time_sensitivity", context_analysis)

            # Verify enum types
            self.assertIsInstance(
                context_analysis["situational_context"], SituationalContext
            )
            self.assertIsInstance(
                context_analysis["complexity_level"], ContextComplexity
            )

        asyncio.run(run_analysis_test())

    def test_p0_framework_recommendation_performance(self):
        """P0: Framework recommendation must meet performance targets"""

        async def run_framework_test():
            # First get context analysis
            context_analysis = await self.intelligence.analyze_strategic_context(
                "Strategic planning for next quarter"
            )

            start_time = time.time()

            framework_rec = await self.intelligence.recommend_optimal_framework(
                context_analysis
            )

            recommendation_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Framework recommendation must be under 150ms
            self.assertLess(
                recommendation_time,
                150,
                f"Framework recommendation took {recommendation_time:.1f}ms, must be <150ms",
            )

            # Verify recommendation structure
            self.assertIsInstance(framework_rec, ContextualFrameworkRecommendation)
            self.assertIsNotNone(framework_rec.framework_name)
            self.assertGreaterEqual(framework_rec.confidence_score, 0.0)
            self.assertLessEqual(framework_rec.confidence_score, 1.0)
            self.assertIsInstance(framework_rec.key_focus_areas, list)
            self.assertIsInstance(framework_rec.adaptation_suggestions, list)

        asyncio.run(run_framework_test())

    def test_p0_persona_recommendation_performance(self):
        """P0: Persona recommendation must meet performance targets"""

        async def run_persona_test():
            # First get context analysis
            context_analysis = await self.intelligence.analyze_strategic_context(
                "Executive communication for board presentation"
            )

            start_time = time.time()

            persona_rec = await self.intelligence.recommend_optimal_persona(
                context_analysis
            )

            recommendation_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Persona recommendation must be under 100ms
            self.assertLess(
                recommendation_time,
                100,
                f"Persona recommendation took {recommendation_time:.1f}ms, must be <100ms",
            )

            # Verify recommendation structure
            self.assertIsInstance(persona_rec, PersonaActivationRecommendation)
            self.assertIn(
                persona_rec.recommended_persona,
                ["diego", "camille", "rachel", "alvaro", "martin"],
            )
            self.assertGreaterEqual(persona_rec.activation_confidence, 0.0)
            self.assertLessEqual(persona_rec.activation_confidence, 1.0)
            self.assertIsInstance(persona_rec.selection_reasoning, list)

        asyncio.run(run_persona_test())

    def test_p0_adaptive_strategy_generation(self):
        """P0: Complete adaptive strategy generation must work end-to-end"""

        async def run_strategy_test():
            start_time = time.time()

            # Full end-to-end workflow
            context_analysis = await self.intelligence.analyze_strategic_context(
                "How do we improve team coordination and delivery quality?"
            )

            framework_rec = await self.intelligence.recommend_optimal_framework(
                context_analysis
            )

            persona_rec = await self.intelligence.recommend_optimal_persona(
                context_analysis
            )

            strategy = await self.intelligence.generate_adaptive_response_strategy(
                context_analysis, framework_rec, persona_rec
            )

            total_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Complete workflow must be under 500ms
            self.assertLess(
                total_time,
                500,
                f"Complete strategy generation took {total_time:.1f}ms, must be <500ms",
            )

            # Verify strategy structure
            self.assertIn("context_analysis", strategy)
            self.assertIn("framework_strategy", strategy)
            self.assertIn("persona_strategy", strategy)
            self.assertIn("response_guidance", strategy)
            self.assertIn("performance_metrics", strategy)

            # Verify performance metrics are tracked
            perf_metrics = strategy["performance_metrics"]
            self.assertIn("total_analysis_time_ms", perf_metrics)
            self.assertIn("context_analysis_time_ms", perf_metrics)
            self.assertIn("framework_selection_time_ms", perf_metrics)

        asyncio.run(run_strategy_test())

    def test_p0_component_integration(self):
        """P0: All modular components must integrate correctly"""

        # Verify component initialization
        self.assertIsNotNone(self.intelligence.context_analyzer)
        self.assertIsNotNone(self.intelligence.framework_selector)
        self.assertIsNotNone(self.intelligence.persona_selector)

        # Test analyzer methods availability
        analyzer = self.intelligence.context_analyzer
        self.assertTrue(hasattr(analyzer, "analyze_query_characteristics"))
        self.assertTrue(hasattr(analyzer, "classify_situational_context"))
        self.assertTrue(hasattr(analyzer, "assess_context_complexity"))

        # Test selector methods availability
        framework_selector = self.intelligence.framework_selector
        self.assertTrue(hasattr(framework_selector, "recommend_optimal_framework"))

        persona_selector = self.intelligence.persona_selector
        self.assertTrue(hasattr(persona_selector, "recommend_optimal_persona"))

    def test_p0_cache_functionality(self):
        """P0: Context analysis caching must work correctly"""

        async def run_cache_test():
            query = "Test strategic question for caching"

            # First call - should cache results
            start_time = time.time()
            context1 = await self.intelligence.analyze_strategic_context(query)
            first_call_time = time.time() - start_time

            # Second call - should use cache
            start_time = time.time()
            context2 = await self.intelligence.analyze_strategic_context(query)
            second_call_time = time.time() - start_time

            # P0 CRITICAL: Second call should be significantly faster (cached)
            self.assertLess(
                second_call_time,
                first_call_time / 2,
                f"Cache not working: second call {second_call_time:.3f}s vs first {first_call_time:.3f}s",
            )

            # Results should be identical (from cache)
            self.assertEqual(context1["query"], context2["query"])
            self.assertEqual(
                context1["situational_context"], context2["situational_context"]
            )
            self.assertEqual(context1["complexity_level"], context2["complexity_level"])

        asyncio.run(run_cache_test())

    def test_p0_error_resilience(self):
        """P0: Intelligence must handle errors gracefully without crashing"""

        async def run_error_test():
            # Test with context gathering failure
            with patch.object(
                self.intelligence,
                "_gather_layered_context",
                side_effect=Exception("Context error"),
            ):
                context_analysis = await self.intelligence.analyze_strategic_context(
                    "test query"
                )
                # Should return default analysis, not crash
                self.assertIn("query", context_analysis)
                self.assertIn("error", context_analysis)

            # Test framework recommendation with invalid context
            invalid_context = {"query": "test", "situational_context": None}
            framework_rec = await self.intelligence.recommend_optimal_framework(
                invalid_context
            )
            # Should return default recommendation, not crash
            self.assertIsInstance(framework_rec, ContextualFrameworkRecommendation)

            # Test persona recommendation with invalid context
            persona_rec = await self.intelligence.recommend_optimal_persona(
                invalid_context
            )
            # Should return default recommendation, not crash
            self.assertIsInstance(persona_rec, PersonaActivationRecommendation)

        asyncio.run(run_error_test())

    def test_p0_situational_context_classification(self):
        """P0: Situational context classification must be accurate"""

        test_cases = [
            (
                "Emergency system failure needs immediate attention",
                SituationalContext.CRISIS_RESPONSE,
            ),
            (
                "Board presentation for VP on strategy",
                SituationalContext.EXECUTIVE_COMMUNICATION,
            ),
            (
                "Team coordination for cross-functional project",
                SituationalContext.TEAM_COORDINATION,
            ),
            (
                "Technical architecture decision needed",
                SituationalContext.TECHNICAL_DECISION,
            ),
            (
                "Stakeholder alignment on requirements",
                SituationalContext.STAKEHOLDER_ALIGNMENT,
            ),
        ]

        async def run_classification_test():
            for query, expected_context in test_cases:
                context_analysis = await self.intelligence.analyze_strategic_context(
                    query
                )
                actual_context = context_analysis["situational_context"]

                self.assertEqual(
                    actual_context,
                    expected_context,
                    f"Query '{query}' classified as {actual_context}, expected {expected_context}",
                )

        asyncio.run(run_classification_test())

    def test_p0_complexity_assessment_accuracy(self):
        """P0: Complexity assessment must be accurate"""

        test_cases = [
            ("Simple bug fix", ContextComplexity.SIMPLE),
            ("Cross-team feature planning", ContextComplexity.MODERATE),
            ("Organization-wide process changes", ContextComplexity.COMPLEX),
            (
                "Enterprise architecture transformation with executive oversight",
                ContextComplexity.ENTERPRISE,
            ),
        ]

        async def run_complexity_test():
            for query, expected_complexity in test_cases:
                context_analysis = await self.intelligence.analyze_strategic_context(
                    query
                )
                actual_complexity = context_analysis["complexity_level"]

                # Allow for some flexibility in complexity assessment
                complexity_order = [
                    ContextComplexity.SIMPLE,
                    ContextComplexity.MODERATE,
                    ContextComplexity.COMPLEX,
                    ContextComplexity.ENTERPRISE,
                ]

                expected_index = complexity_order.index(expected_complexity)
                actual_index = complexity_order.index(actual_complexity)

                # Should be within 1 level of expected
                self.assertLessEqual(
                    abs(actual_index - expected_index),
                    1,
                    f"Query '{query}' assessed as {actual_complexity}, expected {expected_complexity}",
                )

        asyncio.run(run_complexity_test())


if __name__ == "__main__":
    unittest.main()
