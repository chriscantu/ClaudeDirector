#!/usr/bin/env python3
"""
Jira Configuration Management

BLOAT_PREVENTION: Extracted from weekly_reporter.py (DRY compliance)
Centralized configuration management for Jira integration
"""

import yaml
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


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
