#!/usr/bin/env python3
"""
Conversational Data Manager
Phase 7 Week 2 - Real-Time Conversational Analytics

🏗️ Martin | Platform Architecture - Chat-based real-time infrastructure
🤖 Berny | AI/ML Engineering - Query parsing & performance optimization
💼 Alvaro | Business Strategy - ROI tracking integration
🎨 Rachel | Design Systems - Chat-embedded visual UX

Manages real-time data integration that responds to chat queries with <5 second latency.
PRD Compliance: All interactions through Cursor/Claude chat interface only.
"""

import asyncio
import json
import time
import logging
import re
from typing import Dict, Any, List, Optional, Callable, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
from datetime import datetime, timedelta

from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of conversational queries supported"""

    SPRINT_METRICS = "sprint_metrics"
    TEAM_PERFORMANCE = "team_performance"
    ROI_ANALYSIS = "roi_analysis"
    ARCHITECTURE_HEALTH = "architecture_health"
    DESIGN_SYSTEM_STATUS = "design_system_status"
    GITHUB_ACTIVITY = "github_activity"
    GENERAL_ANALYTICS = "general_analytics"


@dataclass
class ConversationalQuery:
    """Represents a parsed conversational query"""

    query_type: QueryType
    entities: List[str]  # Teams, projects, time periods, etc.
    time_range: Optional[str] = None
    filters: Dict[str, Any] = None
    context: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DataResponse:
    """Response from real-time data sources"""

    query_id: str
    data: Dict[str, Any]
    source: str
    timestamp: datetime
    latency_ms: int
    success: bool
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["timestamp"] = self.timestamp.isoformat()
        return result


class ConversationalDataManager:
    """
    Manages real-time data integration for chat-based queries.

    PRD Compliance: Chat-only interface (Lines 158-161)
    - Executive reporting via chat interface
    - Strategic metrics through conversational queries
    - Trend analysis via natural language requests
    """

    def __init__(self):
        self.query_patterns = self._initialize_query_patterns()
        self.data_sources = self._initialize_data_sources()
        self.cache = {}
        self.cache_ttl = 300

        # Week 3: MCP Integration Manager for real data
        from .mcp_integration_manager import create_mcp_integration_manager

        self.mcp_manager = create_mcp_integration_manager()  # 5 minutes

    def _initialize_query_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize natural language query patterns"""
        return {
            # Sprint & Team Metrics
            r"(?i).*(?:show|get|display).*(?:current|latest).*sprint.*metric": {
                "type": QueryType.SPRINT_METRICS,
                "entities_pattern": r"(?:team|project)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            r"(?i).*(?:team|squad).*(?:performance|perform|metrics|status)": {
                "type": QueryType.TEAM_PERFORMANCE,
                "entities_pattern": r"(?:team|squad)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            # ROI & Investment Analysis
            r"(?i).*(?:roi|return|investment).*(?:analysis|metrics|tracking)": {
                "type": QueryType.ROI_ANALYSIS,
                "entities_pattern": r"(?:project|initiative)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            # Architecture & System Health
            r"(?i).*(?:architecture|system|platform).*(?:health|status|metrics)": {
                "type": QueryType.ARCHITECTURE_HEALTH,
                "entities_pattern": r"(?:service|system)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            # Design System Analytics
            r"(?i).*(?:design\s+system|component).*(?:adoption|usage|metrics)": {
                "type": QueryType.DESIGN_SYSTEM_STATUS,
                "entities_pattern": r"(?:component|library)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            # GitHub Activity
            r"(?i).*(?:github|git|repository).*(?:activity|metrics|stats)": {
                "type": QueryType.GITHUB_ACTIVITY,
                "entities_pattern": r"(?:repo|repository)\s+(\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
            # Repository-specific queries (ui-service-shell, velocity, development)
            r"(?i).*(?:velocity|development|ui-service-shell|procore/).*": {
                "type": QueryType.GITHUB_ACTIVITY,
                "entities_pattern": r"(?:ui-service-shell|procore/\w+)",
                "time_pattern": r"(?:last|past|current)\s+(\d+)\s+(\w+)",
            },
        }

    def _initialize_data_sources(self) -> Dict[str, Dict[str, Any]]:
        """Initialize data source configurations"""
        return {
            "jira": {
                "base_url": "https://api.atlassian.com",
                "endpoints": {
                    "sprint_metrics": "/rest/agile/1.0/board/{board_id}/sprint",
                    "team_performance": "/rest/api/3/search",
                },
                "auth_required": True,
                "rate_limit": 100,  # requests per minute
            },
            "github": {
                "base_url": "https://api.github.com",
                "endpoints": {
                    "repository_stats": "/repos/{owner}/{repo}/stats",
                    "pull_requests": "/repos/{owner}/{repo}/pulls",
                    "commits": "/repos/{owner}/{repo}/commits",
                },
                "auth_required": True,
                "rate_limit": 5000,  # requests per hour
            },
            "analytics": {
                "base_url": "https://analytics.internal.com",
                "endpoints": {
                    "user_metrics": "/api/v1/metrics/users",
                    "performance": "/api/v1/metrics/performance",
                },
                "auth_required": True,
                "rate_limit": 1000,  # requests per hour
            },
        }

    async def parse_conversational_query(
        self, query_text: str, context: Dict[str, Any] = None
    ) -> ConversationalQuery:
        """
        Parse natural language query into structured format.

        Args:
            query_text: Natural language query from chat
            context: Conversation context for better parsing

        Returns:
            ConversationalQuery: Structured query object
        """
        start_time = time.time()

        # Match query against patterns
        query_type = QueryType.GENERAL_ANALYTICS
        entities = []
        time_range = None
        filters = {}

        for pattern, config in self.query_patterns.items():
            if re.search(pattern, query_text):
                query_type = config["type"]

                # Extract entities (teams, projects, etc.)
                if "entities_pattern" in config:
                    entity_matches = re.findall(config["entities_pattern"], query_text)
                    entities.extend(entity_matches)

                # Extract time range
                if "time_pattern" in config:
                    time_match = re.search(config["time_pattern"], query_text)
                    if time_match:
                        time_range = f"{time_match.group(1)} {time_match.group(2)}"

                break

        # Apply context if available
        if context:
            if "previous_entities" in context:
                entities.extend(context["previous_entities"])
            if "default_time_range" in context and not time_range:
                time_range = context["default_time_range"]

        parse_time = (time.time() - start_time) * 1000
        logger.info(f"Query parsed in {parse_time:.2f}ms: {query_type.value}")

        return ConversationalQuery(
            query_type=query_type,
            entities=list(set(entities)),  # Remove duplicates
            time_range=time_range,
            filters=filters,
            context=context or {},
        )

    async def fetch_real_time_data(self, query: ConversationalQuery) -> DataResponse:
        """
        Fetch real-time data based on parsed query.

        Args:
            query: Structured conversational query

        Returns:
            DataResponse: Real-time data with metadata
        """
        start_time = time.time()
        query_id = f"{query.query_type.value}_{int(start_time)}"

        try:
            # Check cache first
            cache_key = self._generate_cache_key(query)
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if time.time() - cached_data["timestamp"] < self.cache_ttl:
                    latency_ms = (time.time() - start_time) * 1000
                    logger.info(f"Cache hit for {query_id}: {latency_ms:.2f}ms")
                    return DataResponse(
                        query_id=query_id,
                        data=cached_data["data"],
                        source="cache",
                        timestamp=datetime.now(),
                        latency_ms=int(latency_ms),
                        success=True,
                    )

            # Fetch fresh data based on query type
            data = await self._fetch_by_query_type(query)

            # Cache the result
            self.cache[cache_key] = {"data": data, "timestamp": time.time()}

            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Data fetched for {query_id}: {latency_ms:.2f}ms")

            return DataResponse(
                query_id=query_id,
                data=data,
                source=self._get_primary_source(query.query_type),
                timestamp=datetime.now(),
                latency_ms=int(latency_ms),
                success=True,
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Data fetch failed for {query_id}: {str(e)}")

            return DataResponse(
                query_id=query_id,
                data={},
                source="error",
                timestamp=datetime.now(),
                latency_ms=int(latency_ms),
                success=False,
                error_message=str(e),
            )

    async def _fetch_by_query_type(self, query: ConversationalQuery) -> Dict[str, Any]:
        """Fetch data based on specific query type"""

        if query.query_type == QueryType.SPRINT_METRICS:
            return await self._fetch_sprint_metrics(query)
        elif query.query_type == QueryType.TEAM_PERFORMANCE:
            return await self._fetch_team_performance(query)
        elif query.query_type == QueryType.ROI_ANALYSIS:
            return await self._fetch_roi_analysis(query)
        elif query.query_type == QueryType.ARCHITECTURE_HEALTH:
            return await self._fetch_architecture_health(query)
        elif query.query_type == QueryType.DESIGN_SYSTEM_STATUS:
            return await self._fetch_design_system_status(query)
        elif query.query_type == QueryType.GITHUB_ACTIVITY:
            return await self._fetch_github_activity(query)
        else:
            return await self._fetch_general_analytics(query)

    async def _fetch_sprint_metrics(self, query: ConversationalQuery) -> Dict[str, Any]:
        """Fetch current sprint metrics - Week 3: Real MCP Integration with Zero Setup Fallback"""

        # Week 3: Try real MCP integration first, graceful fallback to simulation
        try:
            # Attempt real Jira data via MCP Integration Manager
            mcp_result = await self.mcp_manager.fetch_jira_data(
                "sprint_metrics",
                {"team": query.entities[0] if query.entities else "Platform Team"},
            )

            if mcp_result.success and mcp_result.method == "mcp":
                # Real MCP data available!
                real_data = mcp_result.data.copy()
                real_data.update(
                    {
                        "✅_REAL_DATA": {
                            "data_source": "REAL JIRA DATA via MCP",
                            "server_used": mcp_result.server_used,
                            "method": "mcp_server",
                            "latency_ms": mcp_result.latency_ms,
                            "last_updated": "real-time",
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "connected",
                    }
                )
                return real_data

            elif mcp_result.success and mcp_result.method == "api_fallback":
                # API fallback data available
                api_data = mcp_result.data.copy()
                api_data.update(
                    {
                        "⚠️_API_FALLBACK_DATA": {
                            "data_source": "REAL JIRA DATA via REST API",
                            "notice": "MCP server unavailable, using REST API fallback",
                            "server_used": mcp_result.server_used,
                            "method": "rest_api",
                            "latency_ms": mcp_result.latency_ms,
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "api_fallback",
                    }
                )
                return api_data

        except Exception as e:
            # Log but don't fail - graceful degradation
            logger.warning(f"MCP integration failed, using simulation: {str(e)}")

        # ZERO SETUP POLICY: Always works - graceful fallback to simulation
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "Real Jira MCP server not available - using realistic sample data",
                "setup_prompt": "Ask me: 'How do I set up real Jira integration?' to connect your account",
                "integration_available": True,
                "mcp_status": "unavailable",
            },
            "sprint_name": "Sprint 42 (SIMULATED)",
            "team": query.entities[0] if query.entities else "Platform Team (SAMPLE)",
            "progress": {"completed": 8, "in_progress": 3, "todo": 2, "total": 13},
            "metrics": {
                "velocity": 34,
                "burndown_remaining": 15,
                "days_remaining": 3,
                "completion_rate": 0.62,
            },
            "risks": [
                "2 stories blocked by external dependency",
                "1 critical bug discovered in testing",
            ],
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real Jira data?'",
            "_integration_status": "simulation_fallback",
        }

    async def _fetch_team_performance(
        self, query: ConversationalQuery
    ) -> Dict[str, Any]:
        """Fetch team performance metrics - Week 3: Real MCP Integration with Zero Setup Fallback"""

        # Week 3: Try real MCP integration first, graceful fallback to simulation
        try:
            # Attempt real Jira data via MCP Integration Manager
            mcp_result = await self.mcp_manager.fetch_jira_data(
                "team_performance",
                {"team": query.entities[0] if query.entities else "UI Foundation Team"},
            )

            if mcp_result.success and mcp_result.method == "mcp":
                # Real MCP data available!
                real_data = mcp_result.data.copy()
                real_data.update(
                    {
                        "✅_REAL_DATA": {
                            "data_source": "REAL JIRA DATA via MCP",
                            "server_used": mcp_result.server_used,
                            "method": "mcp_server",
                            "latency_ms": mcp_result.latency_ms,
                            "last_updated": "real-time",
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "connected",
                    }
                )
                return real_data

            elif mcp_result.success and mcp_result.method == "api_fallback":
                # API fallback data available
                api_data = mcp_result.data.copy()
                api_data.update(
                    {
                        "⚠️_API_FALLBACK_DATA": {
                            "data_source": "REAL JIRA DATA via REST API",
                            "notice": "MCP server unavailable, using REST API fallback",
                            "server_used": mcp_result.server_used,
                            "method": "rest_api",
                            "latency_ms": mcp_result.latency_ms,
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "api_fallback",
                    }
                )
                return api_data

        except Exception as e:
            # Log but don't fail - graceful degradation
            logger.warning(f"MCP integration failed, using simulation: {str(e)}")

        # ZERO SETUP POLICY: Always works - graceful fallback to simulation
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "Real Jira MCP server not available - using realistic sample data",
                "setup_prompt": "Ask me: 'How do I set up real Jira integration?' to connect your account",
                "integration_available": True,
                "mcp_status": "unavailable",
            },
            "team": (
                query.entities[0] if query.entities else "UI Foundation Team (SAMPLE)"
            ),
            "period": query.time_range or "last 30 days",
            "metrics": {
                "story_completion_rate": 0.87,
                "average_cycle_time": 4.2,
                "defect_rate": 0.03,
                "code_review_time": 1.8,
            },
            "trends": {
                "velocity": "increasing",
                "quality": "stable",
                "satisfaction": "high",
            },
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real Jira data?'",
            "_integration_status": "simulation_fallback",
        }

    async def _fetch_roi_analysis(self, query: ConversationalQuery) -> Dict[str, Any]:
        """Fetch ROI analysis data"""
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "This is realistic sample data for demonstration purposes",
                "setup_prompt": "Connect to real analytics data for actual ROI metrics",
                "integration_available": True,
            },
            "project": (
                query.entities[0] if query.entities else "Platform Investment (SAMPLE)"
            ),
            "period": query.time_range or "YTD",
            "investment": {
                "total_cost": 450000,
                "development_cost": 320000,
                "operational_cost": 130000,
            },
            "returns": {
                "productivity_gains": 680000,
                "cost_savings": 240000,
                "revenue_impact": 150000,
            },
            "roi_metrics": {
                "roi_percentage": 2.4,
                "payback_period_months": 8,
                "npv": 820000,
            },
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real analytics data?'",
        }

    async def _fetch_architecture_health(
        self, query: ConversationalQuery
    ) -> Dict[str, Any]:
        """Fetch architecture health metrics"""
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "This is realistic sample data for demonstration purposes",
                "setup_prompt": "Connect to real monitoring systems for actual health metrics",
                "integration_available": True,
            },
            "system": (
                query.entities[0] if query.entities else "Platform Services (SAMPLE)"
            ),
            "health_score": 0.92,
            "services": {
                "api_gateway": {
                    "status": "healthy",
                    "response_time": 45,
                    "uptime": 0.999,
                },
                "user_service": {
                    "status": "healthy",
                    "response_time": 32,
                    "uptime": 0.998,
                },
                "data_service": {
                    "status": "warning",
                    "response_time": 78,
                    "uptime": 0.995,
                },
            },
            "metrics": {
                "average_response_time": 52,
                "error_rate": 0.002,
                "throughput": 1250,
                "availability": 0.997,
            },
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real monitoring data?'",
        }

    async def _fetch_design_system_status(
        self, query: ConversationalQuery
    ) -> Dict[str, Any]:
        """Fetch design system adoption metrics"""
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "This is realistic sample data for demonstration purposes",
                "setup_prompt": "Connect to real design system analytics for actual metrics",
                "integration_available": True,
            },
            "component": (
                query.entities[0] if query.entities else "Design System (SAMPLE)"
            ),
            "adoption": {
                "total_components": 45,
                "adopted_components": 38,
                "adoption_rate": 0.84,
            },
            "usage": {"active_teams": 12, "total_teams": 15, "implementations": 234},
            "health": {
                "consistency_score": 0.91,
                "maintenance_debt": "low",
                "update_frequency": "weekly",
            },
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real design system data?'",
        }

    async def _fetch_github_activity(
        self, query: ConversationalQuery
    ) -> Dict[str, Any]:
        """Fetch GitHub repository activity - Week 3: Real MCP Integration with Zero Setup Fallback"""

        # Week 3: Try real GitHub MCP integration first, graceful fallback to simulation
        try:
            # Attempt real GitHub data via MCP Integration Manager
            mcp_result = await self.mcp_manager.fetch_github_data(
                "repository_activity",
                {"repo": query.entities[0] if query.entities else "ai-leadership"},
            )

            if mcp_result.success and mcp_result.method == "mcp":
                # Real MCP data available!
                real_data = mcp_result.data.copy()
                real_data.update(
                    {
                        "✅_REAL_DATA": {
                            "data_source": "REAL GITHUB DATA via MCP",
                            "server_used": mcp_result.server_used,
                            "method": "mcp_server",
                            "latency_ms": mcp_result.latency_ms,
                            "last_updated": "real-time",
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "connected",
                    }
                )
                return real_data

            elif mcp_result.success and mcp_result.method == "api_fallback":
                # API fallback data available
                api_data = mcp_result.data.copy()
                api_data.update(
                    {
                        "⚠️_API_FALLBACK_DATA": {
                            "data_source": "REAL GITHUB DATA via REST API",
                            "notice": "GitHub MCP server unavailable, using REST API fallback",
                            "server_used": mcp_result.server_used,
                            "method": "rest_api",
                            "latency_ms": mcp_result.latency_ms,
                        },
                        "_data_authenticity": "REAL",
                        "_integration_status": "api_fallback",
                    }
                )
                return api_data

        except Exception as e:
            # Log but don't fail - graceful degradation
            logger.warning(f"GitHub MCP integration failed, using simulation: {str(e)}")

        # ZERO SETUP POLICY: Always works - graceful fallback to simulation
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "SIMULATED DATA - NOT REAL",
                "notice": "Real GitHub MCP server not available - using realistic sample data",
                "setup_prompt": "Ask me: 'How do I set up real GitHub integration?' to connect your account",
                "integration_available": True,
                "mcp_status": "unavailable",
            },
            "repository": (
                query.entities[0] if query.entities else "ai-leadership (SAMPLE)"
            ),
            "period": query.time_range or "last 7 days",
            "activity": {
                "commits": 23,
                "pull_requests": 8,
                "issues_opened": 3,
                "issues_closed": 5,
            },
            "contributors": {
                "active_contributors": 4,
                "new_contributors": 1,
                "top_contributor": "martin",
            },
            "_data_authenticity": "SIMULATED",
            "_setup_integration": "Ask me: 'How do I connect to real GitHub data?'",
            "_integration_status": "simulation_fallback",
        }

    async def _fetch_general_analytics(
        self, query: ConversationalQuery
    ) -> Dict[str, Any]:
        """Fetch general analytics data - Week 3: Enhanced with GitHub/Jira MCP routing"""

        # Week 3: Smart routing based on query content and context
        query_text = (
            str(query.context.get("original_query", "")).lower()
            if query.context
            else ""
        )
        entities_text = " ".join(query.entities).lower() if query.entities else ""
        combined_text = f"{query_text} {entities_text}".strip()

        # Check if this is actually a GitHub query that was misclassified
        github_keywords = [
            "github",
            "repository",
            "repo",
            "commit",
            "pull request",
            "contributor",
            "ui-service-shell",
            "procore",
        ]
        if any(keyword in combined_text for keyword in github_keywords):
            logger.info(
                f"Routing general analytics to GitHub MCP for query: {combined_text[:50]}..."
            )
            try:
                # Attempt real GitHub data via MCP Integration Manager
                mcp_result = await self.mcp_manager.fetch_github_data(
                    "repository_analytics",
                    {"query": combined_text, "entities": query.entities},
                )

                if mcp_result.success and mcp_result.method == "mcp":
                    # Real MCP data available!
                    real_data = mcp_result.data.copy()
                    real_data.update(
                        {
                            "✅_REAL_DATA": {
                                "data_source": "REAL GITHUB DATA via MCP",
                                "server_used": mcp_result.server_used,
                                "method": "mcp_server",
                                "latency_ms": mcp_result.latency_ms,
                                "last_updated": "real-time",
                            },
                            "_data_authenticity": "REAL",
                            "_integration_status": "connected",
                        }
                    )
                    return real_data

                elif mcp_result.success and mcp_result.method == "api_fallback":
                    # API fallback data available
                    api_data = mcp_result.data.copy()
                    api_data.update(
                        {
                            "⚠️_API_FALLBACK_DATA": {
                                "data_source": "REAL GITHUB DATA via REST API",
                                "notice": "GitHub MCP server unavailable, using REST API fallback",
                                "server_used": mcp_result.server_used,
                                "method": "rest_api",
                                "latency_ms": mcp_result.latency_ms,
                            },
                            "_data_authenticity": "REAL",
                            "_integration_status": "api_fallback",
                        }
                    )
                    return api_data

            except Exception as e:
                logger.warning(
                    f"GitHub MCP routing failed, using general response: {str(e)}"
                )

        # Check if this is actually a Jira/team query that was misclassified
        jira_keywords = [
            "team",
            "performance",
            "sprint",
            "velocity",
            "jira",
            "ui foundation",
            "quarter",
        ]
        if any(keyword in combined_text for keyword in jira_keywords):
            logger.info(
                f"Routing general analytics to Jira MCP for query: {combined_text[:50]}..."
            )
            try:
                # Attempt real Jira data via MCP Integration Manager
                mcp_result = await self.mcp_manager.fetch_jira_data(
                    "general_analytics",
                    {"query": combined_text, "entities": query.entities},
                )

                if mcp_result.success and mcp_result.method == "mcp":
                    # Real MCP data available!
                    real_data = mcp_result.data.copy()
                    real_data.update(
                        {
                            "✅_REAL_DATA": {
                                "data_source": "REAL JIRA DATA via MCP",
                                "server_used": mcp_result.server_used,
                                "method": "mcp_server",
                                "latency_ms": mcp_result.latency_ms,
                                "last_updated": "real-time",
                            },
                            "_data_authenticity": "REAL",
                            "_integration_status": "connected",
                        }
                    )
                    return real_data

                elif mcp_result.success and mcp_result.method == "api_fallback":
                    # API fallback data available
                    api_data = mcp_result.data.copy()
                    api_data.update(
                        {
                            "⚠️_API_FALLBACK_DATA": {
                                "data_source": "REAL JIRA DATA via REST API",
                                "notice": "Jira MCP server unavailable, using REST API fallback",
                                "server_used": mcp_result.server_used,
                                "method": "rest_api",
                                "latency_ms": mcp_result.latency_ms,
                            },
                            "_data_authenticity": "REAL",
                            "_integration_status": "api_fallback",
                        }
                    )
                    return api_data

            except Exception as e:
                logger.warning(
                    f"Jira MCP routing failed, using general response: {str(e)}"
                )

        # Default general analytics response with enhanced suggestions
        return {
            "🚨_SIMULATION_WARNING": {
                "data_source": "GENERAL ANALYTICS - LIMITED DATA",
                "notice": "This query didn't match specific data sources - try more specific requests",
                "setup_prompt": "For real data, ask about 'GitHub activity' or 'team performance'",
                "integration_available": True,
                "mcp_status": "routing_available",
            },
            "query_type": "general",
            "message": "General analytics query processed - consider more specific requests",
            "suggestions": [
                "Try: 'GitHub activity for ui-service-shell'",
                "Try: 'UI Foundation team performance this quarter'",
                "Try: 'Show sprint metrics for our team'",
                "Ask: 'How do I connect to real GitHub/Jira data?'",
            ],
            "_data_authenticity": "GENERAL",
            "_setup_integration": "Ask more specific questions about GitHub or Jira data",
            "_integration_status": "routing_fallback",
        }

    def _generate_cache_key(self, query: ConversationalQuery) -> str:
        """Generate cache key for query"""
        key_parts = [
            query.query_type.value,
            "_".join(sorted(query.entities)),
            query.time_range or "default",
        ]
        return "|".join(key_parts)

    def _get_primary_source(self, query_type: QueryType) -> str:
        """Get primary data source for query type"""
        source_mapping = {
            QueryType.SPRINT_METRICS: "jira",
            QueryType.TEAM_PERFORMANCE: "jira",
            QueryType.ROI_ANALYSIS: "analytics",
            QueryType.ARCHITECTURE_HEALTH: "analytics",
            QueryType.DESIGN_SYSTEM_STATUS: "analytics",
            QueryType.GITHUB_ACTIVITY: "github",
            QueryType.GENERAL_ANALYTICS: "internal",
        }
        return source_mapping.get(query_type, "unknown")

    async def process_conversational_query(
        self, query_text: str, context: Dict[str, Any] = None
    ) -> Tuple[ConversationalQuery, DataResponse]:
        """
        Complete pipeline: Parse query and fetch data.

        Args:
            query_text: Natural language query from chat
            context: Conversation context

        Returns:
            Tuple of parsed query and data response
        """
        # Parse the query
        parsed_query = await self.parse_conversational_query(query_text, context)

        # Fetch real-time data
        data_response = await self.fetch_real_time_data(parsed_query)

        return parsed_query, data_response


# Factory function for integration
def create_conversational_data_manager() -> ConversationalDataManager:
    """Create and configure ConversationalDataManager instance"""
    return ConversationalDataManager()
