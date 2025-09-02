"""
Database Architecture Type Definitions - Core Types

Extracted from hybrid database system for use by UnifiedDatabaseCoordinator.
These types provide compatibility with the legacy hybrid system while maintaining
a clean interface for the unified database architecture.

Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
Phase: Phase 2D Safe Legacy Cleanup
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path


class QueryType(Enum):
    """Query type classification for intelligent routing"""

    TRANSACTIONAL = "transactional"  # SQLite
    ANALYTICAL = "analytical"  # DuckDB
    SEMANTIC = "semantic"  # Faiss
    MIXED = "mixed"  # Multiple databases


class WorkloadPattern(Enum):
    """Workload pattern classification"""

    OLTP = "oltp"  # Online Transaction Processing
    OLAP = "olap"  # Online Analytical Processing
    VECTOR_SEARCH = "vector_search"  # Semantic/Vector Search
    HYBRID = "hybrid"  # Mixed workload


@dataclass
class DatabaseConfig:
    """Configuration for database engines with performance SLAs"""

    engine_type: str  # 'sqlite', 'duckdb', 'faiss'
    database_path: Path
    max_query_time_ms: int = 200  # Performance requirement: <200ms
    cache_size_mb: int = 100
    connection_pool_size: int = 10

    # Engine-specific parameters
    sqlite_config: Optional[Dict[str, Any]] = None
    duckdb_config: Optional[Dict[str, Any]] = None
    faiss_config: Optional[Dict[str, Any]] = None

    # Performance monitoring
    enable_query_logging: bool = True
    enable_performance_metrics: bool = True

    def __post_init__(self):
        if self.sqlite_config is None:
            self.sqlite_config = {
                "journal_mode": "WAL",
                "synchronous": "NORMAL",
                "cache_size": -10000,  # 10MB
                "mmap_size": 268435456,  # 256MB
            }

        if self.duckdb_config is None:
            self.duckdb_config = {
                "memory_limit": "1GB",
                "threads": 4,
                "max_memory": "80%",
            }

        if self.faiss_config is None:
            self.faiss_config = {
                "index_type": "IVF",
                "embedding_dim": 768,
                "nlist": 100,
            }


@dataclass
class QueryContext:
    """Context for query routing and optimization"""

    query_type: QueryType
    workload_pattern: WorkloadPattern
    expected_result_size: int = 0
    priority: str = "normal"  # 'low', 'normal', 'high', 'critical'
    cache_enabled: bool = True

    # Performance hints
    estimated_execution_time_ms: int = 0
    preferred_engine: Optional[str] = None
    fallback_engines: List[str] = None

    # Analytics context
    time_range: Optional[Dict[str, str]] = None
    aggregation_level: Optional[str] = None

    # Semantic search context
    embedding_model: Optional[str] = None
    similarity_threshold: float = 0.8

    def __post_init__(self):
        if self.fallback_engines is None:
            self.fallback_engines = []


@dataclass
class DatabaseResult:
    """Standardized database operation result"""

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    rows_affected: int = 0
    query_plan: Optional[str] = None
    cache_hit: bool = False
    engine_used: Optional[str] = None

    # Performance metrics
    parse_time_ms: int = 0
    execution_time_ms: int = 0
    fetch_time_ms: int = 0

    def is_success(self) -> bool:
        return self.success and self.error is None


class DatabaseEngineBase(ABC):
    """Base class for database engines - compatibility interface"""

    def __init__(self, config: DatabaseConfig):
        self.config = config

    @abstractmethod
    def execute_query(
        self,
        query: str,
        params: Optional[Dict] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        """Execute a query with the given context"""
        pass

    @abstractmethod
    def get_connection(self):
        """Get a database connection"""
        pass

    @abstractmethod
    def close(self):
        """Close the database engine"""
        pass
