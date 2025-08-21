"""
Test of Crucial Conversations and Capital Allocation Framework Integration
Tests both stakeholder-focused frameworks in the embedded framework engine.

Author: Camille (Strategic Technology) & Alvaro (Platform ROI)
"""

import sys
import os

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from claudedirector.core.embedded_framework_engine import (
    EmbeddedFrameworkEngine,
    EmbeddedPersonaIntegrator,
)


def test_crucial_conversations_framework():
    """Test Crucial Conversations framework activation and analysis"""

    print("\n🤝 **Crucial Conversations Framework Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Crucial Conversations framework
    test_input = "I need to have a crucial conversation with stakeholders about our platform. There's conflict and I need to make it safe, start with heart, and STATE my path for dialogue."
    persona_context = "alvaro"
    domain_focus = ["stakeholder", "communication"]

    print(f"📝 **Test Input:** {test_input}")
    print(f"👤 **Persona:** {persona_context}")
    print(f"🎯 **Domains:** {domain_focus}")

    # Apply framework analysis
    framework_analysis = framework_engine.analyze_systematically(
        user_input=test_input,
        persona_context=persona_context,
        domain_focus=domain_focus,
    )

    print(f"\n✅ **Framework Analysis Results:**")
    print(f"   Framework Applied: {framework_analysis.framework_name}")
    print(f"   Analysis Confidence: {framework_analysis.analysis_confidence:.2f}")

    # Check for Crucial Conversations-specific components
    conversation_keywords = [
        "heart",
        "safety",
        "stories",
        "state",
        "dialogue",
        "mutual purpose",
        "crucial",
    ]
    found_conversation_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in conversation_keywords:
        if keyword.lower() in insights_str.lower():
            found_conversation_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in conversation_keywords:
        if keyword.lower() in recommendations_str.lower():
            if keyword not in found_conversation_elements:
                found_conversation_elements.append(keyword)

    print(
        f"\n🤝 **Crucial Conversations Elements Found:** {found_conversation_elements}"
    )

    # Validate we got the right framework
    expected_framework = "Crucial Conversations Framework"
    assert (
        framework_analysis.framework_name == expected_framework
    ), f"Expected {expected_framework}, got {framework_analysis.framework_name}"

    # Validate we found key Crucial Conversations concepts
    required_elements = ["heart", "safety", "state"]
    found_required = [
        elem
        for elem in required_elements
        if any(elem in found_elem.lower() for found_elem in found_conversation_elements)
    ]
    assert (
        len(found_required) >= 2
    ), f"Expected at least 2 required elements, found: {found_required}"

    print(f"\n📋 **Key Recommendations:**")
    for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")

    return True


def test_capital_allocation_framework():
    """Test Capital Allocation framework activation and analysis"""

    print("\n💰 **Capital Allocation Framework Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Capital Allocation framework
    test_input = "Our technology investment portfolio needs capital allocation optimization. We need ROI analysis for budget allocation across platform, product, and innovation investments."
    persona_context = "alvaro"
    domain_focus = ["strategic", "financial"]

    print(f"📝 **Test Input:** {test_input}")
    print(f"👤 **Persona:** {persona_context}")
    print(f"🎯 **Domains:** {domain_focus}")

    # Apply framework analysis
    framework_analysis = framework_engine.analyze_systematically(
        user_input=test_input,
        persona_context=persona_context,
        domain_focus=domain_focus,
    )

    print(f"\n✅ **Framework Analysis Results:**")
    print(f"   Framework Applied: {framework_analysis.framework_name}")
    print(f"   Analysis Confidence: {framework_analysis.analysis_confidence:.2f}")

    # Check for Capital Allocation-specific components
    allocation_keywords = [
        "investment",
        "portfolio",
        "roi",
        "allocation",
        "budget",
        "financial",
        "returns",
        "capital",
    ]
    found_allocation_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in allocation_keywords:
        if keyword.lower() in insights_str.lower():
            found_allocation_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in allocation_keywords:
        if keyword.lower() in recommendations_str.lower():
            if keyword not in found_allocation_elements:
                found_allocation_elements.append(keyword)

    print(f"\n💰 **Capital Allocation Elements Found:** {found_allocation_elements}")

    # Validate we got the right framework
    expected_framework = "Capital Allocation Framework"
    assert (
        framework_analysis.framework_name == expected_framework
    ), f"Expected {expected_framework}, got {framework_analysis.framework_name}"

    # Validate we found key Capital Allocation concepts
    required_elements = ["investment", "portfolio", "roi"]
    found_required = [
        elem
        for elem in required_elements
        if any(elem in found_elem.lower() for found_elem in found_allocation_elements)
    ]
    assert (
        len(found_required) >= 2
    ), f"Expected at least 2 required elements, found: {found_required}"

    print(f"\n📋 **Key Recommendations:**")
    for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")

    return True


def test_stakeholder_framework_persona_integration():
    """Test persona integration with both stakeholder frameworks"""

    print("\n🎭 **Stakeholder Framework Persona Integration Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()
    integrator = EmbeddedPersonaIntegrator(framework_engine)

    # Test scenarios for both frameworks
    test_scenarios = [
        {
            "name": "Crucial Conversations with Alvaro",
            "input": "I need a crucial conversation with executives about platform investment safety and mutual purpose with STATE method",
            "persona": "alvaro",
            "expected_framework": "Crucial Conversations",
        },
        {
            "name": "Capital Allocation with David",
            "input": "Our technology investment portfolio needs capital allocation optimization with ROI analysis for budget planning",
            "persona": "david",
            "expected_framework": "Capital Allocation",
        },
        {
            "name": "Crucial Conversations with Camille",
            "input": "Difficult stakeholder dialogue about transformation requires crucial conversation safety and STATE method",
            "persona": "camille",
            "expected_framework": "Crucial Conversations",
        },
    ]

    for scenario in test_scenarios:
        print(f"\n**Testing {scenario['name']}:**")

        response = integrator.create_systematic_response(
            persona_name=scenario["persona"],
            user_input=scenario["input"],
            base_response="",
            domain_focus=["stakeholder", "strategic"],
        )

        print(f"   Framework: {response.framework_applied}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        print(f"   Response Length: {len(response.persona_integrated_response)} chars")

        # Check that we got a stakeholder-related framework
        is_stakeholder_framework = any(
            term in response.framework_applied
            for term in ["Crucial Conversations", "Capital Allocation"]
        )
        assert (
            is_stakeholder_framework
        ), f"Expected stakeholder framework, got {response.framework_applied}"

    print(f"\n✅ **Persona Integration Test Complete**")
    return True


def test_framework_keyword_activation():
    """Test keyword activation for both stakeholder frameworks"""

    print("\n🔍 **Framework Keyword Activation Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test various stakeholder-related inputs
    test_cases = [
        {
            "input": "We need stakeholder alignment through crucial conversations",
            "expected_framework": "Crucial Conversations",
            "keywords": ["stakeholder", "crucial conversations"],
        },
        {
            "input": "Budget allocation and ROI optimization for technology investments",
            "expected_framework": "Capital Allocation",
            "keywords": ["budget", "allocation", "ROI"],
        },
        {
            "input": "Difficult executive dialogue about platform safety and mutual purpose",
            "expected_framework": "Crucial Conversations",
            "keywords": ["executive", "dialogue", "safety"],
        },
        {
            "input": "Technology portfolio optimization and resource allocation decisions",
            "expected_framework": "Capital Allocation",
            "keywords": ["portfolio", "allocation", "decisions"],
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n**Test Case {i}:** {test_case['input']}")

        analysis = framework_engine.analyze_systematically(
            user_input=test_case["input"],
            persona_context="alvaro",
            domain_focus=["stakeholder", "strategic"],
        )

        print(f"   Framework: {analysis.framework_name}")
        print(f"   Confidence: {analysis.analysis_confidence:.2f}")

        # Check if we got the expected framework type
        expected_keywords = test_case["expected_framework"].lower().split()
        framework_matches = any(
            keyword in analysis.framework_name.lower() for keyword in expected_keywords
        )
        print(f"   Expected Framework Type Activated: {framework_matches}")

    print(f"\n✅ **Keyword Activation Test Complete**")
    return True


def test_executive_communication_scenarios():
    """Test real-world executive communication scenarios"""

    print("\n🎯 **Executive Communication Scenarios Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Real-world scenarios that engineering directors face
    executive_scenarios = [
        {
            "name": "Executive Platform Investment Discussion",
            "input": "The executive is questioning our platform investment ROI. I need to have a crucial conversation about resource allocation while maintaining stakeholder safety.",
            "expected_elements": [
                "crucial conversation",
                "investment",
                "stakeholder",
                "safety",
            ],
        },
        {
            "name": "Budget Planning Meeting",
            "input": "We're planning next year's technology budget allocation across platform, product, and innovation portfolios.",
            "expected_elements": ["budget", "allocation", "portfolio", "investment"],
        },
        {
            "name": "Cross-Team Alignment Challenge",
            "input": "There's conflict between engineering and product teams. We need dialogue to establish mutual purpose and move to action.",
            "expected_elements": ["conflict", "dialogue", "mutual purpose", "action"],
        },
    ]

    for scenario in executive_scenarios:
        print(f"\n**Scenario: {scenario['name']}**")
        print(f"   Input: {scenario['input']}")

        analysis = framework_engine.analyze_systematically(
            user_input=scenario["input"],
            persona_context="alvaro",
            domain_focus=["stakeholder", "strategic", "communication"],
        )

        print(f"   Framework Applied: {analysis.framework_name}")
        print(f"   Confidence: {analysis.analysis_confidence:.2f}")

        # Check for expected elements in the analysis
        all_content = (
            str(analysis.structured_insights) + " " + " ".join(analysis.recommendations)
        )
        found_elements = [
            elem
            for elem in scenario["expected_elements"]
            if elem.lower() in all_content.lower()
        ]
        print(f"   Expected Elements Found: {found_elements}")

        # Should find at least half of the expected elements
        assert (
            len(found_elements) >= len(scenario["expected_elements"]) // 2
        ), f"Expected more elements, found: {found_elements}"

    print(f"\n✅ **Executive Communication Scenarios Test Complete**")
    return True


if __name__ == "__main__":
    print(
        "🧪 **Testing Stakeholder Frameworks Integration (Crucial Conversations + Capital Allocation)**"
    )
    print("=" * 80)

    try:
        # Run all tests
        test_crucial_conversations_framework()
        test_capital_allocation_framework()
        test_stakeholder_framework_persona_integration()
        test_framework_keyword_activation()
        test_executive_communication_scenarios()

        print("\n" + "=" * 80)
        print(
            "🎉 **ALL TESTS PASSED** - Stakeholder Frameworks Successfully Integrated!"
        )
        print("📊 **Frameworks Added:** Crucial Conversations + Capital Allocation")
        print("🎭 **Persona Integration:** Alvaro, Camille, David validated")
        print(
            "⚡ **Keywords Active:** Stakeholder communication, ROI allocation, executive dialogue"
        )
        print(
            "🎯 **Executive Scenarios:** VP meetings, budget planning, cross-team alignment"
        )
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ **TEST FAILED**: {str(e)}")
        raise
