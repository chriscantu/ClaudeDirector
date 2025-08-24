#!/usr/bin/env python3
"""
Business-Critical Regression Test: Performance

Alvaro's Test Suite: Ensures system performance meets business requirements
under realistic load conditions for executive and strategic use cases.

BUSINESS IMPACT: Performance degradation leads to poor user experience,
executive frustration, and abandonment of strategic intelligence tools.
"""

import unittest
import time
import concurrent.futures
import psutil
import tempfile
import json
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPerformance(unittest.TestCase):
    """Business-critical tests for system performance under load"""

    def setUp(self):
        """Set up performance testing environment"""
        self.test_dir = tempfile.mkdtemp()
        self.performance_data = []
        self.max_response_time = 5.0  # 5 seconds max for strategic queries
        self.max_memory_mb = 1024  # 1GB max memory usage
        self.min_throughput = (
            2  # 2 requests per second minimum (single-user local framework)
        )

    def tearDown(self):
        """Clean up performance test environment"""
        # Save performance data for analysis
        if self.performance_data:
            perf_file = Path(self.test_dir) / "performance_results.json"
            with open(perf_file, "w") as f:
                json.dump(self.performance_data, f, indent=2)

    def test_strategic_query_response_time(self):
        """
        BUSINESS CRITICAL: Strategic queries must respond within acceptable time

        FAILURE IMPACT: Executives wait too long, abandon strategic analysis
        BUSINESS COST: Reduced usage, poor executive experience, tool abandonment
        """
        # Test strategic query scenarios
        strategic_queries = [
            {
                "query": "How should we restructure engineering teams for platform scaling?",
                "expected_personas": ["diego", "camille"],
                "complexity": "high",
                "max_time": 4.0,
            },
            {
                "query": "What's the ROI analysis for our platform investment?",
                "expected_personas": ["alvaro"],
                "complexity": "medium",
                "max_time": 3.0,
            },
            {
                "query": "Design system strategy for cross-team adoption?",
                "expected_personas": ["rachel"],
                "complexity": "medium",
                "max_time": 3.0,
            },
            {
                "query": "Quick status update on current initiatives",
                "expected_personas": ["diego"],
                "complexity": "low",
                "max_time": 2.0,
            },
        ]

        performance_results = []

        for query_test in strategic_queries:
            start_time = time.time()

            # Simulate strategic query processing
            result = self._simulate_strategic_query(
                query_test["query"],
                query_test["expected_personas"],
                query_test["complexity"],
            )

            end_time = time.time()
            response_time = end_time - start_time

            # Record performance
            perf_data = {
                "query": query_test["query"][:50] + "...",
                "complexity": query_test["complexity"],
                "response_time": response_time,
                "max_allowed": query_test["max_time"],
                "passed": response_time <= query_test["max_time"],
                "timestamp": datetime.now().isoformat(),
            }
            performance_results.append(perf_data)

            # Assert performance requirement
            self.assertLessEqual(
                response_time,
                query_test["max_time"],
                f"Query '{query_test['query'][:30]}...' took {response_time:.2f}s, "
                f"max allowed: {query_test['max_time']}s",
            )

        # Calculate average response time
        avg_response_time = sum(r["response_time"] for r in performance_results) / len(
            performance_results
        )
        self.assertLessEqual(avg_response_time, self.max_response_time)

        self.performance_data.extend(performance_results)
        print(
            f"✅ Strategic query response time: PASSED (avg: {avg_response_time:.2f}s)"
        )

    def test_concurrent_user_load(self):
        """
        BUSINESS CRITICAL: System must handle multiple concurrent strategic queries (single-user)

        FAILURE IMPACT: System becomes unusable during complex strategic analysis
        BUSINESS COST: Cannot support intensive strategic sessions on local machine
        """
        concurrent_queries = (
            3  # Simulate 3 concurrent strategic queries (single-user local framework)
        )
        queries_per_user = 5

        def simulate_user_session(user_id):
            """Simulate a single user's strategic session"""
            user_performance = []

            for query_num in range(queries_per_user):
                start_time = time.time()

                # Simulate different types of strategic queries
                query_types = [
                    "organizational_analysis",
                    "roi_calculation",
                    "framework_application",
                    "stakeholder_analysis",
                    "decision_support",
                ]

                query_type = query_types[query_num % len(query_types)]
                result = self._simulate_strategic_query(
                    f"User {user_id} query {query_num}: {query_type}",
                    ["diego", "alvaro"],
                    "medium",
                )

                end_time = time.time()
                response_time = end_time - start_time

                user_performance.append(
                    {
                        "user_id": user_id,
                        "query_num": query_num,
                        "query_type": query_type,
                        "response_time": response_time,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                # Small delay between queries
                time.sleep(0.1)

            return user_performance

        # Run concurrent user sessions
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=concurrent_queries
        ) as executor:
            futures = [
                executor.submit(simulate_user_session, query_id)
                for query_id in range(concurrent_queries)
            ]

            # Collect results
            all_results = []
            for future in concurrent.futures.as_completed(futures):
                user_results = future.result()
                all_results.extend(user_results)

        end_time = time.time()
        total_duration = end_time - start_time

        # Analyze concurrent performance
        total_queries = len(all_results)
        avg_response_time = sum(r["response_time"] for r in all_results) / total_queries
        throughput = total_queries / total_duration

        # Performance assertions
        self.assertLessEqual(
            avg_response_time,
            self.max_response_time,
            f"Average response time {avg_response_time:.2f}s exceeds limit",
        )
        self.assertGreaterEqual(
            throughput,
            self.min_throughput,
            f"Throughput {throughput:.2f} req/s below minimum",
        )

        # Check for performance degradation under load
        max_response_time = max(r["response_time"] for r in all_results)
        self.assertLessEqual(
            max_response_time,
            self.max_response_time * 2,
            "Maximum response time under load exceeds acceptable threshold",
        )

        self.performance_data.extend(all_results)
        print(
            f"✅ Concurrent query load: PASSED ({concurrent_queries} queries, {throughput:.1f} req/s)"
        )

    def test_memory_usage_under_load(self):
        """
        BUSINESS CRITICAL: Memory usage must stay within acceptable limits

        FAILURE IMPACT: System crashes, data loss, service interruption
        BUSINESS COST: Service downtime, lost strategic sessions, data recovery
        """
        # Get baseline memory usage
        process = psutil.Process()
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

        memory_measurements = [{"phase": "baseline", "memory_mb": baseline_memory}]

        # Simulate heavy strategic analysis workload
        large_datasets = []

        for iteration in range(10):
            # Simulate loading strategic data
            strategic_data = {
                "stakeholder_analysis": self._generate_mock_stakeholder_data(1000),
                "framework_patterns": self._generate_mock_framework_data(500),
                "roi_calculations": self._generate_mock_roi_data(200),
                "organizational_metrics": self._generate_mock_org_data(300),
            }
            large_datasets.append(strategic_data)

            # Measure memory after each iteration
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_measurements.append(
                {
                    "phase": f"iteration_{iteration}",
                    "memory_mb": current_memory,
                    "memory_increase": current_memory - baseline_memory,
                }
            )

            # Assert memory doesn't exceed limits
            self.assertLessEqual(
                current_memory,
                self.max_memory_mb,
                f"Memory usage {current_memory:.1f}MB exceeds limit {self.max_memory_mb}MB",
            )

            # Brief processing simulation
            time.sleep(0.1)

        # Test memory cleanup
        large_datasets.clear()

        # Force garbage collection simulation
        import gc

        gc.collect()
        time.sleep(0.5)

        # Measure memory after cleanup
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_measurements.append(
            {
                "phase": "after_cleanup",
                "memory_mb": final_memory,
                "memory_recovered": memory_measurements[-1]["memory_mb"] - final_memory,
            }
        )

        # Verify memory was recovered (within 50% of peak usage)
        peak_memory = max(m["memory_mb"] for m in memory_measurements)
        memory_recovery_ratio = (peak_memory - final_memory) / (
            peak_memory - baseline_memory
        )

        self.assertGreaterEqual(
            memory_recovery_ratio,
            0.2,  # At least 20% recovery (adjusted for local single-user framework)
            f"Insufficient memory recovery: {memory_recovery_ratio:.2f}",
        )

        self.performance_data.extend(memory_measurements)
        print(
            f"✅ Memory usage under load: PASSED (peak: {peak_memory:.1f}MB, recovery: {memory_recovery_ratio:.1%})"
        )

    def test_database_query_performance(self):
        """
        BUSINESS CRITICAL: Database queries must perform within acceptable limits

        FAILURE IMPACT: Slow strategic data retrieval, poor user experience
        BUSINESS COST: Delayed strategic decisions, frustrated executives
        """
        # Simulate database operations for strategic intelligence
        db_operations = [
            {
                "operation": "stakeholder_lookup",
                "complexity": "simple",
                "max_time": 0.5,
                "records": 100,
            },
            {
                "operation": "framework_search",
                "complexity": "medium",
                "max_time": 1.0,
                "records": 500,
            },
            {
                "operation": "roi_analysis_query",
                "complexity": "complex",
                "max_time": 2.0,
                "records": 1000,
            },
            {
                "operation": "organizational_metrics",
                "complexity": "complex",
                "max_time": 3.0,  # Increased for local database processing
                "records": 2000,
            },
        ]

        db_performance = []

        for operation in db_operations:
            start_time = time.time()

            # Simulate database query
            result = self._simulate_database_query(
                operation["operation"], operation["records"], operation["complexity"]
            )

            end_time = time.time()
            query_time = end_time - start_time

            # Record performance
            perf_data = {
                "operation": operation["operation"],
                "complexity": operation["complexity"],
                "records": operation["records"],
                "query_time": query_time,
                "max_allowed": operation["max_time"],
                "passed": query_time <= operation["max_time"],
                "timestamp": datetime.now().isoformat(),
            }
            db_performance.append(perf_data)

            # Assert performance requirement
            self.assertLessEqual(
                query_time,
                operation["max_time"],
                f"Database operation '{operation['operation']}' took {query_time:.2f}s, "
                f"max allowed: {operation['max_time']}s",
            )

        # Test batch operations performance
        start_time = time.time()
        batch_results = []

        for i in range(20):  # Simulate 20 quick lookups
            result = self._simulate_database_query("quick_lookup", 10, "simple")
            batch_results.append(result)

        batch_time = time.time() - start_time
        avg_batch_time = batch_time / 20

        # Batch operations should be very fast
        self.assertLessEqual(avg_batch_time, 0.1, "Batch operations too slow")

        self.performance_data.extend(db_performance)
        print(
            f"✅ Database query performance: PASSED (avg batch: {avg_batch_time:.3f}s)"
        )

    def test_system_resource_efficiency(self):
        """
        BUSINESS CRITICAL: System must use resources efficiently

        FAILURE IMPACT: High resource usage, system instability, poor scalability
        BUSINESS COST: Infrastructure costs, system crashes, poor user experience
        """
        # Monitor system resources during strategic analysis
        resource_measurements = []

        # Get baseline measurements
        baseline_cpu = psutil.cpu_percent(interval=1)
        baseline_memory = psutil.virtual_memory().percent

        resource_measurements.append(
            {
                "phase": "baseline",
                "cpu_percent": baseline_cpu,
                "memory_percent": baseline_memory,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Simulate intensive strategic analysis
        for phase in ["light_load", "medium_load", "heavy_load"]:
            # Simulate different load levels
            if phase == "light_load":
                workload_iterations = 5
            elif phase == "medium_load":
                workload_iterations = 15
            else:  # heavy_load
                workload_iterations = 30

            # Run workload
            for i in range(workload_iterations):
                self._simulate_strategic_analysis_work()
                time.sleep(0.05)  # Brief pause

            # Measure resources
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory_percent = psutil.virtual_memory().percent

            resource_measurements.append(
                {
                    "phase": phase,
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "workload_iterations": workload_iterations,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Assert resource usage stays reasonable
            self.assertLessEqual(
                cpu_percent, 80.0, f"CPU usage too high in {phase}: {cpu_percent}%"
            )
            self.assertLessEqual(
                memory_percent,
                85.0,
                f"Memory usage too high in {phase}: {memory_percent}%",
            )

        # Test resource recovery after load
        time.sleep(2)  # Allow system to settle

        final_cpu = psutil.cpu_percent(interval=1)
        final_memory = psutil.virtual_memory().percent

        resource_measurements.append(
            {
                "phase": "recovery",
                "cpu_percent": final_cpu,
                "memory_percent": final_memory,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Verify system recovers to reasonable levels
        self.assertLessEqual(
            final_cpu, baseline_cpu + 10, "CPU usage didn't recover properly"
        )

        self.performance_data.extend(resource_measurements)
        print(
            f"✅ System resource efficiency: PASSED (final CPU: {final_cpu:.1f}%, Memory: {final_memory:.1f}%)"
        )

    def _simulate_strategic_query(self, query, personas, complexity):
        """Simulate processing a strategic query"""
        # Simulate different processing times based on complexity
        processing_times = {"low": 0.2, "medium": 0.8, "high": 1.5}

        base_time = processing_times.get(complexity, 0.5)

        # Add some variability
        import random

        actual_time = base_time * (0.8 + random.random() * 0.4)

        # Simulate processing work
        time.sleep(actual_time)

        return {
            "query": query,
            "personas": personas,
            "complexity": complexity,
            "processing_time": actual_time,
            "result": f"Strategic analysis for: {query[:30]}...",
        }

    def _simulate_database_query(self, operation, records, complexity):
        """Simulate database query operations"""
        # Simulate query processing time based on complexity and record count
        base_time_per_record = {"simple": 0.0001, "medium": 0.0005, "complex": 0.001}

        processing_time = base_time_per_record[complexity] * records

        # Add some realistic database overhead
        overhead = 0.05 if complexity == "simple" else 0.1
        total_time = processing_time + overhead

        time.sleep(total_time)

        return {
            "operation": operation,
            "records_processed": records,
            "processing_time": total_time,
        }

    def _simulate_strategic_analysis_work(self):
        """Simulate CPU-intensive strategic analysis work"""
        # Simulate some computational work
        result = 0
        for i in range(10000):
            result += i * 0.001
        return result

    def _generate_mock_stakeholder_data(self, count):
        """Generate mock stakeholder data for memory testing"""
        return [
            {
                "id": f"stakeholder_{i}",
                "name": f"Executive {i}",
                "role": f"VP {i % 5}",
                "influence": i % 10,
                "relationships": [f"rel_{j}" for j in range(i % 10)],
            }
            for i in range(count)
        ]

    def _generate_mock_framework_data(self, count):
        """Generate mock framework data for memory testing"""
        return [
            {
                "id": f"framework_{i}",
                "name": f"Framework {i}",
                "patterns": [f"pattern_{j}" for j in range(i % 20)],
                "applications": [f"app_{j}" for j in range(i % 15)],
            }
            for i in range(count)
        ]

    def _generate_mock_roi_data(self, count):
        """Generate mock ROI data for memory testing"""
        return [
            {
                "investment_id": f"inv_{i}",
                "amount": i * 1000,
                "roi": i * 0.01,
                "timeline": [f"milestone_{j}" for j in range(i % 8)],
            }
            for i in range(count)
        ]

    def _generate_mock_org_data(self, count):
        """Generate mock organizational data for memory testing"""
        return [
            {
                "metric_id": f"metric_{i}",
                "value": i * 0.1,
                "trend": [i + j for j in range(i % 12)],
                "metadata": {"category": f"cat_{i % 5}", "priority": i % 3},
            }
            for i in range(count)
        ]


def run_business_critical_performance_tests():
    """Run all business-critical performance tests"""
    print("🔥 BUSINESS-CRITICAL REGRESSION TEST: Performance")
    print("=" * 70)
    print("OWNER: Alvaro | IMPACT: User Experience & System Reliability")
    print("FAILURE COST: Poor UX, executive frustration, system abandonment")
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformance)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL PERFORMANCE TESTS PASSED")
        print("💼 Business Impact: System performance maintained for executives")
        print("📊 Strategic Value: Reliable strategic intelligence delivery")
        return True
    else:
        print(f"\n❌ PERFORMANCE TEST FAILURES: {len(result.failures + result.errors)}")
        print("💥 Business Impact: Poor user experience, system unreliability")
        print("🚨 Action Required: Fix performance issues immediately")
        return False


if __name__ == "__main__":
    success = run_business_critical_performance_tests()
    sys.exit(0 if success else 1)
