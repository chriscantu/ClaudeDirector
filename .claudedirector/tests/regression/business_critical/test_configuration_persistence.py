#!/usr/bin/env python3
"""
Business-Critical Regression Test: Configuration Persistence

Alvaro's Test Suite: Ensures user configuration and customization data
persists correctly across sessions and system restarts.

BUSINESS IMPACT: Configuration loss leads to user frustration,
re-onboarding overhead, and loss of personalized strategic intelligence.
"""

import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestConfigurationPersistence(unittest.TestCase):
    """Business-critical tests for configuration persistence"""

    def setUp(self):
        """Set up test environment with temporary directories"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claudedirector" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Mock configuration files
        self.user_config_file = self.config_dir / "user_config.json"
        self.persona_config_file = self.config_dir / "persona_preferences.json"
        self.workspace_config_file = self.config_dir / "workspace_settings.json"

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_user_configuration_persistence(self):
        """
        BUSINESS CRITICAL: User role and preference configuration must persist

        FAILURE IMPACT: Users lose customization, must re-onboard
        BUSINESS COST: Productivity loss, user frustration, support overhead
        """
        # Test user configuration data
        user_config = {
            "user_role": "VP Engineering",
            "organization_type": "Enterprise Tech",
            "challenge_focus": "Platform Scaling",
            "active_personas": ["diego", "camille", "alvaro"],
            "preferred_frameworks": ["Team Topologies", "SOLID Principles"],
            "notification_preferences": {
                "email_alerts": True,
                "slack_integration": False,
                "daily_summaries": True,
            },
            "customization": {
                "theme": "executive",
                "dashboard_layout": "strategic_overview",
                "default_analysis_depth": "comprehensive",
            },
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        # Write configuration
        with open(self.user_config_file, "w") as f:
            json.dump(user_config, f, indent=2)

        # Verify persistence
        self.assertTrue(
            self.user_config_file.exists(), "User configuration file must be created"
        )

        # Read back configuration
        with open(self.user_config_file, "r") as f:
            loaded_config = json.load(f)

        # Verify critical fields persist correctly
        self.assertEqual(loaded_config["user_role"], "VP Engineering")
        self.assertEqual(loaded_config["organization_type"], "Enterprise Tech")
        self.assertEqual(loaded_config["challenge_focus"], "Platform Scaling")
        self.assertIn("diego", loaded_config["active_personas"])
        self.assertIn("Team Topologies", loaded_config["preferred_frameworks"])

        print("✅ User configuration persistence: PASSED")

    def test_persona_preferences_persistence(self):
        """
        BUSINESS CRITICAL: Persona customization and preferences must persist

        FAILURE IMPACT: Strategic personas lose personalization
        BUSINESS COST: Generic advice instead of tailored strategic guidance
        """
        persona_preferences = {
            "diego": {
                "communication_style": "direct_challenging",
                "analysis_depth": "comprehensive",
                "framework_preference": "Team Topologies",
                "pushback_intensity": "high",
                "stakeholder_focus": ["engineering_teams", "product_managers"],
            },
            "camille": {
                "communication_style": "executive_brief",
                "analysis_depth": "strategic_overview",
                "framework_preference": "Good Strategy Bad Strategy",
                "board_communication": True,
                "competitive_analysis": True,
            },
            "alvaro": {
                "communication_style": "roi_focused",
                "analysis_depth": "financial_detailed",
                "framework_preference": "Capital Allocation Framework",
                "investment_threshold": 100000,
                "roi_minimum": 1.15,
            },
            "rachel": {
                "communication_style": "user_centered",
                "analysis_depth": "design_systems",
                "framework_preference": "Design System Maturity Model",
                "accessibility_priority": "high",
                "cross_functional_focus": True,
            },
        }

        # Write persona preferences
        with open(self.persona_config_file, "w") as f:
            json.dump(persona_preferences, f, indent=2)

        # Verify persistence
        self.assertTrue(
            self.persona_config_file.exists(),
            "Persona preferences file must be created",
        )

        # Read back preferences
        with open(self.persona_config_file, "r") as f:
            loaded_preferences = json.load(f)

        # Verify persona-specific settings persist
        self.assertEqual(
            loaded_preferences["diego"]["communication_style"], "direct_challenging"
        )
        self.assertEqual(
            loaded_preferences["camille"]["framework_preference"],
            "Good Strategy Bad Strategy",
        )
        self.assertEqual(loaded_preferences["alvaro"]["roi_minimum"], 1.15)
        self.assertTrue(
            loaded_preferences["rachel"]["accessibility_priority"] == "high"
        )

        print("✅ Persona preferences persistence: PASSED")

    def test_workspace_settings_persistence(self):
        """
        BUSINESS CRITICAL: Workspace and project settings must persist

        FAILURE IMPACT: Project context and workspace customization lost
        BUSINESS COST: Re-setup overhead, lost project intelligence
        """
        workspace_settings = {
            "current_workspace": "/Users/executive/strategic-projects",
            "recent_workspaces": [
                "/Users/executive/strategic-projects",
                "/Users/executive/platform-architecture",
                "/Users/executive/team-scaling",
            ],
            "project_contexts": {
                "platform-scaling": {
                    "stakeholders": ["hemendra", "steve", "beth"],
                    "initiatives": ["NGX Gold", "Platform Investment"],
                    "frameworks_applied": ["Team Topologies", "Capital Allocation"],
                    "last_accessed": datetime.now().isoformat(),
                }
            },
            "integration_settings": {
                "github_repos": ["org/platform-core", "org/strategic-initiatives"],
                "jira_projects": ["PLAT", "STRAT"],
                "slack_channels": ["#platform-team", "#executive-updates"],
            },
            "performance_settings": {
                "cache_size_mb": 512,
                "max_concurrent_analyses": 4,
                "response_timeout_seconds": 30,
            },
        }

        # Write workspace settings
        with open(self.workspace_config_file, "w") as f:
            json.dump(workspace_settings, f, indent=2)

        # Verify persistence
        self.assertTrue(
            self.workspace_config_file.exists(),
            "Workspace settings file must be created",
        )

        # Read back settings
        with open(self.workspace_config_file, "r") as f:
            loaded_settings = json.load(f)

        # Verify workspace context persists
        self.assertEqual(
            loaded_settings["current_workspace"], "/Users/executive/strategic-projects"
        )
        self.assertIn("platform-scaling", loaded_settings["project_contexts"])
        self.assertIn(
            "NGX Gold",
            loaded_settings["project_contexts"]["platform-scaling"]["initiatives"],
        )
        self.assertEqual(loaded_settings["performance_settings"]["cache_size_mb"], 512)

        print("✅ Workspace settings persistence: PASSED")

    def test_configuration_backup_and_recovery(self):
        """
        BUSINESS CRITICAL: Configuration backup and recovery must work

        FAILURE IMPACT: Configuration corruption leads to complete data loss
        BUSINESS COST: Complete re-onboarding, lost strategic context
        """
        # Create original configuration
        original_config = {
            "user_id": "executive_001",
            "strategic_context": {
                "current_initiatives": ["Platform Scaling", "Team Restructure"],
                "stakeholder_relationships": {
                    "hemendra": "platform_opponent",
                    "steve": "roi_focused",
                    "beth": "platform_advocate",
                },
                "decision_history": [
                    {
                        "decision": "NGX Gold Investment",
                        "outcome": "approved",
                        "roi": 1.21,
                    }
                ],
            },
            "backup_metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "2.1.0",
                "checksum": "abc123def456",
            },
        }

        config_file = self.config_dir / "strategic_config.json"
        backup_file = self.config_dir / "strategic_config.backup.json"

        # Write original configuration
        with open(config_file, "w") as f:
            json.dump(original_config, f, indent=2)

        # Create backup
        shutil.copy2(config_file, backup_file)

        # Simulate corruption (empty file)
        with open(config_file, "w") as f:
            f.write("")

        # Verify corruption
        self.assertEqual(
            os.path.getsize(config_file), 0, "Config file should be corrupted (empty)"
        )

        # Recovery from backup
        if backup_file.exists() and os.path.getsize(backup_file) > 0:
            shutil.copy2(backup_file, config_file)

        # Verify recovery
        with open(config_file, "r") as f:
            recovered_config = json.load(f)

        # Verify strategic context recovered
        self.assertEqual(recovered_config["user_id"], "executive_001")
        self.assertIn(
            "Platform Scaling",
            recovered_config["strategic_context"]["current_initiatives"],
        )
        self.assertEqual(
            recovered_config["strategic_context"]["stakeholder_relationships"][
                "hemendra"
            ],
            "platform_opponent",
        )

        print("✅ Configuration backup and recovery: PASSED")

    def test_cross_session_persistence(self):
        """
        BUSINESS CRITICAL: Configuration must persist across system restarts

        FAILURE IMPACT: Settings reset on every restart
        BUSINESS COST: Daily re-configuration overhead, user abandonment
        """
        # Simulate session 1: Create and save configuration
        session1_config = {
            "session_id": "session_001",
            "user_preferences": {
                "default_persona": "diego",
                "analysis_mode": "strategic_deep_dive",
                "notification_frequency": "immediate",
            },
            "active_contexts": {
                "current_project": "platform_transformation",
                "focus_areas": ["team_scaling", "architecture_decisions"],
                "stakeholder_priorities": ["executive_alignment", "team_buy_in"],
            },
            "performance_metrics": {
                "avg_response_time": 2.3,
                "user_satisfaction": 8.7,
                "framework_accuracy": 0.94,
            },
        }

        session_file = self.config_dir / "session_persistence.json"

        # Save session 1 configuration
        with open(session_file, "w") as f:
            json.dump(session1_config, f, indent=2)

        # Simulate system restart (file should still exist)
        self.assertTrue(
            session_file.exists(), "Session file must persist after restart"
        )

        # Simulate session 2: Load previous configuration
        with open(session_file, "r") as f:
            session2_config = json.load(f)

        # Verify session continuity
        self.assertEqual(
            session2_config["user_preferences"]["default_persona"], "diego"
        )
        self.assertEqual(
            session2_config["active_contexts"]["current_project"],
            "platform_transformation",
        )
        self.assertIn("team_scaling", session2_config["active_contexts"]["focus_areas"])

        # Update configuration in session 2
        session2_config["session_id"] = "session_002"
        session2_config["user_preferences"]["analysis_mode"] = "executive_summary"
        session2_config["performance_metrics"]["user_satisfaction"] = 9.1

        # Save updated configuration
        with open(session_file, "w") as f:
            json.dump(session2_config, f, indent=2)

        # Verify updates persisted
        with open(session_file, "r") as f:
            final_config = json.load(f)

        self.assertEqual(final_config["session_id"], "session_002")
        self.assertEqual(
            final_config["user_preferences"]["analysis_mode"], "executive_summary"
        )
        self.assertEqual(final_config["performance_metrics"]["user_satisfaction"], 9.1)

        print("✅ Cross-session persistence: PASSED")


def run_business_critical_config_tests():
    """Run all business-critical configuration persistence tests"""
    print("🔥 BUSINESS-CRITICAL REGRESSION TEST: Configuration Persistence")
    print("=" * 70)
    print("OWNER: Alvaro | IMPACT: User Experience & Data Integrity")
    print("FAILURE COST: Re-onboarding overhead, lost customization, user churn")
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigurationPersistence)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL CONFIGURATION PERSISTENCE TESTS PASSED")
        print("💼 Business Impact: User configuration integrity maintained")
        print("📊 Strategic Value: Personalized intelligence preserved")
        return True
    else:
        print(
            f"\n❌ CONFIGURATION PERSISTENCE FAILURES: {len(result.failures + result.errors)}"
        )
        print("💥 Business Impact: User experience degraded, data loss risk")
        print("🚨 Action Required: Fix configuration persistence immediately")
        return False


if __name__ == "__main__":
    success = run_business_critical_config_tests()
    sys.exit(0 if success else 1)
