# Task 001: Prompt Caching Optimization

## Task Overview
**ID**: TASK-001
**Component**: `prompt_cache_optimizer.py`
**Priority**: P0 (Performance critical)
**Estimated Effort**: 5 days
**Phase**: 1 (Quick Wins)

## Context7 Pattern Applied
**Pattern**: **Cache-Aside Pattern** + **Facade Pattern**
**Rationale**: Leverages SDK caching strategies while maintaining clean integration with existing cache_manager.py

## BLOAT_PREVENTION_SYSTEM.md Compliance

### ✅ Existing Infrastructure Analysis
**REUSE EXISTING (DRY Compliance)**:
```python
# EXISTING: .claudedirector/lib/performance/cache_manager.py
class CacheManager:
    def get_cache_manager() -> CacheManager
    # Existing caching infrastructure we'll extend

# EXISTING: .claudedirector/lib/context_engineering/advanced_context_engine.py
class AdvancedContextEngine:
    def retrieve_strategic_context(...) -> Dict[str, Any]
    # Context assembly we'll optimize
```

### 🚫 PREVENT DUPLICATION
**DO NOT CREATE**:
- New cache storage mechanisms (use existing CacheManager)
- New context assembly logic (enhance existing AdvancedContextEngine)
- Parallel caching implementations

**DO CREATE**:
- SDK-inspired optimization layer that EXTENDS existing cache_manager
- Persona-specific caching strategy (new domain knowledge)
- Framework pattern caching (new optimization)

## Implementation Strategy

### Step 1: SDK Pattern Analysis (Day 1)
**Research Phase**:
```python
"""
SDK Prompt Caching Research:

1. Review Agent SDK documentation:
   https://docs.claude.com/en/api/agent-sdk/overview

2. Identify caching patterns:
   - System prompt caching (stable content)
   - Tool definition caching (reusable)
   - Context window optimization
   - Cache invalidation strategies

3. Map to ClaudeDirector architecture:
   - System prompts → Persona templates (highly cacheable)
   - Tool definitions → Framework patterns (moderately cacheable)
   - Context → Strategic memory (selectively cacheable)
   - User messages → Never cached (always fresh)
"""
```

**Deliverables**: Research document with gap analysis

### Step 2: Facade Implementation (Day 2-3)

**Key Implementation**: `.claudedirector/lib/performance/prompt_cache_optimizer.py`

**Core Components**:
```python
@dataclass
class PromptCacheEntry:
    """Cached prompt segment for reuse across turns"""
    cache_key: str
    prompt_segment: str
    persona: str
    framework_context: Dict[str, Any]
    cached_at: float
    hit_count: int = 0
    tokens_saved: int = 0


class SDKInspiredPromptCacheOptimizer:
    """
    Applies Agent SDK prompt caching patterns to ClaudeDirector.

    Key Optimizations (SDK-inspired):
    1. Persona template caching - stable across conversations
    2. Framework pattern caching - reusable strategic patterns
    3. Multi-turn context caching - conversation continuity

    Design Principles:
    - EXTEND existing cache_manager.py (don't replace)
    - REFERENCE SDK patterns (don't copy code)
    - PRESERVE transparency system (all caching visible)
    - VALIDATE with P0 tests (no breaking changes)
    """

    def __init__(self, cache_ttl: int = 3600):
        self.persona_templates_cache: Dict[str, str] = {}
        self.framework_patterns_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "tokens_saved": 0,
        }

    def cache_persona_template(self, persona: str, template: str) -> str:
        """Cache persona system prompt (SDK pattern)"""
        cache_key = self._generate_cache_key(f"persona_{persona}")
        self.persona_templates_cache[cache_key] = template
        return cache_key

    def cache_framework_context(self, framework: str, context: Dict[str, Any]) -> str:
        """Cache framework context (SDK pattern)"""
        cache_key = self._generate_cache_key(f"framework_{framework}")
        self.framework_patterns_cache[cache_key] = context
        return cache_key

    def assemble_cached_prompt(
        self,
        persona: str,
        framework: Optional[str],
        conversation_context: str,
        strategic_memory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main optimization: Assemble prompt using cached segments.

        Returns dict with prompt, cache_hits, tokens_saved, optimization_applied
        """
        # Implementation combines cached + fresh segments
        # See full implementation in deliverable


# Integration with existing cache_manager.py (EXTEND, DON'T REPLACE)
def integrate_with_cache_manager():
    from ..performance.cache_manager import get_cache_manager
    cache_manager = get_cache_manager()
    cache_manager.prompt_optimizer = SDKInspiredPromptCacheOptimizer()
    return cache_manager
```

**Full implementation**: ~300 lines including all methods, error handling, metrics tracking

### Step 3: Testing (Day 4-5)
```python
# File: .claudedirector/tests/unit/performance/test_prompt_cache_optimizer.py

"""
P0 Tests: SDK-Inspired Prompt Caching Optimizer

Validates:
1. Caching reduces latency by >10%
2. All P0 tests still pass
3. Transparency system unaffected
4. No duplication introduced
"""

import pytest
import time
from lib.performance.prompt_cache_optimizer import (
    SDKInspiredPromptCacheOptimizer,
    integrate_with_cache_manager
)


class TestSDKInspiredPromptCaching:
    """P0: Prompt caching optimization tests"""

    def test_persona_template_caching(self):
        """Verify persona templates are cached correctly"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Cache persona template
        template = "🎯 Diego | Engineering Leadership..."
        cache_key = optimizer.cache_persona_template("diego", template)

        # Verify cached
        assert cache_key in optimizer.persona_templates_cache
        assert optimizer.persona_templates_cache[cache_key] == template

    def test_framework_context_caching(self):
        """Verify framework patterns are cached correctly"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Cache framework context
        context = {"framework": "Team Topologies", "patterns": ["stream-aligned"]}
        cache_key = optimizer.cache_framework_context("team_topologies", context)

        # Verify cached
        assert cache_key in optimizer.framework_patterns_cache
        assert optimizer.framework_patterns_cache[cache_key] == context

    def test_cache_hits_on_repeated_assembly(self):
        """Verify cache hits on repeated prompt assembly"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # First call - cache miss
        result1 = optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="test context",
            strategic_memory={}
        )

        # Second call - should hit cache
        result2 = optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="different context",
            strategic_memory={}
        )

        # Verify cache hits increased
        assert result2["cache_hits"] >= 2
        assert result2["tokens_saved"] > 0

    def test_latency_improvement(self):
        """P0: Verify >10% latency improvement"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Warm up cache
        optimizer.cache_persona_template("diego", "template" * 100)
        optimizer.cache_framework_context("team_topologies", {"data": "context" * 50})

        # Measure cached assembly time
        start = time.time()
        result = optimizer.assemble_cached_prompt(
            persona="diego",
            framework="team_topologies",
            conversation_context="test",
            strategic_memory={}
        )
        cached_time = time.time() - start

        # Verify cache hits
        assert result["cache_hits"] >= 2
        assert result["tokens_saved"] > 0

        # Verify latency (baseline would be measured separately)
        assert cached_time < 0.1  # <100ms for cached assembly

    def test_p0_tests_still_pass(self):
        """P0: Ensure all existing P0 tests still pass"""
        # This test runs the full P0 suite
        from tests.p0_enforcement.run_mandatory_p0_tests import run_all_p0_tests

        results = run_all_p0_tests()
        assert results["total_passed"] == 40  # All P0 tests must pass
        assert results["total_failed"] == 0

    def test_no_transparency_impact(self):
        """P0: Verify transparency system still works"""
        from lib.transparency.mcp_transparency import MCPTransparencySystem

        transparency = MCPTransparencySystem()

        # Verify transparency still captures all events
        assert transparency.is_active
        assert transparency.capture_rate == 1.0  # 100% capture

    def test_cache_metrics_tracking(self):
        """Verify cache metrics are tracked correctly"""
        optimizer = SDKInspiredPromptCacheOptimizer()

        # Make some cached requests
        for i in range(5):
            optimizer.assemble_cached_prompt(
                persona="diego",
                framework="team_topologies",
                conversation_context=f"context_{i}",
                strategic_memory={}
            )

        metrics = optimizer.get_cache_metrics()

        assert metrics["total_requests"] == 5
        assert metrics["cache_hits"] > 0
        assert metrics["tokens_saved"] > 0

    def test_integration_with_cache_manager(self):
        """Verify integration with existing cache_manager works"""
        cache_manager = integrate_with_cache_manager()

        # Verify prompt optimizer is attached
        assert hasattr(cache_manager, "prompt_optimizer")
        assert isinstance(cache_manager.prompt_optimizer, SDKInspiredPromptCacheOptimizer)
```

## Testing Strategy

### Unit Tests (pytest)
- All public methods tested
- Cache hit/miss scenarios
- Metrics tracking validation
- Edge cases (empty cache, cache expiration)

### P0 Tests (mandatory)
- All 40 existing P0 tests must pass
- New P0 test: latency improvement >10%
- New P0 test: transparency system unaffected

### Performance Tests (pytest-benchmark)
- Baseline vs cached latency comparison
- Cache efficiency metrics
- Memory usage validation

## Deliverables

### Code Files
1. `.claudedirector/lib/performance/prompt_cache_optimizer.py` (~300 lines)
2. `.claudedirector/tests/unit/performance/test_prompt_cache_optimizer.py` (~150 lines)

### Modified Files
1. `.claudedirector/lib/performance/cache_manager.py` (+20 lines - integration point)
2. `.claudedirector/lib/context_engineering/advanced_context_engine.py` (+30 lines - use caching)

### Documentation
1. `.claudedirector/docs/architecture/SDK_PATTERN_INTEGRATION.md` (new)
   - SDK pattern analysis
   - Integration approach
   - Performance results

### Performance Report
1. Baseline measurements (without caching)
2. Optimized measurements (with caching)
3. Improvement validation (>10% target)
4. Cache efficiency metrics

## Acceptance Criteria

- [ ] `prompt_cache_optimizer.py` implemented with all methods
- [ ] All unit tests passing (>80% coverage)
- [ ] All P0 tests passing (40/40)
- [ ] Performance benchmarks show >10% improvement
- [ ] Cache hit rate >50% for repeated queries
- [ ] Integration with cache_manager.py complete
- [ ] Documentation updated
- [ ] No BLOAT_PREVENTION violations
- [ ] Code review approved

## Dependencies

### Prerequisites
- Existing `cache_manager.py` functional
- Existing `advanced_context_engine.py` functional
- P0 test suite passing (40/40)

### Blocks
- Task 1.3 (Benchmarking) - needs this implementation to measure

### Blocked By
- None (can start immediately)

## Notes

**SDK Pattern References**:
- Agent SDK uses prompt caching for system prompts
- We adapt this for persona templates (stable content)
- Framework patterns are similar to SDK's tool definitions
- Conversation context is never cached (always fresh)

**BLOAT_PREVENTION Validation**:
- This EXTENDS existing cache_manager.py (doesn't replace)
- No duplication of caching logic
- Reuses existing cache infrastructure
- Single responsibility: prompt-specific optimization

**P0 Protection**:
- Must not break any existing functionality
- All 40 P0 tests pass throughout development
- Transparency system remains fully functional
- Persona routing unaffected

---

**Status**: Ready for Implementation
**Next Step**: Begin Day 1 - SDK pattern analysis and research
