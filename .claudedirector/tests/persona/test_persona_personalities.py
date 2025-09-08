#!/usr/bin/env python3
"""
Persona Personality Preservation Tests
Validates that persona personalities, challenge patterns, and strategic pushback remain intact.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestPersonaPersonalities(unittest.TestCase):
    """Test that persona personalities are preserved during cleanup"""

    def setUp(self):
        """Set up test environment"""
        self.cursorrules_file = PROJECT_ROOT / ".cursorrules"
        self.transparency_bridge_file = (
            PROJECT_ROOT
            / ".claudedirector/integration-protection/cursor_transparency_bridge.py"
        )

    def test_cursorrules_persona_headers_preserved(self):
        """Verify persona headers remain in .cursorrules"""
        self.assertTrue(self.cursorrules_file.exists(), ".cursorrules file must exist")

        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        # Test all top 5 persona headers are preserved
        expected_headers = [
            "🎯 Diego | Engineering Leadership",
            "📊 Camille | Strategic Technology",
            "🎨 Rachel | Design Systems Strategy",
            "💼 Alvaro | Platform Investment Strategy",
            "🏗️ Martin | Platform Architecture",
        ]

        for header in expected_headers:
            with self.subTest(header=header):
                self.assertIn(
                    header,
                    content,
                    f"Persona header '{header}' must be preserved in .cursorrules",
                )

    def test_diego_challenge_patterns_preserved(self):
        """Test Diego's engineering leadership challenge patterns"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        # Diego should maintain stress-testing and assumption challenging
        diego_patterns = [
            "stress-test",
            "first principles",
            "assumptions",
            "organizational leverage",
            "cross-team coordination",
        ]

        for pattern in diego_patterns:
            with self.subTest(pattern=pattern):
                # Pattern should appear in context of Diego or general strategic guidance
                self.assertTrue(
                    pattern in content.lower(),
                    f"Diego's challenge pattern '{pattern}' must be preserved",
                )

    def test_camille_business_focus_preserved(self):
        """Test Camille's strategic technology and business alignment focus"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        camille_patterns = ["strategic technology", "executive", "ROI", "stakeholder"]

        for pattern in camille_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Camille's business focus pattern '{pattern}' must be preserved",
                )

    def test_rachel_design_systems_focus_preserved(self):
        """Test Rachel's design systems and UX focus"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        rachel_patterns = [
            "design systems",
            "UX",
            "accessibility",
            "cross-functional",
            "user experience",
        ]

        for pattern in rachel_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Rachel's design focus pattern '{pattern}' must be preserved",
                )

    def test_alvaro_investment_focus_preserved(self):
        """Test Alvaro's platform investment and ROI focus"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        alvaro_patterns = [
            "platform investment",
            "ROI",
            "business value",
            "investment strategy",
            "stakeholder communication",
        ]

        for pattern in alvaro_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Alvaro's investment focus pattern '{pattern}' must be preserved",
                )

    def test_martin_architecture_focus_preserved(self):
        """Test Martin's platform architecture and technical focus"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        martin_patterns = [
            "platform architecture",
            "technical",
            "architecture",
            "evolutionary design",
            "technical debt",
        ]

        for pattern in martin_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Martin's architecture focus pattern '{pattern}' must be preserved",
                )

    def test_persona_challenge_capability_preserved(self):
        """Test that personas maintain ability to challenge and push back"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        # General challenge patterns that should be preserved
        challenge_patterns = [
            "challenge",
            "assumptions",
            "stress-test",
            "first principles",
            "dig deeper",
            "validate",
        ]

        for pattern in challenge_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Challenge capability pattern '{pattern}' must be preserved",
                )

    def test_transparency_bridge_persona_detection_preserved(self):
        """Test that transparency bridge maintains persona detection"""
        if not self.transparency_bridge_file.exists():
            self.skipTest("Transparency bridge file not found - optional component")

        with open(self.transparency_bridge_file, "r") as f:
            content = f.read()

        # Should maintain persona detection and selection logic
        persona_detection_patterns = [
            "detect_persona",
            "diego",
            "camille",
            "rachel",
            "alvaro",
            "martin",
        ]

        for pattern in persona_detection_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Persona detection pattern '{pattern}' must be preserved in transparency bridge",
                )


class TestStrategicCapabilityPreservation(unittest.TestCase):
    """Test that strategic capabilities are preserved during cleanup"""

    def setUp(self):
        """Set up test environment"""
        self.cursorrules_file = PROJECT_ROOT / ".cursorrules"

    def test_framework_detection_preserved(self):
        """Test that strategic framework detection is preserved"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        framework_patterns = [
            "framework",
            "strategic framework",
            "framework detection",
            "Team Topologies",
            "Good Strategy",
            "WRAP",
        ]

        for pattern in framework_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Framework detection pattern '{pattern}' must be preserved",
                )

    def test_mcp_transparency_preserved(self):
        """Test that MCP transparency system is preserved"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        mcp_patterns = ["MCP", "transparency", "🔧 Accessing MCP Server", "sequential"]

        for pattern in mcp_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern in content,
                    f"MCP transparency pattern '{pattern}' must be preserved",
                )

    def test_complexity_analysis_preserved(self):
        """Test that complexity analysis for strategic enhancement is preserved"""
        with open(self.cursorrules_file, "r") as f:
            content = f.read()

        complexity_patterns = [
            "complexity",
            "strategic",
            "organizational",
            "framework",
            "systematic",
            "multi-team",
        ]

        for pattern in complexity_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.lower() in content.lower(),
                    f"Complexity analysis pattern '{pattern}' must be preserved",
                )


class TestDocumentationFunctionalityPreservation(unittest.TestCase):
    """Test that documentation functionality is preserved"""

    def test_technical_documentation_structure(self):
        """Test that core technical documentation structure is preserved"""
        # Check that key architectural documentation exists (TECHNICAL_INDEX.md was removed during cleanup)
        # Core technical documentation that must be preserved
        key_docs = [
            "docs/architecture/OVERVIEW.md",
            "docs/architecture/PROJECT_STRUCTURE.md",
            "docs/architecture/TESTING_ARCHITECTURE.md",
        ]

        for doc_path in key_docs:
            doc_file = PROJECT_ROOT / doc_path
            self.assertTrue(
                doc_file.exists(),
                f"Core technical documentation must exist: {doc_path}",
            )

            # Verify it's not empty
            with open(doc_file, "r") as f:
                content = f.read().strip()
            self.assertTrue(
                len(content) > 100,
                f"Technical documentation should have substantial content: {doc_path}",
            )

    def test_framework_index_exists(self):
        """Test that framework index provides strategic framework access"""
        framework_index = PROJECT_ROOT / "docs/frameworks/FRAMEWORKS_INDEX.md"
        self.assertTrue(framework_index.exists(), "Framework index must exist")

        with open(framework_index, "r") as f:
            content = f.read()

        # Should contain key strategic frameworks
        framework_references = [
            "Good Strategy Bad Strategy",
            "WRAP Decision Framework",
            "Team Topologies",
            "Strategic Platform Assessment",
        ]

        for framework in framework_references:
            with self.subTest(framework=framework):
                self.assertIn(
                    framework,
                    content,
                    f"Framework reference '{framework}' must be preserved",
                )

    def test_architecture_documentation_structure(self):
        """Test that architecture documentation maintains structure"""
        arch_files = [
            "docs/architecture/OVERVIEW.md",
            "docs/architecture/COMPONENTS.md",
            "docs/architecture/PATTERNS.md",
            "docs/architecture/DECISIONS.md",
        ]

        for arch_file in arch_files:
            with self.subTest(file=arch_file):
                file_path = PROJECT_ROOT / arch_file
                self.assertTrue(
                    file_path.exists(), f"Architecture file '{arch_file}' must exist"
                )

                # Verify file has content
                with open(file_path, "r") as f:
                    content = f.read()
                self.assertGreater(
                    len(content),
                    100,
                    f"Architecture file '{arch_file}' must have substantial content",
                )


def run_persona_preservation_tests():
    """Run all persona preservation tests"""
    print("🧪 PERSONA PERSONALITY PRESERVATION TEST SUITE")
    print("=" * 60)
    print("Testing that persona personalities and strategic capabilities")
    print("are preserved during AI verbosity cleanup.")
    print()

    # Create test suite
    suite = unittest.TestSuite()

    # Add persona personality tests
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPersonaPersonalities))
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestStrategicCapabilityPreservation)
    )
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(
            TestDocumentationFunctionalityPreservation
        )
    )

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print(f"📊 PERSONA PRESERVATION TEST RESULTS")
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
        print("\n🎉 ALL PERSONA PRESERVATION TESTS PASSED")
        print("✅ Safe to proceed with AI verbosity cleanup")
    else:
        print("\n❌ PERSONA PRESERVATION TESTS FAILED")
        print("🚫 DO NOT PROCEED - Fix failing tests first")

    return success


if __name__ == "__main__":
    success = run_persona_preservation_tests()
    exit(0 if success else 1)
