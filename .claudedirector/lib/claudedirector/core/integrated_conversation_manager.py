#!/usr/bin/env python3
"""
Integrated Conversation Manager
Martin's solution for automatic session context capture and management
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..memory.session_context_manager import SessionContextManager
from ..bridges.cli_context_bridge import CLIContextBridge


class IntegratedConversationManager:
    """
    Manages conversation sessions with automatic context preservation
    Integrates SessionContextManager with active conversations
    """

    def __init__(self, db_path: str = None):
        """Initialize conversation manager with session tracking"""
        if db_path is None:
            # Default to ClaudeDirector strategic memory database
            from pathlib import Path
            base_path = Path(__file__).parent.parent.parent.parent.parent
            db_path = str(base_path / "data" / "strategic_memory.db")

        self.session_manager = SessionContextManager(db_path)
        self.cli_bridge = CLIContextBridge(db_path)
        self.current_session_id = None
        self.conversation_buffer = []
        self.backup_interval = 300  # 5 minutes
        self.last_backup_time = None
        self.auto_backup_enabled = True

    def start_conversation_session(self, session_type: str = "strategic") -> str:
        """
        Start new conversation session with context tracking

        Args:
            session_type: Type of session ('strategic', 'executive', 'planning', 'technical')

        Returns:
            Session ID
        """
        # Check for recent incomplete sessions first
        recent_session = self._check_for_recent_session()
        if recent_session:
            response = self._prompt_session_recovery(recent_session)
            if response:
                return self._resume_session(recent_session['session_id'])

        # Start new session
        self.current_session_id = self.session_manager.start_session(session_type)
        self.conversation_buffer = []
        self.last_backup_time = datetime.now()

        # Initial context capture
        self._capture_initial_context()

        print(f"✅ Strategic session started (ID: {self.current_session_id[:8]}...)")
        return self.current_session_id

    def capture_conversation_turn(self, user_input: str, assistant_response: str,
                                personas_activated: List[str] = None,
                                context_metadata: Dict[str, Any] = None) -> None:
        """
        Capture conversation turn for context preservation

        Args:
            user_input: User's message/question
            assistant_response: Assistant's response
            personas_activated: List of personas that were activated
            context_metadata: Additional context metadata
        """
        if not self.current_session_id:
            # Auto-start session if not already active
            self.start_conversation_session()

        conversation_turn = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'assistant_response': assistant_response,
            'personas_activated': personas_activated or [],
            'metadata': context_metadata or {}
        }

        self.conversation_buffer.append(conversation_turn)

        # Auto-backup if interval reached
        if self.auto_backup_enabled and self._should_backup():
            self.backup_conversation_context()

        # Detect strategic context updates
        self._analyze_conversation_for_context_updates(conversation_turn)

    def backup_conversation_context(self) -> bool:
        """
        Backup current conversation context to database

        Returns:
            True if backup successful
        """
        if not self.current_session_id:
            return False

        try:
            # Prepare context data
            context_data = {
                'conversation_thread': self.conversation_buffer,
                'active_personas': self._extract_active_personas(),
                'stakeholder_mentions': self._extract_stakeholder_mentions(),
                'strategic_topics': self._extract_strategic_topics(),
                'decisions_made': self._extract_decisions(),
                'action_items': self._extract_action_items()
            }

            # Update session context
            success = self.session_manager.update_session_context(
                self.current_session_id, context_data
            )

            if success:
                self.last_backup_time = datetime.now()
                print(f"✅ Context backup completed ({len(self.conversation_buffer)} turns)")
                return True
            else:
                print("⚠️ Context backup failed")
                return False

        except Exception as e:
            print(f"❌ Context backup error: {e}")
            return False

    def end_conversation_session(self) -> bool:
        """
        End current conversation session with final backup

        Returns:
            True if session ended successfully
        """
        if not self.current_session_id:
            return True

        # Final backup
        backup_success = self.backup_conversation_context()

        # End session
        end_success = self.session_manager.end_session(self.current_session_id)

        # Create CLI export for cross-environment use
        self._create_session_cli_export()

        if backup_success and end_success:
            print(f"✅ Session ended successfully (ID: {self.current_session_id[:8]}...)")
        else:
            print("⚠️ Session ended with some issues")

        self.current_session_id = None
        self.conversation_buffer = []

        return backup_success and end_success

    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status and metrics"""
        if not self.current_session_id:
            return {'status': 'no_active_session'}

        status = {
            'status': 'active',
            'session_id': self.current_session_id,
            'conversation_turns': len(self.conversation_buffer),
            'last_backup': self.last_backup_time.isoformat() if self.last_backup_time else None,
            'time_since_backup': self._time_since_backup(),
            'context_quality': self._estimate_context_quality(),
            'active_personas': self._extract_active_personas(),
            'next_backup_in': self._time_until_next_backup()
        }

        return status

    def export_for_cli(self, output_file: str = None) -> str:
        """
        Export current session context for CLI use

        Args:
            output_file: Optional file to save export

        Returns:
            CLI-formatted context export
        """
        cli_export = self.cli_bridge.create_cli_session_export()

        if output_file:
            with open(output_file, 'w') as f:
                f.write(cli_export)
            print(f"✅ CLI context exported to {output_file}")

        return cli_export

    def recover_from_context_loss(self) -> bool:
        """
        Attempt to recover from context loss using available data

        Returns:
            True if recovery successful
        """
        print("🔄 Attempting context recovery...")

        # Check for recent sessions
        recent_sessions = self.session_manager.get_recent_sessions(hours=24)

        if recent_sessions:
            latest_session = recent_sessions[0]
            print(f"📋 Found recent session: {latest_session['session_id'][:8]}...")

            # Restore context
            context = self.session_manager.restore_session_context(latest_session['session_id'])

            if context:
                # Analyze context gaps
                gaps = self.session_manager.validate_context_completeness(latest_session['session_id'])

                if gaps:
                    print(f"⚠️ Context gaps detected: {len(gaps)} issues")
                    recovery_prompt = self.session_manager.get_context_recovery_prompt(latest_session['session_id'])
                    print("\n📋 Context Recovery Guidance:")
                    print(recovery_prompt)
                else:
                    print("✅ Context recovery completed successfully")

                return True

        print("❌ No recoverable context found")
        return False

    # Private helper methods

    def _check_for_recent_session(self) -> Optional[Dict[str, Any]]:
        """Check for recent incomplete sessions"""
        recent_sessions = self.session_manager.get_recent_sessions(hours=2)

        for session in recent_sessions:
            if not session.get('session_end_timestamp'):
                return session

        return None

    def _prompt_session_recovery(self, session_info: Dict[str, Any]) -> bool:
        """Prompt user for session recovery (simplified for auto-mode)"""
        # In a full implementation, this would prompt the user
        # For now, auto-recover if session is less than 30 minutes old
        session_start = datetime.fromisoformat(session_info['session_start_timestamp'])
        age = datetime.now() - session_start

        return age < timedelta(minutes=30)

    def _resume_session(self, session_id: str) -> str:
        """Resume existing session"""
        self.current_session_id = session_id

        # Restore conversation buffer from database
        context = self.session_manager.restore_session_context(session_id)
        self.conversation_buffer = context.get('conversation_thread', [])

        print(f"🔄 Resumed session {session_id[:8]}... ({len(self.conversation_buffer)} turns)")
        return session_id

    def _capture_initial_context(self) -> None:
        """Capture initial session context"""
        initial_context = {
            'session_start_time': datetime.now().isoformat(),
            'initial_strategic_state': 'session_initialized'
        }

        self.session_manager.update_session_context(self.current_session_id, initial_context)

    def _should_backup(self) -> bool:
        """Check if backup should be triggered"""
        if not self.last_backup_time:
            return True

        time_since_backup = datetime.now() - self.last_backup_time
        return time_since_backup.total_seconds() >= self.backup_interval

    def _time_since_backup(self) -> int:
        """Get seconds since last backup"""
        if not self.last_backup_time:
            return 0

        return int((datetime.now() - self.last_backup_time).total_seconds())

    def _time_until_next_backup(self) -> int:
        """Get seconds until next scheduled backup"""
        if not self.last_backup_time:
            return 0

        time_since = self._time_since_backup()
        return max(0, self.backup_interval - time_since)

    def _estimate_context_quality(self) -> float:
        """Estimate current context quality score"""
        if not self.conversation_buffer:
            return 0.0

        quality_factors = {
            'conversation_length': min(len(self.conversation_buffer) / 10, 1.0),
            'persona_diversity': len(self._extract_active_personas()) / 5,
            'strategic_depth': self._measure_strategic_depth(),
            'recent_backup': 1.0 if self._time_since_backup() < 600 else 0.5  # 10 min
        }

        return sum(quality_factors.values()) / len(quality_factors)

    def _extract_active_personas(self) -> List[str]:
        """Extract active personas from conversation buffer"""
        personas = set()

        for turn in self.conversation_buffer:
            if turn.get('personas_activated'):
                personas.update(turn['personas_activated'])

        return list(personas)

    def _extract_stakeholder_mentions(self) -> List[str]:
        """Extract stakeholder mentions from conversation"""
        stakeholder_keywords = ['vp_engineering', 'director_product', 'director_platform', 'vp_product', 'cto']
        mentions = []

        for turn in self.conversation_buffer:
            user_text = turn.get('user_input', '').lower()
            assistant_text = turn.get('assistant_response', '').lower()

            for keyword in stakeholder_keywords:
                if keyword in user_text or keyword in assistant_text:
                    mentions.append(keyword)

        return list(set(mentions))

    def _extract_strategic_topics(self) -> List[str]:
        """Extract strategic topics from conversation"""
        strategic_keywords = ['platform', 'roi', 'investment', 'strategy', 'stakeholder', 'budget']
        topics = []

        for turn in self.conversation_buffer:
            text = f"{turn.get('user_input', '')} {turn.get('assistant_response', '')}".lower()

            for keyword in strategic_keywords:
                if keyword in text:
                    topics.append(keyword)

        return list(set(topics))

    def _extract_decisions(self) -> List[str]:
        """Extract decisions from conversation"""
        decision_patterns = ['decided to', 'we should', 'the plan is', 'moving forward with']
        decisions = []

        for turn in self.conversation_buffer:
            text = turn.get('assistant_response', '').lower()

            for pattern in decision_patterns:
                if pattern in text:
                    # Extract the sentence containing the decision
                    sentences = text.split('.')
                    for sentence in sentences:
                        if pattern in sentence:
                            decisions.append(sentence.strip())

        return decisions

    def _extract_action_items(self) -> List[str]:
        """Extract action items from conversation"""
        action_patterns = ['next step', 'action item', 'need to', 'should implement', 'todo']
        actions = []

        for turn in self.conversation_buffer:
            text = turn.get('assistant_response', '').lower()

            for pattern in action_patterns:
                if pattern in text:
                    # Extract action context
                    sentences = text.split('.')
                    for sentence in sentences:
                        if pattern in sentence:
                            actions.append(sentence.strip())

        return actions

    def _measure_strategic_depth(self) -> float:
        """Measure strategic depth of conversation"""
        strategic_indicators = ['framework', 'methodology', 'analysis', 'assessment', 'strategy']
        depth_score = 0.0

        for turn in self.conversation_buffer:
            text = f"{turn.get('user_input', '')} {turn.get('assistant_response', '')}".lower()

            for indicator in strategic_indicators:
                if indicator in text:
                    depth_score += 0.1

        return min(depth_score, 1.0)

    def _analyze_conversation_for_context_updates(self, conversation_turn: Dict[str, Any]) -> None:
        """Analyze conversation turn for strategic context updates"""
        # This would implement intelligent analysis of conversation content
        # to detect when stakeholder information, strategic decisions, etc. are mentioned
        # For now, simplified implementation

        user_input = conversation_turn.get('user_input', '').lower()
        assistant_response = conversation_turn.get('assistant_response', '').lower()

        # Detect stakeholder updates
                if any(name in user_input or name in assistant_response
               for name in ['vp_engineering', 'director', 'executive']):
            # Update stakeholder context
            pass

        # Detect strategic decisions
        if any(phrase in assistant_response
               for phrase in ['recommend', 'strategy', 'decision', 'approach']):
            # Update strategic intelligence
            pass

    def _create_session_cli_export(self) -> None:
        """Create CLI export for session end"""
        try:
            export_filename = f"leadership-workspace/strategy/session-export-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
            self.export_for_cli(export_filename)
        except Exception as e:
            print(f"⚠️ CLI export creation failed: {e}")


def main():
    """CLI interface for conversation manager testing"""
    manager = IntegratedConversationManager()

    print("🧪 Testing Integrated Conversation Manager")
    print("=" * 50)

    # Test session lifecycle
    session_id = manager.start_conversation_session("test")

    # Simulate conversation
    manager.capture_conversation_turn(
        "How should we approach the platform investment strategy?",
        "Based on our strategic analysis, I recommend using the Capital Allocation Framework...",
        ["alvaro", "diego"],
        {"complexity_score": 0.8, "enhancement_used": "sequential"}
    )

    # Test backup
    manager.backup_conversation_context()

    # Test status
    status = manager.get_session_status()
    print(f"📋 Session Status: {status}")

    # Test CLI export
    cli_export = manager.export_for_cli()
    print(f"📄 CLI Export Preview:\n{cli_export[:300]}...")

    # End session
    manager.end_conversation_session()

    print("✅ Conversation manager test completed")


if __name__ == "__main__":
    main()
