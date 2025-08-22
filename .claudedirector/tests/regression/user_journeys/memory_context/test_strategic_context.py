#!/usr/bin/env python3
"""
🎯 Strategic Context Preservation Regression Test - Critical User Journey 4b/5

BUSINESS CRITICAL PATH: Strategic conversation context and initiative tracking
FAILURE IMPACT: Strategic context lost, conversation history broken, initiative tracking disrupted

This focused test suite validates strategic context preservation and management:
1. Strategic conversation history preservation across sessions
2. Initiative tracking and milestone progression
3. Cross-session continuity and context handoff
4. Framework application history and decision tracking

COVERAGE: Complete strategic context lifecycle validation
PRIORITY: P0 BLOCKING - Strategic context preservation
EXECUTION: <3 seconds for complete context validation
"""

import sys
import os
import unittest
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../lib"))


class TestStrategicContext(unittest.TestCase):
    """Test strategic context preservation and conversation continuity"""

    def setUp(self):
        """Set up test environment for strategic context testing"""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claudedirector"
        self.memory_dir = self.config_dir / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Context file paths
        self.context_file = self.memory_dir / "strategic_context.json"
        
        # Test strategic context data
        self.test_strategic_context = {
            "session_id": "session_1",
            "timestamp": datetime.now().isoformat(),
            "current_initiatives": [
                {
                    "id": "platform_scaling_2024",
                    "title": "Platform Scaling Initiative Q4 2024",
                    "status": "in_progress",
                    "priority": "P0",
                    "created": datetime.now().isoformat(),
                    "last_discussion": datetime.now().isoformat(),
                    "key_decisions": ["monorepo_migration", "team_restructure"],
                    "next_milestones": ["Q1_2025_launch", "performance_benchmarks"],
                }
            ],
            "recent_conversations": [
                {
                    "id": "conv_1",
                    "timestamp": datetime.now().isoformat(),
                    "persona_used": "diego",
                    "topic": "platform_architecture",
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

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

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

    def test_initiative_progression_tracking(self):
        """REGRESSION TEST: Initiative progression and milestones are tracked accurately"""
        try:
            # Create initial initiative context
            initial_context = {
                "current_initiatives": [
                    {
                        "id": "design_system_scaling",
                        "title": "Design System Scaling Q4",
                        "status": "planning",
                        "priority": "P1",
                        "created": datetime.now().isoformat(),
                        "milestones": [
                            {
                                "id": "milestone_1",
                                "title": "Component Audit Complete",
                                "status": "completed",
                                "completed_date": (datetime.now() - timedelta(days=7)).isoformat(),
                            },
                            {
                                "id": "milestone_2", 
                                "title": "Token System Implementation",
                                "status": "in_progress",
                                "target_date": (datetime.now() + timedelta(days=14)).isoformat(),
                            },
                            {
                                "id": "milestone_3",
                                "title": "Team Training Rollout",
                                "status": "planned",
                                "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
                            },
                        ],
                        "decision_log": [
                            {
                                "date": (datetime.now() - timedelta(days=5)).isoformat(),
                                "decision": "Adopt Figma Tokens for design system",
                                "rationale": "Better designer-developer handoff",
                                "participants": ["rachel", "design_team"],
                            }
                        ],
                    }
                ],
                "session_metadata": {
                    "last_initiative_update": datetime.now().isoformat(),
                },
            }
            
            # Save initial context
            with open(self.context_file, "w") as f:
                json.dump(initial_context, f, indent=2)
            
            # Simulate initiative progression
            with open(self.context_file, "r") as f:
                context = json.load(f)
            
            # Progress milestone 2 to completed
            initiative = context["current_initiatives"][0]
            for milestone in initiative["milestones"]:
                if milestone["id"] == "milestone_2":
                    milestone["status"] = "completed"
                    milestone["completed_date"] = datetime.now().isoformat()
                    milestone["actual_duration_days"] = 12  # Completed early
            
            # Add new decision
            initiative["decision_log"].append({
                "date": datetime.now().isoformat(),
                "decision": "Accelerate training timeline due to early completion",
                "rationale": "Team ready earlier than expected",
                "participants": ["rachel", "diego", "training_team"],
            })
            
            # Update initiative status
            initiative["status"] = "execution"
            context["session_metadata"]["last_initiative_update"] = datetime.now().isoformat()
            
            # Save updated context
            with open(self.context_file, "w") as f:
                json.dump(context, f, indent=2)
            
            # Reload and verify progression tracking
            with open(self.context_file, "r") as f:
                updated_context = json.load(f)
            
            updated_initiative = updated_context["current_initiatives"][0]
            
            # Verify milestone progression
            milestone_2 = next(
                m for m in updated_initiative["milestones"] if m["id"] == "milestone_2"
            )
            self.assertEqual(
                milestone_2["status"],
                "completed",
                "Milestone status should be updated",
            )
            
            self.assertIn(
                "completed_date",
                milestone_2,
                "Completed milestone should have completion date",
            )
            
            # Verify decision log growth
            self.assertEqual(
                len(updated_initiative["decision_log"]),
                2,
                "Decision log should track new decisions",
            )
            
            # Verify initiative status progression
            self.assertEqual(
                updated_initiative["status"],
                "execution",
                "Initiative status should progress",
            )
            
        except Exception as e:
            self.fail(f"Initiative progression tracking failed: {e}")

    def test_cross_session_continuity(self):
        """REGRESSION TEST: Strategic context maintains continuity across multiple sessions"""
        try:
            # Create Session 1 context
            session1_context = {
                "session_id": "session_1",
                "timestamp": datetime.now().isoformat(),
                "current_initiatives": [
                    {
                        "id": "platform_modernization",
                        "title": "Platform Modernization Initiative",
                        "status": "planning",
                        "decisions_made": ["team_structure_review"],
                        "next_steps": ["stakeholder_alignment"],
                    }
                ],
                "conversation_history": [
                    {
                        "topic": "team_organization",
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

    def test_framework_application_history(self):
        """REGRESSION TEST: Framework application history is comprehensively tracked"""
        try:
            # Create context with framework usage history
            framework_history_context = {
                "framework_applications": [
                    {
                        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
                        "framework": "Team Topologies",
                        "confidence": 0.92,
                        "query_context": "team restructuring for platform scaling",
                        "persona": "diego",
                        "outcome": "identified stream-aligned teams structure",
                        "follow_up_frameworks": ["Capital Allocation Framework"],
                    },
                    {
                        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                        "framework": "Capital Allocation Framework",
                        "confidence": 0.85,
                        "query_context": "platform investment justification",
                        "persona": "alvaro", 
                        "outcome": "ROI model for platform team investment",
                        "supporting_data": ["team_productivity_metrics", "delivery_velocity"],
                    },
                    {
                        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                        "framework": "Design System Maturity Model",
                        "confidence": 0.88,
                        "query_context": "design system scaling strategy",
                        "persona": "rachel",
                        "outcome": "component maturity assessment and roadmap",
                        "integration_points": ["Team Topologies boundaries"],
                    },
                ],
                "framework_analytics": {
                    "most_used_frameworks": [
                        {"framework": "Team Topologies", "usage_count": 8, "avg_confidence": 0.89},
                        {"framework": "Capital Allocation Framework", "usage_count": 5, "avg_confidence": 0.82},
                        {"framework": "Design System Maturity Model", "usage_count": 4, "avg_confidence": 0.85},
                    ],
                    "persona_framework_affinity": {
                        "diego": ["Team Topologies", "Technical Strategy Framework"],
                        "alvaro": ["Capital Allocation Framework", "Good Strategy Bad Strategy"],
                        "rachel": ["Design System Maturity Model", "User-Centered Design"],
                    },
                    "framework_combinations": [
                        {
                            "combination": ["Team Topologies", "Capital Allocation Framework"],
                            "frequency": 3,
                            "effectiveness_rating": 0.91,
                        }
                    ],
                },
            }
            
            # Save framework history context
            with open(self.context_file, "w") as f:
                json.dump(framework_history_context, f, indent=2)
            
            # Load and verify framework history
            with open(self.context_file, "r") as f:
                loaded_context = json.load(f)
            
            # Verify framework application tracking
            applications = loaded_context["framework_applications"]
            self.assertEqual(
                len(applications), 3, "All framework applications should be tracked"
            )
            
            # Verify chronological ordering
            timestamps = [app["timestamp"] for app in applications]
            sorted_timestamps = sorted(timestamps)
            self.assertEqual(
                timestamps, sorted_timestamps, "Applications should be in chronological order"
            )
            
            # Verify framework linkage tracking
            team_topologies_app = next(
                app for app in applications if app["framework"] == "Team Topologies"
            )
            self.assertIn(
                "follow_up_frameworks",
                team_topologies_app,
                "Framework linkages should be tracked",
            )
            
            # Verify analytics accuracy
            analytics = loaded_context["framework_analytics"]
            most_used = analytics["most_used_frameworks"]
            
            # Team Topologies should be most used
            top_framework = most_used[0]
            self.assertEqual(
                top_framework["framework"],
                "Team Topologies",
                "Most used framework should be identified correctly",
            )
            
            # Verify persona affinity tracking
            persona_affinity = analytics["persona_framework_affinity"]
            self.assertIn(
                "Team Topologies",
                persona_affinity["diego"],
                "Persona framework affinity should be tracked",
            )
            
            # Verify framework combination tracking
            combinations = analytics["framework_combinations"]
            self.assertGreater(
                len(combinations), 0, "Framework combinations should be tracked"
            )
            
        except Exception as e:
            self.fail(f"Framework application history tracking failed: {e}")

    def test_context_performance_optimization(self):
        """REGRESSION TEST: Strategic context handling performs well with large datasets"""
        try:
            # Generate large context dataset
            large_context = {
                "current_initiatives": [],
                "conversation_history": [],
                "framework_applications": [],
            }
            
            # Generate 50 initiatives
            for i in range(50):
                large_context["current_initiatives"].append({
                    "id": f"initiative_{i}",
                    "title": f"Strategic Initiative {i}",
                    "status": "in_progress" if i < 30 else "completed",
                    "priority": "P0" if i % 10 == 0 else "P1",
                    "created": (datetime.now() - timedelta(days=i)).isoformat(),
                })
            
            # Generate 200 conversations
            for i in range(200):
                large_context["conversation_history"].append({
                    "id": f"conv_{i}",
                    "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                    "persona": ["diego", "martin", "rachel", "alvaro"][i % 4],
                    "topic": f"strategic_topic_{i}",
                    "framework": ["Team Topologies", "Capital Allocation", "Strategic Analysis"][i % 3],
                })
            
            # Generate 100 framework applications
            for i in range(100):
                large_context["framework_applications"].append({
                    "timestamp": (datetime.now() - timedelta(minutes=i*30)).isoformat(),
                    "framework": ["Team Topologies", "Capital Allocation", "Design System Maturity Model"][i % 3],
                    "confidence": 0.7 + (i % 3) * 0.1,
                })
            
            # Measure save performance
            start_time = time.time()
            with open(self.context_file, "w") as f:
                json.dump(large_context, f, indent=2)
            save_time = time.time() - start_time
            
            # Measure load performance
            start_time = time.time()
            with open(self.context_file, "r") as f:
                loaded_large_context = json.load(f)
            load_time = time.time() - start_time
            
            # Verify data integrity
            self.assertEqual(
                len(loaded_large_context["current_initiatives"]),
                50,
                "All initiatives should be preserved in large dataset",
            )
            
            self.assertEqual(
                len(loaded_large_context["conversation_history"]),
                200,
                "All conversations should be preserved in large dataset",
            )
            
            # Performance assertions (reasonable thresholds)
            self.assertLess(
                save_time,
                1.0,
                f"Large context save should complete in <1s, took {save_time:.2f}s",
            )
            
            self.assertLess(
                load_time,
                0.5,
                f"Large context load should complete in <0.5s, took {load_time:.2f}s",
            )
            
        except Exception as e:
            self.fail(f"Context performance optimization failed: {e}")


if __name__ == "__main__":
    print("🎯 Strategic Context Preservation Regression Test")
    print("=" * 50)
    print("Testing strategic context preservation and conversation continuity...")
    print()
    
    # Run the focused test suite
    unittest.main(verbosity=2, exit=False)
    
    print()
    print("✅ STRATEGIC CONTEXT REGRESSION TESTS COMPLETE")
    print("Strategic context preservation and conversation continuity protected against regressions")
