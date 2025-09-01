#!/usr/bin/env python3
"""
Conversational Analytics Workflow
Phase 7 Week 2 - Complete Chat-Based Analytics Pipeline

🏗️ Martin | Platform Architecture - Chat-based real-time infrastructure
🤖 Berny | AI/ML Engineering - Performance optimization
💼 Alvaro | Business Strategy - ROI tracking integration
🎨 Rachel | Design Systems - Chat-embedded visual UX

Complete pipeline: Chat Query → Real-Time Data → Chat-Embedded Visualization
PRD Compliance: All interactions through Cursor/Claude chat interface (Lines 158-161).
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

from .conversational_data_manager import (
    ConversationalDataManager,
    ConversationalQuery,
    DataResponse,
    create_conversational_data_manager,
)
from .executive_visualization_server import (
    ExecutiveVisualizationEngine,
    VisualizationResult,
)
from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConversationalAnalyticsResult:
    """Complete result of conversational analytics pipeline"""

    success: bool
    query_text: str
    parsed_query: ConversationalQuery
    data_response: DataResponse
    visualization_result: VisualizationResult
    total_latency_ms: int
    pipeline_metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["parsed_query"] = self.parsed_query.to_dict()
        result["data_response"] = self.data_response.to_dict()
        return result


class ConversationalAnalyticsWorkflow:
    """
    Complete conversational analytics pipeline for Phase 7 Week 2.

    Integrates:
    - ConversationalDataManager: Parse queries + fetch real-time data
    - ExecutiveVisualizationEngine: Generate chat-embedded visualizations

    PRD Compliance: Chat-only interface with Magic MCP visual embedding.
    """

    def __init__(self):
        self.name = "conversational-analytics-workflow"
        self.version = "1.0.0"

        # Initialize components
        self.data_manager = create_conversational_data_manager()
        self.visualization_engine = ExecutiveVisualizationEngine()

        # Performance tracking
        self.pipeline_metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "avg_latency_ms": 0.0,
            "avg_data_fetch_ms": 0.0,
            "avg_visualization_ms": 0.0,
        }

        logger.info(f"Conversational Analytics Workflow {self.version} initialized")

    async def process_chat_query(
        self, query_text: str, persona: str = "diego", context: Dict[str, Any] = None
    ) -> ConversationalAnalyticsResult:
        """
        Complete pipeline: Chat query → Real-time data → Chat visualization.

        Args:
            query_text: Natural language query from chat
            persona: Strategic persona for visualization style
            context: Conversation context for better parsing

        Returns:
            ConversationalAnalyticsResult: Complete pipeline result
        """
        start_time = time.time()

        try:
            # Step 1: Parse conversational query
            logger.info(f"Processing chat query: '{query_text[:50]}...'")
            parsed_query, data_response = (
                await self.data_manager.process_conversational_query(
                    query_text, context
                )
            )

            data_fetch_time = time.time()

            # Step 2: Generate chat-embedded visualization
            if data_response.success:
                visualization_result = await self.visualization_engine.generate_chat_embedded_visualization(
                    data_response.data, persona=persona, context=context
                )
            else:
                # Create error visualization
                visualization_result = VisualizationResult(
                    success=False,
                    html_output=self._generate_error_response(
                        data_response.error_message
                    ),
                    chart_type="error",
                    persona=persona,
                    generation_time=0.0,
                    file_size_bytes=0,
                    interactive_elements=[],
                    metadata={"error": data_response.error_message},
                )

            total_latency = (time.time() - start_time) * 1000

            # Update metrics
            self._update_pipeline_metrics(
                total_latency,
                data_response.latency_ms,
                visualization_result.generation_time * 1000,
                data_response.success and visualization_result.success,
            )

            return ConversationalAnalyticsResult(
                success=data_response.success and visualization_result.success,
                query_text=query_text,
                parsed_query=parsed_query,
                data_response=data_response,
                visualization_result=visualization_result,
                total_latency_ms=int(total_latency),
                pipeline_metadata={
                    "persona": persona,
                    "context_provided": bool(context),
                    "data_fetch_ms": data_response.latency_ms,
                    "visualization_ms": int(
                        visualization_result.generation_time * 1000
                    ),
                    "pipeline_version": self.version,
                    "chat_optimized": True,
                    "magic_mcp_ready": True,
                },
            )

        except Exception as e:
            total_latency = (time.time() - start_time) * 1000
            logger.error(f"Conversational analytics pipeline failed: {str(e)}")

            # Create error result
            error_visualization = VisualizationResult(
                success=False,
                html_output=self._generate_error_response(str(e)),
                chart_type="pipeline_error",
                persona=persona,
                generation_time=0.0,
                file_size_bytes=0,
                interactive_elements=[],
                metadata={"pipeline_error": str(e)},
            )

            return ConversationalAnalyticsResult(
                success=False,
                query_text=query_text,
                parsed_query=ConversationalQuery(
                    query_type=QueryType.GENERAL_ANALYTICS,
                    entities=[],
                    context=context or {},
                ),
                data_response=DataResponse(
                    query_id="error",
                    data={},
                    source="error",
                    timestamp=datetime.now(),
                    latency_ms=int(total_latency),
                    success=False,
                    error_message=str(e),
                ),
                visualization_result=error_visualization,
                total_latency_ms=int(total_latency),
                pipeline_metadata={"error": str(e), "pipeline_version": self.version},
            )

    def _generate_error_response(self, error_message: str) -> str:
        """Generate user-friendly error response for chat"""

        from jinja2 import Template

        error_template = Template(
            """
        <div class="claudedirector-error-response" style="
            max-width: 100%;
            margin: 10px 0;
            border: 1px solid #dc3545;
            border-radius: 8px;
            background: #f8d7da;
            color: #721c24;
            padding: 16px;
        ">
            <div style="font-weight: 600; margin-bottom: 8px;">
                ⚠️ Unable to Process Query
            </div>
            <div style="font-size: 14px; margin-bottom: 12px;">
                {{ error_message }}
            </div>
            <div style="font-size: 12px; color: #856404;">
                💡 Try asking about:
                <ul style="margin: 4px 0 0 20px;">
                    <li>Sprint metrics: "Show me current sprint status"</li>
                    <li>Team performance: "How is the platform team doing?"</li>
                    <li>ROI analysis: "What's our platform investment ROI?"</li>
                    <li>System health: "Show me architecture health metrics"</li>
                </ul>
            </div>
        </div>
        """
        )

        return error_template.render(error_message=error_message)

    def _update_pipeline_metrics(
        self,
        total_latency_ms: float,
        data_fetch_ms: int,
        visualization_ms: float,
        success: bool,
    ):
        """Update pipeline performance metrics"""

        self.pipeline_metrics["total_queries"] += 1

        if success:
            self.pipeline_metrics["successful_queries"] += 1

        # Update running averages
        total_queries = self.pipeline_metrics["total_queries"]

        self.pipeline_metrics["avg_latency_ms"] = (
            self.pipeline_metrics["avg_latency_ms"] * (total_queries - 1)
            + total_latency_ms
        ) / total_queries

        self.pipeline_metrics["avg_data_fetch_ms"] = (
            self.pipeline_metrics["avg_data_fetch_ms"] * (total_queries - 1)
            + data_fetch_ms
        ) / total_queries

        self.pipeline_metrics["avg_visualization_ms"] = (
            self.pipeline_metrics["avg_visualization_ms"] * (total_queries - 1)
            + visualization_ms
        ) / total_queries

    async def get_pipeline_health(self) -> Dict[str, Any]:
        """Get pipeline health and performance metrics"""

        success_rate = 0.0
        if self.pipeline_metrics["total_queries"] > 0:
            success_rate = (
                self.pipeline_metrics["successful_queries"]
                / self.pipeline_metrics["total_queries"]
            )

        return {
            "pipeline_name": self.name,
            "version": self.version,
            "health_status": (
                "healthy"
                if success_rate > 0.95
                else "warning" if success_rate > 0.8 else "critical"
            ),
            "metrics": {
                **self.pipeline_metrics,
                "success_rate": success_rate,
                "target_latency_ms": 5000,  # <5s per PRD
                "target_success_rate": 0.95,
            },
            "components": {
                "data_manager": "operational",
                "visualization_engine": "operational",
            },
            "prd_compliance": {
                "chat_only_interface": True,
                "magic_mcp_integration": True,
                "real_time_data": True,
                "context_preservation": True,
            },
        }

    def get_supported_query_examples(self) -> List[Dict[str, str]]:
        """Get examples of supported conversational queries"""

        return [
            {
                "category": "Sprint Metrics",
                "example": "Show me current sprint metrics for the platform team",
                "persona": "diego",
            },
            {
                "category": "Team Performance",
                "example": "How is our team performing this quarter?",
                "persona": "diego",
            },
            {
                "category": "ROI Analysis",
                "example": "What's the ROI on our platform investment?",
                "persona": "alvaro",
            },
            {
                "category": "Architecture Health",
                "example": "Show me system health and performance metrics",
                "persona": "martin",
            },
            {
                "category": "Design System",
                "example": "How is design system adoption going?",
                "persona": "rachel",
            },
            {
                "category": "GitHub Activity",
                "example": "Show me repository activity for ai-leadership",
                "persona": "martin",
            },
        ]


# Factory function for integration
def create_conversational_analytics_workflow() -> ConversationalAnalyticsWorkflow:
    """Create and configure ConversationalAnalyticsWorkflow instance"""
    return ConversationalAnalyticsWorkflow()


# Import fix for datetime
from datetime import datetime
from .conversational_data_manager import QueryType
