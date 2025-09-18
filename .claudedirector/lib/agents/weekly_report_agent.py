"""
Weekly Report Generation Agent

Autonomous agent for strategic weekly report generation following ClaudeDirector patterns.
Leverages existing weekly_reporter.py logic for proven Jira integration and report formatting.
Provides Agent pattern orchestration over established reporting infrastructure.

Author: Martin | Platform Architecture
Date: 2025-09-18
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import yaml
from pathlib import Path

from ..core.base_manager import BaseManager
from ..core.types import ProcessingResult
from ..reporting.weekly_reporter import (
    ConfigManager,
    JiraClient,
    StrategicAnalyzer,
    ReportGenerator,
)


@dataclass
class WeeklyReportConfig:
    """Configuration for Weekly Report Agent - simplified to use existing config system"""

    config_file_path: str
    output_file_path: Optional[str] = None
    dry_run: bool = False

    @classmethod
    def from_yaml_config(
        cls, config_path: str, output_path: Optional[str] = None, dry_run: bool = False
    ) -> "WeeklyReportConfig":
        """Create config from existing YAML file path"""
        return cls(
            config_file_path=config_path, output_file_path=output_path, dry_run=dry_run
        )


class WeeklyReportAgent(BaseManager):
    """
    Autonomous Weekly Report Generation Agent

    Agent pattern orchestration over existing weekly_reporter.py infrastructure.
    Leverages proven ConfigManager, JiraClient, StrategicAnalyzer, and ReportGenerator.
    Maintains existing report format and business logic while providing Agent capabilities.
    """

    def __init__(self, config: WeeklyReportConfig):
        # Create BaseManagerConfig for parent class
        from ..core.base_manager import BaseManagerConfig, ManagerType

        base_config = BaseManagerConfig(
            manager_name="weekly_report_agent",
            manager_type=(
                ManagerType.AUTOMATION if hasattr(ManagerType, "AUTOMATION") else None
            ),
            enable_logging=True,
            enable_caching=True,
            enable_metrics=True,
        )

        super().__init__(base_config)
        self.config = config

        # Initialize existing weekly_reporter.py components
        self.config_manager: Optional[ConfigManager] = None
        self.jira_client: Optional[JiraClient] = None
        self.strategic_analyzer: Optional[StrategicAnalyzer] = None
        self.report_generator: Optional[ReportGenerator] = None

        # Initialize components using existing proven logic
        self._initialize_reporting_components()

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """Execute agent operations"""
        if operation == "generate_report":
            return self._generate_report_sync()
        elif operation == "test_connection":
            return self._test_jira_connection()
        elif operation == "validate_config":
            return self._validate_configuration()
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _test_jira_connection(self) -> ProcessingResult:
        """Test Jira connection status using existing JiraClient"""
        if self.jira_client is None:
            return ProcessingResult(
                success=False,
                message="Jira client not initialized",
                data={"status": "not_configured"},
            )

        try:
            # Test connection with a simple JQL query
            test_jql = "project is not empty AND key in (DUMMY-1)"
            self.jira_client.fetch_issues(test_jql, max_results=1)
            return ProcessingResult(
                success=True,
                message="Jira connection successful",
                data={"status": "connected", "base_url": self.jira_client.base_url},
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                message=f"Jira connection failed: {str(e)}",
                data={"status": "connection_failed", "error": str(e)},
            )

    def _validate_configuration(self) -> ProcessingResult:
        """Validate agent configuration using existing ConfigManager validation"""
        try:
            # Check if config file exists
            config_path = Path(self.config.config_file_path)
            if not config_path.exists():
                return ProcessingResult(
                    success=False,
                    message=f"Configuration file not found: {self.config.config_file_path}",
                    data={"file_exists": False},
                )

            # Validate using existing ConfigManager
            if self.config_manager is None:
                self._initialize_reporting_components()

            # If ConfigManager initialization succeeded, validation passed
            jira_config = self.config_manager.get_jira_config()
            jql_queries = self.config_manager.config.get("jql_queries", {})

            return ProcessingResult(
                success=True,
                message="Configuration validation passed",
                data={
                    "config_file": str(config_path),
                    "jira_configured": bool(jira_config),
                    "jql_queries_count": len(jql_queries),
                    "base_url": jira_config.get("base_url", "not_configured"),
                },
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                message=f"Configuration validation failed: {str(e)}",
                data={"error": str(e)},
            )

    def _initialize_reporting_components(self) -> None:
        """Initialize all reporting components using existing weekly_reporter.py infrastructure"""
        try:
            # Initialize ConfigManager with existing YAML configuration
            self.config_manager = ConfigManager(self.config.config_file_path)
            self.logger.info(
                f"ConfigManager initialized with {self.config.config_file_path}"
            )

            # Initialize JiraClient with config
            jira_config = self.config_manager.get_jira_config()
            self.jira_client = JiraClient(jira_config)
            self.logger.info("JiraClient initialized with existing authentication")

            # Initialize StrategicAnalyzer
            self.strategic_analyzer = StrategicAnalyzer()
            self.logger.info("StrategicAnalyzer initialized")

            # Initialize ReportGenerator with all components
            self.report_generator = ReportGenerator(
                config=self.config_manager,
                jira_client=self.jira_client,
                analyzer=self.strategic_analyzer,
            )
            self.logger.info("ReportGenerator initialized with existing proven logic")

        except Exception as e:
            self.logger.error(f"Failed to initialize reporting components: {e}")
            raise

    def _generate_report_sync(self) -> ProcessingResult:
        """
        Generate weekly report using existing ReportGenerator

        Synchronous wrapper around existing proven report generation logic.
        Maintains existing report format and business logic.
        """
        start_time = datetime.now()

        try:
            if self.report_generator is None:
                raise RuntimeError("Report generator not initialized")

            self.logger.info(
                "Starting weekly report generation using existing proven logic"
            )

            # Use existing ReportGenerator.generate_report method
            report_content = self.report_generator.generate_report(
                output_path=self.config.output_file_path, dry_run=self.config.dry_run
            )

            elapsed_time = datetime.now() - start_time

            return ProcessingResult(
                success=True,
                message=f"Weekly report generated successfully in {elapsed_time.total_seconds():.1f}s",
                data={
                    "report_content": report_content,
                    "generation_time": elapsed_time.total_seconds(),
                    "output_file": self.config.output_file_path,
                    "dry_run": self.config.dry_run,
                    "config_file": self.config.config_file_path,
                },
            )

        except Exception as e:
            self.logger.error(f"Weekly report generation failed: {e}")
            return ProcessingResult(
                success=False,
                message=f"Report generation failed: {str(e)}",
                data={"error_type": type(e).__name__, "error": str(e)},
            )

    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration for agent status"""
        if not self.config_manager:
            return {"status": "not_initialized"}

        jira_config = self.config_manager.get_jira_config()
        jql_queries = self.config_manager.config.get("jql_queries", {})

        return {
            "status": "initialized",
            "config_file": self.config.config_file_path,
            "jira_base_url": jira_config.get("base_url", "not_configured"),
            "jql_queries_available": list(jql_queries.keys()),
            "query_count": len(jql_queries),
        }

    def get_jira_status(self) -> Dict[str, Any]:
        """Get Jira client connection status"""
        if not self.jira_client:
            return {"status": "not_initialized"}

        return {
            "status": "connected",
            "base_url": self.jira_client.base_url,
            "email": self.jira_client.email,
            "auth_configured": bool(self.jira_client.api_token),
        }

    @classmethod
    def create_from_config_file(
        cls, config_path: str, output_path: Optional[str] = None, dry_run: bool = False
    ) -> "WeeklyReportAgent":
        """Create agent instance from existing YAML configuration file"""
        config = WeeklyReportConfig.from_yaml_config(
            config_path=config_path, output_path=output_path, dry_run=dry_run
        )
        return cls(config)

    def generate_weekly_report_async(self) -> ProcessingResult:
        """Async wrapper for generate report - for backward compatibility"""
        return self._generate_report_sync()


# Convenience function for direct usage
def create_weekly_report_agent(
    config_path: str, output_path: Optional[str] = None, dry_run: bool = False
) -> WeeklyReportAgent:
    """Create WeeklyReportAgent with existing configuration"""
    return WeeklyReportAgent.create_from_config_file(
        config_path=config_path, output_path=output_path, dry_run=dry_run
    )
