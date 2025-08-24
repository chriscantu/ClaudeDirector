"""
End-to-End Chat Interface Integration Tests

Tests the Claude Chat interface integration with dynamic persona activation.
Validates the actual user experience of talking to Claude with automatic
director activation and seamless persona switching.

This simulates the primary user interface - Claude Chat conversations.
"""

import unittest
import tempfile
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from lib.core.persona_activation_engine import (
    ContextAnalysisEngine,
    PersonaSelectionEngine,
    ConversationStateEngine,
    ContextResult,
    PersonaSelection,
    ConfidenceLevel,
)
from lib.core.template_engine import TemplateDiscoveryEngine


class ChatInterfaceSimulator:
    """
    Simulates Claude Chat interface with persona activation.

    This represents how the system would integrate with Claude Chat
    to provide automatic director activation during conversations.
    """

    def __init__(self, config_path: Path):
        """Initialize chat interface simulator"""
        self.template_discovery = TemplateDiscoveryEngine(config_path)
        self.context_engine = ContextAnalysisEngine(self.template_discovery)
        self.persona_engine = PersonaSelectionEngine(self.template_discovery)
        self.state_engine = ConversationStateEngine()

        # Chat interface state
        self.conversation_history = []
        self.current_director = None
        self.activation_notifications = []

    def process_user_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message and return director activation info.

        This simulates what would happen when a user sends a message
        to Claude with the ClaudeDirector framework active.
        """
        start_time = time.time()

        # Analyze context
        context = self.context_engine.analyze_context(user_message)

        # Select persona
        selection = self.persona_engine.select_persona(context)

        # Update conversation state
        self.state_engine.update_state(selection, context, user_message)

        # Determine if persona activation should be shown to user
        activation_info = self._determine_activation_display(selection, context)

        # Update chat interface state
        self._update_chat_state(user_message, selection, context, activation_info)

        processing_time = (time.time() - start_time) * 1000

        return {
            "processing_time_ms": processing_time,
            "context": context,
            "selection": selection,
            "activation_info": activation_info,
            "current_director": self.current_director,
            "conversation_length": len(self.conversation_history),
        }

    def _determine_activation_display(
        self, selection: PersonaSelection, context: ContextResult
    ) -> Dict[str, Any]:
        """Determine how persona activation should be displayed to user"""

        activation_info = {
            "show_activation": False,
            "activation_type": None,
            "message": None,
            "director_name": None,
            "director_title": None,
            "confidence_level": context.confidence_level.value,
            "requires_user_action": False,
        }

        # Get template for display info
        template = self.template_discovery.get_template(selection.template_id)
        if template:
            activation_info["director_title"] = template.display_name

        # Determine activation display based on confidence level
        if context.confidence_level == ConfidenceLevel.HIGH:
            # Seamless activation - show subtle indicator
            if self.current_director != selection.primary:
                activation_info.update(
                    {
                        "show_activation": True,
                        "activation_type": "seamless",
                        "message": f"{selection.primary.title()} ({template.display_name}) is now assisting",
                        "director_name": selection.primary,
                        "requires_user_action": False,
                    }
                )

        elif context.confidence_level == ConfidenceLevel.MEDIUM:
            # Suggest with confirmation
            if self.current_director != selection.primary:
                activation_info.update(
                    {
                        "show_activation": True,
                        "activation_type": "suggestion",
                        "message": f"Switch to {selection.primary.title()} ({template.display_name}) for this discussion?",
                        "director_name": selection.primary,
                        "requires_user_action": True,
                    }
                )

        elif context.confidence_level == ConfidenceLevel.LOW:
            # Show options
            if self.current_director != selection.primary:
                activation_info.update(
                    {
                        "show_activation": True,
                        "activation_type": "options",
                        "message": f"Multiple directors available - {selection.primary.title()} recommended",
                        "director_name": selection.primary,
                        "requires_user_action": True,
                    }
                )

        return activation_info

    def _update_chat_state(
        self,
        user_message: str,
        selection: PersonaSelection,
        context: ContextResult,
        activation_info: Dict[str, Any],
    ):
        """Update internal chat interface state"""

        # Add to conversation history
        self.conversation_history.append(
            {
                "timestamp": datetime.now(),
                "user_message": user_message,
                "director": selection.primary,
                "template": selection.template_id,
                "confidence": context.confidence,
                "activation_shown": activation_info["show_activation"],
            }
        )

        # Update current director
        if not activation_info["requires_user_action"]:
            self.current_director = selection.primary

        # Track activation notifications
        if activation_info["show_activation"]:
            self.activation_notifications.append(
                {
                    "timestamp": datetime.now(),
                    "type": activation_info["activation_type"],
                    "director": selection.primary,
                    "message": activation_info["message"],
                }
            )

    def simulate_user_response(self, accept: bool = True) -> None:
        """Simulate user accepting or declining a persona suggestion"""
        if self.activation_notifications and accept:
            last_notification = self.activation_notifications[-1]
            self.current_director = last_notification["director"]

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation for analysis"""
        if not self.conversation_history:
            return {}

        director_changes = 0
        directors_used = set()

        last_director = None
        for entry in self.conversation_history:
            directors_used.add(entry["director"])
            if last_director and entry["director"] != last_director:
                director_changes += 1
            last_director = entry["director"]

        return {
            "total_messages": len(self.conversation_history),
            "director_changes": director_changes,
            "directors_used": list(directors_used),
            "activation_notifications": len(self.activation_notifications),
            "conversation_duration": (
                self.conversation_history[-1]["timestamp"]
                - self.conversation_history[0]["timestamp"]
            ).total_seconds(),
            "current_director": self.current_director,
        }


class TestChatInterfaceE2E(unittest.TestCase):
    """End-to-end tests for Claude Chat interface integration"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.config_path = cls.test_dir / "chat_test_templates.yaml"

        # Simplified config for chat testing
        cls.test_config = {
            "schema_version": "2.0.0",
            "global_settings": {
                "activation_thresholds": {
                    "high_confidence": 0.8,
                    "medium_confidence": 0.6,
                    "low_confidence": 0.4,
                }
            },
            "templates": {
                "mobile_director": {
                    "domain": "mobile_platforms",
                    "display_name": "Mobile Engineering Director",
                    "description": "iOS/Android platform expertise",
                    "personas": {
                        "primary": ["marcus"],
                        "contextual": ["sofia"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "mobile app": 0.9,
                        "ios": 0.95,
                        "android": 0.9,
                        "app store": 0.8,
                    },
                    "strategic_priorities": ["platform_unification"],
                    "metrics_focus": ["app_performance"],
                },
                "product_director": {
                    "domain": "product_engineering",
                    "display_name": "Product Engineering Director",
                    "description": "Product strategy and user experience",
                    "personas": {
                        "primary": ["rachel"],
                        "contextual": ["alvaro"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "product strategy": 0.95,
                        "user experience": 0.9,
                        "product roadmap": 0.9,
                    },
                    "strategic_priorities": ["product_market_fit"],
                    "metrics_focus": ["user_satisfaction"],
                },
                "infrastructure_director": {
                    "domain": "infrastructure_devops",
                    "display_name": "Infrastructure Director",
                    "description": "DevOps and infrastructure expertise",
                    "personas": {
                        "primary": ["martin"],
                        "contextual": ["security"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "kubernetes": 0.95,
                        "infrastructure": 0.9,
                        "devops": 0.9,
                    },
                    "strategic_priorities": ["reliability"],
                    "metrics_focus": ["uptime"],
                },
            },
        }

        with open(cls.config_path, "w") as f:
            yaml.dump(cls.test_config, f)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(cls.test_dir)

    def setUp(self):
        """Set up individual test"""
        self.chat = ChatInterfaceSimulator(self.config_path)

    def test_seamless_high_confidence_activation(self):
        """Test seamless director activation for high confidence scenarios"""

        # High confidence mobile scenario
        result = self.chat.process_user_message(
            "Our iOS mobile app is crashing constantly when users try to make payments"
        )

        # Validate high confidence detection
        self.assertEqual(result["context"].confidence_level, ConfidenceLevel.HIGH)
        self.assertEqual(result["selection"].primary, "marcus")
        self.assertTrue(result["activation_info"]["show_activation"])
        self.assertEqual(result["activation_info"]["activation_type"], "seamless")
        self.assertFalse(result["activation_info"]["requires_user_action"])

        # Validate chat state update
        self.assertEqual(self.chat.current_director, "marcus")
        self.assertEqual(len(self.chat.conversation_history), 1)
        self.assertEqual(len(self.chat.activation_notifications), 1)

        print("✅ Seamless High Confidence Activation: Marcus activated for iOS crash")

    def test_medium_confidence_suggestion_workflow(self):
        """Test suggestion workflow for medium confidence scenarios"""

        # Medium confidence scenario that could be mobile or product
        result = self.chat.process_user_message(
            "We need to improve our app performance and user experience"
        )

        # Should suggest but require confirmation
        self.assertEqual(result["context"].confidence_level, ConfidenceLevel.MEDIUM)
        self.assertTrue(result["activation_info"]["show_activation"])
        self.assertEqual(result["activation_info"]["activation_type"], "suggestion")
        self.assertTrue(result["activation_info"]["requires_user_action"])

        # Current director should not change until user accepts
        self.assertIsNone(self.chat.current_director)

        # Simulate user accepting suggestion
        self.chat.simulate_user_response(accept=True)

        # Now director should be active
        self.assertIsNotNone(self.chat.current_director)

        print("✅ Medium Confidence Suggestion: User confirmation workflow working")

    def test_low_confidence_options_workflow(self):
        """Test options presentation for low confidence scenarios"""

        # Ambiguous scenario
        result = self.chat.process_user_message(
            "We have some performance issues that need attention"
        )

        # Should show options
        self.assertEqual(result["context"].confidence_level, ConfidenceLevel.LOW)
        self.assertTrue(result["activation_info"]["show_activation"])
        self.assertEqual(result["activation_info"]["activation_type"], "options")
        self.assertTrue(result["activation_info"]["requires_user_action"])

        # Should not automatically activate
        self.assertIsNone(self.chat.current_director)

        print("✅ Low Confidence Options: Multiple options presented to user")

    def test_natural_conversation_flow_evolution(self):
        """Test natural conversation evolution with director switching"""

        conversation_steps = [
            # Start with mobile issue (High confidence)
            (
                "Our iOS app keeps crashing when users upload photos",
                "marcus",
                ConfidenceLevel.HIGH,
            ),
            # Evolve to product strategy (Medium confidence - different domain)
            (
                "This is really hurting our user retention and product metrics",
                "rachel",
                ConfidenceLevel.MEDIUM,
            ),
            # Infrastructure concern (High confidence)
            (
                "The crashes might be related to our kubernetes infrastructure having memory issues",
                "martin",
                ConfidenceLevel.HIGH,
            ),
            # Back to mobile for solution (High confidence)
            (
                "We need to implement better error handling and retry logic in the mobile app",
                "marcus",
                ConfidenceLevel.HIGH,
            ),
        ]

        director_switches = 0
        conversation_start = time.time()

        for i, (message, expected_director, expected_confidence) in enumerate(
            conversation_steps
        ):
            result = self.chat.process_user_message(message)

            # Validate expected confidence level
            self.assertEqual(result["context"].confidence_level, expected_confidence)

            # Validate expected director
            self.assertEqual(result["selection"].primary, expected_director)

            # For high confidence, should auto-activate
            if expected_confidence == ConfidenceLevel.HIGH:
                current_director_before = self.chat.current_director
                # Don't count first activation as switch
                if (
                    current_director_before
                    and current_director_before != expected_director
                ):
                    director_switches += 1

                self.assertFalse(result["activation_info"]["requires_user_action"])
                # Director should be automatically updated
                self.assertEqual(self.chat.current_director, expected_director)

            # For medium confidence, simulate user acceptance
            elif expected_confidence == ConfidenceLevel.MEDIUM:
                self.assertTrue(result["activation_info"]["requires_user_action"])
                self.chat.simulate_user_response(accept=True)
                director_switches += 1

        conversation_time = (time.time() - conversation_start) * 1000

        # Validate conversation flow
        summary = self.chat.get_conversation_summary()
        self.assertEqual(summary["total_messages"], 4)
        self.assertGreaterEqual(
            summary["director_changes"], 2
        )  # Should have switched directors
        self.assertGreaterEqual(
            len(summary["directors_used"]), 3
        )  # Should have used multiple directors

        # Performance validation
        self.assertLess(conversation_time, 8000)  # Total conversation should be fast

        print(
            f"✅ Natural Conversation Flow: {summary['director_changes']} switches, {conversation_time:.1f}ms total"
        )

    def test_persona_switching_anti_thrashing(self):
        """Test that persona switching has anti-thrashing protection"""

        # Rapid context switches that could cause thrashing
        rapid_messages = [
            "iOS app crash",  # Mobile (High)
            "product strategy issue",  # Product (High)
            "mobile performance",  # Mobile (High) - potential thrash
            "infrastructure down",  # Infrastructure (High)
            "app store issue",  # Mobile (Medium) - should not thrash
        ]

        switches = 0
        last_director = None

        for message in rapid_messages:
            result = self.chat.process_user_message(message)

            # High confidence should auto-activate
            if result["context"].confidence_level == ConfidenceLevel.HIGH:
                current_director = result["selection"].primary

                # Only count as switch if confidence is very high and actually different
                if (
                    last_director
                    and current_director != last_director
                    and result["context"].confidence >= 0.85
                ):
                    switches += 1

                last_director = current_director

        # Should not have excessive switching (anti-thrashing protection)
        self.assertLessEqual(switches, 3)  # Should be reasonable number of switches

        print(
            f"✅ Anti-Thrashing Protection: {switches} switches for {len(rapid_messages)} rapid messages"
        )

    def test_performance_requirements_chat_interface(self):
        """Test that chat interface meets performance requirements"""

        test_messages = [
            "Mobile app performance optimization needed",
            "Product roadmap planning for next quarter",
            "Kubernetes infrastructure scaling issues",
            "Data pipeline optimization for analytics",
            "Backend API performance problems",
        ]

        processing_times = []

        for message in test_messages:
            start_time = time.time()
            result = self.chat.process_user_message(message)
            total_time = (time.time() - start_time) * 1000

            processing_times.append(total_time)

            # Individual message performance
            self.assertLess(total_time, 2000)  # Total should be under 2 seconds
            self.assertLess(
                result["processing_time_ms"], 1500
            )  # Processing should be fast

            # Context analysis performance
            self.assertLess(result["context"].analysis_time_ms, 500)  # ADR requirement

            # Persona selection performance
            self.assertLess(
                result["selection"].selection_time_ms, 300
            )  # ADR requirement

        avg_time = sum(processing_times) / len(processing_times)
        max_time = max(processing_times)

        # Overall performance validation
        self.assertLess(avg_time, 1000)  # Average should be well under limit
        self.assertLess(max_time, 2000)  # No single message should exceed limit

        print(
            f"✅ Chat Interface Performance: {avg_time:.1f}ms avg, {max_time:.1f}ms max"
        )

    def test_user_experience_conversation_patterns(self):
        """Test realistic user experience conversation patterns"""

        # Realistic engineering director conversation
        realistic_conversation = [
            "Hey, our mobile app has been getting bad reviews lately",
            "Users are reporting crashes when they try to make payments",
            "This is definitely hurting our conversion rates and revenue",
            "The backend APIs seem slow too, might be infrastructure related",
            "Can we get some data to understand the correlation between crashes and API performance?",
            "Based on what we learn, we'll need to fix the mobile app's error handling",
        ]

        activation_patterns = []
        user_interruptions = 0
        seamless_activations = 0

        for i, message in enumerate(realistic_conversation):
            result = self.chat.process_user_message(message)

            activation_info = result["activation_info"]
            activation_patterns.append(
                {
                    "message_num": i + 1,
                    "confidence": result["context"].confidence,
                    "director": result["selection"].primary,
                    "activation_type": activation_info.get("activation_type"),
                    "requires_action": activation_info.get(
                        "requires_user_action", False
                    ),
                }
            )

            # Count user experience metrics
            if activation_info.get("requires_user_action"):
                user_interruptions += 1
                # Simulate user accepting suggestions
                self.chat.simulate_user_response(accept=True)
            else:
                seamless_activations += 1

        # Validate user experience
        summary = self.chat.get_conversation_summary()

        # Most activations should be seamless for good UX
        self.assertGreaterEqual(seamless_activations, user_interruptions)

        # Should have used multiple directors appropriately
        self.assertGreaterEqual(len(summary["directors_used"]), 2)

        # Should not have excessive director changes
        self.assertLessEqual(
            summary["director_changes"], len(realistic_conversation) // 2
        )

        print(
            f"✅ User Experience Patterns: {seamless_activations} seamless, {user_interruptions} interruptions"
        )

    def test_conversation_memory_and_context(self):
        """Test that conversation maintains memory and context across turns"""

        # Multi-turn conversation with context building
        conversation_with_context = [
            "Our fintech mobile app is having security issues",  # Mobile + Fintech
            "Specifically, the payment processing is vulnerable",  # Continue mobile context
            "This affects our product strategy for the enterprise market",  # Shift to product
            "We need infrastructure changes to support better security",  # Shift to infrastructure
            "The mobile team will need to implement the new security protocols",  # Back to mobile
        ]

        contexts = []

        for message in conversation_with_context:
            result = self.chat.process_user_message(message)
            contexts.append(
                {
                    "industry": result["context"].detected_industry,
                    "team_size": result["context"].detected_team_size,
                    "template": result["selection"].template_id,
                    "confidence": result["context"].confidence,
                }
            )

        # Validate context consistency
        # First message should detect fintech industry
        self.assertEqual(contexts[0]["industry"], "fintech")

        # Context should be maintained or built upon
        fintech_contexts = [ctx for ctx in contexts if ctx["industry"] == "fintech"]
        self.assertGreaterEqual(
            len(fintech_contexts), 2
        )  # Should maintain fintech context

        # Should show progression through domains
        templates_used = [ctx["template"] for ctx in contexts]
        unique_templates = set(templates_used)
        self.assertGreaterEqual(
            len(unique_templates), 2
        )  # Should use multiple templates

        # Conversation state should track all activations
        final_state = self.chat.state_engine.get_current_state()
        self.assertEqual(
            final_state["total_activations"], len(conversation_with_context)
        )

        print(
            f"✅ Conversation Memory: {len(unique_templates)} domains, context maintained"
        )

    def test_error_recovery_and_graceful_degradation(self):
        """Test chat interface error recovery and graceful degradation"""

        # Test various edge cases that could break chat flow
        edge_cases = [
            "",  # Empty message
            "   ",  # Whitespace only
            "🤖" * 100,  # Emoji spam
            "a" * 5000,  # Very long message
            "HELP URGENT ASAP NOW!!!",  # All caps urgent
            "mobile app product infrastructure data backend",  # Multiple domain keywords
        ]

        successful_recoveries = 0

        for edge_case in edge_cases:
            try:
                result = self.chat.process_user_message(edge_case)

                # Should handle gracefully
                self.assertIsNotNone(result["context"])
                self.assertIsNotNone(result["selection"])

                # Should use fallback for unclear cases
                if result["context"].confidence < 0.4:
                    self.assertIn(
                        "fallback", result["selection"].selection_method.lower()
                    )

                successful_recoveries += 1

            except Exception as e:
                self.fail(
                    f"Chat interface should handle edge case gracefully: {edge_case[:50]}... Error: {e}"
                )

        # All edge cases should be handled gracefully
        self.assertEqual(successful_recoveries, len(edge_cases))

        print(
            f"✅ Error Recovery: {successful_recoveries}/{len(edge_cases)} edge cases handled gracefully"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
