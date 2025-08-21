"""
End-to-End Integration Tests for Dynamic Persona Activation System

Tests the complete workflow from user input through context analysis,
persona selection, state management, and CLI integration. Validates
performance requirements and real-world usage scenarios.

Test Coverage:
- Full persona activation workflow (Phase 2.1)
- Template migration integration (Phase 2.2)
- CLI command integration
- Performance requirements (ADR-004 compliance)
- Industry and team size contexts
- Error handling and graceful degradation
"""

import unittest
import tempfile
import subprocess
import time
import json
import yaml
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from claudedirector.core.persona_activation_engine import (
    ContextAnalysisEngine,
    PersonaSelectionEngine,
    ConversationStateEngine,
    ContextResult,
    PersonaSelection,
    ConfidenceLevel,
)
from claudedirector.core.template_engine import TemplateDiscoveryEngine
from claudedirector.p1_features.template_commands import TemplateCommands
from claudedirector.p1_features.template_migration import (
    TemplateMigrationEngine,
    TemplateMigrationCommands,
)


class TestDynamicPersonaActivationE2E(unittest.TestCase):
    """End-to-end tests for the complete dynamic persona activation system"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment for all tests"""
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.config_path = cls.test_dir / "test_templates.yaml"

        # Create comprehensive test configuration
        cls.test_config = {
            "schema_version": "2.0.0",
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generated_by": "E2E Test Suite",
                "total_templates": 6,
                "supported_domains": [
                    "mobile_platforms",
                    "product_engineering",
                    "platform_engineering",
                    "backend_services",
                    "infrastructure_devops",
                    "data_analytics_ml",
                ],
            },
            "global_settings": {
                "default_fallback_personas": ["camille", "diego", "alvaro"],
                "activation_thresholds": {
                    "high_confidence": 0.8,
                    "medium_confidence": 0.6,
                    "low_confidence": 0.4,
                },
                "selection_weights": {
                    "domain_match": 0.4,
                    "industry_match": 0.3,
                    "team_size_match": 0.2,
                    "keyword_confidence": 0.1,
                },
            },
            "templates": {
                "mobile_director": {
                    "domain": "mobile_platforms",
                    "display_name": "Mobile Engineering Director",
                    "description": "iOS/Android platform strategy, mobile DevOps, and app performance optimization",
                    "industry_modifiers": {
                        "fintech": {
                            "priorities": ["security_compliance", "payment_processing"],
                            "metrics": [
                                "transaction_security",
                                "compliance_audit_score",
                            ],
                        },
                        "gaming": {
                            "priorities": ["real_time_performance", "user_engagement"],
                            "metrics": ["frame_rate_consistency", "user_retention"],
                        },
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["mvp_velocity", "platform_foundation"],
                            "challenges": ["resource_constraints", "technical_debt"],
                        },
                        "enterprise": {
                            "focus": ["enterprise_governance", "app_store_compliance"],
                            "challenges": [
                                "legacy_migration",
                                "regulatory_requirements",
                            ],
                        },
                    },
                    "personas": {
                        "primary": ["marcus", "sofia"],
                        "contextual": ["diego", "security"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "mobile app": 0.9,
                        "ios development": 0.95,
                        "android platform": 0.9,
                        "react native": 0.85,
                        "flutter": 0.85,
                        "app store": 0.8,
                        "mobile performance": 0.85,
                    },
                    "strategic_priorities": [
                        "platform_unification",
                        "developer_experience",
                        "market_speed",
                        "performance_optimization",
                    ],
                    "metrics_focus": [
                        "app_performance",
                        "release_velocity",
                        "user_adoption",
                        "platform_consistency",
                    ],
                },
                "product_engineering_director": {
                    "domain": "product_engineering",
                    "display_name": "Product Engineering Director",
                    "description": "Product strategy execution, user experience optimization, and customer-driven engineering delivery",
                    "industry_modifiers": {
                        "saas": {
                            "priorities": [
                                "customer_retention_engineering",
                                "product_analytics",
                            ],
                            "metrics": [
                                "monthly_active_users",
                                "feature_adoption_rate",
                            ],
                        },
                        "ecommerce": {
                            "priorities": [
                                "conversion_optimization",
                                "personalization_systems",
                            ],
                            "metrics": ["conversion_rate", "cart_abandonment"],
                        },
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["mvp_product_fit", "user_feedback_loops"],
                            "challenges": [
                                "feature_prioritization",
                                "technical_debt_vs_features",
                            ],
                        },
                        "scale": {
                            "focus": [
                                "product_scalability",
                                "user_experience_consistency",
                            ],
                            "challenges": [
                                "feature_coordination",
                                "product_quality_vs_velocity",
                            ],
                        },
                    },
                    "personas": {
                        "primary": ["alvaro", "rachel"],
                        "contextual": ["diego", "data"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "product strategy": 0.95,
                        "user experience": 0.9,
                        "product roadmap": 0.9,
                        "customer feedback": 0.85,
                        "feature delivery": 0.85,
                        "product analytics": 0.8,
                        "user research": 0.8,
                    },
                    "strategic_priorities": [
                        "product_market_fit_engineering",
                        "user_experience_optimization",
                        "feature_delivery_velocity",
                        "data_driven_development",
                    ],
                    "metrics_focus": [
                        "feature_adoption_rate",
                        "user_satisfaction_scores",
                        "product_velocity_metrics",
                        "customer_conversion_impact",
                    ],
                },
                "platform_director": {
                    "domain": "platform_engineering",
                    "display_name": "Platform Engineering Director",
                    "description": "Developer productivity, internal tooling, and platform infrastructure",
                    "industry_modifiers": {
                        "enterprise": {
                            "priorities": [
                                "enterprise_governance",
                                "compliance_frameworks",
                            ],
                            "metrics": ["developer_productivity", "platform_adoption"],
                        }
                    },
                    "team_size_contexts": {
                        "scale": {
                            "focus": ["developer_velocity", "platform_standardization"],
                            "challenges": ["tool_proliferation", "platform_adoption"],
                        }
                    },
                    "personas": {
                        "primary": ["diego", "martin"],
                        "contextual": ["alvaro", "security"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "platform engineering": 0.95,
                        "developer tools": 0.9,
                        "ci/cd": 0.85,
                        "developer productivity": 0.9,
                        "internal tools": 0.85,
                        "platform": 0.8,
                    },
                    "strategic_priorities": [
                        "developer_productivity",
                        "platform_standardization",
                        "tool_consolidation",
                    ],
                    "metrics_focus": [
                        "developer_velocity",
                        "platform_adoption",
                        "build_success_rate",
                    ],
                },
                "backend_director": {
                    "domain": "backend_services",
                    "display_name": "Backend Services Director",
                    "description": "API strategy, microservices architecture, and backend scalability",
                    "industry_modifiers": {
                        "fintech": {
                            "priorities": [
                                "transaction_processing",
                                "data_consistency",
                            ],
                            "metrics": ["transaction_throughput", "data_integrity"],
                        }
                    },
                    "team_size_contexts": {
                        "enterprise": {
                            "focus": ["service_governance", "api_strategy"],
                            "challenges": ["legacy_integration", "service_sprawl"],
                        }
                    },
                    "personas": {
                        "primary": ["martin", "diego"],
                        "contextual": ["data", "security"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "backend": 0.9,
                        "microservices": 0.95,
                        "api": 0.85,
                        "database": 0.8,
                        "scalability": 0.85,
                        "distributed systems": 0.9,
                    },
                    "strategic_priorities": [
                        "service_architecture",
                        "api_governance",
                        "scalability_planning",
                    ],
                    "metrics_focus": [
                        "api_performance",
                        "service_reliability",
                        "database_efficiency",
                    ],
                },
                "infrastructure_director": {
                    "domain": "infrastructure_devops",
                    "display_name": "Infrastructure & DevOps Director",
                    "description": "Cloud platforms, reliability engineering, and DevOps transformation",
                    "industry_modifiers": {
                        "healthcare": {
                            "priorities": ["hipaa_compliance", "data_privacy"],
                            "metrics": ["compliance_coverage", "security_incidents"],
                        }
                    },
                    "team_size_contexts": {
                        "startup": {
                            "focus": ["cloud_adoption", "automation_basics"],
                            "challenges": ["cost_optimization", "skill_gaps"],
                        }
                    },
                    "personas": {
                        "primary": ["martin", "security"],
                        "contextual": ["diego", "david"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "infrastructure": 0.95,
                        "devops": 0.9,
                        "kubernetes": 0.9,
                        "cloud": 0.85,
                        "deployment": 0.8,
                        "monitoring": 0.8,
                        "reliability": 0.85,
                    },
                    "strategic_priorities": [
                        "platform_reliability",
                        "operational_excellence",
                        "cost_optimization",
                    ],
                    "metrics_focus": [
                        "system_reliability",
                        "deployment_velocity",
                        "cost_efficiency",
                    ],
                },
                "data_director": {
                    "domain": "data_analytics_ml",
                    "display_name": "Data Engineering Director",
                    "description": "Data pipelines, analytics platforms, and machine learning infrastructure",
                    "industry_modifiers": {
                        "ecommerce": {
                            "priorities": ["recommendation_systems", "personalization"],
                            "metrics": ["recommendation_accuracy", "conversion_lift"],
                        }
                    },
                    "team_size_contexts": {
                        "scale": {
                            "focus": ["data_governance", "ml_ops"],
                            "challenges": ["data_quality", "model_deployment"],
                        }
                    },
                    "personas": {
                        "primary": ["data", "martin"],
                        "contextual": ["alvaro", "diego"],
                        "fallback": ["camille"],
                    },
                    "activation_keywords": {
                        "data pipeline": 0.95,
                        "machine learning": 0.9,
                        "analytics": 0.85,
                        "data warehouse": 0.9,
                        "ml": 0.85,
                        "business intelligence": 0.8,
                    },
                    "strategic_priorities": [
                        "data_governance",
                        "ml_operations",
                        "analytics_enablement",
                    ],
                    "metrics_focus": [
                        "data_quality",
                        "model_performance",
                        "analytics_adoption",
                    ],
                },
            },
        }

        # Write test configuration
        with open(cls.config_path, "w") as f:
            yaml.dump(cls.test_config, f, default_flow_style=False, indent=2)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(cls.test_dir)

    def setUp(self):
        """Set up individual test"""
        # Create engines with test configuration
        self.template_discovery = TemplateDiscoveryEngine(self.config_path)
        self.context_engine = ContextAnalysisEngine(self.template_discovery)
        self.persona_engine = PersonaSelectionEngine(self.template_discovery)
        self.state_engine = ConversationStateEngine()

        # Track test performance
        self.test_start_time = time.time()

    def tearDown(self):
        """Clean up individual test"""
        test_duration = (time.time() - self.test_start_time) * 1000
        print(f"Test completed in {test_duration:.1f}ms")

    def test_e2e_mobile_development_workflow(self):
        """
        E2E Test: Mobile Development Workflow

        Tests complete workflow for mobile development context with
        industry-specific and team size considerations.
        """
        # Test Scenario: Fintech startup with mobile app performance issues
        user_input = "Our fintech mobile app for iOS is having terrible performance issues, especially during payment processing"

        start_time = time.time()

        # Step 1: Context Analysis
        context = self.context_engine.analyze_context(user_input)

        # Validate context analysis
        self.assertIsNotNone(context.domain)
        self.assertEqual(context.suggested_template, "mobile_director")
        self.assertGreater(context.confidence, 0.6)  # Should be medium-high confidence
        self.assertEqual(context.detected_industry, "fintech")
        self.assertIn("mobile app", context.keywords)
        self.assertIn("ios", [k.lower() for k in context.keywords])

        # Step 2: Persona Selection
        selection = self.persona_engine.select_persona(context)

        # Validate persona selection
        self.assertEqual(selection.template_id, "mobile_director")
        self.assertIn(
            selection.primary, ["marcus", "sofia", "diego"]
        )  # Should select appropriate persona
        self.assertEqual(selection.confidence, context.confidence)
        self.assertIn("Mobile Engineering Director", selection.rationale)

        # Step 3: State Management
        self.state_engine.update_state(selection, context, user_input)

        # Validate state update
        state = self.state_engine.get_current_state()
        self.assertEqual(state["active_persona"], selection.primary)
        self.assertEqual(state["current_template_id"], "mobile_director")
        self.assertEqual(state["total_activations"], 1)

        # Step 4: Performance Validation
        total_time = (time.time() - start_time) * 1000
        self.assertLess(total_time, 2000)  # ADR requirement: <2000ms total
        self.assertLess(
            context.analysis_time_ms, 500
        )  # ADR requirement: <500ms analysis
        self.assertLess(
            selection.selection_time_ms, 300
        )  # ADR requirement: <300ms selection

        # Step 5: Industry Context Application
        template = self.template_discovery.get_template("mobile_director")
        industry_enhancements = template.apply_industry_modifier("fintech")

        # Validate industry-specific enhancements
        self.assertIn("enhanced_priorities", industry_enhancements)
        self.assertIn(
            "security_compliance", industry_enhancements["enhanced_priorities"]
        )
        self.assertIn("enhanced_metrics", industry_enhancements)
        self.assertIn("transaction_security", industry_enhancements["enhanced_metrics"])

        print(
            f"✅ Mobile Development E2E: {total_time:.1f}ms total, {context.confidence:.2f} confidence"
        )

    def test_e2e_product_strategy_workflow(self):
        """
        E2E Test: Product Strategy Workflow

        Tests complete workflow for product strategy context with
        SaaS industry and scaling team considerations.
        """
        # Test Scenario: SaaS scale-up with product strategy challenges
        user_input = "We're a SaaS company scaling rapidly and need to improve our product strategy, user experience, and feature delivery velocity"

        start_time = time.time()

        # Step 1: Context Analysis
        context = self.context_engine.analyze_context(user_input)

        # Validate context analysis
        self.assertEqual(context.suggested_template, "product_engineering_director")
        self.assertGreater(context.confidence, 0.7)  # Should be high confidence
        self.assertEqual(context.detected_industry, "saas")
        self.assertEqual(context.detected_team_size, "scale")
        self.assertIn("product strategy", context.keywords)
        self.assertIn("user experience", context.keywords)

        # Step 2: Persona Selection
        selection = self.persona_engine.select_persona(context)

        # Validate persona selection
        self.assertEqual(selection.template_id, "product_engineering_director")
        self.assertIn(
            selection.primary, ["alvaro", "rachel"]
        )  # Should select product persona

        # Step 3: State Management with Previous Context
        # Simulate previous mobile conversation
        previous_context = ContextResult(
            domain="mobile_platforms",
            confidence=0.8,
            suggested_template="mobile_director",
        )
        previous_selection = PersonaSelection(
            primary="marcus", template_id="mobile_director", confidence=0.8
        )
        self.state_engine.update_state(
            previous_selection, previous_context, "previous mobile discussion"
        )

        # Now update with new product context
        self.state_engine.update_state(selection, context, user_input)

        # Validate state transition
        state = self.state_engine.get_current_state()
        self.assertEqual(state["active_persona"], selection.primary)
        self.assertEqual(state["current_template_id"], "product_engineering_director")
        self.assertEqual(state["total_activations"], 2)

        # Validate persona switch suggestion worked
        switch_suggestion = self.state_engine.suggest_persona_switch(context)
        self.assertIsNone(
            switch_suggestion
        )  # Should not suggest switch since we already switched

        # Step 4: Performance Validation
        total_time = (time.time() - start_time) * 1000
        self.assertLess(total_time, 2000)

        # Step 5: Team Size Context Application
        template = self.template_discovery.get_template("product_engineering_director")
        team_context = template.apply_team_size_context("scale")

        # Validate team size-specific enhancements
        self.assertIn("focus_areas", team_context)
        self.assertIn("product_scalability", team_context["focus_areas"])
        self.assertIn("key_challenges", team_context)
        self.assertIn("feature_coordination", team_context["key_challenges"])

        print(
            f"✅ Product Strategy E2E: {total_time:.1f}ms total, {context.confidence:.2f} confidence"
        )

    def test_e2e_infrastructure_emergency_workflow(self):
        """
        E2E Test: Infrastructure Emergency Workflow

        Tests rapid activation for infrastructure emergencies with
        healthcare compliance considerations.
        """
        # Test Scenario: Healthcare infrastructure emergency
        user_input = "URGENT: Our healthcare platform kubernetes deployment is failing, patient data access is down, need immediate help with HIPAA compliance"

        start_time = time.time()

        # Step 1: Context Analysis
        context = self.context_engine.analyze_context(user_input)

        # Validate emergency detection
        self.assertEqual(context.suggested_template, "infrastructure_director")
        self.assertGreater(
            context.confidence, 0.8
        )  # Should be high confidence for emergency
        self.assertEqual(context.detected_industry, "healthcare")
        self.assertIn("kubernetes", context.keywords)
        self.assertIn("infrastructure", context.keywords)

        # Step 2: Persona Selection (Emergency Priority)
        selection = self.persona_engine.select_persona(context)

        # Validate high-priority persona selection
        self.assertEqual(selection.template_id, "infrastructure_director")
        self.assertIn(
            selection.primary, ["martin", "security"]
        )  # Should select infrastructure expert
        self.assertEqual(selection.selection_method, "automatic_high_confidence")

        # Step 3: Rapid State Update
        self.state_engine.update_state(selection, context, user_input)

        # Step 4: Emergency Performance Validation (Stricter Requirements)
        total_time = (time.time() - start_time) * 1000
        self.assertLess(total_time, 1000)  # Emergency should be faster than 1 second
        self.assertLess(
            context.analysis_time_ms, 300
        )  # Faster analysis for emergencies
        self.assertLess(
            selection.selection_time_ms, 200
        )  # Faster selection for emergencies

        # Step 5: Industry Compliance Context
        template = self.template_discovery.get_template("infrastructure_director")
        industry_enhancements = template.apply_industry_modifier("healthcare")

        # Validate healthcare-specific priorities
        self.assertIn("enhanced_priorities", industry_enhancements)
        self.assertIn("hipaa_compliance", industry_enhancements["enhanced_priorities"])
        self.assertIn("data_privacy", industry_enhancements["enhanced_priorities"])

        print(
            f"✅ Infrastructure Emergency E2E: {total_time:.1f}ms total (emergency response)"
        )

    def test_e2e_persona_switching_workflow(self):
        """
        E2E Test: Dynamic Persona Switching Workflow

        Tests persona switching as conversation evolves across different domains.
        """
        start_time = time.time()

        # Conversation Evolution: Platform → Mobile → Data
        conversations = [
            (
                "Our CI/CD pipeline is slow and developer productivity is suffering",
                "platform_director",
            ),
            (
                "The mobile app built by this pipeline has performance issues on iOS",
                "mobile_director",
            ),
            (
                "We need analytics to understand which features are causing the performance problems",
                "data_director",
            ),
        ]

        activation_times = []

        for i, (user_input, expected_template) in enumerate(conversations):
            step_start = time.time()

            # Context Analysis
            context = self.context_engine.analyze_context(user_input)

            # Validate context evolution
            self.assertEqual(context.suggested_template, expected_template)

            # Persona Selection
            selection = self.persona_engine.select_persona(context)
            self.assertEqual(selection.template_id, expected_template)

            # State Management
            self.state_engine.update_state(selection, context, user_input)

            step_time = (time.time() - step_start) * 1000
            activation_times.append(step_time)

            # Validate state consistency
            state = self.state_engine.get_current_state()
            self.assertEqual(state["total_activations"], i + 1)
            self.assertEqual(state["active_persona"], selection.primary)

        # Validate conversation flow
        total_time = (time.time() - start_time) * 1000
        history = self.state_engine.get_activation_history()

        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["template_id"], "platform_director")
        self.assertEqual(history[1]["template_id"], "mobile_director")
        self.assertEqual(history[2]["template_id"], "data_director")

        # Performance validation for switching
        for activation_time in activation_times:
            self.assertLess(activation_time, 1500)  # Each switch should be fast

        print(f"✅ Persona Switching E2E: {total_time:.1f}ms total for 3 switches")

    def test_e2e_low_confidence_fallback_workflow(self):
        """
        E2E Test: Low Confidence Fallback Workflow

        Tests graceful fallback when confidence is low or context is unclear.
        """
        # Test Scenario: Ambiguous input that doesn't clearly match any template
        user_input = (
            "We have some performance issues and need help with optimization strategies"
        )

        start_time = time.time()

        # Step 1: Context Analysis
        context = self.context_engine.analyze_context(user_input)

        # Validate low confidence detection
        self.assertLess(context.confidence, 0.6)  # Should be low confidence
        self.assertEqual(context.confidence_level, ConfidenceLevel.LOW)

        # Step 2: Persona Selection (Should use fallback strategy)
        selection = self.persona_engine.select_persona(context)

        # Validate fallback behavior
        if context.suggested_template:
            # If template suggested, should use fallback persona from that template
            template = self.template_discovery.get_template(context.suggested_template)
            if template and template.personas.fallback:
                self.assertIn(selection.primary, template.personas.fallback)
        else:
            # If no template suggested, should use global fallback
            self.assertEqual(selection.template_id, "fallback")
            self.assertEqual(selection.primary, "camille")

        self.assertIn("fallback", selection.selection_method.lower())

        # Step 3: State Management
        self.state_engine.update_state(selection, context, user_input)

        # Step 4: Performance Validation (Should still be fast)
        total_time = (time.time() - start_time) * 1000
        self.assertLess(total_time, 2000)

        print(
            f"✅ Low Confidence Fallback E2E: {total_time:.1f}ms total, {context.confidence:.2f} confidence"
        )

    def test_e2e_template_commands_integration(self):
        """
        E2E Test: Template Commands Integration

        Tests integration between persona activation and template management commands.
        """
        # Create template commands with our test engine
        template_commands = TemplateCommands(template_engine=self.template_discovery)

        # Test template discovery via CLI
        discovery_result = template_commands.discover_by_context(
            "fintech mobile app security compliance", threshold=0.5
        )

        # Validate discovery results
        self.assertIn("Mobile Engineering Director", discovery_result)
        self.assertIn("fintech", discovery_result.lower())

        # Test template summary with industry and team context
        summary_result = template_commands.generate_summary(
            "mobile_director", "fintech", "startup"
        )

        # Validate summary includes all contexts
        self.assertIn("Mobile Engineering Director", summary_result)
        self.assertIn("security_compliance", summary_result)
        self.assertIn("mvp_velocity", summary_result)
        self.assertIn("resource_constraints", summary_result)

        # Test template comparison
        comparison_result = template_commands.compare_templates(
            ["mobile_director", "product_engineering_director"]
        )

        # Validate comparison shows both templates
        self.assertIn("Mobile Engineering Director", comparison_result)
        self.assertIn("Product Engineering Director", comparison_result)
        self.assertIn("mobile_platforms", comparison_result)
        self.assertIn("product_engineering", comparison_result)

        print("✅ Template Commands Integration E2E: All CLI commands working")

    def test_e2e_template_migration_integration(self):
        """
        E2E Test: Template Migration Integration

        Tests integration between persona activation and template migration.
        """
        # Create migration engine with test directory
        migration_dir = self.test_dir / "migrations"
        migration_engine = TemplateMigrationEngine(
            templates_config_path=self.config_path,
            migrations_dir=migration_dir,
            template_discovery=self.template_discovery,
        )

        # Test version detection
        current_version = migration_engine.detect_config_version()
        self.assertEqual(current_version, "2.0.0")

        # Test backup creation
        backup_info = migration_engine.create_backup()
        self.assertIsNotNone(backup_info.backup_id)
        self.assertEqual(backup_info.template_count, 6)
        self.assertGreater(backup_info.backup_size_bytes, 0)

        # Test configuration validation
        errors = migration_engine._validate_migrated_config(self.test_config)
        self.assertEqual(len(errors), 0)  # Should be valid

        # Test migration commands
        migration_commands = TemplateMigrationCommands(migration_engine)

        # Test version check
        version_result = migration_commands.check_version()
        self.assertIn("up to date", version_result)

        # Test backup listing
        backup_list_result = migration_commands.list_backups()
        self.assertIn(backup_info.backup_id, backup_list_result)

        print("✅ Template Migration Integration E2E: Migration system working")

    def test_e2e_performance_stress_test(self):
        """
        E2E Test: Performance Stress Test

        Tests system performance under repeated activation scenarios.
        """
        test_scenarios = [
            "iOS mobile app crash analysis",
            "product roadmap planning and user research",
            "kubernetes infrastructure deployment issues",
            "data pipeline optimization and ML model performance",
            "backend API scalability and microservices architecture",
            "platform developer tools and CI/CD improvement",
        ]

        total_start_time = time.time()
        activation_times = []

        for i, scenario in enumerate(test_scenarios):
            scenario_start = time.time()

            # Full activation workflow
            context = self.context_engine.analyze_context(scenario)
            selection = self.persona_engine.select_persona(context)
            self.state_engine.update_state(selection, context, scenario)

            scenario_time = (time.time() - scenario_start) * 1000
            activation_times.append(scenario_time)

            # Individual scenario validation
            self.assertLess(scenario_time, 2000)  # Each scenario should be fast
            self.assertGreater(
                context.confidence, 0.4
            )  # Should have reasonable confidence

        total_time = (time.time() - total_start_time) * 1000
        avg_time = sum(activation_times) / len(activation_times)
        max_time = max(activation_times)

        # Performance requirements validation
        self.assertLess(avg_time, 1500)  # Average should be well under limit
        self.assertLess(max_time, 2000)  # No single activation should exceed limit

        # State consistency validation
        final_state = self.state_engine.get_current_state()
        self.assertEqual(final_state["total_activations"], len(test_scenarios))

        history = self.state_engine.get_activation_history()
        self.assertEqual(len(history), len(test_scenarios))

        print(
            f"✅ Performance Stress Test E2E: {total_time:.1f}ms total, {avg_time:.1f}ms avg, {max_time:.1f}ms max"
        )

    def test_e2e_error_handling_resilience(self):
        """
        E2E Test: Error Handling and Resilience

        Tests system behavior under error conditions and edge cases.
        """
        # Test with invalid/corrupted input
        error_scenarios = [
            "",  # Empty input
            "a" * 10000,  # Very long input
            "🤖💻📱🔧⚡",  # Emoji-only input
            "SELECT * FROM users; DROP TABLE templates;",  # Potential injection
            "\n\n\t\t   \r\n",  # Whitespace only
        ]

        for scenario in error_scenarios:
            try:
                context = self.context_engine.analyze_context(scenario)
                selection = self.persona_engine.select_persona(context)
                self.state_engine.update_state(selection, context, scenario)

                # Should gracefully handle all scenarios
                self.assertIsNotNone(context)
                self.assertIsNotNone(selection)

                # Should use fallback for problematic inputs
                if not scenario.strip():  # Empty or whitespace
                    self.assertLess(context.confidence, 0.4)

            except Exception as e:
                self.fail(
                    f"System should handle error scenario gracefully: {scenario[:50]}... Error: {e}"
                )

        print("✅ Error Handling Resilience E2E: System handles edge cases gracefully")

    def test_e2e_real_world_conversation_flow(self):
        """
        E2E Test: Real-World Conversation Flow

        Tests realistic multi-turn conversation with context evolution.
        """
        # Simulate realistic engineering director conversation
        conversation_flow = [
            # Initial problem statement
            (
                "Our mobile app is getting bad reviews in the app store, users are complaining about crashes and slow performance",
                "mobile_director",
            ),
            # Technical deep dive
            (
                "The crashes seem to be happening during payment processing in our fintech app, especially on iOS",
                "mobile_director",
            ),
            # Expanding scope to product strategy
            (
                "This is affecting our user retention and product metrics, we need to understand the business impact",
                "product_engineering_director",
            ),
            # Infrastructure concerns
            (
                "The backend APIs are also showing high latency, might be related to our kubernetes infrastructure",
                "infrastructure_director",
            ),
            # Data analysis need
            (
                "We need analytics to correlate app crashes with API performance and identify patterns",
                "data_director",
            ),
            # Back to mobile for resolution
            (
                "Based on the data, we need to implement better error handling and performance monitoring in the mobile app",
                "mobile_director",
            ),
        ]

        start_time = time.time()
        persona_switches = 0
        last_template = None

        for turn, (user_input, expected_template) in enumerate(conversation_flow):
            # Process conversation turn
            context = self.context_engine.analyze_context(user_input)
            selection = self.persona_engine.select_persona(context)
            self.state_engine.update_state(selection, context, user_input)

            # Track persona switches
            if last_template and selection.template_id != last_template:
                persona_switches += 1
            last_template = selection.template_id

            # Validate expected template selection
            self.assertEqual(
                selection.template_id,
                expected_template,
                f"Turn {turn + 1}: Expected {expected_template}, got {selection.template_id}",
            )

            # Test persona switch suggestions
            if turn > 0:  # Skip first turn
                switch_suggestion = self.state_engine.suggest_persona_switch(context)
                if (
                    context.confidence >= 0.7
                    and context.suggested_template
                    != self.state_engine.current_template_id
                ):
                    self.assertIsNotNone(switch_suggestion)

        total_time = (time.time() - start_time) * 1000

        # Validate conversation metrics
        final_state = self.state_engine.get_current_state()
        self.assertEqual(final_state["total_activations"], len(conversation_flow))
        self.assertGreater(
            persona_switches, 2
        )  # Should have switched personas multiple times

        # Validate conversation history
        history = self.state_engine.get_activation_history()
        self.assertEqual(len(history), len(conversation_flow))

        # Validate performance for extended conversation
        avg_time_per_turn = total_time / len(conversation_flow)
        self.assertLess(avg_time_per_turn, 1000)  # Should maintain performance

        print(
            f"✅ Real-World Conversation E2E: {len(conversation_flow)} turns, {persona_switches} switches, {total_time:.1f}ms total"
        )


class TestCLIIntegrationE2E(unittest.TestCase):
    """End-to-end tests for CLI integration with real claudedirector command"""

    def setUp(self):
        """Set up CLI integration tests"""
        self.cli_available = os.path.exists("./claudedirector")
        if not self.cli_available:
            self.skipTest("claudedirector CLI not available for testing")

    def test_e2e_cli_templates_workflow(self):
        """Test complete templates workflow via CLI"""
        # Test templates list command
        result = subprocess.run(
            ["./claudedirector", "templates", "list"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Director Template", result.stdout)

        # Test templates discover command
        result = subprocess.run(
            ["./claudedirector", "templates", "discover", "mobile app performance"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("mobile", result.stdout.lower())

        # Test templates show command
        result = subprocess.run(
            ["./claudedirector", "templates", "show", "mobile_director"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Mobile Engineering Director", result.stdout)

        print("✅ CLI Templates Workflow E2E: All commands working")

    def test_e2e_cli_performance(self):
        """Test CLI command performance"""
        commands_to_test = [
            ["./claudedirector", "templates", "list"],
            ["./claudedirector", "templates", "domains"],
            ["./claudedirector", "templates", "discover", "test context"],
        ]

        for cmd in commands_to_test:
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            duration = (time.time() - start_time) * 1000

            self.assertEqual(result.returncode, 0)
            self.assertLess(duration, 5000)  # CLI should respond within 5 seconds

        print("✅ CLI Performance E2E: All commands respond quickly")


if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
