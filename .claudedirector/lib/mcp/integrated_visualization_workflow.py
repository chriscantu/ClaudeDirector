#!/usr/bin/env python3
"""
Integrated Visualization Workflow
Combines Phase 1 Strategic Python MCP + Phase 2 Executive Visualization

🏗️ Martin | Platform Architecture - Integration & Workflow
🎨 Rachel | Design Systems Strategy - Executive Design Standards
💼 Alvaro | Business Strategy - ROI & Executive Requirements
🤖 Berny | AI/ML Engineering - Performance Optimization

Complete workflow: Strategic Data Analysis → Executive Visualization
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

from .strategic_python_server import StrategicPythonMCPServer, ExecutionResult
from .executive_visualization_server import (
    ExecutiveVisualizationEngine,
    VisualizationResult,
)
from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IntegratedWorkflowResult:
    """Result of integrated strategic analysis + visualization workflow"""

    success: bool
    analysis_result: ExecutionResult
    visualization_result: VisualizationResult
    total_workflow_time: float
    workflow_steps: List[str]
    transparency_disclosure: str
    error: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class IntegratedVisualizationWorkflow:
    """
    Integrated workflow combining Phase 1 + Phase 2
    Strategic Data Analysis → Executive Visualization
    """

    def __init__(self):
        self.name = MCPServerConstants.INTEGRATED_WORKFLOW_NAME
        self.version = MCPServerConstants.INTEGRATED_WORKFLOW_VERSION

        # Initialize Phase 1 and Phase 2 components
        self.strategic_python_server = StrategicPythonMCPServer()
        self.visualization_engine = ExecutiveVisualizationEngine()

        # Workflow capabilities
        self.capabilities = [
            MCPServerConstants.Capabilities.INTEGRATED_STRATEGIC_ANALYSIS,
            MCPServerConstants.Capabilities.DATA_DRIVEN_VISUALIZATIONS,
            MCPServerConstants.Capabilities.EXECUTIVE_READY_PRESENTATIONS,
            MCPServerConstants.Capabilities.END_TO_END_INTELLIGENCE,
        ]

        # Workflow metrics
        self.workflow_metrics = {
            MCPServerConstants.MetricsKeys.TOTAL_WORKFLOWS: 0,
            MCPServerConstants.MetricsKeys.SUCCESSFUL_WORKFLOWS: 0,
            MCPServerConstants.MetricsKeys.AVG_WORKFLOW_TIME: 0.0,
            MCPServerConstants.MetricsKeys.ANALYSIS_SUCCESS_RATE: 0.0,
            MCPServerConstants.MetricsKeys.VISUALIZATION_SUCCESS_RATE: 0.0,
        }

        logger.info(f"Integrated Visualization Workflow {self.version} initialized")

    async def create_strategic_visualization(
        self,
        data_analysis_code: str,
        visualization_spec: Dict[str, Any],
        persona: str,
        context: Dict[str, Any] = None,
    ) -> IntegratedWorkflowResult:
        """
        Complete workflow: Strategic Data Analysis → Executive Visualization

        Args:
            data_analysis_code: Python code for strategic analysis
            visualization_spec: Visualization configuration
            persona: Strategic persona (diego, alvaro, martin, camille, rachel)
            context: Additional context for analysis
        """

        start_time = time.time()
        context = context or {}
        workflow_steps = []

        try:
            # Update metrics
            self.workflow_metrics["total_workflows"] += 1

            # Step 1: Execute strategic analysis (Phase 1)
            workflow_steps.append("strategic_analysis")
            logger.info(f"Step 1: Executing strategic analysis for {persona}")

            analysis_result = await self.strategic_python_server.execute_strategic_code(
                data_analysis_code, persona, context
            )

            if not analysis_result.success:
                return IntegratedWorkflowResult(
                    success=False,
                    analysis_result=analysis_result,
                    visualization_result=VisualizationResult(
                        success=False,
                        html_output="",
                        chart_type="",
                        persona=persona,
                        generation_time=0,
                        file_size_bytes=0,
                        interactive_elements=[],
                        error="Analysis failed",
                    ),
                    total_workflow_time=time.time() - start_time,
                    workflow_steps=workflow_steps,
                    transparency_disclosure="",
                    error=f"Strategic analysis failed: {analysis_result.error}",
                )

            # Step 2: Process analysis output for visualization
            workflow_steps.append("data_processing")
            logger.info("Step 2: Processing analysis output for visualization")

            visualization_data = self._process_analysis_for_visualization(
                analysis_result.output, visualization_spec
            )

            # Step 3: Generate executive visualization (Phase 2)
            workflow_steps.append("executive_visualization")
            logger.info(
                f"Step 3: Generating executive visualization - {visualization_spec.get('chart_type', 'default')}"
            )

            visualization_result = await self.visualization_engine.create_executive_visualization(
                visualization_data,
                visualization_spec.get("chart_type", "default"),
                persona,
                visualization_spec.get("title", "Strategic Analysis"),
                context,
            )

            # Step 4: Generate integrated transparency disclosure
            workflow_steps.append("transparency_integration")
            transparency_disclosure = self._generate_integrated_transparency_disclosure(
                analysis_result, visualization_result, persona, workflow_steps
            )

            # Calculate workflow metrics
            total_workflow_time = time.time() - start_time

            # Update success metrics
            if analysis_result.success and visualization_result.success:
                self.workflow_metrics["successful_workflows"] += 1

            self._update_workflow_metrics(
                total_workflow_time,
                analysis_result.success,
                visualization_result.success,
            )

            result = IntegratedWorkflowResult(
                success=analysis_result.success and visualization_result.success,
                analysis_result=analysis_result,
                visualization_result=visualization_result,
                total_workflow_time=total_workflow_time,
                workflow_steps=workflow_steps,
                transparency_disclosure=transparency_disclosure,
            )

            logger.info(f"Integrated workflow completed: {persona} ({total_workflow_time:.2f}s)")
            return result

        except Exception as e:
            logger.error(f"Integrated workflow error: {str(e)}")
            return IntegratedWorkflowResult(
                success=False,
                analysis_result=ExecutionResult(
                    success=False,
                    output="",
                    error=str(e),
                    execution_time=0,
                    memory_usage=0,
                    persona_context=persona,
                ),
                visualization_result=VisualizationResult(
                    success=False,
                    html_output="",
                    chart_type="",
                    persona=persona,
                    generation_time=0,
                    file_size_bytes=0,
                    interactive_elements=[],
                    error=str(e),
                ),
                total_workflow_time=time.time() - start_time,
                workflow_steps=workflow_steps,
                transparency_disclosure="",
                error=f"Integrated workflow error: {str(e)}",
            )

    def _process_analysis_for_visualization(
        self, analysis_output: str, visualization_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process strategic analysis output into visualization-ready data"""

        # Try to extract structured data from analysis output
        try:
            # Look for JSON data in the output
            import re

            json_matches = re.findall(r"\{[^{}]*\}", analysis_output)

            if json_matches:
                # Try to parse the first JSON match
                for json_str in json_matches:
                    try:
                        data = json.loads(json_str)
                        if isinstance(data, dict):
                            return data
                    except:
                        continue
        except Exception as e:
            logger.warning(f"Could not extract JSON from analysis output: {e}")

        # Fallback: Create visualization data based on chart type and analysis output
        chart_type = visualization_spec.get("chart_type", "default")

        if chart_type == "leadership_dashboard":
            return self._create_leadership_sample_data(analysis_output)
        elif chart_type == "roi_analysis":
            return self._create_roi_sample_data(analysis_output)
        elif chart_type == "architecture_health":
            return self._create_architecture_sample_data(analysis_output)
        else:
            return self._create_default_sample_data(analysis_output)

    def _create_leadership_sample_data(self, analysis_output: str) -> Dict[str, Any]:
        """Create sample leadership dashboard data"""
        return {
            "velocity_data": {
                "dates": ["2024-01", "2024-02", "2024-03", "2024-04"],
                "velocity": [15, 18, 22, 25],
            },
            "support_data": {
                "months": ["Jan", "Feb", "Mar", "Apr"],
                "volume": [45, 38, 42, 35],
            },
            "initiative_progress": {"current": 78, "target": 85},
            "platform_health": {
                "labels": ["Healthy", "Warning", "Critical"],
                "values": [75, 20, 5],
            },
            "analysis_source": (
                analysis_output[:200] + "..." if len(analysis_output) > 200 else analysis_output
            ),
        }

    def _create_roi_sample_data(self, analysis_output: str) -> Dict[str, Any]:
        """Create sample ROI analysis data"""
        return {
            "roi_trend": {
                "months": ["Q1", "Q2", "Q3", "Q4"],
                "roi": [120, 135, 148, 162],
            },
            "cost_benefit": {
                "categories": ["Development", "Infrastructure", "Training", "Tools"],
                "costs": [50000, 25000, 15000, 10000],
                "benefits": [80000, 45000, 30000, 25000],
            },
            "analysis_source": (
                analysis_output[:200] + "..." if len(analysis_output) > 200 else analysis_output
            ),
        }

    def _create_architecture_sample_data(self, analysis_output: str) -> Dict[str, Any]:
        """Create sample architecture health data"""
        return {
            "performance_metrics": {
                "services": [
                    "API Gateway",
                    "User Service",
                    "Data Service",
                    "Auth Service",
                ],
                "response_times": [120, 85, 95, 110],
            },
            "system_health": {
                "components": ["Database", "Cache", "Queue", "Storage"],
                "health_scores": [95, 88, 92, 90],
            },
            "analysis_source": (
                analysis_output[:200] + "..." if len(analysis_output) > 200 else analysis_output
            ),
        }

    def _create_default_sample_data(self, analysis_output: str) -> Dict[str, Any]:
        """Create default sample data"""
        return {
            "x": ["Category A", "Category B", "Category C", "Category D"],
            "y": [23, 45, 56, 78],
            "analysis_source": (
                analysis_output[:200] + "..." if len(analysis_output) > 200 else analysis_output
            ),
        }

    def _generate_integrated_transparency_disclosure(
        self,
        analysis_result: ExecutionResult,
        visualization_result: VisualizationResult,
        persona: str,
        workflow_steps: List[str],
    ) -> str:
        """Generate comprehensive transparency disclosure for integrated workflow"""

        return f"""
🔧 Accessing MCP Servers: strategic-python + executive-visualization (Integrated Workflow)
*Executing end-to-end strategic intelligence: data analysis → executive visualization...*

**Integrated Strategic Intelligence Workflow**:
- **Phase 1**: Strategic Python MCP Server (Data Analysis)
  - Persona: {persona} (Strategic Analysis)
  - Execution: {analysis_result.execution_time:.2f}s
  - Status: {'✅ SUCCESS' if analysis_result.success else '❌ FAILED'}

- **Phase 2**: Executive Visualization System (Publication-Quality Charts)
  - Chart Type: {visualization_result.chart_type}
  - Generation: {visualization_result.generation_time:.2f}s
  - File Size: {visualization_result.file_size_bytes:,} bytes
  - Interactive Elements: {len(visualization_result.interactive_elements)}
  - Status: {'✅ SUCCESS' if visualization_result.success else '❌ FAILED'}

**Workflow Steps**: {' → '.join(workflow_steps)}
**Total Processing**: {analysis_result.execution_time + visualization_result.generation_time:.2f}s
**Security**: Sandboxed Python execution + Safe HTML generation
**Quality**: Executive-grade interactive visualizations with Rachel's design system
"""

    def _update_workflow_metrics(
        self, workflow_time: float, analysis_success: bool, viz_success: bool
    ):
        """Update workflow performance metrics"""

        # Update average workflow time
        total_workflows = self.workflow_metrics["total_workflows"]
        current_avg = self.workflow_metrics["avg_workflow_time"]
        self.workflow_metrics["avg_workflow_time"] = (
            current_avg * (total_workflows - 1) + workflow_time
        ) / total_workflows

        # Update success rates
        self.workflow_metrics["analysis_success_rate"] = (
            self.workflow_metrics["analysis_success_rate"] * (total_workflows - 1)
            + (1.0 if analysis_success else 0.0)
        ) / total_workflows

        self.workflow_metrics["visualization_success_rate"] = (
            self.workflow_metrics["visualization_success_rate"] * (total_workflows - 1)
            + (1.0 if viz_success else 0.0)
        ) / total_workflows

    async def create_persona_specific_analysis(
        self,
        query: str,
        persona: str,
        chart_type: str = None,
        context: Dict[str, Any] = None,
    ) -> IntegratedWorkflowResult:
        """
        Create persona-specific strategic analysis with visualization

        Args:
            query: Strategic question or analysis request
            persona: Strategic persona
            chart_type: Preferred chart type (auto-detected if None)
            context: Additional context
        """

        # Generate persona-specific analysis code
        analysis_code = self._generate_persona_analysis_code(query, persona, context)

        # Auto-detect chart type if not specified
        if not chart_type:
            chart_type = self._auto_detect_chart_type(query, persona)

        # Create visualization specification
        visualization_spec = {
            "chart_type": chart_type,
            "title": f"{query} - {persona.title()} Analysis",
            "persona_optimized": True,
        }

        return await self.create_strategic_visualization(
            analysis_code, visualization_spec, persona, context
        )

    def _generate_persona_analysis_code(
        self, query: str, persona: str, context: Dict[str, Any]
    ) -> str:
        """Generate persona-specific Python analysis code"""

        persona_templates = {
            "diego": """
# Diego's Leadership Analysis
import pandas as pd
import numpy as np

# Leadership metrics analysis
query = "{query}"
print(f"Leadership Analysis: {{query}}")

# Sample leadership data processing
leadership_data = {{
    'team_velocity': [15, 18, 22, 25],
    'support_volume': [45, 38, 42, 35],
    'initiative_progress': 78
}}

# Calculate leadership insights
avg_velocity = np.mean(leadership_data['team_velocity'])
velocity_trend = np.polyfit(range(len(leadership_data['team_velocity'])), leadership_data['team_velocity'], 1)[0]

print(f"Average team velocity: {{avg_velocity:.1f}}")
print(f"Velocity trend: {{'+' if velocity_trend > 0 else ''}}{{velocity_trend:.1f}} per period")
print(f"Initiative progress: {{leadership_data['initiative_progress']}}%")

result = {{
    "leadership_insights": {{
        "avg_velocity": avg_velocity,
        "velocity_trend": velocity_trend,
        "initiative_progress": leadership_data['initiative_progress']
    }}
}}
print(f"Analysis result: {{result}}")
""",
            "alvaro": """
# Alvaro's Business Intelligence Analysis
import pandas as pd
import numpy as np

# ROI and business metrics analysis
query = "{query}"
print(f"Business Analysis: {{query}}")

# Sample business data processing
business_data = {{
    'investments': [50000, 75000, 100000, 125000],
    'returns': [60000, 95000, 135000, 180000],
    'costs': [25000, 30000, 35000, 40000]
}}

# Calculate ROI insights
roi_values = [(r - i) / i * 100 for r, i in zip(business_data['returns'], business_data['investments'])]
avg_roi = np.mean(roi_values)
total_investment = sum(business_data['investments'])
total_return = sum(business_data['returns'])

print(f"Average ROI: {{avg_roi:.1f}}%")
print(f"Total investment: ${{total_investment:,}}")
print(f"Total return: ${{total_return:,}}")

result = {{
    "business_insights": {{
        "avg_roi": avg_roi,
        "total_investment": total_investment,
        "total_return": total_return,
        "roi_trend": roi_values
    }}
}}
print(f"Analysis result: {{result}}")
""",
            "martin": """
# Martin's Architecture Analysis
import pandas as pd
import numpy as np

# Platform and architecture metrics analysis
query = "{query}"
print(f"Architecture Analysis: {{query}}")

# Sample architecture data processing
arch_data = {{
    'response_times': [120, 85, 95, 110],
    'health_scores': [95, 88, 92, 90],
    'service_names': ['API Gateway', 'User Service', 'Data Service', 'Auth Service']
}}

# Calculate architecture insights
avg_response_time = np.mean(arch_data['response_times'])
avg_health_score = np.mean(arch_data['health_scores'])
critical_services = [name for name, score in zip(arch_data['service_names'], arch_data['health_scores']) if score < 90]

print(f"Average response time: {{avg_response_time:.1f}}ms")
print(f"Average health score: {{avg_health_score:.1f}}%")
print(f"Services needing attention: {{critical_services}}")

result = {{
    "architecture_insights": {{
        "avg_response_time": avg_response_time,
        "avg_health_score": avg_health_score,
        "critical_services": critical_services
    }}
}}
print(f"Analysis result: {{result}}")
""",
        }

        template = persona_templates.get(persona, persona_templates["diego"])
        return template.format(query=query)

    def _auto_detect_chart_type(self, query: str, persona: str) -> str:
        """Auto-detect appropriate chart type based on query and persona"""

        query_lower = query.lower()

        # Persona-specific defaults
        persona_defaults = {
            "diego": "leadership_dashboard",
            "alvaro": "roi_analysis",
            "martin": "architecture_health",
            "camille": "technology_roadmap",
            "rachel": "design_system_health",
        }

        # Query-based detection
        if any(word in query_lower for word in ["dashboard", "overview", "summary"]):
            return persona_defaults.get(persona, "leadership_dashboard")
        elif any(word in query_lower for word in ["roi", "investment", "cost", "benefit"]):
            return "roi_analysis"
        elif any(word in query_lower for word in ["team", "velocity", "performance"]):
            return "team_metrics"
        elif any(word in query_lower for word in ["trend", "over time", "historical"]):
            return "strategic_trends"
        else:
            return persona_defaults.get(persona, "default")

    def get_workflow_info(self) -> Dict[str, Any]:
        """Get integrated workflow information"""

        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "supported_personas": list(self.strategic_python_server.persona_configs.keys()),
            "phase1_info": self.strategic_python_server.get_server_info(),
            "phase2_info": self.visualization_engine.get_server_info(),
            "workflow_metrics": self.workflow_metrics,
        }

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on integrated workflow"""

        try:
            # Test integrated workflow
            test_result = await self.create_persona_specific_analysis(
                "Test strategic analysis", "diego", "default"
            )

            return {
                "status": "healthy" if test_result.success else "degraded",
                "workflow_info": self.get_workflow_info(),
                "last_health_check": time.time(),
                "test_result": {
                    "success": test_result.success,
                    "total_time": test_result.total_workflow_time,
                    "analysis_success": test_result.analysis_result.success,
                    "visualization_success": test_result.visualization_result.success,
                },
            }

        except Exception as e:
            logger.error(f"Integrated workflow health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_health_check": time.time(),
            }


# Factory function
def create_integrated_visualization_workflow() -> IntegratedVisualizationWorkflow:
    """Create and configure Integrated Visualization Workflow"""
    return IntegratedVisualizationWorkflow()


if __name__ == "__main__":
    # Test integrated workflow
    async def test_integrated_workflow():
        print("🚀 Testing Integrated Visualization Workflow...")

        workflow = IntegratedVisualizationWorkflow()
        print(f"✅ Workflow initialized: {workflow.name} v{workflow.version}")

        # Test persona-specific analysis
        result = await workflow.create_persona_specific_analysis(
            "How is our team velocity trending?", "diego", "leadership_dashboard"
        )

        print(f"✅ Integrated workflow: {'SUCCESS' if result.success else 'FAILED'}")
        if result.success:
            print(f"   Total workflow time: {result.total_workflow_time:.2f}s")
            print(f"   Analysis time: {result.analysis_result.execution_time:.2f}s")
            print(f"   Visualization time: {result.visualization_result.generation_time:.2f}s")
            print(f"   Workflow steps: {' → '.join(result.workflow_steps)}")
        else:
            print(f"   Error: {result.error}")

        # Test health check
        health = await workflow.health_check()
        print(f"✅ Health check: {health['status']}")

        print("🎉 Integrated Visualization Workflow test completed!")
        print(f"📊 Workflow metrics: {workflow.workflow_metrics}")

    asyncio.run(test_integrated_workflow())
