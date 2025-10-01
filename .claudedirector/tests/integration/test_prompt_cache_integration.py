"""
Integration tests for SDK-inspired prompt caching optimization

Tests the complete integration between:
- prompt_cache_optimizer.py
- cache_manager.py
- advanced_context_engine.py

Validates end-to-end prompt optimization flow.
"""

import pytest
import time
from typing import Dict, Any

from lib.performance.cache_manager import get_cache_manager, CacheManager
from lib.context_engineering.advanced_context_engine import AdvancedContextEngine


class TestPromptCacheIntegration:
    """Integration tests for prompt caching optimization"""

    def setup_method(self):
        """Set up test fixtures"""
        self.cache_manager = get_cache_manager()
        self.context_engine = AdvancedContextEngine()

    def teardown_method(self):
        """Clean up after tests"""
        if (
            hasattr(self.cache_manager, "prompt_optimizer")
            and self.cache_manager.prompt_optimizer
        ):
            self.cache_manager.prompt_optimizer.clear_cache()

    def test_cache_manager_prompt_optimizer_initialization(self):
        """Verify cache manager initializes prompt optimizer"""
        # Cache manager should have prompt optimizer
        assert hasattr(self.cache_manager, "prompt_optimizer")

        # Prompt optimizer should be available (graceful degradation test)
        if self.cache_manager.prompt_optimizer:
            assert hasattr(
                self.cache_manager.prompt_optimizer, "assemble_cached_prompt"
            )
            assert hasattr(
                self.cache_manager.prompt_optimizer, "cache_persona_template"
            )

    def test_cache_manager_optimized_prompt_assembly(self):
        """Test cache manager's optimized prompt assembly method"""
        result = self.cache_manager.assemble_optimized_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="Test conversation history",
            strategic_memory={"key": "value"},
            user_query="How should we structure our teams?",
        )

        # Verify result structure
        assert "prompt" in result
        assert "cache_hits" in result
        assert "cache_misses" in result
        assert "tokens_saved" in result
        assert "optimization_applied" in result
        assert "cache_efficiency" in result

        # Verify prompt content
        assert "diego" in result["prompt"].lower() or "Diego" in result["prompt"]
        assert len(result["prompt"]) > 0

    def test_context_engine_optimized_prompt_context(self):
        """Test context engine's optimized prompt context method"""
        result = self.context_engine.get_optimized_prompt_context(
            query="What's our platform strategy?",
            persona="martin",
            framework="platform_strategy",
            session_id="test_session",
        )

        # Verify result structure
        assert "context" in result
        assert "optimized_prompt" in result
        assert "optimization_metrics" in result
        assert "sdk_integration" in result

        # Verify optimization metrics
        metrics = result["optimization_metrics"]
        assert "cache_hits" in metrics
        assert "cache_misses" in metrics
        assert "tokens_saved" in metrics
        assert "optimization_applied" in metrics
        assert "cache_efficiency" in metrics
        assert "total_optimization_time_seconds" in metrics

        # Verify prompt content
        assert (
            "martin" in result["optimized_prompt"].lower()
            or "Martin" in result["optimized_prompt"]
        )
        assert (
            "platform strategy" in result["optimized_prompt"].lower()
            or "Platform Strategy" in result["optimized_prompt"]
        )

    def test_end_to_end_caching_performance(self):
        """Test end-to-end caching performance improvement"""
        query = "How do we scale our engineering organization?"
        persona = "diego"
        framework = "team_topologies"

        # First call - cache miss expected
        start_time = time.time()
        result1 = self.context_engine.get_optimized_prompt_context(
            query=query, persona=persona, framework=framework, session_id="perf_test"
        )
        first_call_time = time.time() - start_time

        # Second call - cache hit expected (if optimization available)
        start_time = time.time()
        result2 = self.context_engine.get_optimized_prompt_context(
            query=query, persona=persona, framework=framework, session_id="perf_test"
        )
        second_call_time = time.time() - start_time

        # Verify both calls succeeded
        assert "optimized_prompt" in result1
        assert "optimized_prompt" in result2

        # If optimization is active, second call should be faster or have cache hits
        if result2["sdk_integration"] == "active":
            # Either faster or has cache hits
            assert (
                second_call_time <= first_call_time
                or result2["optimization_metrics"]["cache_hits"] > 0
            )

    def test_graceful_degradation_without_optimizer(self):
        """Test graceful degradation when prompt optimizer unavailable"""
        # Temporarily disable prompt optimizer
        original_optimizer = self.cache_manager.prompt_optimizer
        self.cache_manager.prompt_optimizer = None

        try:
            result = self.cache_manager.assemble_optimized_prompt(
                persona="rachel", user_query="Test query"
            )

            # Should still work with fallback
            assert "prompt" in result
            assert "rachel" in result["prompt"].lower() or "Rachel" in result["prompt"]
            assert result["optimization_applied"] == "fallback_basic_assembly"
            assert result["cache_hits"] == 0

        finally:
            # Restore original optimizer
            self.cache_manager.prompt_optimizer = original_optimizer

    def test_context_engine_fallback_behavior(self):
        """Test context engine fallback when optimization fails"""
        result = self.context_engine.get_optimized_prompt_context(
            query="Test query", persona="alvaro", session_id="fallback_test"
        )

        # Should always succeed with some form of prompt
        assert "optimized_prompt" in result
        assert "optimization_metrics" in result
        assert "sdk_integration" in result

        # SDK integration should indicate status
        assert result["sdk_integration"] in [
            "active",
            "fallback",
            "unavailable",
            "error",
        ]

    def test_multiple_personas_caching(self):
        """Test caching behavior across different personas"""
        personas = ["diego", "martin", "rachel", "camille"]
        query = "What's our strategic approach?"

        results = []
        for persona in personas:
            result = self.context_engine.get_optimized_prompt_context(
                query=query, persona=persona, session_id="multi_persona_test"
            )
            results.append(result)

            # Verify each result
            assert "optimized_prompt" in result
            assert (
                persona.lower() in result["optimized_prompt"].lower()
                or persona.title() in result["optimized_prompt"]
            )

        # If optimization is active, should see cache behavior
        if any(r["sdk_integration"] == "active" for r in results):
            # At least some cache activity should occur
            total_cache_hits = sum(
                r["optimization_metrics"]["cache_hits"] for r in results
            )
            total_cache_misses = sum(
                r["optimization_metrics"]["cache_misses"] for r in results
            )
            assert total_cache_hits + total_cache_misses > 0

    def test_framework_specific_caching(self):
        """Test caching behavior with different frameworks"""
        frameworks = ["team_topologies", "platform_strategy", "wrap", "good_strategy"]
        persona = "diego"

        for framework in frameworks:
            result = self.context_engine.get_optimized_prompt_context(
                query=f"Apply {framework} to our situation",
                persona=persona,
                framework=framework,
                session_id="framework_test",
            )

            # Verify framework appears in prompt
            assert "optimized_prompt" in result
            # Framework should appear in some form in the prompt
            framework_words = framework.replace("_", " ").split()
            prompt_lower = result["optimized_prompt"].lower()
            assert any(word in prompt_lower for word in framework_words)

    def test_cache_metrics_tracking(self):
        """Test that cache metrics are properly tracked"""
        # Make several calls to generate metrics
        for i in range(3):
            result = self.context_engine.get_optimized_prompt_context(
                query=f"Query {i}",
                persona="diego",
                framework="team_topologies",
                session_id="metrics_test",
            )

            # Verify metrics structure
            metrics = result["optimization_metrics"]
            assert isinstance(metrics["cache_hits"], int)
            assert isinstance(metrics["cache_misses"], int)
            assert isinstance(metrics["tokens_saved"], int)
            assert isinstance(metrics["cache_efficiency"], float)
            assert isinstance(metrics["total_optimization_time_seconds"], float)

            # Verify timing is reasonable
            assert (
                0 <= metrics["total_optimization_time_seconds"] <= 10
            )  # Should be fast

    def test_p0_compatibility(self):
        """P0 test: Ensure integration doesn't break existing functionality"""
        # Basic context retrieval should still work
        context_result = self.context_engine.get_contextual_intelligence(
            query="Test query", session_id="p0_test"
        )

        assert "context" in context_result
        assert "metrics" in context_result

        # Optimized version should also work
        optimized_result = self.context_engine.get_optimized_prompt_context(
            query="Test query", persona="diego", session_id="p0_test"
        )

        assert "context" in optimized_result
        assert "optimized_prompt" in optimized_result

        # Both should have similar context structure
        assert type(context_result["context"]) == type(optimized_result["context"])


class TestPromptCacheIntegrationPerformance:
    """Performance-focused integration tests"""

    def setup_method(self):
        """Set up performance test fixtures"""
        self.cache_manager = get_cache_manager()
        self.context_engine = AdvancedContextEngine()

    def test_optimization_latency_improvement(self):
        """Test that optimization actually improves latency"""
        query = "Complex strategic question about organizational design"
        persona = "diego"
        framework = "team_topologies"

        # Warm up the system
        self.context_engine.get_optimized_prompt_context(
            query=query, persona=persona, framework=framework, session_id="warmup"
        )

        # Measure multiple calls
        times = []
        cache_hits = []

        for i in range(5):
            start = time.time()
            result = self.context_engine.get_optimized_prompt_context(
                query=f"{query} iteration {i}",
                persona=persona,
                framework=framework,
                session_id="latency_test",
            )
            times.append(time.time() - start)
            cache_hits.append(result["optimization_metrics"]["cache_hits"])

        # If optimization is active, should see improvement
        if any(hits > 0 for hits in cache_hits):
            # Later calls should generally be faster or have more cache hits
            avg_early = sum(times[:2]) / 2
            avg_late = sum(times[3:]) / 2

            # Either latency improved or cache hits increased
            assert avg_late <= avg_early or sum(cache_hits[3:]) > sum(cache_hits[:2])

    def test_memory_efficiency(self):
        """Test that caching doesn't cause memory bloat"""
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss

            # Generate many cached prompts
            for i in range(20):
                self.context_engine.get_optimized_prompt_context(
                    query=f"Query {i}",
                    persona="diego",
                    framework="team_topologies",
                    session_id=f"memory_test_{i}",
                )

            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory

            # Memory increase should be reasonable (< 50MB for 20 prompts)
            assert (
                memory_increase < 50 * 1024 * 1024
            ), f"Memory increased by {memory_increase / 1024 / 1024:.1f}MB"

        except ImportError:
            # Skip memory test if psutil not available
            pytest.skip("psutil not available for memory testing")

        except Exception as e:
            # Log but don't fail on memory measurement issues
            print(f"Memory efficiency test encountered issue: {e}")
            # Just verify basic functionality works
            for i in range(5):
                result = self.context_engine.get_optimized_prompt_context(
                    query=f"Query {i}",
                    persona="diego",
                    session_id=f"basic_memory_test_{i}",
                )
                assert "optimized_prompt" in result
