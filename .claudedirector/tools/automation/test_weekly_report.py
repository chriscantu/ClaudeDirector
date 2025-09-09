#!/usr/bin/env python3
"""
Test runner for Weekly Report Generator
Validates configuration, tests API connection, and generates sample report.
"""

import os
import sys
import tempfile
import logging
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from weekly_report_generator import (
        ConfigManager,
        JiraClient,
        StrategicAnalyzer,
        ReportGenerator,
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure weekly_report_generator.py is in the same directory")
    sys.exit(1)


def test_configuration():
    """Test configuration loading and validation."""
    print("🔧 Testing configuration...")

    try:
        # Find config file
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent
        config_path = (
            project_root
            / "leadership-workspace"
            / "configs"
            / "weekly-report-config.yaml"
        )

        if not config_path.exists():
            print(f"❌ Config file not found: {config_path}")
            return False

        # Load config
        config_manager = ConfigManager(str(config_path))

        # Test JQL queries
        queries = config_manager.config.get("jql_queries", {})
        print(f"✅ Loaded {len(queries)} JQL queries")

        # Test essential queries
        essential_queries = ["weekly_executive_epics", "strategic_comprehensive"]
        for query_name in essential_queries:
            query = config_manager.get_jql_query(query_name)
            if query:
                print(f"✅ Found query '{query_name}': {query[:50]}...")
            else:
                print(f"⚠️  Missing query '{query_name}'")

        print("✅ Configuration test passed")
        return True, config_manager

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False, None


def test_jira_connection(config_manager):
    """Test Jira API connection."""
    print("🌐 Testing Jira connection...")

    try:
        jira_client = JiraClient(config_manager)

        # Check environment variables
        required_vars = ["JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
            print("Set these variables to test Jira connection:")
            for var in missing_vars:
                print(f"  export {var}='your-value-here'")
            return False, jira_client

        # Test connection
        if jira_client.test_connection():
            print("✅ Jira connection successful")
            return True, jira_client
        else:
            print("❌ Jira connection failed")
            return False, jira_client

    except Exception as e:
        print(f"❌ Jira connection test failed: {e}")
        return False, None


def test_strategic_analyzer(config_manager):
    """Test strategic analysis functionality."""
    print("🎯 Testing strategic analyzer...")

    try:
        from weekly_report_generator import JiraIssue

        analyzer = StrategicAnalyzer(config_manager)

        # Create test issue
        test_issue = JiraIssue(
            key="UIS-1590",
            summary="Hammer v1 platform tooling automation developer experience",
            status="In Progress",
            assignee="Test User",
            project_name="Web Platform",
            project_key="WEBPLAT",
            priority="Highest",
            updated="2024-01-01T00:00:00.000Z",
            description="Platform developer experience automation tooling",
            watchers=5,
        )

        # Calculate score
        score = analyzer.calculate_strategic_score(test_issue)

        print(f"✅ Strategic scoring works - Score: {score.score}/10")
        print(f"   Indicators: {', '.join(score.indicators)}")
        print(
            f"   Reasoning: {'; '.join(score.reasoning[:2])}..."
        )  # Show first 2 reasons

        return True, analyzer

    except Exception as e:
        print(f"❌ Strategic analyzer test failed: {e}")
        return False, None


def test_report_generation(config_manager, jira_client, strategic_analyzer):
    """Test report generation."""
    print("📊 Testing report generation...")

    try:
        report_generator = ReportGenerator(
            config_manager, jira_client, strategic_analyzer
        )

        # Generate report to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = f.name

        success = report_generator.generate_weekly_report(
            temp_path, "weekly_executive_epics"
        )

        if success:
            # Check file was created and has content
            temp_file = Path(temp_path)
            if temp_file.exists() and temp_file.stat().st_size > 0:
                content = temp_file.read_text()
                print(f"✅ Report generated successfully ({len(content)} characters)")
                print(f"   File: {temp_path}")

                # Show first few lines
                lines = content.split("\n")[:5]
                print("   Preview:")
                for line in lines:
                    print(f"   {line}")

                # Cleanup
                try:
                    temp_file.unlink()
                except:
                    pass

                return True
            else:
                print("❌ Report file was empty or not created")
                return False
        else:
            print("❌ Report generation failed")
            return False

    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Weekly Report Generator - Test Suite")
    print("=" * 50)

    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)  # Suppress info logs during testing

    all_passed = True

    # Test 1: Configuration
    config_success, config_manager = test_configuration()
    if not config_success:
        all_passed = False

    # Test 2: Jira Connection (only if config loaded)
    jira_client = None
    if config_manager:
        jira_success, jira_client = test_jira_connection(config_manager)
        # Note: We don't fail the overall test if Jira is unavailable
        # as the system should work with template reports

    # Test 3: Strategic Analyzer
    strategic_analyzer = None
    if config_manager:
        strategic_success, strategic_analyzer = test_strategic_analyzer(config_manager)
        if not strategic_success:
            all_passed = False

    # Test 4: Report Generation
    if config_manager and strategic_analyzer:
        if jira_client is None:
            # Create a basic jira client for template generation
            jira_client = JiraClient(config_manager)

        report_success = test_report_generation(
            config_manager, jira_client, strategic_analyzer
        )
        if not report_success:
            all_passed = False

    # Summary
    print("=" * 50)
    if all_passed:
        print("✅ All core tests passed!")
        print("\n🚀 Ready to generate reports:")
        print("   python weekly_report_generator.py --help")
        print("   python weekly_report_generator.py --dry-run")
        print("   python weekly_report_generator.py --verbose")
    else:
        print("❌ Some tests failed")
        print("\n🔧 Fix the issues above and run tests again")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
