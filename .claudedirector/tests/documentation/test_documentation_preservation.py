#!/usr/bin/env python3
"""
Documentation Functionality Preservation Tests
Validates that all documentation functionality is preserved during AI verbosity cleanup.
"""

import unittest
import sys
import os
import re
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestDocumentationStructure(unittest.TestCase):
    """Test that documentation structure is preserved"""

    def test_all_setup_guides_exist(self):
        """Test that setup guides exist and are functional"""
        setup_files = ["docs/setup/QUICK_START.md", "docs/setup/INSTALLATION.md"]

        for setup_file in setup_files:
            with self.subTest(file=setup_file):
                file_path = PROJECT_ROOT / setup_file
                self.assertTrue(
                    file_path.exists(), f"Setup file '{setup_file}' must exist"
                )

                # Verify file has substantial content
                with open(file_path, "r") as f:
                    content = f.read()
                self.assertGreater(
                    len(content),
                    500,
                    f"Setup file '{setup_file}' must have substantial content",
                )

                # Verify it contains setup instructions
                self.assertTrue(
                    any(
                        keyword in content.lower()
                        for keyword in ["install", "setup", "start", "configure"]
                    ),
                    f"Setup file '{setup_file}' must contain setup instructions",
                )

    def test_all_development_guides_exist(self):
        """Test that development guides exist and are functional"""
        dev_files = ["docs/development/DEVELOPMENT_GUIDE.md"]

        for dev_file in dev_files:
            with self.subTest(file=dev_file):
                file_path = PROJECT_ROOT / dev_file
                self.assertTrue(
                    file_path.exists(), f"Development file '{dev_file}' must exist"
                )

                # Verify file has substantial content
                with open(file_path, "r") as f:
                    content = f.read()
                self.assertGreater(
                    len(content),
                    1000,
                    f"Development file '{dev_file}' must have substantial content",
                )

                # Verify it contains development information
                self.assertTrue(
                    any(
                        keyword in content.lower()
                        for keyword in [
                            "development",
                            "architecture",
                            "component",
                            "api",
                        ]
                    ),
                    f"Development file '{dev_file}' must contain development information",
                )

    def test_all_reference_guides_exist(self):
        """Test that reference guides exist and are functional"""
        ref_files = ["docs/reference/API_REFERENCE.md"]

        for ref_file in ref_files:
            with self.subTest(file=ref_file):
                file_path = PROJECT_ROOT / ref_file
                self.assertTrue(
                    file_path.exists(), f"Reference file '{ref_file}' must exist"
                )

                # Verify file has substantial content
                with open(file_path, "r") as f:
                    content = f.read()
                self.assertGreater(
                    len(content),
                    1000,
                    f"Reference file '{ref_file}' must have substantial content",
                )

                # Verify it contains API/reference information
                self.assertTrue(
                    any(
                        keyword in content.lower()
                        for keyword in [
                            "api",
                            "reference",
                            "class",
                            "function",
                            "method",
                        ]
                    ),
                    f"Reference file '{ref_file}' must contain API reference information",
                )

    def test_all_framework_guides_exist(self):
        """Test that framework guides exist and are functional"""
        framework_files = [
            "docs/frameworks/FRAMEWORKS_INDEX.md",
            "docs/frameworks/GOOD_STRATEGY_BAD_STRATEGY.md",
            "docs/frameworks/WRAP_DECISION_FRAMEWORK.md",
        ]

        for framework_file in framework_files:
            with self.subTest(file=framework_file):
                file_path = PROJECT_ROOT / framework_file
                self.assertTrue(
                    file_path.exists(), f"Framework file '{framework_file}' must exist"
                )

                # Verify file has substantial content
                with open(file_path, "r") as f:
                    content = f.read()
                self.assertGreater(
                    len(content),
                    500,
                    f"Framework file '{framework_file}' must have substantial content",
                )

                # Verify it contains framework information
                self.assertTrue(
                    any(
                        keyword in content.lower()
                        for keyword in [
                            "framework",
                            "strategy",
                            "decision",
                            "methodology",
                        ]
                    ),
                    f"Framework file '{framework_file}' must contain framework information",
                )


class TestDocumentationLinks(unittest.TestCase):
    """Test that documentation cross-references work"""

    def test_implementation_index_links_valid(self):
        """Test that implementation index contains valid links"""
        index_file = PROJECT_ROOT / "docs/IMPLEMENTATION_INDEX.md"
        self.assertTrue(index_file.exists(), "Implementation index must exist")

        with open(index_file, "r") as f:
            content = f.read()

        # Find markdown links [text](path)
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)

        # Test that linked files exist
        for link_text, link_path in links:
            with self.subTest(link=f"{link_text} -> {link_path}"):
                # Skip external links
                if link_path.startswith("http"):
                    continue

                # Strip anchors from link path for file validation
                file_path = link_path.split("#")[0] if "#" in link_path else link_path

                # Skip placeholder links for future documentation
                future_docs = [
                    "reference/CONFIGURATION.md",
                    "reference/MCP_INTEGRATION.md",
                    "reference/FRAMEWORK_DETECTION.md",
                    "testing/TESTING_OVERVIEW.md",
                    "testing/MCP_TESTS.md",
                    "testing/INTEGRATION_TESTS.md",
                    "reference/QUALITY_STANDARDS.md",
                    "reference/AI_CLEANUP.md",
                    "advanced/CUSTOM_PERSONAS.md",
                    "advanced/FRAMEWORK_EXTENSION.md",
                    "advanced/MCP_DEVELOPMENT.md",
                    "deployment/DEPLOYMENT_GUIDE.md",
                    "deployment/MONITORING.md",
                    "reference/PERFORMANCE_TUNING.md",
                    "reference/MEMORY_MANAGEMENT.md",
                    "reference/CACHING.md",
                    "reference/TROUBLESHOOTING.md",
                    "reference/FAQ.md",
                    "CONTRIBUTING.md",
                    "STRATEGIC_FRAMEWORKS_GUIDE.md",
                ]
                if file_path in future_docs:
                    continue  # Skip validation for future documentation

                # Resolve relative paths
                if not file_path.startswith("/"):
                    full_path = PROJECT_ROOT / "docs" / file_path
                else:
                    full_path = PROJECT_ROOT / file_path.lstrip("/")

                self.assertTrue(
                    full_path.exists(),
                    f"Linked file '{file_path}' from implementation index must exist",
                )

    def test_framework_index_links_valid(self):
        """Test that framework index contains valid links"""
        index_file = PROJECT_ROOT / "docs/frameworks/FRAMEWORKS_INDEX.md"
        self.assertTrue(index_file.exists(), "Framework index must exist")

        with open(index_file, "r") as f:
            content = f.read()

        # Find markdown links [text](path)
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)

        # Test that linked files exist
        for link_text, link_path in links:
            with self.subTest(link=f"{link_text} -> {link_path}"):
                # Skip external links and anchors
                if link_path.startswith("http") or link_path.startswith("#"):
                    continue

                # Skip placeholder framework links for future documentation
                future_frameworks = [
                    "./PLATFORM_ASSESSMENT.md",
                    "./TEAM_TOPOLOGIES.md",
                    "./CRUCIAL_CONVERSATIONS.md",
                    "./SCALING_EXCELLENCE.md",
                    "./CAPITAL_ALLOCATION.md",
                    "./TECHNICAL_STRATEGY.md",
                    "./ACCELERATE_PERFORMANCE.md",
                    "./ORGANIZATIONAL_TRANSFORMATION.md",
                    "./STRATEGIC_DECISION.md",
                ]
                if link_path in future_frameworks:
                    continue  # Skip validation for future framework docs

                # Resolve relative paths
                if not link_path.startswith("/"):
                    full_path = PROJECT_ROOT / "docs/frameworks" / link_path
                else:
                    full_path = PROJECT_ROOT / link_path.lstrip("/")

                # Only test if it should be a file link
                if link_path.endswith(".md"):
                    self.assertTrue(
                        full_path.exists(),
                        f"Linked file '{link_path}' from framework index must exist",
                    )


class TestCodeExamplesPreservation(unittest.TestCase):
    """Test that code examples and technical content are preserved"""

    def test_api_examples_preserved(self):
        """Test that API examples in documentation are preserved"""
        api_file = PROJECT_ROOT / "docs/reference/API_REFERENCE.md"
        if not api_file.exists():
            self.skipTest("API reference file not found")

        with open(api_file, "r") as f:
            content = f.read()

        # Should contain code blocks
        code_block_count = content.count("```")
        self.assertGreater(
            code_block_count, 10, "API reference should contain multiple code examples"
        )

        # Should contain Python class definitions
        self.assertIn(
            "class ", content, "API reference should contain class definitions"
        )
        self.assertIn(
            "def ", content, "API reference should contain method definitions"
        )

    def test_setup_commands_preserved(self):
        """Test that setup commands in guides are preserved"""
        setup_files = ["docs/setup/QUICK_START.md", "docs/setup/INSTALLATION.md"]

        for setup_file in setup_files:
            file_path = PROJECT_ROOT / setup_file
            if not file_path.exists():
                continue

            with self.subTest(file=setup_file):
                with open(file_path, "r") as f:
                    content = f.read()

                # Should contain command examples
                command_indicators = [
                    "```bash",
                    "```",
                    "git clone",
                    "pip install",
                    "python",
                    "cursor",
                ]
                has_commands = any(
                    indicator in content for indicator in command_indicators
                )
                self.assertTrue(
                    has_commands,
                    f"Setup file '{setup_file}' should contain command examples",
                )

    def test_framework_examples_preserved(self):
        """Test that framework examples are preserved"""
        framework_files = [
            "docs/frameworks/GOOD_STRATEGY_BAD_STRATEGY.md",
            "docs/frameworks/WRAP_DECISION_FRAMEWORK.md",
        ]

        for framework_file in framework_files:
            file_path = PROJECT_ROOT / framework_file
            if not file_path.exists():
                continue

            with self.subTest(file=framework_file):
                with open(file_path, "r") as f:
                    content = f.read()

                # Should contain practical examples
                example_indicators = [
                    "example",
                    "Example",
                    "```",
                    "Application",
                    "Case:",
                ]
                has_examples = any(
                    indicator in content for indicator in example_indicators
                )
                self.assertTrue(
                    has_examples,
                    f"Framework file '{framework_file}' should contain practical examples",
                )


class TestContentQuality(unittest.TestCase):
    """Test content quality standards after cleanup"""

    def detect_ai_verbosity_patterns(self, content):
        """Detect AI verbosity patterns that should be removed"""
        ai_patterns = [
            r"revolutionary",
            r"unprecedented",
            r"amazing",
            r"incredible",
            r"comprehensive complete",
            r"complete comprehensive",
            r"transform your entire",
            r"exciting world of",
            r"welcome to the.*world",
            r"🎉.*🚀.*✨",  # Excessive emoji combinations
        ]

        found_patterns = []
        for pattern in ai_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)

        return found_patterns

    def test_readme_quality_standards(self):
        """Test that README meets quality standards"""
        readme_file = PROJECT_ROOT / "README.md"
        self.assertTrue(readme_file.exists(), "README.md must exist")

        with open(readme_file, "r") as f:
            content = f.read()

        # Should have substantial content
        self.assertGreater(len(content), 200, "README should have substantial content")

        # Should contain project description
        self.assertTrue(
            any(
                keyword in content.lower()
                for keyword in ["claudedirector", "strategic", "ai", "leadership"]
            ),
            "README should contain project description",
        )

    def test_documentation_file_sizes_reasonable(self):
        """Test that documentation files are reasonably sized (not too long)"""
        max_lines = 650  # Reasonable upper limit for maintainability (reference docs can be longer)

        doc_files = []
        for doc_dir in [
            "docs/setup",
            "docs/development",
            "docs/reference",
            "docs/frameworks",
            "docs/architecture",
        ]:
            doc_path = PROJECT_ROOT / doc_dir
            if doc_path.exists():
                for md_file in doc_path.glob("*.md"):
                    doc_files.append(md_file)

        for doc_file in doc_files:
            with self.subTest(file=str(doc_file.relative_to(PROJECT_ROOT))):
                with open(doc_file, "r") as f:
                    lines = f.readlines()

                line_count = len(lines)
                self.assertLessEqual(
                    line_count,
                    max_lines,
                    f"Documentation file '{doc_file.name}' has {line_count} lines (max {max_lines})",
                )


def run_documentation_preservation_tests():
    """Run all documentation preservation tests"""
    print("📚 DOCUMENTATION FUNCTIONALITY PRESERVATION TEST SUITE")
    print("=" * 60)
    print("Testing that all documentation functionality is preserved")
    print("during AI verbosity cleanup.")
    print()

    # Create test suite
    suite = unittest.TestSuite()

    # Add documentation tests
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestDocumentationStructure)
    )
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocumentationLinks))
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestCodeExamplesPreservation)
    )
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestContentQuality))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print(f"📊 DOCUMENTATION PRESERVATION TEST RESULTS")
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
        print("\n🎉 ALL DOCUMENTATION PRESERVATION TESTS PASSED")
        print("✅ Documentation functionality validated")
    else:
        print("\n❌ DOCUMENTATION PRESERVATION TESTS FAILED")
        print("🚫 Fix failing tests before proceeding")

    return success


if __name__ == "__main__":
    success = run_documentation_preservation_tests()
    exit(0 if success else 1)
