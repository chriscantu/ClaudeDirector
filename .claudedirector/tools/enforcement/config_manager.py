#!/usr/bin/env python3
"""
🚨 ENFORCEMENT CONFIGURATION MANAGEMENT SYSTEM
Centralized configuration for Real-Time Development Process Enforcement

SOLID Principles Applied:
- Single Responsibility: ConfigManager handles only configuration concerns
- Open/Closed: Extensible through ConfigLoader and ConfigValidator interfaces
- Liskov Substitution: All config loaders/validators interchangeable
- Interface Segregation: Separate interfaces for loading, validation, and watching
- Dependency Inversion: Depends on abstract interfaces, not concrete implementations

DRY Principle Applied:
- Single configuration management across all enforcement components
- Centralized default values eliminate duplication
- Reusable configuration patterns for all gates

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import os
import yaml
import json
import time
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Union, Callable, Set
from pathlib import Path
from enum import Enum
from contextlib import contextmanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .base_enforcement import EnforcementLevel, ViolationType


class ConfigFormat(Enum):
    """
    Configuration file formats following DRY principle.
    Single source of truth for supported formats.
    """

    YAML = "yaml"
    JSON = "json"
    TOML = "toml"


@dataclass(frozen=True)
class GateConfig:
    """
    Configuration for individual enforcement gate.

    Immutable configuration following SOLID Single Responsibility.
    """

    enabled: bool = True
    level: EnforcementLevel = EnforcementLevel.MANDATORY
    timeout_seconds: float = 5.0
    retry_count: int = 0
    retry_delay_seconds: float = 1.0
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate gate configuration"""
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.retry_count < 0:
            raise ValueError("retry_count cannot be negative")
        if self.retry_delay_seconds < 0:
            raise ValueError("retry_delay_seconds cannot be negative")


@dataclass(frozen=True)
class PerformanceConfig:
    """
    Performance-related configuration.

    Immutable configuration following SOLID Single Responsibility.
    """

    max_validation_time_seconds: float = 5.0
    max_alert_time_seconds: float = 1.0
    max_completion_time_seconds: float = 10.0
    parallel_gate_execution: bool = True
    cache_validation_results: bool = True
    cache_ttl_seconds: float = 300.0  # 5 minutes

    def __post_init__(self):
        """Validate performance configuration"""
        if self.max_validation_time_seconds <= 0:
            raise ValueError("max_validation_time_seconds must be positive")
        if self.max_alert_time_seconds <= 0:
            raise ValueError("max_alert_time_seconds must be positive")
        if self.max_completion_time_seconds <= 0:
            raise ValueError("max_completion_time_seconds must be positive")
        if self.cache_ttl_seconds <= 0:
            raise ValueError("cache_ttl_seconds must be positive")


@dataclass(frozen=True)
class AuditConfig:
    """
    Audit logging configuration.

    Immutable configuration following SOLID Single Responsibility.
    """

    enabled: bool = True
    log_directory: str = ".claudedirector/logs"
    retention_days: int = 90
    max_file_size_mb: int = 10
    max_files: int = 10
    compress_old_files: bool = True
    log_format: str = "json"  # json or human
    include_context: bool = True

    def __post_init__(self):
        """Validate audit configuration"""
        if self.retention_days <= 0:
            raise ValueError("retention_days must be positive")
        if self.max_file_size_mb <= 0:
            raise ValueError("max_file_size_mb must be positive")
        if self.max_files <= 0:
            raise ValueError("max_files must be positive")
        if self.log_format not in ["json", "human"]:
            raise ValueError("log_format must be 'json' or 'human'")


@dataclass(frozen=True)
class EnforcementConfig:
    """
    Main enforcement system configuration.

    Immutable configuration following SOLID Single Responsibility.
    This class has ONE responsibility: represent complete enforcement configuration.
    """

    # Gate configurations
    gates: Dict[str, GateConfig] = field(default_factory=dict)

    # System configurations
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)

    # Global settings
    fail_fast: bool = False
    bypass_options: Dict[str, bool] = field(
        default_factory=lambda: {
            "emergency_bypass": False,
            "developer_override": False,
            "admin_override": False,
        }
    )

    # Environment settings
    environment: str = "production"
    debug_mode: bool = False

    def __post_init__(self):
        """Validate enforcement configuration"""
        if not isinstance(self.gates, dict):
            raise ValueError("gates must be a dictionary")
        if self.environment not in ["development", "staging", "production"]:
            raise ValueError("environment must be development, staging, or production")

    def get_gate_config(self, gate_name: str) -> GateConfig:
        """
        Get configuration for specific gate.

        Args:
            gate_name: Name of the gate

        Returns:
            GateConfig for the gate, or default if not configured
        """
        return self.gates.get(gate_name, GateConfig())

    def is_gate_enabled(self, gate_name: str) -> bool:
        """Check if gate is enabled"""
        return self.get_gate_config(gate_name).enabled

    def get_gate_timeout(self, gate_name: str) -> float:
        """Get timeout for specific gate"""
        return self.get_gate_config(gate_name).timeout_seconds

    def is_bypass_enabled(self, bypass_type: str) -> bool:
        """Check if bypass option is enabled"""
        return self.bypass_options.get(bypass_type, False)


class ConfigLoader(ABC):
    """
    Abstract configuration loader interface following SOLID Interface Segregation.

    Single responsibility: Load configuration from various sources.
    """

    @abstractmethod
    def load_config(self, source: str) -> Dict[str, Any]:
        """Load configuration from source"""
        pass

    @abstractmethod
    def supports_format(self, format_type: ConfigFormat) -> bool:
        """Check if loader supports format"""
        pass


class YamlConfigLoader(ConfigLoader):
    """
    YAML configuration loader following SOLID Single Responsibility.

    Single responsibility: Load configuration from YAML files.
    """

    def load_config(self, source: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(source, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {source}: {e}")
        except (IOError, OSError) as e:
            raise ValueError(f"Cannot read {source}: {e}")

    def supports_format(self, format_type: ConfigFormat) -> bool:
        """Check if supports YAML format"""
        return format_type == ConfigFormat.YAML


class JsonConfigLoader(ConfigLoader):
    """
    JSON configuration loader following SOLID Single Responsibility.

    Single responsibility: Load configuration from JSON files.
    """

    def load_config(self, source: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(source, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {source}: {e}")
        except (IOError, OSError) as e:
            raise ValueError(f"Cannot read {source}: {e}")

    def supports_format(self, format_type: ConfigFormat) -> bool:
        """Check if supports JSON format"""
        return format_type == ConfigFormat.JSON


class ConfigValidator(ABC):
    """
    Abstract configuration validator interface following SOLID Interface Segregation.

    Single responsibility: Validate configuration data.
    """

    @abstractmethod
    def validate_config(self, config_data: Dict[str, Any]) -> List[str]:
        """
        Validate configuration data.

        Returns:
            List of validation error messages (empty if valid)
        """
        pass


class EnforcementConfigValidator(ConfigValidator):
    """
    Enforcement configuration validator following SOLID Single Responsibility.

    Single responsibility: Validate enforcement configuration structure and values.
    """

    def validate_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate enforcement configuration data"""
        errors = []

        # Validate gates section
        if "gates" in config_data:
            gates = config_data["gates"]
            if not isinstance(gates, dict):
                errors.append("'gates' must be a dictionary")
            else:
                for gate_name, gate_config in gates.items():
                    if not isinstance(gate_name, str):
                        errors.append(
                            f"Gate name must be string, got {type(gate_name)}"
                        )

                    if not isinstance(gate_config, dict):
                        errors.append(f"Gate config for {gate_name} must be dictionary")
                        continue

                    # Validate gate config fields
                    if "timeout_seconds" in gate_config:
                        timeout = gate_config["timeout_seconds"]
                        if not isinstance(timeout, (int, float)) or timeout <= 0:
                            errors.append(
                                f"Gate {gate_name} timeout_seconds must be positive number"
                            )

        # Validate performance section
        if "performance" in config_data:
            perf = config_data["performance"]
            if not isinstance(perf, dict):
                errors.append("'performance' must be a dictionary")
            else:
                for field in ["max_validation_time_seconds", "max_alert_time_seconds"]:
                    if field in perf:
                        value = perf[field]
                        if not isinstance(value, (int, float)) or value <= 0:
                            errors.append(
                                f"performance.{field} must be positive number"
                            )

        # Validate audit section
        if "audit" in config_data:
            audit = config_data["audit"]
            if not isinstance(audit, dict):
                errors.append("'audit' must be a dictionary")
            else:
                if "retention_days" in audit:
                    retention = audit["retention_days"]
                    if not isinstance(retention, int) or retention <= 0:
                        errors.append("audit.retention_days must be positive integer")

                if "log_format" in audit:
                    log_format = audit["log_format"]
                    if log_format not in ["json", "human"]:
                        errors.append("audit.log_format must be 'json' or 'human'")

        # Validate environment
        if "environment" in config_data:
            env = config_data["environment"]
            if env not in ["development", "staging", "production"]:
                errors.append(
                    "environment must be 'development', 'staging', or 'production'"
                )

        return errors


class ConfigWatcher(FileSystemEventHandler):
    """
    Configuration file watcher following SOLID Single Responsibility.

    Single responsibility: Monitor configuration files for changes.
    """

    def __init__(self, config_manager: "EnforcementConfigManager"):
        """
        Initialize config watcher.

        Args:
            config_manager: ConfigManager to notify of changes
        """
        self._config_manager = config_manager
        self._debounce_delay = 1.0  # 1 second debounce
        self._last_change_time = 0.0
        self._timer = None
        self._lock = threading.Lock()

    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return

        # Check if it's a config file
        config_files = self._config_manager.get_config_files()
        if Path(event.src_path) in config_files:
            self._schedule_reload()

    def _schedule_reload(self):
        """Schedule config reload with debouncing"""
        with self._lock:
            self._last_change_time = time.time()

            if self._timer:
                self._timer.cancel()

            self._timer = threading.Timer(self._debounce_delay, self._reload_config)
            self._timer.start()

    def _reload_config(self):
        """Reload configuration after debounce period"""
        with self._lock:
            # Check if there were more recent changes
            if time.time() - self._last_change_time >= self._debounce_delay:
                self._config_manager.reload_config()


class EnforcementConfigManager:
    """
    Main configuration manager following SOLID principles.

    SOLID Compliance:
    - Single Responsibility: Manages enforcement system configuration
    - Open/Closed: Extensible through loader and validator interfaces
    - Liskov Substitution: Works with any ConfigLoader/ConfigValidator
    - Interface Segregation: Clean interface for config management
    - Dependency Inversion: Depends on abstract interfaces

    DRY Compliance:
    - Single configuration management for all enforcement components
    - Eliminates duplication of config loading across gates
    """

    def __init__(
        self,
        config_files: Optional[List[Path]] = None,
        loaders: Optional[List[ConfigLoader]] = None,
        validators: Optional[List[ConfigValidator]] = None,
        watch_changes: bool = True,
    ):
        """
        Initialize configuration manager.

        Args:
            config_files: List of configuration files to load
            loaders: List of configuration loaders
            validators: List of configuration validators
            watch_changes: Whether to watch for config file changes
        """
        self._config_files = config_files or []
        self._loaders = loaders or [YamlConfigLoader(), JsonConfigLoader()]
        self._validators = validators or [EnforcementConfigValidator()]
        self._watch_changes = watch_changes

        self._current_config: Optional[EnforcementConfig] = None
        self._config_lock = threading.RLock()
        self._change_callbacks: List[Callable[[EnforcementConfig], None]] = []

        # File watching
        self._observer: Optional[Observer] = None
        self._watcher: Optional[ConfigWatcher] = None

        # Load initial configuration
        self._load_initial_config()

        # Start file watching if enabled
        if self._watch_changes:
            self._start_file_watching()

    def _get_default_config_files(self) -> List[Path]:
        """Get default configuration file locations"""
        project_root = Path.cwd()

        default_locations = [
            project_root / ".claudedirector" / "config" / "enforcement_config.yaml",
            project_root / ".claudedirector" / "config" / "enforcement_config.json",
            project_root / "enforcement_config.yaml",
            project_root / "enforcement_config.json",
        ]

        # Return existing files
        return [path for path in default_locations if path.exists()]

    def _load_initial_config(self):
        """Load initial configuration"""
        if not self._config_files:
            self._config_files = self._get_default_config_files()

        if not self._config_files:
            # Use default configuration
            self._current_config = self._create_default_config()
        else:
            self.reload_config()

    def _create_default_config(self) -> EnforcementConfig:
        """Create default enforcement configuration"""
        default_gates = {
            "sequential_thinking_validator": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=5.0
            ),
            "context7_enforcer": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=3.0
            ),
            "spec_kit_validator": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=2.0
            ),
            "solid_principle_checker": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=4.0
            ),
            "dry_principle_checker": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=3.0
            ),
            "p0_continuous_monitor": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=10.0
            ),
            "bloat_prevention_monitor": GateConfig(
                enabled=True, level=EnforcementLevel.MANDATORY, timeout_seconds=5.0
            ),
        }

        return EnforcementConfig(
            gates=default_gates,
            performance=PerformanceConfig(),
            audit=AuditConfig(),
            fail_fast=False,
            environment="production",
            debug_mode=False,
        )

    def reload_config(self) -> None:
        """Reload configuration from files"""
        with self._config_lock:
            merged_config = {}

            # Load and merge all config files
            for config_file in self._config_files:
                try:
                    config_data = self._load_config_file(config_file)
                    merged_config = self._merge_configs(merged_config, config_data)
                except Exception as e:
                    # Log error but continue with other files
                    print(f"Warning: Failed to load config file {config_file}: {e}")

            # Validate merged configuration
            validation_errors = self._validate_config(merged_config)
            if validation_errors:
                error_msg = "Configuration validation failed:\n" + "\n".join(
                    validation_errors
                )
                raise ValueError(error_msg)

            # Create new configuration
            new_config = self._create_config_from_data(merged_config)

            # Update current configuration
            old_config = self._current_config
            self._current_config = new_config

            # Notify change callbacks
            for callback in self._change_callbacks:
                try:
                    callback(new_config)
                except Exception as e:
                    print(f"Warning: Config change callback failed: {e}")

    def _load_config_file(self, config_file: Path) -> Dict[str, Any]:
        """Load configuration from single file"""
        # Determine format from file extension
        suffix = config_file.suffix.lower()
        format_map = {
            ".yaml": ConfigFormat.YAML,
            ".yml": ConfigFormat.YAML,
            ".json": ConfigFormat.JSON,
        }

        config_format = format_map.get(suffix)
        if not config_format:
            raise ValueError(f"Unsupported config file format: {suffix}")

        # Find appropriate loader
        loader = None
        for l in self._loaders:
            if l.supports_format(config_format):
                loader = l
                break

        if not loader:
            raise ValueError(f"No loader available for format: {config_format}")

        return loader.load_config(str(config_file))

    def _merge_configs(
        self, base: Dict[str, Any], overlay: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge two configuration dictionaries"""
        result = base.copy()

        for key, value in overlay.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _validate_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate configuration data"""
        all_errors = []

        for validator in self._validators:
            errors = validator.validate_config(config_data)
            all_errors.extend(errors)

        return all_errors

    def _create_config_from_data(
        self, config_data: Dict[str, Any]
    ) -> EnforcementConfig:
        """Create EnforcementConfig from dictionary data"""
        # Start with default config
        default_config = self._create_default_config()

        # Parse gates
        gates = {}
        if "gates" in config_data:
            for gate_name, gate_data in config_data["gates"].items():
                gates[gate_name] = GateConfig(
                    enabled=gate_data.get("enabled", True),
                    level=EnforcementLevel(gate_data.get("level", "MANDATORY")),
                    timeout_seconds=gate_data.get("timeout_seconds", 5.0),
                    retry_count=gate_data.get("retry_count", 0),
                    retry_delay_seconds=gate_data.get("retry_delay_seconds", 1.0),
                    custom_settings=gate_data.get("custom_settings", {}),
                )
        else:
            gates = default_config.gates

        # Parse performance config
        performance = default_config.performance
        if "performance" in config_data:
            perf_data = config_data["performance"]
            performance = PerformanceConfig(
                max_validation_time_seconds=perf_data.get(
                    "max_validation_time_seconds", 5.0
                ),
                max_alert_time_seconds=perf_data.get("max_alert_time_seconds", 1.0),
                max_completion_time_seconds=perf_data.get(
                    "max_completion_time_seconds", 10.0
                ),
                parallel_gate_execution=perf_data.get("parallel_gate_execution", True),
                cache_validation_results=perf_data.get(
                    "cache_validation_results", True
                ),
                cache_ttl_seconds=perf_data.get("cache_ttl_seconds", 300.0),
            )

        # Parse audit config
        audit = default_config.audit
        if "audit" in config_data:
            audit_data = config_data["audit"]
            audit = AuditConfig(
                enabled=audit_data.get("enabled", True),
                log_directory=audit_data.get("log_directory", ".claudedirector/logs"),
                retention_days=audit_data.get("retention_days", 90),
                max_file_size_mb=audit_data.get("max_file_size_mb", 10),
                max_files=audit_data.get("max_files", 10),
                compress_old_files=audit_data.get("compress_old_files", True),
                log_format=audit_data.get("log_format", "json"),
                include_context=audit_data.get("include_context", True),
            )

        return EnforcementConfig(
            gates=gates,
            performance=performance,
            audit=audit,
            fail_fast=config_data.get("fail_fast", False),
            bypass_options=config_data.get(
                "bypass_options", default_config.bypass_options
            ),
            environment=config_data.get("environment", "production"),
            debug_mode=config_data.get("debug_mode", False),
        )

    def _start_file_watching(self):
        """Start watching configuration files for changes"""
        if not self._config_files:
            return

        self._watcher = ConfigWatcher(self)
        self._observer = Observer()

        # Watch directories containing config files
        watched_dirs = set()
        for config_file in self._config_files:
            config_dir = config_file.parent
            if config_dir not in watched_dirs:
                self._observer.schedule(self._watcher, str(config_dir), recursive=False)
                watched_dirs.add(config_dir)

        self._observer.start()

    def get_config(self) -> EnforcementConfig:
        """Get current enforcement configuration"""
        with self._config_lock:
            if self._current_config is None:
                self._current_config = self._create_default_config()
            return self._current_config

    def get_config_files(self) -> List[Path]:
        """Get list of configuration files being watched"""
        return self._config_files.copy()

    def add_change_callback(
        self, callback: Callable[[EnforcementConfig], None]
    ) -> None:
        """Add callback for configuration changes"""
        self._change_callbacks.append(callback)

    def remove_change_callback(
        self, callback: Callable[[EnforcementConfig], None]
    ) -> None:
        """Remove configuration change callback"""
        if callback in self._change_callbacks:
            self._change_callbacks.remove(callback)

    def save_config(self, config_file: Optional[Path] = None) -> None:
        """Save current configuration to file"""
        if config_file is None:
            if self._config_files:
                config_file = self._config_files[0]
            else:
                config_file = Path(".claudedirector/config/enforcement_config.yaml")

        # Ensure directory exists
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert config to dictionary
        config_dict = asdict(self.get_config())

        # Save based on file extension
        if config_file.suffix.lower() in [".yaml", ".yml"]:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        elif config_file.suffix.lower() == ".json":
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")

    def shutdown(self) -> None:
        """Shutdown configuration manager and stop file watching"""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None

        self._watcher = None
        self._change_callbacks.clear()


# Export public API following DRY principle
__all__ = [
    "ConfigFormat",
    "GateConfig",
    "PerformanceConfig",
    "AuditConfig",
    "EnforcementConfig",
    "ConfigLoader",
    "YamlConfigLoader",
    "JsonConfigLoader",
    "ConfigValidator",
    "EnforcementConfigValidator",
    "EnforcementConfigManager",
]
