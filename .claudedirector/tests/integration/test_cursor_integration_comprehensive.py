#!/usr/bin/env python3
"""
Cursor Test Runner for ClaudeDirector MCP Integration
Consolidated test execution combining manual verification and programmatic validation.
"""

import asyncio
import time
import sys
from pathlib import Path

# Add the lib directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "lib"))


def print_header(title: str):
    """Print formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"🧪 {title}")
    print("=" * 60)


def print_test_case(name: str, input_text: str, expected: list):
    """Print formatted test case"""
    print(f"\n### Test Case: {name}")
    print("**Input:**")
    print(f"```\n{input_text}\n```")
    print("**Expected:**")
    for i, expectation in enumerate(expected, 1):
        print(f"{i}. {expectation}")
    print()


class CursorTestRunner:
    """Test runner for ClaudeDirector in Cursor IDE"""

    def __init__(self):
        self.manual_tests_passed = 0
        self.programmatic_tests_passed = 0
        self.total_tests = 0

    def run_manual_integration_tests(self):
        """Display manual integration tests for Cursor verification"""
        print_header("MANUAL INTEGRATION TESTS")
        print("Copy each test case into Cursor and verify expected behavior:")

        test_cases = [
            {
                "name": "Complex Organizational Question",
                "input": """We're planning a major organizational transformation to scale our platform capabilities across multiple international markets. This involves restructuring our engineering teams, implementing new governance frameworks, and coordinating with executive stakeholders.

How should we approach this systematically?""",
                "expected": [
                    "🎯 Diego | Engineering Leadership",
                    "🔧 Accessing MCP Server: sequential (systematic_analysis)",
                    "*Analyzing your organizational challenge using systematic frameworks...*",
                    "Diego's authentic personality: 'Great to connect! Before we dive in, let me stress-test this thinking...'",
                    "📚 Strategic Framework: [Framework Name] detected",
                ],
            },
            {
                "name": "Design System Strategy",
                "input": "How do we scale our design system across multiple product teams globally while maintaining consistency and accessibility compliance?",
                "expected": [
                    "🎨 Rachel | Design Systems Strategy",
                    "🔧 Accessing MCP Server: magic (diagram_generation) OR context7 (pattern_access)",
                    "Framework: Design System Maturity Model OR User-Centered Design",
                ],
            },
            {
                "name": "Executive Communication",
                "input": "I need to present our platform strategy to the VP of Engineering next week. What should I focus on?",
                "expected": [
                    "📊 Camille | Strategic Technology",
                    "🔧 Accessing MCP Server: sequential (business_modeling)",
                    "Framework: Strategic Analysis Framework OR Good Strategy Bad Strategy",
                ],
            },
        ]

        for test_case in test_cases:
            print_test_case(
                test_case["name"], test_case["input"], test_case["expected"]
            )

        print("### ✅ Verification Checklist:")
        checklist_items = [
            "Persona header appears with emoji and domain",
            "MCP enhancement disclosure shows when complexity is high",
            "Framework attribution appears when frameworks are detected",
            "Persona personality is authentic and consistent",
            "Strategic guidance is actionable and valuable",
            "Response feels natural despite transparency",
        ]

        for item in checklist_items:
            print(f"- [ ] {item}")

        print("\n🎯 **Run these tests in Cursor first to verify basic functionality!**")

    async def run_programmatic_tests(self):
        """Run programmatic tests to validate components"""
        print_header("PROGRAMMATIC COMPONENT TESTS")

        tests_to_run = [
            ("Configuration Loading", self.test_configuration_loading),
            ("Framework Detection", self.test_framework_detection),
            ("Complexity Analysis", self.test_complexity_analysis),
            ("Transparency Engine", self.test_transparency_engine),
        ]

        for test_name, test_func in tests_to_run:
            try:
                print(f"\n🔄 Running: {test_name}")
                start_time = time.time()

                if asyncio.iscoroutinefunction(test_func):
                    await test_func()
                else:
                    test_func()

                duration = time.time() - start_time
                print(f"✅ {test_name} - PASSED ({duration:.3f}s)")
                self.programmatic_tests_passed += 1

            except Exception as e:
                print(f"❌ {test_name} - FAILED: {e}")

            self.total_tests += 1

    def test_configuration_loading(self):
        """Test basic configuration and imports"""
        # Test imports
        try:
            from claudedirector.core.mcp_client import MCPClient
            from claudedirector.frameworks.framework_detector import FrameworkDetector
            from claudedirector.core.complexity_analyzer import ComplexityAnalyzer

            print("  ✓ All core modules imported successfully")
        except ImportError as e:
            raise Exception(f"Failed to import core modules: {e}")

        # Test basic initialization
        try:
            MCPClient()
            FrameworkDetector()
            ComplexityAnalyzer()
            print("  ✓ All components initialize successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize components: {e}")

        print("  ✓ Configuration loading test completed")

    def test_framework_detection(self):
        """Test framework detection functionality"""
        try:
            from claudedirector.frameworks.framework_detector import FrameworkDetector

            detector = FrameworkDetector()

            # Test basic detection
            test_cases = [
                (
                    "We should use Team Topologies for our team structure",
                    "Team Topologies",
                ),
                ("Apply the WRAP framework for this decision", "WRAP Framework"),
                ("Our strategy needs a clear kernel", "Good Strategy Bad Strategy"),
            ]

            successful_detections = 0
            for test_content, expected_framework in test_cases:
                results = detector.detect_frameworks(test_content, {"persona": "diego"})
                detected_names = [r.framework.name for r in results]

                if expected_framework in detected_names:
                    successful_detections += 1
                    print(f"  ✓ Detected {expected_framework}")
                else:
                    print(f"  ⚠ Missed {expected_framework} in: {test_content[:50]}...")

            accuracy = successful_detections / len(test_cases)
            if accuracy >= 0.6:  # 60% minimum for basic functionality
                print(f"  ✓ Framework detection accuracy: {accuracy:.1%}")
            else:
                raise Exception(f"Framework detection accuracy too low: {accuracy:.1%}")

        except ImportError:
            print("  ⚠ Framework detection not available (optional)")

    def test_complexity_analysis(self):
        """Test complexity analysis functionality"""
        try:
            from claudedirector.core.complexity_analyzer import (
                ComplexityAnalyzer,
                ComplexityLevel,
            )

            analyzer = ComplexityAnalyzer()

            # Test complexity scoring
            test_cases = [
                ("What is Team Topologies?", ComplexityLevel.LOW),
                ("How should we improve our design system?", ComplexityLevel.MEDIUM),
                (
                    "How should we restructure our engineering teams for scalability while maintaining design system consistency across multiple international product teams?",
                    ComplexityLevel.HIGH,
                ),
            ]

            correct_classifications = 0
            for test_input, expected_level in test_cases:
                result = analyzer.analyze_complexity(test_input)
                if result.complexity_level == expected_level:
                    correct_classifications += 1
                    print(f"  ✓ Correctly classified as {expected_level.value}")
                else:
                    print(
                        f"  ⚠ Misclassified: expected {expected_level.value}, got {result.complexity_level.value}"
                    )

            accuracy = correct_classifications / len(test_cases)
            if accuracy >= 0.6:
                print(f"  ✓ Complexity analysis accuracy: {accuracy:.1%}")
            else:
                raise Exception(f"Complexity analysis accuracy too low: {accuracy:.1%}")

        except ImportError as e:
            raise Exception(f"Complexity analyzer not available: {e}")

    def test_transparency_engine(self):
        """Test transparency engine functionality"""
        try:
            from claudedirector.transparency.transparency_engine import (
                TransparencyEngine,
            )

            engine = TransparencyEngine()

            # Test persona disclosure
            persona_disclosure = engine.generate_persona_disclosure(
                "diego", "Engineering Leadership"
            )
            if "🎯 Diego | Engineering Leadership" in persona_disclosure:
                print("  ✓ Persona disclosure generation working")
            else:
                raise Exception("Persona disclosure format incorrect")

            # Test MCP disclosure
            mcp_disclosure = engine.create_mcp_enhancement_disclosure(
                server_name="sequential",
                capability="systematic_analysis",
                persona="diego",
                processing_message="Test analysis",
            )

            start_disclosure = mcp_disclosure.get_start_disclosure()
            if "🔧 Accessing MCP Server: sequential" in start_disclosure:
                print("  ✓ MCP disclosure generation working")
            else:
                raise Exception("MCP disclosure format incorrect")

        except ImportError as e:
            raise Exception(f"Transparency engine not available: {e}")

    def print_summary(self):
        """Print test execution summary"""
        print_header("TEST EXECUTION SUMMARY")

        total_programmatic = self.total_tests
        success_rate = (
            (self.programmatic_tests_passed / total_programmatic * 100)
            if total_programmatic > 0
            else 0
        )

        print(
            f"📊 Programmatic Tests: {self.programmatic_tests_passed}/{total_programmatic} passed ({success_rate:.1f}%)"
        )

        if success_rate >= 75:
            status = "🎉 EXCELLENT"
            message = "System ready for production use in Cursor!"
        elif success_rate >= 50:
            status = "✅ GOOD"
            message = "System functional with minor issues to address"
        else:
            status = "⚠️ ATTENTION NEEDED"
            message = "Critical issues require resolution"

        print(f"\n{status}: {message}")

        print(f"\n🎯 Next Steps:")
        print(f"1. Run the Manual Integration Tests in Cursor")
        print(f"2. Verify all checklist items pass")
        print(f"3. System ready for strategic leadership use")


async def main():
    """Main test execution"""
    print_header("CLAUDEDIRECTOR CURSOR TEST SUITE")
    print(
        "Consolidated test suite combining manual verification and programmatic validation"
    )

    runner = CursorTestRunner()

    # Run manual integration instructions
    runner.run_manual_integration_tests()

    # Run programmatic tests
    await runner.run_programmatic_tests()

    # Print summary
    runner.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
