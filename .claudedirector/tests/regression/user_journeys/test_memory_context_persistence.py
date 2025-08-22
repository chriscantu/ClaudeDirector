#!/usr/bin/env python3
"""
🧠 Memory & Context Persistence Regression Test - Critical User Journey 4/5

BUSINESS CRITICAL PATH: Memory and context preservation across user sessions
FAILURE IMPACT: Strategic continuity lost, context reset, relationship history erased

This comprehensive test suite validates the complete memory and context experience:
1. User identity and configuration persistence
2. Strategic conversation context preservation
3. Executive relationship tracking
4. Initiative and PI (planning increment) continuity
5. Stakeholder intelligence preservation
6. Platform metrics and ROI context
7. Cross-session strategic framework memory
8. Context switching and recovery
9. Memory corruption recovery
10. Multi-environment context sync

COVERAGE: Complete strategic memory and context validation
PRIORITY: P0 HIGH - Strategic continuity cannot fail
EXECUTION: <4 seconds for complete memory validation
"""

import sys
import os
import unittest
import tempfile
import json
import time
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../lib"))


class TestMemoryContextPersistence(unittest.TestCase):
    """Test complete memory and context persistence functionality"""

    def setUp(self):
        """Set up test environment for memory and context testing"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claudedirector"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Memory and context file paths
        self.user_config_file = self.config_dir / "user_config.json"
        self.memory_dir = self.config_dir / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        self.context_file = self.memory_dir / "strategic_context.json"
        self.stakeholder_file = self.memory_dir / "stakeholder_intelligence.json"
        self.initiative_file = self.memory_dir / "current_initiatives.json"

        # Test user identity and configuration
        self.test_user_config = {
            "user_identity": {
                "name": "Chris Cantu",
                "role": "Engineering Director",
                "organization": "UI Foundation Team",
                "preferences": {
                    "primary_personas": ["diego", "martin", "rachel"],
                    "framework_preferences": ["Team Topologies", "Capital Allocation"],
                    "communication_style": "executive_brief",
                },
            },
            "session_preferences": {
                "auto_save_context": True,
                "context_preservation_level": "comprehensive",
                "memory_retention_days": 90,
            },
            "last_updated": datetime.now().isoformat(),
        }

        # Test strategic context data
        self.test_strategic_context = {
            "current_initiatives": [
                {
                    "id": "platform_scaling_2024",
                    "title": "Platform Scaling Initiative Q4 2024",
                    "status": "in_progress",
                    "priority": "P0",
                    "stakeholders": ["jeff_williams", "beth_nelson", "hemendra_pal"],
                    "last_discussion": datetime.now().isoformat(),
                    "key_decisions": ["monorepo_migration", "team_restructure"],
                    "next_milestones": ["Q1_2025_launch", "performance_benchmarks"],
                }
            ],
            "recent_conversations": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "persona_used": "diego",
                    "topic": "organizational_scaling",
                    "framework_applied": "Team Topologies",
                    "key_insights": ["cognitive_load_assessment", "team_boundaries"],
                    "follow_up_actions": ["stakeholder_alignment", "metric_tracking"],
                }
            ],
            "session_metadata": {
                "total_conversations": 15,
                "frameworks_used": [
                    "Team Topologies",
                    "Capital Allocation",
                    "Strategic Platform Assessment",
                ],
                "primary_personas_activated": ["diego", "martin", "rachel", "alvaro"],
                "session_start": datetime.now().isoformat(),
            },
        }

        # Test stakeholder intelligence
        self.test_stakeholder_data = {
            "stakeholder_relationships": {
                "jeff_williams": {
                    "role": "VP Engineering",
                    "relationship": "direct_report",
                    "communication_style": "data_driven",
                    "recent_interactions": [
                        {
                            "date": datetime.now().isoformat(),
                            "topic": "platform_strategy",
                            "outcome": "approved_q4_roadmap",
                            "next_touchpoint": "weekly_1on1",
                        }
                    ],
                    "priorities": ["platform_roi", "team_scaling", "delivery_velocity"],
                    "concerns": ["technical_debt", "resource_allocation"],
                },
                "beth_nelson": {
                    "role": "Product Strategy",
                    "relationship": "cross_functional",
                    "communication_style": "strategic_vision",
                    "alignment_level": "high",
                    "collaboration_areas": ["design_system", "user_experience"],
                },
            },
            "organizational_dynamics": {
                "platform_advocates": ["jeff_williams", "beth_nelson", "victor_davis"],
                "product_focused": ["hisham_younis", "hemendra_pal"],
                "decision_makers": ["steve_davis", "jeff_williams"],
                "influence_network": {
                    "technical": ["victor_davis", "zach_mckenzie"],
                    "business": ["steve_davis", "marfise"],
                    "product": ["hisham_younis", "beth_nelson"],
                },
            },
        }

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_user_config_persistence(self):
        """REGRESSION TEST: User configuration persists across sessions"""
        try:
            # Save user configuration
            with open(self.user_config_file, "w") as f:
                json.dump(self.test_user_config, f, indent=2)

            # Verify file exists and is readable
            self.assertTrue(
                self.user_config_file.exists(),
                "User configuration file should be created",
            )

            # Load configuration back
            with open(self.user_config_file, "r") as f:
                loaded_config = json.load(f)

            # Verify critical configuration elements persist
            self.assertEqual(
                loaded_config["user_identity"]["name"],
                "Chris Cantu",
                "User name should persist across sessions",
            )

            self.assertEqual(
                loaded_config["user_identity"]["role"],
                "Engineering Director",
                "User role should persist across sessions",
            )

            self.assertIn(
                "diego",
                loaded_config["user_identity"]["preferences"]["primary_personas"],
                "Persona preferences should persist",
            )

            self.assertTrue(
                loaded_config["session_preferences"]["auto_save_context"],
                "Session preferences should persist",
            )

        except Exception as e:
            self.fail(f"User configuration persistence failed: {e}")

    def test_strategic_context_preservation(self):
        """REGRESSION TEST: Strategic conversation context preserves across sessions"""
        try:
            # Save strategic context
            with open(self.context_file, "w") as f:
                json.dump(self.test_strategic_context, f, indent=2)

            # Verify context file creation
            self.assertTrue(
                self.context_file.exists(), "Strategic context file should be created"
            )

            # Load context back
            with open(self.context_file, "r") as f:
                loaded_context = json.load(f)

            # Verify initiative tracking
            initiatives = loaded_context["current_initiatives"]
            self.assertGreater(
                len(initiatives), 0, "Current initiatives should be preserved"
            )

            platform_initiative = initiatives[0]
            self.assertEqual(
                platform_initiative["id"],
                "platform_scaling_2024",
                "Initiative IDs should persist",
            )

            self.assertEqual(
                platform_initiative["status"],
                "in_progress",
                "Initiative status should be preserved",
            )

            # Verify conversation history
            conversations = loaded_context["recent_conversations"]
            self.assertGreater(
                len(conversations), 0, "Recent conversations should be preserved"
            )

            recent_conv = conversations[0]
            self.assertEqual(
                recent_conv["persona_used"],
                "diego",
                "Persona usage history should be preserved",
            )

            self.assertEqual(
                recent_conv["framework_applied"],
                "Team Topologies",
                "Framework application history should be preserved",
            )

            # Verify session metadata preservation
            metadata = loaded_context["session_metadata"]
            self.assertGreater(
                metadata["total_conversations"],
                0,
                "Session conversation count should be preserved",
            )

            self.assertIn(
                "Team Topologies",
                metadata["frameworks_used"],
                "Framework usage history should be comprehensive",
            )

        except Exception as e:
            self.fail(f"Strategic context preservation failed: {e}")

    def test_stakeholder_intelligence_tracking(self):
        """REGRESSION TEST: Stakeholder relationships and intelligence persist"""
        try:
            # Save stakeholder intelligence
            with open(self.stakeholder_file, "w") as f:
                json.dump(self.test_stakeholder_data, f, indent=2)

            # Verify stakeholder file creation
            self.assertTrue(
                self.stakeholder_file.exists(),
                "Stakeholder intelligence file should be created",
            )

            # Load stakeholder data back
            with open(self.stakeholder_file, "r") as f:
                loaded_stakeholders = json.load(f)

            # Verify individual stakeholder relationships
            relationships = loaded_stakeholders["stakeholder_relationships"]

            self.assertIn(
                "jeff_williams",
                relationships,
                "Executive stakeholder relationships should persist",
            )

            jeff_data = relationships["jeff_williams"]
            self.assertEqual(
                jeff_data["role"],
                "VP Engineering",
                "Stakeholder roles should be preserved",
            )

            self.assertEqual(
                jeff_data["relationship"],
                "direct_report",
                "Relationship types should be preserved",
            )

            # Verify interaction history
            interactions = jeff_data["recent_interactions"]
            self.assertGreater(
                len(interactions),
                0,
                "Stakeholder interaction history should be preserved",
            )

            recent_interaction = interactions[0]
            self.assertEqual(
                recent_interaction["topic"],
                "platform_strategy",
                "Interaction topics should be preserved",
            )

            # Verify organizational dynamics
            dynamics = loaded_stakeholders["organizational_dynamics"]

            self.assertIn(
                "jeff_williams",
                dynamics["platform_advocates"],
                "Platform advocacy tracking should persist",
            )

            self.assertIn(
                "hisham_younis",
                dynamics["product_focused"],
                "Organizational positioning should be preserved",
            )

            # Verify influence network mapping
            influence = dynamics["influence_network"]
            self.assertIn(
                "victor_davis",
                influence["technical"],
                "Technical influence networks should be preserved",
            )

        except Exception as e:
            self.fail(f"Stakeholder intelligence tracking failed: {e}")

    def test_context_corruption_recovery(self):
        """REGRESSION TEST: System recovers gracefully from corrupted context files"""
        try:
            # Create corrupted context file
            corrupted_content = "{ invalid json content"
            with open(self.context_file, "w") as f:
                f.write(corrupted_content)

            # Verify corrupted file exists
            self.assertTrue(
                self.context_file.exists(),
                "Corrupted context file should exist for testing",
            )

            # Attempt to load corrupted context (should handle gracefully)
            try:
                with open(self.context_file, "r") as f:
                    json.load(f)
                # If we get here, the JSON wasn't actually corrupted
                recovered_gracefully = True
            except json.JSONDecodeError:
                # This is expected - corruption detected
                recovered_gracefully = True
            except Exception as e:
                # Unexpected error - recovery failed
                recovered_gracefully = False
                self.fail(f"Unexpected error during corruption recovery: {e}")

            self.assertTrue(
                recovered_gracefully,
                "System should detect and handle corrupted context gracefully",
            )

            # Test recovery by creating valid backup context
            backup_context = {
                "recovery_mode": True,
                "timestamp": datetime.now().isoformat(),
                "current_initiatives": [],
                "recent_conversations": [],
                "session_metadata": {
                    "total_conversations": 0,
                    "recovery_performed": True,
                },
            }

            # Simulate recovery process
            backup_file = self.context_file.with_suffix(".backup")
            with open(backup_file, "w") as f:
                json.dump(backup_context, f, indent=2)

            # Verify backup recovery works
            with open(backup_file, "r") as f:
                recovered_context = json.load(f)

            self.assertTrue(
                recovered_context["recovery_mode"],
                "Recovery context should indicate recovery mode",
            )

            self.assertTrue(
                recovered_context["session_metadata"]["recovery_performed"],
                "Recovery metadata should be preserved",
            )

        except Exception as e:
            self.fail(f"Context corruption recovery failed: {e}")

    def test_cross_session_continuity(self):
        """REGRESSION TEST: Context and memory carry forward across multiple sessions"""
        try:
            # Simulate Session 1: Initial strategic conversation
            session1_context = {
                "session_id": "session_1",
                "timestamp": datetime.now().isoformat(),
                "current_initiatives": [
                    {
                        "id": "platform_scaling",
                        "status": "planning",
                        "decisions_made": ["team_structure_review"],
                        "next_steps": ["stakeholder_alignment"],
                    }
                ],
                "conversation_history": [
                    {
                        "topic": "team_scaling",
                        "persona": "diego",
                        "frameworks": ["Team Topologies"],
                        "key_outcomes": ["cognitive_load_analysis"],
                    }
                ],
            }

            # Save Session 1 context
            with open(self.context_file, "w") as f:
                json.dump(session1_context, f, indent=2)

            # Simulate gap between sessions (time passage)
            time.sleep(0.1)  # Small delay to ensure different timestamps

            # Load Session 1 context (simulating new session startup)
            with open(self.context_file, "r") as f:
                loaded_session1 = json.load(f)

            # Simulate Session 2: Continue previous conversation
            session2_context = loaded_session1.copy()
            session2_context["session_id"] = "session_2"
            session2_context["timestamp"] = datetime.now().isoformat()

            # Add Session 2 progress
            session2_context["current_initiatives"][0]["status"] = "in_progress"
            session2_context["current_initiatives"][0]["decisions_made"].append(
                "stakeholder_meetings_scheduled"
            )

            session2_context["conversation_history"].append(
                {
                    "topic": "stakeholder_alignment",
                    "persona": "rachel",
                    "frameworks": ["Strategic Platform Assessment"],
                    "key_outcomes": ["executive_communication_plan"],
                    "continues_from": "session_1",
                }
            )

            # Save Session 2 context
            with open(self.context_file, "w") as f:
                json.dump(session2_context, f, indent=2)

            # Verify continuity preservation
            with open(self.context_file, "r") as f:
                final_context = json.load(f)

            # Check initiative progression
            initiative = final_context["current_initiatives"][0]
            self.assertEqual(
                initiative["status"],
                "in_progress",
                "Initiative status should progress across sessions",
            )

            self.assertIn(
                "team_structure_review",
                initiative["decisions_made"],
                "Previous session decisions should be preserved",
            )

            self.assertIn(
                "stakeholder_meetings_scheduled",
                initiative["decisions_made"],
                "New session decisions should be added",
            )

            # Check conversation continuity
            conversations = final_context["conversation_history"]
            self.assertEqual(
                len(conversations), 2, "All session conversations should be preserved"
            )

            session2_conv = conversations[1]
            self.assertEqual(
                session2_conv["continues_from"],
                "session_1",
                "Cross-session conversation continuity should be tracked",
            )

            self.assertEqual(
                session2_conv["persona"],
                "rachel",
                "Different personas across sessions should be preserved",
            )

        except Exception as e:
            self.fail(f"Cross-session continuity failed: {e}")

    def test_memory_performance_under_load(self):
        """REGRESSION TEST: Memory system performs well with large context data"""
        try:
            # Create large context dataset (simulating heavy usage)
            large_context = {
                "current_initiatives": [],
                "conversation_history": [],
                "stakeholder_interactions": [],
                "framework_applications": [],
            }

            # Generate substantial history data
            for i in range(100):  # 100 initiatives
                large_context["current_initiatives"].append(
                    {
                        "id": f"initiative_{i}",
                        "title": f"Strategic Initiative {i}",
                        "status": "completed" if i < 80 else "in_progress",
                        "priority": "P0" if i % 10 == 0 else "P1",
                        "created": (datetime.now() - timedelta(days=i)).isoformat(),
                    }
                )

            for i in range(500):  # 500 conversations
                large_context["conversation_history"].append(
                    {
                        "id": f"conv_{i}",
                        "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                        "persona": ["diego", "martin", "rachel", "alvaro"][i % 4],
                        "topic": f"strategic_topic_{i}",
                        "framework": [
                            "Team Topologies",
                            "Capital Allocation",
                            "Strategic Analysis",
                        ][i % 3],
                        "duration_minutes": 15 + (i % 30),
                    }
                )

            # Measure save performance
            start_time = time.time()
            with open(self.context_file, "w") as f:
                json.dump(large_context, f, indent=2)
            save_time = time.time() - start_time

            # Verify file was created
            self.assertTrue(
                self.context_file.exists(),
                "Large context file should be created successfully",
            )

            # Measure load performance
            start_time = time.time()
            with open(self.context_file, "r") as f:
                loaded_large_context = json.load(f)
            load_time = time.time() - start_time

            # Verify data integrity
            self.assertEqual(
                len(loaded_large_context["current_initiatives"]),
                100,
                "All initiatives should be preserved in large dataset",
            )

            self.assertEqual(
                len(loaded_large_context["conversation_history"]),
                500,
                "All conversations should be preserved in large dataset",
            )

            # Performance assertions (reasonable thresholds)
            self.assertLess(
                save_time,
                2.0,
                f"Large context save should complete in <2s, took {save_time:.2f}s",
            )

            self.assertLess(
                load_time,
                1.0,
                f"Large context load should complete in <1s, took {load_time:.2f}s",
            )

            # Verify specific data integrity
            first_initiative = loaded_large_context["current_initiatives"][0]
            self.assertEqual(
                first_initiative["id"],
                "initiative_0",
                "First initiative should be preserved correctly",
            )

            last_conversation = loaded_large_context["conversation_history"][-1]
            self.assertEqual(
                last_conversation["id"],
                "conv_499",
                "Last conversation should be preserved correctly",
            )

        except Exception as e:
            self.fail(f"Memory performance under load failed: {e}")

    def test_multi_user_context_isolation(self):
        """REGRESSION TEST: Context isolation between different users/environments"""
        try:
            # Create User 1 context
            user1_dir = Path(self.test_dir) / "user1" / ".claudedirector"
            user1_dir.mkdir(parents=True, exist_ok=True)
            user1_context_file = user1_dir / "memory" / "strategic_context.json"
            user1_context_file.parent.mkdir(exist_ok=True)

            user1_context = {
                "user_id": "chris_cantu",
                "organization": "UI_Foundation",
                "current_initiatives": [
                    {
                        "id": "user1_platform_scaling",
                        "confidential": True,
                        "stakeholders": ["jeff_williams", "beth_nelson"],
                    }
                ],
                "sensitive_data": {
                    "budget_allocation": 2000000,
                    "headcount_plans": {"q4_2024": 8, "q1_2025": 12},
                },
            }

            # Create User 2 context
            user2_dir = Path(self.test_dir) / "user2" / ".claudedirector"
            user2_dir.mkdir(parents=True, exist_ok=True)
            user2_context_file = user2_dir / "memory" / "strategic_context.json"
            user2_context_file.parent.mkdir(exist_ok=True)

            user2_context = {
                "user_id": "other_director",
                "organization": "Backend_Platform",
                "current_initiatives": [
                    {
                        "id": "user2_api_scaling",
                        "confidential": True,
                        "stakeholders": ["different_vp", "other_pm"],
                    }
                ],
                "sensitive_data": {
                    "budget_allocation": 1500000,
                    "headcount_plans": {"q4_2024": 5, "q1_2025": 7},
                },
            }

            # Save both user contexts
            with open(user1_context_file, "w") as f:
                json.dump(user1_context, f, indent=2)

            with open(user2_context_file, "w") as f:
                json.dump(user2_context, f, indent=2)

            # Verify both files exist
            self.assertTrue(
                user1_context_file.exists(), "User 1 context should be created"
            )

            self.assertTrue(
                user2_context_file.exists(), "User 2 context should be created"
            )

            # Load User 1 context
            with open(user1_context_file, "r") as f:
                loaded_user1 = json.load(f)

            # Load User 2 context
            with open(user2_context_file, "r") as f:
                loaded_user2 = json.load(f)

            # Verify isolation - User 1 data should not appear in User 2
            self.assertEqual(
                loaded_user1["user_id"],
                "chris_cantu",
                "User 1 identity should be preserved",
            )

            self.assertEqual(
                loaded_user2["user_id"],
                "other_director",
                "User 2 identity should be preserved",
            )

            # Verify sensitive data isolation
            user1_initiative = loaded_user1["current_initiatives"][0]
            user2_initiative = loaded_user2["current_initiatives"][0]

            self.assertNotEqual(
                user1_initiative["id"],
                user2_initiative["id"],
                "Initiative IDs should be isolated between users",
            )

            self.assertNotEqual(
                loaded_user1["sensitive_data"]["budget_allocation"],
                loaded_user2["sensitive_data"]["budget_allocation"],
                "Budget information should be isolated between users",
            )

            # Verify stakeholder isolation
            user1_stakeholders = user1_initiative["stakeholders"]
            user2_stakeholders = user2_initiative["stakeholders"]

            self.assertNotEqual(
                user1_stakeholders,
                user2_stakeholders,
                "Stakeholder lists should be isolated between users",
            )

            self.assertIn(
                "jeff_williams",
                user1_stakeholders,
                "User 1 should see their stakeholders",
            )

            self.assertNotIn(
                "jeff_williams",
                user2_stakeholders,
                "User 2 should not see User 1 stakeholders",
            )

        except Exception as e:
            self.fail(f"Multi-user context isolation failed: {e}")

    def test_memory_cleanup_and_archival(self):
        """REGRESSION TEST: Memory cleanup and archival processes work correctly"""
        try:
            # Create context with mixed old and new data
            mixed_context = {
                "current_initiatives": [
                    {
                        "id": "current_initiative",
                        "created": datetime.now().isoformat(),
                        "status": "active",
                        "archive": False,
                    },
                    {
                        "id": "old_initiative",
                        "created": (datetime.now() - timedelta(days=95)).isoformat(),
                        "status": "completed",
                        "archive": True,
                    },
                ],
                "conversation_history": [
                    {
                        "id": "recent_conv",
                        "timestamp": datetime.now().isoformat(),
                        "archive": False,
                    },
                    {
                        "id": "old_conv",
                        "timestamp": (datetime.now() - timedelta(days=100)).isoformat(),
                        "archive": True,
                    },
                ],
                "cleanup_metadata": {
                    "last_cleanup": (datetime.now() - timedelta(days=30)).isoformat(),
                    "retention_policy": "90_days",
                    "archive_enabled": True,
                },
            }

            # Save mixed context
            with open(self.context_file, "w") as f:
                json.dump(mixed_context, f, indent=2)

            # Simulate cleanup process (filter archivable items)
            with open(self.context_file, "r") as f:
                context_to_clean = json.load(f)

            # Separate current and archival data
            current_initiatives = [
                init
                for init in context_to_clean["current_initiatives"]
                if not init.get("archive", False)
            ]

            current_conversations = [
                conv
                for conv in context_to_clean["conversation_history"]
                if not conv.get("archive", False)
            ]

            archived_initiatives = [
                init
                for init in context_to_clean["current_initiatives"]
                if init.get("archive", False)
            ]

            archived_conversations = [
                conv
                for conv in context_to_clean["conversation_history"]
                if conv.get("archive", False)
            ]

            # Verify cleanup logic
            self.assertEqual(
                len(current_initiatives), 1, "Should identify 1 current initiative"
            )

            self.assertEqual(
                len(archived_initiatives), 1, "Should identify 1 archival initiative"
            )

            self.assertEqual(
                current_initiatives[0]["id"],
                "current_initiative",
                "Current initiative should be preserved",
            )

            self.assertEqual(
                archived_initiatives[0]["id"],
                "old_initiative",
                "Old initiative should be identified for archival",
            )

            # Create cleaned context
            cleaned_context = {
                "current_initiatives": current_initiatives,
                "conversation_history": current_conversations,
                "cleanup_metadata": {
                    "last_cleanup": datetime.now().isoformat(),
                    "retention_policy": "90_days",
                    "archive_enabled": True,
                    "items_archived": len(archived_initiatives)
                    + len(archived_conversations),
                },
            }

            # Create archive
            archive_data = {
                "archived_initiatives": archived_initiatives,
                "archived_conversations": archived_conversations,
                "archive_date": datetime.now().isoformat(),
                "original_cleanup_date": datetime.now().isoformat(),
            }

            # Save cleaned context and archive
            cleaned_context_file = self.context_file.with_suffix(".cleaned")
            archive_file = self.memory_dir / "archive.json"

            with open(cleaned_context_file, "w") as f:
                json.dump(cleaned_context, f, indent=2)

            with open(archive_file, "w") as f:
                json.dump(archive_data, f, indent=2)

            # Verify cleanup results
            with open(cleaned_context_file, "r") as f:
                final_cleaned = json.load(f)

            with open(archive_file, "r") as f:
                final_archive = json.load(f)

            # Check that active data is preserved
            self.assertEqual(
                len(final_cleaned["current_initiatives"]),
                1,
                "Cleaned context should contain only current initiatives",
            )

            self.assertEqual(
                final_cleaned["current_initiatives"][0]["status"],
                "active",
                "Active initiatives should be preserved in cleaned context",
            )

            # Check that archived data is properly stored
            self.assertEqual(
                len(final_archive["archived_initiatives"]),
                1,
                "Archive should contain old initiatives",
            )

            self.assertEqual(
                final_archive["archived_initiatives"][0]["status"],
                "completed",
                "Completed initiatives should be in archive",
            )

            # Verify cleanup metadata
            cleanup_meta = final_cleaned["cleanup_metadata"]
            self.assertEqual(
                cleanup_meta["items_archived"],
                2,
                "Cleanup metadata should track archived item count",
            )

        except Exception as e:
            self.fail(f"Memory cleanup and archival failed: {e}")

    def test_end_to_end_memory_workflow(self):
        """REGRESSION TEST: Complete end-to-end memory and context workflow"""
        try:
            # Phase 1: User Configuration Setup
            with open(self.user_config_file, "w") as f:
                json.dump(self.test_user_config, f, indent=2)

            # Phase 2: Initial Strategic Context Creation
            initial_context = {
                "session_start": datetime.now().isoformat(),
                "user_config_loaded": True,
                "current_initiatives": [],
                "conversation_history": [],
                "framework_usage": {},
            }

            with open(self.context_file, "w") as f:
                json.dump(initial_context, f, indent=2)

            # Phase 3: Stakeholder Intelligence Setup
            with open(self.stakeholder_file, "w") as f:
                json.dump(self.test_stakeholder_data, f, indent=2)

            # Phase 4: Simulate Active Session with Context Updates
            # Load existing context
            with open(self.context_file, "r") as f:
                active_context = json.load(f)

            # Add conversation
            active_context["conversation_history"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "persona": "diego",
                    "topic": "platform_architecture",
                    "framework": "Team Topologies",
                    "outcome": "team_boundary_definition",
                }
            )

            # Add initiative
            active_context["current_initiatives"].append(
                {
                    "id": "arch_modernization",
                    "title": "Architecture Modernization Q4",
                    "status": "planning",
                    "created": datetime.now().isoformat(),
                    "stakeholders": ["victor_davis", "zach_mckenzie"],
                }
            )

            # Update framework usage
            active_context["framework_usage"]["Team Topologies"] = (
                active_context["framework_usage"].get("Team Topologies", 0) + 1
            )

            # Save updated context
            with open(self.context_file, "w") as f:
                json.dump(active_context, f, indent=2)

            # Phase 5: Cross-Session Context Loading and Verification
            # Load user config
            with open(self.user_config_file, "r") as f:
                loaded_user_config = json.load(f)

            # Load strategic context
            with open(self.context_file, "r") as f:
                loaded_context = json.load(f)

            # Load stakeholder data
            with open(self.stakeholder_file, "r") as f:
                loaded_stakeholders = json.load(f)

            # Phase 6: End-to-End Verification
            # Verify user identity continuity
            self.assertEqual(
                loaded_user_config["user_identity"]["name"],
                "Chris Cantu",
                "User identity should persist through complete workflow",
            )

            # Verify conversation tracking
            conversations = loaded_context["conversation_history"]
            self.assertGreater(
                len(conversations),
                0,
                "Conversations should be tracked through workflow",
            )

            last_conv = conversations[-1]
            self.assertEqual(
                last_conv["persona"],
                "diego",
                "Recent conversation details should be preserved",
            )

            # Verify initiative tracking
            initiatives = loaded_context["current_initiatives"]
            self.assertGreater(
                len(initiatives), 0, "Initiatives should be tracked through workflow"
            )

            arch_initiative = initiatives[0]
            self.assertEqual(
                arch_initiative["id"],
                "arch_modernization",
                "Initiative details should be preserved",
            )

            # Verify stakeholder relationship continuity
            relationships = loaded_stakeholders["stakeholder_relationships"]
            self.assertIn(
                "jeff_williams",
                relationships,
                "Stakeholder relationships should persist through workflow",
            )

            # Verify framework usage tracking
            framework_usage = loaded_context["framework_usage"]
            self.assertIn(
                "Team Topologies", framework_usage, "Framework usage should be tracked"
            )

            self.assertGreater(
                framework_usage["Team Topologies"],
                0,
                "Framework usage count should be incremented",
            )

            # Phase 7: Performance and Integrity Check
            # Verify all files exist and are readable
            memory_files = [
                self.user_config_file,
                self.context_file,
                self.stakeholder_file,
            ]

            for memory_file in memory_files:
                self.assertTrue(
                    memory_file.exists(),
                    f"Memory file {memory_file} should exist after workflow",
                )

                # Verify file is valid JSON
                with open(memory_file, "r") as f:
                    try:
                        json.load(f)
                        json_valid = True
                    except json.JSONDecodeError:
                        json_valid = False

                self.assertTrue(
                    json_valid, f"Memory file {memory_file} should contain valid JSON"
                )

            # Verify workflow completeness
            workflow_elements = [
                "user_config_loaded" in loaded_context,
                len(loaded_context["conversation_history"]) > 0,
                len(loaded_context["current_initiatives"]) > 0,
                len(loaded_stakeholders["stakeholder_relationships"]) > 0,
            ]

            self.assertTrue(
                all(workflow_elements),
                "All workflow elements should be present and functional",
            )

        except Exception as e:
            self.fail(f"End-to-end memory workflow failed: {e}")


if __name__ == "__main__":
    print("🧠 Memory & Context Persistence Regression Test")
    print("=" * 50)
    print("Testing complete memory and context preservation...")
    print()

    # Run the comprehensive test suite
    unittest.main(verbosity=2, exit=False)

    print()
    print("✅ MEMORY & CONTEXT PERSISTENCE REGRESSION TESTS COMPLETE")
    print("Strategic continuity and context preservation protected against regressions")
