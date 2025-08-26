"""
Context Engineering Phase 1 Integration Tests

Comprehensive integration testing for the 5-layer strategic memory system.
Validates end-to-end functionality and performance targets.
"""

import unittest
import time
import json
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

from context_engineering import (
    AdvancedContextEngine,
    ConversationLayerMemory,
    StrategicLayerMemory,
    StakeholderLayerMemory,
    LearningLayerMemory,
    OrganizationalLayerMemory,
    ContextOrchestrator,
    InitiativeStatus,
    StakeholderRole,
    CommunicationStyle,
)


class TestContextEngineeringPhase1(unittest.TestCase):
    """Integration tests for Context Engineering Phase 1"""

    def setUp(self):
        """Set up test environment"""
        self.config = {
            "conversation": {"retention_days": 90, "max_conversations": 100},
            "strategic": {"max_initiatives": 50, "health_threshold": 0.7},
            "stakeholder": {"max_stakeholders": 100, "interaction_retention": 365},
            "learning": {"min_usage_for_pattern": 2, "effectiveness_threshold": 0.6},
            "organizational": {"max_team_history": 25, "change_retention": 365},
            "orchestrator": {
                "max_context_size": 512 * 1024,
                "performance_target_ms": 200,
            },
        }

        self.context_engine = AdvancedContextEngine(self.config)

        # Test data
        self.test_session_id = "test_session_001"
        self.test_query = (
            "How should I restructure the platform team for better collaboration?"
        )

    def test_context_engine_initialization(self):
        """Test Context Engine initializes all layers correctly"""
        self.assertIsInstance(
            self.context_engine.conversation_layer, ConversationLayerMemory
        )
        self.assertIsInstance(self.context_engine.strategic_layer, StrategicLayerMemory)
        self.assertIsInstance(
            self.context_engine.stakeholder_layer, StakeholderLayerMemory
        )
        self.assertIsInstance(self.context_engine.learning_layer, LearningLayerMemory)
        self.assertIsInstance(
            self.context_engine.organizational_layer, OrganizationalLayerMemory
        )
        self.assertIsInstance(
            self.context_engine.context_orchestrator, ContextOrchestrator
        )

    def test_conversation_layer_functionality(self):
        """Test conversation layer storage and retrieval"""
        # Store conversation
        success = self.context_engine.conversation_layer.store_conversation_context(
            {
                "session_id": self.test_session_id,
                "query": self.test_query,
                "response": "Consider Team Topologies framework for optimal team structure",
                "timestamp": time.time(),
            }
        )
        self.assertTrue(success)

        # Retrieve context
        context = self.context_engine.conversation_layer.retrieve_relevant_context(
            "team restructuring", self.test_session_id
        )
        self.assertIn("conversations", context)
        self.assertGreater(len(context["conversations"]), 0)
        self.assertGreater(context["overall_relevance"], 0.0)

    def test_strategic_layer_functionality(self):
        """Test strategic layer initiative tracking"""
        # Track initiative
        initiative_data = {
            "initiative_id": "platform_restructure_001",
            "name": "Platform Team Restructuring",
            "description": "Reorganize platform team for better collaboration",
            "status": InitiativeStatus.ACTIVE.value,
            "priority": "high",
            "stakeholders": ["engineering_team", "product_team"],
            "frameworks_applied": ["Team Topologies", "Organizational Design"],
            "progress_percentage": 25.0,
            "health_score": 0.8,
        }

        success = self.context_engine.strategic_layer.track_initiative(initiative_data)
        self.assertTrue(success)

        # Get initiative context
        context = self.context_engine.strategic_layer.get_initiative_context(
            self.test_session_id
        )
        self.assertIn("active_initiatives", context)
        self.assertIn("health_metrics", context)
        self.assertEqual(context["health_metrics"]["total_initiatives"], 1)

    def test_stakeholder_layer_functionality(self):
        """Test stakeholder layer relationship tracking"""
        # Update stakeholder profile
        stakeholder_data = {
            "stakeholder_id": "john_doe_engineering",
            "name": "John Doe",
            "role": StakeholderRole.ENGINEERING_MANAGER.value,
            "organization": "Engineering Team",
            "communication_style": CommunicationStyle.COLLABORATIVE.value,
            "influence_level": "high",
            "preferred_frameworks": ["Team Topologies", "Accelerate"],
            "relationship_quality": 0.8,
            "trust_level": 0.9,
        }

        success = self.context_engine.stakeholder_layer.update_stakeholder_profile(
            stakeholder_data
        )
        self.assertTrue(success)

        # Record interaction
        interaction_data = {
            "stakeholder_id": "john_doe_engineering",
            "context": "Discussion about team restructuring",
            "topics": ["team structure", "collaboration"],
            "frameworks": ["Team Topologies"],
            "satisfaction": 0.9,
            "session_id": self.test_session_id,
        }

        success = self.context_engine.stakeholder_layer.record_interaction(
            interaction_data
        )
        self.assertTrue(success)

        # Get relationship context
        context = self.context_engine.stakeholder_layer.get_relationship_context(
            "team collaboration"
        )
        self.assertIn("relevant_stakeholders", context)
        self.assertIn("relationship_insights", context)

    def test_learning_layer_functionality(self):
        """Test learning layer framework tracking and pattern recognition"""
        # Update framework usage
        success = self.context_engine.learning_layer.update_framework_usage(
            "Team Topologies", self.test_session_id, 0.9, "team restructuring"
        )
        self.assertTrue(success)

        # Record decision outcome
        decision_data = {
            "type": "organizational",
            "context_keywords": ["team", "restructuring", "collaboration"],
            "frameworks": ["Team Topologies"],
            "stakeholders": ["john_doe_engineering"],
            "outcome_score": 0.85,
            "session_id": self.test_session_id,
        }

        success = self.context_engine.learning_layer.record_decision_outcome(
            decision_data
        )
        self.assertTrue(success)

        # Get skill context
        context = self.context_engine.learning_layer.get_skill_context(
            self.test_session_id
        )
        self.assertIn("top_performing_frameworks", context)
        self.assertIn("learning_metrics", context)

    def test_organizational_layer_functionality(self):
        """Test organizational layer cultural and team tracking"""
        # Update organizational profile
        profile_data = {
            "organization_name": "TechCorp Engineering",
            "cultural_dimensions": ["collaborative", "innovative"],
            "communication_style": "balanced",
            "change_tolerance": "medium",
        }

        success = (
            self.context_engine.organizational_layer.update_organizational_profile(
                profile_data
            )
        )
        self.assertTrue(success)

        # Track team structure
        team_data = {
            "team_id": "platform_team",
            "team_name": "Platform Engineering Team",
            "team_type": "engineering",
            "size": 8,
            "collaboration_patterns": ["cross-functional", "agile"],
            "decision_making_style": "consensus",
            "performance_metrics": {"velocity": 0.8, "quality": 0.9},
        }

        success = self.context_engine.organizational_layer.track_team_structure(
            team_data
        )
        self.assertTrue(success)

        # Get structure context
        context = self.context_engine.organizational_layer.get_structure_context()
        self.assertIn("organizational_profile", context)
        self.assertIn("team_dynamics", context)
        self.assertIn("organizational_health", context)

    def test_end_to_end_context_retrieval(self):
        """Test end-to-end context retrieval with all layers"""
        # Set up test data in all layers
        self._setup_comprehensive_test_data()

        # Test contextual intelligence retrieval
        start_time = time.time()
        result = self.context_engine.get_contextual_intelligence(
            self.test_query, self.test_session_id, max_context_size=256 * 1024
        )
        retrieval_time = (time.time() - start_time) * 1000  # Convert to ms

        # Validate result structure
        self.assertIn("context", result)
        self.assertIn("metrics", result)
        self.assertIn("session_id", result)
        self.assertIn("timestamp", result)

        # Validate performance targets
        self.assertLess(retrieval_time, 3000, "Context retrieval exceeded 3s target")
        self.assertLess(
            result["metrics"]["context_size_bytes"],
            256 * 1024,
            "Context size exceeded limit",
        )
        self.assertGreater(
            result["metrics"]["relevance_score"], 0.5, "Context relevance too low"
        )

        # Validate context quality
        context = result["context"]
        self.assertIn("strategic_context", context)
        self.assertIn("assembly_metrics", context)
        self.assertIn("context_quality", context)

        quality = context["context_quality"]
        self.assertGreater(quality["coherence_score"], 0.5, "Context coherence too low")
        self.assertGreater(
            quality["layer_coverage"], 0.2, "Insufficient layer coverage"
        )

    def test_conversation_outcome_storage(self):
        """Test storing conversation outcomes across layers"""
        # Set up initial data
        self._setup_comprehensive_test_data()

        # Store conversation outcome
        success = self.context_engine.store_conversation_outcome(
            session_id=self.test_session_id,
            query=self.test_query,
            response="Recommended Team Topologies approach with gradual transition",
            frameworks_used=["Team Topologies", "Change Management"],
            strategic_decisions=[
                {
                    "initiative_id": "platform_restructure_002",
                    "name": "Team Restructuring Phase 2",
                    "status": InitiativeStatus.PLANNED.value,
                    "frameworks_applied": ["Team Topologies"],
                }
            ],
        )

        self.assertTrue(success, "Failed to store conversation outcome")

        # Verify data was stored across layers
        # Check conversation layer
        conv_context = self.context_engine.conversation_layer.retrieve_relevant_context(
            "team restructuring", self.test_session_id
        )
        self.assertGreater(len(conv_context["conversations"]), 0)

        # Check strategic layer
        strategic_context = self.context_engine.strategic_layer.get_initiative_context(
            self.test_session_id
        )
        self.assertGreater(strategic_context["health_metrics"]["total_initiatives"], 1)

        # Check learning layer
        learning_context = self.context_engine.learning_layer.get_skill_context(
            self.test_session_id
        )
        self.assertGreater(len(learning_context["top_performing_frameworks"]), 0)

    def test_performance_monitoring(self):
        """Test performance monitoring and metrics collection"""
        # Perform multiple context retrievals
        for i in range(5):
            self.context_engine.get_contextual_intelligence(
                f"Test query {i} about platform strategy", f"session_{i}"
            )

        # Get performance summary
        summary = self.context_engine.get_performance_summary()

        self.assertIn("performance_summary", summary)
        self.assertIn("targets", summary)
        self.assertIn("compliance", summary)

        perf = summary["performance_summary"]
        self.assertGreater(perf["total_retrievals"], 0)
        self.assertGreater(perf["average_relevance_score"], 0.0)

        # Get orchestrator metrics
        orch_metrics = (
            self.context_engine.context_orchestrator.get_orchestration_metrics()
        )
        self.assertIn("performance_summary", orch_metrics)
        self.assertIn("layer_usage_frequency", orch_metrics)

    def test_memory_usage_tracking(self):
        """Test memory usage tracking across all layers"""
        # Set up test data
        self._setup_comprehensive_test_data()

        # Get memory usage from each layer
        conv_memory = self.context_engine.conversation_layer.get_memory_usage()
        strategic_memory = self.context_engine.strategic_layer.get_memory_usage()
        stakeholder_memory = self.context_engine.stakeholder_layer.get_memory_usage()
        learning_memory = self.context_engine.learning_layer.get_memory_usage()
        org_memory = self.context_engine.organizational_layer.get_memory_usage()
        orch_memory = self.context_engine.context_orchestrator.get_memory_usage()

        # Validate memory tracking
        for memory_stats in [
            conv_memory,
            strategic_memory,
            stakeholder_memory,
            learning_memory,
            org_memory,
            orch_memory,
        ]:
            self.assertIn("total_memory_bytes", memory_stats)
            self.assertIn("total_memory_mb", memory_stats)
            self.assertGreater(memory_stats["total_memory_bytes"], 0)

        # Validate memory efficiency (target: <100MB total per user)
        total_memory_mb = sum(
            [
                conv_memory["total_memory_mb"],
                strategic_memory["total_memory_mb"],
                stakeholder_memory["total_memory_mb"],
                learning_memory["total_memory_mb"],
                org_memory["total_memory_mb"],
                orch_memory["total_memory_mb"],
            ]
        )

        self.assertLess(
            total_memory_mb,
            100,
            f"Total memory usage ({total_memory_mb:.2f}MB) exceeds 100MB target",
        )

    def test_error_handling_and_fallback(self):
        """Test error handling and graceful fallback"""
        # Test with invalid session data
        result = self.context_engine.get_contextual_intelligence(
            "", "invalid_session", max_context_size=100
        )

        # Should get fallback context
        self.assertIn("context", result)
        # Check if we got any valid result structure
        self.assertTrue(
            "strategic_context" in result["context"]
            or "assembly_metrics" in result["context"]
            or len(result["context"]) > 0,
            "Should get some form of context result",
        )

        # Test with extremely small context size
        result = self.context_engine.get_contextual_intelligence(
            self.test_query, self.test_session_id, max_context_size=50
        )

        # Should still return valid result
        self.assertIn("context", result)
        self.assertIn("metrics", result)

    def _setup_comprehensive_test_data(self):
        """Set up comprehensive test data across all layers"""
        # Conversation data
        self.context_engine.conversation_layer.store_conversation_context(
            {
                "session_id": self.test_session_id,
                "query": "How should we improve team collaboration?",
                "response": "Consider implementing Team Topologies patterns",
                "timestamp": time.time() - 86400,  # 1 day ago
            }
        )

        # Strategic data
        self.context_engine.strategic_layer.track_initiative(
            {
                "initiative_id": "collaboration_improvement",
                "name": "Team Collaboration Enhancement",
                "status": InitiativeStatus.ACTIVE.value,
                "priority": "high",
                "progress_percentage": 60.0,
                "health_score": 0.8,
                "frameworks_applied": ["Team Topologies", "Agile"],
            }
        )

        # Stakeholder data
        self.context_engine.stakeholder_layer.update_stakeholder_profile(
            {
                "stakeholder_id": "alice_tech_lead",
                "name": "Alice Johnson",
                "role": StakeholderRole.ENGINEER.value,
                "communication_style": CommunicationStyle.ANALYTICAL.value,
                "influence_level": "high",
                "relationship_quality": 0.9,
            }
        )

        # Learning data
        self.context_engine.learning_layer.update_framework_usage(
            "Team Topologies", self.test_session_id, 0.85, "team collaboration"
        )

        # Organizational data
        self.context_engine.organizational_layer.track_team_structure(
            {
                "team_id": "engineering_team",
                "team_name": "Engineering Team",
                "team_type": "engineering",
                "size": 12,
                "collaboration_patterns": ["agile", "cross-functional"],
                "performance_metrics": {"velocity": 0.75, "satisfaction": 0.8},
            }
        )


if __name__ == "__main__":
    # Run the integration tests
    unittest.main(verbosity=2)
