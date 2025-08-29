"""
P0 Tests for Phase 8 Performance Optimization

Critical performance and functionality tests for enterprise-grade performance components.
Ensures <500ms response times and <50MB memory usage.
"""

import unittest
import asyncio
import time
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import performance components to test
try:
    from claudedirector.lib.performance.cache_manager import CacheManager, CacheLevel
    from claudedirector.lib.performance.memory_optimizer import (
        MemoryOptimizer,
        ObjectPool,
    )
    from claudedirector.lib.performance.response_optimizer import (
        ResponseOptimizer,
        ResponsePriority,
    )
    from claudedirector.lib.performance.performance_monitor import PerformanceMonitor
except ImportError:
    # Fallback for test environment
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    from lib.performance.cache_manager import CacheManager, CacheLevel
    from lib.performance.memory_optimizer import MemoryOptimizer, ObjectPool
    from lib.performance.response_optimizer import ResponseOptimizer, ResponsePriority
    from lib.performance.performance_monitor import PerformanceMonitor


class TestPhase8PerformanceP0(unittest.TestCase):
    """P0 test suite for Phase 8 performance optimization components"""

    def setUp(self):
        """Set up test fixtures"""
        self.cache_manager = CacheManager(max_memory_mb=10, max_entries=100)
        self.memory_optimizer = MemoryOptimizer(
            target_memory_mb=30, alert_threshold_mb=35
        )
        self.response_optimizer = ResponseOptimizer(
            max_workers=2, target_response_ms=400
        )
        self.response_optimizer._test_mode = (
            True  # Enable test mode for direct execution
        )
        self.performance_monitor = PerformanceMonitor(
            retention_hours=1, alert_cooldown_seconds=10
        )

    def test_p0_cache_performance_targets(self):
        """P0: Cache operations must meet <50ms performance targets"""

        async def run_cache_performance_test():
            # Test cache set performance
            start_time = time.time()
            await self.cache_manager.set(
                "test_key", "test_value", CacheLevel.CONTEXT_ANALYSIS
            )
            set_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Cache set must be under 50ms
            self.assertLess(
                set_time, 50, f"Cache set took {set_time:.1f}ms, must be <50ms"
            )

            # Test cache get performance
            start_time = time.time()
            value = await self.cache_manager.get("test_key")
            get_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Cache get must be under 50ms
            self.assertLess(
                get_time, 50, f"Cache get took {get_time:.1f}ms, must be <50ms"
            )

            # Verify cache functionality
            self.assertEqual(value, "test_value")

            # Test cache hit performance with multiple operations
            total_operations = 100
            start_time = time.time()

            for i in range(total_operations):
                await self.cache_manager.get("test_key")

            batch_time = (time.time() - start_time) * 1000
            avg_time_per_op = batch_time / total_operations

            # P0 CRITICAL: Average cache get must be well under 50ms
            self.assertLess(
                avg_time_per_op,
                10,
                f"Average cache get took {avg_time_per_op:.1f}ms, must be <10ms for batched operations",
            )

        asyncio.run(run_cache_performance_test())

    def test_p0_memory_usage_limits(self):
        """P0: Memory optimizer must maintain <50MB usage limits"""

        # Test memory tracking functionality
        current_memory = self.memory_optimizer.get_memory_usage()
        self.assertIsInstance(current_memory, float)
        self.assertGreater(current_memory, 0)

        # Test object pool memory efficiency
        pool = self.memory_optimizer.create_object_pool(
            "test_pool", lambda: {"data": "test"}, max_size=50
        )

        # Create and release objects to test pooling
        objects = []
        for i in range(10):
            obj = pool.acquire()
            objects.append(obj)

        # Release objects back to pool
        for obj in objects:
            pool.release(obj)

        # Now acquire again to test reuse
        reused_objects = []
        for i in range(5):
            obj = pool.acquire()
            reused_objects.append(obj)

        # Test pool efficiency
        pool_stats = pool.get_stats()
        self.assertGreater(pool_stats["reuse_rate"], 0, f"Pool stats: {pool_stats}")

        # Test memory pressure detection
        pressure_detected = self.memory_optimizer.check_memory_pressure()

        # Memory should be well under threshold for tests
        memory_stats = self.memory_optimizer.get_memory_stats()
        self.assertLess(
            memory_stats.current_usage_mb,
            50,
            f"Memory usage {memory_stats.current_usage_mb:.1f}MB exceeds 50MB limit",
        )

    def test_p0_response_time_optimization(self):
        """P0: Response optimizer must achieve <500ms response times"""

        async def run_response_optimization_test():
            # Define test functions with different complexities
            async def fast_function():
                await asyncio.sleep(0.01)  # 10ms
                return "fast_result"

            def sync_function():
                time.sleep(0.05)  # 50ms
                return "sync_result"

            # Test critical priority optimization
            start_time = time.time()
            result = await self.response_optimizer.optimize_call(
                fast_function, priority=ResponsePriority.CRITICAL
            )
            critical_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Critical priority must be under 100ms
            self.assertLess(
                critical_time,
                100,
                f"Critical priority response took {critical_time:.1f}ms, must be <100ms",
            )
            self.assertEqual(result, "fast_result")

            # Test normal priority optimization
            start_time = time.time()
            result = await self.response_optimizer.optimize_call(
                sync_function, priority=ResponsePriority.NORMAL
            )
            normal_time = (time.time() - start_time) * 1000

            # P0 CRITICAL: Normal priority must be under 500ms
            self.assertLess(
                normal_time,
                500,
                f"Normal priority response took {normal_time:.1f}ms, must be <500ms",
            )
            self.assertEqual(result, "sync_result")

            # Test batch performance
            batch_size = 10
            start_time = time.time()

            tasks = []
            for i in range(batch_size):
                task = self.response_optimizer.optimize_call(
                    fast_function, priority=ResponsePriority.HIGH
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            batch_time = (time.time() - start_time) * 1000
            avg_time_per_request = batch_time / batch_size

            # P0 CRITICAL: Batch processing efficiency
            self.assertLess(
                avg_time_per_request,
                200,
                f"Average batch response time {avg_time_per_request:.1f}ms, must be <200ms",
            )
            self.assertEqual(len(results), batch_size)

        asyncio.run(run_response_optimization_test())

    def test_p0_performance_monitoring_accuracy(self):
        """P0: Performance monitor must accurately track system metrics"""

        # Test metric recording
        test_metrics = [100.5, 200.3, 150.7, 300.2, 180.9]

        for metric_value in test_metrics:
            self.performance_monitor.record_metric("test_response_time", metric_value)

        # Test metric retrieval accuracy
        latest_metric = self.performance_monitor.get_latest_metric("test_response_time")
        self.assertEqual(latest_metric, test_metrics[-1])

        # Test average calculation
        avg_metric = self.performance_monitor.get_average_metric(
            "test_response_time", window_seconds=60
        )
        expected_avg = sum(test_metrics) / len(test_metrics)
        self.assertAlmostEqual(avg_metric, expected_avg, places=1)

        # Test percentile calculation
        p95_metric = self.performance_monitor.get_metric_percentile(
            "test_response_time", 0.95, window_seconds=60
        )
        self.assertIsNotNone(p95_metric)
        self.assertGreater(p95_metric, 0)

        # Test counter functionality
        initial_count = self.performance_monitor.counters.get("test_counter", 0)
        self.performance_monitor.increment_counter("test_counter", 5)
        final_count = self.performance_monitor.counters.get("test_counter", 0)
        self.assertEqual(final_count, initial_count + 5)

        # Test alerting functionality
        # Set a low threshold to trigger alert
        self.performance_monitor.set_threshold(
            "test_response_time", warning=50, critical=100
        )

        # Record metric that should trigger alert
        self.performance_monitor.record_metric(
            "test_response_time", 150
        )  # Above critical threshold

        # Verify alert was triggered
        alert_key = "test_response_time_threshold"
        self.assertIn(alert_key, self.performance_monitor.active_alerts)

    def test_p0_integrated_performance_system(self):
        """P0: All performance components must work together effectively"""

        async def run_integration_test():
            # Test integrated cache + response optimization
            cache_key = "integration_test"

            # Function that uses cache
            async def cached_expensive_function(data):
                # Check cache first
                cached_result = await self.cache_manager.get(cache_key)
                if cached_result:
                    return cached_result

                # Simulate expensive computation
                await asyncio.sleep(0.1)  # 100ms
                result = f"computed_{data}"

                # Cache the result
                await self.cache_manager.set(
                    cache_key, result, CacheLevel.CONTEXT_ANALYSIS
                )
                return result

            # First call (cache miss) - should be slower
            start_time = time.time()
            result1 = await self.response_optimizer.optimize_call(
                cached_expensive_function, "test_data", priority=ResponsePriority.NORMAL
            )
            first_call_time = (time.time() - start_time) * 1000

            # Second call (cache hit) - should be much faster
            start_time = time.time()
            result2 = await self.response_optimizer.optimize_call(
                cached_expensive_function, "test_data", priority=ResponsePriority.NORMAL
            )
            second_call_time = (time.time() - start_time) * 1000

            # Verify functionality
            self.assertEqual(result1, result2)
            self.assertEqual(result1, "computed_test_data")

            # P0 CRITICAL: Cache hit should be significantly faster
            self.assertLess(
                second_call_time,
                first_call_time / 2,
                f"Cache hit not fast enough: {second_call_time:.1f}ms vs {first_call_time:.1f}ms",
            )

            # P0 CRITICAL: Even cache miss should be under target
            self.assertLess(
                first_call_time,
                500,
                f"Cache miss response time {first_call_time:.1f}ms exceeds 500ms target",
            )

            # Test memory efficiency during operations
            memory_before = self.memory_optimizer.get_memory_usage()

            # Perform multiple operations
            for i in range(50):
                await self.response_optimizer.optimize_call(
                    lambda x: f"result_{x}", i, priority=ResponsePriority.HIGH
                )

            memory_after = self.memory_optimizer.get_memory_usage()
            memory_increase = memory_after - memory_before

            # P0 CRITICAL: Memory increase should be minimal
            self.assertLess(
                memory_increase,
                10,
                f"Memory increased by {memory_increase:.1f}MB during operations, should be <10MB",
            )

        asyncio.run(run_integration_test())

    def test_p0_component_initialization_performance(self):
        """P0: All performance components must initialize quickly"""

        # Test cache manager initialization
        start_time = time.time()
        cache_mgr = CacheManager(max_memory_mb=5, max_entries=50)
        cache_init_time = (time.time() - start_time) * 1000

        self.assertLess(
            cache_init_time,
            100,
            f"Cache manager initialization took {cache_init_time:.1f}ms, must be <100ms",
        )

        # Test memory optimizer initialization
        start_time = time.time()
        mem_opt = MemoryOptimizer(target_memory_mb=25)
        mem_init_time = (time.time() - start_time) * 1000

        self.assertLess(
            mem_init_time,
            100,
            f"Memory optimizer initialization took {mem_init_time:.1f}ms, must be <100ms",
        )

        # Test response optimizer initialization
        start_time = time.time()
        resp_opt = ResponseOptimizer(max_workers=2)
        resp_init_time = (time.time() - start_time) * 1000

        self.assertLess(
            resp_init_time,
            100,
            f"Response optimizer initialization took {resp_init_time:.1f}ms, must be <100ms",
        )

        # Test performance monitor initialization
        start_time = time.time()
        perf_mon = PerformanceMonitor(retention_hours=1)
        mon_init_time = (time.time() - start_time) * 1000

        self.assertLess(
            mon_init_time,
            100,
            f"Performance monitor initialization took {mon_init_time:.1f}ms, must be <100ms",
        )

    def test_p0_error_handling_and_resilience(self):
        """P0: Performance components must handle errors gracefully"""

        async def run_error_resilience_test():
            # Test cache manager error handling
            try:
                # Test with invalid data that might cause serialization issues
                problematic_data = {"circular_ref": None}
                problematic_data["circular_ref"] = problematic_data

                # Should not crash
                success = await self.cache_manager.set("problem_key", problematic_data)
                # May succeed or fail, but should not crash
                self.assertIsInstance(success, bool)

            except Exception as e:
                self.fail(f"Cache manager crashed on problematic data: {e}")

            # Test response optimizer error handling
            async def failing_function():
                raise ValueError("Test error")

            try:
                await self.response_optimizer.optimize_call(
                    failing_function, priority=ResponsePriority.NORMAL
                )
                self.fail("Expected ValueError to be propagated")
            except ValueError:
                # Expected behavior - error should be propagated
                pass
            except Exception as e:
                self.fail(f"Unexpected error type: {type(e)}: {e}")

            # Test memory optimizer error handling
            try:
                # Force garbage collection should not crash
                collected = self.memory_optimizer.force_gc()
                self.assertIsInstance(collected, int)
                self.assertGreaterEqual(collected, 0)

            except Exception as e:
                self.fail(f"Memory optimizer crashed during GC: {e}")

            # Test performance monitor error handling
            try:
                # Record invalid metric - should handle gracefully
                self.performance_monitor.record_metric("test", float("inf"))
                self.performance_monitor.record_metric("test", float("nan"))

                # Should not crash the monitor
                stats = self.performance_monitor.get_performance_dashboard()
                self.assertIsInstance(stats, dict)

            except Exception as e:
                self.fail(f"Performance monitor crashed on invalid metrics: {e}")

        asyncio.run(run_error_resilience_test())

    def tearDown(self):
        """Clean up test resources"""

        # Clean up async resources
        async def cleanup():
            await self.cache_manager.cleanup()
            await self.response_optimizer.cleanup()
            await self.performance_monitor.cleanup()

        try:
            asyncio.run(cleanup())
        except Exception:
            # Cleanup errors are not critical for tests
            pass

        # Clean up memory optimizer
        self.memory_optimizer.cleanup()


if __name__ == "__main__":
    unittest.main()
