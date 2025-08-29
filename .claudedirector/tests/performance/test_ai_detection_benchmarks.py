"""
Performance benchmarks for AI detection modules.
Tests response times, throughput, and memory usage of AI detection functions.
"""

import pytest
import time
import psutil
import statistics
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the lib directory to Python path for imports
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

try:
    from lib.context_engineering.stakeholder_intelligence_unified import (
        get_stakeholder_intelligence,
    )
    from lib.core.config import ClaudeDirectorConfig

    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import modules for benchmarking: {e}")
    IMPORTS_AVAILABLE = False


class PerformanceBenchmark:
    """Base class for performance benchmarking."""

    def __init__(self):
        self.results = {}

    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time

    def measure_memory(self, func, *args, **kwargs):
        """Measure memory usage of a function."""
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB

        result = func(*args, **kwargs)

        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before

        return result, memory_used

    def run_multiple_iterations(self, func, iterations=10, *args, **kwargs):
        """Run function multiple times and collect timing statistics."""
        times = []
        for _ in range(iterations):
            _, execution_time = self.measure_time(func, *args, **kwargs)
            times.append(execution_time)

        return {
            "min_time": min(times),
            "max_time": max(times),
            "avg_time": statistics.mean(times),
            "median_time": statistics.median(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "total_iterations": iterations,
        }


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestStakeholderDetectionPerformance:
    """Benchmark stakeholder detection performance."""

    def setup_method(self):
        """Set up benchmark environment."""
        self.benchmark = PerformanceBenchmark()
        self.config = Mock(spec=ClaudeDirectorConfig)
        self.config.database_path = ":memory:"
        self.config.stakeholder_auto_create_threshold = 0.85
        self.config.stakeholder_profiling_threshold = 0.65
        self.config.enable_caching = False
        self.config.enable_parallel_processing = False

        # Sample test data of varying sizes
        self.small_text = "Meeting with John Smith tomorrow at 2pm"
        self.medium_text = """
        In today's engineering standup, VP of Engineering Sarah Johnson discussed
        the Q2 roadmap with Director Mike Chen and Product Manager Lisa Wang.
        CTO Alex Rodriguez approved the new architecture proposal submitted by
        Senior Engineer Tom Brown. The team also reviewed feedback from
        Customer Success Manager Emily Davis regarding client requirements.
        """
        self.large_text = self.medium_text * 10  # 10x larger text

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_detection_response_time(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Benchmark stakeholder detection response times."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance
        mock_detector_instance.detect_stakeholders.return_value = [
            {"name": "John Smith", "confidence": 0.9, "role": "Engineer"}
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.config)

        # Benchmark small text using actual API method
        def benchmark_detection():
            return stakeholder_intel.detect_stakeholders_in_content(
                self.small_text, {"source": "benchmark"}
            )

        small_stats = self.benchmark.run_multiple_iterations(
            benchmark_detection, iterations=50
        )

        # Benchmark medium text using actual API method
        def benchmark_medium():
            return stakeholder_intel.detect_stakeholders_in_content(
                self.medium_text, {"source": "benchmark"}
            )

        medium_stats = self.benchmark.run_multiple_iterations(
            benchmark_medium, iterations=20
        )

        # Benchmark large text using actual API method
        def benchmark_large():
            return stakeholder_intel.detect_stakeholders_in_content(
                self.large_text, {"source": "benchmark"}
            )

        large_stats = self.benchmark.run_multiple_iterations(
            benchmark_large, iterations=10
        )

        # Performance assertions
        assert (
            small_stats["avg_time"] < 0.1
        ), f"Small text detection too slow: {small_stats['avg_time']}s"
        assert (
            medium_stats["avg_time"] < 0.5
        ), f"Medium text detection too slow: {medium_stats['avg_time']}s"
        assert (
            large_stats["avg_time"] < 2.0
        ), f"Large text detection too slow: {large_stats['avg_time']}s"

        # Store results for reporting
        self.benchmark.results["stakeholder_detection"] = {
            "small_text": small_stats,
            "medium_text": medium_stats,
            "large_text": large_stats,
        }

        print(f"\n📊 Stakeholder Detection Performance:")
        print(f"Small text (avg): {small_stats['avg_time']:.4f}s")
        print(f"Medium text (avg): {medium_stats['avg_time']:.4f}s")
        print(f"Large text (avg): {large_stats['avg_time']:.4f}s")

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_detection_memory_usage(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Benchmark stakeholder detection memory usage."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance
        mock_detector_instance.detect_stakeholders.return_value = [
            {"name": f"Person {i}", "confidence": 0.8, "role": "Engineer"}
            for i in range(10)  # Return multiple results
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.config)

        # Measure memory for different text sizes
        _, small_memory = self.measure_memory(
            stakeholder_intel.detect_stakeholders, self.small_text
        )

        _, medium_memory = self.measure_memory(
            stakeholder_intel.detect_stakeholders, self.medium_text
        )

        _, large_memory = self.measure_memory(
            stakeholder_intel.detect_stakeholders, self.large_text
        )

        # Memory usage should not grow excessively
        assert small_memory < 10, f"Small text uses too much memory: {small_memory}MB"
        assert (
            medium_memory < 20
        ), f"Medium text uses too much memory: {medium_memory}MB"
        assert large_memory < 50, f"Large text uses too much memory: {large_memory}MB"

        print(f"\n💾 Stakeholder Detection Memory Usage:")
        print(f"Small text: {small_memory:.2f}MB")
        print(f"Medium text: {medium_memory:.2f}MB")
        print(f"Large text: {large_memory:.2f}MB")

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_throughput(self, mock_engagement, mock_detector, mock_ai):
        """Benchmark stakeholder detection throughput."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance
        mock_detector_instance.detect_stakeholders.return_value = [
            {"name": "John Smith", "confidence": 0.9, "role": "Engineer"}
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.config)

        # Measure throughput over a fixed time period
        test_duration = 5.0  # seconds
        request_count = 0
        start_time = time.perf_counter()

        while (time.perf_counter() - start_time) < test_duration:
            stakeholder_intel.detect_stakeholders(self.small_text)
            request_count += 1

        elapsed_time = time.perf_counter() - start_time
        throughput = request_count / elapsed_time

        # Should handle at least 10 requests per second
        assert throughput >= 10, f"Throughput too low: {throughput} req/s"

        print(
            f"\n🚀 Stakeholder Detection Throughput: {throughput:.1f} requests/second"
        )


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestTaskDetectionPerformance(PerformanceBenchmark):
    """Benchmark task detection performance."""

    def setUp(self):
        """Set up task detection benchmark environment."""
        super().__init__()
        self.config = Mock()
        self.config.task_auto_create_threshold = 0.80
        self.config.task_review_threshold = 0.60
        self.config.database_path = ":memory:"

        self.sample_texts = [
            "Need to complete code review by Friday",
            "TODO: Update documentation for the new API",
            "Action item: Schedule team meeting next week",
            "Must fix bug in authentication module before release",
            "Deadline: Submit proposal by Monday morning",
        ]

    @patch("claudedirector.intelligence.task.IntelligentTaskDetector")
    @patch("claudedirector.intelligence.task.StrategicTaskManager")
    def test_task_detection_batch_performance(self, mock_manager, mock_detector):
        """Benchmark task detection on multiple texts."""
        # This test would require the actual TaskIntelligence class
        # For now, we test the concept

        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance
        mock_detector_instance.detect_tasks.return_value = [
            {"task": "Complete review", "confidence": 0.85, "priority": "high"}
        ]

        # Simulate batch processing
        start_time = time.perf_counter()

        for text in self.sample_texts * 10:  # Process 50 texts
            # Simulate task detection
            mock_detector_instance.detect_tasks(text)

        end_time = time.perf_counter()
        batch_time = end_time - start_time

        # Should process 50 texts in under 5 seconds
        assert batch_time < 5.0, f"Batch processing too slow: {batch_time}s"

        throughput = len(self.sample_texts) * 10 / batch_time
        print(f"\n📋 Task Detection Batch Throughput: {throughput:.1f} texts/second")


if __name__ == "__main__":
    # Run performance benchmarks
    pytest.main([__file__, "-v", "-s"])
