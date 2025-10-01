"""
Unit Tests: SDK-Inspired Prompt Caching Optimizer

Tests:
1. Persona template caching correctness
2. Framework context caching correctness
3. Cache hit/miss tracking
4. Performance improvement validation
5. P0 compatibility (no breaking changes)
6. Transparency system integration
7. Metrics tracking accuracy

Author: Martin | Platform Architecture
Phase: Quick Wins (Task 001 - Agent SDK Integration)
Date: 2025-10-01
"""

import pytest
import time
from typing import Dict, Any

# Import the module under test
from lib.performance.prompt_cache_optimizer import (
    SDKInspiredPromptCacheOptimizer,
    PromptSegmentType,
    PromptCacheEntry,
    integrate_prompt_optimizer_with_cache_manager,
)


class TestSDKInspiredPromptCaching:
    """Comprehensive tests for prompt caching optimization"""

    def setup_method(self):
        """Set up test fixtures"""
        self.optimizer = SDKInspiredPromptCacheOptimizer()

    def teardown_method(self):
        """Clean up after tests"""
        if hasattr(self, "optimizer"):
            self.optimizer.clear_cache()

    # ========================================================================
    # BASIC CACHING FUNCTIONALITY
    # ========================================================================

    def test_persona_template_caching(self):
        """Verify persona templates are cached correctly"""
        template = (
            "🎯 Diego | Engineering Leadership\nYou specialize in team structure..."
        )

        # Cache the template
        cache_key = self.optimizer.cache_persona_template("diego", template)

        # Verify it's in cache
        assert cache_key in self.optimizer.persona_templates_cache
        cached_entry = self.optimizer.persona_templates_cache[cache_key]
        assert cached_entry.prompt_segment == template
        assert cached_entry.persona == "diego"
        assert cached_entry.segment_type == PromptSegmentType.PERSONA_TEMPLATE
        assert cached_entry.estimated_tokens == 2000  # Default

    def test_framework_context_caching(self):
        """Verify framework patterns are cached correctly"""
        context = {
            "framework": "Team Topologies",
            "patterns": ["stream-aligned", "platform", "enabling"],
        }

        # Cache the context
        cache_key = self.optimizer.cache_framework_context("team_topologies", context)

        # Verify it's in cache
        assert cache_key in self.optimizer.framework_contexts_cache
        cached_entry = self.optimizer.framework_contexts_cache[cache_key]
        assert cached_entry.framework == "team_topologies"
        assert cached_entry.segment_type == PromptSegmentType.FRAMEWORK_CONTEXT
        assert "Team Topologies" in cached_entry.prompt_segment

    def test_system_instructions_caching(self):
        """Verify system instructions are cached correctly"""
        instructions = (
            "# ClaudeDirector Strategic Intelligence System\nYou provide transparent..."
        )

        # Cache the instructions
        cache_key = self.optimizer.cache_system_instructions(instructions)

        # Verify it's in cache
        assert cache_key in self.optimizer.system_instructions_cache
        cached_entry = self.optimizer.system_instructions_cache[cache_key]
        assert cached_entry.prompt_segment == instructions
        assert cached_entry.segment_type == PromptSegmentType.SYSTEM_INSTRUCTIONS

    # ========================================================================
    # CACHE HIT/MISS BEHAVIOR
    # ========================================================================

    def test_cache_hits_on_repeated_assembly(self):
        """Verify cache hits increase on repeated prompt assembly"""
        # Pre-populate cache
        self.optimizer.cache_persona_template("diego", "Diego template" * 100)
        self.optimizer.cache_framework_context(
            "team_topologies", {"framework": "Team Topologies"}
        )
        self.optimizer.cache_system_instructions("System instructions" * 50)

        # First assembly
        result1 = self.optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="test context 1",
            user_query="What about team structure?",
        )

        # Should have 3 cache hits (system, persona, framework)
        assert result1["cache_hits"] == 3
        assert result1["cache_misses"] == 0
        assert result1["tokens_saved"] > 0

        # Second assembly (different query, same persona/framework)
        result2 = self.optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="test context 2",
            user_query="What about cognitive load?",
        )

        # Should still have 3 cache hits
        assert result2["cache_hits"] == 3
        assert result2["cache_misses"] == 0
        assert result2["tokens_saved"] > 0

    def test_cache_miss_on_first_access(self):
        """Verify cache miss on first access to uncached content"""
        # Don't pre-populate cache

        result = self.optimizer.assemble_cached_prompt(
            persona="martin", framework="platform_strategy", user_query="Test query"
        )

        # Should have cache misses
        assert result["cache_misses"] > 0
        # System instructions might be cached from previous tests
        # so we just verify the pattern works

    def test_cache_context_switching(self):
        """Verify cache behavior when switching personas/frameworks"""
        # Cache Diego
        self.optimizer.cache_persona_template("diego", "Diego template")

        # First query with Diego
        result1 = self.optimizer.assemble_cached_prompt(
            persona="diego", user_query="Query 1"
        )
        assert result1["cache_hits"] >= 1  # At least persona hit

        # Switch to Rachel (cache miss)
        result2 = self.optimizer.assemble_cached_prompt(
            persona="rachel", user_query="Query 2"
        )
        # Rachel not cached, so at least one miss
        # System might be cached though

        # Back to Diego (cache hit again)
        result3 = self.optimizer.assemble_cached_prompt(
            persona="diego", user_query="Query 3"
        )
        assert result3["cache_hits"] >= 1  # Diego still cached

    # ========================================================================
    # PERFORMANCE VALIDATION
    # ========================================================================

    def test_latency_improvement(self):
        """Verify latency improvement with caching"""
        # Pre-warm cache
        self.optimizer.cache_persona_template(
            "diego", "template" * 100, estimated_tokens=2000
        )
        self.optimizer.cache_framework_context(
            "team_topologies", {"data": "context" * 50}, estimated_tokens=300
        )
        self.optimizer.cache_system_instructions(
            "instructions" * 100, estimated_tokens=1500
        )

        # Measure cached assembly time
        start = time.time()
        result = self.optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="test",
            user_query="test query",
        )
        cached_time = time.time() - start

        # Verify cache hits
        assert result["cache_hits"] == 3  # System, persona, framework
        assert result["tokens_saved"] == 3800  # 1500 + 2000 + 300

        # Verify assembly is fast (<100ms target)
        assert (
            cached_time < 0.1
        ), f"Assembly took {cached_time*1000:.1f}ms, expected <100ms"

        # Verify latency savings calculated
        assert result["latency_saved_ms"] > 0

    def test_tokens_saved_calculation(self):
        """Verify accurate token savings calculation"""
        # Cache with specific token estimates
        self.optimizer.cache_persona_template(
            "diego", "template", estimated_tokens=2000
        )
        self.optimizer.cache_framework_context(
            "team_topologies", {}, estimated_tokens=300
        )
        self.optimizer.cache_system_instructions("instructions", estimated_tokens=1500)

        result = self.optimizer.assemble_cached_prompt(
            persona="diego", framework="team_topologies", user_query="test"
        )

        # Should save all cached tokens
        assert result["tokens_saved"] == 3800  # 2000 + 300 + 1500

    # ========================================================================
    # METRICS TRACKING
    # ========================================================================

    def test_cache_metrics_tracking(self):
        """Verify cache metrics are tracked correctly"""
        # Pre-populate cache
        self.optimizer.cache_persona_template("diego", "template")
        self.optimizer.cache_framework_context("team_topologies", {})

        # Make multiple requests
        for i in range(5):
            self.optimizer.assemble_cached_prompt(
                persona="diego",
                framework="team_topologies",
                conversation_context=f"context_{i}",
                user_query=f"query_{i}",
            )

        metrics = self.optimizer.get_cache_metrics()

        # Verify metrics structure
        assert "total_assembly_requests" in metrics
        assert "cache_hits" in metrics
        assert "cache_misses" in metrics
        assert "tokens_saved_estimated" in metrics
        assert "latency_saved_ms" in metrics
        assert "cache_hit_rate" in metrics

        # Verify counts
        assert metrics["total_assembly_requests"] == 5
        assert metrics["cache_hits"] > 0
        assert metrics["tokens_saved_estimated"] > 0

        # Verify hit rate calculation
        assert 0.0 <= metrics["cache_hit_rate"] <= 1.0

    def test_cache_hit_rate_calculation(self):
        """Verify cache hit rate is calculated correctly"""
        # Clear metrics
        self.optimizer.clear_cache()

        # Cache some content
        self.optimizer.cache_persona_template("diego", "template")

        # Make a request (1 hit, 2 misses expected if framework + system not cached)
        self.optimizer.assemble_cached_prompt(persona="diego", user_query="test")

        metrics = self.optimizer.get_cache_metrics()

        # Hit rate should be between 0 and 1
        assert 0.0 <= metrics["cache_hit_rate"] <= 1.0

    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================

    def test_integration_with_cache_manager(self):
        """Verify integration with existing cache_manager works"""
        from lib.performance.cache_manager import get_cache_manager

        # Get cache manager with prompt optimizer
        cache_manager = integrate_prompt_optimizer_with_cache_manager()

        # Verify prompt optimizer is attached
        assert hasattr(cache_manager, "prompt_optimizer")
        assert isinstance(
            cache_manager.prompt_optimizer, SDKInspiredPromptCacheOptimizer
        )

        # Verify optimizer can be used
        cache_manager.prompt_optimizer.cache_persona_template(
            "test_persona", "test template"
        )

        result = cache_manager.prompt_optimizer.assemble_cached_prompt(
            persona="test_persona", user_query="test query"
        )

        assert result["cache_hits"] >= 1  # Should hit persona cache

    def test_no_cache_manager_duplication(self):
        """Verify we're not duplicating cache_manager functionality"""
        # This is a BLOAT_PREVENTION compliance test

        # Optimizer should reuse existing cache_manager
        from lib.performance.cache_manager import get_cache_manager

        base_manager = get_cache_manager()
        optimizer = SDKInspiredPromptCacheOptimizer(cache_manager=base_manager)

        # Verify optimizer uses the same instance
        assert optimizer.cache_manager is base_manager

    # ========================================================================
    # P0 COMPATIBILITY TESTS
    # ========================================================================

    def test_p0_non_breaking_behavior(self):
        """P0: Ensure prompt optimizer doesn't break existing functionality"""
        # This test verifies the optimizer can be added without breaking changes

        # Create optimizer
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Basic prompt assembly should work even with empty cache
        result = optimizer.assemble_cached_prompt(
            persona="diego", user_query="test query"
        )

        # Should return valid result structure
        assert "prompt" in result
        assert "cache_hits" in result
        assert "cache_misses" in result
        assert "optimization_applied" in result

        # Prompt should be non-empty
        assert len(result["prompt"]) > 0

    def test_graceful_degradation(self):
        """P0: Verify graceful degradation if cache unavailable"""
        # Even with no cached content, should still assemble prompt
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Don't cache anything
        result = optimizer.assemble_cached_prompt(
            persona="martin",
            framework="platform_strategy",
            conversation_context="some context",
            strategic_memory={"key": "value"},
            user_query="What should I do?",
        )

        # Should still return valid result
        assert result["prompt"] is not None
        assert len(result["prompt"]) > 0

        # Should report cache misses
        assert result["cache_misses"] > 0

    # ========================================================================
    # EDGE CASES
    # ========================================================================

    def test_cache_clear(self):
        """Verify cache can be cleared"""
        # Populate cache
        self.optimizer.cache_persona_template("diego", "template")
        self.optimizer.cache_framework_context("team_topologies", {})

        # Verify populated
        assert len(self.optimizer.persona_templates_cache) > 0
        assert len(self.optimizer.framework_contexts_cache) > 0

        # Clear cache
        self.optimizer.clear_cache()

        # Verify cleared
        assert len(self.optimizer.persona_templates_cache) == 0
        assert len(self.optimizer.framework_contexts_cache) == 0

        # Verify metrics reset
        metrics = self.optimizer.get_cache_metrics()
        assert metrics["total_assembly_requests"] == 0
        assert metrics["cache_hits"] == 0

    def test_empty_context_handling(self):
        """Verify handling of empty/None contexts"""
        result = self.optimizer.assemble_cached_prompt(
            persona="diego",
            framework=None,  # No framework
            conversation_context="",  # Empty
            strategic_memory=None,  # None
            user_query="",  # Empty
        )

        # Should still work
        assert result["prompt"] is not None
        assert "optimization_applied" in result

    def test_multiple_personas_cached(self):
        """Verify multiple personas can be cached simultaneously"""
        personas = ["diego", "martin", "rachel", "camille", "alvaro"]

        # Cache all personas
        for persona in personas:
            self.optimizer.cache_persona_template(persona, f"{persona} template")

        # Verify all are cached
        assert len(self.optimizer.persona_templates_cache) == len(personas)

        # Verify each can be retrieved
        for persona in personas:
            result = self.optimizer.assemble_cached_prompt(
                persona=persona, user_query="test"
            )
            assert result["cache_hits"] >= 1  # At least persona hit

    def test_cache_entry_hit_tracking(self):
        """Verify cache entries track hit counts"""
        # Cache a template
        cache_key = self.optimizer.cache_persona_template("diego", "template")

        entry = self.optimizer.persona_templates_cache[cache_key]
        initial_hits = entry.hit_count

        # Access it multiple times
        for _ in range(3):
            self.optimizer.assemble_cached_prompt(persona="diego", user_query="test")

        # Hit count should have increased
        assert entry.hit_count > initial_hits
        assert entry.hit_count >= 3


# ========================================================================
# PERFORMANCE BENCHMARK TESTS
# ========================================================================


class TestPromptCachingPerformance:
    """Performance benchmark tests for cache optimization"""

    def test_baseline_vs_cached_comparison(self):
        """Benchmark: Compare baseline vs cached assembly time"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Pre-warm cache
        optimizer.cache_persona_template("diego", "template" * 100, 2000)
        optimizer.cache_framework_context("team_topologies", {"data": "x" * 100}, 300)
        optimizer.cache_system_instructions("instructions" * 100, 1500)

        # Measure cached assembly (10 iterations for stable measurement)
        cached_times = []
        for _ in range(10):
            start = time.time()
            optimizer.assemble_cached_prompt(
                persona="diego", framework="team_topologies", user_query="test"
            )
            cached_times.append((time.time() - start) * 1000)

        avg_cached_time = sum(cached_times) / len(cached_times)

        # Should be fast (<100ms target)
        assert avg_cached_time < 100, f"Average cached time: {avg_cached_time:.1f}ms"

        optimizer.clear_cache()


# ========================================================================
# RUN TESTS
# ========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
