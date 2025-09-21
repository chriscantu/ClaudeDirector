#!/usr/bin/env python3
"""
Simple Personal Retrospective System Test
Tests the basic 3-question personal retrospective functionality

TEST FOCUS:
1. 3 questions work correctly (Progress, Improvement, Rating)
2. Personal responses are stored in session
3. No business intelligence features - personal reflection only
4. Simple session management works
"""

import unittest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add project paths for testing
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Test imports for simple personal retrospective system
try:
    from reporting.retrospective_enabled_chat_reporter import (
        PersonalRetrospectiveSystem,
        RetrospectiveStep,
        RetrospectiveSession,
        create_personal_retrospective_system,
    )

    RETROSPECTIVE_AVAILABLE = True
except ImportError as e:
    RETROSPECTIVE_AVAILABLE = False
    print(f"Personal retrospective system not available: {e}")


class TestSimplePersonalRetrospective(unittest.TestCase):
    """Test simple personal retrospective system - 3 questions only"""

    def setUp(self):
        """Set up test environment"""
        self.config_path = "test_config"

    def test_personal_retrospective_creation(self):
        """Test that personal retrospective system can be created"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Personal retrospective system not available")

        # Create simple retrospective system
        retrospective_system = create_personal_retrospective_system(self.config_path)

        # Verify initialization
        self.assertIsNotNone(retrospective_system)
        self.assertEqual(retrospective_system.config_path, self.config_path)

        # Verify 3 commands are available
        self.assertTrue(hasattr(retrospective_system, "commands"))
        self.assertEqual(len(retrospective_system.commands), 3)
        self.assertIn("/retrospective", retrospective_system.commands)
        self.assertIn("/weekly-retrospective", retrospective_system.commands)
        self.assertIn("/reflection", retrospective_system.commands)

        print("✅ Personal Retrospective: System created successfully with 3 commands")

    def test_retrospective_session_data(self):
        """Test that retrospective session stores personal responses correctly"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Personal retrospective system not available")

        # Create retrospective session
        from datetime import datetime

        session = RetrospectiveSession(
            session_id="test_session",
            current_step=RetrospectiveStep.PROGRESS,
            week_ending="2025-09-21",
            created_at=datetime.now(),
        )

        # Verify session structure
        self.assertEqual(session.session_id, "test_session")
        self.assertEqual(session.current_step, RetrospectiveStep.PROGRESS)
        self.assertEqual(session.week_ending, "2025-09-21")
        self.assertIsInstance(session.responses, dict)

        # Test storing personal responses
        session.responses["progress"] = "Completed 3 major tasks this week"
        session.responses["improvement"] = "Could have better time management"
        session.responses["rating"] = "7"
        session.responses["rating_explanation"] = (
            "Good progress but missed one deadline"
        )

        # Verify responses stored
        self.assertEqual(len(session.responses), 4)
        self.assertIn("progress", session.responses)
        self.assertIn("improvement", session.responses)
        self.assertIn("rating", session.responses)
        self.assertIn("rating_explanation", session.responses)

        print("✅ Personal Retrospective: Session data storage works correctly")

    def test_no_business_intelligence_features(self):
        """Test that no business intelligence features are present"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Personal retrospective system not available")

        retrospective_system = create_personal_retrospective_system(self.config_path)

        # Verify NO business intelligence features
        self.assertFalse(hasattr(retrospective_system, "jira_client"))
        self.assertFalse(hasattr(retrospective_system, "strategic_analyzer"))
        self.assertFalse(hasattr(retrospective_system, "business_metrics"))
        self.assertFalse(hasattr(retrospective_system, "roi_calculator"))
        self.assertFalse(hasattr(retrospective_system, "analytics_engine"))

        # Verify simple session management only
        self.assertTrue(hasattr(retrospective_system, "active_sessions"))
        self.assertIsInstance(retrospective_system.active_sessions, dict)

        print("✅ Personal Retrospective: No business intelligence features present")

    async def test_basic_retrospective_flow(self):
        """Test basic retrospective command flow"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Personal retrospective system not available")

        retrospective_system = create_personal_retrospective_system(self.config_path)

        # Test starting a retrospective
        response = await retrospective_system.process_command("/retrospective")

        # Should be successful and start with question 1
        self.assertTrue(response.success)
        self.assertIn("Question 1 of 3", response.message)
        self.assertIn("What progress did you make this week?", response.message)

        # Verify session was created
        self.assertEqual(len(retrospective_system.active_sessions), 1)

        print("✅ Personal Retrospective: Basic command flow works")

    def test_three_question_flow(self):
        """Test that all 3 questions are handled correctly"""

        # Test the 3 retrospective steps
        steps = [
            RetrospectiveStep.PROGRESS,
            RetrospectiveStep.IMPROVEMENT,
            RetrospectiveStep.RATING,
            RetrospectiveStep.COMPLETE,
        ]

        # Verify all steps exist
        for step in steps:
            self.assertIsInstance(step, RetrospectiveStep)

        # Verify step names match the 3 questions
        self.assertEqual(RetrospectiveStep.PROGRESS.value, "progress")
        self.assertEqual(RetrospectiveStep.IMPROVEMENT.value, "improvement")
        self.assertEqual(RetrospectiveStep.RATING.value, "rating")
        self.assertEqual(RetrospectiveStep.COMPLETE.value, "complete")

        print("✅ Personal Retrospective: 3-question flow structure correct")


def run_async_test(test_method):
    """Helper to run async test methods"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_method())
    finally:
        loop.close()


if __name__ == "__main__":
    # Run the async test manually
    test_instance = TestSimplePersonalRetrospective()
    test_instance.setUp()

    print("Running Simple Personal Retrospective Tests...")

    # Run synchronous tests
    test_instance.test_personal_retrospective_creation()
    test_instance.test_retrospective_session_data()
    test_instance.test_no_business_intelligence_features()
    test_instance.test_three_question_flow()

    # Run async test
    run_async_test(test_instance.test_basic_retrospective_flow)

    print("\n🎉 All Simple Personal Retrospective Tests Passed!")
    print("✅ Focus: 3 questions only - Progress, Improvement, Rating")
    print("✅ No business intelligence features")
    print("✅ Simple personal reflection system working correctly")
