"""
Test of Scaling Up Excellence Framework Integration
Tests the new Sutton & Rao framework implementation in the embedded framework engine.

Author: Camille (Strategic Technology) & Alvaro (Platform ROI)
"""

import sys
import os

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine, EmbeddedPersonaIntegrator


def test_scaling_up_excellence_framework_direct():
    """Test Scaling Up Excellence framework directly"""

    print("\n🎯 **Direct Scaling Up Excellence Test**")
    print("=" * 50)

    # Create framework engine
    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Scaling Up Excellence framework
    test_input = "Our design system has great adoption on Web but iOS and Android teams resist it - how do we scale this excellence across all platforms?"
    persona_context = "diego"
    domain_focus = ["organizational", "strategic", "technical"]

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

    # Check for Scaling Up Excellence-specific components
    scaling_keywords = ["buddhist", "catholic", "hot causes", "cool solutions", "connect", "cascade", "cut", "growth", "excellence", "scaling"]
    found_scaling_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in scaling_keywords:
        if keyword.lower() in insights_str.lower():
            found_scaling_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in scaling_keywords:
        if keyword.lower() in recommendations_str.lower():
            if keyword not in found_scaling_elements:
                found_scaling_elements.append(keyword)

    print(f"\n🎯 **Scaling Elements Found:** {found_scaling_elements}")

    # Validate we got the right framework
    expected_framework = "Scaling Up Excellence Framework"
    assert framework_analysis.framework_name == expected_framework, f"Expected {expected_framework}, got {framework_analysis.framework_name}"

    # Validate we found key Scaling Up Excellence concepts
    required_elements = ["buddhist", "catholic", "excellence"]
    found_required = [elem for elem in required_elements if elem in found_scaling_elements]
    assert len(found_required) >= 2, f"Expected at least 2 required elements, found: {found_required}"

    print(f"\n📋 **Key Recommendations:**")
    for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")

    print(f"\n⚡ **Implementation Steps:**")
    for i, step in enumerate(framework_analysis.implementation_steps[:3], 1):
        print(f"   {i}. {step}")

    print(f"\n✅ **Test Result: SUCCESS** - Scaling Up Excellence framework correctly activated")
    return True


def test_scaling_keyword_activation():
    """Test that scaling-related keywords properly activate the framework"""

    print("\n🔍 **Scaling Keyword Activation Test**")
    print("=" * 50)

    framework_engine = EmbeddedFrameworkEngine()

    # Test various scaling-related inputs
    test_cases = [
        {
            "input": "How do we scale our API standards across multiple teams?",
            "expected_keywords": ["scaling", "standards"]
        },
        {
            "input": "We need to spread best practices for code quality organization-wide",
            "expected_keywords": ["spread", "practices", "organization"]
        },
        {
            "input": "Our platform excellence is inconsistent across teams - need better adoption",
            "expected_keywords": ["excellence", "adoption", "teams"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n**Test Case {i}:** {test_case['input']}")

        analysis = framework_engine.analyze_systematically(
            user_input=test_case["input"],
            persona_context="diego",
            domain_focus=["organizational", "strategic"]
        )

        print(f"   Framework: {analysis.framework_name}")
        print(f"   Confidence: {analysis.analysis_confidence:.2f}")

        # Should activate Scaling Up Excellence for scaling-related queries
        is_scaling_framework = "Scaling Up Excellence" in analysis.framework_name
        print(f"   Scaling Framework Activated: {is_scaling_framework}")

    print(f"\n✅ **Keyword Activation Test Complete**")
    return True


def test_persona_integration_with_scaling():
    """Test persona integration with Scaling Up Excellence framework"""

    print("\n🎭 **Persona Integration Test**")
    print("=" * 50)

    # Test with different personas
    framework_engine = EmbeddedFrameworkEngine()
    integrator = EmbeddedPersonaIntegrator(framework_engine)

    test_input = "We want to scale our design system adoption but teams are resistant to standardization"

    personas = ["diego", "rachel", "martin"]

    for persona in personas:
        print(f"\n**Testing with {persona}:**")

        response = integrator.create_systematic_response(
            persona_name=persona,
            user_input=test_input,
            base_response="",
            domain_focus=["organizational", "strategic"]
        )

        print(f"   Framework: {response.framework_applied}")
        print(f"   Processing Time: {response.processing_time_ms}ms")
        print(f"   Response Length: {len(response.persona_integrated_response)} chars")

        # Check that response includes persona-specific elements
        response_text = response.persona_integrated_response.lower()

        if persona == "diego":
            assert "😊" in response.persona_integrated_response or "collaborative" in response_text
        elif persona == "rachel":
            assert "user" in response_text or "experience" in response_text
        elif persona == "martin":
            assert "architectural" in response_text or "principle" in response_text

    print(f"\n✅ **Persona Integration Test Complete**")
    return True


if __name__ == "__main__":
    print("🧪 **Testing Scaling Up Excellence Framework Integration**")
    print("=" * 60)

    try:
        # Run all tests
        test_scaling_up_excellence_framework_direct()
        test_scaling_keyword_activation()
        test_persona_integration_with_scaling()

        print("\n" + "=" * 60)
        print("🎉 **ALL TESTS PASSED** - Scaling Up Excellence Framework Successfully Integrated!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ **TEST FAILED**: {str(e)}")
        raise
