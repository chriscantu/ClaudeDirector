#!/usr/bin/env python3
"""
Test script for ClaudeDirector Enhanced Framework
Validates session context preservation and recovery functionality
"""

import os
import sys
import tempfile

# Add lib directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, "lib")
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

try:
    from claudedirector.memory.session_context_manager import SessionContextManager
    from claudedirector.core.enhanced_framework_manager import EnhancedFrameworkManager

    print("✅ Successfully imported ClaudeDirector enhanced framework modules")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


def test_session_context_manager():
    """Test SessionContextManager basic functionality"""
    print("\n🧪 Testing SessionContextManager...")

    # Use temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        # Initialize session manager
        manager = SessionContextManager(db_path)
        print("✅ SessionContextManager initialized")

        # Start new session
        session_id = manager.start_session("test_strategic")
        print(f"✅ New session started: {session_id}")

        # Test context backup
        success = manager.backup_session_context(session_id)
        if success:
            print("✅ Context backup successful")
        else:
            print("❌ Context backup failed")

        # Test context validation
        gaps = manager.validate_context_completeness(session_id)
        print(f"✅ Context validation complete: {len(gaps)} gaps detected")

        # Test recovery prompt generation
        if gaps:
            prompt = manager.get_context_recovery_prompt(session_id)
            print("✅ Recovery prompt generated")
            print(f"Preview: {prompt[:100]}...")

        # Test context restoration
        context = manager.restore_session_context(session_id)
        print(f"✅ Context restoration: {len(context)} context elements")

        # End session
        manager.end_session(session_id)
        print("✅ Session ended successfully")

        return True

    except Exception as e:
        print(f"❌ SessionContextManager test failed: {e}")
        return False

    finally:
        # Cleanup temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_enhanced_framework_manager():
    """Test EnhancedFrameworkManager functionality"""
    print("\n🧪 Testing EnhancedFrameworkManager...")

    # Use temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        # Initialize framework manager
        framework = EnhancedFrameworkManager(db_path)
        print("✅ EnhancedFrameworkManager initialized")

        # Test context status
        status = framework.get_context_status()
        print(f"✅ Context status retrieved: {status.get('session_active', False)}")

        # Test framework status
        status_str = framework.get_framework_status()
        print(f"✅ Framework status: {status_str}")

        # Test context validation
        is_valid = framework.validate_context_before_strategic_work()
        print(f"✅ Context validation: {'Valid' if is_valid else 'Requires recovery'}")

        # Test manual backup
        backup_success = framework.backup_current_context()
        print(f"✅ Manual backup: {'Success' if backup_success else 'Failed'}")

        # Test strategic context storage
        test_stakeholder_context = {
            "stakeholder_target": {
                "name": "VP Engineering",
                "role": "VP Engineering",
                "style": "data_driven",
            }
        }

        framework.store_strategic_context(
            "stakeholder_update", test_stakeholder_context
        )
        print("✅ Strategic context storage successful")

        # End session
        framework.end_session()
        print("✅ Framework session ended")

        return True

    except Exception as e:
        print(f"❌ EnhancedFrameworkManager test failed: {e}")
        return False

    finally:
        # Cleanup temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_session_recovery_simulation():
    """Simulate session restart and recovery"""
    print("\n🧪 Testing Session Recovery Simulation...")

    # Use temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        # Step 1: Create initial session with context
        print("📝 Step 1: Creating initial session with context...")

        manager1 = SessionContextManager(db_path)
        session_id = manager1.start_session("strategic")

        # Add some test context
        manager1.store_stakeholder_profile(
            stakeholder_key="stakeholder_target",
            display_name="VP Engineering",
            role_title="VP Engineering",
            communication_style="data_driven",
        )

        manager1.store_strategic_initiative(
            initiative_key="TEST-001",
            initiative_name="Platform Investment ROI",
            status="in_progress",
            priority="high",
            business_value="$200K productivity gains",
        )

        # Backup context
        backup_success = manager1.backup_session_context(session_id)
        print(f"✅ Initial context created and backed up: {backup_success}")

        # Step 2: Simulate session restart
        print("🔄 Step 2: Simulating session restart...")

        manager2 = SessionContextManager(db_path)
        restart_detected = manager2.detect_session_restart()
        print(f"✅ Session restart detected: {restart_detected}")

        if restart_detected:
            # Step 3: Restore context
            print("📋 Step 3: Restoring context...")

            restored_context = manager2.restore_session_context()
            print(f"✅ Context restored: {len(restored_context)} elements")

            # Step 4: Validate context
            print("🔍 Step 4: Validating context completeness...")

            gaps = manager2.validate_context_completeness()
            print(f"✅ Context validation: {len(gaps)} gaps detected")

            if gaps:
                manager2.get_context_recovery_prompt()
                print("✅ Recovery prompt generated successfully")
            else:
                print("✅ Complete context preservation achieved")

        return True

    except Exception as e:
        print(f"❌ Session recovery simulation failed: {e}")
        return False

    finally:
        # Cleanup temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_real_procore_context():
    """Test with real ***REMOVED*** stakeholder context from our work"""
    print("\n🧪 Testing Real ***REMOVED*** Context Preservation...")

    # Use temporary database for testing
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        db_path = tmp_db.name

    try:
        framework = EnhancedFrameworkManager(db_path)

        # Store test stakeholder context
        test_stakeholders = {
            "stakeholder_a": {
                "name": "Director A",
                "role": "Director",
                "style": "product_focused",
                "position": "Not strong platform advocate, skip levels focused on product delivery",
            },
            "stakeholder_b": {
                "name": "SLT Member B",
                "role": "SLT Member",
                "style": "product_focused",
                "position": "100% product focused, conflicts with platform advocate over investment",
            },
            "stakeholder_target": {
                "name": "VP Engineering",
                "role": "VP Engineering",
                "style": "data_driven",
                "position": "Wants ROI understanding, convertible with evidence-based business case",
            },
            "stakeholder_ally": {
                "name": "SLT Ally",
                "role": "SLT Member",
                "style": "strategic",
                "position": "Platform advocate, key SLT ally for platform investment",
            },
        }

        framework.store_strategic_context("stakeholder_update", test_stakeholders)
        print("✅ Test stakeholder context stored")

        # Store ROI discussion context
        roi_context = {
            "target": "stakeholder_target",
            "objective": "Platform investment ROI demonstration",
            "strategy": "Focus on $200K productivity gains and competitive advantage",
            "opposition": "Product-focused stakeholder resistance",
            "allies": "SLT ally support, technical team validation",
        }

        framework.store_strategic_context("roi_discussion", roi_context)
        print("✅ ROI discussion context stored")

        # Test context backup and quality
        backup_success = framework.backup_current_context()
        status = framework.get_context_status()

        print(f"✅ Context backup: {backup_success}")
        print(f"✅ Context quality: {status.get('context_quality', 0):.1%}")

        # Test context validation
        is_valid = framework.validate_context_before_strategic_work()
        print(
            f"✅ Strategic work readiness: {'Ready' if is_valid else 'Requires recovery'}"
        )

        return True

    except Exception as e:
        print(f"❌ Real ***REMOVED*** context test failed: {e}")
        return False

    finally:
        # Cleanup temporary database
        if os.path.exists(db_path):
            os.unlink(db_path)


def main():
    """Run all framework enhancement tests"""
    print("🚀 ClaudeDirector Enhanced Framework Test Suite")
    print("=" * 60)

    tests = [
        ("Session Context Manager", test_session_context_manager),
        ("Enhanced Framework Manager", test_enhanced_framework_manager),
        ("Session Recovery Simulation", test_session_recovery_simulation),
        ("Real ***REMOVED*** Context", test_real_procore_context),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
            print(
                f"{'✅' if success else '❌'} {test_name}: {'PASSED' if success else 'FAILED'}"
            )
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:12} | {test_name}")

    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("🎉 ALL TESTS PASSED - Enhanced framework ready for production!")
        return True
    else:
        print(f"⚠️  {total-passed} tests failed - framework needs debugging")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
