#!/usr/bin/env python3
"""
Personal Retrospective Chat Integration Tests
Following BLOAT_PREVENTION_SYSTEM.md and PROJECT_STRUCTURE.md

ARCHITECTURE COMPLIANCE:
- DRY: Reuses existing test patterns
- SOLID: Single responsibility for chat integration testing
- P0 Protection: Validates critical chat functionality
- Performance: <500ms response time validation
"""

import unittest
import asyncio
import tempfile
import os
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from lib.mcp.conversational_interaction_manager import (
    ConversationalInteractionManager,
    InteractionIntent,
    QueryIntent,
)
from lib.agents.personal_retrospective_agent import PersonalRetrospectiveAgent
from lib.core.types import ProcessingResult
from lib.performance import ResponseStatus


class TestPersonalRetrospectiveChatIntegration(unittest.TestCase):
    """
    Comprehensive Chat Integration Tests for Personal Retrospective

    TESTING SCOPE:
    ✅ Command recognition and routing
    ✅ Agent integration and delegation
    ✅ Database persistence validation
    ✅ Performance requirements (<500ms)
    ✅ Error handling and fallback
    ✅ End-to-end user journey
    """

    def setUp(self):
        """Set up test environment with isolated database"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_retrospective_chat.db")

        # Create chat manager with test configuration
        self.chat_manager = ConversationalInteractionManager()

        # Override retrospective agent with test database
        self.chat_manager._retrospective_agent = PersonalRetrospectiveAgent()
        self.chat_manager._retrospective_agent.db_path = self.db_path
        self.chat_manager._retrospective_agent._init_database()

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_retrospective_command_recognition(self):
        """Test that retrospective commands are correctly recognized"""
        test_cases = [
            ("/retrospective create", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("/retrospective view", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("/retrospective help", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("retrospective create", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("personal retrospective", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("weekly retrospective", InteractionIntent.RETROSPECTIVE_COMMAND),
            ("show me data", InteractionIntent.UNKNOWN),  # Should not match
        ]

        for query, expected_intent in test_cases:
            with self.subTest(query=query):
                intent = self.chat_manager._parse_query_intent(query)
                if expected_intent == InteractionIntent.RETROSPECTIVE_COMMAND:
                    self.assertEqual(
                        intent.intent,
                        expected_intent,
                        f"Query '{query}' should be recognized as retrospective command",
                    )
                    self.assertGreater(
                        intent.confidence,
                        0.0,
                        f"Query '{query}' should have confidence > 0",
                    )
                else:
                    self.assertNotEqual(
                        intent.intent,
                        InteractionIntent.RETROSPECTIVE_COMMAND,
                        f"Query '{query}' should NOT be recognized as retrospective command",
                    )

    async def test_retrospective_help_command(self):
        """Test /retrospective help command routing and response"""
        response = await self.chat_manager.process_interaction_query(
            query="/retrospective help",
            chart_id="test_chart",
            current_context={"user_id": "test_user"},
        )

        self.assertTrue(response.success, "Help command should succeed")
        self.assertEqual(response.status, ResponseStatus.SUCCESS)
        self.assertIn("Personal Retrospective Agent", response.content)
        self.assertIn("Commands:", response.content)
        self.assertIn("/retrospective create", response.content)

    async def test_retrospective_create_command(self):
        """Test /retrospective create command starts interactive session"""
        response = await self.chat_manager.process_interaction_query(
            query="/retrospective create",
            chart_id="test_chart",
            current_context={"user_id": "test_user_create"},
        )

        self.assertTrue(response.success, "Create command should succeed")
        self.assertEqual(response.status, ResponseStatus.SUCCESS)
        self.assertIn("Question 1:", response.content)
        self.assertIn("What went well", response.content)

        # Verify session was created in agent
        agent = self.chat_manager.retrospective_agent
        self.assertIn("test_user_create", agent.active_sessions)

    async def test_interactive_retrospective_flow(self):
        """Test complete interactive retrospective flow with database persistence"""
        user_id = "test_user_flow"

        # Step 1: Start retrospective
        response1 = await self.chat_manager.process_interaction_query(
            query="/retrospective create",
            chart_id="test_chart",
            current_context={"user_id": user_id},
        )
        self.assertTrue(response1.success)
        self.assertIn("Question 1:", response1.content)

        # Step 2: Answer question 1
        response2 = await self.chat_manager.process_interaction_query(
            query="Successfully implemented chat integration with zero bloat",
            chart_id="test_chart",
            current_context={"user_id": user_id},
        )
        self.assertTrue(response2.success)
        self.assertIn("Question 2:", response2.content)

        # Step 3: Answer question 2
        response3 = await self.chat_manager.process_interaction_query(
            query="Could have applied Sequential Thinking earlier in the process",
            chart_id="test_chart",
            current_context={"user_id": user_id},
        )
        self.assertTrue(response3.success)
        self.assertIn("Question 3:", response3.content)

        # Step 4: Answer question 3 (completes retrospective)
        response4 = await self.chat_manager.process_interaction_query(
            query="8",  # Sentiment score
            chart_id="test_chart",
            current_context={"user_id": user_id},
        )
        self.assertTrue(response4.success)
        self.assertIn("✅ Retrospective completed", response4.content)

        # Verify session was cleaned up
        agent = self.chat_manager.retrospective_agent
        self.assertNotIn(user_id, agent.active_sessions)

        # Verify data was persisted to database
        recent_retros = agent._get_recent_retrospectives(1)
        self.assertEqual(len(recent_retros), 1)
        self.assertIn(
            "Successfully implemented chat integration", recent_retros[0].went_well
        )
        self.assertIn(
            "Could have applied Sequential Thinking", recent_retros[0].could_improve
        )
        self.assertIn("8", recent_retros[0].next_focus)

    async def test_retrospective_view_command(self):
        """Test /retrospective view command shows stored entries"""
        # First create a retrospective entry
        agent = self.chat_manager.retrospective_agent
        test_entry_data = {
            "date": "2025-09-22",
            "went_well": "Test retrospective entry",
            "could_improve": "Test improvement area",
            "next_focus": "7",
        }
        result = agent._create_retrospective(test_entry_data)
        self.assertTrue(result.success)

        # Now test view command
        response = await self.chat_manager.process_interaction_query(
            query="/retrospective view",
            chart_id="test_chart",
            current_context={"user_id": "test_user_view"},
        )

        self.assertTrue(response.success)
        self.assertEqual(response.status, ResponseStatus.SUCCESS)
        self.assertIn("Test retrospective entry", response.content)
        self.assertIn("Test improvement area", response.content)
        self.assertIn("2025-09-22", response.content)

    async def test_performance_requirements(self):
        """Test that retrospective commands meet <500ms performance target"""
        import time

        commands = [
            "/retrospective help",
            "/retrospective view",
            "/retrospective create",
        ]

        for command in commands:
            with self.subTest(command=command):
                start_time = time.time()

                response = await self.chat_manager.process_interaction_query(
                    query=command,
                    chart_id="test_chart",
                    current_context={
                        "user_id": f"perf_test_{command.replace(' ', '_')}"
                    },
                )

                processing_time = time.time() - start_time

                self.assertTrue(response.success, f"Command {command} should succeed")
                self.assertLess(
                    processing_time,
                    0.5,
                    f"Command {command} took {processing_time:.3f}s, should be <500ms",
                )

    async def test_error_handling_and_fallback(self):
        """Test error handling for invalid commands and database issues"""
        # Test invalid retrospective command
        response = await self.chat_manager.process_interaction_query(
            query="/retrospective invalid",
            chart_id="test_chart",
            current_context={"user_id": "error_test"},
        )

        # Should still succeed with error message (graceful degradation)
        self.assertFalse(response.success)
        self.assertEqual(response.status, ResponseStatus.ERROR)
        self.assertIn("error", response.content.lower())

    def test_agent_lazy_initialization(self):
        """Test that retrospective agent is lazily initialized"""
        # Create fresh chat manager
        fresh_manager = ConversationalInteractionManager()

        # Agent should not be initialized yet
        self.assertIsNone(fresh_manager._retrospective_agent)

        # Access agent property to trigger initialization
        agent = fresh_manager.retrospective_agent

        # Now agent should be initialized
        self.assertIsNotNone(fresh_manager._retrospective_agent)
        self.assertIsInstance(agent, PersonalRetrospectiveAgent)

    async def test_context_preservation(self):
        """Test that user context is properly preserved across retrospective sessions"""
        user_id = "context_test_user"
        context = {
            "user_id": user_id,
            "session_data": {"role": "Engineering Director", "org": "UI Foundation"},
        }

        # Start retrospective with context
        response = await self.chat_manager.process_interaction_query(
            query="/retrospective create",
            chart_id="test_chart",
            current_context=context,
        )

        self.assertTrue(response.success)

        # Verify user_id was passed to agent
        agent = self.chat_manager.retrospective_agent
        self.assertIn(user_id, agent.active_sessions)

        # Verify metadata includes context information
        self.assertIn("retrospective_command", response.metadata)
        self.assertEqual(
            response.metadata["retrospective_command"], "/retrospective create"
        )


class TestRetrospectiveChatIntegrationAsync(unittest.IsolatedAsyncioTestCase):
    """Async test cases for retrospective chat integration"""

    async def asyncSetUp(self):
        """Set up async test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_async_retrospective.db")

        self.chat_manager = ConversationalInteractionManager()
        self.chat_manager._retrospective_agent = PersonalRetrospectiveAgent()
        self.chat_manager._retrospective_agent.db_path = self.db_path
        self.chat_manager._retrospective_agent._init_database()

    async def asyncTearDown(self):
        """Clean up async test environment"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    async def test_concurrent_retrospective_sessions(self):
        """Test that multiple users can have concurrent retrospective sessions"""
        user1_id = "concurrent_user_1"
        user2_id = "concurrent_user_2"

        # Start concurrent sessions
        response1 = await self.chat_manager.process_interaction_query(
            query="/retrospective create",
            chart_id="chart1",
            current_context={"user_id": user1_id},
        )

        response2 = await self.chat_manager.process_interaction_query(
            query="/retrospective create",
            chart_id="chart2",
            current_context={"user_id": user2_id},
        )

        # Both should succeed
        self.assertTrue(response1.success)
        self.assertTrue(response2.success)

        # Both sessions should exist
        agent = self.chat_manager.retrospective_agent
        self.assertIn(user1_id, agent.active_sessions)
        self.assertIn(user2_id, agent.active_sessions)

        # Sessions should be independent
        self.assertNotEqual(
            agent.active_sessions[user1_id]["date"],
            agent.active_sessions[user2_id]["date"],
        )


if __name__ == "__main__":
    # Run sync tests
    unittest.main(verbosity=2)
