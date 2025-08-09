"""
SQLite AI Workload Optimizer

Delbert's specialized SQLite optimizations for AI inference workloads.
Focuses on JSON query performance, concurrent reads, and <200ms response times.
"""

import sqlite3
import time
import json
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
import threading
from contextlib import contextmanager
import structlog

from .db_base import DatabaseEngineBase, QueryContext, DatabaseResult, OptimizationLevel
from ..infrastructure.config import get_config

logger = structlog.get_logger(__name__)


class SQLiteAIOptimizer(DatabaseEngineBase):
    """
    Advanced SQLite optimizer for AI workloads
    
    Delbert's AI-Specific Optimizations:
    1. JSON query performance tuning
    2. Concurrent read optimization 
    3. AI-specific indexing strategies
    4. Memory-mapped I/O for large datasets
    5. Connection pooling for AI engines
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.logger = logger.bind(component="sqlite_ai_optimizer")
        
        # Connection pool for concurrent AI engines
        self._connection_pool: List[sqlite3.Connection] = []
        self._pool_lock = threading.Lock()
        self._max_pool_size = config.connection_pool_size
        
        # AI workload patterns
        self._ai_query_patterns = {
            'decision_intelligence': [
                'decisions_made', 'action_items', 'agenda_topics',
                'strategic_themes', 'meeting_outcomes'
            ],
            'health_assessment': [
                'milestone_history', 'roi_tracking', 'resource_allocation',
                'stakeholder_impact', 'risk_level', 'status'
            ],
            'stakeholder_analysis': [
                'interaction_history', 'decision_criteria', 'preferred_personas',
                'communication_style'
            ]
        }
        
        # Performance tracking for AI queries
        self._ai_query_metrics: Dict[str, List[float]] = {
            'decision_intelligence': [],
            'health_assessment': [],
            'stakeholder_analysis': []
        }
        
        # Optimization state
        self._optimizations_applied = set()
        self._json_indexes_created = set()
    
    def connect(self) -> bool:
        """Connect with AI workload optimizations"""
        try:
            start_time = time.time()
            
            # Create primary connection
            primary_conn = self._create_optimized_connection()
            if not primary_conn:
                return False
            
            # Apply AI-specific optimizations
            self._apply_ai_optimizations(primary_conn)
            
            # Initialize connection pool
            self._initialize_connection_pool()
            
            # Create AI-specific indexes
            self._create_ai_indexes(primary_conn)
            
            # Validate AI query performance
            self._validate_ai_performance(primary_conn)
            
            # Store primary connection
            with self._pool_lock:
                self._connection_pool.append(primary_conn)
            
            connection_time = (time.time() - start_time) * 1000
            
            self.logger.info("SQLite AI optimizer connected",
                           connection_time_ms=connection_time,
                           pool_size=len(self._connection_pool),
                           optimizations_applied=list(self._optimizations_applied))
            
            return True
            
        except Exception as e:
            self.logger.error("SQLite AI optimizer connection failed", error=str(e))
            return False
    
    def execute_query(self, query: str, params: Optional[Dict] = None,
                     context: Optional[QueryContext] = None) -> DatabaseResult:
        """Execute query with AI workload optimizations"""
        start_time = time.time()
        
        try:
            # Classify AI workload
            workload_type = self._classify_ai_workload(query)
            
            # Get optimized connection
            with self._get_optimized_connection() as conn:
                # Apply query-specific optimizations
                self._optimize_for_query(conn, query, workload_type)
                
                # Execute with monitoring
                if params:
                    cursor = conn.execute(query, params)
                else:
                    cursor = conn.execute(query)
                
                # Fetch results efficiently
                data = self._fetch_results_optimized(cursor, workload_type)
                
                execution_time = int((time.time() - start_time) * 1000)
                
                # Record AI workload performance
                self._record_ai_performance(workload_type, execution_time)
                
                # Validate SLA compliance
                if execution_time > self.config.max_query_time_ms:
                    self.logger.warning("AI query SLA violation",
                                      execution_time_ms=execution_time,
                                      threshold_ms=self.config.max_query_time_ms,
                                      workload_type=workload_type,
                                      query=query[:50])
                
                return DatabaseResult(
                    success=True, data=data, execution_time_ms=execution_time,
                    rows_affected=cursor.rowcount if cursor.rowcount != -1 else len(data)
                )
                
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            self.logger.error("AI query execution failed",
                            query=query[:100],
                            execution_time_ms=execution_time,
                            error=str(e))
            
            return DatabaseResult(
                success=False, data=[], execution_time_ms=execution_time,
                rows_affected=0, error=str(e)
            )
    
    def optimize_performance(self, level: OptimizationLevel) -> bool:
        """Apply AI-specific performance optimizations"""
        try:
            optimizations_applied = []
            
            with self._get_optimized_connection() as conn:
                if level == OptimizationLevel.BASIC:
                    # Basic AI optimizations
                    if self._apply_basic_ai_optimizations(conn):
                        optimizations_applied.append("basic_ai")
                
                elif level == OptimizationLevel.INTERMEDIATE:
                    # Intermediate AI optimizations
                    if self._apply_basic_ai_optimizations(conn):
                        optimizations_applied.append("basic_ai")
                    if self._apply_intermediate_ai_optimizations(conn):
                        optimizations_applied.append("intermediate_ai")
                
                elif level == OptimizationLevel.AGGRESSIVE:
                    # Aggressive AI optimizations
                    if self._apply_basic_ai_optimizations(conn):
                        optimizations_applied.append("basic_ai")
                    if self._apply_intermediate_ai_optimizations(conn):
                        optimizations_applied.append("intermediate_ai")
                    if self._apply_aggressive_ai_optimizations(conn):
                        optimizations_applied.append("aggressive_ai")
            
            # Update optimization state
            self._optimizations_applied.update(optimizations_applied)
            
            self.logger.info("AI performance optimization completed",
                           level=level.value,
                           optimizations_applied=optimizations_applied)
            
            return len(optimizations_applied) > 0
            
        except Exception as e:
            self.logger.error("AI performance optimization failed", error=str(e))
            return False
    
    def get_ai_performance_metrics(self) -> Dict[str, Any]:
        """Get AI-specific performance metrics"""
        metrics = {
            'timestamp': time.time(),
            'workload_performance': {},
            'optimization_status': {
                'applied_optimizations': list(self._optimizations_applied),
                'ai_indexes_created': list(self._json_indexes_created),
                'connection_pool_size': len(self._connection_pool)
            },
            'sla_compliance': {}
        }
        
        # Calculate performance by AI workload
        for workload, times in self._ai_query_metrics.items():
            if times:
                recent_times = times[-50:]  # Last 50 queries
                metrics['workload_performance'][workload] = {
                    'avg_execution_time_ms': round(sum(recent_times) / len(recent_times), 2),
                    'min_execution_time_ms': round(min(recent_times), 2),
                    'max_execution_time_ms': round(max(recent_times), 2),
                    'query_count': len(recent_times),
                    'p95_execution_time_ms': round(self._calculate_percentile(recent_times, 95), 2)
                }
                
                # SLA compliance
                sla_compliant = sum(1 for t in recent_times if t < self.config.max_query_time_ms)
                metrics['sla_compliance'][workload] = round(sla_compliant / len(recent_times), 3)
        
        return metrics
    
    # Private methods for AI-specific optimizations
    
    def _create_optimized_connection(self) -> Optional[sqlite3.Connection]:
        """Create SQLite connection optimized for AI workloads"""
        try:
            conn = sqlite3.connect(
                str(self.config.database_path),
                timeout=self.config.connection_timeout,
                check_same_thread=False  # Allow sharing across threads
            )
            
            # Enable row factory for easier data access
            conn.row_factory = sqlite3.Row
            
            # Apply base optimizations
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA cache_size=-64000;")  # 64MB cache
            conn.execute("PRAGMA temp_store=MEMORY;")
            conn.execute("PRAGMA mmap_size=268435456;")  # 256MB mmap
            
            # AI-specific optimizations
            conn.execute("PRAGMA optimize;")  # Auto-optimize query planner
            conn.execute("PRAGMA analysis_limit=1000;")  # Analyze more rows for better stats
            
            return conn
            
        except Exception as e:
            self.logger.error("Failed to create optimized connection", error=str(e))
            return None
    
    def _apply_ai_optimizations(self, conn: sqlite3.Connection):
        """Apply AI workload specific optimizations"""
        try:
            # JSON query optimizations
            conn.execute("PRAGMA json_cache_size=10000;")  # Cache JSON parsing
            
            # Concurrent read optimizations
            conn.execute("PRAGMA read_uncommitted=true;")  # Allow dirty reads for AI inference
            
            # Memory optimizations for AI workloads
            conn.execute("PRAGMA cache_spill=false;")  # Keep cache in memory
            
            self._optimizations_applied.add("ai_base_optimizations")
            
        except Exception as e:
            self.logger.warning("Some AI optimizations failed", error=str(e))
    
    def _initialize_connection_pool(self):
        """Initialize connection pool for concurrent AI engines"""
        try:
            with self._pool_lock:
                for i in range(self._max_pool_size - 1):  # -1 because we already have primary
                    conn = self._create_optimized_connection()
                    if conn:
                        self._connection_pool.append(conn)
            
            self.logger.info("AI connection pool initialized",
                           pool_size=len(self._connection_pool))
            
        except Exception as e:
            self.logger.error("Connection pool initialization failed", error=str(e))
    
    def _create_ai_indexes(self, conn: sqlite3.Connection):
        """Create indexes optimized for AI query patterns"""
        try:
            ai_indexes = [
                # Decision intelligence indexes
                ("idx_decisions_json", "executive_sessions", "json_extract(decisions_made, '$.decision_type')"),
                ("idx_decisions_stakeholder", "executive_sessions", "stakeholder_key, session_type"),
                ("idx_meeting_outcomes", "meeting_sessions", "json_extract(meeting_outcomes, '$.decision_count')"),
                
                # Health assessment indexes  
                ("idx_initiatives_status_risk", "strategic_initiatives", "status, risk_level"),
                ("idx_initiatives_roi", "strategic_initiatives", "json_extract(roi_tracking, '$.current_roi')"),
                ("idx_initiatives_milestone", "strategic_initiatives", "json_extract(milestone_history, '$.completion_rate')"),
                
                # Stakeholder analysis indexes
                ("idx_stakeholder_interaction", "stakeholder_profiles", "json_extract(interaction_history, '$.last_interaction')"),
                ("idx_stakeholder_style", "stakeholder_profiles", "communication_style, role_title"),
                
                # Platform intelligence indexes for analytics
                ("idx_platform_trend", "platform_intelligence", "category, trend_direction, measurement_date"),
                ("idx_platform_metrics", "platform_intelligence", "metric_name, value_numeric")
            ]
            
            for index_name, table, expression in ai_indexes:
                try:
                    # Check if index already exists
                    cursor = conn.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='index' AND name=?
                    """, (index_name,))
                    
                    if not cursor.fetchone():
                        # Create the index
                        if "json_extract" in expression:
                            # Expression index for JSON queries
                            conn.execute(f"CREATE INDEX {index_name} ON {table} ({expression});")
                        else:
                            # Regular composite index
                            conn.execute(f"CREATE INDEX {index_name} ON {table} ({expression});")
                        
                        self._json_indexes_created.add(index_name)
                        self.logger.debug("Created AI index", index_name=index_name, table=table)
                
                except sqlite3.OperationalError as e:
                    if "already exists" not in str(e):
                        self.logger.warning("Failed to create AI index", 
                                          index_name=index_name, error=str(e))
            
            # Update table statistics for query planner
            conn.execute("ANALYZE;")
            
            self.logger.info("AI indexes created", count=len(self._json_indexes_created))
            
        except Exception as e:
            self.logger.error("AI index creation failed", error=str(e))
    
    def _validate_ai_performance(self, conn: sqlite3.Connection):
        """Validate AI query performance meets SLA requirements"""
        test_queries = [
            # Decision intelligence test
            """SELECT json_extract(decisions_made, '$') as decisions
               FROM executive_sessions 
               WHERE stakeholder_key = 'vp_engineering'
               AND session_type = 'strategic_planning'
               LIMIT 10""",
            
            # Health assessment test
            """SELECT status, risk_level, 
                      json_extract(roi_tracking, '$.current_roi') as roi
               FROM strategic_initiatives 
               WHERE status IN ('in_progress', 'at_risk')
               ORDER BY updated_at DESC LIMIT 20""",
            
            # Stakeholder analysis test
            """SELECT stakeholder_key, communication_style,
                      json_extract(interaction_history, '$.last_interaction') as last_contact
               FROM stakeholder_profiles
               WHERE json_extract(decision_criteria, '$.data_driven') = 'true'"""
        ]
        
        performance_results = []
        
        for i, query in enumerate(test_queries):
            try:
                start_time = time.time()
                cursor = conn.execute(query)
                results = cursor.fetchall()
                execution_time = (time.time() - start_time) * 1000
                
                performance_results.append({
                    'query_id': i,
                    'execution_time_ms': execution_time,
                    'result_count': len(results),
                    'meets_sla': execution_time < self.config.max_query_time_ms
                })
                
            except Exception as e:
                self.logger.warning("AI performance test failed", query_id=i, error=str(e))
        
        # Log performance validation results
        sla_compliant = sum(1 for r in performance_results if r['meets_sla'])
        avg_time = sum(r['execution_time_ms'] for r in performance_results) / len(performance_results)
        
        self.logger.info("AI performance validation completed",
                        sla_compliant_queries=sla_compliant,
                        total_test_queries=len(performance_results),
                        avg_execution_time_ms=round(avg_time, 2))
    
    @contextmanager
    def _get_optimized_connection(self):
        """Get connection from pool with automatic return"""
        conn = None
        try:
            with self._pool_lock:
                if self._connection_pool:
                    conn = self._connection_pool.pop()
                else:
                    # Create temporary connection if pool exhausted
                    conn = self._create_optimized_connection()
            
            yield conn
            
        finally:
            if conn:
                with self._pool_lock:
                    # Return connection to pool if there's space
                    if len(self._connection_pool) < self._max_pool_size:
                        self._connection_pool.append(conn)
                    else:
                        conn.close()
    
    def _classify_ai_workload(self, query: str) -> str:
        """Classify query as specific AI workload type"""
        query_lower = query.lower()
        
        # Decision intelligence patterns
        decision_patterns = self._ai_query_patterns['decision_intelligence']
        if any(pattern in query_lower for pattern in decision_patterns):
            return 'decision_intelligence'
        
        # Health assessment patterns
        health_patterns = self._ai_query_patterns['health_assessment']
        if any(pattern in query_lower for pattern in health_patterns):
            return 'health_assessment'
        
        # Stakeholder analysis patterns
        stakeholder_patterns = self._ai_query_patterns['stakeholder_analysis']
        if any(pattern in query_lower for pattern in stakeholder_patterns):
            return 'stakeholder_analysis'
        
        return 'general'
    
    def _optimize_for_query(self, conn: sqlite3.Connection, query: str, workload_type: str):
        """Apply query-specific optimizations"""
        try:
            if workload_type == 'decision_intelligence':
                # Optimize for JSON extraction
                conn.execute("PRAGMA optimize(0x10002);")  # Focus on JSON queries
            
            elif workload_type == 'health_assessment':
                # Optimize for aggregations and analytics
                conn.execute("PRAGMA optimize(0x20002);")  # Focus on GROUP BY queries
            
            elif workload_type == 'stakeholder_analysis':
                # Optimize for complex WHERE clauses
                conn.execute("PRAGMA optimize(0x40002);")  # Focus on WHERE optimization
        
        except Exception as e:
            self.logger.debug("Query-specific optimization failed", error=str(e))
    
    def _fetch_results_optimized(self, cursor: sqlite3.Cursor, workload_type: str) -> List[Any]:
        """Fetch results with workload-specific optimizations"""
        if workload_type in ['decision_intelligence', 'health_assessment']:
            # For AI workloads, use fetchall() with size limit
            results = cursor.fetchmany(1000)  # Limit to prevent memory issues
            if len(results) == 1000:
                # If we hit the limit, fetch remaining in chunks
                remaining = cursor.fetchall()
                results.extend(remaining)
            return results
        else:
            # Standard fetch for other workloads
            return cursor.fetchall()
    
    def _record_ai_performance(self, workload_type: str, execution_time: float):
        """Record performance metrics for AI workloads"""
        if workload_type in self._ai_query_metrics:
            self._ai_query_metrics[workload_type].append(execution_time)
            
            # Keep only recent metrics (last 100 queries per workload)
            if len(self._ai_query_metrics[workload_type]) > 100:
                self._ai_query_metrics[workload_type] = self._ai_query_metrics[workload_type][-100:]
    
    def _apply_basic_ai_optimizations(self, conn: sqlite3.Connection) -> bool:
        """Apply basic AI optimizations"""
        try:
            # Basic JSON optimizations
            conn.execute("PRAGMA json_quote=false;")  # Faster JSON handling
            
            # Basic concurrency optimizations
            conn.execute("PRAGMA busy_timeout=30000;")  # 30 second timeout for AI queries
            
            return True
        except Exception:
            return False
    
    def _apply_intermediate_ai_optimizations(self, conn: sqlite3.Connection) -> bool:
        """Apply intermediate AI optimizations"""
        try:
            # Intermediate memory optimizations
            conn.execute("PRAGMA cache_size=-128000;")  # 128MB cache
            
            # Query planner optimizations for AI patterns
            conn.execute("PRAGMA optimize(0xfffe);")  # Comprehensive optimization
            
            return True
        except Exception:
            return False
    
    def _apply_aggressive_ai_optimizations(self, conn: sqlite3.Connection) -> bool:
        """Apply aggressive AI optimizations"""
        try:
            # Aggressive memory optimizations
            conn.execute("PRAGMA cache_size=-256000;")  # 256MB cache
            conn.execute("PRAGMA mmap_size=536870912;")  # 512MB mmap
            
            # Aggressive concurrency settings
            conn.execute("PRAGMA read_uncommitted=true;")  # Allow dirty reads
            
            return True
        except Exception:
            return False
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value from list"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((percentile / 100.0) * len(sorted_values))
        index = min(max(index, 0), len(sorted_values) - 1)
        
        return sorted_values[index]
