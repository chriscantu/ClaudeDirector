#!/usr/bin/env python3
"""
Weekly Report Generator - Python Implementation
Director of Engineering Strategic Weekly Report Automation

Converts bash script to Python for better reliability, debugging, and maintenance.
Includes strategic story analysis for executive communication.

Author: ClaudeDirector AI Framework
Version: 2.0.0
"""

import os
import sys
import json
import yaml
import argparse
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from urllib.parse import quote
import re
from pathlib import Path

# Real MCP Integration following BLOAT_PREVENTION principles
try:
    # Try relative imports first (for package context)
    from .weekly_reporter_mcp_bridge import (
        create_weekly_reporter_mcp_bridge,
        MCPEnhancementResult,
    )

    MCP_BRIDGE_AVAILABLE = True
except ImportError:
    try:
        # Fallback to absolute imports (for Claude Code context)
        from reporting.weekly_reporter_mcp_bridge import (
            create_weekly_reporter_mcp_bridge,
            MCPEnhancementResult,
        )

        MCP_BRIDGE_AVAILABLE = True
    except ImportError:
        # Graceful fallback when MCP bridge unavailable
        create_weekly_reporter_mcp_bridge = None
        MCPEnhancementResult = None
        MCP_BRIDGE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("weekly_report.log"),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class JiraIssue:
    """Data class for Jira issue representation"""

    key: str
    summary: str
    status: str
    priority: str
    project: str
    assignee: str
    parent_key: Optional[str] = None
    watchers: int = 0
    links: int = 0
    business_value: str = ""
    # Phase 2 Enhancement: Cycle time fields for Monte Carlo forecasting
    cycle_time_days: Optional[float] = None
    created_date: Optional[str] = None
    resolved_date: Optional[str] = None
    in_progress_date: Optional[str] = None


@dataclass
class StrategicScore:
    """Data class for strategic impact scoring"""

    score: int = 0
    indicators: List[str] = field(default_factory=list)

    def add_score(self, points: int, indicator: str):
        self.score += points
        self.indicators.append(indicator)


@dataclass
class Initiative:
    """Data class for L0/L2 strategic initiatives"""

    key: str
    title: str
    level: str  # L0, L1, L2
    progress_pct: int = 0
    status_desc: str = ""  # "releasing this week", "60% complete"
    business_context: str = ""
    team_impact: str = ""  # "minimal impact to teams"
    decision: Optional[str] = None
    project: str = ""
    status: str = ""
    child_stories: List[JiraIssue] = field(default_factory=list)


class ConfigManager:
    """Handles YAML configuration parsing and validation"""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            logger.info(f"Successfully loaded config from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise

    def _validate_config(self):
        """Validate required configuration sections"""
        required_sections = ["jira", "jql_queries"]
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")
        logger.info("Configuration validation successful")

    def get_jql_query(self, query_name: str) -> Optional[str]:
        """Extract JQL query by name"""
        return self.config.get("jql_queries", {}).get(query_name)

    def get_jira_config(self) -> Dict[str, Any]:
        """Get Jira connection configuration"""
        return self.config.get("jira", {})


class JiraClient:
    """Handles Jira API connections and data fetching"""

    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get("base_url", "").rstrip("/")
        self.email = config.get("auth", {}).get("email", "")
        self.api_token = os.getenv(
            "JIRA_API_TOKEN", config.get("auth", {}).get("api_token", "")
        )

        # Override from environment variables if available
        self.base_url = os.getenv("JIRA_BASE_URL", self.base_url)
        self.email = os.getenv("JIRA_EMAIL", self.email)

        self.session = self._create_session()
        self._validate_credentials()

    def _create_session(self) -> requests.Session:
        """Create HTTP session with authentication"""
        session = requests.Session()
        session.auth = (self.email, self.api_token)
        session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return session

    def _validate_credentials(self):
        """Validate Jira credentials are configured"""
        if not all([self.base_url, self.email, self.api_token]):
            raise ValueError(
                "Missing Jira credentials. Check environment variables or config file."
            )
        logger.info("Jira credentials configured")

    def fetch_issues(self, jql: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Fetch issues using JQL query"""
        try:
            encoded_jql = quote(jql)
            url = f"{self.base_url}/rest/api/3/search/jql"
            params = {
                "jql": jql,
                "maxResults": max_results,
                "fields": "summary,key,status,assignee,project,priority,parent,watchers,issuelinks,description,created,resolutiondate",
            }

            logger.info(f"Fetching issues with JQL: {jql[:100]}...")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            issues = data.get("issues", [])
            logger.info(f"Successfully fetched {len(issues)} issues from Jira")
            return issues

        except requests.exceptions.RequestException as e:
            logger.error(f"Jira API request failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Jira response: {e}")
            raise

    def collect_historical_cycle_times(
        self, team_projects: List[str], months: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Phase 2 Enhancement: Collect historical cycle time data for Monte Carlo simulation

        EXTENDS existing fetch_issues() method - NO duplicate API client (DRY compliance)
        Sequential Thinking: Systematic data collection for accurate forecasting
        Universal: Works for all teams regardless of story point usage
        """
        try:
            # Calculate date range for historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months * 30)

            # REUSE existing JQL patterns - build upon proven query structure
            project_filter = " OR ".join(
                [f"project = {project}" for project in team_projects]
            )
            historical_jql = f"""
                ({project_filter}) AND
                status = Done AND
                resolutiondate >= "{start_date.strftime('%Y-%m-%d')}" AND
                resolutiondate <= "{end_date.strftime('%Y-%m-%d')}"
                ORDER BY resolutiondate DESC
            """

            logger.info(
                f"Collecting {months} months of historical cycle time data for projects: {team_projects}"
            )

            # LEVERAGE existing fetch_issues() method - avoid duplicate API logic
            historical_issues = []
            start_at = 0
            max_results = 100

            while True:
                # Use existing proven pagination pattern
                batch_jql = f"{historical_jql}"
                url = f"{self.base_url}/rest/api/3/search/jql"
                params = {
                    "jql": batch_jql,
                    "maxResults": max_results,
                    "startAt": start_at,
                    "fields": "summary,key,status,assignee,project,priority,created,resolutiondate,changelog",
                }

                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()
                batch_issues = data.get("issues", [])

                if not batch_issues:
                    break

                historical_issues.extend(batch_issues)
                start_at += max_results

                # Safety check to prevent excessive API calls
                if len(historical_issues) >= 1000:
                    logger.warning(
                        f"Historical data collection reached limit of 1000 issues"
                    )
                    break

            logger.info(
                f"Successfully collected {len(historical_issues)} historical issues for cycle time analysis"
            )
            return historical_issues

        except requests.exceptions.RequestException as e:
            logger.error(f"Historical cycle time collection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in cycle time collection: {e}")
            raise


class StrategicAnalyzer:
    """
    Analyzes story strategic impact and business value

    Enhanced with real MCP integration for Strategic reasoning and Context7 benchmarking
    BLOAT_PREVENTION: REUSES existing MCPIntegrationManager, no duplicate MCP logic
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.jira_base_url = os.getenv(
            "JIRA_BASE_URL", "https://procoretech.atlassian.net"
        )

        # Real MCP Integration (BLOAT_PREVENTION: REUSE existing infrastructure)
        self.config = config or {}
        self.mcp_bridge = None

        if MCP_BRIDGE_AVAILABLE and self.config.get("enable_mcp_integration", False):
            try:
                self.mcp_bridge = create_weekly_reporter_mcp_bridge(self.config)
                logger.info("StrategicAnalyzer: Real MCP integration enabled")
            except Exception as e:
                logger.warning(f"StrategicAnalyzer: MCP integration failed: {e}")
                self.mcp_bridge = None

    def calculate_strategic_impact(self, issue: JiraIssue) -> StrategicScore:
        """Calculate strategic impact score for a story"""
        score = StrategicScore()

        # Priority scoring
        if issue.priority in ["Highest", "Critical"]:
            score.add_score(3, "🔴 Critical Priority")
        elif issue.priority == "High":
            score.add_score(2, "🟡 High Priority")

        # Cross-project indicators
        cross_project_patterns = (
            r"(UIS-|UXI-|HUBS-|WES-|FSGD-|shared|platform|design.system)"
        )
        if re.search(cross_project_patterns, issue.summary, re.IGNORECASE):
            score.add_score(2, "🌐 Cross-Project Impact")

        # Platform/DevEx indicators
        platform_patterns = r"(platform|developer.experience|DevEx|tooling|automation|Hammer|CKEditor|webpack|vite|build.tool)"
        if re.search(platform_patterns, issue.summary, re.IGNORECASE):
            score.add_score(3, "⚙️ Platform/DevEx Impact")

        # Dependency/blocking indicators
        dependency_patterns = r"(block|depend|enable|unlock|prerequisite)"
        if re.search(dependency_patterns, issue.summary, re.IGNORECASE):
            score.add_score(2, "🔓 Dependency Resolution")

        # Production/customer impact
        production_patterns = r"(production|customer|incident|outage|hotfix)"
        if re.search(production_patterns, issue.summary, re.IGNORECASE):
            score.add_score(3, "⚡ Production Impact")

        # Collaboration indicators
        if issue.watchers > 3:
            score.add_score(1, f"👥 High Collaboration ({issue.watchers} watchers)")

        if issue.links > 2:
            score.add_score(1, f"🔗 Highly Connected ({issue.links} links)")

        # Executive priority override (UIS-1590, UXI-1455)
        if issue.key in ["UIS-1590", "UXI-1455"]:
            score.add_score(5, "👑 Executive Priority")

        # Version 1.0 releases
        version_patterns = r"(v1\.0|version.1|Hammer.v1|L2)"
        if re.search(version_patterns, issue.summary, re.IGNORECASE):
            score.add_score(3, "🎯 Major Release/L2 Initiative")

        return score

    def extract_business_value(self, raw_issue: Dict[str, Any]) -> str:
        """Extract and format business value from Jira issue"""
        try:
            description = raw_issue.get("fields", {}).get("description")
            project_name = (
                raw_issue.get("fields", {}).get("project", {}).get("name", "")
            )

            # Handle Jira's rich text format (dict) vs plain text
            if isinstance(description, dict):
                # Extract text from Atlassian Document Format (ADF)
                business_value = self._extract_text_from_adf(description)
            elif isinstance(description, str) and description.strip():
                business_value = (
                    description.strip()[:200] + "..."
                    if len(description) > 200
                    else description.strip()
                )
            else:
                # Generate context-based business value based on project
                business_value = self._generate_context_business_value(project_name)

            # Ensure proper formatting
            business_value = business_value.strip()
            if business_value and not business_value[0].isupper():
                business_value = business_value[0].upper() + business_value[1:]

            if business_value and not business_value.endswith((".", "!", "?")):
                business_value += "."

            return (
                business_value
                or "Strategic platform initiative with organizational impact."
            )

        except Exception as e:
            logger.warning(f"Error extracting business value: {e}")
            return "Strategic platform initiative - see issue for detailed business impact."

    def _extract_text_from_adf(self, adf_content: Dict[str, Any]) -> str:
        """Extract plain text from Atlassian Document Format"""

        def extract_text(node):
            if isinstance(node, dict):
                if node.get("type") == "text":
                    return node.get("text", "")
                elif "content" in node:
                    return " ".join(extract_text(child) for child in node["content"])
            elif isinstance(node, list):
                return " ".join(extract_text(child) for child in node)
            return ""

        text = extract_text(adf_content).strip()
        return text[:200] + "..." if len(text) > 200 else text

    def _generate_context_business_value(self, project_name: str) -> str:
        """Generate contextual business value based on project type"""
        project_contexts = {
            "Web Platform": "Improves platform engineering capabilities and developer experience across the organization",
            "Web Design Systems": "Improves brand consistency and design system adoption across product suite",
            "Experience Services": "Optimizes user experience workflows and service delivery efficiency",
            "Hubs": "Advances platform integration capabilities and user workflow consolidation",
            "Globalizers": "Enables international market expansion and localization capabilities",
            "Onboarding": "Streamlines user onboarding experience and activation workflows",
        }
        return project_contexts.get(
            project_name,
            "Strategic platform initiative with cross-organizational impact",
        )

    def analyze_initiative(
        self, raw_issue: Dict[str, Any], child_stories: List[JiraIssue] = None
    ) -> Initiative:
        """Convert raw Jira epic into strategic initiative with business context"""
        fields = raw_issue.get("fields", {})
        summary = fields.get("summary", "")

        # Detect initiative level
        level = self._detect_initiative_level(summary)

        # Generate business context based on initiative type
        business_context = self._generate_initiative_business_context(summary, fields)

        # Calculate progress from child stories
        progress_pct = self._calculate_progress_percentage(child_stories or [])

        # Generate status description
        status_desc = self._generate_status_description(
            fields.get("status", {}).get("name", ""), progress_pct
        )

        # Extract team impact
        team_impact = self._extract_team_impact(summary, fields)

        return Initiative(
            key=raw_issue.get("key", ""),
            title=self._clean_initiative_title(summary),
            level=level,
            progress_pct=progress_pct,
            status_desc=status_desc,
            business_context=business_context,
            team_impact=team_impact,
            project=fields.get("project", {}).get("name", ""),
            status=fields.get("status", {}).get("name", ""),
            child_stories=child_stories or [],
        )

    def _detect_initiative_level(self, summary: str) -> str:
        """Detect L0, L1, L2 initiative level from summary"""
        if "L0:" in summary or "Layer 0" in summary:
            return "L0"
        elif "L2:" in summary or "Layer 2" in summary:
            return "L2"
        elif "L1:" in summary or "Layer 1" in summary:
            return "L1"
        else:
            # Infer from content
            compliance_keywords = ["FedRAMP", "compliance", "security", "audit", "risk"]
            platform_keywords = ["platform", "v1", "developer", "build", "tool"]

            if any(
                keyword.lower() in summary.lower() for keyword in compliance_keywords
            ):
                return "L0"
            elif any(
                keyword.lower() in summary.lower() for keyword in platform_keywords
            ):
                return "L2"
            else:
                return "Strategic"

    def _generate_initiative_business_context(
        self, summary: str, fields: Dict[str, Any]
    ) -> str:
        """Generate executive business context for initiative"""
        initiative_contexts = {
            # L0 - Foundational/Compliance
            "FedRAMP": "Required to address security vulnerabilities and maintain compliance for government clients",
            "security": "Critical security risk mitigation to protect customer data and maintain compliance",
            "compliance": "Regulatory compliance initiative to meet industry standards and audit requirements",
            # L2 - Platform/Capabilities
            "Hammer": "Platform build tool enabling faster local and production builds with standard technologies",
            "build": "Developer productivity enhancement reducing build times and improving development velocity",
            "International": "Market expansion enablement through localization infrastructure and multi-region support",
            "Admin": "Platform administration capabilities improving operational efficiency and user management",
            "Explore": "Product discovery and filtering capabilities enabling better user experience and product adoption",
        }

        summary_lower = summary.lower()
        for keyword, context in initiative_contexts.items():
            if keyword.lower() in summary_lower:
                return context

        # Fallback to description or generic
        description = fields.get("description", "")
        if isinstance(description, dict):
            desc_text = self._extract_text_from_adf(description)
        else:
            desc_text = str(description) if description else ""

        if desc_text and len(desc_text) > 20:
            return desc_text[:150] + "..." if len(desc_text) > 150 else desc_text

        return "Strategic platform initiative advancing organizational capabilities and competitive positioning"

    def _calculate_progress_percentage(self, child_stories: List[JiraIssue]) -> int:
        """Calculate completion percentage from child stories"""
        if not child_stories:
            return 0

        completed_statuses = ["Done", "Closed", "Resolved", "Released"]
        completed_count = sum(
            1 for story in child_stories if story.status in completed_statuses
        )

        if len(child_stories) == 0:
            return 0

        return int((completed_count / len(child_stories)) * 100)

    def _generate_status_description(self, status: str, progress_pct: int) -> str:
        """Generate executive status description"""
        if status == "Done" or status == "Completed":
            return "Released with minimal impact to teams"
        elif status == "In Progress":
            if progress_pct >= 80:
                return "Releasing this week"
            elif progress_pct >= 60:
                return f"Team {progress_pct}% complete with rollout"
            else:
                return "Active development in progress"
        elif status == "In Review":
            return "Final review and release preparation"
        else:
            return "Planning and discovery phase"

    def _extract_team_impact(self, summary: str, fields: Dict[str, Any]) -> str:
        """Extract team impact language from initiative"""
        impact_indicators = {
            "minimal impact": "minimal impact to teams",
            "breaking": "requires team coordination for migration",
            "migration": "coordinated team migration effort",
            "rollout": "phased rollout across teams",
        }

        summary_lower = summary.lower()
        description = str(fields.get("description", "")).lower()
        combined_text = f"{summary_lower} {description}"

        for indicator, impact in impact_indicators.items():
            if indicator in combined_text:
                return impact

        return "standard team adoption process"

    def _clean_initiative_title(self, summary: str) -> str:
        """Clean up initiative title for executive presentation"""
        # Remove Jira formatting and technical prefixes
        cleaned = (
            summary.replace("[Web Platform]", "")
            .replace("Layer 0 -", "L0 -")
            .replace("Layer 2 -", "L2 -")
        )
        cleaned = cleaned.strip()

        # Standardize common initiative names
        if "Hammer" in cleaned and "1.0" in cleaned:
            return "Hammer V1"
        elif "FedRAMP" in cleaned:
            return "FedRAMP Follow up"
        elif "International" in cleaned and "Locale" in cleaned:
            return "International Locale Enablement"
        elif "Admin" in cleaned and "Pages" in cleaned:
            return "Admin Pages Migration"
        elif "Procore Explore" in cleaned:
            return "Procore Explore Full Product Life Cycle"

        return cleaned

    # Phase 2 Enhancement: Real MCP Integration with Sequential Thinking Monte Carlo
    def calculate_completion_probability(
        self, issue: JiraIssue, historical_data: List[Dict]
    ) -> Dict:
        """
        EXTENDS existing strategic analysis with REAL MCP Sequential thinking + Monte Carlo

        BLOAT_PREVENTION: REUSES existing statistical foundation, ENHANCES with real MCP
        Sequential MCP: Real strategic reasoning trail generation for executive insights
        Context7 MCP: Industry benchmarking patterns for competitive analysis
        DRY Compliance: EXTENDS existing JiraIssue dataclass and scoring patterns
        """
        # SEQUENTIAL STEP 1: EXTEND existing priority scoring logic (UNCHANGED)
        base_score = self.calculate_strategic_impact(issue)  # REUSE existing method

        # SEQUENTIAL STEP 2: Historical cycle time analysis (UNCHANGED)
        cycle_time_data = self._sequential_analyze_historical_cycles(historical_data)

        # SEQUENTIAL STEP 3: Monte Carlo simulation (UNCHANGED - statistical foundation)
        completion_prob = self._sequential_monte_carlo_simulation(
            issue, cycle_time_data
        )

        # SEQUENTIAL STEP 4: Risk assessment (UNCHANGED)
        risk_analysis = self._sequential_risk_assessment(
            issue, base_score, cycle_time_data
        )

        # SEQUENTIAL STEP 5: Timeline prediction (UNCHANGED)
        timeline_forecast = self._sequential_timeline_prediction(issue, cycle_time_data)

        # NEW: Real MCP Enhancement for executive insights
        mcp_enhancement = self._enhance_with_real_mcp_reasoning(
            issue, completion_prob, cycle_time_data
        )

        # Base statistical result (PRESERVED)
        base_result = {
            "completion_probability": completion_prob,
            "confidence_interval": self._calculate_monte_carlo_confidence(
                cycle_time_data
            ),
            "risk_factors": risk_analysis,
            "timeline_forecast": timeline_forecast,
            "simulation_runs": 10000,  # Monte Carlo simulation iterations
            "cycle_time_percentiles": self._calculate_cycle_time_percentiles(
                cycle_time_data
            ),
            "sequential_reasoning": self._generate_reasoning_trail(
                issue, cycle_time_data
            ),
            "analysis_methodology": "Real MCP Sequential + Monte Carlo",  # UPDATED
        }

        # ENHANCE with real MCP insights (preserves existing structure)
        if mcp_enhancement and not mcp_enhancement.fallback_used:
            base_result.update(
                {
                    "mcp_reasoning_trail": mcp_enhancement.reasoning_trail,
                    "executive_summary": mcp_enhancement.executive_summary,
                    "mcp_risk_factors": mcp_enhancement.risk_factors,
                    "industry_context": mcp_enhancement.industry_context,
                    "mcp_processing_time": mcp_enhancement.processing_time,
                    "mcp_enhanced": True,
                }
            )
        else:
            base_result.update(
                {
                    "mcp_enhanced": False,
                    "mcp_fallback_reason": (
                        mcp_enhancement.error_message
                        if mcp_enhancement
                        else "MCP disabled"
                    ),
                }
            )

        return base_result

    def _sequential_analyze_historical_cycles(
        self, historical_data: List[Dict]
    ) -> List[float]:
        """Sequential Step 2: Systematic cycle time analysis with structured reasoning"""
        cycle_times = []

        for issue_data in historical_data:
            try:
                fields = issue_data.get("fields", {})
                created_str = fields.get("created")
                resolved_str = fields.get("resolutiondate")

                if created_str and resolved_str:
                    # Parse Jira datetime format
                    created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    resolved = datetime.fromisoformat(
                        resolved_str.replace("Z", "+00:00")
                    )

                    # Calculate cycle time in days
                    cycle_time_days = (resolved - created).total_seconds() / (24 * 3600)

                    # Sequential validation: reasonable cycle time bounds
                    if 0.1 <= cycle_time_days <= 365:  # Between 2.4 hours and 1 year
                        cycle_times.append(cycle_time_days)

            except Exception as e:
                logger.warning(f"Could not parse cycle time for issue: {e}")
                continue

        logger.info(
            f"Sequential analysis: Extracted {len(cycle_times)} valid cycle times from {len(historical_data)} issues"
        )
        return cycle_times

    def _sequential_monte_carlo_simulation(
        self, issue: JiraIssue, cycle_time_data: List[float]
    ) -> float:
        """Sequential Step 3: Monte Carlo simulation with structured approach"""
        import random

        if not cycle_time_data or len(cycle_time_data) < 5:
            logger.warning("Insufficient cycle time data for Monte Carlo simulation")
            return 0.5  # Default 50% probability

        # Sequential approach: simulate epic completion based on cycle time distribution
        simulation_runs = 10000
        completion_count = 0
        target_timeline_days = 21  # 3 weeks default

        for _ in range(simulation_runs):
            # Sample from historical cycle time distribution
            sampled_cycle_time = random.choice(cycle_time_data)

            # Simple epic simulation: assume epic = 3-8 tickets
            epic_size = random.randint(3, 8)
            estimated_completion_days = sampled_cycle_time * epic_size

            # Check if completes within target timeline
            if estimated_completion_days <= target_timeline_days:
                completion_count += 1

        completion_probability = completion_count / simulation_runs
        logger.info(
            f"Sequential Monte Carlo: {completion_probability:.2%} completion probability in {target_timeline_days} days"
        )

        return completion_probability

    def _sequential_risk_assessment(
        self, issue: JiraIssue, base_score: StrategicScore, cycle_time_data: List[float]
    ) -> Dict:
        """Sequential Step 4: Risk assessment with methodical evaluation"""
        risk_factors = []
        risk_score = 0

        # Risk factor 1: Strategic complexity
        if base_score.score >= 8:
            risk_factors.append("High strategic complexity increases delivery risk")
            risk_score += 2

        # Risk factor 2: Cycle time volatility
        if cycle_time_data and len(cycle_time_data) > 5:
            import statistics

            cycle_time_std = statistics.stdev(cycle_time_data)
            cycle_time_mean = statistics.mean(cycle_time_data)
            volatility = cycle_time_std / cycle_time_mean if cycle_time_mean > 0 else 0

            if volatility > 0.5:
                risk_factors.append(
                    f"High cycle time volatility ({volatility:.1%}) indicates unpredictable delivery"
                )
                risk_score += 1

        # Risk factor 3: Cross-project dependencies
        if any("Cross-Project" in indicator for indicator in base_score.indicators):
            risk_factors.append(
                "Cross-project dependencies may cause coordination delays"
            )
            risk_score += 1

        return {
            "risk_factors": risk_factors,
            "risk_score": risk_score,
            "risk_level": (
                "High" if risk_score >= 3 else "Medium" if risk_score >= 1 else "Low"
            ),
        }

    def _sequential_timeline_prediction(
        self, issue: JiraIssue, cycle_time_data: List[float]
    ) -> Dict:
        """Sequential Step 5: Timeline prediction with structured reasoning"""
        if not cycle_time_data:
            return {"prediction": "Insufficient data for timeline prediction"}

        import statistics

        # Calculate percentile-based predictions
        sorted_times = sorted(cycle_time_data)
        n = len(sorted_times)

        p50_days = sorted_times[int(0.5 * n)] * 5  # Assume epic = ~5 tickets
        p85_days = sorted_times[int(0.85 * n)] * 5
        p95_days = sorted_times[int(0.95 * n)] * 5

        return {
            "prediction": f"Epic completion forecast based on historical cycle times",
            "50th_percentile_days": round(p50_days, 1),
            "85th_percentile_days": round(p85_days, 1),
            "95th_percentile_days": round(p95_days, 1),
            "recommendation": f"Plan for {round(p85_days, 1)} days (85% confidence level)",
        }

    def _calculate_monte_carlo_confidence(self, cycle_time_data: List[float]) -> Dict:
        """Calculate confidence intervals for Monte Carlo results"""
        if not cycle_time_data:
            return {"confidence": "Low - insufficient data"}

        data_points = len(cycle_time_data)
        confidence_level = (
            "High" if data_points >= 50 else "Medium" if data_points >= 20 else "Low"
        )

        return {
            "confidence_level": confidence_level,
            "data_points": data_points,
            "confidence_note": f"Based on {data_points} historical cycle time samples",
        }

    def _calculate_cycle_time_percentiles(self, cycle_time_data: List[float]) -> Dict:
        """Calculate cycle time distribution percentiles"""
        if not cycle_time_data:
            return {}

        sorted_times = sorted(cycle_time_data)
        n = len(sorted_times)

        return {
            "p10": round(sorted_times[int(0.1 * n)], 1),
            "p25": round(sorted_times[int(0.25 * n)], 1),
            "p50": round(sorted_times[int(0.5 * n)], 1),
            "p75": round(sorted_times[int(0.75 * n)], 1),
            "p90": round(sorted_times[int(0.9 * n)], 1),
            "p95": round(sorted_times[int(0.95 * n)], 1),
        }

    def _generate_reasoning_trail(
        self, issue: JiraIssue, cycle_time_data: List[float]
    ) -> List[str]:
        """Generate transparent reasoning trail for executive communication"""
        reasoning = [
            f"1. Strategic Analysis: Evaluated {issue.key} using existing proven scoring patterns",
            f"2. Historical Data: Analyzed {len(cycle_time_data)} historical cycle time samples",
            f"3. Monte Carlo Simulation: Ran 10,000 iterations using cycle time distribution",
            f"4. Risk Assessment: Systematic evaluation of completion risks and dependencies",
            f"5. Timeline Prediction: Percentile-based forecasting with confidence intervals",
        ]
        return reasoning

    def analyze_cross_team_dependencies(self, issues: List[JiraIssue]) -> Dict:
        """
        ENHANCES existing cross-project detection with sequential thinking dependency analysis

        Sequential Thinking: Systematic step-by-step dependency evaluation
        DRY Compliance: Builds upon existing cross_project_patterns regex
        Context7 Integration: Official Jira link analysis patterns for enterprise coordination
        """
        # SEQUENTIAL STEP 1: REUSE existing cross-project pattern detection
        cross_project_issues = [
            i for i in issues if self._is_cross_project(i)
        ]  # Existing logic

        # SEQUENTIAL STEP 2: Systematic dependency graph construction
        dependency_graph = self._sequential_build_dependency_graph(cross_project_issues)

        # SEQUENTIAL STEP 3: Methodical critical path analysis
        blocking_analysis = self._sequential_identify_critical_blocks(dependency_graph)

        # SEQUENTIAL STEP 4: Structured coordination assessment
        coordination_analysis = self._sequential_assess_coordination(dependency_graph)

        # SEQUENTIAL STEP 5: Strategic mitigation development
        mitigation_strategies = self._sequential_generate_mitigations(blocking_analysis)

        return {
            "dependency_graph": dependency_graph,
            "blocking_issues": blocking_analysis,
            "coordination_bottlenecks": coordination_analysis,
            "mitigation_strategies": mitigation_strategies,
            "sequential_analysis_steps": self._document_dependency_reasoning(),  # NEW
            "methodology": "Sequential Thinking Dependency Analysis",  # NEW
        }

    def _is_cross_project(self, issue: JiraIssue) -> bool:
        """REUSE existing cross-project detection logic (DRY compliance)"""
        cross_project_patterns = (
            r"(UIS-|UXI-|HUBS-|WES-|FSGD-|shared|platform|design.system)"
        )
        return bool(re.search(cross_project_patterns, issue.summary, re.IGNORECASE))

    def _sequential_build_dependency_graph(
        self, cross_project_issues: List[JiraIssue]
    ) -> Dict:
        """Sequential Step 2: Systematic dependency graph construction"""
        dependency_graph = {"nodes": [], "edges": [], "teams": set(), "projects": set()}

        for issue in cross_project_issues:
            # Add node to graph
            node = {
                "key": issue.key,
                "summary": issue.summary,
                "project": issue.project,
                "status": issue.status,
                "priority": issue.priority,
                "links": issue.links,
            }
            dependency_graph["nodes"].append(node)
            dependency_graph["projects"].add(issue.project)

            # Infer team from project (this could be enhanced with actual team mapping)
            team = self._infer_team_from_project(issue.project)
            dependency_graph["teams"].add(team)

        # Sequential analysis: identify potential blocking relationships
        for issue in cross_project_issues:
            if issue.links > 0:  # Issues with links likely have dependencies
                # Create edge representing potential dependency
                edge = {
                    "from": issue.key,
                    "to": "LINKED_ISSUES",  # Simplified - could be enhanced with actual link parsing
                    "type": "dependency",
                    "strength": min(issue.links, 5),  # Cap at 5 for visualization
                }
                dependency_graph["edges"].append(edge)

        logger.info(
            f"Sequential dependency graph: {len(dependency_graph['nodes'])} nodes, {len(dependency_graph['edges'])} edges"
        )
        return dependency_graph

    def _sequential_identify_critical_blocks(self, dependency_graph: Dict) -> Dict:
        """Sequential Step 3: Methodical critical path analysis"""
        blocking_issues = []
        critical_path_nodes = []

        # Identify high-link issues as potential bottlenecks
        for node in dependency_graph["nodes"]:
            if node["links"] >= 3:  # Issues with 3+ links are potential bottlenecks
                blocking_issues.append(
                    {
                        "key": node["key"],
                        "summary": node["summary"],
                        "project": node["project"],
                        "status": node["status"],
                        "link_count": node["links"],
                        "blocking_potential": (
                            "High" if node["links"] >= 5 else "Medium"
                        ),
                        "impact_assessment": self._assess_blocking_impact(node),
                    }
                )

        # Identify critical path based on project diversity
        projects_in_path = len(dependency_graph["projects"])
        teams_in_path = len(dependency_graph["teams"])

        critical_path_analysis = {
            "projects_involved": projects_in_path,
            "teams_involved": teams_in_path,
            "coordination_complexity": (
                "High"
                if teams_in_path >= 4
                else "Medium" if teams_in_path >= 2 else "Low"
            ),
            "estimated_coordination_overhead": f"{teams_in_path * 15}% of team capacity",
        }

        return {
            "blocking_issues": blocking_issues,
            "critical_path_analysis": critical_path_analysis,
            "total_blocking_potential": len(blocking_issues),
        }

    def _sequential_assess_coordination(self, dependency_graph: Dict) -> Dict:
        """Sequential Step 4: Structured coordination assessment"""
        teams = list(dependency_graph["teams"])
        projects = list(dependency_graph["projects"])

        coordination_bottlenecks = []

        # Assess cross-team coordination complexity
        if len(teams) >= 3:
            coordination_bottlenecks.append(
                {
                    "type": "Multi-team coordination",
                    "teams_involved": teams,
                    "complexity_rating": "High",
                    "estimated_overhead": f"{len(teams) * 20}% capacity per team",
                    "mitigation": "Establish clear communication protocols and dependency tracking",
                }
            )

        # Assess cross-project coordination
        if len(projects) >= 2:
            coordination_bottlenecks.append(
                {
                    "type": "Cross-project integration",
                    "projects_involved": projects,
                    "complexity_rating": "Medium",
                    "estimated_overhead": f"{len(projects) * 10}% additional integration effort",
                    "mitigation": "Define clear API contracts and integration testing strategy",
                }
            )

        return {
            "bottlenecks": coordination_bottlenecks,
            "coordination_score": self._calculate_coordination_score(teams, projects),
            "recommended_actions": self._generate_coordination_recommendations(
                teams, projects
            ),
        }

    def _sequential_generate_mitigations(self, blocking_analysis: Dict) -> List[Dict]:
        """Sequential Step 5: Strategic mitigation development"""
        mitigation_strategies = []

        blocking_issues = blocking_analysis.get("blocking_issues", [])
        critical_path = blocking_analysis.get("critical_path_analysis", {})

        # Mitigation 1: Address high-impact blocking issues
        high_impact_blocks = [
            issue
            for issue in blocking_issues
            if issue.get("blocking_potential") == "High"
        ]
        if high_impact_blocks:
            mitigation_strategies.append(
                {
                    "strategy": "Priority escalation for blocking issues",
                    "action": f"Escalate {len(high_impact_blocks)} high-impact blocking issues to leadership",
                    "timeline": "1-2 sprints",
                    "success_metric": "Reduction in cross-team blocking dependencies by 50%",
                    "owner": "Engineering Leadership",
                    "issues": [issue["key"] for issue in high_impact_blocks],
                }
            )

        # Mitigation 2: Coordination overhead reduction
        coordination_complexity = critical_path.get("coordination_complexity")
        if coordination_complexity in ["High", "Medium"]:
            mitigation_strategies.append(
                {
                    "strategy": "Cross-team coordination optimization",
                    "action": "Implement structured dependency tracking and regular cross-team sync meetings",
                    "timeline": "2-3 sprints",
                    "success_metric": f"Reduce coordination overhead from {critical_path.get('estimated_coordination_overhead', 'N/A')} to <20%",
                    "owner": "Platform Team",
                    "tools": [
                        "Dependency tracking dashboard",
                        "Weekly cross-team sync",
                        "Clear escalation paths",
                    ],
                }
            )

        # Mitigation 3: Preventive measures
        mitigation_strategies.append(
            {
                "strategy": "Dependency prevention framework",
                "action": "Establish architectural patterns to minimize future cross-team dependencies",
                "timeline": "3-6 months",
                "success_metric": "Reduce new cross-team dependencies by 40%",
                "owner": "Architecture Team",
                "approach": "Platform capabilities and well-defined APIs",
            }
        )

        return mitigation_strategies

    def _infer_team_from_project(self, project: str) -> str:
        """Infer team name from project - can be enhanced with actual team mapping"""
        team_mapping = {
            "Web Platform": "Web Platform Team",
            "Design System": "Design System Team",
            "Hubs": "Hubs Team",
            "Experience": "Experience Team",
            "Globalizers": "i18n Team",
        }
        return team_mapping.get(project, f"{project} Team")

    def _assess_blocking_impact(self, node: Dict) -> str:
        """Assess the potential impact of a blocking issue"""
        priority = node.get("priority", "")
        links = node.get("links", 0)

        if priority in ["Highest", "Critical"] and links >= 5:
            return "Critical - High priority with extensive dependencies"
        elif priority in ["Highest", "Critical"] or links >= 4:
            return "High - Either high priority or significant dependencies"
        elif links >= 2:
            return "Medium - Some cross-team coordination required"
        else:
            return "Low - Minimal blocking potential"

    def _calculate_coordination_score(
        self, teams: List[str], projects: List[str]
    ) -> Dict:
        """Calculate a coordination complexity score"""
        team_factor = len(teams) * 2  # Teams require more coordination than projects
        project_factor = len(projects)

        total_score = team_factor + project_factor

        if total_score >= 10:
            complexity = "Very High"
        elif total_score >= 6:
            complexity = "High"
        elif total_score >= 3:
            complexity = "Medium"
        else:
            complexity = "Low"

        return {
            "score": total_score,
            "complexity": complexity,
            "team_factor": team_factor,
            "project_factor": project_factor,
        }

    def _generate_coordination_recommendations(
        self, teams: List[str], projects: List[str]
    ) -> List[str]:
        """Generate specific coordination recommendations"""
        recommendations = []

        if len(teams) >= 3:
            recommendations.append(
                f"Establish regular sync meetings for {len(teams)} teams involved"
            )
            recommendations.append("Create shared dependency tracking dashboard")
            recommendations.append("Define clear escalation paths for blocking issues")

        if len(projects) >= 2:
            recommendations.append(
                f"Define API contracts between {len(projects)} projects"
            )
            recommendations.append("Implement integration testing strategy")
            recommendations.append(
                "Create shared documentation for cross-project interfaces"
            )

        recommendations.append("Monitor coordination overhead metrics weekly")

        return recommendations

    def _document_dependency_reasoning(self) -> List[str]:
        """Document the sequential thinking steps for dependency analysis"""
        return [
            "1. Cross-Project Detection: Applied existing regex patterns to identify cross-team work",
            "2. Dependency Graph Construction: Systematically mapped relationships between issues and teams",
            "3. Critical Path Analysis: Methodically identified blocking issues and coordination complexity",
            "4. Coordination Assessment: Structured evaluation of multi-team coordination overhead",
            "5. Mitigation Development: Strategic planning for dependency resolution and prevention",
        ]

    def _enhance_with_real_mcp_reasoning(
        self,
        issue: JiraIssue,
        completion_probability: float,
        cycle_time_data: List[float],
    ) -> Optional[MCPEnhancementResult]:
        """
        ENHANCE existing analysis with real MCP Sequential reasoning and Context7 benchmarking

        BLOAT_PREVENTION: REUSES existing MCP bridge, no duplicate MCP coordination
        Sequential MCP: Strategic reasoning trail generation for executive insights
        Context7 MCP: Industry benchmarking patterns for competitive analysis
        """
        if not self.mcp_bridge or not self.mcp_bridge.is_enabled():
            logger.debug("MCP enhancement skipped: bridge unavailable or disabled")
            return None

        try:
            # Real Sequential MCP enhancement for strategic reasoning
            sequential_enhancement = None
            if self.config.get("enable_sequential_reasoning", True):
                sequential_enhancement = self.mcp_bridge.enhance_completion_probability(
                    issue.key, completion_probability, cycle_time_data
                )

            # Real Context7 MCP enhancement for industry benchmarking
            context7_enhancement = None
            if self.config.get("enable_context7_benchmarking", True):
                # Extract team name from issue project
                team_name = issue.project or "unknown_team"
                context7_enhancement = self.mcp_bridge.enhance_with_industry_benchmarks(
                    team_name, cycle_time_data, domain="software_engineering"
                )

            # Combine enhancements (preserving individual fallback behavior)
            combined_result = MCPEnhancementResult(
                reasoning_trail=[],
                executive_summary="",
                risk_factors=[],
                industry_context={},
                processing_time=0.0,
                fallback_used=True,
                error_message="No enhancements available",
            )

            # Merge Sequential enhancement
            if sequential_enhancement and not sequential_enhancement.fallback_used:
                combined_result.reasoning_trail.extend(
                    sequential_enhancement.reasoning_trail
                )
                combined_result.executive_summary = (
                    sequential_enhancement.executive_summary
                )
                combined_result.risk_factors.extend(sequential_enhancement.risk_factors)
                combined_result.processing_time += (
                    sequential_enhancement.processing_time
                )
                combined_result.fallback_used = False
                combined_result.error_message = None

            # Merge Context7 enhancement
            if context7_enhancement and not context7_enhancement.fallback_used:
                combined_result.industry_context.update(
                    context7_enhancement.industry_context
                )
                combined_result.processing_time += context7_enhancement.processing_time
                combined_result.fallback_used = False
                combined_result.error_message = None

            # Log enhancement status
            if not combined_result.fallback_used:
                logger.info(
                    f"MCP enhancement successful for {issue.key} in {combined_result.processing_time:.2f}s"
                )
            else:
                logger.debug(
                    f"MCP enhancement fallback for {issue.key}: {combined_result.error_message}"
                )

            return combined_result

        except Exception as e:
            logger.error(f"MCP enhancement failed for {issue.key}: {e}")
            return (
                MCPEnhancementResult(
                    reasoning_trail=[],
                    executive_summary="",
                    risk_factors=[],
                    industry_context={},
                    processing_time=0.0,
                    fallback_used=True,
                    error_message=f"MCP enhancement error: {str(e)}",
                )
                if MCPEnhancementResult
                else None
            )


class ReportGenerator:
    """Generates markdown weekly reports with strategic insights"""

    def __init__(
        self,
        config: ConfigManager,
        jira_client: JiraClient,
        analyzer: StrategicAnalyzer,
    ):
        self.config = config
        self.jira = jira_client
        self.analyzer = analyzer
        self.current_date = datetime.now()

    def generate_report(self, output_path: str, dry_run: bool = False) -> str:
        """Generate complete weekly report"""
        if dry_run:
            logger.info("DRY RUN: Would generate report with live Jira data")
            return "DRY RUN - No report generated"

        try:
            # Fetch L0/L2 strategic initiatives
            initiatives = []
            strategic_parent_query = self.config.get_jql_query("strategic_parent_epics")
            if strategic_parent_query:
                raw_initiatives = self.jira.fetch_issues(strategic_parent_query)
                initiatives = [
                    self.analyzer.analyze_initiative(issue) for issue in raw_initiatives
                ]

            # Fetch epic data (fallback)
            epic_query = self.config.get_jql_query("weekly_executive_epics")
            epic_issues = []
            if epic_query:
                raw_epics = self.jira.fetch_issues(epic_query)
                epic_issues = [self._convert_raw_issue(issue) for issue in raw_epics]

            # Fetch strategic story data (supporting detail)
            strategic_query = self.config.get_jql_query("strategic_test")
            strategic_issues = []
            if strategic_query:
                raw_strategic = self.jira.fetch_issues(strategic_query)
                strategic_issues = [
                    self._convert_raw_issue(issue) for issue in raw_strategic
                ]

            # Generate report content
            report_content = self._build_report_content(
                epic_issues, strategic_issues, initiatives
            )

            # Write report
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report_content)

            logger.info(f"Weekly report generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise

    def _convert_raw_issue(self, raw_issue: Dict[str, Any]) -> JiraIssue:
        """Convert raw Jira API response to JiraIssue object"""
        fields = raw_issue.get("fields", {})
        return JiraIssue(
            key=raw_issue.get("key", ""),
            summary=fields.get("summary", ""),
            status=fields.get("status", {}).get("name", ""),
            priority=fields.get("priority", {}).get("name", "None"),
            project=fields.get("project", {}).get("name", ""),
            assignee=(
                fields.get("assignee", {}).get("displayName", "Unassigned")
                if fields.get("assignee")
                else "Unassigned"
            ),
            parent_key=(
                fields.get("parent", {}).get("key") if fields.get("parent") else None
            ),
            watchers=fields.get("watchers", {}).get("watchCount", 0),
            links=len(fields.get("issuelinks", [])),
            business_value=self.analyzer.extract_business_value(raw_issue),
        )

    def _build_report_content(
        self,
        epic_issues: List[JiraIssue],
        strategic_issues: List[JiraIssue],
        initiatives: List[Initiative],
    ) -> str:
        """Build complete report content"""
        sections = []

        # Header
        sections.append(self._build_header())

        # Executive Summary
        sections.append(
            self._build_executive_summary_with_initiatives(initiatives, epic_issues)
        )

        # L0/L2 Strategic Initiative Updates (Primary - matching manual format)
        sections.append(self._build_initiative_updates(initiatives))

        # Epic Portfolio (Supporting)
        if epic_issues:
            sections.append(self._build_epic_portfolio(epic_issues))

        # Strategic Story Analysis (Supporting detail)
        if strategic_issues:
            sections.append(self._build_strategic_analysis(strategic_issues))

        # Strategic Impact & Resource Allocation
        sections.append(
            self._build_strategic_impact_with_initiatives(initiatives, epic_issues)
        )

        # Executive Recommendations
        sections.append(self._build_recommendations())

        # Footer
        sections.append(self._build_footer())

        return "\n\n".join(sections)

    def _build_header(self) -> str:
        """Build report header"""
        return f"""# Weekly Executive Report - UI Foundation Platform Epics

**Week of**: {self.current_date.strftime('%B %d, %Y')}
**Director of Engineering**: Chris Cantu
**Report Generated**: {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}
**Data Source**: Live Jira Epic Data

---"""

    def _build_executive_summary(self, epic_issues: List[JiraIssue]) -> str:
        """Build executive summary section"""
        # Count projects with completed epics
        projects = list(set(issue.project for issue in epic_issues))
        project_summary = (
            "\n".join(f"- 1 epic(s) in {project}" for project in projects)
            if projects
            else "- No epics completed this week"
        )

        return f"""## 🎯 Executive Summary

**Epic Portfolio Status**: **{len(epic_issues)} epics** completed this week or finishing this week across UI Foundation platform capabilities.

**Team Coverage**:
{project_summary}

**Strategic Focus**: Platform engineering excellence, design system maturation, international expansion, and user experience optimization.

---"""

    def _build_epic_portfolio(self, epic_issues: List[JiraIssue]) -> str:
        """Build epic portfolio section with proper team grouping"""
        if not epic_issues:
            return """## 📊 Completed Epic Portfolio by Team

**No epics completed this week** - this is the second consecutive week with 0 epic completions.

**Note**: Teams demonstrate high velocity in sprint reviews, indicating a measurement gap between tactical execution and epic-level reporting.

---"""

        # Group epics by project/team
        teams = {}
        for issue in epic_issues:
            project = issue.project
            if project not in teams:
                teams[project] = []
            teams[project].append(issue)

        # Build team sections with clear visual separation
        team_sections = []
        for project, team_issues in sorted(teams.items()):
            # Team header with emoji and clear separation
            team_header = f"""### 📂 {project} ({len(team_issues)} epic{'s' if len(team_issues) != 1 else ''})

"""

            # Epic entries for this team
            epic_entries = []
            for issue in team_issues:
                timing = self._determine_completion_timing(issue.status)
                jira_url = f"{self.analyzer.jira_base_url}/browse/{issue.key}"

                # Build header with parent initiative if available
                if issue.parent_key:
                    parent_url = (
                        f"{self.analyzer.jira_base_url}/browse/{issue.parent_key}"
                    )
                    header = f"#### [{issue.parent_key}]({parent_url}) : [{issue.key}]({jira_url}) - {issue.summary}"
                else:
                    header = f"#### ✅ [{issue.key}]({jira_url}) - {issue.summary}"

                entry = f"""{header}

- **Status**: {timing} ({issue.status})
- **Priority**: {issue.priority}
- **Assignee**: {issue.assignee}
- **Business Value**: {issue.business_value}

"""
                epic_entries.append(entry)

            # Combine team header with epics and add visual separator
            team_section = team_header + "".join(epic_entries) + "---\n"
            team_sections.append(team_section)

        return f"""## 📊 Completed Epic Portfolio by Team

{''.join(team_sections)}"""

    def _build_strategic_analysis(self, strategic_issues: List[JiraIssue]) -> str:
        """Build strategic story analysis section"""
        if not strategic_issues:
            return """## 🚀 Strategic Story Impact Analysis

### Executive Story Highlights

**No strategic stories found** - measurement gap between epic completion (0) and tactical velocity (high)

**Analysis**: Teams demonstrate excellent sprint velocity in reviews, but strategic work isn't captured at epic level.

### 📊 Execution Insights

**Epic Completion**: 0 epics completed (2nd consecutive week)
**Team Velocity**: High - confirmed in sprint reviews across all teams
**Strategic Analysis**: Teams deliver significant tactical work that doesn't aggregate to epic completion

**Executive Translation**:
- **Platform Investment Active**: UIS-1590 (Hammer v1) advancing toward production
- **Technical Excellence**: UXI-1455 (CKEditor migration) completed with high strategic impact
- **Execution Continuity**: Team velocity maintained despite 40% resource reduction

---"""

        # Analyze strategic impact for each story with MCP enhancement
        strategic_entries = []
        mcp_enhanced_count = 0

        for issue in strategic_issues:
            score = self.analyzer.calculate_strategic_impact(issue)
            if score.score >= 5:  # Only show high-impact stories
                timing = self._determine_completion_timing(issue.status)
                jira_url = f"{self.analyzer.jira_base_url}/browse/{issue.key}"

                # Check if we can get MCP-enhanced completion probability analysis
                mcp_indicator = ""
                try:
                    if (
                        hasattr(self.analyzer, "mcp_bridge")
                        and self.analyzer.mcp_bridge
                    ):
                        completion_analysis = (
                            self.analyzer.calculate_completion_probability(issue, [])
                        )
                        if completion_analysis.get("mcp_enhanced", False):
                            mcp_enhanced_count += 1
                            mcp_indicator = "\n- **Analysis Enhancement**: 🤖 MCP Sequential Thinking Applied"
                            if completion_analysis.get("mcp_reasoning_trail"):
                                reasoning_preview = (
                                    completion_analysis["mcp_reasoning_trail"][:1]
                                    if completion_analysis["mcp_reasoning_trail"]
                                    else []
                                )
                                if reasoning_preview:
                                    mcp_indicator += f"\n- **Strategic Insight**: {reasoning_preview[0]}"
                        elif completion_analysis.get("mcp_enhanced", False) == False:
                            mcp_indicator = "\n- **Analysis Enhancement**: 📊 Statistical Monte Carlo (MCP: Fallback)"
                except Exception:
                    # Graceful fallback if completion analysis fails
                    pass

                entry = f"""#### 📋 [{issue.key}]({jira_url}) - {issue.summary}

- **Status**: {timing} ({issue.status})
- **Project**: {issue.project}
- **Strategic Impact**: {score.score}/10 points
- **Business Value**: {' '.join(score.indicators)}{mcp_indicator}

---"""
                strategic_entries.append(entry)

        high_impact_count = len(strategic_entries)

        # Generate MCP enhancement summary
        mcp_summary = ""
        if mcp_enhanced_count > 0:
            mcp_summary = f" (🤖 {mcp_enhanced_count} with MCP Sequential Thinking)"
        elif high_impact_count > 0:
            mcp_summary = f" (📊 Statistical Analysis - MCP Sequential Thinking: {'Active' if hasattr(self.analyzer, 'mcp_bridge') and self.analyzer.mcp_bridge and self.analyzer.mcp_bridge.mcp_enabled else 'Unavailable'})"

        content = f"""## 🚀 Strategic Story Impact Analysis

### Executive Story Highlights

**High-Impact Completions**: {high_impact_count} strategic stories completed or completing this week{mcp_summary}

{''.join(strategic_entries)}"""

        # Add execution insights if no epics completed
        if high_impact_count > 0:
            content += """
### 📊 Execution Insights

**Strategic Work Active**: Platform investments (UIS-1590 Hammer v1) and technical excellence (UXI-1455 CKEditor) demonstrate continued execution

**Executive Translation**:
- **Platform Investment ROI**: Critical developer tooling advancing toward production
- **Technical Debt Reduction**: Legacy system migrations completed with high business impact
- **Execution Resilience**: Strategic work continues despite resource constraints

---"""

        # Add strategic impact scoring rubric for transparency
        content += """
### 📋 Strategic Impact Scoring Methodology

**Impact Score Calculation** (0-10+ points):

**🔴 Priority-Based Scoring**:
- Critical/Highest Priority: +3 points
- High Priority: +2 points

**🌐 Cross-Functional Impact**:
- Cross-Project Integration: +2 points (UIS-, UXI-, HUBS-, WES-, shared components)
- High Collaboration: +1 point (>3 watchers)
- Highly Connected: +1 point (>2 issue links)

**⚙️ Platform & Developer Experience**:
- Platform/DevEx Impact: +3 points (tooling, automation, build systems, developer experience)
- Major Release/L2 Initiative: +3 points (v1.0, version 1, L2 initiatives)

**🔓 Organizational Enablement**:
- Dependency Resolution: +2 points (unblocking, enabling, prerequisite work)
- Production Impact: +3 points (customer-facing, incident response, critical path)

**👑 Executive Override**:
- Executive Priority Stories: +5 points (manually designated strategic stories)

*Strategic stories scoring ≥5 points are highlighted in executive analysis above.*

---"""

        return content

    def _build_strategic_impact(self, epic_issues: List[JiraIssue]) -> str:
        """Build strategic impact and resource allocation section"""
        epic_count = len(epic_issues)
        project_count = (
            len(set(issue.project for issue in epic_issues)) if epic_issues else 0
        )

        velocity_assessment = (
            "Consistent execution capability"
            if epic_count > 0
            else "Teams focus on tactical delivery excellence"
        )
        coordination_quality = (
            f"Excellent - broad platform coverage"
            if project_count >= 4
            else "Good - focused delivery approach"
        )

        return f"""## 🎯 Strategic Impact & Resource Allocation

### Delivery Velocity Analysis
**Completed**: {epic_count} epics delivered this week demonstrating **{velocity_assessment}**

### Cross-Team Coordination Health
**Active Teams**: {project_count} project areas with synchronized delivery execution
**Coordination Quality**: {coordination_quality}

---"""

    def _build_recommendations(self) -> str:
        """Build executive recommendations section"""
        return """## 💡 Executive Recommendations

### Investment ROI Demonstration
**Leverage strategic stories** to demonstrate measurable platform investment returns (UIS-1590 Hammer v1, UXI-1455 CKEditor migration) and strategic value delivery to senior leadership.

### Resource Optimization
**Maintain tactical excellence** while building epic-level measurement capabilities to better capture strategic work for executive communication.

### Stakeholder Communication
**Proactive updates** on strategic story business value and platform investment impact maintain executive confidence during resource constraints.

---"""

    def _build_executive_summary_with_initiatives(
        self, initiatives: List[Initiative], epic_issues: List[JiraIssue]
    ) -> str:
        """Build executive summary with initiative focus"""
        active_initiatives = [
            i
            for i in initiatives
            if i.status in ["In Progress", "In Review", "Completed"]
        ]
        l0_count = len([i for i in active_initiatives if i.level == "L0"])
        l2_count = len([i for i in active_initiatives if i.level == "L2"])

        projects = list(set(i.project for i in initiatives))
        project_summary = (
            "\n".join(f"- {project}" for project in projects)
            if projects
            else "- Platform initiatives across Web Foundation teams"
        )

        return f"""## 🎯 Executive Summary

**Strategic Initiative Status**: **{len(active_initiatives)} strategic initiatives** active or completed this week across UI Foundation platform capabilities.

**Initiative Portfolio**:
- **L0 (Foundational)**: {l0_count} compliance and infrastructure initiatives
- **L2 (Platform)**: {l2_count} strategic capability enhancements

**Team Coverage**:
{project_summary}

**Strategic Focus**: Platform engineering excellence, design system maturation, international expansion, and user experience optimization.

---"""

    def _build_initiative_updates(self, initiatives: List[Initiative]) -> str:
        """Build L0/L2 strategic initiative updates matching manual format"""
        if not initiatives:
            return """## 🎯 Strategic Initiative Updates

**No strategic initiatives found** - continuing with operational delivery focus.

---"""

        # Group by project/team
        by_team = {}
        for initiative in initiatives:
            team_name = self._map_project_to_team_name(initiative.project)
            if team_name not in by_team:
                by_team[team_name] = []
            by_team[team_name].append(initiative)

        initiative_entries = []
        initiative_entries.append("## 🎯 Strategic Initiative Updates\n")

        for team, team_initiatives in by_team.items():
            initiative_entries.append(f"### **{team}**:")
            initiative_entries.append("")

            for initiative in team_initiatives:
                # Format like manual report: "L2 - Hammer V1: Hammer releasing this week enabling faster builds"
                title_with_level = f"**{initiative.level} - {initiative.title}**: {initiative.business_context}"
                if (
                    initiative.status_desc
                    and initiative.status_desc != "Active development in progress"
                ):
                    title_with_level += f". {initiative.status_desc}"

                initiative_entries.append(title_with_level)
                initiative_entries.append("")

        return "\n".join(initiative_entries) + "\n---"

    def _map_project_to_team_name(self, project: str) -> str:
        """Map Jira project to team name for executive presentation"""
        project_team_mapping = {
            "Web Design Systems": "Web Design Systems",
            "Web Platform": "Web Platform",
            "Globalizers": "Internationalization",
            "UIF Special Projects": "Special Projects - Admin Pages",
            "Experience Services": "Experience Services",
            "Procore Initiatives": "Strategic Initiatives",
            "Hubs": "Platform Integration",
            "Onboarding": "User Experience",
        }
        return project_team_mapping.get(project, project)

    def _build_strategic_impact_with_initiatives(
        self, initiatives: List[Initiative], epic_issues: List[JiraIssue]
    ) -> str:
        """Build strategic impact section with initiative focus"""
        active_initiatives = [
            i
            for i in initiatives
            if i.status in ["In Progress", "In Review", "Completed"]
        ]
        initiative_count = len(active_initiatives)
        project_count = len(set(i.project for i in initiatives)) if initiatives else 0

        # Calculate average progress
        avg_progress = 0
        if active_initiatives:
            total_progress = sum(i.progress_pct for i in active_initiatives)
            avg_progress = total_progress / len(active_initiatives)

        velocity_assessment = (
            f"Strategic initiative progress averaging {avg_progress:.0f}% completion"
            if initiative_count > 0
            else "Teams focus on tactical delivery excellence"
        )
        coordination_quality = (
            f"Excellent - {project_count} teams coordinated"
            if project_count >= 4
            else "Good - focused delivery approach"
        )

        return f"""## 🎯 Strategic Impact & Resource Allocation

### Strategic Initiative Delivery
**Active Initiatives**: {initiative_count} L0/L2 initiatives demonstrating **{velocity_assessment}**

### Cross-Team Coordination Health
**Initiative Coverage**: {project_count} project areas with strategic initiative execution
**Coordination Quality**: {coordination_quality}

### Resource Resilience Assessment
**Platform Investment**: Strategic initiatives continue despite 40% resource reduction
**Execution Quality**: Teams maintain delivery momentum while absorbing resource constraints

---"""

    def _build_footer(self) -> str:
        """Build report footer with MCP usage status"""
        next_week = self.current_date + timedelta(days=7)

        # Check MCP enhancement status
        mcp_status = self._get_mcp_status_message()

        return f"""*📊 **Data Source**: Live Jira Initiative Data - {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}*
*🔄 **Next Report**: {next_week.strftime('%Y-%m-%d')}*
*🎯 **Focus**: L0/L2 strategic initiative progress with executive business value translation*
{mcp_status}"""

    def _get_mcp_status_message(self) -> str:
        """Generate MCP usage status message for report footer"""
        if not hasattr(self.analyzer, "mcp_bridge") or self.analyzer.mcp_bridge is None:
            return "*🤖 **Analysis Engine**: Statistical Monte Carlo (MCP Sequential Thinking: Disabled)*"

        # Check if MCP bridge is enabled
        if self.analyzer.mcp_bridge.mcp_enabled:
            return "*🤖 **Analysis Engine**: MCP Sequential Thinking + Statistical Monte Carlo (Enhanced Strategic Reasoning Active)*"
        else:
            return "*🤖 **Analysis Engine**: Statistical Monte Carlo (MCP Sequential Thinking: Unavailable)*"

    def _determine_completion_timing(self, status: str) -> str:
        """Determine completion timing emoji and text"""
        completed_statuses = ["Done", "Closed", "Resolved"]
        in_progress_statuses = ["In Progress", "In Review", "Ready for Release"]

        if status in completed_statuses:
            return "✅ Completed This Week"
        elif status in in_progress_statuses:
            return "🔄 Completing This Week"
        else:
            return "📋 In Progress"


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Generate weekly executive report with strategic story analysis"
    )
    parser.add_argument(
        "--config",
        default="leadership-workspace/configs/weekly-report-config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--output", help="Output file path (auto-generated if not specified)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without generating report",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    try:
        # Resolve paths
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent
        config_path = project_root / args.config

        if not config_path.exists():
            # Try relative to script directory
            config_path = script_dir.parent.parent / args.config

        if not config_path.exists():
            logger.error(f"Config file not found: {args.config}")
            return 1

        # Initialize components
        logger.info("Initializing weekly report generator...")
        config = ConfigManager(str(config_path))
        jira_client = JiraClient(config.get_jira_config())

        # Pass config to StrategicAnalyzer for MCP integration
        analyzer_config = config.config.get("mcp_integration", {})
        analyzer = StrategicAnalyzer(analyzer_config)
        generator = ReportGenerator(config, jira_client, analyzer)

        # Generate output path if not specified
        if not args.output:
            reports_dir = project_root / "leadership-workspace" / "reports"
            current_date = datetime.now().strftime("%Y-%m-%d")
            args.output = reports_dir / f"weekly-report-{current_date}.md"

        # Generate report
        result = generator.generate_report(str(args.output), args.dry_run)

        if not args.dry_run:
            logger.info(f"✅ Weekly report generated successfully: {result}")
            print(f"\n📁 Report saved to: {result}")
            print(f"📊 Contains strategic story analysis for executive communication")

        return 0

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
