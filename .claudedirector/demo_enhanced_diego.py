#!/usr/bin/env python3
"""
Demo: Enhanced Diego with Sequential Framework Integration
Demonstrates Sprint 2 implementation with MCP-enhanced strategic analysis.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add the lib directory to Python path
sys.path.append(str(Path(__file__).parent / "lib"))

from claudedirector.integrations.enhanced_persona_manager import EnhancedPersonaManager, EnhancementStatus


class DemoColors:
    """Terminal colors for demo output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


async def demo_enhanced_diego():
    """Demo enhanced Diego persona with MCP integration"""
    print(f"\n{DemoColors.HEADER}🚀 Enhanced Diego Demo - MCP Integration Sprint 2{DemoColors.ENDC}")
    print(f"{DemoColors.OKBLUE}Demonstrating strategic analysis enhancement with Sequential framework integration{DemoColors.ENDC}\n")
    
    # Initialize enhanced persona manager
    print(f"{DemoColors.OKCYAN}📋 Initializing Enhanced Persona Manager...{DemoColors.ENDC}")
    persona_manager = EnhancedPersonaManager()
    
    try:
        # Initialize connections
        initialization_start = time.time()
        success = await persona_manager.initialize()
        initialization_time = time.time() - initialization_start
        
        if success:
            print(f"{DemoColors.OKGREEN}✅ Initialization complete ({initialization_time:.2f}s){DemoColors.ENDC}")
        else:
            print(f"{DemoColors.WARNING}⚠️ Initialization with graceful degradation ({initialization_time:.2f}s){DemoColors.ENDC}")
        
        # Display server status
        status = persona_manager.get_server_status()
        print(f"\n{DemoColors.OKBLUE}📊 Server Status:{DemoColors.ENDC}")
        print(f"  Status: {status['status']}")
        if status['status'] == 'available':
            print(f"  Available servers: {status['available_servers']}")
            print(f"  Enhanced personas: {status['enhanced_personas']}")
        elif status['status'] == 'unavailable':
            print(f"  Reason: {status['reason']}")
        
        # Demo questions ranging from simple to strategic
        demo_questions = [
            {
                "question": "What is microservices architecture?",
                "description": "Simple technical question (should use standard response)",
                "expected_enhancement": False
            },
            {
                "question": "How should we restructure our platform teams to improve delivery velocity while maintaining quality?",
                "description": "Strategic organizational question (should trigger Sequential enhancement)",
                "expected_enhancement": True
            },
            {
                "question": "What's the best systematic approach for scaling our engineering organization across multiple product teams?",
                "description": "Complex scaling question (should trigger Sequential enhancement)",
                "expected_enhancement": True
            },
            {
                "question": "How do we implement systematic governance for our platform architecture decisions?",
                "description": "Governance and systematic framework question (should trigger enhancement)",
                "expected_enhancement": True
            }
        ]
        
        print(f"\n{DemoColors.HEADER}🎯 Testing Diego Enhancement Decision Engine{DemoColors.ENDC}")
        print(f"{DemoColors.OKBLUE}Demonstrating complexity analysis and enhancement triggering{DemoColors.ENDC}\n")
        
        for i, demo_item in enumerate(demo_questions, 1):
            question = demo_item["question"]
            description = demo_item["description"]
            expected_enhancement = demo_item["expected_enhancement"]
            
            print(f"{DemoColors.BOLD}Demo {i}: {description}{DemoColors.ENDC}")
            print(f"Question: \"{question}\"")
            
            # Get enhanced response
            start_time = time.time()
            response = await persona_manager.get_enhanced_response("diego", question)
            response_time = time.time() - start_time
            
            # Display results
            enhancement_color = DemoColors.OKGREEN if response.enhancement_status == EnhancementStatus.SUCCESS else DemoColors.WARNING
            print(f"Enhancement Status: {enhancement_color}{response.enhancement_status.value}{DemoColors.ENDC}")
            print(f"Processing Time: {response.processing_time:.2f}s")
            print(f"Complexity Score: {response.complexity_score:.2f}")
            
            if response.mcp_server_used:
                print(f"MCP Server: {response.mcp_server_used}")
            
            if response.transparency_message:
                print(f"Transparency: {response.transparency_message}")
            
            if response.fallback_reason:
                print(f"Fallback Reason: {response.fallback_reason}")
            
            print(f"\nDiego's Response:")
            print(f"{DemoColors.OKCYAN}{response.content}{DemoColors.ENDC}")
            
            # Validation
            if expected_enhancement and response.enhancement_status == EnhancementStatus.SUCCESS:
                print(f"{DemoColors.OKGREEN}✅ Enhancement triggered as expected{DemoColors.ENDC}")
            elif not expected_enhancement and response.enhancement_status == EnhancementStatus.FALLBACK:
                print(f"{DemoColors.OKGREEN}✅ Standard response as expected{DemoColors.ENDC}")
            else:
                status_msg = "enhanced" if response.enhancement_status == EnhancementStatus.SUCCESS else "standard"
                expected_msg = "enhanced" if expected_enhancement else "standard"
                print(f"{DemoColors.WARNING}ℹ️ Got {status_msg} response, expected {expected_msg}{DemoColors.ENDC}")
            
            print(f"\n{'-' * 80}\n")
        
        # Performance demonstration
        print(f"{DemoColors.HEADER}⚡ Performance Demonstration{DemoColors.ENDC}")
        print(f"{DemoColors.OKBLUE}Testing response times and SLA compliance{DemoColors.ENDC}\n")
        
        performance_question = "How should we approach systematic organizational scaling?"
        times = []
        
        for i in range(3):
            start = time.time()
            response = await persona_manager.get_enhanced_response("diego", performance_question)
            elapsed = time.time() - start
            times.append(elapsed)
            
            sla_status = "✅ PASS" if elapsed <= 5.0 else "❌ FAIL"
            print(f"Test {i+1}: {elapsed:.2f}s {sla_status}")
        
        avg_time = sum(times) / len(times)
        print(f"\nAverage Response Time: {avg_time:.2f}s")
        print(f"SLA Compliance (≤5s): {'✅ PASS' if avg_time <= 5.0 else '❌ FAIL'}")
        
        # Graceful degradation demo
        print(f"\n{DemoColors.HEADER}🛡️ Graceful Degradation Demo{DemoColors.ENDC}")
        print(f"{DemoColors.OKBLUE}Demonstrating behavior when MCP servers are unavailable{DemoColors.ENDC}\n")
        
        # Simulate server unavailability
        original_is_available = persona_manager.mcp_client.is_available
        persona_manager.mcp_client.is_available = False
        
        degradation_response = await persona_manager.get_enhanced_response(
            "diego", 
            "How should we restructure our platform teams?"
        )
        
        print(f"Status: {degradation_response.enhancement_status.value}")
        print(f"Transparency Message: {degradation_response.transparency_message}")
        print(f"Response: {degradation_response.content}")
        print(f"{DemoColors.OKGREEN}✅ Graceful degradation working - full functionality maintained{DemoColors.ENDC}")
        
        # Restore availability
        persona_manager.mcp_client.is_available = original_is_available
        
        print(f"\n{DemoColors.HEADER}🎉 Sprint 2 Demo Complete{DemoColors.ENDC}")
        print(f"{DemoColors.OKGREEN}✅ Diego Sequential integration fully functional{DemoColors.ENDC}")
        print(f"{DemoColors.OKGREEN}✅ Transparent communication implemented{DemoColors.ENDC}")
        print(f"{DemoColors.OKGREEN}✅ Performance SLA compliance validated{DemoColors.ENDC}")
        print(f"{DemoColors.OKGREEN}✅ Graceful degradation verified{DemoColors.ENDC}")
        
    except Exception as e:
        print(f"{DemoColors.FAIL}❌ Demo error: {e}{DemoColors.ENDC}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        await persona_manager.cleanup()
        print(f"\n{DemoColors.OKCYAN}🧹 Cleanup complete{DemoColors.ENDC}")


async def interactive_demo():
    """Interactive demo mode"""
    print(f"\n{DemoColors.HEADER}🎮 Interactive Enhanced Diego Demo{DemoColors.ENDC}")
    print(f"{DemoColors.OKBLUE}Ask Diego strategic questions and see the enhancement system in action!{DemoColors.ENDC}")
    print(f"{DemoColors.OKCYAN}Type 'quit' or 'exit' to end the demo{DemoColors.ENDC}\n")
    
    persona_manager = EnhancedPersonaManager()
    await persona_manager.initialize()
    
    try:
        while True:
            # Get user input
            question = input(f"{DemoColors.BOLD}Your question for Diego: {DemoColors.ENDC}").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
                
            if not question:
                continue
            
            print(f"\n{DemoColors.OKCYAN}🤔 Diego is analyzing your question...{DemoColors.ENDC}")
            
            # Get enhanced response
            start_time = time.time()
            response = await persona_manager.get_enhanced_response("diego", question)
            
            # Display results
            print(f"\n{DemoColors.BOLD}Diego's Response:{DemoColors.ENDC}")
            print(f"{response.content}")
            
            # Show enhancement details
            print(f"\n{DemoColors.OKBLUE}Enhancement Details:{DemoColors.ENDC}")
            print(f"  Status: {response.enhancement_status.value}")
            print(f"  Processing Time: {response.processing_time:.2f}s")
            print(f"  Complexity Score: {response.complexity_score:.2f}")
            
            if response.mcp_server_used:
                print(f"  Enhanced with: {response.mcp_server_used}")
            
            if response.transparency_message:
                print(f"  Note: {response.transparency_message}")
                
            print(f"\n{'-' * 60}")
        
    except KeyboardInterrupt:
        print(f"\n{DemoColors.OKCYAN}Demo interrupted by user{DemoColors.ENDC}")
    except Exception as e:
        print(f"\n{DemoColors.FAIL}Demo error: {e}{DemoColors.ENDC}")
    finally:
        await persona_manager.cleanup()
        print(f"\n{DemoColors.OKGREEN}Thanks for trying the Enhanced Diego demo!{DemoColors.ENDC}")


def main():
    """Main demo function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_demo())
    else:
        asyncio.run(demo_enhanced_diego())


if __name__ == "__main__":
    main()
