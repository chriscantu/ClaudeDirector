"""
JIRA Integration Client

Smart JIRA client with caching and on-demand sync strategy
for ClaudeDirector P2.1 Executive Communication features.
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import sqlite3
from pathlib import Path

from ..interfaces.report_interface import IDataSource


@dataclass
class JIRAConfig:
    """JIRA connection configuration."""

    base_url: str
    username: str
    api_token: str
    project_keys: List[str]
    cache_ttl_hours: int = 2
    rate_limit_calls_per_hour: int = 1000


@dataclass
class CachedData:
    """Cached JIRA data with metadata."""

    data: Dict[str, Any]
    timestamp: datetime
    source: str
    freshness_hours: float


class JIRAIntegrationClient(IDataSource):
    """
    JIRA integration client with smart caching strategy.

    Implements on-demand sync pattern:
    - Fetches fresh data only when CLI commands are executed
    - Uses cached data if less than 2 hours old
    - Provides graceful degradation when JIRA unavailable
    """

    def __init__(self, config: JIRAConfig, cache_db_path: str = "memory/jira_cache.db"):
        self.config = config
        self.cache_db_path = Path(cache_db_path)
        self._init_cache_db()
        self._last_api_call = 0
        self._api_call_count = 0

    def _init_cache_db(self) -> None:
        """Initialize SQLite cache database."""
        self.cache_db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jira_cache (
                    key TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    source TEXT NOT NULL
                )
            """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON jira_cache(timestamp)
            """
            )

    def get_data(self, time_period: str, metrics: List[str]) -> Dict[str, Any]:
        """
        Get JIRA data with smart caching strategy.

        Args:
            time_period: Time period for data (e.g., "30d", "current_sprint")
            metrics: List of metrics to retrieve

        Returns:
            Dictionary containing requested JIRA data
        """
        cache_key = f"{time_period}_{hash(tuple(sorted(metrics)))}"

        # Try to get cached data first
        cached_data = self._get_cached_data(cache_key)
        if cached_data and self._is_cache_fresh(cached_data):
            return cached_data.data

        # Fetch fresh data if cache is stale or missing
        try:
            fresh_data = self._fetch_fresh_data(time_period, metrics)
            self._cache_data(cache_key, fresh_data, "jira_api")
            return fresh_data
        except Exception as e:
            # Graceful degradation: return stale cache if available
            if cached_data:
                print(
                    f"⚠️  JIRA unavailable, using cached data ({cached_data.freshness_hours:.1f}h old)"
                )
                return cached_data.data
            else:
                raise Exception(f"JIRA unavailable and no cached data: {e}")

    def get_data_freshness(self) -> str:
        """Return timestamp of when data was last updated."""
        with sqlite3.connect(self.cache_db_path) as conn:
            cursor = conn.execute(
                """
                SELECT MAX(timestamp) FROM jira_cache
            """
            )
            max_timestamp = cursor.fetchone()[0]

        if max_timestamp:
            last_update = datetime.fromtimestamp(max_timestamp)
            return last_update.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "No data available"

    def is_available(self) -> bool:
        """Check if JIRA is currently available."""
        try:
            # Simple connectivity check with rate limiting
            if self._should_rate_limit():
                return False

            # TODO: Implement actual JIRA ping
            # For now, assume available
            return True
        except Exception:
            return False

    def _get_cached_data(self, cache_key: str) -> Optional[CachedData]:
        """Retrieve data from cache."""
        with sqlite3.connect(self.cache_db_path) as conn:
            cursor = conn.execute(
                """
                SELECT data, timestamp, source
                FROM jira_cache
                WHERE key = ?
            """,
                (cache_key,),
            )

            row = cursor.fetchone()
            if not row:
                return None

            data, timestamp, source = row
            cached_timestamp = datetime.fromtimestamp(timestamp)
            freshness_hours = (datetime.now() - cached_timestamp).total_seconds() / 3600

            return CachedData(
                data=json.loads(data),
                timestamp=cached_timestamp,
                source=source,
                freshness_hours=freshness_hours,
            )

    def _is_cache_fresh(self, cached_data: CachedData) -> bool:
        """Check if cached data is still fresh."""
        return cached_data.freshness_hours < self.config.cache_ttl_hours

    def _cache_data(self, cache_key: str, data: Dict[str, Any], source: str) -> None:
        """Store data in cache."""
        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO jira_cache (key, data, timestamp, source)
                VALUES (?, ?, ?, ?)
            """,
                (cache_key, json.dumps(data), time.time(), source),
            )

    def _fetch_fresh_data(self, time_period: str, metrics: List[str]) -> Dict[str, Any]:
        """
        Fetch fresh data from JIRA API.

        This is a placeholder implementation that would integrate with
        the actual JIRA REST API.
        """
        if self._should_rate_limit():
            raise Exception("Rate limit exceeded")

        self._track_api_call()

        # TODO: Implement actual JIRA API calls
        # For now, return mock data structure
        mock_data = {
            "team_velocity": {
                "current_sprint": 42,
                "last_sprint": 38,
                "trend": "increasing",
            },
            "risk_indicators": {
                "blocked_issues": 3,
                "overdue_issues": 5,
                "critical_bugs": 1,
            },
            "cross_team_dependencies": {
                "total_dependencies": 12,
                "blocked_dependencies": 2,
                "at_risk_dependencies": 3,
            },
            "initiative_health": {"on_track": 8, "at_risk": 2, "critical": 1},
            "data_freshness": datetime.now().isoformat(),
            "time_period": time_period,
            "metrics_requested": metrics,
        }

        return mock_data

    def _should_rate_limit(self) -> bool:
        """Check if we should rate limit API calls."""
        current_time = time.time()

        # Reset counter if more than an hour has passed
        if current_time - self._last_api_call > 3600:
            self._api_call_count = 0

        return self._api_call_count >= self.config.rate_limit_calls_per_hour

    def _track_api_call(self) -> None:
        """Track API call for rate limiting."""
        self._api_call_count += 1
        self._last_api_call = time.time()

    def get_velocity_data(self, team_id: str, sprints: int = 5) -> Dict[str, Any]:
        """Get velocity data for a specific team."""
        return self.get_data(
            f"velocity_{team_id}_{sprints}", ["velocity", "story_points"]
        )

    def get_risk_indicators(self, project_keys: List[str]) -> Dict[str, Any]:
        """Get risk indicators for specified projects."""
        return self.get_data("risk_indicators", ["blocked", "overdue", "critical"])

    def get_initiative_status(
        self, time_period: str = "current_quarter"
    ) -> Dict[str, Any]:
        """Get strategic initiative status."""
        return self.get_data(time_period, ["initiatives", "epics", "progress"])


# Configuration helper
def create_jira_client_from_env() -> JIRAIntegrationClient:
    """Create JIRA client from environment variables."""
    import os

    config = JIRAConfig(
        base_url=os.getenv("JIRA_BASE_URL", "https://company.atlassian.net"),
        username=os.getenv("JIRA_USERNAME", ""),
        api_token=os.getenv("JIRA_API_TOKEN", ""),
        project_keys=os.getenv("JIRA_PROJECT_KEYS", "").split(","),
        cache_ttl_hours=int(os.getenv("JIRA_CACHE_TTL_HOURS", "2")),
        rate_limit_calls_per_hour=int(os.getenv("JIRA_RATE_LIMIT", "1000")),
    )

    return JIRAIntegrationClient(config)
