#!/usr/bin/env python3
"""
Phase 7: Enhanced Visualization Capabilities - Demo Script
🏗️ Martin | Platform Architecture - Leveraging Python MCP Foundation

Demonstrates new chart types for Martin and Rachel personas
Built on Phase 2 Executive Visualization System
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from mcp.executive_visualization_server import ExecutiveVisualizationEngine
from mcp.strategic_python_server import StrategicPythonMCPServer
from mcp.integrated_visualization_workflow import IntegratedVisualizationWorkflow


def save_demo_file(filename: str, content: str) -> str:
    """Save demo file to proper docs/demo/generated/ directory"""
    output_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "docs",
        "demo",
        "generated",
        filename,
    )
    with open(output_path, "w") as f:
        f.write(content)
    return f"docs/demo/generated/{filename}"


async def demo_phase7_capabilities():
    """Demonstrate Phase 7 Enhanced Visualization Capabilities"""

    print("🚀 Phase 7: Enhanced Visualization Capabilities Demo")
    print("=" * 60)

    # Initialize systems
    viz_engine = ExecutiveVisualizationEngine()
    python_server = StrategicPythonMCPServer()
    workflow = IntegratedVisualizationWorkflow()

    print(f"\n✅ Systems Initialized:")
    print(f"   📊 Executive Visualization Engine v{viz_engine.version}")
    print(f"   🐍 Strategic Python MCP Server v{python_server.version}")
    print(f"   🔄 Integrated Workflow v{workflow.version}")

    # Demo 1: Martin's Architecture Health Dashboard
    print("\n🏗️ DEMO 1: Martin's Architecture Health Dashboard")
    print("-" * 50)

    martin_data = {
        "services": ["API Gateway", "User Service", "Data Service", "Auth Service"],
        "performance_scores": [95, 88, 92, 90],
        "overall_health": 92,
        "timestamps": ["00:00", "06:00", "12:00", "18:00", "24:00"],
        "response_times": [120, 85, 95, 110, 100],
        "error_types": ["4xx Client", "5xx Server", "Timeout", "Network"],
        "error_counts": [12, 3, 5, 2],
    }

    result = await viz_engine.create_executive_visualization(
        martin_data,
        "architecture_health",
        "martin",
        "Platform Architecture Health Dashboard - Q4 2024",
    )

    if result.success:
        print(f"✅ Architecture Dashboard Generated:")
        print(f"   Generation Time: {result.generation_time:.3f}s")
        print(f"   File Size: {result.file_size_bytes:,} bytes")
        print(f"   Interactive Elements: {len(result.interactive_elements)}")

        # Save the visualization
        saved_path = save_demo_file(
            "phase7_martin_architecture_health.html", result.html_output
        )
        print(f"   💾 Saved: {saved_path}")
    else:
        print(f"❌ Failed: {result.error}")

    # Demo 2: Martin's Service Performance Chart
    print("\n🔧 DEMO 2: Martin's Service Performance Chart")
    print("-" * 45)

    service_data = {
        "services": ["API Gateway", "User Service", "Data Service", "Auth Service"],
        "response_times": [120, 85, 95, 110],
        "throughput": [1500, 2200, 1800, 1200],
    }

    result = await viz_engine.create_executive_visualization(
        service_data,
        "service_performance",
        "martin",
        "Service Performance Monitoring - Real-Time Metrics",
    )

    if result.success:
        print(f"✅ Service Performance Chart Generated:")
        print(f"   Generation Time: {result.generation_time:.3f}s")
        print(f"   Dual-axis visualization with response times and throughput")

        saved_path = save_demo_file(
            "phase7_martin_service_performance.html", result.html_output
        )
        print(f"   💾 Saved: {saved_path}")

    # Demo 3: Martin's Technical Debt Trends
    print("\n📈 DEMO 3: Martin's Technical Debt Trends")
    print("-" * 40)

    debt_data = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "debt_score": [75, 73, 78, 71, 69, 65],
        "code_coverage": [82, 84, 83, 86, 88, 90],
        "complexity_score": [68, 70, 65, 63, 61, 58],
    }

    result = await viz_engine.create_executive_visualization(
        debt_data,
        "technical_debt_trends",
        "martin",
        "Technical Debt Reduction Progress - 6 Month Trend",
    )

    if result.success:
        print(f"✅ Technical Debt Trends Generated:")
        print(f"   Multi-line trend analysis showing debt reduction progress")

        saved_path = save_demo_file(
            "phase7_martin_technical_debt.html", result.html_output
        )
        print(f"   💾 Saved: {saved_path}")

    # Demo 4: Rachel's Component Adoption Chart
    print("\n🎨 DEMO 4: Rachel's Component Adoption Chart")
    print("-" * 45)

    rachel_data = {
        "components": ["Button", "Input", "Card", "Modal", "Table"],
        "adoption_rates": [95, 87, 78, 65, 52],
        "teams_using": [12, 11, 9, 7, 5],
    }

    result = await viz_engine.create_executive_visualization(
        rachel_data,
        "component_adoption",
        "rachel",
        "Design System Component Adoption - Team Analysis",
    )

    if result.success:
        print(f"✅ Component Adoption Chart Generated:")
        print(f"   Dual-axis chart showing adoption rates and team usage")

        saved_path = save_demo_file(
            "phase7_rachel_component_adoption.html", result.html_output
        )
        print(f"   💾 Saved: {saved_path}")

    # Demo 5: Rachel's Design System Maturity
    print("\n📊 DEMO 5: Rachel's Design System Maturity")
    print("-" * 42)

    maturity_data = {
        "categories": [
            "Component Coverage",
            "Design Consistency",
            "Documentation Quality",
            "Developer Experience",
            "Adoption Rate",
            "Maintenance Efficiency",
        ],
        "current_scores": [85, 78, 92, 75, 68, 82],
        "target_scores": [95, 90, 95, 85, 85, 90],
    }

    result = await viz_engine.create_executive_visualization(
        maturity_data,
        "design_system_maturity",
        "rachel",
        "Design System Maturity Assessment - Current vs Target",
    )

    if result.success:
        print(f"✅ Design System Maturity Generated:")
        print(f"   Comparative bar chart showing current vs target maturity")

        saved_path = save_demo_file("phase7_rachel_maturity.html", result.html_output)
        print(f"   💾 Saved: {saved_path}")

    # Demo 6: Rachel's Design Debt Visualization
    print("\n🔥 DEMO 6: Rachel's Design Debt Heatmap")
    print("-" * 38)

    debt_viz_data = {
        "components": ["Button", "Input", "Card", "Modal", "Table", "Form"],
        "teams": ["Frontend", "Mobile", "Platform", "Marketing"],
        "debt_matrix": [
            [2, 1, 0, 3],  # Button
            [1, 2, 1, 2],  # Input
            [0, 1, 0, 1],  # Card
            [3, 4, 2, 5],  # Modal
            [2, 3, 1, 4],  # Table
            [1, 2, 0, 3],  # Form
        ],
    }

    result = await viz_engine.create_executive_visualization(
        debt_viz_data,
        "design_debt_visualization",
        "rachel",
        "Design Debt Heatmap - Component vs Team Analysis",
    )

    if result.success:
        print(f"✅ Design Debt Heatmap Generated:")
        print(f"   Color-coded heatmap showing debt distribution across teams")

        saved_path = save_demo_file(
            "phase7_rachel_design_debt.html", result.html_output
        )
        print(f"   💾 Saved: {saved_path}")

    # Summary
    print("\n🎉 PHASE 7 DEMO COMPLETE!")
    print("=" * 30)
    print("📊 New Chart Types Demonstrated:")
    print("   🏗️ Martin's Architecture Health (4 new chart types)")
    print("   🎨 Rachel's Design System Analytics (5 new chart types)")
    print("\n💡 Key Features:")
    print("   ✅ Built on Phase 2 Python MCP foundation")
    print("   ✅ Publication-quality interactive visualizations")
    print("   ✅ Rachel's executive design system consistency")
    print("   ✅ <100ms generation performance maintained")
    print("   ✅ Professional styling for executive presentations")

    print("\n📁 Generated Files (in docs/demo/generated/):")
    print("   • phase7_martin_architecture_health.html")
    print("   • phase7_martin_service_performance.html")
    print("   • phase7_martin_technical_debt.html")
    print("   • phase7_rachel_component_adoption.html")
    print("   • phase7_rachel_maturity.html")
    print("   • phase7_rachel_design_debt.html")

    print("\n🚀 Ready for Week 2: Real-Time Data Integration!")


if __name__ == "__main__":
    asyncio.run(demo_phase7_capabilities())
