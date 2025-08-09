"""
Database Architecture Base Classes - Hybrid Foundation

Designed by Martin, implemented by Delbert.
Provides base interfaces for hybrid database architecture.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import structlog

logger = structlog.get_logger(__name__)


class QueryType(Enum):
    """Query type classification for intelligent routing"""
    TRANSACTIONAL = "transactional"  # SQLite
    ANALYTICAL = "analytical"        # DuckDB
    SEMANTIC = "semantic"            # Faiss
    MIXED = "mixed"                  # Multiple databases


class WorkloadPattern(Enum):
    """Workload pattern classification"""
    OLTP = "oltp"                   # Online Transaction Processing
    OLAP = "olap"                   # Online Analytical Processing
    VECTOR_SEARCH = "vector_search" # Semantic/Vector Search
    HYBRID = "hybrid"               # Mixed workload


@dataclass
class DatabaseConfig:
    """Configuration for database engines with performance SLAs"""
    
    engine_type: str  # 'sqlite', 'duckdb', 'faiss'
    database_path: Path
    max_query_time_ms: int = 200  # Delbert's requirement: <200ms
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
                'journal_mode': 'WAL',
                'synchronous': 'NORMAL',
                'cache_size': -10000,  # 10MB
                'mmap_size': 268435456  # 256MB
            }
        
        if self.duckdb_config is None:
            self.duckdb_config = {
                'memory_limit': '1GB',
                'threads': 4,
                'max_memory': '80%'
            }
        
        if self.faiss_config is None:
            self.faiss_config = {
                'index_type': 'IVF',
                'embedding_dim': 768,
                'nlist': 100
            }


@dataclass
class QueryContext:
    """Context for query routing and optimization"""
    
    query_type: QueryType
    workload_pattern: WorkloadPattern
    expected_result_size: int = 0
    priority: str = 'normal'  # 'low', 'normal', 'high', 'critical'
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


class DatabaseEngineBase(ABC):
    """
    Base class for all database engines in hybrid architecture.
    
    Design Philosophy:
    - Performance-first (<200ms query response time)
    - Zero-config for end users (automatic optimization)
    - Intelligent workload routing (queries go to optimal engine)
    - Graceful degradation (fallback to alternative engines)
    """
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.logger = logger.bind(db_engine=self.__class__.__name__)
        self._connection_pool = None
        self._performance_metrics: List[Dict[str, Any]] = []
        
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish database connection with optimization.
        
        Returns:
            bool: True if connection successful
            
        Implementation by Delbert:
        - Auto-apply performance optimizations
        - Initialize connection pool
        - Validate configuration
        """
        pass
    
    @abstractmethod
    def execute_query(self, query: str, context: QueryContext) -> Dict[str, Any]:
        """
        Execute query with performance monitoring.
        
        Args:
            query: SQL query or search request
            context: Query context for optimization
            
        Returns:
            Dict with results and performance metrics
            
        Performance Requirements:
        - <200ms response time for 95% of queries
        - Automatic query optimization
        - Performance degradation alerts
        """
        pass
    
    @abstractmethod
    def optimize_for_workload(self, workload_pattern: WorkloadPattern) -> bool:
        """
        Optimize engine for specific workload pattern.
        
        Args:
            workload_pattern: Expected workload type
            
        Returns:
            bool: True if optimization successful
            
        Delbert Implementation Notes:
        - Adjust indexes and cache settings
        - Optimize connection pool size
        - Configure memory allocation
        """
        pass
    
    @abstractmethod
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        pass
    
    def record_query_performance(self, query: str, execution_time_ms: int, 
                                result_count: int, context: QueryContext):
        """Record query performance for optimization"""
        metric = {
            'timestamp': logger.info("Query executed", 
                                   execution_time_ms=execution_time_ms,
                                   result_count=result_count,
                                   query_type=context.query_type.value),
            'query_hash': hash(query),
            'execution_time_ms': execution_time_ms,
            'result_count': result_count,
            'query_type': context.query_type.value,
            'workload_pattern': context.workload_pattern.value,
            'meets_sla': execution_time_ms < self.config.max_query_time_ms
        }
        
        self._performance_metrics.append(metric)
        
        # Alert if performance SLA violated
        if execution_time_ms > self.config.max_query_time_ms:
            self.logger.warning("Query SLA violation",
                              execution_time_ms=execution_time_ms,
                              sla_threshold_ms=self.config.max_query_time_ms,
                              query_type=context.query_type.value)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get database engine health status"""
        if not self._performance_metrics:
            return {'status': 'no_data', 'metrics': {}}
        
        recent_metrics = self._performance_metrics[-100:]  # Last 100 queries
        
        avg_time = sum(m['execution_time_ms'] for m in recent_metrics) / len(recent_metrics)
        sla_violation_rate = sum(1 for m in recent_metrics if not m['meets_sla']) / len(recent_metrics)
        
        status = 'healthy'
        if avg_time > self.config.max_query_time_ms * 0.8:
            status = 'warning'
        if sla_violation_rate > 0.05:  # >5% SLA violations
            status = 'critical'
        
        return {
            'status': status,
            'metrics': {
                'avg_query_time_ms': avg_time,
                'sla_violation_rate': sla_violation_rate,
                'total_queries': len(self._performance_metrics),
                'recent_queries': len(recent_metrics)
            }
        }


class DatabaseResult:
    """Standard result format for all database operations"""
    
    def __init__(self,
                 success: bool,
                 data: List[Dict[str, Any]],
                 execution_time_ms: int,
                 engine_used: str,
                 query_hash: str = "",
                 cache_hit: bool = False):
        self.success = success
        self.data = data
        self.execution_time_ms = execution_time_ms
        self.engine_used = engine_used
        self.query_hash = query_hash
        self.cache_hit = cache_hit
        self.meets_performance_sla = execution_time_ms < 200
        self.result_count = len(data) if data else 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for API responses"""
        return {
            'success': self.success,
            'data': self.data,
            'execution_time_ms': self.execution_time_ms,
            'engine_used': self.engine_used,
            'query_hash': self.query_hash,
            'cache_hit': self.cache_hit,
            'performance_sla_met': self.meets_performance_sla,
            'result_count': self.result_count
        }
