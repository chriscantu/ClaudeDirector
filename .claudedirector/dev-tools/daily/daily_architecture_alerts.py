#!/usr/bin/env python3
"""
ClaudeDirector Daily Architecture Health Alerts
Martin's proactive migration notification system
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from memory.architecture_health_monitor import ArchitectureHealthMonitor


class DailyArchitectureAlerts:
    """
    Martin's Architecture Decision Framework:
    Proactive migration alerts based on measurable criteria
    """

    def __init__(self):
        self.monitor = ArchitectureHealthMonitor()
        self.alert_thresholds = {
            "migration_readiness_critical": 0.7,
            "migration_readiness_warning": 0.4,
            "migration_readiness_monitor": 0.2,
        }

    def generate_daily_alerts(self) -> bool:
        """Generate daily architecture health alerts"""
        print("🏗️  ClaudeDirector Architecture Health Alert")
        print("=" * 50)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        try:
            # Run architecture health assessment
            assessment = self.monitor.assess_migration_readiness()

            if "error" in assessment:
                print("❌ Architecture health assessment failed")
                print(f"   Error: {assessment['error']}")
                return False

            # Extract key metrics
            recommendation = assessment["migration_recommendation"]
            readiness_score = assessment["migration_readiness_score"]
            criteria_analysis = assessment.get("criteria_analysis", {})
            action_items = assessment.get("action_items", [])

            # Generate alerts based on migration readiness
            if readiness_score >= self.alert_thresholds["migration_readiness_critical"]:
                self._generate_critical_migration_alert(assessment)
            elif (
                readiness_score >= self.alert_thresholds["migration_readiness_warning"]
            ):
                self._generate_warning_migration_alert(assessment)
            elif (
                readiness_score >= self.alert_thresholds["migration_readiness_monitor"]
            ):
                self._generate_monitoring_alert(assessment)
            else:
                self._generate_healthy_status(assessment)

            # Show trend analysis
            self._show_trend_analysis()

            # Show specific criteria status
            self._show_criteria_status(criteria_analysis)

            # Show action items if any
            if action_items:
                self._show_action_items(action_items)

            print()
            print("💡 Architecture Health Commands:")
            print("   claudedirector db-optimize --stats-only  # Current performance")
            print(
                "   python memory/architecture_health_monitor.py --assess  # Full assessment"
            )
            print(
                "   python memory/architecture_health_monitor.py --trends  # Trend analysis"
            )

            return True

        except Exception as e:
            print(f"❌ Daily architecture alert generation failed: {e}")
            return False

    def _generate_critical_migration_alert(self, assessment: Dict):
        """Generate critical migration alert"""
        readiness_score = assessment["migration_readiness_score"]
        recommendation = assessment["migration_recommendation"]
        workload = assessment.get("workload_analysis", {})

        print("🚨 CRITICAL: Embedded Database Migration Recommended")
        print("=" * 55)
        print(f"   Migration Readiness Score: {readiness_score:.2f}/1.00")
        print(f"   Recommendation: {recommendation}")
        print()
        print("⚠️  Multiple critical migration criteria have been exceeded.")
        print(
            "   ClaudeDirector's SQLite database is approaching architectural limits."
        )
        print()

        # Provide specific embedded database recommendations
        if recommendation == "migrate_duckdb":
            print("📊 RECOMMENDED: DuckDB for Analytics Performance")
            print("   • Zero-config embedded analytical database")
            print("   • 10-100x faster executive dashboard queries")
            print("   • Maintains single-file deployment simplicity")
            print("   • Perfect for ClaudeDirector's analytical workload")
        elif recommendation == "consider_kuzu":
            print("🕸️  RECOMMENDED: Kuzu for Graph Relationships")
            print("   • Zero-config embedded graph database")
            print("   • Optimized for stakeholder network analysis")
            print("   • Natural organizational relationship queries")
            print("   • Maintains ClaudeDirector's plug-and-play philosophy")
        elif recommendation == "hybrid_architecture":
            print("🏗️  RECOMMENDED: Hybrid Embedded Architecture")
            print("   • SQLite + DuckDB + Faiss specialized components")
            print("   • Best performance for each workload type")
            print("   • Zero external dependencies")
            print("   • Maintains deployment simplicity")

        print()
        print("📋 IMMEDIATE ACTIONS REQUIRED:")
        if recommendation == "migrate_duckdb":
            print("   1. Create DuckDB Migration ADR (Architecture Decision Record)")
            print("   2. Implement hybrid SQLite+DuckDB architecture")
            print("   3. Route analytics to DuckDB, transactions to SQLite")
        elif recommendation == "consider_kuzu":
            print("   1. Evaluate Kuzu graph database for stakeholder networks")
            print("   2. Design graph data model for organizational relationships")
            print("   3. Plan Cypher query migration strategy")
        else:
            print("   1. Design multi-database embedded architecture")
            print("   2. Plan workload-specific database routing")
            print("   3. Implement zero-downtime migration strategy")

        print()
        print("🎯 Martin's Embedded Database Framework:")
        print("   • Preserve zero-config deployment philosophy")
        print("   • Use embedded alternatives over PostgreSQL complexity")
        print("   • Maintain ClaudeDirector's plug-and-play experience")
        print("   • Choose database by workload characteristics")

    def _generate_warning_migration_alert(self, assessment: Dict):
        """Generate warning migration alert"""
        readiness_score = assessment["migration_readiness_score"]
        recommendation = assessment["migration_recommendation"]
        workload = assessment.get("workload_analysis", {})

        print("⚠️  WARNING: Approaching Embedded Database Migration Thresholds")
        print("=" * 60)
        print(f"   Migration Readiness Score: {readiness_score:.2f}/1.00")
        print(f"   Recommendation: {recommendation}")
        print()
        print("📈 ClaudeDirector is approaching SQLite performance limits.")
        print(
            "   Consider planning embedded database migration in the next 1-3 months."
        )
        print()

        # Workload-specific recommendations
        if workload.get("analytics_heavy"):
            print("📊 Analytics Workload Detected:")
            print("   • Executive reporting becoming performance bottleneck")
            print("   • DuckDB migration recommended for analytical queries")
            print("   • Maintain SQLite for transactional operations")

        if workload.get("semantic_value"):
            print("🔍 Semantic Search Opportunity:")
            print("   • Document intelligence could benefit from vector search")
            print("   • Consider adding Faiss for semantic document features")
            print("   • Hybrid SQLite + Faiss architecture")

        if workload.get("graph_heavy"):
            print("🕸️  Graph Relationships Detected:")
            print("   • Complex stakeholder networks present")
            print("   • Kuzu graph database could optimize relationship queries")
            print("   • Natural organizational analysis capabilities")

        print()
        print("📋 RECOMMENDED ACTIONS:")
        if recommendation == "plan_duckdb_migration":
            print("   1. Research DuckDB analytics migration strategy")
            print("   2. Plan hybrid SQLite+DuckDB architecture")
            print("   3. Identify analytical vs transactional queries")
        elif recommendation == "add_faiss_semantic":
            print("   1. Implement semantic search proof-of-concept")
            print("   2. Add Faiss vector search for document intelligence")
            print("   3. Evaluate user adoption of semantic features")
        else:
            print("   1. Apply advanced SQLite optimizations")
            print("   2. Monitor architecture health weekly")
            print("   3. Evaluate embedded database alternatives")

        print()
        print("🎯 Embedded Database Planning Options:")
        print("   • DuckDB for analytical performance (zero-config)")
        print("   • Faiss for semantic document intelligence")
        print("   • Kuzu for stakeholder network analysis")
        print("   • Maintain plug-and-play deployment philosophy")

    def _generate_monitoring_alert(self, assessment: Dict):
        """Generate monitoring alert"""
        readiness_score = assessment["migration_readiness_score"]

        print("👀 MONITORING: Some Migration Indicators Present")
        print("=" * 45)
        print(f"   Migration Readiness Score: {readiness_score:.2f}/1.00")
        print(f"   Recommendation: {assessment['migration_recommendation']}")
        print()
        print("📊 ClaudeDirector is showing early migration indicators.")
        print("   Monitor trends and prepare for potential future migration.")
        print()
        print("📋 MONITORING ACTIONS:")
        print("   1. Increase architecture health monitoring frequency")
        print("   2. Track performance trends over time")
        print("   3. Begin researching PostgreSQL options")
        print("   4. Optimize current SQLite performance")

    def _generate_healthy_status(self, assessment: Dict):
        """Generate healthy status message"""
        readiness_score = assessment["migration_readiness_score"]

        print("✅ HEALTHY: SQLite Performance Excellent")
        print("=" * 40)
        print(f"   Migration Readiness Score: {readiness_score:.2f}/1.00")
        print(f"   Recommendation: {assessment['migration_recommendation']}")
        print()
        print("🚀 ClaudeDirector's optimized SQLite is performing excellently.")
        print("   Continue with current architecture - no migration needed.")
        print()
        print("📊 Performance Status:")
        print("   • Query performance: Excellent")
        print("   • Database size: Within optimal range")
        print("   • Concurrency: No issues detected")
        print("   • Organizational scale: Well supported")

    def _show_trend_analysis(self):
        """Show migration readiness trend analysis"""
        try:
            trends = self.monitor.get_migration_trend_analysis()

            if trends.get("trend") == "insufficient_data":
                print("\n📈 Trend Analysis: Insufficient historical data")
                return

            print(f"\n📈 Migration Readiness Trends (90 days):")
            print(f"   Trend Direction: {trends['trend']}")
            print(f"   Current Score: {trends['current_score']:.2f}")
            print(f"   Score Change: {trends['score_change']:+.2f}")
            print(f"   Assessments: {trends['assessments_count']}")

            indicators = trends.get("trend_indicators", {})
            if indicators.get("improving"):
                print("   📉 Trend: Migration pressure decreasing")
            elif indicators.get("degrading"):
                print("   📈 Trend: Migration pressure increasing")
            else:
                print("   ➡️  Trend: Stable migration readiness")

        except Exception as e:
            print(f"\n📈 Trend Analysis: Failed to analyze trends ({e})")

    def _show_criteria_status(self, criteria_analysis: Dict):
        """Show specific criteria status"""
        if not criteria_analysis:
            return

        print("\n📊 Migration Criteria Status:")

        # Performance criteria
        if "performance" in criteria_analysis:
            perf = criteria_analysis["performance"]
            print(f"   Performance:")

            if "slow_queries" in perf:
                sq = perf["slow_queries"]
                status_icon = self._get_status_icon(sq["status"])
                print(
                    f"     {status_icon} Slow Queries: {sq['current']:.1f}% (threshold: {sq['warning_threshold']:.1f}%)"
                )

            if "avg_query_time" in perf:
                qt = perf["avg_query_time"]
                status_icon = self._get_status_icon(qt["status"])
                print(
                    f"     {status_icon} Avg Query Time: {qt['current']:.3f}s (threshold: {qt['warning_threshold']:.1f}s)"
                )

        # Scale criteria
        if "scale" in criteria_analysis:
            scale = criteria_analysis["scale"]
            print(f"   Scale:")

            if "database_size" in scale:
                ds = scale["database_size"]
                status_icon = self._get_status_icon(ds["status"])
                print(
                    f"     {status_icon} Database Size: {ds['current_mb']:.1f}MB (threshold: {ds['warning_threshold_gb']:.1f}GB)"
                )

            if "stakeholder_count" in scale:
                sc = scale["stakeholder_count"]
                status_icon = self._get_status_icon(sc["status"])
                print(
                    f"     {status_icon} Stakeholders: {sc['current']} (threshold: {sc['warning_threshold']})"
                )

        # Organizational criteria
        if "organizational" in criteria_analysis:
            org = criteria_analysis["organizational"]
            print(f"   Organizational:")

            if "user_count" in org:
                uc = org["user_count"]
                status_icon = self._get_status_icon(uc["status"])
                print(
                    f"     {status_icon} Estimated Users: {uc['current']} (threshold: {uc['warning_threshold']})"
                )

    def _show_action_items(self, action_items: List[Dict]):
        """Show action items from assessment"""
        print("\n📋 Recommended Actions:")

        for item in action_items[:5]:  # Show top 5 actions
            priority_icon = {
                "critical": "🚨",
                "high": "⚠️",
                "medium": "📋",
                "low": "💡",
            }.get(item.get("priority", "medium"), "📋")

            print(f"   {priority_icon} {item.get('action', 'Unknown action')}")
            print(f"      {item.get('description', '')}")
            print(f"      Timeline: {item.get('timeline', 'Not specified')}")

    def _get_status_icon(self, status: str) -> str:
        """Get status icon for criteria"""
        icons = {"healthy": "✅", "warning": "⚠️", "critical": "🚨"}
        return icons.get(status, "❓")


def main():
    """Main entry point for daily architecture alerts"""
    try:
        alert_system = DailyArchitectureAlerts()
        success = alert_system.generate_daily_alerts()

        if success:
            print("\n✅ Architecture health alert completed")
        else:
            print("\n❌ Architecture health alert failed")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Daily architecture alert system failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
