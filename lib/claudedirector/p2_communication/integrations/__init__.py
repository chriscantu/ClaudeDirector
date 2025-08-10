"""
P2.1 Integrations Module

External system integrations for P2.1 Executive Communication.
Includes JIRA client and demo data sources.
"""

from .jira_client import JIRAIntegrationClient, JIRAConfig, create_jira_client_from_env
from .demo_data_source import DemoDataSource
from .alert_system import IntelligentAlertSystem, AlertSeverity, AlertCategory, Alert

__all__ = [
    "JIRAIntegrationClient",
    "JIRAConfig",
    "create_jira_client_from_env",
    "DemoDataSource",
    "IntelligentAlertSystem",
    "AlertSeverity",
    "AlertCategory",
    "Alert",
]
