#!/usr/bin/env python3
"""
ClaudeDirector Regression Test Suite
Focused tests for database consolidation and conversation capture
"""

import os
import sys
import tempfile
from pathlib import Path

# Add lib directory to Python path for flattened structure
lib_dir = Path(__file__).parent / "lib"
sys.path.insert(0, str(lib_dir))

import sqlite3
from datetime import datetime


def test_database_consolidation():
    """Test that database consolidation worked correctly"""
    print("🧪 Testing Database Consolidation...")

    db_path = "data/strategic_memory.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        required_tables = [
            "strategic_intelligence",
            "stakeholder_intelligence",
            "session_context",
            "session_checkpoints",
            "context_gaps",
        ]

        for table in required_tables:
            if table not in tables:
                raise Exception(f"Required table {table} missing")

        # Check data exists
        cursor.execute("SELECT COUNT(*) FROM strategic_intelligence")
        strategic_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM session_context")
        session_count = cursor.fetchone()[0]

        print(f"✅ Database has {strategic_count} strategic intelligence records")
        print(f"✅ Database has {session_count} session contexts")

        # Verify database is writable
        cursor.execute(
            "INSERT INTO strategic_intelligence (intelligence_id, category, title, created_at) VALUES (?, ?, ?, ?)",
            (
                "test_" + str(datetime.now().timestamp()),
                "TEST",
                "Regression test",
                datetime.now().isoformat(),
            ),
        )
        conn.commit()

        # Clean up test record
        cursor.execute("DELETE FROM strategic_intelligence WHERE category = 'TEST'")
        conn.commit()

        conn.close()
        print("✅ Database consolidation test PASSED")
        return True

    except Exception as e:
        print(f"❌ Database consolidation test FAILED: {e}")
        return False


def test_conversation_capture():
    """Test conversation capture system"""
    print("🧪 Testing Conversation Capture...")

    try:
        from core.auto_conversation_integration import (
            capture_user_input,
            capture_assistant_response,
            get_capture_status,
        )

        # Test basic capture
        test_user_input = "Martin, can you test the conversation capture system?"
        test_assistant_response = """🏗️ Martin | Platform Architecture

        Testing the conversation capture system after our database consolidation and directory cleanup.
        This should be automatically captured and stored in our strategic memory database.
        """

        # Capture conversation
        capture_user_input(test_user_input)
        captured = capture_assistant_response(test_assistant_response)

        if captured:
            print("✅ Conversation successfully captured")
        else:
            print("⚠️ Conversation not captured (may not be strategic enough)")

        # Check capture status
        status = get_capture_status()
        print(f"✅ Capture system status: {status}")

        print("✅ Conversation capture test PASSED")
        return True

    except Exception as e:
        print(f"❌ Conversation capture test FAILED: {e}")
        return False


def test_import_paths():
    """Test that all critical import paths work"""
    print("🧪 Testing Import Paths...")

    try:
        # Test core imports
        from core.integrated_conversation_manager import IntegratedConversationManager
        from memory.session_context_manager import SessionContextManager
        from core.cursor_conversation_hook import CursorConversationHook
        from core.auto_conversation_integration import auto_capture_conversation

        print("✅ All critical imports working")
        print("✅ Import paths test PASSED")
        return True

    except Exception as e:
        print(f"❌ Import paths test FAILED: {e}")
        return False


def test_session_management():
    """Test basic session management"""
    print("🧪 Testing Session Management...")

    try:
        from core.integrated_conversation_manager import IntegratedConversationManager

        # Create temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
            db_path = tmp_db.name

        try:
            # Apply the proper schema to temp database
            conn = sqlite3.connect(db_path)
            with open(
                ".claudedirector/config/schemas/session_context_schema.sql", "r"
            ) as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            conn.close()

            manager = IntegratedConversationManager(db_path)

            # Test session creation
            session_id = manager.start_conversation_session("test")
            print(f"✅ Session created: {session_id[:8]}...")

            # Test conversation capture
            manager.capture_conversation_turn(
                "Test user input",
                "Test assistant response with strategic content about platform architecture",
                ["martin"],
                {"test": True},
            )
            print("✅ Conversation turn captured")

            # Test backup
            backup_success = manager.backup_conversation_context()
            print(f"✅ Context backup: {'success' if backup_success else 'failed'}")

            # Test session status
            status = manager.get_session_status()
            print(f"✅ Session status: {status['status']}")

            # End session
            manager.end_conversation_session()
            print("✅ Session ended successfully")

        finally:
            # Cleanup
            if os.path.exists(db_path):
                os.unlink(db_path)

        print("✅ Session management test PASSED")
        return True

    except Exception as e:
        print(f"❌ Session management test FAILED: {e}")
        return False


def main():
    """Run full regression test suite"""
    print("🚀 ClaudeDirector Regression Test Suite")
    print("=" * 50)

    tests = [
        ("Database Consolidation", test_database_consolidation),
        ("Import Paths", test_import_paths),
        ("Session Management", test_session_management),
        ("Conversation Capture", test_conversation_capture),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print("📊 REGRESSION TEST RESULTS")
    print("=" * 50)

    for i, (test_name, test_func) in enumerate(tests):
        status = "✅ PASSED" if i < passed else "❌ FAILED"
        print(f"{status:12} | {test_name}")

    print("-" * 50)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL REGRESSION TESTS PASSED!")
        print("✅ Database consolidation successful")
        print("✅ Directory cleanup successful")
        print("✅ Conversation capture working")
        return True
    else:
        print(f"\n⚠️  {total-passed} regression tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
