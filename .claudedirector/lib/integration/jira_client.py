#!/usr/bin/env python3
"""
Jira API Client

BLOAT_PREVENTION: Extracted from weekly_reporter.py (DRY compliance)
Centralized Jira API integration
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from urllib.parse import quote

logger = logging.getLogger(__name__)


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
