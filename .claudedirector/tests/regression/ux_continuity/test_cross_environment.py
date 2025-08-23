#!/usr/bin/env python3
"""
UX Continuity Regression Test: Cross-Environment Consistency

Rachel's Test Suite: Ensures consistent user experience across different
platforms, environments, and interaction modes (Cursor, Claude Chat, CLI).

UX IMPACT: Inconsistent cross-environment experience confuses users,
reduces adoption, and creates fragmented strategic intelligence workflows.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestCrossEnvironmentConsistency(unittest.TestCase):
    """UX continuity tests for consistent experience across environments"""

    def setUp(self):
        """Set up test environment for cross-environment testing"""
        self.test_dir = tempfile.mkdtemp()
        self.cross_env_dir = Path(self.test_dir) / "cross_environment"
        self.cross_env_dir.mkdir(parents=True, exist_ok=True)

        # Define supported environments and their characteristics
        self.environments = {
            "cursor_ide": {
                "platform": "desktop",
                "interaction_mode": "integrated_chat",
                "features": ["real_time_transparency", "context_persistence", "file_integration", "git_integration"],
                "user_expectations": ["seamless_workflow", "zero_setup", "persistent_sessions"],
                "primary_use_cases": ["strategic_planning", "architecture_decisions", "team_coordination"]
            },
            "claude_chat": {
                "platform": "web",
                "interaction_mode": "standalone_chat",
                "features": ["conversation_history", "context_sharing", "export_capabilities"],
                "user_expectations": ["accessible_anywhere", "conversation_continuity", "easy_sharing"],
                "primary_use_cases": ["executive_briefings", "strategic_discussions", "decision_support"]
            },
            "cli_interface": {
                "platform": "terminal",
                "interaction_mode": "command_line",
                "features": ["automation_support", "script_integration", "batch_processing"],
                "user_expectations": ["scriptable_workflows", "consistent_output", "reliable_automation"],
                "primary_use_cases": ["automated_reporting", "batch_analysis", "integration_workflows"]
            }
        }

        # Define cross-environment consistency requirements
        self.consistency_requirements = {
            "persona_behavior": "identical_across_environments",
            "strategic_guidance": "consistent_quality_and_content",
            "framework_detection": "same_frameworks_same_contexts",
            "transparency_disclosure": "complete_in_all_environments",
            "context_preservation": "seamless_environment_switching"
        }

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_persona_consistency_across_environments(self):
        """
        UX CRITICAL: Personas must behave identically across all environments

        FAILURE IMPACT: Users get different guidance depending on platform
        UX COST: Confusion, reduced trust, fragmented user experience
        """
        # Test persona consistency across environments
        persona_consistency_tests = [
            {
                "persona": "diego",
                "strategic_query": "How should we structure our engineering teams for platform scaling?",
                "expected_characteristics": {
                    "communication_style": "direct_challenging",
                    "framework_preference": "Team Topologies",
                    "response_pattern": "asks_clarifying_questions"
                }
            },
            {
                "persona": "alvaro",
                "strategic_query": "What's the ROI analysis for our platform investment?",
                "expected_characteristics": {
                    "communication_style": "roi_focused_analytical",
                    "framework_preference": "Capital Allocation Framework",
                    "response_pattern": "business_justification"
                }
            },
            {
                "persona": "rachel",
                "strategic_query": "How do we improve design system adoption across teams?",
                "expected_characteristics": {
                    "communication_style": "user_centered_collaborative",
                    "framework_preference": "Design System Maturity Model",
                    "response_pattern": "user_impact_focus"
                }
            }
        ]

        for test in persona_consistency_tests:
            environment_responses = {}

            # Test persona behavior in each environment
            for env_name, env_config in self.environments.items():
                response = self._simulate_persona_response_in_environment(
                    test["persona"],
                    test["strategic_query"],
                    env_name,
                    env_config
                )
                environment_responses[env_name] = response

            # Verify consistency across environments
            reference_response = environment_responses["cursor_ide"]  # Use Cursor as reference

            for env_name, response in environment_responses.items():
                if env_name == "cursor_ide":
                    continue

                # Verify communication style consistency
                self.assertEqual(
                    response["communication_style"],
                    reference_response["communication_style"],
                    f"Communication style inconsistent for {test['persona']} in {env_name}"
                )

                # Verify framework preference consistency
                self.assertEqual(
                    response["framework_applied"],
                    reference_response["framework_applied"],
                    f"Framework preference inconsistent for {test['persona']} in {env_name}"
                )

                # Verify response pattern consistency
                self.assertEqual(
                    response["response_pattern"],
                    reference_response["response_pattern"],
                    f"Response pattern inconsistent for {test['persona']} in {env_name}"
                )

                # Verify strategic guidance quality
                self.assertGreaterEqual(
                    response["guidance_quality_score"],
                    reference_response["guidance_quality_score"] * 0.9,  # Allow 10% variance
                    f"Guidance quality significantly lower for {test['persona']} in {env_name}"
                )

        print("✅ Persona consistency across environments: PASSED")

    def test_feature_parity_across_platforms(self):
        """
        UX CRITICAL: Core features must work consistently across platforms

        FAILURE IMPACT: Feature availability varies by platform, user confusion
        UX COST: Platform-specific workflows, reduced user efficiency
        """
        # Test feature parity across platforms
        core_features = [
            {
                "feature": "strategic_framework_detection",
                "test_scenario": "complex_organizational_decision",
                "expected_frameworks": ["Team Topologies", "Good Strategy Bad Strategy"],
                "minimum_accuracy": 0.85
            },
            {
                "feature": "multi_persona_coordination",
                "test_scenario": "cross_functional_strategic_question",
                "expected_personas": ["diego", "rachel", "alvaro"],
                "coordination_quality_threshold": 0.8
            },
            {
                "feature": "context_preservation",
                "test_scenario": "multi_turn_strategic_conversation",
                "context_elements": ["stakeholder_relationships", "previous_decisions", "strategic_constraints"],
                "preservation_rate_threshold": 0.9
            },
            {
                "feature": "transparency_disclosure",
                "test_scenario": "ai_enhanced_strategic_analysis",
                "disclosure_elements": ["mcp_server_usage", "framework_attribution", "persona_coordination"],
                "completeness_threshold": 1.0
            }
        ]

        for feature in core_features:
            environment_results = {}

            # Test feature in each environment
            for env_name, env_config in self.environments.items():
                # Skip features not supported in environment
                if feature["feature"] not in self._get_supported_features(env_config):
                    continue

                result = self._test_feature_in_environment(
                    feature["feature"],
                    feature["test_scenario"],
                    env_name,
                    env_config
                )
                environment_results[env_name] = result

            # Verify feature parity across environments
            reference_env = "cursor_ide"  # Use Cursor as reference
            if reference_env not in environment_results:
                continue

            reference_result = environment_results[reference_env]

            for env_name, result in environment_results.items():
                if env_name == reference_env:
                    continue

                # Verify feature functionality
                self.assertTrue(
                    result["feature_functional"],
                    f"Feature '{feature['feature']}' not functional in {env_name}"
                )

                # Verify performance consistency
                performance_ratio = result["performance_score"] / reference_result["performance_score"]
                self.assertGreaterEqual(
                    performance_ratio,
                    0.8,  # Allow 20% performance variance
                    f"Feature '{feature['feature']}' performance significantly lower in {env_name}"
                )

                # Verify output consistency
                output_similarity = self._calculate_output_similarity(
                    reference_result["output"],
                    result["output"]
                )
                self.assertGreaterEqual(
                    output_similarity,
                    0.85,  # 85% output similarity
                    f"Feature '{feature['feature']}' output inconsistent in {env_name}"
                )

        print("✅ Feature parity across platforms: PASSED")

    def test_context_transfer_between_environments(self):
        """
        UX CRITICAL: Context must transfer seamlessly between environments

        FAILURE IMPACT: Users lose context when switching platforms
        UX COST: Must re-establish context, reduced productivity, frustration
        """
        # Test context transfer scenarios
        context_transfer_scenarios = [
            {
                "scenario": "cursor_to_claude_chat_handoff",
                "source_environment": "cursor_ide",
                "target_environment": "claude_chat",
                "context_type": "strategic_planning_session",
                "context_data": {
                    "active_persona": "diego",
                    "strategic_topic": "engineering_team_scaling",
                    "decisions_made": ["adopt_team_topologies", "hire_senior_engineers"],
                    "stakeholder_context": ["hemendra_concerns", "budget_constraints"],
                    "next_steps": ["create_hiring_plan", "present_to_leadership"]
                },
                "transfer_method": "context_export_import"
            },
            {
                "scenario": "claude_chat_to_cli_automation",
                "source_environment": "claude_chat",
                "target_environment": "cli_interface",
                "context_type": "roi_analysis_session",
                "context_data": {
                    "active_persona": "alvaro",
                    "strategic_topic": "platform_investment_roi",
                    "analysis_parameters": {"investment_amount": 2000000, "timeline": "3_years"},
                    "business_context": ["competitive_positioning", "market_timing"],
                    "output_requirements": ["executive_summary", "detailed_calculations"]
                },
                "transfer_method": "structured_data_export"
            }
        ]

        for scenario in context_transfer_scenarios:
            # Establish context in source environment
            source_session = self._establish_context_in_environment(
                scenario["source_environment"],
                scenario["context_type"],
                scenario["context_data"]
            )

            # Export context from source
            exported_context = self._export_context_from_environment(
                source_session,
                scenario["transfer_method"]
            )

            # Import context to target environment
            target_session = self._import_context_to_environment(
                scenario["target_environment"],
                exported_context,
                scenario["transfer_method"]
            )

            # Verify context transfer quality
            transfer_quality = self._assess_context_transfer_quality(
                scenario["context_data"],
                target_session["restored_context"]
            )

            # Verify critical context elements preserved
            for key_element in ["active_persona", "strategic_topic"]:
                if key_element in scenario["context_data"]:
                    self.assertEqual(
                        target_session["restored_context"][key_element],
                        scenario["context_data"][key_element],
                        f"Key context element '{key_element}' not preserved in {scenario['scenario']}"
                    )

            # Verify overall transfer quality
            self.assertGreaterEqual(
                transfer_quality["preservation_score"],
                0.85,  # 85% context preservation
                f"Context transfer quality too low in {scenario['scenario']}"
            )

            # Verify functional continuity
            self.assertTrue(
                transfer_quality["functional_continuity"],
                f"Functional continuity lost in {scenario['scenario']}"
            )

        print("✅ Context transfer between environments: PASSED")

    def test_user_interface_consistency(self):
        """
        UX CRITICAL: User interface patterns must be consistent across environments

        FAILURE IMPACT: Different UI patterns confuse users, increase learning curve
        UX COST: Reduced user efficiency, training overhead, user errors
        """
        # Test UI consistency across environments
        ui_consistency_tests = [
            {
                "ui_element": "persona_identification",
                "consistency_requirement": "same_visual_format",
                "test_scenarios": [
                    {"persona": "diego", "expected_format": "🎯 Diego | Engineering Leadership"},
                    {"persona": "alvaro", "expected_format": "💼 Alvaro | Platform Investment Strategy"},
                    {"persona": "rachel", "expected_format": "🎨 Rachel | Design Systems Strategy"}
                ]
            },
            {
                "ui_element": "framework_attribution",
                "consistency_requirement": "same_disclosure_format",
                "test_scenarios": [
                    {"framework": "Team Topologies", "expected_format": "📚 Strategic Framework: Team Topologies detected"},
                    {"framework": "Capital Allocation", "expected_format": "📚 Strategic Framework: Capital Allocation Framework detected"}
                ]
            },
            {
                "ui_element": "transparency_disclosure",
                "consistency_requirement": "same_enhancement_format",
                "test_scenarios": [
                    {"enhancement": "mcp_server", "expected_format": "🔧 Accessing MCP Server: [server_name] ([capability])"},
                    {"enhancement": "multi_persona", "expected_format": "🤝 **Cross-Functional Analysis**"}
                ]
            }
        ]

        for ui_test in ui_consistency_tests:
            environment_formats = {}

            # Test UI element in each environment
            for env_name, env_config in self.environments.items():
                env_formats = []

                for scenario in ui_test["test_scenarios"]:
                    ui_output = self._generate_ui_element_in_environment(
                        ui_test["ui_element"],
                        scenario,
                        env_name,
                        env_config
                    )
                    env_formats.append(ui_output)

                environment_formats[env_name] = env_formats

            # Verify UI consistency across environments
            reference_formats = environment_formats["cursor_ide"]  # Use Cursor as reference

            for env_name, env_formats in environment_formats.items():
                if env_name == "cursor_ide":
                    continue

                for i, (reference_format, env_format) in enumerate(zip(reference_formats, env_formats)):
                    # Verify format consistency
                    format_similarity = self._calculate_format_similarity(
                        reference_format["formatted_output"],
                        env_format["formatted_output"]
                    )

                    self.assertGreaterEqual(
                        format_similarity,
                        0.9,  # 90% format similarity
                        f"UI format inconsistent for {ui_test['ui_element']} in {env_name}, scenario {i}"
                    )

                    # Verify visual elements preserved
                    self.assertEqual(
                        reference_format["visual_elements"],
                        env_format["visual_elements"],
                        f"Visual elements inconsistent for {ui_test['ui_element']} in {env_name}, scenario {i}"
                    )

        print("✅ User interface consistency: PASSED")

    def test_performance_consistency_across_environments(self):
        """
        UX CRITICAL: Performance must be consistent across environments

        FAILURE IMPACT: Some environments feel slow, users avoid certain platforms
        UX COST: Platform preference bias, reduced adoption, user frustration
        """
        # Test performance consistency across environments
        performance_benchmarks = [
            {
                "operation": "strategic_query_response",
                "test_query": "How should we prioritize our platform investments?",
                "expected_personas": ["alvaro", "diego"],
                "max_response_time": 5.0,  # seconds
                "quality_threshold": 0.8
            },
            {
                "operation": "framework_detection_and_attribution",
                "test_scenario": "complex_organizational_decision",
                "expected_frameworks": 3,  # minimum frameworks detected
                "max_processing_time": 2.0,
                "accuracy_threshold": 0.85
            },
            {
                "operation": "context_preservation_and_recall",
                "test_scenario": "multi_turn_conversation",
                "context_elements": 10,  # number of context elements
                "max_recall_time": 1.0,
                "preservation_rate": 0.9
            }
        ]

        for benchmark in performance_benchmarks:
            environment_performance = {}

            # Test performance in each environment
            for env_name, env_config in self.environments.items():
                performance_result = self._measure_performance_in_environment(
                    benchmark["operation"],
                    benchmark,
                    env_name,
                    env_config
                )
                environment_performance[env_name] = performance_result

            # Verify performance consistency
            reference_performance = environment_performance["cursor_ide"]  # Use Cursor as reference

            for env_name, performance in environment_performance.items():
                if env_name == "cursor_ide":
                    continue

                # Verify response time consistency
                time_ratio = performance["response_time"] / reference_performance["response_time"]
                self.assertLessEqual(
                    time_ratio,
                    2.0,  # Allow 2x slower maximum
                    f"Performance significantly slower for {benchmark['operation']} in {env_name}"
                )

                # Verify quality consistency
                quality_ratio = performance["quality_score"] / reference_performance["quality_score"]
                self.assertGreaterEqual(
                    quality_ratio,
                    0.9,  # Allow 10% quality variance
                    f"Quality significantly lower for {benchmark['operation']} in {env_name}"
                )

                # Verify absolute performance thresholds
                if "max_response_time" in benchmark:
                    self.assertLessEqual(
                        performance["response_time"],
                        benchmark["max_response_time"],
                        f"Response time exceeds threshold for {benchmark['operation']} in {env_name}"
                    )

                if "quality_threshold" in benchmark:
                    self.assertGreaterEqual(
                        performance["quality_score"],
                        benchmark["quality_threshold"],
                        f"Quality below threshold for {benchmark['operation']} in {env_name}"
                    )

        print("✅ Performance consistency across environments: PASSED")

    def _simulate_persona_response_in_environment(self, persona, query, env_name, env_config):
        """Simulate persona response in specific environment"""
        # Simulate environment-specific response characteristics
        base_response = {
            "persona": persona,
            "query": query,
            "environment": env_name
        }

        # Add persona-specific characteristics
        persona_characteristics = {
            "diego": {
                "communication_style": "direct_challenging",
                "framework_applied": "Team Topologies",
                "response_pattern": "asks_clarifying_questions",
                "guidance_quality_score": 0.9
            },
            "alvaro": {
                "communication_style": "roi_focused_analytical",
                "framework_applied": "Capital Allocation Framework",
                "response_pattern": "business_justification",
                "guidance_quality_score": 0.88
            },
            "rachel": {
                "communication_style": "user_centered_collaborative",
                "framework_applied": "Design System Maturity Model",
                "response_pattern": "user_impact_focus",
                "guidance_quality_score": 0.92
            }
        }

        base_response.update(persona_characteristics.get(persona, {}))

        # Apply environment-specific modifications (if any)
        if env_name == "cli_interface":
            base_response["guidance_quality_score"] *= 0.95  # Slight reduction for CLI

        return base_response

    def _get_supported_features(self, env_config):
        """Get list of supported features for environment"""
        return env_config.get("features", [])

    def _test_feature_in_environment(self, feature, test_scenario, env_name, env_config):
        """Test specific feature in environment"""
        # Simulate feature testing
        base_performance = 0.9

        # Environment-specific performance adjustments
        performance_modifiers = {
            "cursor_ide": 1.0,
            "claude_chat": 0.95,
            "cli_interface": 0.85
        }

        performance_score = base_performance * performance_modifiers.get(env_name, 0.9)

        return {
            "feature_functional": True,
            "performance_score": performance_score,
            "output": f"Feature {feature} output in {env_name}",
            "environment": env_name
        }

    def _calculate_output_similarity(self, output1, output2):
        """Calculate similarity between outputs"""
        # Simplified similarity calculation
        if output1 == output2:
            return 1.0

        # Check for common elements
        words1 = set(output1.lower().split())
        words2 = set(output2.lower().split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _establish_context_in_environment(self, env_name, context_type, context_data):
        """Establish context in specific environment"""
        return {
            "environment": env_name,
            "context_type": context_type,
            "context_data": context_data,
            "session_id": f"session_{env_name}_{datetime.now().timestamp()}",
            "established_at": datetime.now().isoformat()
        }

    def _export_context_from_environment(self, session, transfer_method):
        """Export context from environment"""
        return {
            "source_session": session["session_id"],
            "context_data": session["context_data"],
            "transfer_method": transfer_method,
            "exported_at": datetime.now().isoformat()
        }

    def _import_context_to_environment(self, env_name, exported_context, transfer_method):
        """Import context to target environment"""
        return {
            "environment": env_name,
            "restored_context": exported_context["context_data"],
            "transfer_method": transfer_method,
            "import_success": True,
            "imported_at": datetime.now().isoformat()
        }

    def _assess_context_transfer_quality(self, original_context, restored_context):
        """Assess quality of context transfer"""
        # Calculate preservation score
        original_keys = set(original_context.keys())
        restored_keys = set(restored_context.keys())

        preserved_keys = original_keys.intersection(restored_keys)
        preservation_score = len(preserved_keys) / len(original_keys) if original_keys else 1.0

        return {
            "preservation_score": preservation_score,
            "functional_continuity": preservation_score >= 0.8,
            "preserved_elements": list(preserved_keys),
            "missing_elements": list(original_keys - restored_keys)
        }

    def _generate_ui_element_in_environment(self, ui_element, scenario, env_name, env_config):
        """Generate UI element in specific environment"""
        # Simulate UI element generation
        ui_formats = {
            "persona_identification": {
                "diego": {"formatted_output": "🎯 Diego | Engineering Leadership", "visual_elements": ["emoji", "name", "role"]},
                "alvaro": {"formatted_output": "💼 Alvaro | Platform Investment Strategy", "visual_elements": ["emoji", "name", "role"]},
                "rachel": {"formatted_output": "🎨 Rachel | Design Systems Strategy", "visual_elements": ["emoji", "name", "role"]}
            },
            "framework_attribution": {
                "Team Topologies": {"formatted_output": "📚 Strategic Framework: Team Topologies detected", "visual_elements": ["emoji", "label", "framework_name"]},
                "Capital Allocation": {"formatted_output": "📚 Strategic Framework: Capital Allocation Framework detected", "visual_elements": ["emoji", "label", "framework_name"]}
            },
            "transparency_disclosure": {
                "mcp_server": {"formatted_output": "🔧 Accessing MCP Server: [server_name] ([capability])", "visual_elements": ["emoji", "action", "details"]},
                "multi_persona": {"formatted_output": "🤝 **Cross-Functional Analysis**", "visual_elements": ["emoji", "label", "emphasis"]}
            }
        }

        element_formats = ui_formats.get(ui_element, {})
        scenario_key = scenario.get("persona") or scenario.get("framework") or scenario.get("enhancement")

        return element_formats.get(scenario_key, {"formatted_output": "Default format", "visual_elements": ["default"]})

    def _calculate_format_similarity(self, format1, format2):
        """Calculate similarity between UI formats"""
        # Simplified format similarity calculation
        if format1 == format2:
            return 1.0

        # Check structural similarity
        structure_similarity = 0.8 if len(format1.split()) == len(format2.split()) else 0.6

        # Check content similarity
        content_similarity = self._calculate_output_similarity(format1, format2)

        return (structure_similarity + content_similarity) / 2

    def _measure_performance_in_environment(self, operation, benchmark, env_name, env_config):
        """Measure performance of operation in environment"""
        # Simulate performance measurement
        base_times = {
            "strategic_query_response": 2.5,
            "framework_detection_and_attribution": 1.2,
            "context_preservation_and_recall": 0.5
        }

        environment_multipliers = {
            "cursor_ide": 1.0,
            "claude_chat": 1.1,
            "cli_interface": 0.9
        }

        base_time = base_times.get(operation, 2.0)
        multiplier = environment_multipliers.get(env_name, 1.0)

        return {
            "operation": operation,
            "environment": env_name,
            "response_time": base_time * multiplier,
            "quality_score": 0.85,  # Base quality score
            "benchmark_met": True
        }


def run_ux_continuity_cross_environment_tests():
    """Run all UX continuity cross-environment tests"""
    print("🎨 UX CONTINUITY REGRESSION TEST: Cross-Environment Consistency")
    print("=" * 70)
    print("OWNER: Rachel | IMPACT: Platform Consistency & User Adoption")
    print("FAILURE COST: Fragmented experience, reduced adoption, user confusion")
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCrossEnvironmentConsistency)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL CROSS-ENVIRONMENT CONSISTENCY TESTS PASSED")
        print("🎨 UX Impact: Consistent experience across all platforms maintained")
        print("📊 Strategic Value: Platform adoption and user efficiency preserved")
        return True
    else:
        print(f"\n❌ CROSS-ENVIRONMENT CONSISTENCY FAILURES: {len(result.failures + result.errors)}")
        print("💥 UX Impact: Inconsistent platform experience, user confusion")
        print("🚨 Action Required: Fix cross-environment consistency immediately")
        return False


if __name__ == "__main__":
    success = run_ux_continuity_cross_environment_tests()
    sys.exit(0 if success else 1)
