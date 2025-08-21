"""
Template Migration CLI Commands - Phase 2.2

Provides comprehensive template migration capabilities including:
- Template format migrations and updates
- Configuration backup and restore
- Template validation and compatibility checking
- Version management and rollback support

Supports Alvaro's user stories for template lifecycle management.
"""

import json
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

from ..core.template_engine import TemplateDiscoveryEngine
from ..utils.formatting import (
    format_success,
    format_warning,
    format_error,
    format_table,
    format_list,
    format_status_indicator,
)

logger = logging.getLogger(__name__)


@dataclass
class MigrationRecord:
    """Record of template migration operation"""

    migration_id: str
    source_version: str
    target_version: str
    template_ids: List[str]
    timestamp: datetime
    status: str  # success, failed, partial
    backup_path: Optional[str] = None
    error_messages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "migration_id": self.migration_id,
            "source_version": self.source_version,
            "target_version": self.target_version,
            "template_ids": self.template_ids,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "backup_path": self.backup_path,
            "error_messages": self.error_messages,
            "warnings": self.warnings,
        }


@dataclass
class BackupInfo:
    """Information about template configuration backup"""

    backup_id: str
    backup_path: str
    original_path: str
    template_count: int
    timestamp: datetime
    backup_size_bytes: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "backup_id": self.backup_id,
            "backup_path": self.backup_path,
            "original_path": self.original_path,
            "template_count": self.template_count,
            "timestamp": self.timestamp.isoformat(),
            "backup_size_bytes": self.backup_size_bytes,
        }


class TemplateMigrationEngine:
    """
    Template Migration Engine - Phase 2.2

    Handles template format migrations, version updates, and configuration management.
    Provides safe migration paths with automatic backup and rollback capabilities.
    """

    SUPPORTED_VERSIONS = ["1.0.0", "1.1.0", "2.0.0"]
    CURRENT_VERSION = "2.0.0"

    # Configuration constants for DRY compliance
    DEFAULT_ACTIVATION_THRESHOLDS = {
        "high_confidence": 0.8,
        "medium_confidence": 0.6,
        "low_confidence": 0.4,
    }

    DEFAULT_SELECTION_WEIGHTS = {
        "domain_match": 0.4,
        "industry_match": 0.3,
        "team_size_match": 0.2,
        "keyword_confidence": 0.1,
    }

    def __init__(
        self,
        templates_config_path: Optional[Path] = None,
        migrations_dir: Optional[Path] = None,
        template_discovery: Optional[TemplateDiscoveryEngine] = None,
    ):
        """Initialize migration engine"""
        self.templates_config_path = templates_config_path or Path(
            "config/director_templates.yaml"
        )
        self.migrations_dir = migrations_dir or Path("migrations/templates")
        self.migrations_dir.mkdir(parents=True, exist_ok=True)

        # Migration history tracking
        self.migration_history_path = self.migrations_dir / "migration_history.json"
        self.backups_dir = self.migrations_dir / "backups"
        self.backups_dir.mkdir(parents=True, exist_ok=True)

        # Template discovery engine for validation (dependency injection)
        self.template_discovery = template_discovery or TemplateDiscoveryEngine(
            self.templates_config_path
        )

    def detect_config_version(self, config_path: Optional[Path] = None) -> str:
        """
        Detect the version of template configuration file

        Args:
            config_path: Path to config file, defaults to main config

        Returns:
            Version string or "unknown"
        """
        config_path = config_path or self.templates_config_path

        try:
            if not config_path.exists():
                return "none"

            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            # Check for version indicators
            if "schema_version" in config:
                return config["schema_version"]
            elif "metadata" in config and "version" in config["metadata"]:
                return config["metadata"]["version"]
            elif "templates" in config and "global_settings" in config:
                return "2.0.0"  # Current format
            elif "templates" in config:
                return "1.0.0"  # Legacy format
            else:
                return "unknown"

        except Exception as e:
            logger.error(f"Failed to detect config version: {e}")
            return "unknown"

    def create_backup(
        self, config_path: Optional[Path] = None, backup_id: Optional[str] = None
    ) -> BackupInfo:
        """
        Create backup of template configuration

        Args:
            config_path: Path to config file to backup
            backup_id: Optional custom backup ID

        Returns:
            BackupInfo with backup details
        """
        config_path = config_path or self.templates_config_path
        backup_id = backup_id or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")

            # Create backup file
            backup_filename = f"{backup_id}_{config_path.name}"
            backup_path = self.backups_dir / backup_filename

            shutil.copy2(config_path, backup_path)

            # Count templates in backup
            with open(backup_path, "r") as f:
                config = yaml.safe_load(f)
            template_count = len(config.get("templates", {}))

            # Get file size
            backup_size = backup_path.stat().st_size

            backup_info = BackupInfo(
                backup_id=backup_id,
                backup_path=str(backup_path),
                original_path=str(config_path),
                template_count=template_count,
                timestamp=datetime.now(),
                backup_size_bytes=backup_size,
            )

            # Save backup metadata
            metadata_path = self.backups_dir / f"{backup_id}_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(backup_info.to_dict(), f, indent=2)

            logger.info(
                f"Created backup: {backup_id} ({template_count} templates, {backup_size} bytes)"
            )
            return backup_info

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise

    def restore_backup(
        self, backup_id: str, target_path: Optional[Path] = None
    ) -> bool:
        """
        Restore template configuration from backup

        Args:
            backup_id: ID of backup to restore
            target_path: Target path for restore, defaults to original location

        Returns:
            True if restore successful
        """
        try:
            # Find backup metadata
            metadata_path = self.backups_dir / f"{backup_id}_metadata.json"
            if not metadata_path.exists():
                raise FileNotFoundError(f"Backup metadata not found: {backup_id}")

            with open(metadata_path, "r") as f:
                backup_info = json.load(f)

            backup_path = Path(backup_info["backup_path"])
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            # Determine restore target
            target_path = target_path or Path(backup_info["original_path"])

            # Create backup of current config before restore
            if target_path.exists():
                restore_backup_id = (
                    f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                self.create_backup(target_path, restore_backup_id)
                logger.info(f"Created pre-restore backup: {restore_backup_id}")

            # Perform restore
            shutil.copy2(backup_path, target_path)

            logger.info(f"Restored backup {backup_id} to {target_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore backup {backup_id}: {e}")
            return False

    def migrate_to_version(
        self, target_version: str, dry_run: bool = False
    ) -> MigrationRecord:
        """
        Migrate template configuration to target version

        Args:
            target_version: Target schema version
            dry_run: If True, validate migration without applying changes

        Returns:
            MigrationRecord with migration results
        """
        migration_id = f"migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        current_version = self.detect_config_version()

        migration_record = MigrationRecord(
            migration_id=migration_id,
            source_version=current_version,
            target_version=target_version,
            template_ids=[],
            timestamp=datetime.now(),
            status="started",
        )

        try:
            # Validate target version
            if target_version not in self.SUPPORTED_VERSIONS:
                raise ValueError(f"Unsupported target version: {target_version}")

            if current_version == target_version:
                migration_record.status = "no_change"
                migration_record.warnings.append(
                    f"Already at target version {target_version}"
                )
                return migration_record

            # Load current configuration
            if not self.templates_config_path.exists():
                raise FileNotFoundError(
                    f"Template config not found: {self.templates_config_path}"
                )

            with open(self.templates_config_path, "r") as f:
                config = yaml.safe_load(f)

            migration_record.template_ids = list(config.get("templates", {}).keys())

            # Create backup before migration
            if not dry_run:
                backup_info = self.create_backup(backup_id=f"pre_{migration_id}")
                migration_record.backup_path = backup_info.backup_path

            # Apply version-specific migrations
            migrated_config = self._apply_version_migration(
                config, current_version, target_version, migration_record
            )

            # Validate migrated configuration
            validation_errors = self._validate_migrated_config(migrated_config)
            if validation_errors:
                migration_record.error_messages.extend(validation_errors)
                migration_record.status = "failed"
                return migration_record

            # Apply changes if not dry run
            if not dry_run:
                with open(self.templates_config_path, "w") as f:
                    yaml.dump(migrated_config, f, default_flow_style=False, indent=2)

                migration_record.status = "success"
                logger.info(
                    f"Successfully migrated from {current_version} to {target_version}"
                )
            else:
                migration_record.status = "dry_run_success"
                logger.info(
                    f"Dry run migration from {current_version} to {target_version} validated"
                )

            # Save migration record
            self._save_migration_record(migration_record)

            return migration_record

        except Exception as e:
            migration_record.status = "failed"
            migration_record.error_messages.append(str(e))
            logger.error(f"Migration failed: {e}")

            # Save failed migration record
            self._save_migration_record(migration_record)

            return migration_record

    def _apply_version_migration(
        self,
        config: Dict[str, Any],
        source_version: str,
        target_version: str,
        migration_record: MigrationRecord,
    ) -> Dict[str, Any]:
        """Apply version-specific migration transformations"""

        migrated_config = config.copy()

        # Migration from 1.0.0 to 2.0.0
        if source_version == "1.0.0" and target_version in ["1.1.0", "2.0.0"]:
            migrated_config = self._migrate_1_0_to_2_0(
                migrated_config, migration_record
            )

        # Migration from 1.1.0 to 2.0.0
        if source_version == "1.1.0" and target_version == "2.0.0":
            migrated_config = self._migrate_1_1_to_2_0(
                migrated_config, migration_record
            )

        # Add schema version
        migrated_config["schema_version"] = target_version

        # Add/update metadata
        if "metadata" not in migrated_config:
            migrated_config["metadata"] = {}

        migrated_config["metadata"].update(
            {
                "generated_at": datetime.now().isoformat(),
                "migrated_from": source_version,
                "migration_id": migration_record.migration_id,
                "total_templates": len(migrated_config.get("templates", {})),
            }
        )

        return migrated_config

    def _migrate_1_0_to_2_0(
        self, config: Dict[str, Any], migration_record: MigrationRecord
    ) -> Dict[str, Any]:
        """Migrate from legacy 1.0 format to current 2.0 format"""

        migrated = config.copy()

        # Add global_settings if missing
        if "global_settings" not in migrated:
            migrated["global_settings"] = {
                "default_fallback_personas": ["camille", "diego", "alvaro"],
                "activation_thresholds": self.DEFAULT_ACTIVATION_THRESHOLDS.copy(),
                "selection_weights": self.DEFAULT_SELECTION_WEIGHTS.copy(),
            }
            migration_record.warnings.append("Added default global_settings")

        # Migrate templates to new format
        if "templates" in migrated:
            for template_id, template_config in migrated["templates"].items():
                # Add industry_modifiers if missing
                if "industry_modifiers" not in template_config:
                    template_config["industry_modifiers"] = {}

                # Add team_size_contexts if missing
                if "team_size_contexts" not in template_config:
                    template_config["team_size_contexts"] = {}

                # Ensure activation_keywords is properly formatted
                if "activation_keywords" in template_config:
                    if isinstance(template_config["activation_keywords"], list):
                        # Convert from list to dict format
                        keywords_dict = {}
                        for keyword in template_config["activation_keywords"]:
                            keywords_dict[keyword] = 0.8  # Default confidence
                        template_config["activation_keywords"] = keywords_dict
                        migration_record.warnings.append(
                            f"Converted activation_keywords to dict format for {template_id}"
                        )

        return migrated

    def _migrate_1_1_to_2_0(
        self, config: Dict[str, Any], migration_record: MigrationRecord
    ) -> Dict[str, Any]:
        """Migrate from 1.1 format to current 2.0 format"""

        migrated = config.copy()

        # Update selection weights if using old format
        if "global_settings" in migrated and "weights" in migrated["global_settings"]:
            old_weights = migrated["global_settings"].pop("weights")
            migrated["global_settings"]["selection_weights"] = {
                "domain_match": old_weights.get(
                    "domain", self.DEFAULT_SELECTION_WEIGHTS["domain_match"]
                ),
                "industry_match": old_weights.get(
                    "industry", self.DEFAULT_SELECTION_WEIGHTS["industry_match"]
                ),
                "team_size_match": old_weights.get(
                    "team_size", self.DEFAULT_SELECTION_WEIGHTS["team_size_match"]
                ),
                "keyword_confidence": old_weights.get(
                    "keyword", self.DEFAULT_SELECTION_WEIGHTS["keyword_confidence"]
                ),
            }
            migration_record.warnings.append(
                "Updated weights format to selection_weights"
            )

        return migrated

    def _validate_migrated_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate migrated configuration"""
        errors = []

        try:
            # Check required top-level keys
            required_keys = ["schema_version", "templates"]
            for key in required_keys:
                if key not in config:
                    errors.append(f"Missing required key: {key}")

            # Validate schema version
            if "schema_version" in config:
                if config["schema_version"] not in self.SUPPORTED_VERSIONS:
                    errors.append(
                        f"Unsupported schema version: {config['schema_version']}"
                    )

            # Validate templates
            if "templates" in config:
                for template_id, template_config in config["templates"].items():
                    template_errors = self._validate_template_config(
                        template_id, template_config
                    )
                    errors.extend(template_errors)

            # Validate global_settings
            if "global_settings" in config:
                global_errors = self._validate_global_settings(
                    config["global_settings"]
                )
                errors.extend(global_errors)

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        return errors

    def _validate_template_config(
        self, template_id: str, config: Dict[str, Any]
    ) -> List[str]:
        """Validate individual template configuration"""
        errors = []

        required_fields = [
            "domain",
            "display_name",
            "description",
            "personas",
            "activation_keywords",
        ]
        for required_field in required_fields:
            if required_field not in config:
                errors.append(f"Template {template_id} missing required field: {required_field}")

        # Validate personas structure
        if "personas" in config:
            personas = config["personas"]
            if not isinstance(personas, dict):
                errors.append(f"Template {template_id} personas must be a dict")
            else:
                if "primary" not in personas or not personas["primary"]:
                    errors.append(
                        f"Template {template_id} must have at least one primary persona"
                    )

        # Validate activation_keywords
        if "activation_keywords" in config:
            keywords = config["activation_keywords"]
            if not isinstance(keywords, dict):
                errors.append(
                    f"Template {template_id} activation_keywords must be a dict"
                )
            else:
                for keyword, confidence in keywords.items():
                    if (
                        not isinstance(confidence, (int, float))
                        or not 0 <= confidence <= 1
                    ):
                        errors.append(
                            f"Template {template_id} keyword '{keyword}' confidence must be 0-1"
                        )

        return errors

    def _validate_global_settings(self, global_settings: Dict[str, Any]) -> List[str]:
        """Validate global settings configuration"""
        errors = []

        # Validate activation_thresholds
        if "activation_thresholds" in global_settings:
            thresholds = global_settings["activation_thresholds"]
            required_thresholds = [
                "high_confidence",
                "medium_confidence",
                "low_confidence",
            ]
            for threshold in required_thresholds:
                if threshold not in thresholds:
                    errors.append(f"Missing activation threshold: {threshold}")
                elif not 0 <= thresholds[threshold] <= 1:
                    errors.append(f"Threshold {threshold} must be between 0 and 1")

        # Validate selection_weights
        if "selection_weights" in global_settings:
            weights = global_settings["selection_weights"]
            total_weight = sum(weights.values())
            if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
                errors.append(f"Selection weights must sum to 1.0, got {total_weight}")

        return errors

    def _save_migration_record(self, migration_record: MigrationRecord) -> None:
        """Save migration record to history"""
        try:
            # Load existing history
            history = []
            if self.migration_history_path.exists():
                with open(self.migration_history_path, "r") as f:
                    history = json.load(f)

            # Add new record
            history.append(migration_record.to_dict())

            # Save updated history
            with open(self.migration_history_path, "w") as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save migration record: {e}")

    def get_migration_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get migration history"""
        try:
            if not self.migration_history_path.exists():
                return []

            with open(self.migration_history_path, "r") as f:
                history = json.load(f)

            # Return most recent migrations
            return history[-limit:] if limit > 0 else history

        except Exception as e:
            logger.error(f"Failed to load migration history: {e}")
            return []

    def list_backups(self) -> List[BackupInfo]:
        """List available backups"""
        backups = []

        try:
            for metadata_file in self.backups_dir.glob("*_metadata.json"):
                with open(metadata_file, "r") as f:
                    backup_data = json.load(f)

                # Convert timestamp string back to datetime
                backup_data["timestamp"] = datetime.fromisoformat(
                    backup_data["timestamp"]
                )

                backup_info = BackupInfo(**backup_data)
                backups.append(backup_info)

            # Sort by timestamp, most recent first
            backups.sort(key=lambda b: b.timestamp, reverse=True)

        except Exception as e:
            logger.error(f"Failed to list backups: {e}")

        return backups


class TemplateMigrationCommands:
    """
    Template Migration CLI Commands - Phase 2.2

    Provides user-friendly CLI interface for template migration operations.
    Supports all migration workflows from Alvaro's user stories.
    """

    def __init__(self, migration_engine: Optional[TemplateMigrationEngine] = None):
        """Initialize migration commands"""
        self.migration_engine = migration_engine or TemplateMigrationEngine()

    def check_version(self) -> str:
        """Check current template configuration version"""
        try:
            current_version = self.migration_engine.detect_config_version()

            if current_version == "none":
                return (
                    format_warning("⚠️  No template configuration found")
                    + "\n"
                    + "Run `claudedirector templates list` to initialize configuration."
                )

            elif current_version == "unknown":
                return (
                    format_warning("⚠️  Unknown template configuration format")
                    + "\n"
                    + "Configuration may need manual review or migration."
                )

            elif current_version == TemplateMigrationEngine.CURRENT_VERSION:
                return (
                    format_success(f"✅ Template configuration is up to date")
                    + "\n"
                    + f"**Current Version**: {current_version}\n"
                    + f"**Latest Supported**: {TemplateMigrationEngine.CURRENT_VERSION}"
                )

            else:
                return (
                    format_status_indicator(f"📋 Template Configuration Status")
                    + "\n\n"
                    + f"**Current Version**: {current_version}\n"
                    + f"**Latest Available**: {TemplateMigrationEngine.CURRENT_VERSION}\n\n"
                    + f"Migration available. Run `claudedirector templates migrate --to {TemplateMigrationEngine.CURRENT_VERSION}` to upgrade."
                )

        except Exception as e:
            return format_error(f"❌ Failed to check version: {e}")

    def migrate_templates(self, target_version: str, dry_run: bool = False) -> str:
        """Migrate templates to target version"""
        try:
            if dry_run:
                result_header = format_status_indicator(
                    "🔍 Template Migration - Dry Run"
                )
            else:
                result_header = format_status_indicator("🚀 Template Migration")

            # Perform migration
            migration_record = self.migration_engine.migrate_to_version(
                target_version, dry_run=dry_run
            )

            # Format results
            result_lines = [result_header, ""]

            # Migration summary
            result_lines.extend(
                [
                    f"**Migration ID**: {migration_record.migration_id}",
                    f"**Source Version**: {migration_record.source_version}",
                    f"**Target Version**: {migration_record.target_version}",
                    f"**Templates Affected**: {len(migration_record.template_ids)}",
                    f"**Status**: {migration_record.status.upper()}",
                    f"**Timestamp**: {migration_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                ]
            )

            # Add backup info if created
            if migration_record.backup_path:
                result_lines.extend(
                    [f"**Backup Created**: {migration_record.backup_path}", ""]
                )

            # Show affected templates
            if migration_record.template_ids:
                result_lines.extend(
                    [
                        "**Affected Templates**:",
                        format_list(migration_record.template_ids),
                        "",
                    ]
                )

            # Show warnings
            if migration_record.warnings:
                result_lines.extend(["**Warnings**:", ""])
                for warning in migration_record.warnings:
                    result_lines.append(f"⚠️  {warning}")
                result_lines.append("")

            # Show errors
            if migration_record.error_messages:
                result_lines.extend(["**Errors**:", ""])
                for error in migration_record.error_messages:
                    result_lines.append(f"❌ {error}")
                result_lines.append("")

            # Status-specific messages
            if migration_record.status == "success":
                result_lines.append(
                    format_success("✅ Migration completed successfully!")
                )
                result_lines.append(
                    "Templates are now ready to use with enhanced features."
                )

            elif migration_record.status == "dry_run_success":
                result_lines.append(format_success("✅ Dry run validation passed!"))
                result_lines.append(
                    f"Run without --dry-run to apply migration to version {target_version}."
                )

            elif migration_record.status == "no_change":
                result_lines.append(format_status_indicator("📋 No migration needed"))
                result_lines.append(
                    f"Templates are already at version {target_version}."
                )

            elif migration_record.status == "failed":
                result_lines.append(format_error("❌ Migration failed"))
                if migration_record.backup_path:
                    result_lines.append(
                        f"Original configuration backed up to: {migration_record.backup_path}"
                    )

            return "\n".join(result_lines)

        except Exception as e:
            return format_error(f"❌ Migration operation failed: {e}")

    def create_backup(self, backup_id: Optional[str] = None) -> str:
        """Create backup of current template configuration"""
        try:
            backup_info = self.migration_engine.create_backup(backup_id=backup_id)

            return (
                format_success("✅ Backup created successfully!")
                + "\n\n"
                + f"**Backup ID**: {backup_info.backup_id}\n"
                + f"**Backup Path**: {backup_info.backup_path}\n"
                + f"**Templates Backed Up**: {backup_info.template_count}\n"
                + f"**Backup Size**: {self._format_file_size(backup_info.backup_size_bytes)}\n"
                + f"**Created**: {backup_info.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                + f"Use `claudedirector templates restore {backup_info.backup_id}` to restore this backup."
            )

        except Exception as e:
            return format_error(f"❌ Failed to create backup: {e}")

    def restore_backup(self, backup_id: str) -> str:
        """Restore template configuration from backup"""
        try:
            success = self.migration_engine.restore_backup(backup_id)

            if success:
                return (
                    format_success("✅ Backup restored successfully!")
                    + "\n\n"
                    + f"**Backup ID**: {backup_id}\n"
                    + "Template configuration has been restored.\n"
                    + "Run `claudedirector templates list` to verify templates."
                )
            else:
                return format_error(f"❌ Failed to restore backup: {backup_id}")

        except Exception as e:
            return format_error(f"❌ Restore operation failed: {e}")

    def list_backups(self) -> str:
        """List available template backups"""
        try:
            backups = self.migration_engine.list_backups()

            if not backups:
                return (
                    format_warning("⚠️  No backups found")
                    + "\n"
                    + "Use `claudedirector templates backup` to create a backup."
                )

            # Create table data
            table_data = []
            for backup in backups:
                table_data.append(
                    [
                        backup.backup_id,
                        backup.timestamp.strftime("%Y-%m-%d %H:%M"),
                        str(backup.template_count),
                        self._format_file_size(backup.backup_size_bytes),
                    ]
                )

            headers = ["Backup ID", "Created", "Templates", "Size"]
            table = format_table(table_data, headers)

            return (
                format_status_indicator("📋 Template Configuration Backups")
                + "\n\n"
                + table
                + "\n\n"
                + "Use `claudedirector templates restore <backup_id>` to restore a backup."
            )

        except Exception as e:
            return format_error(f"❌ Failed to list backups: {e}")

    def show_migration_history(self, limit: int = 10) -> str:
        """Show template migration history"""
        try:
            history = self.migration_engine.get_migration_history(limit=limit)

            if not history:
                return (
                    format_warning("⚠️  No migration history found")
                    + "\n"
                    + "No template migrations have been performed yet."
                )

            # Create table data
            table_data = []
            for record in reversed(history):  # Show most recent first
                timestamp = datetime.fromisoformat(record["timestamp"])
                table_data.append(
                    [
                        record["migration_id"],
                        timestamp.strftime("%Y-%m-%d %H:%M"),
                        f"{record['source_version']} → {record['target_version']}",
                        record["status"],
                        str(len(record["template_ids"])),
                    ]
                )

            headers = ["Migration ID", "Date", "Version", "Status", "Templates"]
            table = format_table(table_data, headers)

            return (
                format_status_indicator("📋 Template Migration History")
                + "\n\n"
                + table
                + "\n\n"
                + f"Showing {len(history)} most recent migrations."
            )

        except Exception as e:
            return format_error(f"❌ Failed to show migration history: {e}")

    def validate_configuration(self) -> str:
        """Validate current template configuration"""
        try:
            # Load current config
            if not self.migration_engine.templates_config_path.exists():
                return (
                    format_warning("⚠️  No template configuration found")
                    + "\n"
                    + "Run `claudedirector templates list` to initialize configuration."
                )

            with open(self.migration_engine.templates_config_path, "r") as f:
                config = yaml.safe_load(f)

            # Validate configuration
            errors = self.migration_engine._validate_migrated_config(config)

            current_version = config.get("schema_version", "unknown")
            template_count = len(config.get("templates", {}))

            result_lines = [
                format_status_indicator("🔍 Template Configuration Validation"),
                "",
                f"**Configuration Path**: {self.migration_engine.templates_config_path}",
                f"**Schema Version**: {current_version}",
                f"**Total Templates**: {template_count}",
                "",
            ]

            if not errors:
                result_lines.extend(
                    [
                        format_success("✅ Configuration is valid!"),
                        "All templates and settings are properly configured.",
                    ]
                )
            else:
                result_lines.extend(
                    [format_error(f"❌ Found {len(errors)} validation errors:"), ""]
                )
                for error in errors:
                    result_lines.append(f"• {error}")

                result_lines.extend(
                    [
                        "",
                        "Run `claudedirector templates migrate --dry-run` to see migration options.",
                    ]
                )

            return "\n".join(result_lines)

        except Exception as e:
            return format_error(f"❌ Validation failed: {e}")

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
