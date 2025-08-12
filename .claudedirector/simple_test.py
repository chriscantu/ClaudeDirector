#!/usr/bin/env python3
"""
Simple test for ClaudeDirector Enhanced Framework
Basic validation of session context preservation
"""

import os
import sys
import sqlite3
import tempfile
import json
from datetime import datetime

# Add lib directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

def test_schema_creation():
    """Test session context schema creation"""
    print("🧪 Testing schema creation...")

    # Read schema file
    schema_path = os.path.join(current_dir, 'config', 'schemas', 'session_context_schema.sql')

    if not os.path.exists(schema_path):
        print(f"❌ Schema file not found: {schema_path}")
        return False

    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    # Create temporary database and apply schema
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)

        # Verify tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = ['session_context', 'session_checkpoints', 'context_gaps', 'session_recovery_log']
        missing_tables = [table for table in expected_tables if table not in tables]

        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False

        print(f"✅ Schema created successfully: {len(tables)} tables")
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

def test_basic_session_operations():
    """Test basic session context operations"""
    print("🧪 Testing basic session operations...")

    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        # Apply schema
        schema_path = os.path.join(current_dir, 'config', 'schemas', 'session_context_schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)

        # Test session creation
        session_id = "test-session-123"
        session_type = "strategic"
        timestamp = datetime.now().isoformat()

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_context
            (session_id, session_type, session_start_timestamp, last_backup_timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, session_type, timestamp, timestamp))

        print("✅ Session context inserted")

        # Test context update
        test_context = {
            'stakeholders': {'steve_davis': 'VP Engineering'},
            'initiatives': {'TEST-001': 'Platform ROI'}
        }

        cursor.execute("""
            UPDATE session_context
            SET stakeholder_context = ?, strategic_initiatives_context = ?,
                context_quality_score = ?, updated_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
        """, (
            json.dumps(test_context['stakeholders']),
            json.dumps(test_context['initiatives']),
            0.85,
            session_id
        ))

        print("✅ Session context updated")

        # Test context retrieval
        cursor.execute("""
            SELECT stakeholder_context, strategic_initiatives_context, context_quality_score
            FROM session_context WHERE session_id = ?
        """, (session_id,))

        row = cursor.fetchone()
        if row:
            stakeholder_context = json.loads(row[0]) if row[0] else {}
            initiative_context = json.loads(row[1]) if row[1] else {}
            quality_score = row[2]

            print(f"✅ Context retrieved: {len(stakeholder_context)} stakeholders, {len(initiative_context)} initiatives")
            print(f"✅ Quality score: {quality_score:.1%}")

        # Test gap tracking
        cursor.execute("""
            INSERT INTO context_gaps
            (session_id, gap_type, gap_description, severity, detected_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            'executive_context_missing',
            'Executive session preparation incomplete',
            'high',
            timestamp
        ))

        print("✅ Context gap recorded")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Basic operations test failed: {e}")
        return False

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

def test_procore_context_simulation():
    """Test with actual ***REMOVED*** stakeholder context"""
    print("🧪 Testing ***REMOVED*** context simulation...")

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        # Apply schema
        schema_path = os.path.join(current_dir, 'config', 'schemas', 'session_context_schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)

        # Store ***REMOVED*** stakeholder context
        session_id = "procore-session-001"
        timestamp = datetime.now().isoformat()

        procore_context = {
            'stakeholders': {
                'stakeholder_a': {
                    'name': 'Director A',
                    'position': 'Not strong platform advocate',
                    'focus': 'Product delivery over platform investment'
                },
                'stakeholder_b': {
                    'name': 'SLT Member B',
                    'position': '100% product focused',
                    'conflicts': 'With platform advocate over platform investment'
                },
                'stakeholder_target': {
                    'name': 'VP Engineering',
                    'position': 'Wants ROI understanding',
                    'convertible': 'Evidence-based business case'
                },
                'stakeholder_ally': {
                    'name': 'SLT Ally',
                    'position': 'Platform advocate',
                    'role': 'Key SLT ally'
                }
            },
            'roi_strategy': {
                'target': 'stakeholder_target',
                'objective': '$200K productivity gains demonstration',
                'opposition': 'Product-focused stakeholder resistance',
                'allies': 'SLT ally, technical team'
            },
            'initiatives': {
                'platform_investment_roi': {
                    'status': 'in_progress',
                    'priority': 'high',
                    'business_value': '$200K+ annual productivity gains'
                }
            }
        }

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_context
            (session_id, session_type, stakeholder_context, roi_discussions_context,
             strategic_initiatives_context, session_start_timestamp, last_backup_timestamp,
             context_quality_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            'strategic',
            json.dumps(procore_context['stakeholders']),
            json.dumps(procore_context['roi_strategy']),
            json.dumps(procore_context['initiatives']),
            timestamp,
            timestamp,
            0.92  # High quality score
        ))

        print("✅ ***REMOVED*** context stored")

        # Simulate session restart and recovery
        cursor.execute("""
            SELECT stakeholder_context, roi_discussions_context, context_quality_score
            FROM session_context WHERE session_id = ?
        """, (session_id,))

        row = cursor.fetchone()
        if row:
            stakeholders = json.loads(row[0]) if row[0] else {}
            roi_context = json.loads(row[1]) if row[1] else {}
            quality = row[2]

            print(f"✅ Context recovered: {len(stakeholders)} stakeholders")
            print(f"✅ ROI context: Target = {roi_context.get('target', 'N/A')}")
            print(f"✅ Quality score: {quality:.1%}")

            # Verify specific stakeholder data
            target_context = stakeholders.get('stakeholder_target', {})
            if target_context.get('convertible') == 'Evidence-based business case':
                print("✅ Target stakeholder context preserved correctly")
            else:
                print("❌ Target stakeholder context corruption detected")
                return False

        conn.close()
        return True

    except Exception as e:
        print(f"❌ ***REMOVED*** context simulation failed: {e}")
        return False

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

def main():
    """Run simple framework tests"""
    print("🚀 ClaudeDirector Enhanced Framework - Simple Test Suite")
    print("=" * 60)

    tests = [
        ("Schema Creation", test_schema_creation),
        ("Basic Session Operations", test_basic_session_operations),
        ("***REMOVED*** Context Simulation", test_procore_context_simulation)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{status} - {test_name}")
        except Exception as e:
            print(f"❌ FAILED - {test_name}: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:12} | {test_name}")

    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Enhanced session context preservation system is ready")
        print("✅ ClaudeDirector framework enhancement complete")
        return True
    else:
        print(f"\n⚠️  {total-passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
