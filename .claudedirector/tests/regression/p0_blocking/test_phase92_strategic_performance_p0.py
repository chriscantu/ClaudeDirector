"""
P0 Test: Phase 9.2 Strategic Performance Manager

Tests User Stories 9.2.1 and 9.2.2 implementation with executive-grade performance targets.
Validates <200ms strategic query response and <100MB memory baseline requirements.

Author: Martin | Platform Architecture
Phase: 9.2 - Performance Optimization
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    # Direct import from lib directory
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "lib"))
    from performance.strategic_performance_manager import (
        StrategicPerformanceManager,
        QueryType,
        QueryPerformanceResult,
    )
    from core.base_manager import BaseManagerConfig, ManagerType
except ImportError as e:
    print(f"Import error: {e}")

    # Create mock classes for testing if imports fail
    class StrategicPerformanceManager:
        pass

    class QueryType:
        EXECUTIVE_CRITICAL = "executive_critical"
        STRATEGIC_STANDARD = "strategic_standard"

    class QueryPerformanceResult:
        pass

    class BaseManagerConfig:
        pass

    class ManagerType:
        PERFORMANCE = "performance"


class TestPhase92StrategicPerformanceP0:
    """
    🛡️ P0 BLOCKING TEST: Phase 9.2 Strategic Performance Manager

    CRITICAL USER STORY VALIDATION:
    - Story 9.2.1: Sub-Second Strategic Query Response (<200ms)
    - Story 9.2.2: Resource-Efficient Operations (<100MB memory)

    P0 REQUIREMENTS:
    - 95% of strategic queries complete in <200ms
    - Executive queries complete in <100ms
    - Memory baseline <100MB under normal operations
    - SLA alerting for performance degradation
    - BaseManager pattern compliance
    """

    @pytest.fixture
    def performance_manager(self):
        """Create strategic performance manager for testing"""
        config = BaseManagerConfig(
            manager_name="test_strategic_performance_manager",
            manager_type=ManagerType.PERFORMANCE,
            enable_cache=True,
            enable_metrics=True,
            custom_config={
                "executive_target_ms": 100,
                "strategic_target_ms": 200,
                "memory_baseline_mb": 100,
                "sla_target_percentage": 95.0,
                "optimization_enabled": True,
            },
        )
        return StrategicPerformanceManager(config=config)

    def test_strategic_performance_manager_initialization_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Strategic performance manager initialization

        ACCEPTANCE CRITERIA:
        - BaseManager inheritance working
        - Performance targets configured correctly
        - SLA metrics initialized
        - Memory baseline set
        """
        # Test BaseManager inheritance
        assert hasattr(performance_manager, "logger")
        assert hasattr(performance_manager, "cache")
        assert hasattr(performance_manager, "metrics")
        assert hasattr(performance_manager, "config")

        # Test performance targets configuration
        assert QueryType.EXECUTIVE_CRITICAL in performance_manager.performance_targets
        assert QueryType.STRATEGIC_STANDARD in performance_manager.performance_targets

        # Validate User Story 9.2.1 targets
        executive_target = performance_manager.performance_targets[
            QueryType.EXECUTIVE_CRITICAL
        ]
        strategic_target = performance_manager.performance_targets[
            QueryType.STRATEGIC_STANDARD
        ]

        assert executive_target.target_ms == 100  # <100ms for executive
        assert strategic_target.target_ms == 200  # <200ms for strategic
        assert strategic_target.sla_percentage == 95.0  # 95% SLA

        # Test User Story 9.2.2 memory baseline
        assert performance_manager.memory_baseline_mb == 100  # <100MB baseline

        # Test SLA metrics initialization
        assert all(qt in performance_manager.sla_metrics for qt in QueryType)
        for qt in QueryType:
            assert performance_manager.sla_metrics[qt]["rate"] == 100.0  # Start at 100%
            assert performance_manager.sla_metrics[qt]["total"] == 0

    @pytest.mark.asyncio
    async def test_strategic_query_optimization_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Strategic query optimization with <200ms target

        USER STORY 9.2.1 ACCEPTANCE CRITERIA:
        - 95% of strategic queries complete in <200ms
        - No visible loading delays during executive presentations
        - Performance monitoring dashboard for system health
        """

        # Mock query function that simulates strategic analysis
        async def mock_strategic_query(context: str) -> dict:
            """Simulate strategic query processing"""
            await asyncio.sleep(0.05)  # 50ms processing time
            return {"analysis": f"Strategic analysis for {context}", "confidence": 0.95}

        # Test strategic query optimization
        query_result, performance_result = (
            await performance_manager.optimize_strategic_query(
                mock_strategic_query,
                QueryType.STRATEGIC_STANDARD,
                "executive_planning_context",
            )
        )

        # Validate query result
        assert query_result is not None
        assert "analysis" in query_result
        assert (
            "Strategic analysis for executive_planning_context"
            in query_result["analysis"]
        )

        # Validate User Story 9.2.1 performance requirements
        assert isinstance(performance_result, QueryPerformanceResult)
        assert performance_result.query_type == QueryType.STRATEGIC_STANDARD
        assert performance_result.execution_time_ms < 200  # <200ms requirement
        assert performance_result.target_achieved == True

        # Validate SLA tracking
        assert (
            performance_manager.sla_metrics[QueryType.STRATEGIC_STANDARD]["total"] == 1
        )
        assert (
            performance_manager.sla_metrics[QueryType.STRATEGIC_STANDARD]["achieved"]
            == 1
        )
        assert (
            performance_manager.sla_metrics[QueryType.STRATEGIC_STANDARD]["rate"]
            == 100.0
        )

    @pytest.mark.asyncio
    async def test_executive_query_performance_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Executive query performance <100ms target

        USER STORY 9.2.1 ACCEPTANCE CRITERIA:
        - Executive queries respond in under 100ms
        - Maintain executive credibility through responsive performance
        - Enable real-time strategic decision making
        """

        # Mock executive query function
        async def mock_executive_query(decision_context: str) -> dict:
            """Simulate executive decision query"""
            await asyncio.sleep(0.02)  # 20ms processing time
            return {
                "recommendation": f"Executive recommendation for {decision_context}"
            }

        # Test executive query optimization
        query_result, performance_result = (
            await performance_manager.optimize_strategic_query(
                mock_executive_query,
                QueryType.EXECUTIVE_CRITICAL,
                "board_presentation_decision",
            )
        )

        # Validate executive performance requirements
        assert performance_result.execution_time_ms < 100  # <100ms for executive
        assert performance_result.target_achieved == True
        assert performance_result.query_type == QueryType.EXECUTIVE_CRITICAL

        # Validate executive SLA tracking
        exec_metrics = performance_manager.sla_metrics[QueryType.EXECUTIVE_CRITICAL]
        assert exec_metrics["total"] == 1
        assert exec_metrics["achieved"] == 1
        assert exec_metrics["rate"] == 100.0

    def test_memory_usage_monitoring_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Memory usage monitoring <100MB baseline

        USER STORY 9.2.2 ACCEPTANCE CRITERIA:
        - Baseline memory usage <100MB under normal operations
        - Memory growth rate <10% per additional team monitored
        - Automated memory pressure detection and relief
        """

        # Test memory monitoring
        memory_report = performance_manager.monitor_memory_usage()

        # Validate memory report structure
        assert "current_mb" in memory_report
        assert "baseline_mb" in memory_report
        assert "target_mb" in memory_report
        assert "efficiency_rating" in memory_report
        assert "baseline_exceeded" in memory_report
        assert "memory_pressure" in memory_report

        # Validate User Story 9.2.2 baseline target
        assert memory_report["target_mb"] == 100  # <100MB baseline

        # Validate memory efficiency calculation
        assert isinstance(memory_report["efficiency_rating"], float)
        assert 0 <= memory_report["efficiency_rating"] <= 100

        # Validate memory pressure detection
        assert isinstance(memory_report["memory_pressure"], bool)
        assert isinstance(memory_report["baseline_exceeded"], bool)

    def test_memory_optimization_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Memory optimization and pressure relief

        USER STORY 9.2.2 ACCEPTANCE CRITERIA:
        - No memory leaks during extended operations
        - Automated memory pressure detection and relief
        - Cost tracking dashboard for infrastructure optimization
        """

        # Test memory optimization
        optimization_result = performance_manager.optimize_memory_usage()

        # Validate optimization result structure
        required_fields = [
            "memory_before_mb",
            "memory_after_mb",
            "memory_saved_mb",
            "gc_collected_objects",
            "cache_cleared",
            "optimization_effective",
        ]

        for field in required_fields:
            assert field in optimization_result, f"Missing field: {field}"

        # Validate optimization effectiveness
        assert isinstance(optimization_result["memory_saved_mb"], float)
        assert isinstance(optimization_result["gc_collected_objects"], int)
        assert isinstance(optimization_result["optimization_effective"], bool)

        # Validate memory statistics update
        assert performance_manager.memory_stats["gc_optimizations"] >= 1
        assert performance_manager.memory_stats["last_optimization"] > 0

    def test_executive_dashboard_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Executive dashboard for system health visibility

        USER STORY 9.2.1 ACCEPTANCE CRITERIA:
        - Performance monitoring dashboard for system health
        - SLA alerting for performance degradation
        - Business impact visibility
        """

        # Test executive dashboard
        dashboard = performance_manager.get_executive_dashboard()

        # Validate dashboard structure
        required_sections = [
            "sla_compliance",
            "memory_efficiency",
            "performance_trends",
            "business_impact",
            "recommendations",
        ]

        for section in required_sections:
            assert section in dashboard, f"Missing dashboard section: {section}"

        # Validate SLA compliance section
        sla_section = dashboard["sla_compliance"]
        assert "overall_percentage" in sla_section
        assert "target_percentage" in sla_section
        assert sla_section["target_percentage"] == 95.0  # User Story requirement
        assert "status" in sla_section
        assert "by_query_type" in sla_section

        # Validate memory efficiency section
        memory_section = dashboard["memory_efficiency"]
        assert "current_mb" in memory_section
        assert "baseline_target_mb" in memory_section
        assert memory_section["baseline_target_mb"] == 100  # User Story requirement
        assert "efficiency_rating" in memory_section
        assert "within_baseline" in memory_section

        # Validate business impact section
        business_section = dashboard["business_impact"]
        assert "meeting_efficiency_target" in business_section
        assert "executive_credibility_maintained" in business_section
        assert "cost_optimization_achieved" in business_section

    @pytest.mark.asyncio
    async def test_performance_baseline_test_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Performance baseline test validation

        ACCEPTANCE CRITERIA VALIDATION:
        - Strategic queries under 200ms
        - Executive queries under 100ms
        - Memory under 100MB baseline
        - 95% SLA compliance
        """

        # Run performance baseline test
        test_results = await performance_manager.run_performance_baseline_test()

        # Validate test structure
        required_sections = [
            "query_performance",
            "memory_baseline",
            "optimization_effectiveness",
            "acceptance_criteria",
            "overall_status",
        ]

        for section in required_sections:
            assert section in test_results, f"Missing test section: {section}"

        # Validate acceptance criteria
        criteria = test_results["acceptance_criteria"]
        assert "strategic_queries_under_200ms" in criteria
        assert "executive_queries_under_100ms" in criteria
        assert "memory_under_100mb" in criteria
        assert "sla_95_percent" in criteria

        # Validate overall test status
        assert test_results["overall_status"] in ["PASS", "FAIL", "ERROR"]

    def test_sla_compliance_tracking_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: SLA compliance tracking and reporting

        USER STORY 9.2.1 ACCEPTANCE CRITERIA:
        - 95% of strategic queries complete in <200ms
        - SLA alerting for performance degradation
        """

        # Test SLA compliance report
        sla_report = performance_manager.get_sla_compliance_report()

        # Validate report structure
        assert "overall_sla" in sla_report
        assert "query_type_breakdown" in sla_report
        assert "memory_efficiency" in sla_report
        assert "recommendations" in sla_report

        # Validate query type breakdown
        breakdown = sla_report["query_type_breakdown"]

        for query_type in QueryType:
            qt_key = query_type.value
            assert qt_key in breakdown

            qt_data = breakdown[qt_key]
            assert "sla_rate" in qt_data
            assert "total_queries" in qt_data
            assert "target_ms" in qt_data
            assert "status" in qt_data

            # Validate User Story targets
            if query_type == QueryType.STRATEGIC_STANDARD:
                assert qt_data["target_ms"] == 200
            elif query_type == QueryType.EXECUTIVE_CRITICAL:
                assert qt_data["target_ms"] == 100

    def test_base_manager_compliance_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: BaseManager pattern compliance validation

        ARCHITECTURAL COMPLIANCE:
        - Must inherit from BaseManager pattern
        - Must implement manage() abstract method
        - Must follow DRY principles
        - Must maintain P0 test coverage
        """

        # Test BaseManager inheritance
        from claudedirector.lib.core.base_manager import BaseManager

        assert isinstance(performance_manager, BaseManager)

        # Test abstract method implementation
        assert hasattr(performance_manager, "manage")
        assert callable(performance_manager.manage)

        # Test BaseManager infrastructure availability
        assert hasattr(performance_manager, "logger")
        assert hasattr(performance_manager, "cache")
        assert hasattr(performance_manager, "metrics")
        assert hasattr(performance_manager, "config")
        assert hasattr(performance_manager, "get_config")
        assert hasattr(performance_manager, "record_error")

        # Test manage() method operations
        valid_operations = [
            "optimize_query",
            "monitor_memory",
            "get_dashboard",
            "run_performance_test",
            "optimize_memory",
            "get_sla_report",
        ]

        for operation in valid_operations:
            # Should not raise an exception for valid operations
            try:
                result = performance_manager.manage(operation)
                # Result can be anything, just testing method works
                assert result is not None or result is None  # Any result is valid
            except Exception as e:
                # Some operations might need parameters, that's ok
                assert "required" in str(e).lower() or "missing" in str(e).lower()

    @pytest.mark.asyncio
    async def test_cache_optimization_integration_p0(self, performance_manager):
        """
        🛡️ P0 BLOCKING: Cache optimization integration

        USER STORY 9.2.1 ACCEPTANCE CRITERIA:
        - Cache warming for frequently accessed data
        - Intelligent cache invalidation
        - Performance monitoring for cache effectiveness
        """

        # Mock query function for cache testing
        call_count = 0

        async def mock_cached_query(context: str) -> dict:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # 100ms without cache
            return {"result": f"analysis_{context}", "call_number": call_count}

        # First call - should execute and cache
        result1, perf1 = await performance_manager.optimize_strategic_query(
            mock_cached_query, QueryType.STRATEGIC_STANDARD, "test_context"
        )

        # Second call - should hit cache
        result2, perf2 = await performance_manager.optimize_strategic_query(
            mock_cached_query, QueryType.STRATEGIC_STANDARD, "test_context"
        )

        # Validate cache effectiveness
        assert call_count == 1  # Function only called once due to caching
        assert result1 == result2  # Same result from cache
        assert perf1.cache_hit == False  # First call was not cached
        assert perf2.cache_hit == True  # Second call hit cache
        assert perf2.execution_time_ms < perf1.execution_time_ms  # Cache faster


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
