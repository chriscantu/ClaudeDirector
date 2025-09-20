#!/usr/bin/env python3
"""
MCP Integration Manager
Phase 7 Week 3 - Native MCP Server Integration

🏗️ Martin | Platform Architecture - MCP server orchestration
🤖 Berny | AI/ML Engineering - Performance optimization
💼 Alvaro | Business Strategy - ROI tracking integration

Manages integration with external MCP servers (Jira, GitHub) with fallback to RESTful APIs.
Maintains PRD compliance with chat-only interface while leveraging native MCP protocols.
"""

import asyncio
import json
import time
import logging
import subprocess
import os
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

# 🚀 ENHANCEMENT FIX: Make aiohttp import optional for basic MCP integration compatibility
try:
    import aiohttp

    AIOHTTP_AVAILABLE = True
except ImportError:
    aiohttp = None
    AIOHTTP_AVAILABLE = False

from datetime import datetime

from .constants import MCPServerConstants

# 🚀 ENHANCEMENT: Import for Claude Code MCP server integration
try:
    # Try relative imports first (for package context)
    from ..transparency.real_mcp_integration import RealMCPIntegrationHelper
    from ..transparency.integrated_transparency import TransparencyContext
    from ..transparency.persona_integration import TransparentPersonaManager

    CLAUDE_CODE_MCP_AVAILABLE = True
except ImportError:
    try:
        # Fallback to absolute imports (for Claude Code context)
        from transparency.real_mcp_integration import RealMCPIntegrationHelper
        from transparency.integrated_transparency import TransparencyContext
        from transparency.persona_integration import TransparentPersonaManager

        CLAUDE_CODE_MCP_AVAILABLE = True
    except ImportError:
        # Graceful fallback if Claude Code MCP servers not available
        RealMCPIntegrationHelper = None
        TransparencyContext = None
        TransparentPersonaManager = None
        CLAUDE_CODE_MCP_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerType(Enum):
    """Types of MCP servers supported"""

    JIRA = "jira"
    GITHUB = "github"
    ANALYTICS = "analytics"
    # 🚀 ENHANCEMENT: Add Claude Code MCP servers
    CONTEXT7 = "context7"
    SEQUENTIAL = "sequential"
    MAGIC = "magic"
    PLAYWRIGHT = "playwright"


class MCPServerStatus(Enum):
    """Status of MCP server connections"""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    FALLBACK = "fallback"
    ERROR = "error"


# 🚀 ENHANCEMENT: Query pattern classification for intelligent routing
class QueryPattern(Enum):
    """Types of query patterns for intelligent MCP server routing"""

    STRATEGIC_ANALYSIS = "strategic_analysis"  # → Sequential primary
    TECHNICAL_QUESTION = "technical_question"  # → Context7 primary
    UI_COMPONENT = "ui_component"  # → Magic primary
    TESTING_AUTOMATION = "testing_automation"  # → Playwright primary
    # 🚀 PHASE 1 EXTENSION: Add retrospective pattern (REUSE existing routing infrastructure)
    RETROSPECTIVE_ANALYSIS = "retrospective_analysis"  # → Sequential primary
    GENERAL_QUERY = "general_query"  # → Sequential primary


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server"""

    server_type: MCPServerType
    package_name: str
    version: str
    capabilities: List[str]
    auth_required: bool
    fallback_api_base: str
    priority: int = 1  # Lower number = higher priority


@dataclass
class MCPIntegrationResult:
    """Result of MCP server integration call"""

    success: bool
    data: Dict[str, Any]
    server_used: str
    method: str  # "mcp" or "api_fallback"
    latency_ms: int
    error_message: Optional[str] = None


class MCPIntegrationManager:
    """
    Manages integration with external MCP servers for real-time data.

    Phase 7 Week 3: Native MCP Server Integration
    - Prioritizes MCP servers when available
    - Falls back to RESTful APIs when MCP unavailable
    - Maintains <5s latency requirement from PRD
    """

    def __init__(self):
        self.name = "mcp-integration-manager"
        self.version = "1.1.0"  # 🚀 ENHANCEMENT: Version bump for intelligent routing

        # MCP Server configurations (prioritized)
        self.mcp_servers = self._initialize_mcp_servers()

        # Server status tracking
        self.server_status = {}

        # Performance metrics
        self.integration_metrics = {
            "total_requests": 0,
            "mcp_requests": 0,
            "fallback_requests": 0,
            "avg_latency_ms": 0.0,
            "success_rate": 0.0,
            "intelligent_routing_requests": 0,  # 🚀 ENHANCEMENT: Track intelligent routing usage
        }

        # 🚀 ENHANCEMENT: Initialize Claude Code MCP integration if available
        self.claude_code_mcp_helper = None
        if CLAUDE_CODE_MCP_AVAILABLE:
            try:
                self._initialize_claude_code_mcp()
                logger.info("Claude Code MCP integration initialized successfully")
            except Exception as e:
                logger.warning(f"Claude Code MCP initialization failed: {e}")

        # 🚀 ENHANCEMENT: Session-scoped performance tracking for optimization
        self.session_performance = {}

        logger.info(
            f"MCP Integration Manager {self.version} initialized with intelligent routing"
        )

    def _initialize_claude_code_mcp(self):
        """🚀 ENHANCEMENT: Initialize Claude Code MCP server integration"""
        if not CLAUDE_CODE_MCP_AVAILABLE:
            return

        # Initialize transparency system for MCP integration
        from transparency.integrated_transparency import IntegratedTransparencySystem

        transparency_system = IntegratedTransparencySystem(config={"debug_mode": False})
        transparency_context = TransparencyContext(persona="diego")
        persona_manager = TransparentPersonaManager(transparency_system)

        # Create fallback MCP client if real client not available
        try:
            from ..integration.unified_bridge import MCPUseClient

            mcp_client = MCPUseClient()
        except ImportError:
            # Use fallback client class when MCP infrastructure not available
            class FallbackMCPClient:
                def __init__(self):
                    self.is_available = False

                def is_server_available(self, server_name: str) -> bool:
                    return False

                async def call_server(self, server_name: str, *args, **kwargs):
                    return {
                        "success": False,
                        "error": "MCP client not available",
                        "fallback": True,
                    }

            mcp_client = FallbackMCPClient()

        # Initialize Claude Code MCP integration helper with proper client
        self.claude_code_mcp_helper = RealMCPIntegrationHelper(
            transparency_context=transparency_context,
            persona_manager=persona_manager,
            mcp_client=mcp_client,
        )

    def _initialize_mcp_servers(self) -> Dict[MCPServerType, List[MCPServerConfig]]:
        """Initialize MCP server configurations by priority"""

        return {
            MCPServerType.JIRA: [
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@quialorraine/jira-mcp-server",
                    version="1.0.3",
                    capabilities=[
                        "issue_management",
                        "jql_search",
                        "comments",
                        "transitions",
                    ],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=1,
                ),
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@answerai/jira-mcp",
                    version="1.0.2",
                    capabilities=["ai_integration", "issue_crud", "project_management"],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=2,
                ),
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@orengrinker/jira-mcp-server",
                    version="1.0.3",
                    capabilities=[
                        "comprehensive_management",
                        "time_tracking",
                        "boards",
                    ],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=3,
                ),
            ],
            MCPServerType.GITHUB: [
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="@andrebuzeli/github-mcp-v2",
                    version="6.0.4",
                    capabilities=[
                        "releases",
                        "ci_cd",
                        "issues",
                        "security",
                        "analytics",
                    ],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=1,
                ),
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="github-mcp-server",
                    version="1.8.7",
                    capabilities=["git_operations", "workflows", "cli_integration"],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=2,
                ),
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="@skhatri/github-mcp",
                    version="0.7.0",
                    capabilities=["pull_requests", "code_review", "api_integration"],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=3,
                ),
            ],
        }

    async def check_mcp_server_availability(
        self, server_type: MCPServerType
    ) -> MCPServerStatus:
        """Check if MCP servers are available for the given type"""

        servers = self.mcp_servers.get(server_type, [])
        if not servers:
            return MCPServerStatus.UNAVAILABLE

        # Check highest priority server first
        for server in sorted(servers, key=lambda s: s.priority):
            try:
                # Try to detect if the MCP server package is available
                result = await self._check_mcp_package_available(server.package_name)
                if result:
                    self.server_status[server_type] = MCPServerStatus.AVAILABLE
                    logger.info(f"MCP server available: {server.package_name}")
                    return MCPServerStatus.AVAILABLE
            except Exception as e:
                logger.warning(
                    f"MCP server check failed for {server.package_name}: {e}"
                )
                continue

        # No MCP servers available, use fallback
        self.server_status[server_type] = MCPServerStatus.FALLBACK
        logger.info(
            f"No MCP servers available for {server_type.value}, using API fallback"
        )
        return MCPServerStatus.FALLBACK

    async def _check_mcp_package_available(self, package_name: str) -> bool:
        """Check if an MCP package is available (installed or installable)"""

        try:
            # Check if package exists in npm registry
            process = await asyncio.create_subprocess_exec(
                "npm",
                "view",
                package_name,
                "version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0 and stdout:
                return True
            return False

        except Exception as e:
            logger.warning(f"Package check failed for {package_name}: {e}")
            return False

    async def fetch_jira_data(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fetch Jira data using MCP server or API fallback"""

        start_time = time.time()
        server_status = await self.check_mcp_server_availability(MCPServerType.JIRA)

        if server_status == MCPServerStatus.AVAILABLE:
            try:
                result = await self._fetch_via_jira_mcp(query_type, params)
                if result.success:
                    self._update_metrics("mcp", time.time() - start_time, True)
                    return result
            except Exception as e:
                logger.warning(f"Jira MCP failed, falling back to API: {e}")

        # Fallback to RESTful API
        result = await self._fetch_via_jira_api(query_type, params)
        self._update_metrics("api_fallback", time.time() - start_time, result.success)
        return result

    async def fetch_github_data(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fetch GitHub data using MCP server or API fallback"""

        start_time = time.time()
        server_status = await self.check_mcp_server_availability(MCPServerType.GITHUB)

        if server_status == MCPServerStatus.AVAILABLE:
            try:
                result = await self._fetch_via_github_mcp(query_type, params)
                if result.success:
                    self._update_metrics("mcp", time.time() - start_time, True)
                    return result
            except Exception as e:
                logger.warning(f"GitHub MCP failed, falling back to API: {e}")

        # Fallback to RESTful API
        result = await self._fetch_via_github_api(query_type, params)
        self._update_metrics("api_fallback", time.time() - start_time, result.success)
        return result

    async def _fetch_via_jira_mcp(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fetch data via Jira MCP server"""

        start_time = time.time()

        # Get highest priority available Jira MCP server
        jira_servers = self.mcp_servers[MCPServerType.JIRA]
        server = sorted(jira_servers, key=lambda s: s.priority)[0]

        try:
            # Simulate MCP server call (would be actual MCP protocol in production)
            if query_type == "sprint_metrics":
                data = await self._simulate_jira_mcp_sprint_data(params)
            elif query_type == "team_performance":
                data = await self._simulate_jira_mcp_team_data(params)
            else:
                data = {
                    "message": f"Jira MCP query type '{query_type}' not implemented"
                }

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
                error_message=str(e),
            )

    async def _fetch_via_github_mcp(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fetch data via GitHub MCP server"""

        start_time = time.time()

        # Get highest priority available GitHub MCP server
        github_servers = self.mcp_servers[MCPServerType.GITHUB]
        server = sorted(github_servers, key=lambda s: s.priority)[0]

        try:
            # Simulate MCP server call (would be actual MCP protocol in production)
            if query_type == "repository_activity":
                data = await self._simulate_github_mcp_activity_data(params)
            elif query_type == "pull_requests":
                data = await self._simulate_github_mcp_pr_data(params)
            else:
                data = {
                    "message": f"GitHub MCP query type '{query_type}' not implemented"
                }

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
                error_message=str(e),
            )

    async def _fetch_via_jira_api(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fallback: Fetch data via Jira REST API"""

        start_time = time.time()

        try:
            # Simulate RESTful API call (would be actual HTTP requests in production)
            if query_type == "sprint_metrics":
                data = await self._simulate_jira_api_sprint_data(params)
            elif query_type == "team_performance":
                data = await self._simulate_jira_api_team_data(params)
            else:
                data = {
                    "message": f"Jira API query type '{query_type}' not implemented"
                }

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used="jira_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used="jira_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
                error_message=str(e),
            )

    async def _fetch_via_github_api(
        self, query_type: str, params: Dict[str, Any] = None
    ) -> MCPIntegrationResult:
        """Fallback: Fetch data via GitHub REST API"""

        start_time = time.time()

        try:
            # Simulate RESTful API call (would be actual HTTP requests in production)
            if query_type == "repository_activity":
                data = await self._simulate_github_api_activity_data(params)
            elif query_type == "pull_requests":
                data = await self._simulate_github_api_pr_data(params)
            else:
                data = {
                    "message": f"GitHub API query type '{query_type}' not implemented"
                }

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used="github_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used="github_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
                error_message=str(e),
            )

    # Simulation methods (replace with actual MCP/API calls in production)

    async def _simulate_jira_mcp_sprint_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate Jira MCP sprint data (enhanced with MCP capabilities)"""
        await asyncio.sleep(0.1)  # Simulate MCP call latency
        return {
            "sprint_name": "Sprint 42",
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "progress": {"completed": 9, "in_progress": 2, "todo": 2, "total": 13},
            "metrics": {
                "velocity": 36,  # Slightly better via MCP
                "burndown_remaining": 12,
                "days_remaining": 3,
                "completion_rate": 0.69,
            },
            "mcp_enhanced": {
                "jql_query_used": "project = PLAT AND sprint in openSprints()",
                "real_time_updates": True,
                "advanced_metrics": True,
            },
            "source": "jira_mcp",
        }

    async def _simulate_jira_mcp_team_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate Jira MCP team performance data"""
        await asyncio.sleep(0.1)
        return {
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "period": "last 30 days",
            "metrics": {
                "story_completion_rate": 0.89,  # Better via MCP
                "average_cycle_time": 3.8,
                "defect_rate": 0.025,
                "code_review_time": 1.6,
            },
            "mcp_enhanced": {
                "workflow_analysis": True,
                "predictive_insights": True,
                "team_collaboration_score": 0.92,
            },
            "source": "jira_mcp",
        }

    async def _simulate_github_mcp_activity_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate GitHub MCP activity data"""
        await asyncio.sleep(0.1)
        return {
            "repository": (
                params.get("repo", "ai-leadership") if params else "ai-leadership"
            ),
            "period": "last 7 days",
            "activity": {
                "commits": 28,  # Enhanced via MCP
                "pull_requests": 12,
                "issues_opened": 4,
                "issues_closed": 7,
            },
            "mcp_enhanced": {
                "code_quality_metrics": {
                    "test_coverage": 0.87,
                    "complexity_score": "A",
                },
                "ci_cd_status": {"success_rate": 0.94, "avg_build_time": "4m 32s"},
                "security_insights": {"vulnerabilities": 0, "last_scan": "2025-08-31"},
            },
            "source": "github_mcp",
        }

    async def _simulate_jira_api_sprint_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate Jira REST API sprint data (fallback)"""
        await asyncio.sleep(0.2)  # Slightly slower than MCP
        return {
            "sprint_name": "Sprint 42",
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "progress": {"completed": 8, "in_progress": 3, "todo": 2, "total": 13},
            "metrics": {
                "velocity": 34,
                "burndown_remaining": 15,
                "days_remaining": 3,
                "completion_rate": 0.62,
            },
            "source": "jira_api_fallback",
        }

    async def _simulate_jira_api_team_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate Jira REST API team data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "period": "last 30 days",
            "metrics": {
                "story_completion_rate": 0.87,
                "average_cycle_time": 4.2,
                "defect_rate": 0.03,
                "code_review_time": 1.8,
            },
            "source": "jira_api_fallback",
        }

    async def _simulate_github_api_activity_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate GitHub REST API activity data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "repository": (
                params.get("repo", "ai-leadership") if params else "ai-leadership"
            ),
            "period": "last 7 days",
            "activity": {
                "commits": 23,
                "pull_requests": 8,
                "issues_opened": 3,
                "issues_closed": 5,
            },
            "source": "github_api_fallback",
        }

    async def _simulate_github_mcp_pr_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate GitHub MCP PR data"""
        await asyncio.sleep(0.1)
        return {
            "repository": (
                params.get("repo", "ai-leadership") if params else "ai-leadership"
            ),
            "pull_requests": [
                {
                    "number": 109,
                    "title": "Phase 7 Week 2: Real-Time Conversational Analytics",
                    "state": "open",
                    "author": "martin",
                    "created_at": "2025-08-31T19:00:00Z",
                    "mcp_insights": {
                        "complexity_score": "medium",
                        "review_readiness": 0.95,
                        "estimated_review_time": "15 minutes",
                    },
                }
            ],
            "source": "github_mcp",
        }

    async def _simulate_github_api_pr_data(
        self, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Simulate GitHub REST API PR data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "repository": (
                params.get("repo", "ai-leadership") if params else "ai-leadership"
            ),
            "pull_requests": [
                {
                    "number": 109,
                    "title": "Phase 7 Week 2: Real-Time Conversational Analytics",
                    "state": "open",
                    "author": "martin",
                    "created_at": "2025-08-31T19:00:00Z",
                }
            ],
            "source": "github_api_fallback",
        }

    # 🚀 ENHANCEMENT: Intelligent Query Routing Methods

    async def route_query_intelligently(
        self, query: str, context: Optional[Dict] = None
    ) -> MCPIntegrationResult:
        """
        🚀 ENHANCEMENT: Route query to optimal MCP server with intelligent pattern detection

        Leverages existing server connection patterns while adding:
        - Simple query pattern detection (strategic vs technical vs UI)
        - Intelligent server selection based on query characteristics
        - Fallback to secondary server if primary fails
        - Session-scoped performance tracking
        """
        start_time = time.time()
        self.integration_metrics["intelligent_routing_requests"] += 1

        # Classify query pattern using simple rule-based approach
        query_pattern = self._classify_query_pattern(query)

        # Select optimal Claude Code MCP server for pattern
        primary_server = self._select_optimal_server(query_pattern)

        if primary_server and self.claude_code_mcp_helper:
            try:
                # Route to Claude Code MCP server
                response = await self._query_claude_code_mcp_server(
                    primary_server, query, context
                )

                # Track performance for session optimization
                response_time = time.time() - start_time
                self._track_performance(primary_server, response_time)

                return MCPIntegrationResult(
                    success=True,
                    data=response,
                    server_used=primary_server.value,
                    method="claude_code_mcp",
                    latency_ms=int(response_time * 1000),
                )

            except Exception as e:
                logger.warning(
                    f"Primary Claude Code MCP server {primary_server.value} failed: {e}"
                )

                # Try fallback server
                fallback_server = self._get_fallback_server(primary_server)
                if fallback_server and fallback_server != primary_server:
                    try:
                        response = await self._query_claude_code_mcp_server(
                            fallback_server, query, context
                        )
                        response_time = time.time() - start_time

                        return MCPIntegrationResult(
                            success=True,
                            data=response,
                            server_used=fallback_server.value,
                            method="claude_code_mcp_fallback",
                            latency_ms=int(response_time * 1000),
                        )
                    except Exception as fallback_error:
                        logger.warning(
                            f"Fallback server {fallback_server.value} also failed: {fallback_error}"
                        )

        # Final fallback: return simple response indicating pattern detected
        response_time = time.time() - start_time
        return MCPIntegrationResult(
            success=True,
            data={
                "message": f"Query pattern '{query_pattern.value}' detected",
                "recommended_server": (
                    primary_server.value if primary_server else "sequential"
                ),
                "claude_code_mcp_available": CLAUDE_CODE_MCP_AVAILABLE,
                "query_sample": query[:100] + "..." if len(query) > 100 else query,
            },
            server_used="pattern_detection",
            method="fallback",
            latency_ms=int(response_time * 1000),
        )

    def _classify_query_pattern(self, query: str) -> QueryPattern:
        """Simple rule-based query pattern classification - no ML dependencies."""
        query_lower = query.lower()

        # 🚀 PHASE 1 EXTENSION: Add retrospective pattern detection (REUSE existing classification logic)
        retrospective_keywords = [
            "retrospective",
            "reflection",
            "weekly review",
            "progress",
            "improvement",
            "rating",
            "what did i",
            "how could i",
            "scale of 1",
        ]
        if any(keyword in query_lower for keyword in retrospective_keywords):
            return QueryPattern.RETROSPECTIVE_ANALYSIS

        # Strategic analysis patterns
        strategic_keywords = [
            "strategy",
            "roadmap",
            "planning",
            "decision",
            "business",
            "roi",
            "investment",
            "team",
            "organization",
        ]
        if any(keyword in query_lower for keyword in strategic_keywords):
            return QueryPattern.STRATEGIC_ANALYSIS

        # UI component patterns
        ui_keywords = [
            "component",
            "design",
            "ui",
            "interface",
            "button",
            "form",
            "layout",
            "style",
            "css",
        ]
        if any(keyword in query_lower for keyword in ui_keywords):
            return QueryPattern.UI_COMPONENT

        # Technical documentation patterns
        tech_keywords = [
            "documentation",
            "docs",
            "api",
            "library",
            "framework",
            "guide",
            "tutorial",
            "reference",
        ]
        if any(keyword in query_lower for keyword in tech_keywords):
            return QueryPattern.TECHNICAL_QUESTION

        # Testing automation patterns
        test_keywords = [
            "test",
            "testing",
            "automation",
            "e2e",
            "playwright",
            "browser",
            "visual",
        ]
        if any(keyword in query_lower for keyword in test_keywords):
            return QueryPattern.TESTING_AUTOMATION

        # Default to general query (Sequential server)
        return QueryPattern.GENERAL_QUERY

    def _select_optimal_server(self, pattern: QueryPattern) -> Optional[MCPServerType]:
        """Select best Claude Code MCP server for query pattern."""
        server_mapping = {
            QueryPattern.STRATEGIC_ANALYSIS: MCPServerType.SEQUENTIAL,
            QueryPattern.TECHNICAL_QUESTION: MCPServerType.CONTEXT7,
            QueryPattern.UI_COMPONENT: MCPServerType.MAGIC,
            QueryPattern.TESTING_AUTOMATION: MCPServerType.PLAYWRIGHT,
            # 🚀 PHASE 1 EXTENSION: Add retrospective routing (REUSE existing server mapping)
            QueryPattern.RETROSPECTIVE_ANALYSIS: MCPServerType.SEQUENTIAL,
            QueryPattern.GENERAL_QUERY: MCPServerType.SEQUENTIAL,
        }
        return server_mapping.get(pattern)

    def _get_fallback_server(self, primary: MCPServerType) -> Optional[MCPServerType]:
        """Get fallback server if primary fails."""
        fallback_mapping = {
            MCPServerType.SEQUENTIAL: MCPServerType.CONTEXT7,
            MCPServerType.CONTEXT7: MCPServerType.SEQUENTIAL,
            MCPServerType.MAGIC: MCPServerType.CONTEXT7,
            MCPServerType.PLAYWRIGHT: MCPServerType.SEQUENTIAL,
        }
        return fallback_mapping.get(primary)

    async def _query_claude_code_mcp_server(
        self, server_type: MCPServerType, query: str, context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Query Claude Code MCP server using existing integration patterns."""
        if not self.claude_code_mcp_helper:
            raise Exception("Claude Code MCP helper not initialized")

        # Use existing MCP integration helper to call server
        capability = (
            "strategic_analysis"
            if server_type == MCPServerType.SEQUENTIAL
            else "query_processing"
        )

        response = await self.claude_code_mcp_helper.call_mcp_server(
            server_name=server_type.value,
            capability=capability,
            query=query,
            context=context or {},
        )

        return {
            "server_type": server_type.value,
            "response": response,
            "enhanced": True,
            "timestamp": time.time(),
        }

    def _track_performance(
        self, server_type: MCPServerType, response_time: float
    ) -> None:
        """Track session-scoped performance for optimization."""
        server_key = server_type.value

        if server_key not in self.session_performance:
            self.session_performance[server_key] = {
                "total_calls": 0,
                "total_time": 0.0,
                "avg_response_time": 0.0,
                "success_rate": 1.0,
            }

        perf = self.session_performance[server_key]
        perf["total_calls"] += 1
        perf["total_time"] += response_time
        perf["avg_response_time"] = perf["total_time"] / perf["total_calls"]

    def _update_metrics(self, method: str, latency_seconds: float, success: bool):
        """Update integration performance metrics"""

        self.integration_metrics["total_requests"] += 1

        if method == "mcp":
            self.integration_metrics["mcp_requests"] += 1
        else:
            self.integration_metrics["fallback_requests"] += 1

        # Update running averages
        total_requests = self.integration_metrics["total_requests"]
        latency_ms = latency_seconds * 1000

        self.integration_metrics["avg_latency_ms"] = (
            self.integration_metrics["avg_latency_ms"] * (total_requests - 1)
            + latency_ms
        ) / total_requests

        if success:
            current_successes = self.integration_metrics["success_rate"] * (
                total_requests - 1
            )
            self.integration_metrics["success_rate"] = (
                current_successes + 1
            ) / total_requests
        else:
            current_successes = self.integration_metrics["success_rate"] * (
                total_requests - 1
            )
            self.integration_metrics["success_rate"] = (
                current_successes / total_requests
            )

    async def get_integration_health(self) -> Dict[str, Any]:
        """Get MCP integration health and metrics"""

        return {
            "manager_name": self.name,
            "version": self.version,
            "server_status": {
                server_type.value: status.value
                for server_type, status in self.server_status.items()
            },
            "metrics": self.integration_metrics,
            "available_servers": {
                server_type.value: [
                    {
                        "package": server.package_name,
                        "version": server.version,
                        "priority": server.priority,
                        "capabilities": server.capabilities,
                    }
                    for server in servers
                ]
                for server_type, servers in self.mcp_servers.items()
            },
            "prd_compliance": {
                "chat_only_interface": True,
                "fallback_strategy": True,
                "latency_target_met": self.integration_metrics["avg_latency_ms"] < 5000,
            },
            # 🚀 ENHANCEMENT: Claude Code MCP integration status
            "claude_code_mcp": {
                "available": CLAUDE_CODE_MCP_AVAILABLE,
                "helper_initialized": self.claude_code_mcp_helper is not None,
                "supported_servers": ["context7", "sequential", "magic", "playwright"],
                "session_performance": self.session_performance,
            },
            # 🚀 ENHANCEMENT: Intelligent routing metrics
            "intelligent_routing": {
                "enabled": True,
                "requests_routed": self.integration_metrics.get(
                    "intelligent_routing_requests", 0
                ),
                "supported_patterns": [pattern.value for pattern in QueryPattern],
            },
        }


# Factory function
def create_mcp_integration_manager() -> MCPIntegrationManager:
    """Create and configure MCP Integration Manager"""
    return MCPIntegrationManager()
