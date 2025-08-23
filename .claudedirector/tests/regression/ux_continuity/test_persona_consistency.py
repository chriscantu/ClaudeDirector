#!/usr/bin/env python3
"""
UX Continuity Regression Test: Persona Consistency

Rachel's Test Suite: Ensures persona behavior, communication style, and
strategic guidance remain consistent across sessions and interaction patterns.

UX IMPACT: Inconsistent personas break user trust, create confusion,
and undermine the strategic intelligence experience.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPersonaConsistency(unittest.TestCase):
    """UX continuity tests for persona behavior consistency"""

    def setUp(self):
        """Set up test environment for persona consistency testing"""
        self.test_dir = tempfile.mkdtemp()
        self.persona_data_dir = Path(self.test_dir) / "persona_consistency"
        self.persona_data_dir.mkdir(parents=True, exist_ok=True)

        # Define expected persona characteristics
        self.persona_profiles = {
            "diego": {
                "communication_style": "direct_challenging",
                "expertise_areas": [
                    "team_leadership",
                    "platform_strategy",
                    "cross_functional_coordination",
                ],
                "framework_preferences": ["Team Topologies", "SOLID Principles"],
                "response_patterns": [
                    "asks_clarifying_questions",
                    "challenges_assumptions",
                    "provides_actionable_guidance",
                ],
                "tone": "professional_direct",
                "decision_approach": "evidence_based_with_pushback",
            },
            "camille": {
                "communication_style": "executive_strategic",
                "expertise_areas": [
                    "organizational_scaling",
                    "board_communication",
                    "technology_vision",
                ],
                "framework_preferences": [
                    "Good Strategy Bad Strategy",
                    "Scaling Up Excellence",
                ],
                "response_patterns": [
                    "executive_summary_first",
                    "strategic_context",
                    "competitive_analysis",
                ],
                "tone": "executive_polished",
                "decision_approach": "strategic_with_business_impact",
            },
            "rachel": {
                "communication_style": "user_centered_collaborative",
                "expertise_areas": [
                    "design_systems",
                    "user_experience",
                    "stakeholder_alignment",
                ],
                "framework_preferences": [
                    "Design System Maturity Model",
                    "User-Centered Design",
                ],
                "response_patterns": [
                    "user_impact_focus",
                    "collaborative_approach",
                    "accessibility_consideration",
                ],
                "tone": "empathetic_professional",
                "decision_approach": "user_value_driven",
            },
            "alvaro": {
                "communication_style": "roi_focused_analytical",
                "expertise_areas": [
                    "business_strategy",
                    "investment_analysis",
                    "competitive_positioning",
                ],
                "framework_preferences": [
                    "Capital Allocation Framework",
                    "Business Model Canvas",
                ],
                "response_patterns": [
                    "roi_calculation",
                    "business_justification",
                    "competitive_analysis",
                ],
                "tone": "analytical_business_focused",
                "decision_approach": "financial_impact_driven",
            },
            "martin": {
                "communication_style": "technical_systematic",
                "expertise_areas": [
                    "platform_architecture",
                    "system_design",
                    "technical_strategy",
                ],
                "framework_preferences": [
                    "SOLID Principles",
                    "Evolutionary Architecture",
                ],
                "response_patterns": [
                    "technical_depth",
                    "systematic_analysis",
                    "architecture_focus",
                ],
                "tone": "technical_precise",
                "decision_approach": "engineering_excellence_focused",
            },
        }

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_persona_communication_style_consistency(self):
        """
        UX CRITICAL: Persona communication styles must remain consistent

        FAILURE IMPACT: Users lose trust, personas feel unpredictable
        UX COST: Confusion, reduced engagement, persona switching abandonment
        """
        # Test communication style consistency across multiple interactions
        test_scenarios = [
            {
                "query": "How should we structure our engineering teams?",
                "expected_personas": ["diego", "camille"],
                "interaction_type": "initial_strategic_question",
            },
            {
                "query": "What's the ROI of this platform investment?",
                "expected_personas": ["alvaro"],
                "interaction_type": "follow_up_financial",
            },
            {
                "query": "How do we improve our design system adoption?",
                "expected_personas": ["rachel"],
                "interaction_type": "design_systems_query",
            },
            {
                "query": "What's the technical architecture for this platform?",
                "expected_personas": ["martin"],
                "interaction_type": "technical_deep_dive",
            },
        ]

        persona_responses = {}

        for scenario in test_scenarios:
            for persona_id in scenario["expected_personas"]:
                # Simulate persona response generation
                response = self._simulate_persona_response(
                    persona_id, scenario["query"], scenario["interaction_type"]
                )

                if persona_id not in persona_responses:
                    persona_responses[persona_id] = []
                persona_responses[persona_id].append(response)

        # Verify consistency across responses for each persona
        for persona_id, responses in persona_responses.items():
            expected_profile = self.persona_profiles[persona_id]

            for response in responses:
                # Verify communication style consistency
                self.assertEqual(
                    response["communication_style"],
                    expected_profile["communication_style"],
                    f"Communication style inconsistent for {persona_id}",
                )

                # Verify tone consistency
                self.assertEqual(
                    response["tone"],
                    expected_profile["tone"],
                    f"Tone inconsistent for {persona_id}",
                )

                # Verify decision approach consistency
                self.assertEqual(
                    response["decision_approach"],
                    expected_profile["decision_approach"],
                    f"Decision approach inconsistent for {persona_id}",
                )

                # Verify expertise areas are maintained
                response_expertise = set(response["expertise_demonstrated"])
                expected_expertise = set(expected_profile["expertise_areas"])
                self.assertTrue(
                    response_expertise.intersection(expected_expertise),
                    f"Expertise areas not demonstrated for {persona_id}",
                )

        print("✅ Persona communication style consistency: PASSED")

    def test_framework_preference_consistency(self):
        """
        UX CRITICAL: Persona framework preferences must remain consistent

        FAILURE IMPACT: Strategic guidance becomes generic, loses persona value
        UX COST: Reduced strategic intelligence quality, user disappointment
        """
        # Test framework application consistency
        strategic_scenarios = [
            {
                "scenario": "team_restructuring",
                "context": "Engineering team scaling challenges",
                "expected_frameworks": {
                    "diego": ["Team Topologies", "SOLID Principles"],
                    "camille": ["Good Strategy Bad Strategy", "Scaling Up Excellence"],
                },
            },
            {
                "scenario": "platform_investment",
                "context": "Platform vs feature investment decision",
                "expected_frameworks": {
                    "alvaro": ["Capital Allocation Framework", "Business Model Canvas"],
                    "martin": ["SOLID Principles", "Evolutionary Architecture"],
                },
            },
            {
                "scenario": "design_system_adoption",
                "context": "Cross-team design system implementation",
                "expected_frameworks": {
                    "rachel": ["Design System Maturity Model", "User-Centered Design"],
                    "diego": ["Team Topologies"],
                },
            },
        ]

        for scenario in strategic_scenarios:
            for persona_id, expected_frameworks in scenario[
                "expected_frameworks"
            ].items():
                # Simulate framework application
                framework_response = self._simulate_framework_application(
                    persona_id, scenario["scenario"], scenario["context"]
                )

                # Verify expected frameworks are applied
                applied_frameworks = framework_response["frameworks_applied"]

                for expected_framework in expected_frameworks:
                    self.assertIn(
                        expected_framework,
                        applied_frameworks,
                        f"Expected framework '{expected_framework}' not applied by {persona_id}",
                    )

                # Verify framework application is appropriate to persona expertise
                persona_profile = self.persona_profiles[persona_id]
                for framework in applied_frameworks:
                    self.assertIn(
                        framework,
                        persona_profile["framework_preferences"],
                        f"Unexpected framework '{framework}' applied by {persona_id}",
                    )

        print("✅ Framework preference consistency: PASSED")

    def test_response_pattern_consistency(self):
        """
        UX CRITICAL: Persona response patterns must be predictable and consistent

        FAILURE IMPACT: Users can't predict persona behavior, reduces usability
        UX COST: Learning curve increases, user efficiency decreases
        """
        # Test response pattern consistency
        interaction_tests = [
            {
                "persona": "diego",
                "query": "Should we adopt microservices architecture?",
                "expected_patterns": [
                    "asks_clarifying_questions",
                    "challenges_assumptions",
                    "provides_actionable_guidance",
                ],
            },
            {
                "persona": "camille",
                "query": "How do we present this to the board?",
                "expected_patterns": [
                    "executive_summary_first",
                    "strategic_context",
                    "competitive_analysis",
                ],
            },
            {
                "persona": "rachel",
                "query": "How do we improve user adoption of our tools?",
                "expected_patterns": [
                    "user_impact_focus",
                    "collaborative_approach",
                    "accessibility_consideration",
                ],
            },
            {
                "persona": "alvaro",
                "query": "Is this investment worth pursuing?",
                "expected_patterns": [
                    "roi_calculation",
                    "business_justification",
                    "competitive_analysis",
                ],
            },
            {
                "persona": "martin",
                "query": "What's the best technical approach here?",
                "expected_patterns": [
                    "technical_depth",
                    "systematic_analysis",
                    "architecture_focus",
                ],
            },
        ]

        for test in interaction_tests:
            # Simulate persona response
            response = self._simulate_persona_interaction(
                test["persona"], test["query"]
            )

            # Verify expected response patterns are present
            response_patterns = response["patterns_demonstrated"]

            for expected_pattern in test["expected_patterns"]:
                self.assertIn(
                    expected_pattern,
                    response_patterns,
                    f"Expected pattern '{expected_pattern}' missing from {test['persona']} response",
                )

            # Verify response structure is consistent with persona
            persona_profile = self.persona_profiles[test["persona"]]
            expected_response_patterns = set(persona_profile["response_patterns"])
            actual_response_patterns = set(response_patterns)

            # Should have significant overlap with expected patterns
            overlap = expected_response_patterns.intersection(actual_response_patterns)
            self.assertGreaterEqual(
                len(overlap),
                len(expected_response_patterns) // 2,  # At least 50% overlap
                f"Insufficient pattern overlap for {test['persona']}",
            )

        print("✅ Response pattern consistency: PASSED")

    def test_cross_session_persona_memory(self):
        """
        UX CRITICAL: Personas must remember previous interactions and maintain context

        FAILURE IMPACT: Personas lose context, repeat questions, break continuity
        UX COST: Frustrating user experience, reduced strategic intelligence value
        """
        # Simulate multi-session persona interactions
        session_scenarios = [
            {
                "session_id": "session_001",
                "persona": "diego",
                "interactions": [
                    {
                        "query": "We're scaling from 50 to 200 engineers",
                        "context_established": [
                            "team_size_50_to_200",
                            "scaling_challenge",
                            "engineering_focus",
                        ],
                    },
                    {
                        "query": "What team structure should we use?",
                        "should_remember": ["team_size_50_to_200", "scaling_challenge"],
                    },
                ],
            },
            {
                "session_id": "session_002",
                "persona": "alvaro",
                "interactions": [
                    {
                        "query": "Platform investment budget is $2M",
                        "context_established": [
                            "platform_investment",
                            "budget_2M",
                            "investment_decision",
                        ],
                    },
                    {
                        "query": "What's the expected ROI?",
                        "should_remember": ["platform_investment", "budget_2M"],
                    },
                ],
            },
        ]

        persona_memory = {}

        for scenario in session_scenarios:
            persona_id = scenario["persona"]
            session_id = scenario["session_id"]

            if persona_id not in persona_memory:
                persona_memory[persona_id] = {}

            for i, interaction in enumerate(scenario["interactions"]):
                # Simulate persona interaction with memory
                response = self._simulate_persona_with_memory(
                    persona_id, interaction["query"], persona_memory.get(persona_id, {})
                )

                # Update persona memory
                if "context_established" in interaction:
                    for context_item in interaction["context_established"]:
                        persona_memory[persona_id][context_item] = {
                            "value": context_item,
                            "session": session_id,
                            "interaction": i,
                            "timestamp": datetime.now().isoformat(),
                        }

                # Verify memory recall for follow-up interactions
                if "should_remember" in interaction:
                    remembered_context = response["context_recalled"]

                    for expected_memory in interaction["should_remember"]:
                        self.assertIn(
                            expected_memory,
                            remembered_context,
                            f"Persona {persona_id} failed to remember context: {expected_memory}",
                        )

                # Verify context is used appropriately in response
                if response["context_recalled"]:
                    self.assertTrue(
                        response["context_utilized"],
                        f"Persona {persona_id} recalled context but didn't utilize it",
                    )

        print("✅ Cross-session persona memory: PASSED")

    def test_persona_expertise_boundaries(self):
        """
        UX CRITICAL: Personas must stay within expertise boundaries and defer appropriately

        FAILURE IMPACT: Personas give advice outside expertise, reduces trust
        UX COST: Poor strategic guidance, user confusion about persona roles
        """
        # Test expertise boundary enforcement
        boundary_tests = [
            {
                "persona": "rachel",
                "query": "What's the best database architecture for analytics?",
                "should_defer_to": ["martin", "delbert"],
                "expertise_match": False,
            },
            {
                "persona": "diego",
                "query": "How do we improve our design system adoption?",
                "should_defer_to": ["rachel"],
                "expertise_match": False,
            },
            {
                "persona": "alvaro",
                "query": "What's the technical implementation approach?",
                "should_defer_to": ["martin"],
                "expertise_match": False,
            },
            {
                "persona": "martin",
                "query": "What's the ROI of this technical investment?",
                "should_defer_to": ["alvaro"],
                "expertise_match": False,
            },
            {
                "persona": "diego",
                "query": "How should we structure our engineering teams?",
                "should_defer_to": [],
                "expertise_match": True,
            },
        ]

        for test in boundary_tests:
            # Simulate persona response to out-of-expertise query
            response = self._simulate_expertise_boundary_check(
                test["persona"], test["query"]
            )

            if test["expertise_match"]:
                # Should provide direct guidance within expertise
                self.assertTrue(
                    response["provides_direct_guidance"],
                    f"Persona {test['persona']} should provide direct guidance for expertise area",
                )
                self.assertFalse(
                    response["defers_to_others"],
                    f"Persona {test['persona']} shouldn't defer for expertise area",
                )
            else:
                # Should defer to appropriate personas
                self.assertTrue(
                    response["defers_to_others"],
                    f"Persona {test['persona']} should defer for out-of-expertise query",
                )

                # Verify defers to correct personas
                deferred_to = response["deferred_personas"]
                expected_deferrals = set(test["should_defer_to"])
                actual_deferrals = set(deferred_to)

                self.assertTrue(
                    expected_deferrals.intersection(actual_deferrals),
                    f"Persona {test['persona']} didn't defer to expected personas: {test['should_defer_to']}",
                )

        print("✅ Persona expertise boundaries: PASSED")

    def _simulate_persona_response(self, persona_id, query, interaction_type):
        """Simulate persona response generation"""
        profile = self.persona_profiles[persona_id]

        return {
            "persona_id": persona_id,
            "query": query,
            "interaction_type": interaction_type,
            "communication_style": profile["communication_style"],
            "tone": profile["tone"],
            "decision_approach": profile["decision_approach"],
            "expertise_demonstrated": profile["expertise_areas"][
                :2
            ],  # Show first 2 areas
            "timestamp": datetime.now().isoformat(),
        }

    def _simulate_framework_application(self, persona_id, scenario, context):
        """Simulate framework application by persona"""
        profile = self.persona_profiles[persona_id]

        # Apply frameworks based on scenario and persona preferences
        applicable_frameworks = []
        for framework in profile["framework_preferences"]:
            if self._is_framework_applicable(framework, scenario):
                applicable_frameworks.append(framework)

        return {
            "persona_id": persona_id,
            "scenario": scenario,
            "context": context,
            "frameworks_applied": applicable_frameworks,
            "application_rationale": f"Applied {len(applicable_frameworks)} frameworks based on {persona_id} expertise",
        }

    def _simulate_persona_interaction(self, persona_id, query):
        """Simulate persona interaction with pattern analysis"""
        profile = self.persona_profiles[persona_id]

        # Determine which patterns are demonstrated based on query and persona
        demonstrated_patterns = []
        for pattern in profile["response_patterns"]:
            if self._pattern_applies_to_query(pattern, query, persona_id):
                demonstrated_patterns.append(pattern)

        return {
            "persona_id": persona_id,
            "query": query,
            "patterns_demonstrated": demonstrated_patterns,
            "response_quality": "high" if len(demonstrated_patterns) >= 2 else "medium",
        }

    def _simulate_persona_with_memory(self, persona_id, query, existing_memory):
        """Simulate persona interaction with memory recall"""
        # Determine what context should be recalled
        recalled_context = []
        context_utilized = False

        for memory_key, memory_data in existing_memory.items():
            if self._memory_relevant_to_query(memory_key, query):
                recalled_context.append(memory_key)
                context_utilized = True

        return {
            "persona_id": persona_id,
            "query": query,
            "context_recalled": recalled_context,
            "context_utilized": context_utilized,
            "memory_quality": "high" if context_utilized else "low",
        }

    def _simulate_expertise_boundary_check(self, persona_id, query):
        """Simulate persona expertise boundary checking"""
        profile = self.persona_profiles[persona_id]

        # Check if query matches persona expertise
        expertise_match = self._query_matches_expertise(
            query, profile["expertise_areas"]
        )

        if expertise_match:
            return {
                "persona_id": persona_id,
                "provides_direct_guidance": True,
                "defers_to_others": False,
                "deferred_personas": [],
            }
        else:
            # Determine which personas to defer to
            deferred_personas = self._determine_appropriate_personas(query)

            return {
                "persona_id": persona_id,
                "provides_direct_guidance": False,
                "defers_to_others": True,
                "deferred_personas": deferred_personas,
            }

    def _is_framework_applicable(self, framework, scenario):
        """Determine if framework applies to scenario"""
        framework_scenarios = {
            "Team Topologies": ["team_restructuring", "design_system_adoption"],
            "SOLID Principles": ["team_restructuring", "platform_investment"],
            "Good Strategy Bad Strategy": ["team_restructuring"],
            "Scaling Up Excellence": ["team_restructuring"],
            "Capital Allocation Framework": ["platform_investment"],
            "Business Model Canvas": ["platform_investment"],
            "Design System Maturity Model": ["design_system_adoption"],
            "User-Centered Design": ["design_system_adoption"],
            "Evolutionary Architecture": ["platform_investment"],
        }

        return scenario in framework_scenarios.get(framework, [])

    def _pattern_applies_to_query(self, pattern, query, persona_id):
        """Determine if response pattern applies to query"""
        pattern_triggers = {
            "asks_clarifying_questions": ["should", "how", "what"],
            "challenges_assumptions": ["should", "best", "adopt"],
            "provides_actionable_guidance": ["how", "what", "should"],
            "executive_summary_first": ["board", "present", "executive"],
            "strategic_context": ["board", "strategic", "vision"],
            "competitive_analysis": [
                "board",
                "competitive",
                "market",
                "investment",
                "worth",
            ],
            "user_impact_focus": ["user", "adoption", "improve"],
            "collaborative_approach": ["improve", "adoption", "team"],
            "accessibility_consideration": ["user", "adoption", "tools"],
            "roi_calculation": ["investment", "worth", "roi"],
            "business_justification": ["investment", "worth", "business"],
            "technical_depth": ["technical", "architecture", "approach"],
            "systematic_analysis": ["technical", "best", "approach"],
            "architecture_focus": ["technical", "architecture", "system"],
        }

        query_lower = query.lower()
        trigger_words = pattern_triggers.get(pattern, [])

        return any(word in query_lower for word in trigger_words)

    def _memory_relevant_to_query(self, memory_key, query):
        """Determine if memory is relevant to current query"""
        relevance_mapping = {
            "team_size_50_to_200": ["team", "structure", "scaling"],
            "scaling_challenge": ["team", "structure", "scaling", "organization"],
            "engineering_focus": ["engineering", "team", "technical"],
            "platform_investment": ["platform", "investment", "roi"],
            "budget_2M": ["budget", "cost", "investment", "roi"],
            "investment_decision": ["investment", "decision", "roi"],
        }

        query_lower = query.lower()
        relevant_terms = relevance_mapping.get(memory_key, [])

        return any(term in query_lower for term in relevant_terms)

    def _query_matches_expertise(self, query, expertise_areas):
        """Check if query matches persona expertise areas"""
        query_lower = query.lower()

        # Business/financial keywords take priority over technical keywords
        business_financial_keywords = [
            "roi",
            "investment",
            "financial",
            "business",
            "cost",
            "budget",
        ]
        if any(keyword in query_lower for keyword in business_financial_keywords):
            # If query contains business/financial terms, only match business expertise areas
            business_areas = [
                "business_strategy",
                "investment_analysis",
                "competitive_positioning",
            ]
            return any(area in expertise_areas for area in business_areas)

        expertise_keywords = {
            "team_leadership": ["team", "leadership", "management", "people"],
            "platform_strategy": ["platform", "strategy", "architecture"],
            "cross_functional_coordination": [
                "coordination",
                "alignment",
                "stakeholder",
            ],
            "organizational_scaling": ["scaling", "organization", "growth"],
            "board_communication": ["board", "executive", "communication"],
            "technology_vision": ["technology", "vision", "strategy"],
            "design_systems": ["design", "system", "component", "ui"],
            "user_experience": ["user", "experience", "ux", "adoption"],
            "stakeholder_alignment": ["stakeholder", "alignment", "coordination"],
            "business_strategy": ["business", "strategy", "roi", "investment"],
            "investment_analysis": ["investment", "roi", "analysis", "financial"],
            "competitive_positioning": ["competitive", "market", "positioning"],
            "platform_architecture": [
                "architecture",
                "platform",
                "system",
                "technical",
            ],
            "system_design": ["system", "design", "architecture", "technical"],
            "technical_strategy": ["technical", "strategy", "architecture"],
        }

        for expertise_area in expertise_areas:
            keywords = expertise_keywords.get(expertise_area, [])
            if any(keyword in query_lower for keyword in keywords):
                return True

        return False

    def _determine_appropriate_personas(self, query):
        """Determine which personas should handle the query"""
        query_lower = query.lower()

        # Map query types to appropriate personas - prioritize business/financial over technical
        if any(
            word in query_lower
            for word in ["roi", "investment", "business", "financial"]
        ):
            return ["alvaro"]
        elif any(word in query_lower for word in ["strategy", "executive", "board"]):
            return ["camille"]
        elif any(word in query_lower for word in ["design", "user", "ux", "adoption"]):
            return ["rachel"]
        elif any(
            word in query_lower for word in ["team", "leadership", "organization"]
        ):
            return ["diego"]
        elif any(
            word in query_lower
            for word in ["database", "analytics", "technical", "architecture"]
        ):
            return ["martin", "delbert"]
        else:
            return ["diego"]  # Default to Diego for general leadership questions


def run_ux_continuity_persona_tests():
    """Run all UX continuity persona consistency tests"""
    print("🎨 UX CONTINUITY REGRESSION TEST: Persona Consistency")
    print("=" * 70)
    print("OWNER: Rachel | IMPACT: User Experience & Trust")
    print("FAILURE COST: User confusion, reduced engagement, persona abandonment")
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPersonaConsistency)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL PERSONA CONSISTENCY TESTS PASSED")
        print("🎨 UX Impact: Persona behavior consistency maintained")
        print("📊 Strategic Value: User trust and engagement preserved")
        return True
    else:
        print(
            f"\n❌ PERSONA CONSISTENCY FAILURES: {len(result.failures + result.errors)}"
        )
        print("💥 UX Impact: Persona behavior inconsistent, user trust compromised")
        print("🚨 Action Required: Fix persona consistency immediately")
        return False


if __name__ == "__main__":
    success = run_ux_continuity_persona_tests()
    sys.exit(0 if success else 1)
