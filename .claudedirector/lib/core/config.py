#!/usr/bin/env python3
"""
ClaudeDirector Configuration System

CRITICAL: This module centralizes all hard-coded values to enable SOLID refactoring.
Provides type-safe configuration access with validation and backwards compatibility.

Requirements from regression tests:
- Must provide get() interface
- Must support threshold access
- Must validate ranges and enum values
- Must maintain backwards compatibility
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThresholdConfig:
    """Threshold configuration with validation"""

    quality_threshold: float = 0.7
    complexity_threshold: float = 0.4
    confidence_threshold: float = 0.8
    stakeholder_auto_create_threshold: float = 0.85
    stakeholder_profiling_threshold: float = 0.6
    conversation_quality_minimum: float = 0.7
    performance_degradation_limit: float = 0.05

    def __post_init__(self):
        """Validate threshold ranges"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Threshold {field_name} must be numeric, got {type(value)}"
                )
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Threshold {field_name} must be between 0.0 and 1.0, got {value}"
                )


@dataclass
class EnumConfig:
    """Enumeration values configuration"""

    priority_levels: List[str] = field(
        default_factory=lambda: ["urgent", "high", "medium", "low"]
    )
    health_statuses: List[str] = field(
        default_factory=lambda: ["excellent", "healthy", "at_risk", "failing"]
    )
    decision_types: List[str] = field(
        default_factory=lambda: [
            "strategic",
            "operational",
            "technical",
            "organizational",
        ]
    )
    stakeholder_types: List[str] = field(
        default_factory=lambda: ["stakeholder", "internal", "external", "executive"]
    )
    risk_levels: List[str] = field(
        default_factory=lambda: ["low", "medium", "high", "critical"]
    )
    complexity_levels: List[str] = field(
        default_factory=lambda: ["simple", "moderate", "complex", "very_complex"]
    )

    def __post_init__(self):
        """Validate enum configurations"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, list):
                raise ValueError(f"Enum {field_name} must be a list, got {type(value)}")
            if not all(isinstance(item, str) for item in value):
                raise ValueError(f"All items in {field_name} must be strings")
            if len(value) == 0:
                raise ValueError(f"Enum {field_name} cannot be empty")


@dataclass
class SecurityConfig:
    """Security scanner configuration"""

    severity_levels: List[str] = field(
        default_factory=lambda: ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    )
    stakeholder_patterns: List[str] = field(
        default_factory=lambda: [
            r"(?i)(stakeholder[_\s-]?data|strategic[_\s-]?intelligence)",
            r"(?i)(platform[_\s-]?opposition[_\s-]?mapping[_\s-]?data)",
            r"(?i)(slt[_\s-]?resistance[_\s-]?pattern[_\s-]?analysis)",
        ]
    )
    strategic_intelligence_patterns: List[str] = field(
        default_factory=lambda: [
            r"(?i)(quarterly[_\s-]?revenue[_\s-]?data[_\s-]?\$)",
            r"(?i)(competitive[_\s-]?intelligence[_\s-]?report)",
            r"(?i)(customer[_\s-]?acquisition[_\s-]?cost[_\s-]?\$)",
            r"(?i)(internal[_\s-]?strategy[_\s-]?document[_\s-]?confidential)",
        ]
    )


@dataclass
class MessageConfig:
    """Message templates configuration"""

    framework_detection_message: str = (
        "📚 Strategic Framework: {framework_name} detected"
    )
    mcp_enhancement_message: str = (
        "🔧 Accessing MCP Server: {server_name} ({capability})"
    )
    persona_activation_message: str = "{emoji} {name} | {domain}"
    p0_failure_message: str = "❌ BLOCKING FAILURE: {test_name} failed"
    quality_threshold_message: str = (
        "⚠️ Quality below threshold ({score:.2f} < {threshold:.2f})"
    )

    def __post_init__(self):
        """Validate message templates"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str):
                raise ValueError(
                    f"Message {field_name} must be a string, got {type(value)}"
                )
            if len(value.strip()) == 0:
                raise ValueError(f"Message {field_name} cannot be empty")


@dataclass
class PathConfig:
    """File path configuration"""

    strategic_memory_db: str = "data/strategic/strategic_memory.db"
    user_config_path: str = ".claudedirector/config/user_identity.yaml"
    p0_test_definitions: str = (
        ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml"
    )
    quality_reports_dir: str = ".claudedirector/reports/quality"
    backup_dir: str = ".claudedirector/backups"

    def __post_init__(self):
        """Validate path configurations"""
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str):
                raise ValueError(
                    f"Path {field_name} must be a string, got {type(value)}"
                )
            if len(value.strip()) == 0:
                raise ValueError(f"Path {field_name} cannot be empty")


class ClaudeDirectorConfig:
    """
    Central configuration system for ClaudeDirector

    Provides type-safe access to all configuration values with validation.
    Supports both dict-like access and property access for backwards compatibility.
    """

    def __init__(self, config_file: Optional[Path] = None):
        """Initialize configuration system"""
        self.config_file = (
            config_file
            or Path.home() / ".claudedirector" / "config" / "system_config.yaml"
        )

        # Initialize with defaults
        self.thresholds = ThresholdConfig()
        self.enums = EnumConfig()
        self.security = SecurityConfig()
        self.messages = MessageConfig()
        self.paths = PathConfig()

        # Load custom configuration if available
        self._load_config()

        # Create lookup dictionary for backwards compatibility
        self._create_lookup_dict()

    def _load_config(self):
        """Load configuration from YAML file if it exists"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

                # Update thresholds
                if "thresholds" in config_data:
                    for key, value in config_data["thresholds"].items():
                        if hasattr(self.thresholds, key):
                            setattr(self.thresholds, key, value)

                # Update enums
                if "enums" in config_data:
                    for key, value in config_data["enums"].items():
                        if hasattr(self.enums, key):
                            setattr(self.enums, key, value)

                # Update messages
                if "messages" in config_data:
                    for key, value in config_data["messages"].items():
                        if hasattr(self.messages, key):
                            setattr(self.messages, key, value)

                # Update paths
                if "paths" in config_data:
                    for key, value in config_data["paths"].items():
                        if hasattr(self.paths, key):
                            setattr(self.paths, key, value)

                logger.info(f"Configuration loaded from {self.config_file}")

            except Exception as e:
                logger.warning(
                    f"Failed to load configuration from {self.config_file}: {e}"
                )
                logger.info("Using default configuration")

    def _create_lookup_dict(self):
        """Create lookup dictionary for backwards compatibility"""
        self._lookup = {}

        # Add thresholds
        for key, value in self.thresholds.__dict__.items():
            self._lookup[key] = value
            self._lookup[f"threshold_{key}"] = value

        # Add enums
        for key, value in self.enums.__dict__.items():
            self._lookup[key] = value
            self._lookup[f"enum_{key}"] = value

        # Add security
        for key, value in self.security.__dict__.items():
            self._lookup[key] = value
            self._lookup[f"security_{key}"] = value

        # Add messages
        for key, value in self.messages.__dict__.items():
            self._lookup[key] = value
            self._lookup[f"message_{key}"] = value

        # Add paths
        for key, value in self.paths.__dict__.items():
            self._lookup[key] = value
            self._lookup[f"path_{key}"] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dict-like interface)"""
        return self._lookup.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Dict-like access"""
        if key not in self._lookup:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._lookup[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._lookup

    def get_threshold(self, name: str) -> float:
        """Get threshold value with validation"""
        threshold_key = name if hasattr(self.thresholds, name) else f"{name}_threshold"

        if hasattr(self.thresholds, name):
            return getattr(self.thresholds, name)
        elif hasattr(self.thresholds, threshold_key):
            return getattr(self.thresholds, threshold_key)
        else:
            raise ValueError(f"Unknown threshold: {name}")

    def get_enum_values(self, category: str) -> List[str]:
        """Get enum values for category"""
        if hasattr(self.enums, category):
            return getattr(self.enums, category)
        else:
            raise ValueError(f"Unknown enum category: {category}")

    def get_message_template(self, name: str) -> str:
        """Get message template"""
        if hasattr(self.messages, name):
            return getattr(self.messages, name)
        else:
            raise ValueError(f"Unknown message template: {name}")

    def get_path(self, name: str) -> str:
        """Get file path"""
        if hasattr(self.paths, name):
            return getattr(self.paths, name)
        else:
            raise ValueError(f"Unknown path: {name}")

    def validate_all(self) -> List[str]:
        """Validate all configuration values"""
        errors = []

        try:
            # Validate thresholds (done in __post_init__)
            ThresholdConfig(**self.thresholds.__dict__)
        except Exception as e:
            errors.append(f"Threshold validation failed: {e}")

        try:
            # Validate enums (done in __post_init__)
            EnumConfig(**self.enums.__dict__)
        except Exception as e:
            errors.append(f"Enum validation failed: {e}")

        try:
            # Validate messages (done in __post_init__)
            MessageConfig(**self.messages.__dict__)
        except Exception as e:
            errors.append(f"Message validation failed: {e}")

        try:
            # Validate paths (done in __post_init__)
            PathConfig(**self.paths.__dict__)
        except Exception as e:
            errors.append(f"Path validation failed: {e}")

        return errors

    def save_config(self):
        """Save current configuration to file"""
        config_data = {
            "thresholds": self.thresholds.__dict__,
            "enums": self.enums.__dict__,
            "security": self.security.__dict__,
            "messages": self.messages.__dict__,
            "paths": self.paths.__dict__,
        }

        # Ensure directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=True)

        logger.info(f"Configuration saved to {self.config_file}")

    def get_all_keys(self) -> List[str]:
        """Get all available configuration keys"""
        return list(self._lookup.keys())

    def get_consolidated_hardcoded_values(self) -> Dict[str, Any]:
        """Get all hard-coded values that should be replaced with config access"""
        return {
            # Most common hard-coded thresholds identified by regression tests
            "0.7": self.get_threshold("quality_threshold"),
            "0.85": self.get_threshold("stakeholder_auto_create_threshold"),
            "0.8": self.get_threshold("confidence_threshold"),
            "0.4": self.get_threshold("complexity_threshold"),
            "0.5": self.get_threshold("performance_degradation_limit")
            * 10,  # 0.05 * 10 = 0.5
            "0.6": self.get_threshold("stakeholder_profiling_threshold"),
            # Common string patterns
            "strategic": "strategic",
            "operational": "operational",
            "technical": "technical",
            "organizational": "organizational",
            "stakeholder": "stakeholder",
            "urgent": self.get_enum_values("priority_levels")[0],
            "high": self.get_enum_values("priority_levels")[1],
            "medium": self.get_enum_values("priority_levels")[2],
            "low": self.get_enum_values("priority_levels")[3],
        }


# Global configuration instance
_config_instance: Optional[ClaudeDirectorConfig] = None


def get_config() -> ClaudeDirectorConfig:
    """Get global configuration instance (singleton pattern)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ClaudeDirectorConfig()
    return _config_instance


def reload_config():
    """Force reload of configuration"""
    global _config_instance
    _config_instance = None
    return get_config()


# Convenience functions for backwards compatibility
def get_threshold(name: str) -> float:
    """Get threshold value (backwards compatible)"""
    return get_config().get_threshold(name)


def get_enum_values(category: str) -> List[str]:
    """Get enum values (backwards compatible)"""
    return get_config().get_enum_values(category)


def get_message_template(name: str) -> str:
    """Get message template (backwards compatible)"""
    return get_config().get_message_template(name)


def get_path(name: str) -> str:
    """Get file path (backwards compatible)"""
    return get_config().get_path(name)


# Export main classes and functions
__all__ = [
    "ClaudeDirectorConfig",
    "ThresholdConfig",
    "EnumConfig",
    "MessageConfig",
    "PathConfig",
    "get_config",
    "reload_config",
    "get_threshold",
    "get_enum_values",
    "get_message_template",
    "get_path",
]
