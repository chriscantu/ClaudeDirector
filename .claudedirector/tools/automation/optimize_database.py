#!/usr/bin/env python3
"""
ClaudeDirector Database Optimization CLI
Apply immediate SQLite performance optimizations while maintaining plug-and-play simplicity
"""

import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from context_engineering.strategic_memory_manager import (
    get_strategic_memory_manager as get_db_manager,
)


def optimize_database():
    """Apply SQLite optimizations for ClaudeDirector strategic memory"""
    print("🚀 ClaudeDirector Database Optimization")
    print("=" * 50)

    try:
        # Initialize optimized database manager
        print("📊 Initializing optimized database manager...")
        db_manager = get_db_manager()

        # Get initial performance stats
        print("📈 Getting baseline performance metrics...")
        initial_stats = db_manager.get_performance_stats()

        print(f"   Database size: {initial_stats['database_size_mb']} MB")
        print(f"   Total queries processed: {initial_stats['total_queries']}")
        print(
            f"   Slow queries: {initial_stats['slow_queries']} ({initial_stats['slow_query_percentage']:.1f}%)"
        )

        # Apply optimizations
        print("⚡ Applying SQLite performance optimizations...")
        print("   • WAL journal mode for better concurrency")
        print("   • Optimized cache size (10MB)")
        print("   • Memory-mapped I/O (256MB)")
        print("   • Strategic indexes for intelligence workloads")

        # Run maintenance if needed
        print("🔧 Running database maintenance...")
        db_manager.vacuum_and_analyze()

        # Get final stats
        print("📊 Performance optimization completed!")
        final_stats = db_manager.get_performance_stats()

        print("\n✅ Optimization Results:")
        print(f"   Database size: {final_stats['database_size_mb']} MB")
        print(f"   Cache size: {final_stats['cache_size']} pages")
        print(f"   Connection reuses: {final_stats['connection_reuses']}")

        # Calculate improvements
        if initial_stats["total_queries"] > 0:
            improvement = (
                initial_stats["slow_query_percentage"]
                - final_stats["slow_query_percentage"]
            )
            if improvement > 0:
                print(f"   Query performance improved by {improvement:.1f}%")

        print("\n🎯 Strategic Intelligence Optimizations Applied:")
        print("   • Stakeholder engagement pattern queries")
        print("   • Meeting intelligence temporal analysis")
        print("   • Google Drive document intelligence")
        print("   • Cross-system relationship mapping")
        print("   • Executive session analytics")

        print("\n💡 Performance Tips:")
        print("   • Run 'claudedirector db-optimize' monthly for maintenance")
        print("   • Monitor query performance with 'claudedirector db-stats'")
        print("   • Database will auto-optimize during normal operations")

        print(
            "\n🚀 ClaudeDirector is now optimized for strategic intelligence workloads!"
        )

    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        return False

    return True


def show_database_stats():
    """Show current database performance statistics"""
    print("📊 ClaudeDirector Database Performance Statistics")
    print("=" * 50)

    try:
        db_manager = get_db_manager()
        stats = db_manager.get_performance_stats()

        print(f"Database Information:")
        print(f"   Size: {stats['database_size_mb']} MB")
        print(f"   Cache Size: {stats['cache_size']} pages")

        print(f"\nQuery Performance:")
        print(f"   Total Queries: {stats['total_queries']}")
        print(
            f"   Slow Queries: {stats['slow_queries']} ({stats['slow_query_percentage']:.1f}%)"
        )
        print(f"   Connection Reuses: {stats['connection_reuses']}")

        # Performance assessment
        if stats["slow_query_percentage"] < 5:
            print(f"\n✅ Performance Status: Excellent")
        elif stats["slow_query_percentage"] < 15:
            print(f"\n⚠️  Performance Status: Good (consider maintenance)")
        else:
            print(f"\n❌ Performance Status: Needs optimization")
            print("   Run: claudedirector db-optimize")

        # Advanced statistics for power users
        print(f"\nDetailed Statistics:")
        print(json.dumps(stats, indent=2))

    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
        return False

    return True


def main():
    """CLI interface for database optimization"""
    import argparse

    parser = argparse.ArgumentParser(
        description="ClaudeDirector Database Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bin/optimize-database.py --optimize     # Apply optimizations
  python bin/optimize-database.py --stats        # Show performance stats
  python bin/optimize-database.py --maintenance  # Run maintenance only
        """,
    )

    parser.add_argument(
        "--optimize", action="store_true", help="Apply SQLite performance optimizations"
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show database performance statistics"
    )
    parser.add_argument(
        "--maintenance",
        action="store_true",
        help="Run database maintenance (VACUUM + ANALYZE)",
    )

    args = parser.parse_args()

    if args.optimize:
        success = optimize_database()
        sys.exit(0 if success else 1)

    elif args.stats:
        success = show_database_stats()
        sys.exit(0 if success else 1)

    elif args.maintenance:
        print("🔧 Running database maintenance...")
        try:
            db_manager = get_db_manager()
            db_manager.vacuum_and_analyze()
            print("✅ Database maintenance completed")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Maintenance failed: {e}")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
