#!/usr/bin/env python3
"""
Demo Persona Chat Integration

Test script to demonstrate persona-based chat interface with P2.1 system.
Shows how personas can interact with executive reporting and alerts.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib.claudedirector.persona_integration.persona_bridge import PersonaP2Bridge


def demo_persona_interactions():
    """Demonstrate persona chat interactions."""
    print("🚀 PERSONA CHAT INTEGRATION DEMO")
    print("=" * 50)
    print()

    # Initialize persona bridge
    bridge = PersonaP2Bridge()

    # Demo scenarios
    demo_scenarios = [
        {
            "persona": "diego",
            "request": "Can you give me an executive summary of how the platform teams are doing?",
            "description": "Diego requesting platform engineering status",
        },
        {
            "persona": "camille",
            "request": "What strategic technology issues should I be aware of right now?",
            "description": "Camille asking for strategic alerts",
        },
        {
            "persona": "rachel",
            "request": "How is team health looking from a design systems perspective?",
            "description": "Rachel checking team health with design focus",
        },
        {
            "persona": "alvaro",
            "request": "Any business risks or ROI concerns I should know about?",
            "description": "Alvaro asking for business risk analysis",
        },
        {
            "persona": "martin",
            "request": "What's the current status of our platform architecture and technical health?",
            "description": "Martin requesting technical architecture status",
        },
    ]

    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"📋 SCENARIO {i}: {scenario['description']}")
        print("-" * 60)
        print(f"**User**: @## --persona-{scenario['persona']} {scenario['request']}")
        print()

        # Handle the request
        response = bridge.handle_persona_request(
            scenario["persona"], scenario["request"]
        )

        print(f"**{scenario['persona'].title()}**: {response.response_text}")
        print()

        # Show metadata
        print(
            f"*Confidence: {response.confidence_score:.1%} | "
            f"Data Sources: {', '.join(response.data_sources)} | "
            f"Used P2.1: {response.metadata.get('used_p2_system', False)}*"
        )
        print()

        # Show follow-up suggestions
        if response.follow_up_suggestions:
            print("**Follow-up suggestions:**")
            for suggestion in response.follow_up_suggestions[:2]:
                print(f"• {suggestion}")
            print()

        print("=" * 60)
        print()


def demo_persona_capabilities():
    """Show available persona capabilities."""
    print("👥 AVAILABLE PERSONAS & CAPABILITIES")
    print("=" * 50)
    print()

    bridge = PersonaP2Bridge()
    personas = bridge.get_available_personas()

    for persona in personas:
        print(f"**@## --persona-{persona['name']}**")
        print(f"*{persona['title']}*")
        print(f"Focus: {persona['focus']}")
        print(f"Capabilities: {', '.join(persona['capabilities'])}")
        print()


def demo_quick_status():
    """Demo quick status checks for different personas."""
    print("⚡ QUICK STATUS DEMOS")
    print("=" * 50)
    print()

    bridge = PersonaP2Bridge()

    test_personas = ["diego", "camille", "rachel"]

    for persona in test_personas:
        print(f"📊 Quick status for {persona}:")
        print("-" * 30)

        response = bridge.quick_status_check(persona)
        print(response.response_text)
        print()
        print("=" * 40)
        print()


if __name__ == "__main__":
    print("🎯 ClaudeDirector Persona Chat Integration Demo")
    print("This demonstrates how personas interact with P2.1 Executive Communication")
    print()

    try:
        # Demo 1: Persona capabilities
        demo_persona_capabilities()

        input("Press Enter to continue to interaction demos...")
        print()

        # Demo 2: Persona interactions
        demo_persona_interactions()

        input("Press Enter to continue to quick status demos...")
        print()

        # Demo 3: Quick status checks
        demo_quick_status()

        print("✅ Demo completed successfully!")
        print()
        print("🎯 Next steps:")
        print("• Integration with actual persona framework")
        print("• Enhanced conversation context handling")
        print("• Real-time JIRA data integration")

    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback

        traceback.print_exc()
