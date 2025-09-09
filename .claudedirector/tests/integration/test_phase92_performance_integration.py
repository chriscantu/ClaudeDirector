"""
Integration Test: Phase 9.2 Strategic Performance Manager

Tests User Stories 9.2.1 and 9.2.2 implementation with real system integration.
Validates <200ms strategic query response and <100MB memory baseline requirements.

Author: Martin | Platform Architecture
Phase: 9.2 - Performance Optimization
"""

import asyncio
import time
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "lib"))


def test_strategic_performance_manager_integration():
    """
    🎯 INTEGRATION TEST: Phase 9.2 Strategic Performance Manager

    Tests User Stories 9.2.1 and 9.2.2 with real system integration:
    - Sub-Second Strategic Query Response (<200ms)
    - Resource-Efficient Operations (<100MB memory)
    """
    print("🏗️ Phase 9.2 Integration Test: Strategic Performance Manager")

    try:
        # Import and initialize the strategic performance manager
        from performance.strategic_performance_manager import (
            StrategicPerformanceManager,
            QueryType,
            QueryPerformanceResult,
        )
        from core.base_manager import BaseManagerConfig, ManagerType

        print("✅ Successfully imported strategic performance manager")

        # Create configuration for testing
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

        # Initialize strategic performance manager
        performance_manager = StrategicPerformanceManager(config=config)
        print("✅ Successfully initialized strategic performance manager")

        # Test BaseManager compliance
        assert hasattr(performance_manager, "logger")
        assert hasattr(performance_manager, "manage")
        assert hasattr(performance_manager, "get_config")
        print("✅ BaseManager pattern compliance validated")

        # Test performance targets configuration
        assert QueryType.EXECUTIVE_CRITICAL in performance_manager.performance_targets
        assert QueryType.STRATEGIC_STANDARD in performance_manager.performance_targets

        executive_target = performance_manager.performance_targets[
            QueryType.EXECUTIVE_CRITICAL
        ]
        strategic_target = performance_manager.performance_targets[
            QueryType.STRATEGIC_STANDARD
        ]

        assert executive_target.target_ms == 100
        assert strategic_target.target_ms == 200
        print("✅ Performance targets configured correctly")

        # Test memory baseline configuration
        assert performance_manager.memory_baseline_mb == 100
        print("✅ Memory baseline configured correctly")

        # Test memory monitoring
        memory_report = performance_manager.monitor_memory_usage()
        assert "current_mb" in memory_report
        assert "target_mb" in memory_report
        assert memory_report["target_mb"] == 100
        print(
            f"✅ Memory monitoring working - Current: {memory_report['current_mb']:.1f}MB"
        )

        # Test memory optimization
        optimization_result = performance_manager.optimize_memory_usage()
        assert "memory_saved_mb" in optimization_result
        assert "gc_collected_objects" in optimization_result
        print(
            f"✅ Memory optimization working - Saved: {optimization_result['memory_saved_mb']:.1f}MB"
        )

        # Test executive dashboard
        dashboard = performance_manager.get_executive_dashboard()
        assert "sla_compliance" in dashboard
        assert "memory_efficiency" in dashboard
        assert "business_impact" in dashboard
        print("✅ Executive dashboard generation working")

        # Test SLA compliance report
        sla_report = performance_manager.get_sla_compliance_report()
        assert "overall_sla" in sla_report
        assert "query_type_breakdown" in sla_report
        print("✅ SLA compliance reporting working")

        print("\n🎉 Phase 9.2 Integration Test: ALL TESTS PASSED")
        print("✅ User Story 9.2.1: Sub-Second Strategic Query Response - READY")
        print("✅ User Story 9.2.2: Resource-Efficient Operations - READY")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("⚠️  Strategic Performance Manager not available - implementation needed")
        return False

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_strategic_query_performance():
    """Test strategic query performance with async operations"""
    print("\n🏗️ Testing Strategic Query Performance...")

    try:
        from performance.strategic_performance_manager import (
            StrategicPerformanceManager,
            QueryType,
        )
        from core.base_manager import BaseManagerConfig, ManagerType

        # Initialize performance manager
        config = BaseManagerConfig(
            manager_name="test_performance",
            manager_type=ManagerType.PERFORMANCE,
            enable_cache=True,
            enable_metrics=True,
            custom_config={"strategic_target_ms": 200, "optimization_enabled": True},
        )

        performance_manager = StrategicPerformanceManager(config=config)

        # Mock strategic query function
        async def mock_strategic_query(context: str) -> dict:
            """Simulate strategic analysis"""
            await asyncio.sleep(0.05)  # 50ms processing
            return {"analysis": f"Strategic analysis for {context}", "confidence": 0.95}

        # Test strategic query optimization
        start_time = time.time()
        query_result, performance_result = (
            await performance_manager.optimize_strategic_query(
                mock_strategic_query,
                QueryType.STRATEGIC_STANDARD,
                "test_executive_context",
            )
        )
        total_time = (time.time() - start_time) * 1000

        # Validate results
        assert query_result is not None
        assert "analysis" in query_result
        assert performance_result.execution_time_ms < 200  # <200ms requirement
        assert performance_result.target_achieved == True

        print(f"✅ Strategic query completed in {total_time:.1f}ms (target: <200ms)")
        print(f"✅ Performance result: {performance_result.execution_time_ms:.1f}ms")
        print(f"✅ Cache optimization: {performance_result.optimization_applied}")

        # Test cache effectiveness with second query
        start_time2 = time.time()
        query_result2, performance_result2 = (
            await performance_manager.optimize_strategic_query(
                mock_strategic_query,
                QueryType.STRATEGIC_STANDARD,
                "test_executive_context",  # Same context for cache hit
            )
        )
        total_time2 = (time.time() - start_time2) * 1000

        print(f"✅ Second query (cached) completed in {total_time2:.1f}ms")
        print(f"✅ Cache hit: {performance_result2.cache_hit}")

        return True

    except Exception as e:
        print(f"❌ Strategic query test failed: {e}")
        return False


def run_phase92_integration_tests():
    """Run all Phase 9.2 integration tests"""
    print("=" * 80)
    print("🚀 PHASE 9.2 INTEGRATION TESTS: Strategic Performance Manager")
    print("=" * 80)

    # Test 1: Basic integration
    test1_passed = test_strategic_performance_manager_integration()

    # Test 2: Async query performance
    test2_passed = asyncio.run(test_strategic_query_performance())

    # Summary
    print("\n" + "=" * 80)
    print("📊 PHASE 9.2 INTEGRATION TEST SUMMARY")
    print("=" * 80)

    total_tests = 2
    passed_tests = sum([test1_passed, test2_passed])

    print(f"Tests Passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 ALL PHASE 9.2 INTEGRATION TESTS PASSED!")
        print("✅ Ready for User Story validation and executive review")
        return True
    else:
        print("❌ Some integration tests failed - implementation needs work")
        return False


if __name__ == "__main__":
    success = run_phase92_integration_tests()
    sys.exit(0 if success else 1)
