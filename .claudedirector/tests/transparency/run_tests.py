"""
Simple test runner for transparency integration
No external dependencies required
"""

import sys
import time
from pathlib import Path

# Add paths for imports
lib_path = Path(__file__).parent.parent.parent / "lib"
integration_path = Path(__file__).parent.parent.parent / "integration-protection"
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(integration_path))

from cursor_transparency_bridge import (
    CursorTransparencyBridge,
    ensure_transparency_compliance,
    get_transparency_summary,
)


def test_persona_detection():
    """Test persona detection from context"""
    print("🧪 Testing Persona Detection...")

    bridge = CursorTransparencyBridge()

    test_cases = [
        ("How should we architect our platform for scale?", "martin"),
        ("What's our team structure strategy?", "diego"),
        ("ROI analysis for platform investment", "alvaro"),
        ("Design system component strategy", "rachel"),
        ("Strategic technology assessment", "camille"),
    ]

    passed = 0
    for user_input, expected_persona in test_cases:
        persona = bridge.detect_persona_from_context(user_input)
        if persona == expected_persona:
            print(f"  ✅ '{user_input[:30]}...' → {persona}")
            passed += 1
        else:
            print(
                f"  ❌ '{user_input[:30]}...' → {persona} (expected {expected_persona})"
            )

    print(f"  📊 Persona Detection: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


def test_persona_headers():
    """Test persona header application"""
    print("\n🧪 Testing Persona Headers...")

    bridge = CursorTransparencyBridge()

    test_cases = [
        ("martin", "🏗️ Martin | Platform Architecture"),
        ("diego", "🎯 Diego | Engineering Leadership"),
        ("alvaro", "💼 Alvaro | Platform Investment Strategy"),
        ("rachel", "🎨 Rachel | Design Systems Strategy"),
    ]

    passed = 0
    for persona, expected_header in test_cases:
        response = "Here's the analysis..."
        enhanced = bridge.add_persona_header(response, persona)

        if enhanced.startswith(expected_header):
            print(f"  ✅ {persona} → {expected_header}")
            passed += 1
        else:
            print(f"  ❌ {persona} → Missing header")

    # Test header detection
    response_with_header = "🏗️ Martin | Platform Architecture\n\nContent..."
    has_header = bridge.has_persona_header(response_with_header)
    if has_header:
        print("  ✅ Header detection working")
        passed += 1
    else:
        print("  ❌ Header detection failed")

    print(f"  📊 Header Tests: {passed}/{len(test_cases) + 1} passed")
    return passed == len(test_cases) + 1


def test_transparency_compliance():
    """Test complete transparency compliance"""
    print("\n🧪 Testing Transparency Compliance...")

    test_scenarios = [
        {
            "input": "Platform architecture scalability concerns",
            "response": "Here's a systematic approach...",
            "expected_persona": "martin",
            "expected_header": "🏗️ Martin | Platform Architecture",
        },
        {
            "input": "Team coordination strategy",
            "response": "Team structure considerations...",
            "expected_persona": "diego",
            "expected_header": "🎯 Diego | Engineering Leadership",
        },
        {
            "input": "Business value ROI analysis",
            "response": "Investment analysis shows...",
            "expected_persona": "alvaro",
            "expected_header": "💼 Alvaro | Platform Investment Strategy",
        },
    ]

    passed = 0
    for scenario in test_scenarios:
        enhanced = ensure_transparency_compliance(
            scenario["response"], scenario["input"]
        )

        if scenario["expected_header"] in enhanced:
            print(f"  ✅ {scenario['expected_persona']}: {scenario['input'][:30]}...")
            passed += 1
        else:
            print(f"  ❌ {scenario['expected_persona']}: Missing header")

    print(f"  📊 Compliance Tests: {passed}/{len(test_scenarios)} passed")
    return passed == len(test_scenarios)


def test_transparency_summary():
    """Test transparency summary generation"""
    print("\n🧪 Testing Transparency Summary...")

    user_input = "Architecture design patterns for microservices"
    response = "Microservices require careful design..."

    enhanced = ensure_transparency_compliance(response, user_input)
    summary = get_transparency_summary(enhanced, user_input)

    checks = [
        ("persona_detected", lambda: summary["persona_detected"] == "martin"),
        ("has_persona_header", lambda: summary["has_persona_header"] == True),
        ("transparency_applied", lambda: summary["transparency_applied"] == True),
    ]

    passed = 0
    for check_name, check_func in checks:
        if check_func():
            print(f"  ✅ {check_name}: {summary[check_name]}")
            passed += 1
        else:
            print(f"  ❌ {check_name}: {summary[check_name]}")

    print(f"  📊 Summary Tests: {passed}/{len(checks)} passed")
    return passed == len(checks)


def test_error_handling():
    """Test error handling and edge cases"""
    print("\n🧪 Testing Error Handling...")

    test_cases = [
        ("", "Empty input"),
        ("   ", "Whitespace only"),
        ("x" * 1000, "Very long input"),
    ]

    passed = 0
    for test_input, description in test_cases:
        try:
            enhanced = ensure_transparency_compliance("Response", test_input)
            # Should have some persona header
            has_header = any(
                header in enhanced
                for header in [
                    "🏗️ Martin",
                    "🎯 Diego",
                    "💼 Alvaro",
                    "🎨 Rachel",
                    "📊 Camille",
                ]
            )
            if has_header:
                print(f"  ✅ {description}: Handled gracefully")
                passed += 1
            else:
                print(f"  ❌ {description}: No persona header added")
        except Exception as e:
            print(f"  ❌ {description}: Exception: {e}")

    print(f"  📊 Error Handling: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


def test_performance():
    """Test performance characteristics"""
    print("\n🧪 Testing Performance...")

    user_input = "Architecture scalability platform microservices design patterns"
    response = "Here's a comprehensive analysis of platform architecture..."

    # Test multiple iterations to check for consistency and performance
    times = []
    for i in range(10):
        start_time = time.time()
        ensure_transparency_compliance(response, user_input)
        end_time = time.time()
        times.append(end_time - start_time)

    avg_time = sum(times) / len(times)
    max_time = max(times)

    # Performance targets
    performance_ok = max_time < 0.01  # <10ms max
    consistency_ok = all(
        "🏗️ Martin | Platform Architecture"
        in ensure_transparency_compliance(response, user_input)
        for _ in range(5)
    )

    if performance_ok:
        print(f"  ✅ Performance: {avg_time*1000:.2f}ms avg, {max_time*1000:.2f}ms max")
    else:
        print(
            f"  ⚠️ Performance: {avg_time*1000:.2f}ms avg, {max_time*1000:.2f}ms max (target <10ms)"
        )

    if consistency_ok:
        print("  ✅ Consistency: Deterministic results")
    else:
        print("  ❌ Consistency: Non-deterministic results")

    passed = (1 if performance_ok else 0) + (1 if consistency_ok else 0)
    print(f"  📊 Performance Tests: {passed}/2 passed")
    return passed == 2


def run_all_tests():
    """Run all transparency integration tests"""
    print("🚀 ClaudeDirector Transparency Integration Test Suite")
    print("=" * 60)

    tests = [
        ("Persona Detection", test_persona_detection),
        ("Persona Headers", test_persona_headers),
        ("Transparency Compliance", test_transparency_compliance),
        ("Transparency Summary", test_transparency_summary),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name}: Exception occurred: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed_tests = 0
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {test_name}")
        if passed:
            passed_tests += 1

    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100

    print(
        f"\n📈 Overall Results: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
    )

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Review before proceeding.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
