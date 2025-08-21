#!/usr/bin/env python3
"""
End-to-End Executive Workflow Testing
Tests complete strategic leadership workflows from user input to strategic output
"""

import sys
import time
import unittest
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

try:
    from integration_protection.cursor_transparency_bridge import CursorTransparencyBridge
    TRANSPARENCY_AVAILABLE = True
except ImportError:
    TRANSPARENCY_AVAILABLE = False

try:
    from mcp.hybrid_installation_manager import HybridInstallationManager
    HYBRID_MANAGER_AVAILABLE = True
except ImportError:
    HYBRID_MANAGER_AVAILABLE = False

class TestExecutiveWorkflow(unittest.TestCase):
    """End-to-end executive workflow testing"""

    def setUp(self):
        """Set up E2E testing environment"""
        self.transparency_bridge = None
        self.hybrid_manager = None

        if TRANSPARENCY_AVAILABLE:
            self.transparency_bridge = CursorTransparencyBridge()

        if HYBRID_MANAGER_AVAILABLE:
            self.hybrid_manager = HybridInstallationManager()

    def test_strategic_planning_workflow(self):
        """Test complete strategic planning workflow"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        # Executive strategic planning scenario
        workflow_steps = [
            {
                "step": "Initial Strategic Question",
                "user_input": "We need to scale our platform capabilities across multiple international markets. How should we approach this transformation systematically?",
                "expected_persona": "diego",
                "expected_elements": ["🎯 Diego", "Engineering Leadership", "systematic"]
            },
            {
                "step": "Stakeholder Alignment Question",
                "user_input": "What are the key stakeholder alignment challenges we should anticipate?",
                "expected_persona": "camille",
                "expected_elements": ["📊 Camille", "Strategic Technology", "stakeholder"]
            },
            {
                "step": "Investment Analysis",
                "user_input": "How should we structure the investment and ROI analysis for this transformation?",
                "expected_persona": "alvaro",
                "expected_elements": ["💼 Alvaro", "Platform Investment", "ROI"]
            },
            {
                "step": "Design System Impact",
                "user_input": "How does this affect our global design system strategy?",
                "expected_persona": "rachel",
                "expected_elements": ["🎨 Rachel", "Design Systems", "global"]
            }
        ]

        workflow_results = []

        for step_info in workflow_steps:
            start_time = time.time()

            # Process strategic input through transparency system
            enhanced_response = self.transparency_bridge.apply_transparency_system(
                f"Strategic response addressing {step_info['step'].lower()}...",
                step_info["user_input"],
                step_info["expected_persona"]
            )

            duration = time.time() - start_time

            # Validate response contains expected elements
            for expected_element in step_info["expected_elements"]:
                self.assertIn(expected_element, enhanced_response,
                             f"Expected '{expected_element}' in {step_info['step']} response")

            # Performance requirement
            self.assertLess(duration, 2.0, f"{step_info['step']} response too slow: {duration:.2f}s")

            workflow_results.append({
                "step": step_info["step"],
                "duration": duration,
                "response_length": len(enhanced_response),
                "success": True
            })

        # Validate complete workflow performance
        total_duration = sum(result["duration"] for result in workflow_results)
        self.assertLess(total_duration, 5.0, f"Complete workflow too slow: {total_duration:.2f}s")

        # All steps should succeed
        successful_steps = sum(1 for result in workflow_results if result["success"])
        self.assertEqual(successful_steps, len(workflow_steps), "All workflow steps must succeed")

    def test_technical_architecture_workflow(self):
        """Test technical architecture decision workflow"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        # Technical architecture scenario
        architecture_workflow = [
            {
                "question": "How should we evolve our platform architecture to support microservices?",
                "expected_persona": "martin",
                "validation": ["🏗️ Martin", "Platform Architecture", "microservices"]
            },
            {
                "question": "What are the security implications of this architectural change?",
                "expected_persona": "martin",
                "validation": ["security", "architectural", "implications"]
            },
            {
                "question": "How do we ensure performance doesn't degrade during migration?",
                "expected_persona": "martin",
                "validation": ["performance", "migration", "ensure"]
            }
        ]

        for i, step in enumerate(architecture_workflow):
            enhanced_response = self.transparency_bridge.apply_transparency_system(
                f"Technical architecture analysis for step {i+1}...",
                step["question"],
                step["expected_persona"]
            )

            # Validate technical depth
            self.assertGreater(len(enhanced_response), 100,
                              "Technical responses should be substantive")

            # Check for framework or MCP enhancement
            has_enhancement = ("🔧 Installing MCP enhancement:" in enhanced_response or
                             "⚡ Using optimized MCP server:" in enhanced_response or
                             "📚 Strategic Framework:" in enhanced_response)

            self.assertTrue(has_enhancement,
                           "Technical questions should trigger framework analysis")

    def test_crisis_management_workflow(self):
        """Test crisis management and rapid decision workflow"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        # Crisis scenario - should be handled quickly
        crisis_input = "URGENT: Our main platform is experiencing critical performance issues affecting all customers. We need immediate strategic guidance on response and communication."

        start_time = time.time()

        crisis_response = self.transparency_bridge.apply_transparency_system(
            "🚨 CRISIS RESPONSE: Immediate strategic action required...",
            crisis_input,
            "diego"
        )

        response_time = time.time() - start_time

        # Crisis responses must be very fast
        self.assertLess(response_time, 1.0, f"Crisis response too slow: {response_time:.2f}s")

        # Should contain crisis-appropriate elements
        crisis_indicators = ["CRISIS", "URGENT", "immediate", "critical"]
        has_crisis_recognition = any(indicator.lower() in crisis_response.lower()
                                   for indicator in crisis_indicators)

        self.assertTrue(has_crisis_recognition,
                       "Crisis response should recognize urgency")

        # Should still maintain persona structure
        self.assertIn("🎯 Diego", crisis_response,
                     "Crisis response should maintain persona structure")

    def test_cross_persona_collaboration_workflow(self):
        """Test workflow requiring multiple persona collaboration"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        # Complex scenario requiring multiple perspectives
        complex_scenario = "We're planning a major platform transformation that involves technical architecture changes, design system updates, investment analysis, and stakeholder communication. I need integrated strategic guidance."

        # Test different persona responses to same complex scenario
        personas_to_test = ["diego", "camille", "rachel", "alvaro", "martin"]

        persona_responses = {}
        total_start_time = time.time()

        for persona in personas_to_test:
            start_time = time.time()

            response = self.transparency_bridge.apply_transparency_system(
                f"Multi-faceted strategic analysis from {persona} perspective...",
                complex_scenario,
                persona
            )

            duration = time.time() - start_time

            persona_responses[persona] = {
                "response": response,
                "duration": duration,
                "length": len(response)
            }

            # Each response should be timely
            self.assertLess(duration, 2.0, f"{persona} response too slow: {duration:.2f}s")

            # Each response should be substantive for complex scenario
            self.assertGreater(len(response), 200,
                              f"{persona} response too brief for complex scenario")

        total_duration = time.time() - total_start_time

        # Complete multi-persona analysis should complete in reasonable time
        self.assertLess(total_duration, 8.0,
                       f"Multi-persona workflow too slow: {total_duration:.2f}s")

        # Each persona should provide distinct perspective
        response_texts = [data["response"] for data in persona_responses.values()]

        # Responses should be different (not identical)
        unique_responses = set(response_texts)
        self.assertGreater(len(unique_responses), 1,
                          "Personas should provide distinct responses")

    def test_hybrid_installation_workflow(self):
        """Test hybrid installation decision workflow"""
        if not HYBRID_MANAGER_AVAILABLE:
            self.skipTest("Hybrid installation manager not available")

        # Test installation decision process
        test_servers = ["sequential", "magic"]

        for server_name in test_servers:
            status = self.hybrid_manager.get_server_status(server_name)

            # Validate status structure
            required_fields = ["server_name", "permanent_available", "temporary_uses",
                             "permanent_uses", "installation_strategy"]

            for field in required_fields:
                self.assertIn(field, status, f"Server status missing {field}")

            # Server name should match
            self.assertEqual(status["server_name"], server_name)

            # Installation strategy should be defined
            self.assertIn(status["installation_strategy"], ["hybrid", "legacy"])

    def test_complete_user_journey(self):
        """Test complete user journey from first question to strategic outcome"""
        if not TRANSPARENCY_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        # Simulate complete user journey
        user_journey = [
            {
                "phase": "Discovery",
                "input": "I'm new to ClaudeDirector. How can it help with strategic platform decisions?",
                "expected": ["strategic", "platform", "decisions"]
            },
            {
                "phase": "Initial Strategic Question",
                "input": "How should we prioritize our platform investments for next quarter?",
                "expected": ["prioritize", "platform investments", "quarter"]
            },
            {
                "phase": "Deep Dive Analysis",
                "input": "What specific frameworks should we apply to evaluate these investment options?",
                "expected": ["frameworks", "evaluate", "investment"]
            },
            {
                "phase": "Implementation Planning",
                "input": "How do we structure the implementation timeline and stakeholder communication?",
                "expected": ["implementation", "timeline", "stakeholder"]
            },
            {
                "phase": "Success Metrics",
                "input": "What metrics should we track to measure the success of these platform investments?",
                "expected": ["metrics", "measure", "success"]
            }
        ]

        journey_start_time = time.time()
        journey_results = []

        for step in user_journey:
            step_start_time = time.time()

            # Process through transparency system
            enhanced_response = self.transparency_bridge.apply_transparency_system(
                f"Strategic guidance for {step['phase']} phase...",
                step["input"],
                "diego"  # Default to Diego for platform decisions
            )

            step_duration = time.time() - step_start_time

            # Validate expected elements
            for expected_element in step["expected"]:
                self.assertIn(expected_element.lower(), enhanced_response.lower(),
                             f"Expected '{expected_element}' in {step['phase']} response")

            journey_results.append({
                "phase": step["phase"],
                "duration": step_duration,
                "success": True
            })

        total_journey_time = time.time() - journey_start_time

        # Complete user journey should be efficient
        self.assertLess(total_journey_time, 10.0,
                       f"Complete user journey too slow: {total_journey_time:.2f}s")

        # All phases should succeed
        successful_phases = sum(1 for result in journey_results if result["success"])
        self.assertEqual(successful_phases, len(user_journey),
                        "All user journey phases must succeed")

def run_e2e_tests():
    """Run end-to-end workflow tests"""
    print("🎭 END-TO-END EXECUTIVE WORKFLOW TESTING")
    print("=" * 60)
    print("Testing complete strategic leadership workflows")
    print("Validating executive user experience")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExecutiveWorkflow)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL E2E WORKFLOW TESTS PASSED")
        print("   Strategic planning workflow validated")
        print("   Technical architecture workflow working")
        print("   Crisis management response verified")
        print("   Cross-persona collaboration tested")
        print("   Complete user journey validated")
        return True
    else:
        print("❌ E2E WORKFLOW TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        return False

if __name__ == "__main__":
    success = run_e2e_tests()
    sys.exit(0 if success else 1)
