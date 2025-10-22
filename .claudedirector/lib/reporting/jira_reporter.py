#!/usr/bin/env python3
"""
Duration-Agnostic Jira Reporter - Refactored Core Module
Phase 0: Architectural Refactoring (ADR-004)

BLOAT_PREVENTION: Single source of truth for duration-based Jira reporting.
Extracts duration-agnostic classes from weekly_reporter.py to eliminate hardcoded "weekly" assumptions.

This module supports weekly, 90-day, quarterly, and custom duration reports through a single parameterized implementation.

Author: ClaudeDirector AI Framework (Martin)
Version: 1.0.0 (Phase 0 - Duration-Agnostic Refactoring)
"""

import os
import sys
import json
import yaml
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from urllib.parse import quote
import re
from pathlib import Path

# Configure logging
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
    """Data class for L0/L1/L2 strategic initiatives"""
    
    key: str
    title: str
    level: str  # L0, L1, L2
    progress_pct: int = 0
    status_desc: str = ""
    business_context: str = ""
    team_impact: str = ""
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


class StrategicAnalyzer:
    """
    Analyzes story strategic impact and business value
    
    BLOAT_PREVENTION: Extracted from weekly_reporter.py with core functionality.
    This is the foundation for strategic analysis - no duplication.
    Advanced MCP/Monte Carlo features remain in weekly_reporter.py for now.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.jira_base_url = os.getenv(
            "JIRA_BASE_URL", "https://***REMOVED***"
        )
        self.config = config or {}
    
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
        """
        Generate contextual business value based on project type
        
        SECURITY: Generic fallback only - no hardcoded team/project names
        Project-specific contexts should be configured externally via config files
        """
        # Generic business value - no PII or company-specific data
        return "Strategic platform initiative with cross-organizational impact"
    
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
        """
        Generate executive business context for initiative
        
        SECURITY: Generic patterns only - no company-specific initiative names
        """
        # Generic keyword-based patterns (no company-specific names)
        initiative_contexts = {
            # L0 - Foundational/Compliance (generic security/compliance patterns)
            "security": "Critical security risk mitigation to protect customer data and maintain compliance",
            "compliance": "Regulatory compliance initiative to meet industry standards and audit requirements",
            "audit": "Audit readiness and compliance validation initiative",
            # L2 - Platform/Capabilities (generic capability patterns)
            "build": "Developer productivity enhancement reducing build times and improving development velocity",
            "platform": "Platform capability advancement improving organizational efficiency",
            "tool": "Tooling improvement enabling better developer experience and productivity",
            "international": "Market expansion enablement through localization infrastructure",
            "localization": "Localization capability enhancement for international market support",
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
        """
        Clean up initiative title for executive presentation
        
        SECURITY: Generic cleaning only - no hardcoded initiative names
        Initiative-specific formatting should be configured externally
        """
        # Remove generic Jira formatting and technical prefixes
        cleaned = (
            summary.replace("Layer 0 -", "L0 -")
            .replace("Layer 2 -", "L2 -")
            .replace("Layer 1 -", "L1 -")
        )
        cleaned = cleaned.strip()
        
        return cleaned


class JiraReporter:
    """
    Duration-Agnostic Jira Reporter Base Class
    
    BLOAT_PREVENTION: Single source of truth for all duration-based reports.
    Accepts duration_days parameter to support weekly (7), 90-day (90), quarterly (91), 
    monthly (30), and custom duration reports.
    
    This eliminates the need for separate weekly_reporter, monthly_reporter, quarterly_reporter modules.
    """
    
    def __init__(self, config: ConfigManager, duration_days: int = 7):
        """
        Initialize duration-agnostic Jira reporter
        
        Args:
            config: ConfigManager instance with Jira configuration
            duration_days: Duration window for report (default: 7 for weekly)
        """
        self.config = config
        self.duration_days = duration_days
        self.duration_label = self._get_duration_label(duration_days)
        
        logger.info(f"JiraReporter initialized: {self.duration_label} report ({self.duration_days} days)")
    
    @staticmethod
    def _get_duration_label(days: int) -> str:
        """
        Generate human-readable duration label
        
        Args:
            days: Number of days in report window
        
        Returns:
            String label (e.g., "Weekly", "90-Day", "2-Week")
        """
        if days == 7:
            return "Weekly"
        elif days == 30:
            return "Monthly"
        elif days == 90:
            return "90-Day"
        elif days == 91:
            return "Quarterly"  # Support both 90 and 91 for quarterly
        elif days % 7 == 0:
            weeks = days // 7
            return f"{weeks}-Week"
        else:
            return f"{days}-Day"
    
    def _calculate_start_date(self, end_date: datetime) -> datetime:
        """
        Calculate start date based on duration
        
        Args:
            end_date: End date for report window
        
        Returns:
            Start date (end_date - duration_days)
        """
        return end_date - timedelta(days=self.duration_days)
    
    def _build_jql_date_filter(self, end_date: Optional[datetime] = None) -> str:
        """
        Build JQL date filter for duration window
        
        Args:
            end_date: End date for report (default: now)
        
        Returns:
            JQL date filter string (e.g., "-7d", "-90d")
        """
        return f"-{self.duration_days}d"
    
    def _get_log_file_path(self) -> Path:
        """
        Get duration-agnostic log file path
        
        Returns:
            Path to jira_report.log (not weekly_report.log)
        """
        project_root = Path(__file__).parent.parent.parent
        return project_root / "jira_report.log"
    
    def _get_report_header(self) -> str:
        """
        Generate duration-aware report header
        
        Returns:
            Report header string with duration label
        """
        return f"{self.duration_label} Executive Report"
    
    def _get_report_description(self) -> str:
        """
        Generate duration-aware report description
        
        Returns:
            Description string (e.g., "this week", "this 90-day period")
        """
        duration_lower = self.duration_label.lower()
        
        if duration_lower == "weekly":
            return "this week"
        elif duration_lower == "monthly":
            return "this month"
        elif duration_lower == "quarterly":
            return "this quarter"
        else:
            return f"this {duration_lower} period"
    
    def _calculate_next_report_date(self, current_date: datetime) -> datetime:
        """
        Calculate next report date based on duration
        
        Args:
            current_date: Current report date
        
        Returns:
            Next report date (current_date + duration_days)
        """
        return current_date + timedelta(days=self.duration_days)


# BLOAT_PREVENTION: Export all classes for backward compatibility
__all__ = [
    "JiraReporter",
    "JiraClient",
    "StrategicAnalyzer",
    "ConfigManager",
    "JiraIssue",
    "StrategicScore",
    "Initiative",
]

