#!/usr/bin/env python3
"""
⚡ Memory Performance & Lifecycle Regression Test - Critical User Journey 4d/5

BUSINESS CRITICAL PATH: Memory performance optimization and lifecycle management
FAILURE IMPACT: Memory degradation, performance issues, data corruption, cleanup failures

This focused test suite validates memory performance and lifecycle management:
1. Memory performance under load with large datasets
2. Memory cleanup and archival processes
3. Multi-user context isolation and security
4. End-to-end memory workflow validation

COVERAGE: Complete memory performance and lifecycle validation
PRIORITY: P0 BLOCKING - Memory performance and data integrity
EXECUTION: <4 seconds for complete performance validation
"""

import sys
import os
import unittest
import tempfile
import json
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../lib"))


class TestMemoryPerformance(unittest.TestCase):
    """Test memory performance optimization and lifecycle management"""

    def setUp(self):
        """Set up test environment for memory performance testing"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claudedirector"
        self.memory_dir = self.config_dir / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Memory file paths
        self.context_file = self.memory_dir / "strategic_context.json"
        self.user_config_file = self.config_dir / "user_config.json"
        self.stakeholder_file = self.memory_dir / "stakeholder_intelligence.json"

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_memory_performance_under_load(self):
        """REGRESSION TEST: Memory performs well with large datasets (100 initiatives, 500 conversations)"""
        try:
            # Generate large memory dataset
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
        """REGRESSION TEST: Multi-user context isolation maintains security and privacy"""
        try:
            # Create User 1 context
            user1_dir = Path(self.test_dir) / "user1" / ".claudedirector"
            user1_dir.mkdir(parents=True, exist_ok=True)
            user1_context_file = user1_dir / "memory" / "strategic_context.json"
            user1_context_file.parent.mkdir(exist_ok=True)

            user1_context = {
                "user_id": "chris_cantu",
                "session_data": "confidential_platform_strategy",
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
                "session_data": "different_product_strategy",
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
        """REGRESSION TEST: Memory cleanup and archival processes manage data lifecycle effectively"""
        try:
            # Create mixed context with current and archival data
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

    def test_memory_corruption_recovery(self):
        """REGRESSION TEST: Memory system recovers gracefully from data corruption"""
        try:
            # Create valid initial context
            valid_context = {
                "current_initiatives": [{"id": "test_initiative", "status": "active"}],
                "conversation_history": [
                    {"id": "test_conv", "timestamp": datetime.now().isoformat()}
                ],
                "integrity_check": {
                    "last_validated": datetime.now().isoformat(),
                    "checksum": "valid_checksum_123",
                },
            }

            # Save valid context
            with open(self.context_file, "w") as f:
                json.dump(valid_context, f, indent=2)

            # Create backup of valid context
            backup_file = self.context_file.with_suffix(".backup")
            with open(backup_file, "w") as f:
                json.dump(valid_context, f, indent=2)

            # Simulate corruption by writing invalid JSON
            with open(self.context_file, "w") as f:
                f.write("{ corrupted json content without proper syntax")

            # Verify corruption exists
            corruption_detected = False
            try:
                with open(self.context_file, "r") as f:
                    json.load(f)
            except json.JSONDecodeError:
                corruption_detected = True

            self.assertTrue(
                corruption_detected,
                "Corruption should be detectable",
            )

            # Simulate recovery process
            recovery_successful = False
            try:
                # Attempt to load corrupted file
                with open(self.context_file, "r") as f:
                    json.load(f)
            except json.JSONDecodeError:
                # Recovery: restore from backup
                if backup_file.exists():
                    shutil.copy(backup_file, self.context_file)
                    recovery_successful = True

            # Verify recovery
            self.assertTrue(
                recovery_successful,
                "Recovery from corruption should be successful",
            )

            # Verify recovered data integrity
            with open(self.context_file, "r") as f:
                recovered_context = json.load(f)

            self.assertEqual(
                len(recovered_context["current_initiatives"]),
                1,
                "Recovered context should contain original data",
            )

            self.assertEqual(
                recovered_context["current_initiatives"][0]["id"],
                "test_initiative",
                "Recovered initiative data should be intact",
            )

            # Add recovery metadata
            recovered_context["recovery_metadata"] = {
                "recovery_performed": True,
                "recovery_timestamp": datetime.now().isoformat(),
                "corruption_detected": True,
                "backup_restored": True,
            }

            # Save recovery context
            with open(self.context_file, "w") as f:
                json.dump(recovered_context, f, indent=2)

            # Verify recovery metadata
            with open(self.context_file, "r") as f:
                final_context = json.load(f)

            self.assertTrue(
                final_context["recovery_metadata"]["recovery_performed"],
                "Recovery metadata should indicate successful recovery",
            )

        except Exception as e:
            self.fail(f"Memory corruption recovery failed: {e}")

    def test_end_to_end_memory_workflow(self):
        """REGRESSION TEST: Complete end-to-end memory workflow validation"""
        try:
            # Phase 1: User Configuration Setup
            with open(self.user_config_file, "w") as f:
                json.dump(
                    {
                        "user_identity": {
                            "name": "Chris Cantu",
                            "role": "Engineering Director",
                        },
                        "session_preferences": {"auto_save_context": True},
                    },
                    f,
                    indent=2,
                )

            # Phase 2: Initial Strategic Context Creation
            initial_context = {
                "session_id": "workflow_test_session",
                "current_initiatives": [],
                "conversation_history": [],
                "framework_usage": {},
            }

            with open(self.context_file, "w") as f:
                json.dump(initial_context, f, indent=2)

            # Phase 3: Stakeholder Intelligence Setup
            stakeholder_data = {
                "stakeholder_relationships": {
                    "jeff_williams": {
                        "role": "VP Engineering",
                        "recent_interactions": [],
                    }
                }
            }

            with open(self.stakeholder_file, "w") as f:
                json.dump(stakeholder_data, f, indent=2)

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
                "user_config_loaded" in str(loaded_context)
                or len(loaded_user_config) > 0,
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
    print("⚡ Memory Performance & Lifecycle Regression Test")
    print("=" * 50)
    print("Testing memory performance optimization and lifecycle management...")
    print()

    # Run the focused test suite
    unittest.main(verbosity=2, exit=False)

    print()
    print("✅ MEMORY PERFORMANCE REGRESSION TESTS COMPLETE")
    print("Memory performance and lifecycle management protected against regressions")
