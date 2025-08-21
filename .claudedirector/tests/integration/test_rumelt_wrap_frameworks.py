"""
Direct Test of Rumelt and WRAP Frameworks
Tests the embedded framework engine directly to validate framework integration.

Author: Martin (Principal Platform Architect)
"""

import sys
import os

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../lib"))

from claudedirector.core.embedded_framework_engine import (
    EmbeddedFrameworkEngine,
    EmbeddedPersonaIntegrator,
)


def test_rumelt_framework_direct():
    """Test Rumelt Strategy Kernel framework directly"""

    print("\n🎯 **Direct Rumelt Strategy Kernel Test**")
    print("=" * 50)

    # Create framework engine
    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger Rumelt framework
    test_input = "Our strategy feels like fluff - help me create a real strategy that addresses our core engineering challenges"
    persona_context = "diego"
    domain_focus = ["strategic", "organizational"]

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

    # Check for Rumelt-specific components
    rumelt_keywords = [
        "diagnosis",
        "policy",
        "action",
        "challenge",
        "leverage",
        "fluff",
        "coherent",
    ]
    found_rumelt_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in rumelt_keywords:
        if keyword.lower() in insights_str.lower():
            found_rumelt_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in rumelt_keywords:
        if keyword.lower() in recommendations_str.lower():
            found_rumelt_elements.append(keyword)

    found_rumelt_elements = list(set(found_rumelt_elements))  # Remove duplicates

    print(
        f"   Rumelt Elements Found: {len(found_rumelt_elements)}/{len(rumelt_keywords)}"
    )
    print(f"   Elements: {', '.join(found_rumelt_elements)}")

    # Show some recommendations
    if framework_analysis.recommendations:
        print(f"\n📋 **Sample Recommendations:**")
        for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
            print(f"   {i}. {rec}")

    # Evaluate success
    if (
        "Rumelt" in framework_analysis.framework_name
        and len(found_rumelt_elements) >= 3
    ):
        print(f"\n✅ **SUCCESS: Rumelt framework properly applied**")
        return True
    else:
        print(f"\n❌ **ISSUE: Framework or content may need adjustment**")
        return False


def test_wrap_framework_direct():
    """Test WRAP Decision framework directly"""

    print("\n🎯 **Direct WRAP Decision Framework Test**")
    print("=" * 50)

    # Create framework engine
    framework_engine = EmbeddedFrameworkEngine()

    # Test input that should trigger WRAP framework
    test_input = "We need to decide between microservices vs monolith architecture - what's the best approach?"
    persona_context = "martin"
    domain_focus = ["technical", "strategic"]

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

    # Check for WRAP-specific components
    wrap_keywords = [
        "widen",
        "reality",
        "distance",
        "prepare",
        "options",
        "assumptions",
        "evidence",
        "test",
    ]
    found_wrap_elements = []

    # Check in structured insights
    insights_str = str(framework_analysis.structured_insights)
    for keyword in wrap_keywords:
        if keyword.lower() in insights_str.lower():
            found_wrap_elements.append(keyword)

    # Check in recommendations
    recommendations_str = " ".join(framework_analysis.recommendations)
    for keyword in wrap_keywords:
        if keyword.lower() in recommendations_str.lower():
            found_wrap_elements.append(keyword)

    found_wrap_elements = list(set(found_wrap_elements))  # Remove duplicates

    print(f"   WRAP Elements Found: {len(found_wrap_elements)}/{len(wrap_keywords)}")
    print(f"   Elements: {', '.join(found_wrap_elements)}")

    # Show some recommendations
    if framework_analysis.recommendations:
        print(f"\n📋 **Sample Recommendations:**")
        for i, rec in enumerate(framework_analysis.recommendations[:3], 1):
            print(f"   {i}. {rec}")

    # Evaluate success
    if "WRAP" in framework_analysis.framework_name and len(found_wrap_elements) >= 3:
        print(f"\n✅ **SUCCESS: WRAP framework properly applied**")
        return True
    else:
        print(f"\n❌ **ISSUE: Framework or content may need adjustment**")
        return False


def test_persona_integration():
    """Test persona integration with new frameworks"""

    print("\n🎭 **Persona Integration Test**")
    print("=" * 40)

    # Create framework engine and persona integrator
    framework_engine = EmbeddedFrameworkEngine()
    persona_integrator = EmbeddedPersonaIntegrator(framework_engine)

    # Test Rumelt with Diego
    test_input = "Our current platform strategy feels like fluff - help me create a real strategy"
    base_response = "Let me help you think through your platform strategy challenges."

    print(f"📝 **Test Input:** {test_input}")
    print(f"👤 **Persona:** diego")

    # Create systematic response
    systematic_response = persona_integrator.create_systematic_response(
        persona_name="diego",
        user_input=test_input,
        base_response=base_response,
        domain_focus=["strategic"],
    )

    print(f"\n✅ **Integration Results:**")
    print(f"   Framework Used: {systematic_response.framework_applied}")
    print(f"   Processing Time: {systematic_response.processing_time_ms}ms")

    # Check for Diego's personality in the response
    diego_markers = [
        "😊",
        "excited",
        "systematic",
        "collaborate",
        "resonates",
        "thoughts",
    ]
    response_lower = systematic_response.persona_integrated_response.lower()
    found_diego_markers = [
        marker for marker in diego_markers if marker.lower() in response_lower
    ]

    print(
        f"   Diego Personality Markers: {len(found_diego_markers)}/{len(diego_markers)}"
    )
    print(f"   Found: {', '.join(found_diego_markers)}")

    # Show response preview
    response_preview = (
        systematic_response.persona_integrated_response[:300] + "..."
        if len(systematic_response.persona_integrated_response) > 300
        else systematic_response.persona_integrated_response
    )
    print(f"\n📋 **Response Preview:**")
    print(f"   {response_preview}")

    return len(found_diego_markers) >= 2  # At least 2 personality markers


def run_framework_validation():
    """Run complete framework validation"""

    print("📚 **Rumelt & WRAP Framework Validation**")
    print("=" * 60)
    print("Testing direct framework integration and persona compatibility")
    print("=" * 60)

    results = {"rumelt_test": False, "wrap_test": False, "persona_integration": False}

    try:
        # Test 1: Rumelt Framework
        results["rumelt_test"] = test_rumelt_framework_direct()

        # Test 2: WRAP Framework
        results["wrap_test"] = test_wrap_framework_direct()

        # Test 3: Persona Integration
        results["persona_integration"] = test_persona_integration()

        # Summary
        print("\n" + "=" * 60)
        print("📊 **Validation Summary:**")

        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")

        all_passed = all(results.values())
        if all_passed:
            print(
                "\n🎉 **ALL TESTS PASSED: Rumelt & WRAP frameworks successfully integrated!**"
            )
        else:
            print(f"\n⚠️ **PARTIAL SUCCESS: {sum(results.values())}/3 tests passed**")

        print("=" * 60)
        return all_passed

    except Exception as e:
        print(f"\n❌ **Validation Failed:** {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    """Run validation when executed directly"""
    success = run_framework_validation()
    exit(0 if success else 1)
