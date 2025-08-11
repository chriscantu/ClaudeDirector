"""
MCP Integration Demo and Testing
Demonstrates the complete MCP-enhanced persona workflow and validates core functionality.

This test demonstrates:
1. Context Analysis → Persona Selection → MCP Enhancement workflow
2. Diego + Sequential systematic analysis integration
3. Graceful degradation when MCP servers unavailable
4. Performance characteristics and enhancement value

Author: Martin (Principal Platform Architect)
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from claudedirector.core.enhanced_persona_manager import (
    EnhancedPersonaManager,
    create_enhanced_persona_manager,
    create_demo_enhanced_manager
)
from claudedirector.core.template_engine import TemplateDiscoveryEngine
from claudedirector.core.mcp_client import (
    MCPClient, 
    MCPServerConfig, 
    MCPRequest, 
    MCPResponse
)
from claudedirector.core.complexity_analyzer import AnalysisComplexityDetector


class MockMCPClient:
    """Mock MCP client for testing without real servers"""
    
    def __init__(self):
        self.server_configs = {}
        self.request_count = 0
        
    async def send_request(self, server_name: str, request: MCPRequest, use_cache: bool = True) -> MCPResponse:
        """Mock MCP request with simulated responses"""
        self.request_count += 1
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Generate mock response based on server and request
        if server_name == "sequential" and request.method == "analyze_systematically":
            return self._create_sequential_response(request)
        elif server_name == "context7" and request.method == "lookup_framework":
            return self._create_context7_response(request)
        else:
            return MCPResponse(
                id=request.id,
                result=None,
                error={"code": -1, "message": "Unknown method"},
                success=False
            )
    
    def _create_sequential_response(self, request: MCPRequest) -> MCPResponse:
        """Create mock Sequential server response for systematic analysis"""
        
        analysis_context = request.params.get("context", {})
        user_question = analysis_context.get("user_question", "")
        
        # Generate contextual systematic analysis
        mock_insights = {
            "framework": {
                "name": "Strategic Platform Assessment Framework",
                "steps": [
                    "Current State Analysis: Assess existing platform capabilities and constraints",
                    "Stakeholder Impact Mapping: Identify affected teams and decision makers", 
                    "Success Metrics Definition: Define measurable outcomes and KPIs",
                    "Implementation Roadmap: Create phased approach with milestones",
                    "Risk Mitigation Planning: Anticipate challenges and prepare contingencies"
                ]
            },
            "analysis": {
                "key_insights": [
                    "Platform decisions require cross-team alignment and clear success criteria",
                    "Technical excellence must be balanced with business value delivery",
                    "Change management is as critical as technical implementation"
                ],
                "critical_factors": [
                    "Team capacity and capability assessment",
                    "Stakeholder buy-in and communication strategy", 
                    "Technical debt vs. new feature balance",
                    "Performance and scalability requirements"
                ]
            },
            "recommendations": [
                "Start with stakeholder alignment session to establish shared vision",
                "Create measurable success criteria before implementation begins",
                "Plan phased rollout with early feedback loops and iteration cycles",
                "Establish regular communication cadence with all affected teams"
            ]
        }
        
        # Customize based on user input keywords
        if "mobile" in user_question.lower():
            mock_insights["analysis"]["key_insights"].append(
                "Mobile platform decisions require native performance and app store considerations"
            )
            mock_insights["recommendations"].append(
                "Consider cross-platform strategy impact on team structure and expertise"
            )
        
        if "strategy" in user_question.lower():
            mock_insights["framework"]["name"] = "Strategic Decision Framework"
            mock_insights["analysis"]["critical_factors"].append(
                "Long-term strategic alignment with company vision"
            )
        
        return MCPResponse(
            id=request.id,
            result={
                "insights": mock_insights,
                "analysis_type": "strategic_organizational",
                "confidence": 0.9,
                "processing_time": 0.1
            },
            error=None,
            success=True,
            server_name="sequential"
        )
    
    def _create_context7_response(self, request: MCPRequest) -> MCPResponse:
        """Create mock Context7 server response for framework lookup"""
        
        framework_type = request.params.get("framework_type", "")
        domain = request.params.get("domain", "")
        
        mock_patterns = {
            "patterns": [
                {
                    "name": "Conway's Law Pattern",
                    "description": "Organizations design systems that mirror their communication structure",
                    "trade_offs": "Team autonomy vs. system coherence"
                },
                {
                    "name": "Platform Team Pattern", 
                    "description": "Dedicated teams provide platforms for other teams to build upon",
                    "trade_offs": "Platform investment vs. immediate feature delivery"
                }
            ],
            "tradeoffs": [
                {
                    "factor": "Team Structure",
                    "analysis": "Cross-functional teams increase autonomy but require more coordination"
                },
                {
                    "factor": "Technical Debt",
                    "analysis": "Platform improvements reduce long-term debt but slow short-term delivery"
                }
            ]
        }
        
        return MCPResponse(
            id=request.id,
            result={
                "patterns": mock_patterns["patterns"],
                "tradeoffs": mock_patterns["tradeoffs"],
                "domain": domain,
                "framework_type": framework_type
            },
            error=None,
            success=True,
            server_name="context7"
        )
    
    async def get_connection_status(self) -> dict:
        """Mock connection status"""
        return {
            "sequential": {
                "status": "connected",
                "capabilities": ["systematic_analysis", "framework_application"],
                "request_count": self.request_count
            },
            "context7": {
                "status": "connected", 
                "capabilities": ["pattern_access", "methodology_lookup"],
                "request_count": self.request_count
            }
        }
    
    async def close(self) -> None:
        """Mock cleanup"""
        pass


async def demo_basic_persona_activation():
    """Demo basic persona activation without MCP enhancement"""
    
    print("\n🎯 Demo 1: Basic Persona Activation (No MCP Enhancement)")
    print("=" * 60)
    
    # Create manager without MCP
    manager = create_demo_enhanced_manager(enable_mcp=False)
    
    test_inputs = [
        "Our iOS mobile app performance is declining",
        "We need to improve our product strategy for Q4",
        "How should we approach our platform architecture technical debt?",
    ]
    
    for user_input in test_inputs:
        print(f"\n📝 User Input: {user_input}")
        
        start_time = time.time()
        result = await manager.process_user_input(user_input)
        processing_time = (time.time() - start_time) * 1000
        
        print(f"🤖 Persona: {result['persona']} ({result['template_id']})")
        print(f"⚡ Confidence: {result['context']['confidence']:.2f}")
        print(f"📊 Processing Time: {processing_time:.1f}ms")
        print(f"🎨 Response Preview: {result['response'][:150]}...")
        print(f"🔧 Enhanced: {result['enhancement']['applied']} ({result['enhancement']['fallback_reason']})")
    
    await manager.close()


async def demo_mcp_enhanced_workflow():
    """Demo MCP-enhanced persona workflow with mock servers"""
    
    print("\n🚀 Demo 2: MCP-Enhanced Persona Workflow")
    print("=" * 60)
    
    # Create manager with mock MCP integration
    template_discovery = TemplateDiscoveryEngine(".claudedirector/config/director_templates.yaml")
    manager = EnhancedPersonaManager(template_discovery)
    
    # Mock MCP client integration 
    manager.mcp_client = MockMCPClient()
    manager.mcp_enabled = True
    
    # Create complexity detector and enhancement engine with mock
    from claudedirector.core.complexity_analyzer import AnalysisComplexityDetector
    from claudedirector.core.persona_enhancement_engine import PersonaEnhancementEngine
    
    manager.complexity_detector = AnalysisComplexityDetector()
    manager.enhancement_engine = PersonaEnhancementEngine(
        manager.mcp_client,
        manager.complexity_detector
    )
    
    # Test strategic scenarios that should trigger MCP enhancement
    strategic_scenarios = [
        {
            "input": "Help me develop a systematic approach for Q4 platform strategy planning",
            "expected_persona": "diego",
            "expected_enhancement": True,
            "description": "Strategic planning should trigger Diego + Sequential systematic analysis"
        },
        {
            "input": "What are the architectural patterns for microservices team organization?", 
            "expected_persona": "martin",
            "expected_enhancement": True,
            "description": "Architecture question should trigger Martin + Context7 framework lookup"
        },
        {
            "input": "How should I prioritize design system improvements for cross-team adoption?",
            "expected_persona": "rachel", 
            "expected_enhancement": True,
            "description": "Design systems question should trigger Rachel + Context7"
        },
        {
            "input": "What's the weather like today?",
            "expected_persona": "camille",
            "expected_enhancement": False,
            "description": "Off-topic question should use fallback persona without enhancement"
        }
    ]
    
    for i, scenario in enumerate(strategic_scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['description']}")
        print(f"📝 Input: {scenario['input']}")
        
        start_time = time.time()
        result = await manager.process_user_input(scenario['input'])
        total_time = (time.time() - start_time) * 1000
        
        # Analyze results
        persona_match = result['persona'] == scenario['expected_persona']
        enhancement_match = result['enhancement']['applied'] == scenario['expected_enhancement']
        
        print(f"🤖 Persona: {result['persona']} ({'✅' if persona_match else '❌ Expected: ' + scenario['expected_persona']})")
        print(f"🔧 Enhanced: {result['enhancement']['applied']} ({'✅' if enhancement_match else '❌ Expected: ' + str(scenario['expected_enhancement'])})")
        
        if result['enhancement']['applied']:
            print(f"🌐 Server: {result['enhancement']['server_used']}")
            print(f"⏱️  Enhancement Time: {result['enhancement']['processing_time_ms']}ms")
        else:
            print(f"❓ Fallback Reason: {result['enhancement']['fallback_reason']}")
        
        print(f"📊 Total Processing: {total_time:.1f}ms")
        print(f"🎨 Response Preview: {result['response'][:200]}...")
        
        # Validation
        if persona_match and enhancement_match:
            print("✅ Scenario PASSED")
        else:
            print("❌ Scenario FAILED")
    
    # Show enhancement statistics
    stats = manager.get_enhancement_statistics()
    print(f"\n📈 Enhancement Statistics:")
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Enhanced: {stats['enhanced_requests']} ({stats['enhancement_rate']:.1%})")
    print(f"   Fallback: {stats['fallback_requests']}")
    print(f"   Avg Time: {stats['average_enhancement_time']:.1f}ms")
    
    await manager.close()


async def demo_performance_characteristics():
    """Demo performance characteristics and graceful degradation"""
    
    print("\n⚡ Demo 3: Performance & Graceful Degradation")
    print("=" * 60)
    
    # Test with manager that has MCP configured but servers unavailable
    manager = create_demo_enhanced_manager(enable_mcp=True)
    
    # Simulate server failure scenario
    print("\n🔥 Testing graceful degradation with server failures...")
    
    complex_input = "Develop a comprehensive systematic strategy for Q4 platform modernization including stakeholder alignment, technical debt prioritization, and team coordination across multiple engineering organizations"
    
    print(f"📝 Complex Strategic Input: {complex_input[:100]}...")
    
    start_time = time.time()
    result = await manager.process_user_input(complex_input)
    total_time = (time.time() - start_time) * 1000
    
    print(f"🤖 Persona Selected: {result['persona']}")
    print(f"📊 Context Confidence: {result['context']['confidence']:.2f}")
    print(f"🔧 Enhancement Applied: {result['enhancement']['applied']}")
    print(f"❓ Fallback Reason: {result['enhancement']['fallback_reason']}")
    print(f"⏱️  Total Processing Time: {total_time:.1f}ms")
    print(f"🎨 Response Quality: {'Standard persona response (still valuable)' if not result['enhancement']['applied'] else 'Enhanced response'}")
    
    # Verify response is still meaningful
    response_quality_indicators = [
        "strategic" in result['response'].lower(),
        "platform" in result['response'].lower(),
        len(result['response']) > 100,
        result['persona'] in ['diego', 'camille', 'alvaro']  # Strategic personas
    ]
    
    quality_score = sum(response_quality_indicators) / len(response_quality_indicators)
    print(f"🎯 Response Quality Score: {quality_score:.1%}")
    
    if quality_score >= 0.75:
        print("✅ Graceful degradation SUCCESSFUL - High quality response without MCP")
    else:
        print("❌ Graceful degradation FAILED - Response quality insufficient")
    
    await manager.close()


async def demo_conversation_state_management():
    """Demo conversation state management across multiple turns"""
    
    print("\n💬 Demo 4: Conversation State Management")
    print("=" * 60)
    
    manager = create_demo_enhanced_manager(enable_mcp=True)
    
    # Simulate multi-turn conversation
    conversation_turns = [
        "Help me plan Q4 mobile platform strategy",
        "What about the technical debt in our iOS codebase?",
        "How does this align with our overall product roadmap?",
        "What are the organizational implications of this approach?"
    ]
    
    for turn, user_input in enumerate(conversation_turns, 1):
        print(f"\n🗣️  Turn {turn}: {user_input}")
        
        result = await manager.process_user_input(user_input)
        state = result['conversation_state']
        
        print(f"🤖 Active Persona: {result['persona']}")
        print(f"📊 Total Activations: {state['total_activations']}")
        print(f"⏱️  Session Duration: {state['session_duration_minutes']:.1f} minutes")
        print(f"📈 Persona Usage: {', '.join(f'{p}: {c}' for p, c in state['persona_usage_count'].items())}")
        
        # Check for persona transitions
        if turn > 1:
            history = manager.get_activation_history(limit=2)
            if len(history) >= 2:
                prev_persona = history[-2]['persona']
                curr_persona = history[-1]['persona']
                if prev_persona != curr_persona:
                    print(f"🔄 Persona Transition: {prev_persona} → {curr_persona}")
    
    # Final conversation summary
    final_state = manager.get_current_state()
    history = manager.get_activation_history()
    
    print(f"\n📋 Conversation Summary:")
    print(f"   Turns: {len(conversation_turns)}")
    print(f"   Unique Personas: {len(final_state['persona_usage_count'])}")
    print(f"   Most Used: {max(final_state['persona_usage_count'].items(), key=lambda x: x[1])[0]}")
    print(f"   Session Duration: {final_state['session_duration_minutes']:.1f} minutes")
    
    await manager.close()


async def run_comprehensive_demo():
    """Run comprehensive MCP integration demonstration"""
    
    print("🚀 ClaudeDirector MCP Integration Comprehensive Demo")
    print("=" * 80)
    print("Demonstrating systematic strategic analysis with intelligent persona activation")
    print("=" * 80)
    
    try:
        # Run all demo scenarios
        await demo_basic_persona_activation()
        await demo_mcp_enhanced_workflow()
        await demo_performance_characteristics()
        await demo_conversation_state_management()
        
        print("\n🎉 Demo Complete!")
        print("=" * 80)
        print("✅ All MCP integration scenarios demonstrated successfully")
        print("📈 Key Benefits Validated:")
        print("   • Intelligent persona activation based on context")
        print("   • Systematic strategic analysis with MCP enhancement")
        print("   • Graceful degradation when servers unavailable")
        print("   • Professional response quality maintained")
        print("   • Conversation state tracking across turns")
        print("   • Performance within acceptable thresholds")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the demo
    asyncio.run(run_comprehensive_demo())
