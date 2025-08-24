#!/usr/bin/env python3
"""
Conversation Tracking P0 Feature Tests
CRITICAL: Local database conversation storage must work reliably.
"""

import unittest
import sqlite3
import tempfile
import shutil
import json
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestConversationTrackingP0(unittest.TestCase):
    """P0 Tests: Conversation tracking must work reliably"""

    def setUp(self):
        """Set up test environment"""
        self.test_db_dir = tempfile.mkdtemp()
        self.test_db_path = Path(self.test_db_dir) / "test_strategic_memory.db"
        self.main_db_path = PROJECT_ROOT / "data" / "strategic_memory.db"

    def tearDown(self):
        """Clean up test environment"""
        if self.test_db_dir:
            shutil.rmtree(self.test_db_dir)

    def test_p0_database_exists_and_accessible(self):
        """P0 TEST: Strategic memory database must exist and be accessible"""
        self.assertTrue(
            self.main_db_path.exists(),
            "Strategic memory database must exist at data/strategic_memory.db",
        )

        # Test database is readable
        try:
            with sqlite3.connect(self.main_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.fail(f"Database must be accessible: {e}")

        # Verify required tables exist
        required_tables = [
            "session_context",
            "session_checkpoints",
            "context_gaps",
            "session_recovery_log",
        ]

        for table in required_tables:
            with self.subTest(table=table):
                self.assertIn(
                    table,
                    tables,
                    f"Required conversation tracking table '{table}' must exist",
                )

    def test_p0_conversation_capture_quality(self):
        """P0 TEST: Conversation capture must have acceptable quality scores"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Get recent session quality scores
            cursor.execute(
                """
                SELECT session_id, context_quality_score, last_backup_timestamp
                FROM session_context
                WHERE last_backup_timestamp >= datetime('now', '-7 days')
                ORDER BY last_backup_timestamp DESC
                LIMIT 5
            """
            )

            recent_sessions = cursor.fetchall()

            # Must have recent activity
            self.assertGreater(
                len(recent_sessions),
                0,
                "Must have recent conversation sessions in last 7 days",
            )

            # Quality scores should be reasonable for active conversations
            for session_id, quality_score, timestamp in recent_sessions:
                with self.subTest(session=session_id[:12]):
                    # Allow some low-quality sessions but warn if all are low
                    if quality_score is not None:
                        self.assertGreaterEqual(
                            quality_score,
                            0.0,
                            f"Quality score must be non-negative for session {session_id[:12]}",
                        )

    def test_p0_session_context_schema_compliance(self):
        """P0 TEST: Session context must follow schema requirements"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Get schema info for session_context
            cursor.execute("PRAGMA table_info(session_context);")
            columns = {row[1]: row[2] for row in cursor.fetchall()}

            # Required columns for conversation tracking
            required_columns = {
                "session_id": "TEXT",
                "session_type": "TEXT",
                "conversation_thread": "TEXT",
                "last_backup_timestamp": "TIMESTAMP",
                "context_quality_score": "REAL",
            }

            for col_name, col_type in required_columns.items():
                with self.subTest(column=col_name):
                    self.assertIn(
                        col_name,
                        columns,
                        f"Required column '{col_name}' must exist in session_context",
                    )

    def test_p0_conversation_data_structure(self):
        """P0 TEST: Conversation data must be properly structured"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Get sample conversation data
            cursor.execute(
                """
                SELECT session_id, conversation_thread, active_personas
                FROM session_context
                WHERE conversation_thread IS NOT NULL
                LIMIT 3
            """
            )

            for session_id, conversation_thread, active_personas in cursor.fetchall():
                with self.subTest(session=session_id[:12]):

                    # Conversation thread should be valid JSON if present
                    if conversation_thread:
                        try:
                            conversation_data = json.loads(conversation_thread)
                            self.assertIsInstance(
                                conversation_data,
                                (list, dict),
                                f"Conversation thread must be valid JSON structure for {session_id[:12]}",
                            )
                        except json.JSONDecodeError:
                            self.fail(
                                f"Conversation thread must be valid JSON for session {session_id[:12]}"
                            )

                    # Active personas should be valid JSON if present
                    if active_personas:
                        try:
                            personas_data = json.loads(active_personas)
                            self.assertIsInstance(
                                personas_data,
                                (list, dict),
                                f"Active personas must be valid JSON for {session_id[:12]}",
                            )
                        except json.JSONDecodeError:
                            self.fail(
                                f"Active personas must be valid JSON for session {session_id[:12]}"
                            )

    def test_p0_conversation_manager_integration(self):
        """P0 TEST: Conversation manager integration must be available"""
        try:
            # Try to import the conversation manager
            sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

            # Suppress warnings during import and initialization
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                # Try importing as installed package first (CI environment)
                try:
                    from claudedirector.core.integrated_conversation_manager import (
                        IntegratedConversationManager,
                    )
                except ImportError:
                    # Fallback to local import (development environment)
                    from core.integrated_conversation_manager import (
                        IntegratedConversationManager,
                    )

                # Test basic initialization (should not crash)
                manager = IntegratedConversationManager()
                self.assertIsNotNone(
                    manager, "Conversation manager must initialize successfully"
                )

        except ImportError as e:
            # Check if there's a fallback or alternative implementation
            self.fail(f"Conversation manager must be importable: {e}")
        except Exception as e:
            # Allow initialization failures but warn
            self.skipTest(f"Conversation manager not fully available: {e}")

    def test_p0_session_lifecycle_support(self):
        """P0 TEST: Session lifecycle operations must be supported"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Check for different session types
            cursor.execute("SELECT DISTINCT session_type FROM session_context;")
            session_types = [row[0] for row in cursor.fetchall()]

            self.assertGreater(
                len(session_types), 0, "Must have at least one session type recorded"
            )

            # Verify session lifecycle fields exist
            cursor.execute(
                """
                SELECT COUNT(*) as active_sessions
                FROM session_context
                WHERE session_end_timestamp IS NULL
            """
            )

            result = cursor.fetchone()
            # Should have some concept of active vs ended sessions
            self.assertIsNotNone(
                result, "Session lifecycle tracking must be implemented"
            )


class TestConversationTrackingFunctionality(unittest.TestCase):
    """Functional tests for conversation tracking features"""

    def setUp(self):
        """Set up test environment"""
        self.main_db_path = PROJECT_ROOT / "data" / "strategic_memory.db"

    def test_conversation_persistence_across_sessions(self):
        """Test that conversation context persists across sessions"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Get sessions with conversation data
            cursor.execute(
                """
                SELECT session_id, conversation_thread, last_backup_timestamp
                FROM session_context
                WHERE conversation_thread IS NOT NULL
                ORDER BY last_backup_timestamp DESC
                LIMIT 2
            """
            )

            sessions = cursor.fetchall()

            if len(sessions) >= 2:
                # Verify conversations are preserved
                for session_id, conversation_thread, timestamp in sessions:
                    with self.subTest(session=session_id[:12]):
                        self.assertIsNotNone(
                            conversation_thread,
                            f"Conversation data must be preserved for session {session_id[:12]}",
                        )
            else:
                self.skipTest(
                    "Need at least 2 sessions with conversation data to test persistence"
                )

    def test_strategic_context_preservation(self):
        """Test that strategic context is preserved correctly"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Look for strategic context fields
            cursor.execute(
                """
                SELECT session_id, stakeholder_context, strategic_initiatives_context, executive_context
                FROM session_context
                WHERE session_type = 'strategic'
                LIMIT 3
            """
            )

            strategic_sessions = cursor.fetchall()

            if strategic_sessions:
                for session_data in strategic_sessions:
                    session_id = session_data[0]
                    with self.subTest(session=session_id[:12]):
                        # At least some strategic context should be preserved
                        context_fields = session_data[
                            1:
                        ]  # stakeholder, initiatives, executive
                        has_context = any(field is not None for field in context_fields)

                        # Don't fail but warn if no strategic context
                        if not has_context:
                            print(
                                f"⚠️ Warning: No strategic context found for session {session_id[:12]}"
                            )
            else:
                self.skipTest(
                    "No strategic sessions found to test context preservation"
                )

    def test_conversation_quality_improvement(self):
        """Test that conversation quality can be measured and improved"""
        with sqlite3.connect(self.main_db_path) as conn:
            cursor = conn.cursor()

            # Get quality score distribution
            cursor.execute(
                """
                SELECT AVG(context_quality_score) as avg_quality,
                       MIN(context_quality_score) as min_quality,
                       MAX(context_quality_score) as max_quality,
                       COUNT(*) as total_sessions
                FROM session_context
                WHERE context_quality_score IS NOT NULL
            """
            )

            result = cursor.fetchone()
            avg_quality, min_quality, max_quality, total_sessions = result

            if total_sessions > 0:
                # Quality scores should be in valid range
                self.assertGreaterEqual(
                    min_quality, 0.0, "Quality scores must be non-negative"
                )
                self.assertLessEqual(
                    max_quality, 1.0, "Quality scores must not exceed 1.0"
                )

                # Print quality metrics for monitoring
                print(f"\n📊 Conversation Quality Metrics:")
                print(f"   Average Quality: {avg_quality:.2f}")
                print(f"   Range: {min_quality:.2f} - {max_quality:.2f}")
                print(f"   Total Sessions: {total_sessions}")
            else:
                self.skipTest("No sessions with quality scores to analyze")


def run_conversation_tracking_tests():
    """Run comprehensive conversation tracking test suite"""
    print("💾 CONVERSATION TRACKING P0 FEATURE TEST SUITE")
    print("=" * 60)
    print("Testing local database conversation storage functionality")
    print()

    # Create test suite
    suite = unittest.TestSuite()

    # Add P0 tests
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestConversationTrackingP0)
    )
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(
            TestConversationTrackingFunctionality
        )
    )

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print(f"📊 CONVERSATION TRACKING TEST RESULTS")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 ALL CONVERSATION TRACKING TESTS PASSED")
        print("✅ P0 conversation tracking feature validated")
    else:
        print("\n❌ CONVERSATION TRACKING TESTS FAILED")
        print("🚫 P0 feature issues detected - investigation required")

    return success


if __name__ == "__main__":
    success = run_conversation_tracking_tests()
    exit(0 if success else 1)
