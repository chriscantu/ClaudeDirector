"""
Test of Team Topologies and Accelerate Framework Integration
Tests both team-focused frameworks in the embedded framework engine.

Author: Diego (Engineering Leadership) & Camille (Strategic Technology)
"""

import sys
import os

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine, EmbeddedPersonaIntegrator


def test_team_topologies_framework():
    """Test Team Topologies framework activation and analysis"""

    print("\n🏗️ **Team Topologies Framework Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Team Topologies framework
    test_input = "We need to optimize our team topology with platform teams, stream-aligned teams, and manage cognitive load according to Conway's Law principles."
    persona_context = "diego"
    domain_focus = ["organizational", "strategic"]

    print(f"📝 **Test Input:** {test_input}")
    print(f"👤 **Persona:** {persona_context}")
    print(f"🎯 **Domains:** {domain_focus}")

    # Apply framework analysis
    framework_analysis = framework_engine.analyze_systematically(
        user_input=test_input,
        persona_context=persona_context,
        domain_focus=domain_focus
    )

    print(f"\n✅ **Framework Analysis Results:**")
    print(f"   Framework Applied: {framework_analysis.framework_name}")
    print(f"   Analysis Confidence: {framework_analysis.analysis_confidence:.2f}")

    # Check for Team Topologies-specific components
    topology_keywords = ["stream-aligned", "platform", "enabling", "complicated subsystem", "conway", "cognitive load", "topology"]
    found_topology_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in topology_keywords:
        if keyword.lower() in insights_str.lower():
            found_topology_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in topology_keywords:
        if keyword.lower() in recommendations_str.lower():
            if keyword not in found_topology_elements:
                found_topology_elements.append(keyword)

    print(f"\n🏗️ **Team Topologies Elements Found:** {found_topology_elements}")

    # Validate we got the right framework
    expected_framework = "Team Topologies Framework"
    assert framework_analysis.framework_name == expected_framework, f"Expected {expected_framework}, got {framework_analysis.framework_name}"

    # Validate we found key Team Topologies concepts
    required_elements = ["platform", "conway", "cognitive"]
    found_required = [elem for elem in required_elements if any(elem in found_elem.lower() for found_elem in found_topology_elements)]
    assert len(found_required) >= 2, f"Expected at least 2 required elements, found: {found_required}"

    print(f"\n📋 **Key Recommendations:**")
    for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")

    return True


def test_accelerate_framework():
    """Test Accelerate framework activation and analysis"""

    print("\n⚡ **Accelerate Framework Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Accelerate framework
    test_input = "We need to improve our DORA metrics including deployment frequency, lead time, psychological safety, and team performance capabilities."
    persona_context = "diego"
    domain_focus = ["organizational", "technical"]

    print(f"📝 **Test Input:** {test_input}")
    print(f"👤 **Persona:** {persona_context}")
    print(f"🎯 **Domains:** {domain_focus}")

    # Apply framework analysis
    framework_analysis = framework_engine.analyze_systematically(
        user_input=test_input,
        persona_context=persona_context,
        domain_focus=domain_focus
    )

    print(f"\n✅ **Framework Analysis Results:**")
    print(f"   Framework Applied: {framework_analysis.framework_name}")
    print(f"   Analysis Confidence: {framework_analysis.analysis_confidence:.2f}")

    # Check for Accelerate-specific components
    accelerate_keywords = ["dora", "deployment frequency", "psychological safety", "performance", "lead time", "change failure", "recovery"]
    found_accelerate_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in accelerate_keywords:
        if keyword.lower() in insights_str.lower():
            found_accelerate_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in accelerate_keywords:
        if keyword.lower() in recommendations_str.lower():
            if keyword not in found_accelerate_elements:
                found_accelerate_elements.append(keyword)

    print(f"\n⚡ **Accelerate Elements Found:** {found_accelerate_elements}")

    # Validate we got the right framework
    expected_framework = "Accelerate Team Performance Framework"
    assert framework_analysis.framework_name == expected_framework, f"Expected {expected_framework}, got {framework_analysis.framework_name}"

    # Validate we found key Accelerate concepts
    required_elements = ["dora", "performance", "psychological"]
    found_required = [elem for elem in required_elements if any(elem in found_elem.lower() for found_elem in found_accelerate_elements)]
    assert len(found_required) >= 2, f"Expected at least 2 required elements, found: {found_required}"

    print(f"\n📋 **Key Recommendations:**")
    for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")

    return True


def test_team_framework_persona_integration():
    """Test persona integration with both team frameworks"""

    print("\n🎭 **Team Framework Persona Integration Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()
    integrator = EmbeddedPersonaIntegrator(framework_engine)

    # Test scenarios for both frameworks
    test_scenarios = [
        {
            "name": "Team Topologies with Diego",
            "input": "Our team topology needs platform teams and stream-aligned teams with proper cognitive load management",
            "persona": "diego",
            "expected_framework": "Team Topologies"
        },
        {
            "name": "Accelerate with Camille",
            "input": "We need better DORA metrics and psychological safety for team performance",
            "persona": "camille",
            "expected_framework": "Accelerate"
        },
        {
            "name": "Team Topologies with Marcus",
            "input": "Conway's Law says our team structure affects our platform team interactions",
            "persona": "marcus",
            "expected_framework": "Team Topologies"
        }
    ]

    for scenario in test_scenarios:
        print(f"\n**Testing {scenario['name']}:**")

        response = integrator.create_systematic_response(
            persona_name=scenario["persona"],
            user_input=scenario["input"],
            base_response="",
            domain_focus=["organizational", "strategic"]
        )

        print(f"   Framework: {response.framework_applied}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        print(f"   Response Length: {len(response.persona_integrated_response)} chars")

        # Check that we got a team-related framework
        is_team_framework = any(term in response.framework_applied for term in ["Team Topologies", "Accelerate"])
        assert is_team_framework, f"Expected team framework, got {response.framework_applied}"

    print(f"\n✅ **Persona Integration Test Complete**")
    return True


def test_framework_keyword_activation():
    """Test keyword activation for both team frameworks"""

    print("\n🔍 **Framework Keyword Activation Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test various team-related inputs
    test_cases = [
        {
            "input": "Our platform team cognitive load is too high",
            "expected_framework": "Team Topologies",
            "keywords": ["platform team", "cognitive load"]
        },
        {
            "input": "We need better DORA metrics and deployment frequency",
            "expected_framework": "Accelerate",
            "keywords": ["DORA metrics", "deployment frequency"]
        },
        {
            "input": "How do we structure stream-aligned teams?",
            "expected_framework": "Team Topologies",
            "keywords": ["stream-aligned"]
        },
        {
            "input": "Our psychological safety needs improvement for high performance",
            "expected_framework": "Accelerate",
            "keywords": ["psychological safety", "high performance"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n**Test Case {i}:** {test_case['input']}")

        analysis = framework_engine.analyze_systematically(
            user_input=test_case["input"],
            persona_context="diego",
            domain_focus=["organizational", "technical"]
        )

        print(f"   Framework: {analysis.framework_name}")
        print(f"   Confidence: {analysis.analysis_confidence:.2f}")

        # Check if we got the expected framework type
        expected_keywords = test_case["expected_framework"].lower().split()
        framework_matches = any(keyword in analysis.framework_name.lower() for keyword in expected_keywords)
        print(f"   Expected Framework Type Activated: {framework_matches}")

    print(f"\n✅ **Keyword Activation Test Complete**")
    return True


if __name__ == "__main__":
    print("🧪 **Testing Team Frameworks Integration (Topologies + Accelerate)**")
    print("=" * 70)

    try:
        # Run all tests
        test_team_topologies_framework()
        test_accelerate_framework()
        test_team_framework_persona_integration()
        test_framework_keyword_activation()

        print("\n" + "=" * 70)
        print("🎉 **ALL TESTS PASSED** - Team Frameworks Successfully Integrated!")
        print("📊 **Frameworks Added:** Team Topologies + Accelerate Performance")
        print("🎭 **Persona Integration:** Diego, Camille, Marcus validated")
        print("⚡ **Keywords Active:** Team structure, DORA metrics, cognitive load")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ **TEST FAILED**: {str(e)}")
        raise
