#!/usr/bin/env python3
"""
Performance Requirements Testing
Tests that ClaudeDirector meets strict performance requirements for CI/CD
"""

import sys
import time
import unittest
import subprocess
import statistics
from pathlib import Path
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

try:
    from integration_protection.cursor_transparency_bridge import CursorTransparencyBridge
    TRANSPARENCY_AVAILABLE = True
except ImportError:
    TRANSPARENCY_AVAILABLE = False

class TestPerformanceRequirements(unittest.TestCase):
    """Performance requirements validation for CI/CD pipeline"""

    def setUp(self):
        """Set up performance testing environment"""
        self.performance_results = {}
        self.max_response_time = 2.0  # 2 second requirement from CI config
        self.max_api_response = 0.5   # 500ms requirement from CI config

    def measure_execution_time(self, func, *args, **kwargs) -> Tuple[float, any]:
        """Measure execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        return duration, result

    def test_transparency_bridge_performance(self):
        """Test transparency bridge meets performance requirements"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        bridge = CursorTransparencyBridge()

        # Test simple response (should be very fast)
        simple_input = "Hello"
        simple_response = "Hello! How can I help you today?"

        duration, enhanced_response = self.measure_execution_time(
            bridge.apply_transparency_system,
            simple_response, simple_input, "martin"
        )

        self.assertLess(duration, 0.1)  # Should be under 100ms for simple responses
        self.assertIsInstance(enhanced_response, str)

        # Test complex strategic response (should still be under limit)
        complex_input = "How should we scale our platform architecture across multiple international markets while coordinating with executive stakeholders?"
        complex_response = "🎯 Diego | Engineering Leadership\n\nGreat strategic question! Let me apply systematic frameworks to analyze this complex organizational challenge..."

        duration, enhanced_response = self.measure_execution_time(
            bridge.apply_transparency_system,
            complex_response, complex_input, "diego"
        )

        self.assertLess(duration, self.max_api_response)  # Under 500ms requirement
        self.assertIsInstance(enhanced_response, str)

        # Store results
        self.performance_results["transparency_bridge"] = {
            "simple_response_time": duration,
            "complex_response_time": duration,
            "requirement_met": duration < self.max_api_response
        }

    def test_p0_test_performance(self):
        """Test that P0 tests complete within performance requirements"""
        test_commands = [
            ("MCP Transparency P0", "python3 .claudedirector/tests/regression/test_mcp_transparency_p0.py"),
            ("Hybrid Installation P0", "python3 .claudedirector/tests/integration/test_hybrid_installation_p0.py"),
            ("P0 Enforcement", "python3 .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py")
        ]

        test_results = {}

        for test_name, command in test_commands:
            start_time = time.time()

            try:
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout
                    cwd=PROJECT_ROOT
                )

                duration = time.time() - start_time
                success = result.returncode == 0

                test_results[test_name] = {
                    "duration": duration,
                    "success": success,
                    "requirement_met": duration < 10.0  # P0 tests should complete quickly
                }

                self.assertTrue(success, f"{test_name} must pass for performance testing")
                self.assertLess(duration, 10.0, f"{test_name} took too long: {duration:.2f}s")

            except subprocess.TimeoutExpired:
                self.fail(f"{test_name} timed out (>30s)")

        self.performance_results["p0_tests"] = test_results

    def test_concurrent_load_performance(self):
        """Test performance under concurrent load"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        def simulate_request(request_id):
            """Simulate a single strategic request"""
            bridge = CursorTransparencyBridge()

            strategic_input = f"Strategic question {request_id}: How should we approach organizational transformation?"
            strategic_response = f"🎯 Diego | Engineering Leadership\n\nStrategic analysis {request_id}..."

            start_time = time.time()
            enhanced_response = bridge.apply_transparency_system(
                strategic_response, strategic_input, "diego"
            )
            duration = time.time() - start_time

            return {
                "request_id": request_id,
                "duration": duration,
                "success": isinstance(enhanced_response, str) and len(enhanced_response) > 0
            }

        # Test with 10 concurrent requests
        max_concurrent_users = 10
        request_durations = []
        successful_requests = 0

        with ThreadPoolExecutor(max_workers=max_concurrent_users) as executor:
            # Submit all requests
            futures = [executor.submit(simulate_request, i) for i in range(max_concurrent_users)]

            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    request_durations.append(result["duration"])

                    if result["success"]:
                        successful_requests += 1

                except Exception as e:
                    self.fail(f"Concurrent request failed: {str(e)}")

        # Analyze performance under load
        avg_duration = statistics.mean(request_durations)
        max_duration = max(request_durations)
        success_rate = successful_requests / max_concurrent_users

        # Performance requirements under load
        self.assertEqual(successful_requests, max_concurrent_users, "All requests must succeed")
        self.assertLess(avg_duration, self.max_api_response, f"Average response time too high: {avg_duration:.3f}s")
        self.assertLess(max_duration, self.max_response_time, f"Max response time too high: {max_duration:.3f}s")
        self.assertGreaterEqual(success_rate, 0.95, "Success rate too low under load")

        self.performance_results["concurrent_load"] = {
            "concurrent_users": max_concurrent_users,
            "avg_duration": avg_duration,
            "max_duration": max_duration,
            "success_rate": success_rate,
            "requirement_met": max_duration < self.max_response_time
        }

    def test_memory_performance(self):
        """Test memory usage stays within reasonable bounds"""
        import psutil
        import os

        # Measure initial memory
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Perform memory-intensive operations
        if TRANSPARENCY_AVAILABLE:
            bridge = CursorTransparencyBridge()

            # Process multiple strategic responses
            for i in range(50):
                strategic_input = f"Strategic question {i}: Complex organizational analysis required."
                strategic_response = f"🎯 Diego | Engineering Leadership\n\nDetailed strategic analysis {i} with comprehensive framework application..."

                enhanced_response = bridge.apply_transparency_system(
                    strategic_response, strategic_input, "diego"
                )

        # Measure final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory should not increase excessively
        max_memory_increase = 150  # 150MB max increase

        self.assertLess(memory_increase, max_memory_increase,
                       f"Memory increase too high: {memory_increase:.1f}MB")

        self.performance_results["memory_usage"] = {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": memory_increase,
            "requirement_met": memory_increase < max_memory_increase
        }

    def test_startup_performance(self):
        """Test system startup time performance"""
        import importlib
        import sys

        # Test module import times
        modules_to_test = [
            "integration_protection.cursor_transparency_bridge",
            "mcp.hybrid_installation_manager",
        ]

        import_times = {}

        for module_name in modules_to_test:
            # Clear module from cache if already loaded
            if module_name in sys.modules:
                del sys.modules[module_name]

            start_time = time.time()
            try:
                importlib.import_module(module_name)
                import_duration = time.time() - start_time
                import_times[module_name] = import_duration

                # Each module should import quickly
                self.assertLess(import_duration, 1.0,
                               f"Module {module_name} import too slow: {import_duration:.3f}s")

            except ImportError:
                # Module not available - record as 0 time
                import_times[module_name] = 0.0

        total_import_time = sum(import_times.values())

        # Total startup should be fast
        self.assertLess(total_import_time, 2.0,
                       f"Total import time too slow: {total_import_time:.3f}s")

        self.performance_results["startup"] = {
            "import_times": import_times,
            "total_import_time": total_import_time,
            "requirement_met": total_import_time < 2.0
        }

def run_performance_tests():
    """Run performance requirements tests"""
    print("⚡ PERFORMANCE REQUIREMENTS TESTING")
    print("=" * 60)
    print("Target: <2s dashboard load time, <0.5s API response")
    print("Load testing: 10 concurrent users")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceRequirements)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE TEST SUMMARY")
    print("=" * 60)

    if result.wasSuccessful():
        print("✅ ALL PERFORMANCE REQUIREMENTS MET")
        print("   Response times under limits")
        print("   Concurrent load handled successfully")
        print("   Memory usage within bounds")
        print("   Startup performance optimized")
        return True
    else:
        print("❌ PERFORMANCE REQUIREMENTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")

        # Show specific failures
        for test, traceback in result.failures:
            print(f"   Failed: {test}")

        for test, traceback in result.errors:
            print(f"   Error: {test}")

        return False

if __name__ == "__main__":
    success = run_performance_tests()
    sys.exit(0 if success else 1)
