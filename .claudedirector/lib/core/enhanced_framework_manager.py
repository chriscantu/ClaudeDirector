#!/usr/bin/env python3
"""
Enhanced ClaudeDirector Framework Manager
Automatic session context preservation and recovery system
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.dirname(current_dir)
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from context_engineering.strategic_memory_manager import get_strategic_memory_manager


class EnhancedFrameworkManager:
    """
    Enhanced ClaudeDirector framework with automatic session context preservation
    Ensures critical context survives session restarts and provides recovery mechanisms
    """

    def __init__(self, db_path: str = None):
        """Initialize enhanced framework with session management"""
        self.session_manager = SessionContextManager(db_path)
        self.current_session = None
        self.context_validated = False
        self.recovery_required = False

        # Initialize session on startup
        self._initialize_session()

    def _initialize_session(self):
        """Initialize session with automatic recovery detection"""
        print("🔄 Initializing ClaudeDirector Enhanced Framework...")

        # Check for session restart
        if self.session_manager.detect_session_restart():
            print("📋 Previous session detected - initiating context recovery...")
            self.recovery_required = True
            self._handle_session_recovery()
        else:
            print("🚀 Starting new strategic session...")
            self.current_session = self.session_manager.start_session("strategic")
            self.context_validated = True

    def _handle_session_recovery(self):
        """Handle session recovery with context validation"""
        try:
            # Restore context from last session
            context = self.session_manager.restore_session_context()

            if context:
                print(
                    f"✅ Context restored (Quality: {context.get('quality_score', 0):.1%})"
                )

                # Validate context completeness
                gaps = self.session_manager.validate_context_completeness()

                if gaps:
                    print(f"⚠️  {len(gaps)} context gaps detected")
                    self._present_recovery_prompt(gaps)
                else:
                    print("✅ Complete context preserved - ready for strategic work")
                    self.context_validated = True
                    self.recovery_required = False
            else:
                print("❌ No recoverable context found - starting fresh session")
                self.current_session = self.session_manager.start_session("strategic")
                self.context_validated = True
                self.recovery_required = False

        except Exception as e:
            print(f"❌ Context recovery failed: {e}")
            print("🔄 Starting new session...")
            self.current_session = self.session_manager.start_session("strategic")
            self.context_validated = True
            self.recovery_required = False

    def _present_recovery_prompt(self, gaps: List[Dict[str, Any]]):
        """Present context recovery prompt to user"""
        prompt = self.session_manager.get_context_recovery_prompt()

        print("\n" + "=" * 60)
        print("🔄 CONTEXT RECOVERY REQUIRED")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

        # Mark as requiring manual recovery
        self.context_validated = False
        self.recovery_required = True

    def validate_context_before_strategic_work(self) -> bool:
        """
        Validate context is complete before allowing strategic work
        Returns True if context is valid, False if recovery needed
        """
        if not self.context_validated:
            if self.recovery_required:
                print("\n⚠️  Context recovery required before continuing strategic work")
                print("Please provide missing context or run /context-recover")
                return False

            # Re-validate current context
            gaps = self.session_manager.validate_context_completeness()
            if gaps:
                self._present_recovery_prompt(gaps)
                return False

            self.context_validated = True

        return True

    def backup_current_context(self) -> bool:
        """Manually trigger context backup"""
        if not self.current_session:
            self.current_session = self.session_manager.current_session_id

        if self.current_session:
            success = self.session_manager.backup_session_context(self.current_session)
            if success:
                print("✅ Context backup completed")
            else:
                print("❌ Context backup failed")
            return success

        print("❌ No active session to backup")
        return False

    def get_context_status(self) -> Dict[str, Any]:
        """Get current context status and quality information"""
        if not self.current_session:
            return {
                "session_active": False,
                "context_validated": False,
                "recovery_required": False,
            }

        context = self.session_manager.restore_session_context()
        gaps = self.session_manager.validate_context_completeness()

        return {
            "session_id": self.current_session,
            "session_active": True,
            "context_validated": self.context_validated,
            "recovery_required": self.recovery_required,
            "context_quality": context.get("quality_score", 0.0),
            "context_gaps": len(gaps),
            "gap_details": gaps,
        }

    def mark_context_recovered(self, recovery_details: Dict[str, Any] = None):
        """Mark context as recovered after user provides missing information"""
        if recovery_details:
            # Store recovery details for context enhancement
            # This would integrate with the memory system to update context
            pass

        # Re-validate context
        gaps = self.session_manager.validate_context_completeness()

        if not gaps:
            print("✅ Context recovery complete - strategic work ready")
            self.context_validated = True
            self.recovery_required = False

            # Backup the recovered context
            self.backup_current_context()
        else:
            print(f"⚠️  {len(gaps)} context gaps remain")
            self._present_recovery_prompt(gaps)

    def store_strategic_context(self, context_type: str, context_data: Dict[str, Any]):
        """Store strategic context for preservation"""
        if context_type == "stakeholder_update":
            self._store_stakeholder_context(context_data)
        elif context_type == "initiative_update":
            self._store_initiative_context(context_data)
        elif context_type == "executive_session":
            self._store_executive_context(context_data)
        elif context_type == "roi_discussion":
            self._store_roi_context(context_data)

        # Trigger automatic backup after context update
        self.backup_current_context()

    def _store_stakeholder_context(self, data: Dict[str, Any]):
        """Store stakeholder context updates"""
        for stakeholder_key, details in data.items():
            self.session_manager.store_stakeholder_profile(
                stakeholder_key=stakeholder_key,
                display_name=details.get("name", ""),
                role_title=details.get("role", ""),
                communication_style=details.get("style", ""),
            )

    def _store_initiative_context(self, data: Dict[str, Any]):
        """Store strategic initiative context updates"""
        for initiative_key, details in data.items():
            self.session_manager.store_strategic_initiative(
                initiative_key=initiative_key,
                initiative_name=details.get("name", ""),
                status=details.get("status", "new"),
                priority=details.get("priority", "medium"),
                business_value=details.get("business_value", ""),
                assignee=details.get("assignee", ""),
            )

    def _store_executive_context(self, data: Dict[str, Any]):
        """Store executive session context"""
        self.session_manager.store_executive_session(
            session_type=data.get("type", "strategic_planning"),
            stakeholder_key=data.get("stakeholder", "unknown"),
            meeting_date=data.get("date", datetime.now().date().isoformat()),
            agenda_topics=data.get("agenda", []),
            decisions_made=data.get("decisions", {}),
            business_impact=data.get("impact", ""),
            next_session_prep=data.get("prep", ""),
            persona_activated=data.get("persona", ""),
        )

    def _store_roi_context(self, data: Dict[str, Any]):
        """Store ROI discussion context"""
        # This would store ROI-specific context
        # For now, store as platform intelligence
        self.session_manager.store_platform_intelligence(
            intelligence_type="roi_discussion",
            category="platform_investment",
            value_text=json.dumps(data),
            data_source="user_input",
        )

    def end_session(self):
        """Properly end current session with final backup"""
        if self.current_session:
            print("🔄 Ending session with final context backup...")
            self.backup_current_context()
            self.session_manager.end_session(self.current_session)
            print("✅ Session ended successfully")

    def get_framework_status(self) -> str:
        """Get formatted framework status for display"""
        status = self.get_context_status()

        if not status["session_active"]:
            return "❌ No active session"

        if status["recovery_required"]:
            return f"⚠️  Context recovery required ({status['context_gaps']} gaps)"

        if status["context_validated"]:
            quality = status["context_quality"]
            quality_str = f"{quality:.1%}"
            return f"✅ Strategic session ready (Context quality: {quality_str})"

        return "🔄 Context validation in progress"


# Global framework instance for easy access
_framework_instance = None


def get_framework_manager() -> EnhancedFrameworkManager:
    """Get global framework manager instance"""
    global _framework_instance

    if _framework_instance is None:
        _framework_instance = EnhancedFrameworkManager()

    return _framework_instance


def ensure_context_ready() -> bool:
    """Ensure context is ready for strategic work"""
    framework = get_framework_manager()
    return framework.validate_context_before_strategic_work()


# CLI Integration
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ClaudeDirector Enhanced Framework Manager"
    )
    parser.add_argument("--status", action="store_true", help="Show framework status")
    parser.add_argument("--backup", action="store_true", help="Backup current context")
    parser.add_argument(
        "--recover", action="store_true", help="Show context recovery prompt"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate context completeness"
    )

    args = parser.parse_args()

    framework = get_framework_manager()

    if args.status:
        print(framework.get_framework_status())
        status = framework.get_context_status()
        print(f"\nDetailed Status:")
        print(f"Session ID: {status.get('session_id', 'None')}")
        print(f"Context Quality: {status.get('context_quality', 0):.1%}")
        print(f"Context Gaps: {status.get('context_gaps', 0)}")

    elif args.backup:
        framework.backup_current_context()

    elif args.recover:
        gaps = framework.session_manager.validate_context_completeness()
        if gaps:
            prompt = framework.session_manager.get_context_recovery_prompt()
            print(prompt)
        else:
            print("✅ No context recovery needed")

    elif args.validate:
        if framework.validate_context_before_strategic_work():
            print("✅ Context validated - ready for strategic work")
        else:
            print("❌ Context validation failed - recovery required")

    else:
        print(framework.get_framework_status())
