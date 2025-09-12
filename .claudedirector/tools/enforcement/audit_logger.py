#!/usr/bin/env python3
"""
🚨 ENFORCEMENT AUDIT LOGGING SYSTEM
Comprehensive audit trail for Real-Time Development Process Enforcement

SOLID Principles Applied:
- Single Responsibility: AuditLogger handles only audit logging concerns
- Open/Closed: Extensible through LogFormatter and LogStorage interfaces
- Liskov Substitution: All log formatters/storage implementations interchangeable
- Interface Segregation: Separate interfaces for formatting, storage, and querying
- Dependency Inversion: Depends on abstract interfaces, not concrete implementations

DRY Principle Applied:
- Single audit logging implementation across all enforcement components
- Centralized log formatting eliminates duplication
- Reusable query patterns for audit trail analysis

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import json
import time
import gzip
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Iterator, Union
from pathlib import Path
from enum import Enum
from datetime import datetime, timedelta
from contextlib import contextmanager

from .base_enforcement import EnforcementResult, EnforcementViolation, EnforcementLevel


class LogLevel(Enum):
    """
    Audit log levels following DRY principle.
    Single source of truth for log severity.
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AuditEventType(Enum):
    """
    Types of audit events following DRY principle.
    Single source of truth for event categorization.
    """

    ENFORCEMENT_START = "ENFORCEMENT_START"
    ENFORCEMENT_COMPLETE = "ENFORCEMENT_COMPLETE"
    ENFORCEMENT_ERROR = "ENFORCEMENT_ERROR"
    VIOLATION_DETECTED = "VIOLATION_DETECTED"
    OPERATION_BLOCKED = "OPERATION_BLOCKED"
    OPERATION_ALLOWED = "OPERATION_ALLOWED"
    GATE_ENABLED = "GATE_ENABLED"
    GATE_DISABLED = "GATE_DISABLED"
    CONFIG_CHANGED = "CONFIG_CHANGED"
    SYSTEM_START = "SYSTEM_START"
    SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"


@dataclass(frozen=True)
class AuditEvent:
    """
    Immutable audit event record following SOLID Single Responsibility.

    This class has ONE responsibility: represent a single audit event
    with all necessary context for compliance tracking.
    """

    event_id: str
    event_type: AuditEventType
    timestamp: float
    level: LogLevel
    gate_name: Optional[str]
    operation: Optional[str]
    user_context: Dict[str, Any]
    system_context: Dict[str, Any]
    message: str
    execution_time_ms: Optional[float] = None
    result: Optional[EnforcementResult] = None

    def __post_init__(self):
        """Validate audit event data integrity"""
        if not self.event_id:
            raise ValueError("event_id cannot be empty")
        if not self.message:
            raise ValueError("message cannot be empty")
        if self.timestamp <= 0:
            raise ValueError("timestamp must be positive")

    @property
    def datetime_iso(self) -> str:
        """Get timestamp as ISO format datetime string"""
        return datetime.fromtimestamp(self.timestamp).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert audit event to dictionary for serialization"""
        data = asdict(self)

        # Convert result to dict if present
        if self.result:
            data["result"] = {
                "gate_name": self.result.gate_name,
                "operation": self.result.operation,
                "passed": self.result.passed,
                "violation_count": len(self.result.violations),
                "execution_time_ms": self.result.execution_time_ms,
                "blocking_violation_count": len(self.result.blocking_violations),
            }

        # Add readable timestamp
        data["datetime"] = self.datetime_iso

        return data


class LogFormatter(ABC):
    """
    Abstract log formatter interface following SOLID Interface Segregation.

    Single responsibility: Format audit events for storage/display.
    """

    @abstractmethod
    def format_event(self, event: AuditEvent) -> str:
        """Format audit event for output"""
        pass


class JsonLogFormatter(LogFormatter):
    """
    JSON log formatter following SOLID Single Responsibility.

    Single responsibility: Format audit events as JSON strings.
    """

    def __init__(self, pretty_print: bool = False):
        """
        Initialize JSON formatter.

        Args:
            pretty_print: Whether to format JSON with indentation
        """
        self._pretty_print = pretty_print

    def format_event(self, event: AuditEvent) -> str:
        """Format audit event as JSON string"""
        data = event.to_dict()

        if self._pretty_print:
            return json.dumps(data, indent=2, default=str)
        else:
            return json.dumps(data, default=str)


class HumanReadableLogFormatter(LogFormatter):
    """
    Human-readable log formatter following SOLID Single Responsibility.

    Single responsibility: Format audit events for human consumption.
    """

    def format_event(self, event: AuditEvent) -> str:
        """Format audit event as human-readable string"""
        timestamp_str = event.datetime_iso
        level_str = event.level.value.ljust(8)
        gate_str = f"[{event.gate_name}]" if event.gate_name else "[SYSTEM]"

        base_msg = f"{timestamp_str} {level_str} {gate_str} {event.message}"

        if event.execution_time_ms is not None:
            base_msg += f" ({event.execution_time_ms:.1f}ms)"

        if event.result and not event.result.passed:
            base_msg += f" - {len(event.result.violations)} violations"

        return base_msg


class LogStorage(ABC):
    """
    Abstract log storage interface following SOLID Interface Segregation.

    Single responsibility: Store and retrieve audit events.
    """

    @abstractmethod
    def store_event(self, event: AuditEvent) -> None:
        """Store audit event"""
        pass

    @abstractmethod
    def query_events(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        event_types: Optional[List[AuditEventType]] = None,
        gate_names: Optional[List[str]] = None,
        levels: Optional[List[LogLevel]] = None,
        limit: Optional[int] = None,
    ) -> Iterator[AuditEvent]:
        """Query stored audit events"""
        pass

    @abstractmethod
    def cleanup_old_events(self, retention_days: int) -> int:
        """Remove old events and return count of removed events"""
        pass


class FileLogStorage(LogStorage):
    """
    File-based log storage following SOLID Single Responsibility.

    Single responsibility: Store audit events in rotating log files.
    """

    def __init__(
        self,
        log_directory: Path,
        formatter: LogFormatter,
        max_file_size_mb: int = 10,
        max_files: int = 10,
        compress_old: bool = True,
    ):
        """
        Initialize file log storage.

        Args:
            log_directory: Directory for log files
            formatter: Log formatter to use
            max_file_size_mb: Maximum size per log file
            max_files: Maximum number of log files to keep
            compress_old: Whether to compress rotated files
        """
        self._log_directory = Path(log_directory)
        self._formatter = formatter
        self._max_file_size = max_file_size_mb * 1024 * 1024  # Convert to bytes
        self._max_files = max_files
        self._compress_old = compress_old
        self._lock = threading.Lock()

        # Ensure log directory exists
        self._log_directory.mkdir(parents=True, exist_ok=True)

    @property
    def current_log_file(self) -> Path:
        """Get current log file path"""
        return self._log_directory / "enforcement_audit.log"

    def store_event(self, event: AuditEvent) -> None:
        """Store audit event to log file with rotation"""
        with self._lock:
            # Check if rotation is needed
            if (
                self.current_log_file.exists()
                and self.current_log_file.stat().st_size > self._max_file_size
            ):
                self._rotate_logs()

            # Write event to current log file
            formatted_event = self._formatter.format_event(event)

            with open(self.current_log_file, "a", encoding="utf-8") as f:
                f.write(formatted_event + "\n")

    def _rotate_logs(self) -> None:
        """Rotate log files, compressing old ones if configured"""
        if not self.current_log_file.exists():
            return

        # Move existing numbered files up
        for i in range(self._max_files - 1, 0, -1):
            old_file = self._log_directory / f"enforcement_audit.log.{i}"
            new_file = self._log_directory / f"enforcement_audit.log.{i + 1}"

            if self._compress_old:
                old_file = old_file.with_suffix(".log.gz")
                new_file = new_file.with_suffix(".log.gz")

            if old_file.exists():
                if i + 1 > self._max_files:
                    old_file.unlink()  # Delete oldest file
                else:
                    old_file.rename(new_file)

        # Move current file to .1
        rotated_file = self._log_directory / "enforcement_audit.log.1"

        if self._compress_old:
            # Compress the rotated file
            with open(self.current_log_file, "rb") as f_in:
                with gzip.open(rotated_file.with_suffix(".log.gz"), "wb") as f_out:
                    f_out.writelines(f_in)
            self.current_log_file.unlink()
        else:
            self.current_log_file.rename(rotated_file)

    def query_events(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        event_types: Optional[List[AuditEventType]] = None,
        gate_names: Optional[List[str]] = None,
        levels: Optional[List[LogLevel]] = None,
        limit: Optional[int] = None,
    ) -> Iterator[AuditEvent]:
        """Query events from log files (simplified implementation)"""
        # Note: This is a simplified implementation for demonstration
        # Production version would need more sophisticated indexing

        count = 0

        # Read from current and rotated log files
        log_files = [self.current_log_file]

        # Add rotated files
        for i in range(1, self._max_files + 1):
            rotated_file = self._log_directory / f"enforcement_audit.log.{i}"
            if rotated_file.exists():
                log_files.append(rotated_file)

            # Check compressed files
            compressed_file = rotated_file.with_suffix(".log.gz")
            if compressed_file.exists():
                log_files.append(compressed_file)

        for log_file in log_files:
            if limit and count >= limit:
                break

            try:
                if log_file.suffix == ".gz":
                    file_handle = gzip.open(log_file, "rt", encoding="utf-8")
                else:
                    file_handle = open(log_file, "r", encoding="utf-8")

                with file_handle:
                    for line in file_handle:
                        if limit and count >= limit:
                            break

                        try:
                            # Assume JSON format for querying
                            data = json.loads(line.strip())

                            # Apply filters
                            if start_time and data.get("timestamp", 0) < start_time:
                                continue
                            if end_time and data.get("timestamp", 0) > end_time:
                                continue
                            if event_types and data.get("event_type") not in [
                                et.value for et in event_types
                            ]:
                                continue
                            if gate_names and data.get("gate_name") not in gate_names:
                                continue
                            if levels and data.get("level") not in [
                                l.value for l in levels
                            ]:
                                continue

                            # Reconstruct AuditEvent (simplified)
                            event = AuditEvent(
                                event_id=data["event_id"],
                                event_type=AuditEventType(data["event_type"]),
                                timestamp=data["timestamp"],
                                level=LogLevel(data["level"]),
                                gate_name=data.get("gate_name"),
                                operation=data.get("operation"),
                                user_context=data.get("user_context", {}),
                                system_context=data.get("system_context", {}),
                                message=data["message"],
                                execution_time_ms=data.get("execution_time_ms"),
                            )

                            yield event
                            count += 1

                        except (json.JSONDecodeError, KeyError, ValueError):
                            # Skip malformed log entries
                            continue

            except (IOError, OSError):
                # Skip files that can't be read
                continue

    def cleanup_old_events(self, retention_days: int) -> int:
        """Remove log files older than retention period"""
        cutoff_time = time.time() - (retention_days * 24 * 60 * 60)
        removed_count = 0

        for log_file in self._log_directory.glob("enforcement_audit.log.*"):
            try:
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    removed_count += 1
            except (OSError, IOError):
                # Skip files that can't be accessed
                continue

        return removed_count


class EnforcementAuditLogger:
    """
    Main audit logger for enforcement system following SOLID principles.

    SOLID Compliance:
    - Single Responsibility: Coordinates audit logging for enforcement events
    - Open/Closed: Extensible through formatter and storage interfaces
    - Liskov Substitution: Works with any LogFormatter/LogStorage implementation
    - Interface Segregation: Clean interface for audit logging
    - Dependency Inversion: Depends on abstract interfaces

    DRY Compliance:
    - Single audit logging interface for all enforcement components
    - Eliminates duplication of logging logic across gates
    """

    def __init__(
        self,
        storage: LogStorage,
        enabled: bool = True,
        default_level: LogLevel = LogLevel.INFO,
    ):
        """
        Initialize audit logger.

        Args:
            storage: Log storage implementation
            enabled: Whether logging is enabled
            default_level: Default log level for events
        """
        self._storage = storage
        self._enabled = enabled
        self._default_level = default_level
        self._event_counter = 0
        self._lock = threading.Lock()

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        with self._lock:
            self._event_counter += 1
            timestamp = int(time.time() * 1000)  # Milliseconds
            return f"ENF_{timestamp}_{self._event_counter:06d}"

    def log_enforcement_start(
        self,
        gate_name: str,
        operation: str,
        user_context: Optional[Dict[str, Any]] = None,
        system_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log enforcement validation start.

        Returns:
            Event ID for correlation with completion event
        """
        event_id = self._generate_event_id()

        if self._enabled:
            event = AuditEvent(
                event_id=event_id,
                event_type=AuditEventType.ENFORCEMENT_START,
                timestamp=time.time(),
                level=LogLevel.INFO,
                gate_name=gate_name,
                operation=operation,
                user_context=user_context or {},
                system_context=system_context or {},
                message=f"Starting enforcement validation: {gate_name} for {operation}",
            )

            self._storage.store_event(event)

        return event_id

    def log_enforcement_complete(
        self,
        event_id: str,
        result: EnforcementResult,
        user_context: Optional[Dict[str, Any]] = None,
        system_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log enforcement validation completion"""
        if not self._enabled:
            return

        level = LogLevel.INFO if result.passed else LogLevel.WARNING
        if result.should_block:
            level = LogLevel.ERROR

        message = f"Enforcement validation complete: {result.gate_name}"
        if not result.passed:
            message += f" - {len(result.violations)} violations"
        if result.should_block:
            message += " - OPERATION BLOCKED"

        event = AuditEvent(
            event_id=event_id,
            event_type=AuditEventType.ENFORCEMENT_COMPLETE,
            timestamp=time.time(),
            level=level,
            gate_name=result.gate_name,
            operation=result.operation,
            user_context=user_context or {},
            system_context=system_context or {},
            message=message,
            execution_time_ms=result.execution_time_ms,
            result=result,
        )

        self._storage.store_event(event)

    def log_violation(
        self,
        violation: EnforcementViolation,
        gate_name: str,
        operation: str,
        user_context: Optional[Dict[str, Any]] = None,
        system_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log individual enforcement violation"""
        if not self._enabled:
            return

        level_mapping = {
            EnforcementLevel.MANDATORY: LogLevel.CRITICAL,
            EnforcementLevel.CRITICAL: LogLevel.ERROR,
            EnforcementLevel.WARNING: LogLevel.WARNING,
            EnforcementLevel.INFO: LogLevel.INFO,
        }

        event = AuditEvent(
            event_id=self._generate_event_id(),
            event_type=AuditEventType.VIOLATION_DETECTED,
            timestamp=time.time(),
            level=level_mapping.get(violation.level, LogLevel.WARNING),
            gate_name=gate_name,
            operation=operation,
            user_context=user_context or {},
            system_context={
                "violation_type": violation.violation_type.value,
                "rule_id": violation.rule_id,
                "file_path": violation.file_path,
                "line_number": violation.line_number,
                **(system_context or {}),
            },
            message=f"Violation detected: {violation.message}",
        )

        self._storage.store_event(event)

    def log_operation_blocked(
        self,
        operation: str,
        blocking_violations: List[EnforcementViolation],
        user_context: Optional[Dict[str, Any]] = None,
        system_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log operation being blocked due to violations"""
        if not self._enabled:
            return

        event = AuditEvent(
            event_id=self._generate_event_id(),
            event_type=AuditEventType.OPERATION_BLOCKED,
            timestamp=time.time(),
            level=LogLevel.CRITICAL,
            gate_name=None,
            operation=operation,
            user_context=user_context or {},
            system_context={
                "blocking_violation_count": len(blocking_violations),
                "violation_types": [
                    v.violation_type.value for v in blocking_violations
                ],
                **(system_context or {}),
            },
            message=f"Operation blocked: {operation} - {len(blocking_violations)} blocking violations",
        )

        self._storage.store_event(event)

    @contextmanager
    def enforcement_session(
        self,
        gate_name: str,
        operation: str,
        user_context: Optional[Dict[str, Any]] = None,
        system_context: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for enforcement session logging.

        Automatically logs start and completion events.
        """
        event_id = self.log_enforcement_start(
            gate_name, operation, user_context, system_context
        )

        try:
            yield event_id
        except Exception as e:
            if self._enabled:
                error_event = AuditEvent(
                    event_id=self._generate_event_id(),
                    event_type=AuditEventType.ENFORCEMENT_ERROR,
                    timestamp=time.time(),
                    level=LogLevel.ERROR,
                    gate_name=gate_name,
                    operation=operation,
                    user_context=user_context or {},
                    system_context={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        **(system_context or {}),
                    },
                    message=f"Enforcement error in {gate_name}: {str(e)}",
                )

                self._storage.store_event(error_event)

            raise

    def query_events(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        event_types: Optional[List[AuditEventType]] = None,
        gate_names: Optional[List[str]] = None,
        levels: Optional[List[LogLevel]] = None,
        limit: Optional[int] = None,
    ) -> Iterator[AuditEvent]:
        """Query audit events from storage"""
        return self._storage.query_events(
            start_time=start_time,
            end_time=end_time,
            event_types=event_types,
            gate_names=gate_names,
            levels=levels,
            limit=limit,
        )

    def cleanup_old_events(self, retention_days: int) -> int:
        """Clean up old audit events"""
        return self._storage.cleanup_old_events(retention_days)

    @property
    def is_enabled(self) -> bool:
        """Check if audit logging is enabled"""
        return self._enabled

    def enable(self) -> None:
        """Enable audit logging"""
        self._enabled = True

    def disable(self) -> None:
        """Disable audit logging"""
        self._enabled = False


# Export public API following DRY principle
__all__ = [
    "LogLevel",
    "AuditEventType",
    "AuditEvent",
    "LogFormatter",
    "JsonLogFormatter",
    "HumanReadableLogFormatter",
    "LogStorage",
    "FileLogStorage",
    "EnforcementAuditLogger",
]
