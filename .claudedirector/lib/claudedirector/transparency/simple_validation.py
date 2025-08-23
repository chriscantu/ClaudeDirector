#!/usr/bin/env python3
"""
Simple Standalone Validation for ClaudeDirector Transparency System
Tests core components independently
"""

import asyncio
import time


# Test MCP Transparency Components
def test_mcp_transparency():
    """Test MCP transparency functionality"""
    print("🔍 Testing MCP Transparency Components...")

    # Import and test MCPContext and MCPCall
    from mcp_transparency import MCPContext, MCPCall, MCPTransparencyMiddleware

    # Test basic MCP call tracking
    context = MCPContext()
    from datetime import datetime

    call = MCPCall("test_server", "analysis", 0.15, datetime.now(), True)
    context.add_mcp_call(call)

    assert len(context.mcp_calls) == 1
    assert context.has_mcp_calls()
    assert "test_server" in context.get_server_names()
    print("  ✓ MCPContext and MCPCall working")

    # Test middleware
    middleware = MCPTransparencyMiddleware()
    middleware.track_mcp_call(context, "server2", "capability2", 0.05, True)

    assert len(context.mcp_calls) == 2
    print("  ✓ MCPTransparencyMiddleware tracking working")

    # Test response wrapping
    test_response = "Here's my strategic analysis of your market position."
    wrapped = middleware.wrap_persona_response("diego", test_response, context)

    print(f"    DEBUG: Original response: {test_response}")
    print(f"    DEBUG: Wrapped response: {wrapped}")

    assert test_response in wrapped
    assert "MCP" in wrapped or "server" in wrapped.lower() or "🔧" in wrapped
    print("  ✓ Response wrapping with transparency working")

    print("  ✅ MCP Transparency tests passed\n")


def test_framework_detection():
    """Test framework detection functionality"""
    print("🎯 Testing Framework Detection...")

    from framework_detection import FrameworkDetectionMiddleware

    # Test framework detection
    middleware = FrameworkDetectionMiddleware()

    test_text = """
    I recommend using the OGSM strategic framework to structure our approach.
    We should apply Blue Ocean Strategy principles to identify uncontested market spaces.
    The Design Thinking process will help us understand user needs better.
    Porter's Five Forces analysis reveals the competitive landscape.
    """

    detected_frameworks = middleware.detect_frameworks_used(test_text)

    print(
        f"    DEBUG: Detected frameworks: {[(f.framework_name, f.confidence_score) for f in detected_frameworks]}"
    )

    assert len(detected_frameworks) > 0
    framework_names = [f.framework_name for f in detected_frameworks]

    # Check that key frameworks were detected
    expected_frameworks = [
        "OGSM",
        "Blue Ocean Strategy",
        "Design Thinking",
        "Porter's Five Forces",
    ]
    detected_count = sum(1 for fw in expected_frameworks if fw in framework_names)

    assert (
        detected_count >= 2
    ), f"Expected at least 2 frameworks, detected: {framework_names}"
    print(f"  ✓ Detected {len(detected_frameworks)} frameworks: {framework_names}")

    # Test framework attribution
    enhanced = middleware.add_framework_attribution(
        "camille", test_text, detected_frameworks
    )

    assert test_text in enhanced
    assert "Framework" in enhanced or "methodology" in enhanced
    print("  ✓ Framework attribution working")

    print("  ✅ Framework Detection tests passed\n")


def test_persona_communication_patterns():
    """Test persona-specific communication patterns"""
    print("🎭 Testing Persona Communication Patterns...")

    from mcp_transparency import MCPTransparencyMiddleware, MCPContext, MCPCall

    middleware = MCPTransparencyMiddleware()

    # Test different persona patterns
    personas_to_test = ["diego", "camille", "rachel", "alvaro", "martin"]

    for persona in personas_to_test:
        context = MCPContext()
        from datetime import datetime

        context.add_mcp_call(
            MCPCall(f"{persona}_server", "analysis", 0.1, datetime.now(), True)
        )

        response = f"Test response from {persona}"
        enhanced = middleware.wrap_persona_response(persona, response, context)

        # Verify persona-specific elements are present
        assert response in enhanced
        assert (
            "🔧" in enhanced
            or "MCP" in enhanced.lower()
            or "server" in enhanced.lower()
        )

        print(f"  ✓ {persona.title()} communication pattern working")

    print("  ✅ Persona Communication Pattern tests passed\n")


def test_performance_characteristics():
    """Test system performance characteristics"""
    print("⚡ Testing Performance Characteristics...")

    from mcp_transparency import MCPTransparencyMiddleware, MCPContext, MCPCall
    from framework_detection import FrameworkDetectionMiddleware

    # Performance test for MCP tracking
    start_time = time.time()

    mcp_middleware = MCPTransparencyMiddleware()

    from datetime import datetime

    for i in range(100):
        context = MCPContext()
        context.add_mcp_call(MCPCall(f"server_{i}", "test", 0.01, datetime.now(), True))
        mcp_middleware.wrap_persona_response("diego", f"Response {i}", context)

    mcp_time = time.time() - start_time
    assert mcp_time < 1.0, f"MCP processing took too long: {mcp_time:.3f}s"
    print(f"  ✓ MCP transparency processing: {mcp_time:.3f}s for 100 operations")

    # Performance test for framework detection
    start_time = time.time()

    framework_middleware = FrameworkDetectionMiddleware()
    test_text = "Using OGSM framework with Blue Ocean Strategy and Design Thinking."

    for i in range(50):
        frameworks = framework_middleware.detect_frameworks_used(test_text)
        framework_middleware.add_framework_attribution("test", test_text, frameworks)

    framework_time = time.time() - start_time
    assert (
        framework_time < 2.0
    ), f"Framework detection took too long: {framework_time:.3f}s"
    print(
        f"  ✓ Framework detection processing: {framework_time:.3f}s for 50 operations"
    )

    print("  ✅ Performance tests passed\n")


async def test_integration_scenario():
    """Test a realistic integration scenario"""
    print("🚀 Testing Integration Scenario...")

    from mcp_transparency import MCPTransparencyMiddleware, MCPContext, MCPCall
    from framework_detection import FrameworkDetectionMiddleware

    # Simulate a comprehensive persona response scenario
    start_time = time.time()

    # Step 1: Create MCP context and track calls
    mcp_context = MCPContext()
    mcp_middleware = MCPTransparencyMiddleware()

    # Simulate multiple MCP calls
    mcp_calls = [
        ("market_analysis", "competitive_intel", 0.15),
        ("strategic_research", "industry_trends", 0.08),
        ("financial_modeling", "revenue_projection", 0.12),
    ]

    from datetime import datetime

    for server, capability, duration in mcp_calls:
        mcp_context.add_mcp_call(
            MCPCall(server, capability, duration, datetime.now(), True)
        )

    # Step 2: Generate base response with strategic frameworks
    base_response = """
    Strategic Analysis - Market Positioning Recommendation

    Based on comprehensive market intelligence, I recommend the following approach:

    Using the OGSM strategic framework:
    - Objective: Capture 15% market share in the AI SaaS segment
    - Goals: Launch 3 product variants, establish partnerships, achieve $10M ARR
    - Strategy: Blue Ocean approach focusing on uncontested market spaces
    - Measures: Customer acquisition, revenue growth, market penetration

    The Design Thinking methodology guides our user-centric approach:
    1. Empathize with target customer segments
    2. Define core problems and opportunities
    3. Ideate innovative solutions
    4. Prototype minimum viable products
    5. Test and iterate based on feedback

    Porter's Five Forces analysis reveals favorable competitive dynamics,
    while BCG Matrix positioning suggests investing in question mark products
    to develop them into stars.
    """

    # Step 3: Apply MCP transparency
    mcp_enhanced = mcp_middleware.wrap_persona_response(
        "diego", base_response, mcp_context
    )

    # Step 4: Apply framework detection and attribution
    framework_middleware = FrameworkDetectionMiddleware()
    detected_frameworks = framework_middleware.detect_frameworks_used(mcp_enhanced)

    final_response = framework_middleware.add_framework_attribution(
        "diego", mcp_enhanced, detected_frameworks
    )

    processing_time = time.time() - start_time

    # Validate the integrated response
    assert base_response in final_response
    assert (
        len(detected_frameworks) >= 4
    )  # OGSM, Blue Ocean, Design Thinking, Porter's, BCG
    assert len(mcp_context.mcp_calls) == 3
    assert "market_analysis" in mcp_context.get_server_names()

    framework_names = [f.framework_name for f in detected_frameworks]
    expected_frameworks = [
        "OGSM",
        "Blue Ocean",
        "Design Thinking",
        "Porter's Five Forces",
        "BCG Matrix",
    ]
    detected_expected = [
        fw
        for fw in expected_frameworks
        if any(fw in fname for fname in framework_names)
    ]

    print(f"  ✓ Integration test completed in {processing_time:.3f}s")
    print(f"    - MCP calls tracked: {len(mcp_context.mcp_calls)}")
    print(f"    - MCP servers used: {', '.join(mcp_context.get_server_names())}")
    print(f"    - Frameworks detected: {len(detected_frameworks)}")
    print(f"    - Expected frameworks found: {detected_expected}")

    # Performance validation
    assert processing_time < 0.5, f"Integration took too long: {processing_time:.3f}s"
    assert len(final_response) > len(base_response), "Response should be enhanced"

    print("  ✅ Integration scenario test passed\n")


async def main():
    """Main validation function"""
    print("🌟 ClaudeDirector Transparency System - Simple Validation")
    print("=" * 65)

    start_time = time.time()

    try:
        # Run component tests
        test_mcp_transparency()
        test_framework_detection()
        test_persona_communication_patterns()
        test_performance_characteristics()
        await test_integration_scenario()

        total_time = time.time() - start_time

        print("🎉 ALL VALIDATION TESTS PASSED!")
        print(f"⏱️  Total validation time: {total_time:.3f}s")
        print("\n✅ Core transparency system components are working correctly")
        print("✅ Ready for integration with ClaudeDirector persona system")

        return True

    except AssertionError as e:
        print(f"❌ Validation assertion failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    print(
        f"\n{'🚀 SUCCESS' if success else '💥 FAILURE'}: Transparency system validation {'completed' if success else 'failed'}"
    )
    exit(0 if success else 1)
