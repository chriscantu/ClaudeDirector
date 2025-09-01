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
import aiohttp
from datetime import datetime

from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerType(Enum):
    """Types of MCP servers supported"""
    JIRA = "jira"
    GITHUB = "github"
    ANALYTICS = "analytics"


class MCPServerStatus(Enum):
    """Status of MCP server connections"""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    FALLBACK = "fallback"
    ERROR = "error"


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
        self.version = "1.0.0"

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
        }

        logger.info(f"MCP Integration Manager {self.version} initialized")

    def _initialize_mcp_servers(self) -> Dict[MCPServerType, List[MCPServerConfig]]:
        """Initialize MCP server configurations by priority"""

        return {
            MCPServerType.JIRA: [
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@quialorraine/jira-mcp-server",
                    version="1.0.3",
                    capabilities=["issue_management", "jql_search", "comments", "transitions"],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=1
                ),
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@answerai/jira-mcp",
                    version="1.0.2",
                    capabilities=["ai_integration", "issue_crud", "project_management"],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=2
                ),
                MCPServerConfig(
                    server_type=MCPServerType.JIRA,
                    package_name="@orengrinker/jira-mcp-server",
                    version="1.0.3",
                    capabilities=["comprehensive_management", "time_tracking", "boards"],
                    auth_required=True,
                    fallback_api_base="https://api.atlassian.com",
                    priority=3
                ),
            ],

            MCPServerType.GITHUB: [
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="@andrebuzeli/github-mcp-v2",
                    version="6.0.4",
                    capabilities=["releases", "ci_cd", "issues", "security", "analytics"],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=1
                ),
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="github-mcp-server",
                    version="1.8.7",
                    capabilities=["git_operations", "workflows", "cli_integration"],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=2
                ),
                MCPServerConfig(
                    server_type=MCPServerType.GITHUB,
                    package_name="@skhatri/github-mcp",
                    version="0.7.0",
                    capabilities=["pull_requests", "code_review", "api_integration"],
                    auth_required=True,
                    fallback_api_base="https://api.github.com",
                    priority=3
                ),
            ],
        }

    async def check_mcp_server_availability(self, server_type: MCPServerType) -> MCPServerStatus:
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
                logger.warning(f"MCP server check failed for {server.package_name}: {e}")
                continue

        # No MCP servers available, use fallback
        self.server_status[server_type] = MCPServerStatus.FALLBACK
        logger.info(f"No MCP servers available for {server_type.value}, using API fallback")
        return MCPServerStatus.FALLBACK

    async def _check_mcp_package_available(self, package_name: str) -> bool:
        """Check if an MCP package is available (installed or installable)"""

        try:
            # Check if package exists in npm registry
            process = await asyncio.create_subprocess_exec(
                "npm", "view", package_name, "version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0 and stdout:
                return True
            return False

        except Exception as e:
            logger.warning(f"Package check failed for {package_name}: {e}")
            return False

    async def fetch_jira_data(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
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

    async def fetch_github_data(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
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

    async def _fetch_via_jira_mcp(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
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
                data = {"message": f"Jira MCP query type '{query_type}' not implemented"}

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms)
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
                error_message=str(e)
            )

    async def _fetch_via_github_mcp(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
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
                data = {"message": f"GitHub MCP query type '{query_type}' not implemented"}

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms)
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used=server.package_name,
                method="mcp",
                latency_ms=int(latency_ms),
                error_message=str(e)
            )

    async def _fetch_via_jira_api(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
        """Fallback: Fetch data via Jira REST API"""

        start_time = time.time()

        try:
            # Simulate RESTful API call (would be actual HTTP requests in production)
            if query_type == "sprint_metrics":
                data = await self._simulate_jira_api_sprint_data(params)
            elif query_type == "team_performance":
                data = await self._simulate_jira_api_team_data(params)
            else:
                data = {"message": f"Jira API query type '{query_type}' not implemented"}

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used="jira_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms)
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used="jira_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
                error_message=str(e)
            )

    async def _fetch_via_github_api(self, query_type: str, params: Dict[str, Any] = None) -> MCPIntegrationResult:
        """Fallback: Fetch data via GitHub REST API"""

        start_time = time.time()

        try:
            # Simulate RESTful API call (would be actual HTTP requests in production)
            if query_type == "repository_activity":
                data = await self._simulate_github_api_activity_data(params)
            elif query_type == "pull_requests":
                data = await self._simulate_github_api_pr_data(params)
            else:
                data = {"message": f"GitHub API query type '{query_type}' not implemented"}

            latency_ms = (time.time() - start_time) * 1000

            return MCPIntegrationResult(
                success=True,
                data=data,
                server_used="github_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms)
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return MCPIntegrationResult(
                success=False,
                data={},
                server_used="github_rest_api",
                method="api_fallback",
                latency_ms=int(latency_ms),
                error_message=str(e)
            )

    # Simulation methods (replace with actual MCP/API calls in production)

    async def _simulate_jira_mcp_sprint_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
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
                "completion_rate": 0.69
            },
            "mcp_enhanced": {
                "jql_query_used": "project = PLAT AND sprint in openSprints()",
                "real_time_updates": True,
                "advanced_metrics": True
            },
            "source": "jira_mcp"
        }

    async def _simulate_jira_mcp_team_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate Jira MCP team performance data"""
        await asyncio.sleep(0.1)
        return {
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "period": "last 30 days",
            "metrics": {
                "story_completion_rate": 0.89,  # Better via MCP
                "average_cycle_time": 3.8,
                "defect_rate": 0.025,
                "code_review_time": 1.6
            },
            "mcp_enhanced": {
                "workflow_analysis": True,
                "predictive_insights": True,
                "team_collaboration_score": 0.92
            },
            "source": "jira_mcp"
        }

    async def _simulate_github_mcp_activity_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate GitHub MCP activity data"""
        await asyncio.sleep(0.1)
        return {
            "repository": params.get("repo", "ai-leadership") if params else "ai-leadership",
            "period": "last 7 days",
            "activity": {
                "commits": 28,  # Enhanced via MCP
                "pull_requests": 12,
                "issues_opened": 4,
                "issues_closed": 7
            },
            "mcp_enhanced": {
                "code_quality_metrics": {"test_coverage": 0.87, "complexity_score": "A"},
                "ci_cd_status": {"success_rate": 0.94, "avg_build_time": "4m 32s"},
                "security_insights": {"vulnerabilities": 0, "last_scan": "2025-08-31"}
            },
            "source": "github_mcp"
        }

    async def _simulate_jira_api_sprint_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
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
                "completion_rate": 0.62
            },
            "source": "jira_api_fallback"
        }

    async def _simulate_jira_api_team_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate Jira REST API team data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "team": params.get("team", "Platform Team") if params else "Platform Team",
            "period": "last 30 days",
            "metrics": {
                "story_completion_rate": 0.87,
                "average_cycle_time": 4.2,
                "defect_rate": 0.03,
                "code_review_time": 1.8
            },
            "source": "jira_api_fallback"
        }

    async def _simulate_github_api_activity_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate GitHub REST API activity data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "repository": params.get("repo", "ai-leadership") if params else "ai-leadership",
            "period": "last 7 days",
            "activity": {
                "commits": 23,
                "pull_requests": 8,
                "issues_opened": 3,
                "issues_closed": 5
            },
            "source": "github_api_fallback"
        }

    async def _simulate_github_mcp_pr_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate GitHub MCP PR data"""
        await asyncio.sleep(0.1)
        return {
            "repository": params.get("repo", "ai-leadership") if params else "ai-leadership",
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
                        "estimated_review_time": "15 minutes"
                    }
                }
            ],
            "source": "github_mcp"
        }

    async def _simulate_github_api_pr_data(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate GitHub REST API PR data (fallback)"""
        await asyncio.sleep(0.2)
        return {
            "repository": params.get("repo", "ai-leadership") if params else "ai-leadership",
            "pull_requests": [
                {
                    "number": 109,
                    "title": "Phase 7 Week 2: Real-Time Conversational Analytics",
                    "state": "open",
                    "author": "martin",
                    "created_at": "2025-08-31T19:00:00Z"
                }
            ],
            "source": "github_api_fallback"
        }

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
            (self.integration_metrics["avg_latency_ms"] * (total_requests - 1) + latency_ms) / total_requests
        )

        if success:
            current_successes = self.integration_metrics["success_rate"] * (total_requests - 1)
            self.integration_metrics["success_rate"] = (current_successes + 1) / total_requests
        else:
            current_successes = self.integration_metrics["success_rate"] * (total_requests - 1)
            self.integration_metrics["success_rate"] = current_successes / total_requests

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
                        "capabilities": server.capabilities
                    }
                    for server in servers
                ]
                for server_type, servers in self.mcp_servers.items()
            },
            "prd_compliance": {
                "chat_only_interface": True,
                "fallback_strategy": True,
                "latency_target_met": self.integration_metrics["avg_latency_ms"] < 5000
            }
        }


# Factory function
def create_mcp_integration_manager() -> MCPIntegrationManager:
    """Create and configure MCP Integration Manager"""
    return MCPIntegrationManager()
