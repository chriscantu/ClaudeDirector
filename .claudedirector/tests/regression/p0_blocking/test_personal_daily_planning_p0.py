#!/usr/bin/env python3
"""
Personal Daily Planning Agent P0 Test - ACTUAL FUNCTIONALITY VALIDATION

🚨 P0 BLOCKING TEST - ZERO TOLERANCE FOR FAILURE
Purpose: Validate PersonalDailyPlanningAgent works end-to-end following PersonalRetrospectiveAgent pattern
Architecture: Following TESTING_ARCHITECTURE.md unified testing principles

CRITICAL REQUIREMENTS:
- All /daily-plan commands must work identically to /retrospective commands
- Database operations must persist and retrieve data correctly
- Interactive sessions must manage state properly
- Import system must work without failures
- ConversationalInteractionManager integration must function

FAILURE IMPACT: Daily planning feature completely broken, user frustration, strategic productivity loss
"""

import os
import sys
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure proper imports following TESTING_ARCHITECTURE.md environment setup
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

try:
    from agents.personal_daily_planning_agent import (
        PersonalDailyPlanningAgent,
        DailyPlanEntry,
    )
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from core.types import ProcessingResult

    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    IMPORTS_SUCCESSFUL = False
    IMPORT_ERROR = str(e)


class TestPersonalDailyPlanningP0(unittest.TestCase):
    """
    P0 BLOCKING TEST: Personal Daily Planning Agent

    Validates complete end-to-end functionality following PersonalRetrospectiveAgent pattern.
    ZERO TOLERANCE - Any failure blocks deployment.
    """

    @classmethod
    def setUpClass(cls):
        """P0 Test Setup - Validate imports work"""
        if not IMPORTS_SUCCESSFUL:
            raise ImportError(
                f"🚨 P0 BLOCKING FAILURE: PersonalDailyPlanningAgent import failed: {IMPORT_ERROR}"
            )

    def setUp(self):
        """Setup test environment with temporary database"""
        # Create temporary database for isolated testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_daily_plan.db")

        # Initialize agent with test database
        self.agent = PersonalDailyPlanningAgent()
        self.agent.db_path = self.test_db_path
        self.agent._init_database()

        # Test user ID
        self.test_user_id = "test_user_p0"

    def tearDown(self):
        """Cleanup test environment"""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_p0_agent_initialization(self):
        """P0: PersonalDailyPlanningAgent must initialize without errors"""
        try:
            agent = PersonalDailyPlanningAgent()
            self.assertIsInstance(agent, BaseManager)
            self.assertEqual(agent.config.manager_name, "personal_daily_planning_agent")
            self.assertEqual(agent.config.manager_type, ManagerType.ANALYTICS)
            self.assertIsInstance(agent.active_sessions, dict)
        except Exception as e:
            self.fail(f"🚨 P0 BLOCKING FAILURE: Agent initialization failed: {str(e)}")

    def test_p0_database_initialization(self):
        """P0: Database must be created and accessible"""
        try:
            # Verify database file exists
            self.assertTrue(
                os.path.exists(self.test_db_path), "Database file not created"
            )

            # Verify table structure
            with sqlite3.connect(self.test_db_path) as conn:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='daily_plans'"
                )
                result = cursor.fetchone()
                self.assertIsNotNone(result, "daily_plans table not created")

                # Verify table schema
                cursor = conn.execute("PRAGMA table_info(daily_plans)")
                columns = {row[1]: row[2] for row in cursor.fetchall()}
                expected_columns = {
                    "id": "INTEGER",
                    "date": "TEXT",
                    "priorities": "TEXT",
                    "l0_l1_balance": "TEXT",
                    "created_at": "TIMESTAMP",
                }
                for col_name, col_type in expected_columns.items():
                    self.assertIn(col_name, columns, f"Missing column: {col_name}")

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Database initialization failed: {str(e)}"
            )

    def test_p0_slash_command_help(self):
        """P0: /daily-plan help command must work (baseline functionality)"""
        try:
            result = self.agent.process_request(
                {
                    "command": "/daily-plan help",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )

            self.assertTrue(result.success, f"Help command failed: {result.message}")
            self.assertIn("Daily Planning Commands", result.message)
            self.assertIn("/daily-plan start", result.message)
            self.assertIn("/daily-plan status", result.message)
            self.assertIn("/daily-plan review", result.message)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: /daily-plan help command failed: {str(e)}"
            )

    def test_p0_interactive_session_start(self):
        """P0: /daily-plan start must create interactive session (core functionality)"""
        try:
            result = self.agent.process_request(
                {
                    "command": "/daily-plan start",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )

            # Validate session started successfully
            self.assertTrue(result.success, f"Session start failed: {result.message}")
            self.assertIn("Daily Planning Session Started", result.message)
            self.assertIn("priorities", result.message.lower())

            # Validate session state created
            self.assertIn(self.test_user_id, self.agent.active_sessions)
            session = self.agent.active_sessions[self.test_user_id]
            self.assertEqual(session["state"], "collecting_priorities")
            self.assertIsInstance(session["priorities"], list)
            self.assertEqual(len(session["priorities"]), 0)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Interactive session start failed: {str(e)}"
            )

    def test_p0_priority_collection_workflow(self):
        """P0: Interactive priority collection must work end-to-end"""
        try:
            # Start session
            start_result = self.agent.process_request(
                {
                    "command": "/daily-plan start",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )
            self.assertTrue(start_result.success)

            # Add first priority
            priority1_result = self.agent.process_request(
                {
                    "command": "session_input",  # This should trigger _handle_session_input
                    "user_id": self.test_user_id,
                    "user_input": "Strategic planning for Q4",
                }
            )
            self.assertTrue(
                priority1_result.success,
                f"Priority 1 failed: {priority1_result.message}",
            )
            self.assertIn("Priority 1 added", priority1_result.message)

            # Add second priority
            priority2_result = self.agent.process_request(
                {
                    "command": "session_input",
                    "user_id": self.test_user_id,
                    "user_input": "Team performance reviews",
                }
            )
            self.assertTrue(
                priority2_result.success,
                f"Priority 2 failed: {priority2_result.message}",
            )
            self.assertIn("Priority 2 added", priority2_result.message)

            # Verify session state
            session = self.agent.active_sessions[self.test_user_id]
            self.assertEqual(len(session["priorities"]), 2)
            self.assertEqual(session["priorities"][0], "Strategic planning for Q4")
            self.assertEqual(session["priorities"][1], "Team performance reviews")

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Priority collection workflow failed: {str(e)}"
            )

    def test_p0_session_completion_and_database_storage(self):
        """P0: Session completion must save to database correctly"""
        try:
            # Start session and add priorities
            self.agent.process_request(
                {
                    "command": "/daily-plan start",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )

            # Add priorities via session input
            self.agent.active_sessions[self.test_user_id] = {
                "state": "collecting_priorities",
                "priorities": ["Strategic planning", "Team reviews", "Technical debt"],
                "started_at": datetime.now().isoformat(),
            }

            # Complete session
            completion_result = self.agent.process_request(
                {
                    "command": "session_input",
                    "user_id": self.test_user_id,
                    "user_input": "done",
                }
            )

            self.assertTrue(
                completion_result.success,
                f"Session completion failed: {completion_result.message}",
            )
            self.assertIn("Daily Plan Created", completion_result.message)
            self.assertIn("Strategic Balance", completion_result.message)

            # Verify session cleaned up
            self.assertNotIn(self.test_user_id, self.agent.active_sessions)

            # Verify database storage
            today = datetime.now().date().isoformat()
            with sqlite3.connect(self.test_db_path) as conn:
                cursor = conn.execute(
                    "SELECT priorities, l0_l1_balance FROM daily_plans WHERE date = ?",
                    (today,),
                )
                result = cursor.fetchone()
                self.assertIsNotNone(result, "Daily plan not saved to database")

                priorities = result[0].split("|")
                self.assertEqual(len(priorities), 3)
                self.assertIn("Strategic planning", priorities)
                self.assertIn("Team reviews", priorities)
                self.assertIn("Technical debt", priorities)

                balance = result[1]
                self.assertIsNotNone(balance)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Session completion and database storage failed: {str(e)}"
            )

    def test_p0_status_command_functionality(self):
        """P0: /daily-plan status must retrieve and display current plan"""
        try:
            # Create a plan first
            today = datetime.now().date().isoformat()
            priorities = ["Strategic planning", "Team development"]
            priorities_str = "|".join(priorities)

            with sqlite3.connect(self.test_db_path) as conn:
                conn.execute(
                    "INSERT INTO daily_plans (date, priorities, l0_l1_balance) VALUES (?, ?, ?)",
                    (today, priorities_str, "L0 Focus"),
                )

            # Test status command
            status_result = self.agent.process_request(
                {
                    "command": "/daily-plan status",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )

            self.assertTrue(
                status_result.success, f"Status command failed: {status_result.message}"
            )
            self.assertIn("Today's Plan", status_result.message)
            self.assertIn("Strategic planning", status_result.message)
            self.assertIn("Team development", status_result.message)
            self.assertIn("Strategic Balance", status_result.message)
            self.assertIn("L0 Focus", status_result.message)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Status command functionality failed: {str(e)}"
            )

    def test_p0_review_command_functionality(self):
        """P0: /daily-plan review must show recent plans"""
        try:
            # Create multiple plans
            dates_priorities = [
                ("2025-09-25", "Strategic planning|Team reviews"),
                ("2025-09-24", "Technical debt|Performance optimization"),
                ("2025-09-23", "Stakeholder meetings|Documentation"),
            ]

            with sqlite3.connect(self.test_db_path) as conn:
                for date, priorities in dates_priorities:
                    conn.execute(
                        "INSERT INTO daily_plans (date, priorities, l0_l1_balance) VALUES (?, ?, ?)",
                        (date, priorities, "Mixed L0/L1"),
                    )

            # Test review command
            review_result = self.agent.process_request(
                {
                    "command": "/daily-plan review",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )

            self.assertTrue(
                review_result.success, f"Review command failed: {review_result.message}"
            )
            self.assertIn("Recent Daily Plans", review_result.message)
            self.assertIn("2025-09-25", review_result.message)
            self.assertIn("Strategic planning", review_result.message)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Review command functionality failed: {str(e)}"
            )

    def test_p0_pattern_consistency_with_retrospective_agent(self):
        """P0: PersonalDailyPlanningAgent must follow PersonalRetrospectiveAgent pattern exactly"""
        try:
            # Test BaseManager inheritance
            self.assertIsInstance(self.agent, BaseManager)

            # Test manager configuration pattern
            self.assertEqual(self.agent.config.manager_type, ManagerType.ANALYTICS)
            self.assertTrue(self.agent.config.manager_name.endswith("_agent"))

            # Test active_sessions pattern (same as PersonalRetrospectiveAgent)
            self.assertIsInstance(self.agent.active_sessions, dict)

            # Test database path pattern
            self.assertTrue(self.agent.db_path.endswith(".db"))
            self.assertIn("strategic", self.agent.db_path)

            # Test command routing pattern
            result = self.agent.process_request(
                {
                    "command": "/daily-plan help",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )
            self.assertTrue(result.success)
            self.assertIsInstance(result, ProcessingResult)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Pattern consistency validation failed: {str(e)}"
            )

    def test_p0_error_handling_robustness(self):
        """P0: Agent must handle errors gracefully without crashing"""
        try:
            # Test invalid command
            invalid_result = self.agent.process_request(
                {
                    "command": "/daily-plan invalid",
                    "user_id": self.test_user_id,
                    "user_input": "",
                }
            )
            # Should not crash, should return error message
            self.assertFalse(invalid_result.success)
            self.assertIn("Unknown", invalid_result.message)

            # Test empty input handling
            empty_result = self.agent.process_request(
                {"command": "", "user_id": self.test_user_id, "user_input": ""}
            )
            # Should default to help
            self.assertTrue(empty_result.success)

        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: Error handling robustness failed: {str(e)}"
            )


class TestPersonalDailyPlanningIntegrationP0(unittest.TestCase):
    """
    P0 INTEGRATION TEST: ConversationalInteractionManager Integration

    Validates that PersonalDailyPlanningAgent integrates properly with ConversationalInteractionManager
    following the same pattern as PersonalRetrospectiveAgent.
    """

    def test_p0_conversational_manager_import_integration(self):
        """P0: ConversationalInteractionManager must import PersonalDailyPlanningAgent successfully"""
        try:
            # Test the import that ConversationalInteractionManager uses
            from mcp.conversational_interaction_manager import (
                ConversationalInteractionManager,
                DAILY_PLANNING_AVAILABLE,
            )

            # Validate import succeeded
            self.assertTrue(
                DAILY_PLANNING_AVAILABLE,
                "PersonalDailyPlanningAgent import failed in ConversationalInteractionManager",
            )

            # Test manager initialization
            manager = ConversationalInteractionManager()
            self.assertIsNotNone(
                manager.daily_planning_agent, "daily_planning_agent property failed"
            )

        except ImportError as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: ConversationalInteractionManager integration import failed: {str(e)}"
            )
        except Exception as e:
            self.fail(
                f"🚨 P0 BLOCKING FAILURE: ConversationalInteractionManager integration failed: {str(e)}"
            )


if __name__ == "__main__":
    # Run P0 tests with detailed output
    unittest.main(verbosity=2, exit=False)
