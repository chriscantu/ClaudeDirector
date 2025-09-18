"""
Type definitions for ClaudeDirector core modules.
Provides common type hints and type aliases for consistent typing across the codebase.
"""

from typing import Dict, List, Optional, Any, Union, TypeVar
from typing import Protocol, runtime_checkable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import sqlite3

# Basic type aliases
FilePath = Union[str, Path]
JsonDict = Dict[str, Any]
ConfigDict = Dict[str, Any]
MetadataDict = Dict[str, Any]

# Database types
DatabaseRow = sqlite3.Row
DatabaseConnection = sqlite3.Connection
DatabaseCursor = sqlite3.Cursor

# Generic type variables
T = TypeVar("T")
ConfigT = TypeVar("ConfigT", bound="ConfigDict")


# File lifecycle types
class FileMetadata(Protocol):
    """Protocol for file metadata objects."""

    file_path: FilePath
    created_at: datetime
    modified_at: datetime
    size_bytes: int
    content_type: str
    retention_score: float


@runtime_checkable
class ArchivableFile(Protocol):
    """Protocol for files that can be archived."""

    def get_metadata(self) -> FileMetadata: ...
    def get_content(self) -> str: ...
    def get_retention_score(self) -> float: ...


# Smart organization types
class ConsolidationOpportunity(Protocol):
    """Protocol for file consolidation opportunities."""

    files: List[FilePath]
    suggested_name: str
    confidence_score: float
    reasoning: str


class SessionPattern(Protocol):
    """Protocol for detected session patterns."""

    pattern_type: str
    frequency: int
    last_occurrence: datetime
    suggested_template: Optional[str]


# Framework types
class FrameworkResult(Protocol):
    """Protocol for framework analysis results."""

    framework_name: str
    confidence_score: float
    recommendations: List[str]
    persona_suggestions: List[str]


# Workspace types
class WorkspaceConfig(Protocol):
    """Protocol for workspace configuration."""

    workspace_path: FilePath
    generation_mode: str
    consolidate_analysis: bool
    max_session_files: int
    auto_archive_days: int


# Intelligence types
class PatternInsight(Protocol):
    """Protocol for pattern recognition insights."""

    pattern_id: str
    description: str
    impact_score: float
    optimization_suggestions: List[str]


# Error types
class ClaudeDirectorError(Exception):
    """Base exception for ClaudeDirector operations."""


class ConfigurationError(ClaudeDirectorError):
    """Raised when configuration is invalid or missing."""


class FileLifecycleError(ClaudeDirectorError):
    """Raised when file lifecycle operations fail."""


class ArchivingError(ClaudeDirectorError):
    """Raised when archiving operations fail."""


class PatternRecognitionError(ClaudeDirectorError):
    """Raised when pattern recognition operations fail."""


# Processing result types
@dataclass
class ProcessingResult:
    """Standard result type for processing operations"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
