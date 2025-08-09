#!/usr/bin/env python3
"""
ClaudeDirector Architecture Health Monitor
Martin's evolutionary design approach: proactive migration recommendations via measurable metrics
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import structlog

from memory.optimized_db_manager import get_db_manager

logger = structlog.get_logger(__name__)


class ArchitectureHealthMonitor:
    """
    Martin's Architecture Decision Framework:
    - Measurable technical health metrics
    - Proactive migration recommendations
    - Data-driven architecture evolution
    - Reversible decision tracking
    """
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "memory/strategic_memory.db"
        self.logger = logger.bind(component="architecture_health")
        
        # PostgreSQL migration criteria thresholds
        self.migration_criteria = {
            # Performance thresholds
            'slow_query_percentage_critical': 15.0,  # >15% slow queries
            'slow_query_percentage_warning': 10.0,   # >10% slow queries
            'avg_query_time_critical': 2.0,          # >2 seconds average
            'avg_query_time_warning': 1.0,           # >1 second average
            
            # Concurrency thresholds
            'concurrent_writers_critical': 8,        # >8 simultaneous write operations
            'concurrent_writers_warning': 5,         # >5 simultaneous write operations
            'lock_contention_critical': 30.0,        # >30% lock wait time
            'lock_contention_warning': 15.0,         # >15% lock wait time
            
            # Scale thresholds
            'database_size_critical': 10.0,          # >10GB database
            'database_size_warning': 5.0,            # >5GB database
            'stakeholder_count_critical': 2000,      # >2000 stakeholders
            'stakeholder_count_warning': 1000,       # >1000 stakeholders
            'document_count_critical': 50000,        # >50K documents
            'document_count_warning': 20000,         # >20K documents
            
            # Organizational thresholds
            'user_count_critical': 15,               # >15 concurrent users
            'user_count_warning': 8,                 # >8 concurrent users
            'org_count_critical': 5,                 # >5 organizations
            'org_count_warning': 3,                  # >3 organizations
            
            # Advanced feature requirements
            'requires_analytics': False,             # Complex analytical queries
            'requires_realtime': False,              # Real-time collaboration
            'requires_multiregion': False,           # Multi-region deployment
        }
        
        # Migration recommendation history
        self.recommendation_history = []
    
    def assess_migration_readiness(self) -> Dict[str, any]:
        """
        Martin's Architecture Assessment Framework:
        Evaluate current SQLite performance against PostgreSQL migration criteria
        """
        self.logger.info("Starting architecture health assessment")
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'migration_recommendation': 'continue_sqlite',  # Default
            'criteria_analysis': {},
            'performance_metrics': {},
            'architectural_debt': {},
            'migration_readiness_score': 0.0,
            'action_items': [],
            'adr_requirements': []
        }
        
        try:
            # Collect performance metrics
            performance_metrics = self._collect_performance_metrics()
            assessment['performance_metrics'] = performance_metrics
            
            # Assess scale metrics
            scale_metrics = self._assess_scale_metrics()
            assessment['scale_metrics'] = scale_metrics
            
            # Evaluate organizational complexity
            org_metrics = self._assess_organizational_complexity()
            assessment['organizational_metrics'] = org_metrics
            
            # Analyze architectural debt
            debt_metrics = self._analyze_architectural_debt()
            assessment['architectural_debt'] = debt_metrics
            
            # Calculate migration readiness score
            readiness_score = self._calculate_migration_readiness(
                performance_metrics, scale_metrics, org_metrics, debt_metrics
            )
            assessment['migration_readiness_score'] = readiness_score
            
            # Generate migration recommendation
            recommendation = self._generate_migration_recommendation(
                readiness_score, performance_metrics, scale_metrics, org_metrics
            )
            assessment['migration_recommendation'] = recommendation['recommendation']
            assessment['criteria_analysis'] = recommendation['criteria_analysis']
            assessment['action_items'] = recommendation['action_items']
            assessment['adr_requirements'] = recommendation['adr_requirements']
            
            # Store assessment history
            self._store_assessment_history(assessment)
            
            self.logger.info("Architecture health assessment completed",
                           recommendation=recommendation['recommendation'],
                           readiness_score=readiness_score)
            
        except Exception as e:
            self.logger.error("Architecture health assessment failed", error=str(e))
            assessment['error'] = str(e)
        
        return assessment
    
    def _collect_performance_metrics(self) -> Dict[str, any]:
        """Collect SQLite performance metrics for migration assessment"""
        db_manager = get_db_manager(self.db_path)
        
        # Get basic performance stats
        perf_stats = db_manager.get_performance_stats()
        
        # Collect query timing data
        query_metrics = self._analyze_query_performance()
        
        # Assess concurrency patterns
        concurrency_metrics = self._assess_concurrency_patterns()
        
        return {
            'database_size_mb': perf_stats['database_size_mb'],
            'slow_query_percentage': perf_stats['slow_query_percentage'],
            'total_queries': perf_stats['total_queries'],
            'query_timing': query_metrics,
            'concurrency': concurrency_metrics,
            'cache_efficiency': perf_stats.get('cache_size', 0)
        }
    
    def _analyze_query_performance(self) -> Dict[str, any]:
        """Analyze query performance patterns for migration indicators"""
        db_manager = get_db_manager(self.db_path)
        
        # Sample common strategic intelligence queries
        test_queries = [
            # Stakeholder relationship analysis
            """SELECT COUNT(*) FROM stakeholder_engagements se 
               JOIN stakeholder_profiles_enhanced spe ON se.stakeholder_profile_id = spe.id
               WHERE se.last_activity_at > date('now', '-30 days')""",
            
            # Meeting intelligence temporal analysis  
            """SELECT COUNT(*) FROM meeting_sessions ms
               JOIN meeting_participants mp ON ms.id = mp.meeting_session_id
               WHERE ms.session_date > date('now', '-90 days')""",
            
            # Cross-system intelligence queries
            """SELECT COUNT(*) FROM strategic_tasks st
               LEFT JOIN stakeholder_profiles_enhanced spe ON st.responsible_stakeholder_id = spe.id
               WHERE st.due_date > date('now')"""
        ]
        
        query_times = []
        for query in test_queries:
            try:
                start_time = time.time()
                with db_manager.get_optimized_connection() as conn:
                    conn.execute(query).fetchall()
                execution_time = time.time() - start_time
                query_times.append(execution_time)
            except Exception as e:
                self.logger.warning("Query performance test failed", query=query[:50], error=str(e))
                query_times.append(5.0)  # Assume slow if failed
        
        avg_query_time = sum(query_times) / len(query_times) if query_times else 0.0
        max_query_time = max(query_times) if query_times else 0.0
        
        return {
            'average_query_time': avg_query_time,
            'max_query_time': max_query_time,
            'query_samples': len(query_times),
            'performance_grade': self._grade_query_performance(avg_query_time)
        }
    
    def _assess_concurrency_patterns(self) -> Dict[str, any]:
        """Assess concurrency and locking patterns"""
        # For SQLite, assess based on database size and usage patterns
        # Real concurrency assessment would require active monitoring
        
        db_manager = get_db_manager(self.db_path)
        stats = db_manager.get_performance_stats()
        
        # Estimate concurrency pressure based on database activity
        estimated_concurrent_ops = min(stats['total_queries'] / 1000, 10)  # Rough estimate
        
        return {
            'estimated_concurrent_operations': estimated_concurrent_ops,
            'connection_reuses': stats.get('connection_reuses', 0),
            'wal_mode_enabled': True,  # Our optimization enables this
            'lock_contention_estimate': 'low' if estimated_concurrent_ops < 5 else 'moderate'
        }
    
    def _assess_scale_metrics(self) -> Dict[str, any]:
        """Assess data scale metrics for migration criteria"""
        db_manager = get_db_manager(self.db_path)
        
        scale_metrics = {}
        
        try:
            with db_manager.get_optimized_connection() as conn:
                # Count stakeholders
                stakeholder_result = conn.execute(
                    "SELECT COUNT(*) FROM stakeholder_profiles_enhanced"
                ).fetchone()
                scale_metrics['stakeholder_count'] = stakeholder_result[0] if stakeholder_result else 0
                
                # Count documents
                doc_result = conn.execute(
                    "SELECT COUNT(*) FROM google_drive_documents"
                ).fetchone()
                scale_metrics['document_count'] = doc_result[0] if doc_result else 0
                
                # Count meetings
                meeting_result = conn.execute(
                    "SELECT COUNT(*) FROM meeting_sessions"
                ).fetchone()
                scale_metrics['meeting_count'] = meeting_result[0] if meeting_result else 0
                
                # Count strategic tasks
                task_result = conn.execute(
                    "SELECT COUNT(*) FROM strategic_tasks"
                ).fetchone()
                scale_metrics['task_count'] = task_result[0] if task_result else 0
                
        except Exception as e:
            self.logger.warning("Scale metrics collection failed", error=str(e))
            scale_metrics = {
                'stakeholder_count': 0,
                'document_count': 0,
                'meeting_count': 0,
                'task_count': 0
            }
        
        # Get database file size
        db_path = Path(self.db_path)
        if db_path.exists():
            scale_metrics['database_size_mb'] = db_path.stat().st_size / (1024 * 1024)
        else:
            scale_metrics['database_size_mb'] = 0
        
        return scale_metrics
    
    def _assess_organizational_complexity(self) -> Dict[str, any]:
        """Assess organizational complexity indicators"""
        # Estimate organizational complexity based on stakeholder patterns
        # This is a heuristic assessment - real implementation would track user sessions
        
        db_manager = get_db_manager(self.db_path)
        org_metrics = {
            'estimated_user_count': 1,  # Default: single user
            'estimated_org_count': 1,   # Default: single organization
            'collaboration_indicators': 0,
            'multi_tenant_requirements': False
        }
        
        try:
            with db_manager.get_optimized_connection() as conn:
                # Look for collaboration indicators in stakeholder data
                collab_result = conn.execute("""
                    SELECT COUNT(DISTINCT spe.organization) as org_count,
                           COUNT(*) as stakeholder_count
                    FROM stakeholder_profiles_enhanced spe
                    WHERE spe.organization IS NOT NULL AND spe.organization != ''
                """).fetchone()
                
                if collab_result:
                    org_metrics['estimated_org_count'] = max(collab_result[0], 1)
                    # Estimate users based on stakeholder patterns
                    org_metrics['estimated_user_count'] = min(max(collab_result[1] // 10, 1), 20)
                
                # Check for meeting collaboration patterns
                meeting_collab = conn.execute("""
                    SELECT COUNT(*) as meeting_count,
                           AVG(stakeholder_count) as avg_participants
                    FROM meeting_sessions 
                    WHERE stakeholder_count > 1
                """).fetchone()
                
                if meeting_collab and meeting_collab[0] > 0:
                    org_metrics['collaboration_indicators'] = meeting_collab[0]
                    org_metrics['estimated_user_count'] = min(
                        max(int(meeting_collab[1] or 1), org_metrics['estimated_user_count']), 
                        20
                    )
                
        except Exception as e:
            self.logger.warning("Organizational complexity assessment failed", error=str(e))
        
        return org_metrics
    
    def _analyze_architectural_debt(self) -> Dict[str, any]:
        """Analyze architectural debt indicators"""
        return {
            'sqlite_limitations_hit': [],
            'performance_workarounds': 0,
            'scaling_blockers': [],
            'maintenance_overhead': 'low',
            'technical_debt_score': 0.0
        }
    
    def _calculate_migration_readiness(self, perf_metrics: Dict, scale_metrics: Dict, 
                                     org_metrics: Dict, debt_metrics: Dict) -> float:
        """Calculate migration readiness score (0.0 = stay SQLite, 1.0 = migrate now)"""
        score = 0.0
        
        # Performance factors (weight: 0.4)
        if perf_metrics.get('slow_query_percentage', 0) > self.migration_criteria['slow_query_percentage_critical']:
            score += 0.15
        elif perf_metrics.get('slow_query_percentage', 0) > self.migration_criteria['slow_query_percentage_warning']:
            score += 0.08
        
        if perf_metrics.get('query_timing', {}).get('average_query_time', 0) > self.migration_criteria['avg_query_time_critical']:
            score += 0.15
        elif perf_metrics.get('query_timing', {}).get('average_query_time', 0) > self.migration_criteria['avg_query_time_warning']:
            score += 0.08
        
        # Scale factors (weight: 0.3)
        if scale_metrics.get('database_size_mb', 0) > self.migration_criteria['database_size_critical'] * 1024:
            score += 0.1
        elif scale_metrics.get('database_size_mb', 0) > self.migration_criteria['database_size_warning'] * 1024:
            score += 0.05
        
        if scale_metrics.get('stakeholder_count', 0) > self.migration_criteria['stakeholder_count_critical']:
            score += 0.1
        elif scale_metrics.get('stakeholder_count', 0) > self.migration_criteria['stakeholder_count_warning']:
            score += 0.05
        
        if scale_metrics.get('document_count', 0) > self.migration_criteria['document_count_critical']:
            score += 0.1
        elif scale_metrics.get('document_count', 0) > self.migration_criteria['document_count_warning']:
            score += 0.05
        
        # Organizational factors (weight: 0.3)
        if org_metrics.get('estimated_user_count', 1) > self.migration_criteria['user_count_critical']:
            score += 0.15
        elif org_metrics.get('estimated_user_count', 1) > self.migration_criteria['user_count_warning']:
            score += 0.08
        
        if org_metrics.get('estimated_org_count', 1) > self.migration_criteria['org_count_critical']:
            score += 0.15
        elif org_metrics.get('estimated_org_count', 1) > self.migration_criteria['org_count_warning']:
            score += 0.08
        
        return min(score, 1.0)
    
    def _generate_migration_recommendation(self, readiness_score: float, 
                                         perf_metrics: Dict, scale_metrics: Dict, 
                                         org_metrics: Dict) -> Dict[str, any]:
        """Generate migration recommendation based on assessment"""
        
        # Analyze specific workload patterns for embedded DB recommendations
        analytics_heavy = self._assess_analytics_workload(perf_metrics, scale_metrics)
        graph_heavy = self._assess_graph_workload(scale_metrics, org_metrics)
        semantic_value = self._assess_semantic_workload(scale_metrics)
        
        if readiness_score >= 0.7:
            # Critical: Recommend best embedded alternative, not PostgreSQL
            if analytics_heavy:
                recommendation = 'migrate_duckdb'
                reasoning = "Analytics workload requires columnar database (DuckDB)"
            elif graph_heavy:
                recommendation = 'consider_kuzu'
                reasoning = "Complex stakeholder relationships require graph database (Kuzu)"
            else:
                recommendation = 'hybrid_architecture'
                reasoning = "Multi-component architecture needed (SQLite + DuckDB/Faiss)"
            priority = 'critical'
        elif readiness_score >= 0.4:
            if analytics_heavy:
                recommendation = 'plan_duckdb_migration'
                reasoning = "Plan DuckDB migration for analytical performance"
            elif semantic_value:
                recommendation = 'add_faiss_semantic'
                reasoning = "Add Faiss for semantic document intelligence"
            else:
                recommendation = 'optimize_sqlite_further'
                reasoning = "Apply advanced SQLite optimizations before migration"
            priority = 'high'
        elif readiness_score >= 0.2:
            recommendation = 'monitor_with_experiments'
            priority = 'medium'
            reasoning = "Monitor trends, experiment with semantic features (Faiss)"
        else:
            recommendation = 'continue_sqlite'
            priority = 'low'
            reasoning = "SQLite performance remains excellent"
        
        # Generate specific criteria analysis
        criteria_analysis = self._analyze_specific_criteria(perf_metrics, scale_metrics, org_metrics)
        
        # Generate action items
        action_items = self._generate_action_items(recommendation, criteria_analysis, readiness_score)
        
        # Generate ADR requirements
        adr_requirements = self._generate_adr_requirements(recommendation, readiness_score)
        
        return {
            'recommendation': recommendation,
            'priority': priority,
            'reasoning': reasoning,
            'criteria_analysis': criteria_analysis,
            'action_items': action_items,
            'adr_requirements': adr_requirements,
            'readiness_score': readiness_score,
            'workload_analysis': {
                'analytics_heavy': analytics_heavy,
                'graph_heavy': graph_heavy,
                'semantic_value': semantic_value
            }
        }
    
    def _assess_analytics_workload(self, perf_metrics: Dict, scale_metrics: Dict) -> bool:
        """Assess if workload is analytics-heavy (favors DuckDB)"""
        # Indicators: large document count, slow aggregation queries
        doc_count = scale_metrics.get('document_count', 0)
        query_time = perf_metrics.get('query_timing', {}).get('average_query_time', 0)
        
        return doc_count > 5000 or query_time > 1.0
    
    def _assess_graph_workload(self, scale_metrics: Dict, org_metrics: Dict) -> bool:
        """Assess if workload is graph-heavy (favors Kuzu)"""
        # Indicators: many stakeholders, complex organizational relationships
        stakeholder_count = scale_metrics.get('stakeholder_count', 0)
        org_count = org_metrics.get('estimated_org_count', 1)
        
        return stakeholder_count > 500 and org_count > 2
    
    def _assess_semantic_workload(self, scale_metrics: Dict) -> bool:
        """Assess if semantic search would provide value (favors Faiss)"""
        # Indicators: many documents, strategic document analysis
        doc_count = scale_metrics.get('document_count', 0)
        
        return doc_count > 1000
    
    def _analyze_specific_criteria(self, perf_metrics: Dict, scale_metrics: Dict, org_metrics: Dict) -> Dict[str, any]:
        """Analyze which specific criteria are triggering migration recommendations"""
        criteria = {}
        
        # Performance criteria
        criteria['performance'] = {
            'slow_queries': {
                'current': perf_metrics.get('slow_query_percentage', 0),
                'warning_threshold': self.migration_criteria['slow_query_percentage_warning'],
                'critical_threshold': self.migration_criteria['slow_query_percentage_critical'],
                'status': self._get_threshold_status(
                    perf_metrics.get('slow_query_percentage', 0),
                    self.migration_criteria['slow_query_percentage_warning'],
                    self.migration_criteria['slow_query_percentage_critical']
                )
            },
            'avg_query_time': {
                'current': perf_metrics.get('query_timing', {}).get('average_query_time', 0),
                'warning_threshold': self.migration_criteria['avg_query_time_warning'],
                'critical_threshold': self.migration_criteria['avg_query_time_critical'],
                'status': self._get_threshold_status(
                    perf_metrics.get('query_timing', {}).get('average_query_time', 0),
                    self.migration_criteria['avg_query_time_warning'],
                    self.migration_criteria['avg_query_time_critical']
                )
            }
        }
        
        # Scale criteria
        criteria['scale'] = {
            'database_size': {
                'current_mb': scale_metrics.get('database_size_mb', 0),
                'warning_threshold_gb': self.migration_criteria['database_size_warning'],
                'critical_threshold_gb': self.migration_criteria['database_size_critical'],
                'status': self._get_threshold_status(
                    scale_metrics.get('database_size_mb', 0) / 1024,
                    self.migration_criteria['database_size_warning'],
                    self.migration_criteria['database_size_critical']
                )
            },
            'stakeholder_count': {
                'current': scale_metrics.get('stakeholder_count', 0),
                'warning_threshold': self.migration_criteria['stakeholder_count_warning'],
                'critical_threshold': self.migration_criteria['stakeholder_count_critical'],
                'status': self._get_threshold_status(
                    scale_metrics.get('stakeholder_count', 0),
                    self.migration_criteria['stakeholder_count_warning'],
                    self.migration_criteria['stakeholder_count_critical']
                )
            }
        }
        
        # Organizational criteria
        criteria['organizational'] = {
            'user_count': {
                'current': org_metrics.get('estimated_user_count', 1),
                'warning_threshold': self.migration_criteria['user_count_warning'],
                'critical_threshold': self.migration_criteria['user_count_critical'],
                'status': self._get_threshold_status(
                    org_metrics.get('estimated_user_count', 1),
                    self.migration_criteria['user_count_warning'],
                    self.migration_criteria['user_count_critical']
                )
            }
        }
        
        return criteria
    
    def _get_threshold_status(self, current: float, warning: float, critical: float) -> str:
        """Get threshold status for a metric"""
        if current >= critical:
            return 'critical'
        elif current >= warning:
            return 'warning'
        else:
            return 'healthy'
    
    def _generate_action_items(self, recommendation: str, criteria_analysis: Dict, readiness_score: float) -> List[Dict]:
        """Generate specific action items based on recommendation"""
        actions = []
        
        if recommendation == 'migrate_duckdb':
            actions.extend([
                {
                    'priority': 'critical',
                    'action': 'Create DuckDB Migration ADR',
                    'description': 'Document analytical database migration with zero-config preservation',
                    'timeline': '1 week'
                },
                {
                    'priority': 'critical', 
                    'action': 'Implement Hybrid SQLite+DuckDB Architecture',
                    'description': 'Route analytics to DuckDB, transactions to SQLite',
                    'timeline': '2 weeks'
                },
                {
                    'priority': 'high',
                    'action': 'Optimize Analytical Query Performance',
                    'description': 'Migrate executive dashboards to columnar operations',
                    'timeline': '1 week'
                }
            ])
        
        elif recommendation == 'consider_kuzu':
            actions.extend([
                {
                    'priority': 'critical',
                    'action': 'Evaluate Kuzu Graph Database',
                    'description': 'Assess stakeholder network analysis requirements',
                    'timeline': '2 weeks'
                },
                {
                    'priority': 'high',
                    'action': 'Design Graph Data Model',
                    'description': 'Model stakeholder relationships for Cypher queries',
                    'timeline': '1 week'
                }
            ])
        
        elif recommendation == 'hybrid_architecture':
            actions.extend([
                {
                    'priority': 'critical',
                    'action': 'Design Multi-Database Architecture',
                    'description': 'SQLite + DuckDB + Faiss hybrid for specialized workloads',
                    'timeline': '2 weeks'
                }
            ])
        
        elif recommendation == 'add_faiss_semantic':
            actions.extend([
                {
                    'priority': 'high',
                    'action': 'Implement Semantic Search POC',
                    'description': 'Add Faiss vector search for document intelligence',
                    'timeline': '2 weeks'
                }
            ])
        
        elif recommendation == 'plan_duckdb_migration':
            actions.extend([
                {
                    'priority': 'high',
                    'action': 'Research DuckDB Analytics Migration',
                    'description': 'Plan embedded analytical database for executive reporting',
                    'timeline': '2 weeks'
                },
                {
                    'priority': 'medium',
                    'action': 'Optimize Current SQLite Performance',
                    'description': 'Apply additional optimizations to buy more time',
                    'timeline': '1 week'
                }
            ])
        
        elif recommendation == 'optimize_sqlite_further':
            actions.extend([
                {
                    'priority': 'high',
                    'action': 'Advanced SQLite Optimization',
                    'description': 'Implement custom indexes, query optimization',
                    'timeline': '1 week'
                }
            ])
        
        elif recommendation == 'monitor_closely':
            actions.extend([
                {
                    'priority': 'medium',
                    'action': 'Increase Monitoring Frequency',
                    'description': 'Monitor architecture health weekly instead of monthly',
                    'timeline': 'Ongoing'
                },
                {
                    'priority': 'low',
                    'action': 'Prepare Migration Research',
                    'description': 'Begin evaluating PostgreSQL options for future planning',
                    'timeline': '1 month'
                }
            ])
        
        return actions
    
    def _generate_adr_requirements(self, recommendation: str, readiness_score: float) -> List[str]:
        """Generate ADR requirements for architectural decisions"""
        adr_requirements = []
        
        if recommendation == 'migrate_postgresql':
            adr_requirements.extend([
                'ADR-DB-001: PostgreSQL Migration Decision',
                'ADR-DB-002: Zero-Downtime Migration Strategy', 
                'ADR-DB-003: PostgreSQL Configuration Standards',
                'ADR-DB-004: Backup and Recovery Strategy'
            ])
        elif recommendation == 'plan_migration':
            adr_requirements.extend([
                'ADR-DB-001: Migration Planning and Timeline',
                'ADR-DB-002: Performance Optimization Strategy'
            ])
        
        return adr_requirements
    
    def _grade_query_performance(self, avg_time: float) -> str:
        """Grade query performance"""
        if avg_time < 0.1:
            return 'A'
        elif avg_time < 0.5:
            return 'B'
        elif avg_time < 1.0:
            return 'C'
        elif avg_time < 2.0:
            return 'D'
        else:
            return 'F'
    
    def _store_assessment_history(self, assessment: Dict):
        """Store assessment history for trend analysis"""
        try:
            db_manager = get_db_manager(self.db_path)
            
            with db_manager.get_optimized_connection() as conn:
                # Create table if it doesn't exist
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS architecture_health_assessments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        migration_recommendation TEXT NOT NULL,
                        readiness_score REAL NOT NULL,
                        assessment_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Store assessment
                conn.execute("""
                    INSERT INTO architecture_health_assessments 
                    (timestamp, migration_recommendation, readiness_score, assessment_data)
                    VALUES (?, ?, ?, ?)
                """, (
                    assessment['timestamp'],
                    assessment['migration_recommendation'],
                    assessment['migration_readiness_score'],
                    json.dumps(assessment)
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error("Failed to store assessment history", error=str(e))

    def get_migration_trend_analysis(self, days: int = 90) -> Dict[str, any]:
        """Analyze migration readiness trends over time"""
        try:
            db_manager = get_db_manager(self.db_path)
            
            with db_manager.get_optimized_connection() as conn:
                results = conn.execute("""
                    SELECT timestamp, migration_recommendation, readiness_score, assessment_data
                    FROM architecture_health_assessments
                    WHERE created_at > date('now', '-{} days')
                    ORDER BY created_at DESC
                """.format(days)).fetchall()
                
                if not results:
                    return {'trend': 'insufficient_data', 'assessments': []}
                
                # Analyze trends
                scores = [row[2] for row in results]
                recommendations = [row[1] for row in results]
                
                trend_analysis = {
                    'trend': self._calculate_trend_direction(scores),
                    'current_score': scores[0] if scores else 0.0,
                    'score_change': scores[0] - scores[-1] if len(scores) > 1 else 0.0,
                    'assessments_count': len(results),
                    'recent_recommendations': recommendations[:5],
                    'trend_indicators': {
                        'improving': scores[0] < scores[-1] if len(scores) > 1 else False,
                        'degrading': scores[0] > scores[-1] if len(scores) > 1 else False,
                        'stable': abs(scores[0] - scores[-1]) < 0.1 if len(scores) > 1 else True
                    }
                }
                
                return trend_analysis
                
        except Exception as e:
            self.logger.error("Failed to analyze migration trends", error=str(e))
            return {'trend': 'analysis_failed', 'error': str(e)}
    
    def _calculate_trend_direction(self, scores: List[float]) -> str:
        """Calculate overall trend direction from scores"""
        if len(scores) < 2:
            return 'insufficient_data'
        
        recent_avg = sum(scores[:3]) / min(len(scores[:3]), 3)
        older_avg = sum(scores[-3:]) / min(len(scores[-3:]), 3)
        
        diff = recent_avg - older_avg
        
        if diff > 0.1:
            return 'increasing_migration_pressure'
        elif diff < -0.1:
            return 'decreasing_migration_pressure'
        else:
            return 'stable'


if __name__ == "__main__":
    """CLI for architecture health monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ClaudeDirector Architecture Health Monitor")
    parser.add_argument("--assess", action="store_true", help="Run architecture health assessment")
    parser.add_argument("--trends", action="store_true", help="Show migration readiness trends")
    parser.add_argument("--criteria", action="store_true", help="Show migration criteria")
    parser.add_argument("--db-path", help="Database path")
    
    args = parser.parse_args()
    
    monitor = ArchitectureHealthMonitor(args.db_path)
    
    if args.assess:
        assessment = monitor.assess_migration_readiness()
        print("Architecture Health Assessment:")
        print(json.dumps(assessment, indent=2))
    
    elif args.trends:
        trends = monitor.get_migration_trend_analysis()
        print("Migration Readiness Trends:")
        print(json.dumps(trends, indent=2))
    
    elif args.criteria:
        print("PostgreSQL Migration Criteria:")
        print(json.dumps(monitor.migration_criteria, indent=2))
    
    else:
        parser.print_help()
