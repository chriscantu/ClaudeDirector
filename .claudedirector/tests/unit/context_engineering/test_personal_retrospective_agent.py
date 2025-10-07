#!/usr/bin/env python3
"""
Test Personal Retrospective Agent - Clean Implementation
Following PR #150 testing patterns
"""

import unittest
import tempfile
import os
from datetime import datetime

from lib.agents.personal_retrospective_agent import (
    PersonalRetrospectiveAgent,
    RetrospectiveEntry,
)
from lib.core.types import ProcessingResult


class TestPersonalRetrospectiveAgent(unittest.TestCase):
    """Test Personal Retrospective Agent functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_retrospective.db")

        # Create agent with test database
        self.agent = PersonalRetrospectiveAgent()
        self.agent.db_path = self.db_path
        self.agent._init_database()

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_create_retrospective(self):
        """Test creating retrospective entry"""
        request_data = {
            "command": "create",
            "date": "2025-09-21",
            "went_well": "Completed rollback successfully",
            "could_improve": "Better planning to avoid bloat",
            "next_focus": "Clean architecture principles",
        }

        result = self.agent.process_request(request_data)

        self.assertTrue(result.success)
        self.assertIn("Retrospective saved", result.message)
        self.assertIsInstance(result.data["entry"], RetrospectiveEntry)

    def test_view_retrospectives(self):
        """Test viewing retrospective entries"""
        # Create test entry first
        create_data = {
            "command": "create",
            "date": "2025-09-21",
            "went_well": "Test entry",
            "could_improve": "Test improvement",
            "next_focus": "Test focus",
        }
        self.agent.process_request(create_data)

        # View entries
        view_data = {"command": "view", "limit": 5}
        result = self.agent.process_request(view_data)

        self.assertTrue(result.success)
        self.assertEqual(len(result.data["entries"]), 1)
        self.assertEqual(result.data["entries"][0].went_well, "Test entry")

    def test_help_command(self):
        """Test help command"""
        result = self.agent.process_request({"command": "help"})

        self.assertTrue(result.success)
        self.assertIn("Personal Retrospective Agent", result.message)
        self.assertIn(
            "4-Question Framework", result.message
        )  # FIX: Production has 4 questions (added rating)

    def test_unknown_command(self):
        """Test unknown command handling"""
        result = self.agent.process_request({"command": "invalid"})

        self.assertFalse(result.success)
        self.assertIn("Unknown command", result.message)

    # Phase 2: Interactive Chat Tests
    def test_interactive_retrospective_flow(self):
        """Test complete interactive retrospective flow"""
        user_id = "test_user_interactive"

        # Start interactive session
        result = self.agent.process_request(
            {"command": "/retrospective create", "user_id": user_id}
        )
        self.assertTrue(result.success)
        self.assertIn("Question 1:", result.message)
        self.assertIn(user_id, self.agent.active_sessions)

        # Answer question 1
        result = self.agent.process_request(
            {
                "user_id": user_id,
                "user_input": "Completed Phase 2 implementation successfully",
            }
        )
        self.assertTrue(result.success)
        self.assertIn("Question 2:", result.message)

        # Answer question 2
        result = self.agent.process_request(
            {
                "user_id": user_id,
                "user_input": "Could have planned better to avoid analysis paralysis",
            }
        )
        self.assertTrue(result.success)
        self.assertIn("Question 3:", result.message)

        # Answer question 3
        result = self.agent.process_request(
            {
                "user_id": user_id,
                "user_input": "Focus on immediate implementation over extensive analysis",
            }
        )
        self.assertTrue(result.success)
        self.assertIn("Question 4:", result.message)  # FIX: Production has 4 questions

        # Answer question 4 (rating - completes retrospective)
        result = self.agent.process_request({"user_id": user_id, "user_input": "8"})
        self.assertTrue(result.success)
        self.assertIn("✅ Retrospective completed", result.message)
        self.assertNotIn(user_id, self.agent.active_sessions)  # Session cleaned up

    def test_chat_commands(self):
        """Test chat command routing"""
        # Test help command
        result = self.agent.process_request({"command": "/retrospective help"})
        self.assertTrue(result.success)
        self.assertIn("Chat Commands", result.message)

        # Test view command
        result = self.agent.process_request({"command": "/retrospective view"})
        self.assertTrue(result.success)

        # Test unknown chat command
        result = self.agent.process_request({"command": "/retrospective unknown"})
        self.assertFalse(result.success)
        self.assertIn("Unknown chat command", result.message)


if __name__ == "__main__":
    unittest.main()
