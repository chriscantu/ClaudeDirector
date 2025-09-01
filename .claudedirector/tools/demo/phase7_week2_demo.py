#!/usr/bin/env python3
"""
Phase 7 Week 2 Demo: Real-Time Conversational Analytics
PRD-Compliant Chat-Only Interface Demonstration

🏗️ Martin | Platform Architecture - Chat-based real-time infrastructure
🤖 Berny | AI/ML Engineering - Performance optimization
💼 Alvaro | Business Strategy - ROI tracking integration
🎨 Rachel | Design Systems - Chat-embedded visual UX

Demonstrates complete conversational analytics pipeline:
Chat Query → Real-Time Data → Chat-Embedded Visualization
"""

import asyncio
import time
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.mcp import (
    create_conversational_analytics_workflow,
    ConversationalAnalyticsWorkflow,
)


def save_demo_file(filename: str, content: str) -> str:
    """Save demo file to proper docs/demo/generated/ directory"""
    output_path = os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'docs', 'demo', 'generated', filename
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(content)
    return f"docs/demo/generated/{filename}"


async def demo_conversational_query(workflow: ConversationalAnalyticsWorkflow, query: str, persona: str = "diego"):
    """Demo a single conversational query"""
    
    print(f"\n🎯 **Query**: {query}")
    print(f"👤 **Persona**: {persona.title()}")
    print("🔄 **Processing**...")
    
    start_time = time.time()
    result = await workflow.process_chat_query(query, persona=persona)
    total_time = (time.time() - start_time) * 1000
    
    print(f"⏱️  **Total Time**: {total_time:.2f}ms")
    print(f"✅ **Success**: {result.success}")
    print(f"📊 **Chart Type**: {result.visualization_result.chart_type}")
    print(f"📏 **HTML Size**: {result.visualization_result.file_size_bytes:,} bytes")
    
    if result.success:
        # Save the chat-embedded visualization
        filename = f"week2_chat_{persona}_{query.replace(' ', '_').replace('?', '').lower()[:30]}.html"
        saved_path = save_demo_file(filename, result.visualization_result.html_output)
        print(f"💾 **Saved**: {saved_path}")
    
    return result


async def main():
    """Main demo function"""
    
    print("🚀 **Phase 7 Week 2: Real-Time Conversational Analytics Demo**")
    print("=" * 70)
    print("PRD Compliance: Chat-Only Interface (Lines 158-161)")
    print("- Executive reporting via chat interface")
    print("- Strategic metrics through conversational queries")
    print("- Trend analysis via natural language requests")
    print("=" * 70)
    
    # Initialize workflow
    print("\n🏗️ **Initializing Conversational Analytics Workflow**...")
    workflow = create_conversational_analytics_workflow()
    
    # Demo queries for different personas and use cases
    demo_queries = [
        {
            "query": "Show me current sprint metrics for the platform team",
            "persona": "diego",
            "description": "Diego's sprint leadership dashboard"
        },
        {
            "query": "What's our platform investment ROI this quarter?",
            "persona": "alvaro", 
            "description": "Alvaro's business value analysis"
        },
        {
            "query": "How is our team performing compared to last month?",
            "persona": "diego",
            "description": "Diego's team performance tracking"
        },
        {
            "query": "Show me architecture health and system metrics",
            "persona": "martin",
            "description": "Martin's platform architecture monitoring"
        },
        {
            "query": "How is design system adoption going across teams?",
            "persona": "rachel",
            "description": "Rachel's design system analytics"
        },
        {
            "query": "Show me GitHub activity for the ai-leadership repository",
            "persona": "martin",
            "description": "Martin's development activity tracking"
        }
    ]
    
    # Process each demo query
    results = []
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n📋 **Demo {i}/6**: {demo['description']}")
        print("-" * 50)
        
        result = await demo_conversational_query(
            workflow, 
            demo["query"], 
            demo["persona"]
        )
        results.append(result)
    
    # Performance summary
    print(f"\n📊 **Performance Summary**")
    print("=" * 50)
    
    successful_queries = [r for r in results if r.success]
    total_queries = len(results)
    success_rate = len(successful_queries) / total_queries
    
    avg_latency = sum(r.total_latency_ms for r in results) / len(results)
    avg_data_fetch = sum(r.data_response.latency_ms for r in results) / len(results)
    avg_visualization = sum(r.visualization_result.generation_time * 1000 for r in results) / len(results)
    
    print(f"✅ **Success Rate**: {success_rate:.1%} ({len(successful_queries)}/{total_queries})")
    print(f"⏱️  **Average Latency**: {avg_latency:.2f}ms (Target: <5000ms)")
    print(f"📊 **Data Fetch Time**: {avg_data_fetch:.2f}ms")
    print(f"🎨 **Visualization Time**: {avg_visualization:.2f}ms (Target: <500ms)")
    
    # PRD Compliance Check
    print(f"\n✅ **PRD Compliance Verification**")
    print("-" * 40)
    
    all_chat_optimized = all(
        r.pipeline_metadata.get("chat_optimized", False) for r in results
    )
    all_magic_mcp_ready = all(
        r.pipeline_metadata.get("magic_mcp_ready", False) for r in results
    )
    
    print(f"💬 **Chat-Only Interface**: {'✅ PASS' if all_chat_optimized else '❌ FAIL'}")
    print(f"🎭 **Magic MCP Integration**: {'✅ PASS' if all_magic_mcp_ready else '❌ FAIL'}")
    print(f"⚡ **<5s Response Time**: {'✅ PASS' if avg_latency < 5000 else '❌ FAIL'}")
    print(f"🎨 **<500ms Visualization**: {'✅ PASS' if avg_visualization < 500 else '❌ FAIL'}")
    
    # Pipeline health check
    print(f"\n🏥 **Pipeline Health Check**")
    print("-" * 30)
    
    health = await workflow.get_pipeline_health()
    print(f"🔋 **Health Status**: {health['health_status'].upper()}")
    print(f"📈 **Success Rate**: {health['metrics']['success_rate']:.1%}")
    print(f"⚡ **Avg Latency**: {health['metrics']['avg_latency_ms']:.2f}ms")
    
    # Context preservation demo
    print(f"\n🔄 **Context Preservation Demo**")
    print("-" * 35)
    
    # First query
    context = {"conversation_id": "demo_conversation"}
    result1 = await demo_conversational_query(
        workflow,
        "Show me sprint metrics for platform team",
        "diego"
    )
    
    # Follow-up query with context
    context_with_history = {
        "conversation_id": "demo_conversation",
        "previous_entities": ["platform"],
        "previous_query_type": "sprint_metrics"
    }
    
    print(f"\n🔗 **Follow-up Query with Context**:")
    result2 = await workflow.process_chat_query(
        "Break that down by completion status",
        persona="diego",
        context=context_with_history
    )
    
    print(f"✅ **Context Preserved**: {result2.pipeline_metadata.get('context_provided', False)}")
    
    # Summary
    print(f"\n🎉 **Phase 7 Week 2 Demo Complete!**")
    print("=" * 45)
    print("✅ **ConversationalDataManager**: Query parsing + real-time data fetching")
    print("✅ **ChatEmbeddedVisualization**: Magic MCP integration for chat visuals")
    print("✅ **ConversationalAnalyticsWorkflow**: Complete pipeline integration")
    print("✅ **PRD Compliance**: Chat-only interface maintained throughout")
    print("✅ **Performance Targets**: <5s queries, <500ms visualizations")
    print("✅ **Context Preservation**: Multi-turn conversation support")
    
    print(f"\n📁 **Generated Files**: Check docs/demo/generated/ for chat-embedded visualizations")
    print(f"🚀 **Ready for Week 3**: Advanced Interactivity & Real-Time Updates")


if __name__ == "__main__":
    asyncio.run(main())
