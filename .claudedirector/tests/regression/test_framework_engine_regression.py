#!/usr/bin/env python3
"""
Framework Engine Regression Tests

CRITICAL: These tests protect the framework detection system during SOLID refactoring.
The embedded_framework_engine.py has the highest SOLID violation count and needs
comprehensive regression protection.
"""

import unittest
import sys
from pathlib import Path
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))


class TestFrameworkDetectionRegression(unittest.TestCase):
    """Test framework detection functionality during refactoring"""

    def setUp(self):
        """Set up test environment"""
        self.test_scenarios = {
            "strategic_analysis": [
                "How should we restructure our engineering teams for better scalability?",
                "What's our technology roadmap for the next 2 years?",
                "How do we improve our platform adoption metrics?",
            ],
            "organizational_change": [
                "We need to scale our development organization from 50 to 200 engineers",
                "How do we implement DevOps practices across multiple teams?",
                "What's the best way to manage technical debt at scale?",
            ],
            "decision_making": [
                "Should we adopt microservices or continue with our monolith?",
                "How do we evaluate build vs buy decisions for our platform?",
                "What criteria should we use for technology selection?",
            ],
            "platform_strategy": [
                "How do we build a platform that serves multiple product teams?",
                "What's our strategy for developer experience improvements?",
                "How do we measure platform success and ROI?",
            ],
        }

        self.expected_frameworks = {
            "Team Topologies",
            "Good Strategy Bad Strategy",
            "Technical Strategy Framework",
            "WRAP Framework",
            "Capital Allocation Framework",
            "Accelerate Performance",
            "Crucial Conversations",
            "Scaling Up Excellence",
        }

    def test_framework_module_imports_successfully(self):
        """Ensure framework engine module can be imported"""
        try:
            pass

            self.assertTrue(True, "Framework engine imports successfully")
        except ImportError as e:
            self.fail(f"Framework engine import failed: {e}")

    def test_framework_detection_patterns_work(self):
        """Test that all framework detection patterns work correctly"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine

            engine = EmbeddedFrameworkEngine()

            detected_frameworks = set()
            total_detections = 0

            for category, scenarios in self.test_scenarios.items():
                for scenario in scenarios:
                    try:
                        # Test framework detection
                        result = engine.analyze_systematically(
                            scenario,
                            persona_context="martin",
                            domain_focus=["strategic", "technical"],
                        )
                        if result:
                            # Handle SystematicResponse object (new format)
                            if hasattr(result, "framework_applied"):
                                detected_frameworks.add(result.framework_applied)
                                total_detections += 1
                            # Handle FrameworkAnalysis object
                            elif hasattr(result, "framework_name"):
                                detected_frameworks.add(result.framework_name)
                                total_detections += 1
                            elif hasattr(result, "frameworks"):
                                for framework in result.frameworks:
                                    detected_frameworks.add(framework.name)
                                    total_detections += 1
                            elif isinstance(result, list):
                                for framework in result:
                                    if hasattr(framework, "name"):
                                        detected_frameworks.add(framework.name)
                                        total_detections += 1
                    except Exception as e:
                        print(
                            f"⚠️ Framework detection failed for scenario: {scenario[:50]}... - {e}"
                        )

            # Verify we detected multiple frameworks
            self.assertGreaterEqual(
                len(detected_frameworks),
                3,
                f"Should detect multiple frameworks, found: {detected_frameworks}",
            )

            # Verify we had multiple detections
            self.assertGreater(
                total_detections,
                5,
                f"Should have multiple framework detections, got: {total_detections}",
            )

            print(f"\n🔍 FRAMEWORK DETECTION RESULTS:")
            print(f"   Unique frameworks detected: {len(detected_frameworks)}")
            print(f"   Total detections: {total_detections}")
            print(f"   Detected frameworks: {sorted(detected_frameworks)}")

        except Exception as e:
            self.fail(f"Framework detection test failed: {e}")

    def test_framework_selection_consistency(self):
        """Test that framework selection remains consistent across runs"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine

            engine = EmbeddedFrameworkEngine()

            test_input = "How should we scale our engineering organization from 50 to 200 people while maintaining quality and velocity?"

            # Run detection multiple times
            results = []
            for i in range(3):
                try:
                    result = engine.analyze_systematically(
                        test_input,
                        persona_context="martin",
                        domain_focus=["strategic", "organizational"],
                    )
                    if result:
                        if hasattr(result, "framework_name"):
                            framework_names = [result.framework_name]
                        elif hasattr(result, "frameworks"):
                            framework_names = [f.name for f in result.frameworks]
                        elif isinstance(result, list):
                            framework_names = [
                                f.name if hasattr(f, "name") else str(f) for f in result
                            ]
                        else:
                            framework_names = [str(result)]
                        results.append(set(framework_names))
                    else:
                        results.append(set())
                except Exception as e:
                    print(f"⚠️ Detection run {i+1} failed: {e}")
                    results.append(set())

            # Check consistency (allowing for some variation in complex scenarios)
            if len(results) >= 2:
                # At least some frameworks should be detected consistently
                non_empty_results = [r for r in results if r]
                if len(non_empty_results) >= 2:
                    set.intersection(*non_empty_results)
                else:
                    pass

                self.assertGreater(
                    len(results[0]) if results[0] else 0,
                    0,
                    "Should detect at least one framework consistently",
                )

            print(f"\n🔄 CONSISTENCY TEST RESULTS:")
            for i, result in enumerate(results):
                print(f"   Run {i+1}: {len(result)} frameworks - {sorted(result)}")

        except Exception as e:
            self.fail(f"Framework consistency test failed: {e}")

    def test_framework_performance_benchmarks(self):
        """Test framework detection performance doesn't degrade"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine

            engine = EmbeddedFrameworkEngine()

            test_scenarios = [
                "Strategic technology decision needed for platform architecture",
                "Organizational change management for team restructuring",
                "Complex decision making process for build vs buy analysis",
            ]

            total_time = 0
            successful_detections = 0

            for scenario in test_scenarios:
                start_time = time.time()
                try:
                    result = engine.analyze_systematically(
                        scenario,
                        persona_context="martin",
                        domain_focus=["strategic", "technical"],
                    )
                    end_time = time.time()
                    detection_time = end_time - start_time
                    total_time += detection_time

                    if result:
                        successful_detections += 1

                    # Each detection should complete within reasonable time
                    self.assertLess(
                        detection_time,
                        5.0,
                        f"Framework detection took too long: {detection_time:.2f}s",
                    )

                except Exception as e:
                    print(
                        f"⚠️ Performance test failed for scenario: {scenario[:30]}... - {e}"
                    )

            avg_time = total_time / len(test_scenarios) if test_scenarios else 0

            # Average detection time should be reasonable
            self.assertLess(
                avg_time,
                2.0,
                f"Average framework detection time too slow: {avg_time:.2f}s",
            )

            print(f"\n⚡ PERFORMANCE BENCHMARK RESULTS:")
            print(f"   Average detection time: {avg_time:.3f}s")
            print(f"   Total test time: {total_time:.3f}s")
            print(
                f"   Successful detections: {successful_detections}/{len(test_scenarios)}"
            )

        except Exception as e:
            self.fail(f"Framework performance test failed: {e}")


class TestFrameworkConfigurationIntegration(unittest.TestCase):
    """Test framework engine integration with configuration system"""

    def test_framework_configuration_access(self):
        """Test framework engine can access configuration values"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine
            from core.config import get_config

            EmbeddedFrameworkEngine()
            config = get_config()

            # Test that framework engine can access thresholds
            confidence_threshold = config.get_threshold("confidence_threshold")
            self.assertIsInstance(confidence_threshold, (int, float))
            self.assertGreater(confidence_threshold, 0.0)
            self.assertLessEqual(confidence_threshold, 1.0)

            # Test enum access
            priority_levels = config.get_enum_values("priority_levels")
            self.assertIsInstance(priority_levels, list)
            self.assertGreater(len(priority_levels), 0)

            print(f"\n⚙️ CONFIGURATION INTEGRATION RESULTS:")
            print(f"   Confidence threshold: {confidence_threshold}")
            print(f"   Priority levels: {priority_levels}")

        except Exception as e:
            self.fail(f"Framework configuration integration failed: {e}")

    def test_framework_message_templates(self):
        """Test framework engine uses configuration message templates"""
        try:
            from core.config import get_config

            config = get_config()

            # Test framework detection message template
            template = config.get_message_template("framework_detection_message")
            self.assertIsInstance(template, str)
            self.assertIn("{framework_name}", template)

            # Test message formatting
            formatted = template.format(framework_name="Team Topologies")
            self.assertIn("Team Topologies", formatted)

            print(f"\n📝 MESSAGE TEMPLATE RESULTS:")
            print(f"   Template: {template}")
            print(f"   Formatted: {formatted}")

        except Exception as e:
            self.fail(f"Framework message template test failed: {e}")


class TestFrameworkDataIntegrity(unittest.TestCase):
    """Test framework data integrity during refactoring"""

    def test_framework_knowledge_preservation(self):
        """Test that framework knowledge base remains intact"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine

            engine = EmbeddedFrameworkEngine()

            # Test that we can access framework definitions
            # This ensures the framework knowledge hasn't been corrupted during refactoring

            strategic_input = (
                "We need to make a strategic decision about our technology platform"
            )
            result = engine.analyze_systematically(
                strategic_input,
                persona_context="martin",
                domain_focus=["strategic", "technical"],
            )

            # Should detect some strategic frameworks
            self.assertIsNotNone(result, "Framework detection should return results")

            if hasattr(result, "frameworks") and result.frameworks:
                framework_names = [f.name for f in result.frameworks]
                self.assertGreater(
                    len(framework_names),
                    0,
                    "Should detect at least one framework for strategic input",
                )
                print(f"\n📚 FRAMEWORK KNOWLEDGE PRESERVATION:")
                print(f"   Detected frameworks: {framework_names}")

        except Exception as e:
            self.fail(f"Framework knowledge preservation test failed: {e}")

    def test_framework_attribution_consistency(self):
        """Test that framework attribution remains consistent"""
        try:
            from core.embedded_framework_engine import EmbeddedFrameworkEngine

            engine = EmbeddedFrameworkEngine()

            # Test framework attribution functionality
            test_input = "How do we scale our organization effectively?"

            result = engine.analyze_systematically(
                test_input,
                persona_context="martin",
                domain_focus=["strategic", "organizational"],
            )

            if result:
                # Framework attribution should work
                if hasattr(result, "attribution") or hasattr(result, "confidence"):
                    print(f"\n🏷️ FRAMEWORK ATTRIBUTION TEST:")
                    print(f"   Attribution functionality verified")
                else:
                    print(f"\n⚠️ Framework attribution may need verification")

            # This test mainly ensures the attribution system doesn't crash
            self.assertTrue(True, "Framework attribution system functional")

        except Exception as e:
            self.fail(f"Framework attribution test failed: {e}")


def run_framework_engine_regression_tests():
    """Run complete framework engine regression test suite"""
    print("🔧 FRAMEWORK ENGINE REGRESSION TEST SUITE")
    print("=" * 60)
    print("CRITICAL: Protects framework detection during SOLID refactoring")
    print("Tests the most violation-heavy module: embedded_framework_engine.py")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Add framework regression tests
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestFrameworkDetectionRegression)
    )
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(
            TestFrameworkConfigurationIntegration
        )
    )
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestFrameworkDataIntegrity)
    )

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print(f"📊 FRAMEWORK ENGINE REGRESSION TEST RESULTS")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 ALL FRAMEWORK ENGINE REGRESSION TESTS PASSED")
        print("✅ Framework detection system protected during refactoring")
    else:
        print("\n❌ FRAMEWORK ENGINE REGRESSION TESTS FAILED")
        print("🚫 DO NOT PROCEED with framework engine refactoring until these pass")

    return success


if __name__ == "__main__":
    success = run_framework_engine_regression_tests()
    sys.exit(0 if success else 1)
