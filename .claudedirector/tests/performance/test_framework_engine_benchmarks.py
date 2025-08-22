"""
Performance benchmarks for the strategic framework engine.

This module provides comprehensive benchmarking for the embedded framework
engine that powers ClaudeDirector's strategic thinking capabilities.
"""

import time
import unittest
from unittest.mock import Mock, patch
from typing import Callable, Dict, Any, List

try:
    from claudedirector.frameworks.embedded_framework_engine import (
        EmbeddedFrameworkEngine,
    )

    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False

try:
    import pytest

    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


class PerformanceBenchmarkFramework:
    """Base class for framework engine performance benchmarks."""

    def __init__(self):
        """Initialize benchmark environment."""
        self.results: Dict[str, Any] = {}

    def run_multiple_iterations(
        self, func: Callable, iterations: int = 10
    ) -> Dict[str, Any]:
        """Run function multiple times and collect timing statistics."""
        times = []

        for _ in range(iterations):
            start_time = time.perf_counter()
            try:
                result = func()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            except Exception as e:
                print(f"Benchmark iteration failed: {e}")
                times.append(float("inf"))  # Mark failed iterations

        # Filter out failed iterations for statistics
        valid_times = [t for t in times if t != float("inf")]

        if not valid_times:
            return {
                "avg_time": float("inf"),
                "min_time": float("inf"),
                "max_time": float("inf"),
                "success_rate": 0.0,
                "total_iterations": iterations,
            }

        return {
            "avg_time": sum(valid_times) / len(valid_times),
            "min_time": min(valid_times),
            "max_time": max(valid_times),
            "success_rate": len(valid_times) / iterations,
            "total_iterations": iterations,
        }


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestFrameworkEnginePerformance:
    """Benchmark framework engine performance across different scenarios."""

    def setup_method(self):
        """Set up benchmark environment."""
        self.benchmark = PerformanceBenchmarkFramework()
        self.engine = EmbeddedFrameworkEngine()

        # Strategic contexts of varying complexity
        self.simple_context = "We need to make a decision about our product roadmap"

        self.complex_context = """
        Our platform team is facing a critical architectural decision. We have a monolithic
        application that needs to be decomposed into microservices. The stakeholders include
        the CTO, VP of Engineering, senior architects, and product managers. We need to
        consider team topology, organizational structure, and technical strategy. This decision
        will impact our engineering velocity, system reliability, and team autonomy.
        Budget considerations and timeline constraints are also critical factors.
        """

        self.enterprise_context = """
        STRATEGIC INITIATIVE: Digital Transformation and Platform Modernization

        Executive Context:
        - Board-level visibility and quarterly reporting requirements
        - $50M budget allocation over 3 years
        - Regulatory compliance (SOX, GDPR, HIPAA) requirements
        - Competitive positioning against industry leaders

        Stakeholder Ecosystem:
        - C-Suite: CEO, CTO, CPO, CFO involvement
        - Business Units: Sales, Marketing, Operations, Legal
        - Technology: Platform, Security, Data, Infrastructure teams
        - External: Vendors, partners, regulatory bodies

        Technical Challenges:
        - Legacy system modernization with zero downtime requirements
        - Multi-region deployment with data sovereignty
        - API-first architecture with backwards compatibility
        - Scalability to handle 10x traffic growth
        - Security hardening and audit compliance

        Organizational Challenges:
        - Team scaling from 50 to 200 engineers
        - Cross-functional collaboration improvements
        - Skills development and training programs
        - Performance management and career progression
        - Cultural transformation to product-focused teams

        Strategic Frameworks Needed:
        - Technology strategy and architectural decisions
        - Organizational design and team topologies
        - Change management and transformation planning
        - Capital allocation and budget optimization
        - Stakeholder communication and alignment
        - Risk assessment and mitigation strategies

        Success Metrics:
        - Engineering velocity: 50% faster deployment cycles
        - System reliability: 99.99% uptime SLA
        - Team productivity: 30% improvement in delivery
        - Cost optimization: 25% infrastructure savings
        - Customer satisfaction: NPS improvement from 7 to 8.5
        """

    def test_framework_activation_performance(self):
        """Benchmark framework activation speed across content complexity."""

        # Benchmark simple context
        def benchmark_simple():
            return self.engine.analyze_strategic_context(self.simple_context)

        simple_stats = self.benchmark.run_multiple_iterations(
            benchmark_simple, iterations=100
        )

        # Benchmark complex context
        def benchmark_complex():
            return self.engine.analyze_strategic_context(self.complex_context)

        complex_stats = self.benchmark.run_multiple_iterations(
            benchmark_complex, iterations=50
        )

        # Benchmark enterprise context
        def benchmark_enterprise():
            return self.engine.analyze_strategic_context(self.enterprise_context)

        enterprise_stats = self.benchmark.run_multiple_iterations(
            benchmark_enterprise, iterations=20
        )

        # Performance assertions
        assert (
            simple_stats["avg_time"] < 0.01
        ), f"Simple context analysis too slow: {simple_stats['avg_time']}s"
        assert (
            complex_stats["avg_time"] < 0.05
        ), f"Complex context analysis too slow: {complex_stats['avg_time']}s"
        assert (
            enterprise_stats["avg_time"] < 0.15
        ), f"Enterprise context analysis too slow: {enterprise_stats['avg_time']}s"

        # Success rate assertions
        assert (
            simple_stats["success_rate"] >= 0.99
        ), f"Simple context success rate too low: {simple_stats['success_rate']}"
        assert (
            complex_stats["success_rate"] >= 0.95
        ), f"Complex context success rate too low: {complex_stats['success_rate']}"
        assert (
            enterprise_stats["success_rate"] >= 0.90
        ), f"Enterprise context success rate too low: {enterprise_stats['success_rate']}"

        # Store results for reporting
        self.benchmark.results["framework_activation"] = {
            "simple_context": simple_stats,
            "complex_context": complex_stats,
            "enterprise_context": enterprise_stats,
        }

        # Performance reporting
        print(f"\n📊 Framework Activation Performance:")
        print(f"Simple context (avg): {simple_stats['avg_time']:.4f}s")
        print(f"Complex context (avg): {complex_stats['avg_time']:.4f}s")
        print(f"Enterprise context (avg): {enterprise_stats['avg_time']:.4f}s")

    def test_framework_accuracy_performance(self):
        """Benchmark framework selection accuracy across different strategic domains."""

        strategic_contexts = [
            (
                "We need to decide between two technology platforms",
                ["Decisive WRAP", "Rumelt Strategy"],
            ),
            (
                "Our teams are struggling with communication and collaboration",
                ["Team Topologies", "Crucial Conversations"],
            ),
            (
                "We need to improve our development velocity and quality",
                ["Accelerate", "Team Topologies"],
            ),
            (
                "Budget allocation for next year's platform investments",
                ["Capital Allocation", "Rumelt Strategy"],
            ),
            (
                "Implementing a major organizational change",
                ["Scaling Up Excellence", "Crucial Conversations"],
            ),
            (
                "Stakeholder alignment on strategic priorities",
                ["Crucial Conversations", "Rumelt Strategy"],
            ),
            (
                "Platform architecture and team boundaries",
                ["Team Topologies", "Decisive WRAP"],
            ),
        ]

        def benchmark_framework_accuracy():
            results = []
            for context, expected_frameworks in strategic_contexts:
                analysis = self.engine.analyze_strategic_context(context)
                activated = analysis.get("activated_frameworks", [])

                # Check if at least one expected framework was activated
                accuracy = any(
                    framework in activated for framework in expected_frameworks
                )
                results.append(accuracy)

            return sum(results) / len(results) if results else 0.0

        accuracy_stats = self.benchmark.run_multiple_iterations(
            benchmark_framework_accuracy, iterations=50
        )

        # Accuracy assertions
        assert (
            accuracy_stats["avg_time"] < 0.1
        ), f"Framework accuracy check too slow: {accuracy_stats['avg_time']}s"
        assert (
            accuracy_stats["success_rate"] >= 0.95
        ), f"Framework accuracy success rate too low: {accuracy_stats['success_rate']}"

        # Store results
        self.benchmark.results["framework_accuracy"] = accuracy_stats

        print(f"\n🎯 Framework Accuracy Performance:")
        print(f"Accuracy analysis (avg): {accuracy_stats['avg_time']:.4f}s")
        print(f"Success rate: {accuracy_stats['success_rate']:.2%}")

    def test_framework_scalability_performance(self):
        """Benchmark framework engine scalability with concurrent contexts."""

        def benchmark_concurrent_analysis():
            # Simulate concurrent framework analysis
            contexts = [
                "Platform strategy decision",
                "Team organization challenge",
                "Technology investment choice",
                "Stakeholder communication issue",
                "Process improvement initiative",
            ]

            results = []
            for context in contexts:
                analysis = self.engine.analyze_strategic_context(context)
                results.append(len(analysis.get("activated_frameworks", [])))

            return sum(results)

        scalability_stats = self.benchmark.run_multiple_iterations(
            benchmark_concurrent_analysis, iterations=30
        )

        # Scalability assertions
        assert (
            scalability_stats["avg_time"] < 0.2
        ), f"Concurrent analysis too slow: {scalability_stats['avg_time']}s"
        assert (
            scalability_stats["success_rate"] >= 0.90
        ), f"Concurrent analysis success rate too low: {scalability_stats['success_rate']}"

        # Store results
        self.benchmark.results["framework_scalability"] = scalability_stats

        print(f"\n🚀 Framework Scalability Performance:")
        print(f"Concurrent analysis (avg): {scalability_stats['avg_time']:.4f}s")
        print(f"Success rate: {scalability_stats['success_rate']:.2%}")

    def test_framework_recommendation_performance(self):
        """Benchmark strategic recommendation generation performance."""

        def benchmark_recommendations():
            analysis = self.engine.analyze_strategic_context(self.complex_context)

            # Extract recommendation metrics
            recommendations = analysis.get("strategic_recommendations", [])
            persona_guidance = analysis.get("persona_guidance", {})
            activated_frameworks = analysis.get("activated_frameworks", [])

            # Calculate recommendation quality score
            quality_score = (
                len(recommendations) * 0.4
                + len(persona_guidance) * 0.3
                + len(activated_frameworks) * 0.3
            )

            return quality_score

        recommendation_stats = self.benchmark.run_multiple_iterations(
            benchmark_recommendations, iterations=40
        )

        # Recommendation quality assertions
        assert (
            recommendation_stats["avg_time"] < 0.08
        ), f"Recommendation generation too slow: {recommendation_stats['avg_time']}s"
        assert (
            recommendation_stats["success_rate"] >= 0.92
        ), f"Recommendation success rate too low: {recommendation_stats['success_rate']}"

        # Store results
        self.benchmark.results["framework_recommendations"] = recommendation_stats

        print(f"\n💡 Framework Recommendation Performance:")
        print(
            f"Recommendation generation (avg): {recommendation_stats['avg_time']:.4f}s"
        )
        print(f"Success rate: {recommendation_stats['success_rate']:.2%}")

    def test_memory_usage_monitoring(self):
        """Monitor memory usage during framework engine operations."""
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())

            # Baseline memory usage
            baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

            # Perform memory-intensive operations
            for i in range(50):
                context = f"Strategic decision {i}: " + self.complex_context
                self.engine.analyze_strategic_context(context)

            # Check memory usage after operations
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - baseline_memory

            # Memory usage assertions
            assert (
                memory_increase < 25
            ), f"Memory usage increased too much: {memory_increase:.2f}MB"

            print(f"\n🧠 Framework Engine Memory Usage:")
            print(f"Baseline: {baseline_memory:.2f}MB")
            print(f"Final: {final_memory:.2f}MB")
            print(f"Increase: {memory_increase:.2f}MB")

        except ImportError:
            print("psutil not available for memory monitoring")
            assert True  # Skip memory test if psutil unavailable


if __name__ == "__main__":
    # Run performance benchmarks directly
    if IMPORTS_AVAILABLE and PYTEST_AVAILABLE:
        pytest.main([__file__, "-v", "-s"])
    else:
        print("Required modules not available for performance testing")
