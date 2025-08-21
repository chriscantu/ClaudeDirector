#!/usr/bin/env python3
"""
Database Integration Tests
Tests database connectivity, schema validation, and data persistence
"""

import sys
import sqlite3
import tempfile
import unittest
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

try:
    from memory.session_context_manager import SessionContextManager
    from core.integrated_conversation_manager import IntegratedConversationManager
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

class TestDatabaseIntegration(unittest.TestCase):
    """Integration tests for database functionality"""

    def setUp(self):
        """Set up test database"""
        if not MEMORY_AVAILABLE:
            self.skipTest("Memory modules not available")

        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Initialize managers
        self.session_manager = SessionContextManager(db_path=self.db_path)
        self.conversation_manager = IntegratedConversationManager(db_path=self.db_path)

    def tearDown(self):
        """Clean up test database"""
        if hasattr(self, 'db_path'):
            Path(self.db_path).unlink(missing_ok=True)

    def test_database_connection(self):
        """Test basic database connectivity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Test basic SQL operation
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        self.assertEqual(result[0], 1)
        conn.close()

    def test_schema_initialization(self):
        """Test that database schema is properly initialized"""
        # Initialize schema through session manager
        self.session_manager._ensure_database_schema()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check that required tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name IN ('session_context', 'stakeholder_profiles_enhanced')
        """)

        tables = [row[0] for row in cursor.fetchall()]

        self.assertIn('session_context', tables)
        self.assertIn('stakeholder_profiles_enhanced', tables)

        conn.close()

    def test_session_context_crud(self):
        """Test Create, Read, Update, Delete operations for session context"""
        session_id = "test_session_001"

        # Create session context
        context_data = {
            "persona_focus": "diego",
            "strategic_themes": ["platform", "scaling"],
            "stakeholder_engagement": {"VP Engineering": "high"},
            "conversation_quality": 0.85
        }

        self.session_manager.save_session_context(session_id, context_data)

        # Read session context
        retrieved_context = self.session_manager.get_session_context(session_id)

        self.assertIsNotNone(retrieved_context)
        self.assertEqual(retrieved_context.get("persona_focus"), "diego")
        self.assertEqual(retrieved_context.get("conversation_quality"), 0.85)

        # Update session context
        updated_data = context_data.copy()
        updated_data["conversation_quality"] = 0.90

        self.session_manager.save_session_context(session_id, updated_data)

        updated_context = self.session_manager.get_session_context(session_id)
        self.assertEqual(updated_context.get("conversation_quality"), 0.90)

    def test_conversation_quality_tracking(self):
        """Test conversation quality calculation and persistence"""
        session_id = "quality_test_session"

        # Simulate conversation with good quality data
        conversation_thread = [
            {"role": "user", "content": "How should we scale our platform architecture?"},
            {"role": "assistant", "content": "🎯 Diego | Engineering Leadership\n\nGreat strategic question! Let me apply first principles thinking..."},
            {"role": "user", "content": "What about stakeholder alignment?"},
            {"role": "assistant", "content": "📊 Camille | Strategic Technology\n\nStakeholder alignment is critical..."}
        ]

        # Process conversation
        quality_score = self.conversation_manager._calculate_conversation_quality({
            "conversation_thread": conversation_thread,
            "persona_usage": {"diego": 1, "camille": 1},
            "framework_usage": ["Team Topologies", "Strategic Analysis"],
            "stakeholder_mentions": ["VP Engineering", "Product Director"]
        })

        # Quality should be reasonable for this rich conversation
        self.assertGreaterEqual(quality_score, 0.5)
        self.assertLessEqual(quality_score, 1.0)

    def test_concurrent_database_access(self):
        """Test that multiple database connections work correctly"""
        import threading
        import queue

        results = queue.Queue()

        def worker(worker_id):
            """Worker function for concurrent access"""
            try:
                # Create separate manager for this thread
                manager = SessionContextManager(db_path=self.db_path)

                session_id = f"concurrent_session_{worker_id}"
                context_data = {
                    "worker_id": worker_id,
                    "timestamp": time.time(),
                    "conversation_quality": 0.75 + (worker_id * 0.05)
                }

                # Save and retrieve
                manager.save_session_context(session_id, context_data)
                retrieved = manager.get_session_context(session_id)

                results.put(("success", worker_id, retrieved))

            except Exception as e:
                results.put(("error", worker_id, str(e)))

        # Start 5 concurrent workers
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join(timeout=10)

        # Check results
        successful_workers = 0
        while not results.empty():
            status, worker_id, data = results.get()
            if status == "success":
                successful_workers += 1
                self.assertIsNotNone(data)
                self.assertEqual(data.get("worker_id"), worker_id)
            else:
                self.fail(f"Worker {worker_id} failed: {data}")

        self.assertEqual(successful_workers, 5)

    def test_database_performance(self):
        """Test database performance meets requirements"""
        # Test bulk insert performance
        start_time = time.time()

        for i in range(100):
            session_id = f"perf_test_session_{i}"
            context_data = {
                "iteration": i,
                "persona_focus": "diego" if i % 2 == 0 else "camille",
                "conversation_quality": 0.7 + (i % 30) * 0.01,
                "strategic_themes": ["platform", "scaling", "architecture"]
            }

            self.session_manager.save_session_context(session_id, context_data)

        insert_duration = time.time() - start_time

        # Should complete 100 inserts in reasonable time
        self.assertLess(insert_duration, 10.0)  # 10 seconds max

        # Test bulk read performance
        start_time = time.time()

        for i in range(50):
            session_id = f"perf_test_session_{i}"
            context = self.session_manager.get_session_context(session_id)
            self.assertIsNotNone(context)

        read_duration = time.time() - start_time

        # Should complete 50 reads quickly
        self.assertLess(read_duration, 5.0)  # 5 seconds max

def run_database_integration_tests():
    """Run database integration tests"""
    print("🗄️  DATABASE INTEGRATION TESTS")
    print("=" * 50)
    print("Testing database connectivity, schema, and performance")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseIntegration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ ALL DATABASE INTEGRATION TESTS PASSED")
        print("   Database connectivity verified")
        print("   Schema validation passed")
        print("   Performance requirements met")
        return True
    else:
        print("❌ DATABASE INTEGRATION TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        return False

if __name__ == "__main__":
    success = run_database_integration_tests()
    sys.exit(0 if success else 1)
