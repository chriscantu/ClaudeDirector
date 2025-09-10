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
                "fields": "summary,key,status,assignee,project,priority,parent,watchers,issuelinks,description",
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
    """Analyzes story strategic impact and business value"""

    def __init__(self):
        self.jira_base_url = os.getenv(
            "JIRA_BASE_URL", "https://***REMOVED***"
        )

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
        elif "***REMOVED*** Explore" in cleaned:
            return "***REMOVED*** Explore Full Product Life Cycle"

        return cleaned


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
            assignee=fields.get("assignee", {}).get("displayName", "Unassigned"),
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
        """Build epic portfolio section"""
        if not epic_issues:
            return """## 📊 Completed Epic Portfolio by Team

**No epics completed this week** - this is the second consecutive week with 0 epic completions.

**Note**: Teams demonstrate high velocity in sprint reviews, indicating a measurement gap between tactical execution and epic-level reporting.

---"""

        epic_entries = []
        for issue in epic_issues:
            timing = self._determine_completion_timing(issue.status)
            jira_url = f"{self.analyzer.jira_base_url}/browse/{issue.key}"

            entry = f"""### ✅ [{issue.key}]({jira_url}) - {issue.summary}

- **Status**: {timing} ({issue.status})
- **Priority**: {issue.priority}
- **Project**: {issue.project}
- **Assignee**: {issue.assignee}
- **Business Value**: {issue.business_value}

---"""
            epic_entries.append(entry)

        return f"""## 📊 Completed Epic Portfolio by Team

{''.join(epic_entries)}

---"""

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

        # Analyze strategic impact for each story
        strategic_entries = []
        for issue in strategic_issues:
            score = self.analyzer.calculate_strategic_impact(issue)
            if score.score >= 5:  # Only show high-impact stories
                timing = self._determine_completion_timing(issue.status)
                jira_url = f"{self.analyzer.jira_base_url}/browse/{issue.key}"

                entry = f"""#### 📋 [{issue.key}]({jira_url}) - {issue.summary}

- **Status**: {timing} ({issue.status})
- **Project**: {issue.project}
- **Strategic Impact**: {score.score}/10 points
- **Business Value**: {' '.join(score.indicators)}

---"""
                strategic_entries.append(entry)

        high_impact_count = len(strategic_entries)

        content = f"""## 🚀 Strategic Story Impact Analysis

### Executive Story Highlights

**High-Impact Completions**: {high_impact_count} strategic stories completed or completing this week

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
            "***REMOVED*** Initiatives": "Strategic Initiatives",
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
        """Build report footer"""
        next_week = self.current_date + timedelta(days=7)
        return f"""*📊 **Data Source**: Live Jira Initiative Data - {self.current_date.strftime('%Y-%m-%d %H:%M:%S')}*
*🔄 **Next Report**: {next_week.strftime('%Y-%m-%d')}*
*🎯 **Focus**: L0/L2 strategic initiative progress with executive business value translation*"""

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
        analyzer = StrategicAnalyzer()
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
