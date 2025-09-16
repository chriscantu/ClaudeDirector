#!/usr/bin/env python3
"""
Conversation Persistence Bridge - Phase B Implementation
Conversation Persistence System Recovery

Authors: Martin | Platform Architecture + Diego | Engineering Leadership
Story: Phase B - Automatic Response Interception
Priority: P0 - BLOCKING (Conversation persistence foundation)

This module provides the bridge between existing conversation management systems
and the validated database, enabling automatic conversation capture and storage.

Key Features:
- Observer pattern for real-time conversation monitoring
- Factory pattern for platform-specific handlers (Cursor/Claude)
- Strategy pattern for different capture approaches
- HIGH TRUST AI capabilities only (regex patterns, keyword detection)
- Zero impact on existing P0 functionality

CRITICAL: Follows PROJECT_STRUCTURE.md core/ patterns and BLOAT_PREVENTION_SYSTEM.md
"""

import re
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from abc import ABC, abstractmethod

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import existing components to avoid duplication (BLOAT_PREVENTION_SYSTEM.md)
try:
    from .database import DatabaseManager
except ImportError:
    from .unified_database import UnifiedDatabaseCoordinator as DatabaseManager

try:
    from ..context_engineering.conversation_layer import ConversationLayerMemory
except ImportError:
    # Lightweight fallback if context_engineering not available
    ConversationLayerMemory = None


class ConversationPlatform(Enum):
    """Supported conversation platforms"""

    CURSOR = "cursor"
    CLAUDE = "claude"
    UNKNOWN = "unknown"


class ConversationEvent(Enum):
    """Types of conversation events to capture"""

    USER_INPUT = "user_input"
    AI_RESPONSE = "ai_response"
    PERSONA_ACTIVATION = "persona_activation"
    SESSION_START = "session_start"
    SESSION_END = "session_end"


@dataclass
class ConversationCapture:
    """Data structure for captured conversation data"""

    session_id: str
    user_input: str
    assistant_response: str
    timestamp: float
    platform: ConversationPlatform
    persona_detected: Optional[str] = None
    action_pattern_count: int = 0
    strategic_context_score: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class ConversationPatternDetector:
    """
    HIGH TRUST AI pattern detection for strategic conversations.
    Uses regex patterns and keyword detection (reliable AI capabilities).
    """

    # HIGH TRUST: Regex patterns for persona detection
    PERSONA_PATTERNS = {
        "diego": re.compile(
            r"🎯\s*Diego\s*\|\s*Engineering\s*Leadership", re.IGNORECASE
        ),
        "camille": re.compile(
            r"📊\s*Camille\s*\|\s*Strategic\s*Technology", re.IGNORECASE
        ),
        "rachel": re.compile(r"🎨\s*Rachel\s*\|\s*Design\s*Systems", re.IGNORECASE),
        "alvaro": re.compile(
            r"💼\s*Alvaro\s*\|\s*Platform\s*Investment", re.IGNORECASE
        ),
        "martin": re.compile(
            r"🏗️\s*Martin\s*\|\s*Platform\s*Architecture", re.IGNORECASE
        ),
        "marcus": re.compile(r"📈\s*Marcus\s*\|\s*Platform\s*Adoption", re.IGNORECASE),
    }

    # HIGH TRUST: Action pattern keywords
    ACTION_KEYWORDS = [
        "implement",
        "create",
        "develop",
        "build",
        "design",
        "analyze",
        "review",
        "optimize",
        "refactor",
        "test",
        "deploy",
        "configure",
        "strategic",
        "recommend",
        "evaluate",
        "assess",
        "plan",
        "execute",
    ]

    # HIGH TRUST: Strategic context indicators
    STRATEGIC_INDICATORS = [
        "strategic",
        "architecture",
        "platform",
        "framework",
        "system",
        "organization",
        "team",
        "leadership",
        "decision",
        "investment",
        "roadmap",
        "planning",
        "vision",
        "objectives",
        "goals",
    ]

    def detect_persona(self, text: str) -> Optional[str]:
        """Detect persona using HIGH TRUST regex patterns"""
        for persona_name, pattern in self.PERSONA_PATTERNS.items():
            if pattern.search(text):
                return persona_name
        return None

    def count_action_patterns(self, text: str) -> int:
        """Count action patterns using HIGH TRUST keyword detection"""
        text_lower = text.lower()
        return sum(1 for keyword in self.ACTION_KEYWORDS if keyword in text_lower)

    def calculate_strategic_context_score(self, text: str) -> float:
        """Calculate strategic context score using HIGH TRUST indicators"""
        text_lower = text.lower()
        matches = sum(
            1 for indicator in self.STRATEGIC_INDICATORS if indicator in text_lower
        )
        # Normalize to 0.0-1.0 range
        return min(matches / len(self.STRATEGIC_INDICATORS), 1.0)


class ConversationCaptureStrategy(ABC):
    """Abstract strategy for capturing conversations from different platforms"""

    def __init__(self, pattern_detector: ConversationPatternDetector):
        self.pattern_detector = pattern_detector
        self.logger = logger.bind(strategy=self.__class__.__name__)

    @abstractmethod
    def should_capture(self, user_input: str, ai_response: str) -> bool:
        """Determine if this conversation should be captured"""
        pass

    @abstractmethod
    def extract_metadata(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """Extract platform-specific metadata"""
        pass


class CursorCaptureStrategy(ConversationCaptureStrategy):
    """Strategy for capturing conversations from Cursor IDE"""

    def should_capture(self, user_input: str, ai_response: str) -> bool:
        """Capture if persona detected or strategic indicators present"""
        has_persona = self.pattern_detector.detect_persona(ai_response) is not None
        has_strategic_context = (
            self.pattern_detector.calculate_strategic_context_score(
                user_input + " " + ai_response
            )
            > 0.2
        )
        return has_persona or has_strategic_context

    def extract_metadata(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """Extract Cursor-specific metadata"""
        return {
            "platform": "cursor",
            "ide_integration": True,
            "session_type": "development",
        }


class ClaudeCaptureStrategy(ConversationCaptureStrategy):
    """Strategy for capturing conversations from Claude.ai"""

    def should_capture(self, user_input: str, ai_response: str) -> bool:
        """More selective capture for Claude.ai (manual trigger preferred)"""
        has_persona = self.pattern_detector.detect_persona(ai_response) is not None
        has_high_strategic_context = (
            self.pattern_detector.calculate_strategic_context_score(
                user_input + " " + ai_response
            )
            > 0.4
        )
        return has_persona or has_high_strategic_context

    def extract_metadata(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """Extract Claude-specific metadata"""
        return {
            "platform": "claude",
            "web_interface": True,
            "session_type": "strategic",
        }


class ConversationPersistenceBridge:
    """
    Main bridge class that connects conversation events to database persistence.

    Implements Observer pattern to monitor conversations and Strategy pattern
    to handle different platforms appropriately.

    CRITICAL: Follows BLOAT_PREVENTION_SYSTEM.md by reusing existing components:
    - DatabaseManager for database operations
    - ConversationLayerMemory for conversation structure
    - Established patterns for data validation
    """

    def __init__(self, db_path: Optional[str] = None):
        self.logger = logger.bind(component="ConversationPersistenceBridge")

        # Initialize pattern detector (HIGH TRUST AI capabilities)
        self.pattern_detector = ConversationPatternDetector()

        # Initialize capture strategies
        self.strategies = {
            ConversationPlatform.CURSOR: CursorCaptureStrategy(self.pattern_detector),
            ConversationPlatform.CLAUDE: ClaudeCaptureStrategy(self.pattern_detector),
        }

        # Initialize database connection (reuse existing DatabaseManager)
        self.db_manager = self._initialize_database(db_path)

        # Initialize conversation layer if available
        self.conversation_layer = self._initialize_conversation_layer()

        # Event observers
        self.observers: List[Callable[[ConversationCapture], None]] = []

        self.logger.info("ConversationPersistenceBridge initialized")

    def _initialize_database(self, db_path: Optional[str] = None) -> DatabaseManager:
        """Initialize database manager with existing validated database"""
        try:
            if db_path:
                return DatabaseManager(db_path=db_path)
            else:
                # Use default database path from Phase A validation
                return DatabaseManager()
        except Exception as e:
            self.logger.error(f"Failed to initialize database manager: {e}")
            raise

    def _initialize_conversation_layer(self) -> Optional[ConversationLayerMemory]:
        """Initialize conversation layer if available"""
        if ConversationLayerMemory:
            try:
                return ConversationLayerMemory()
            except Exception as e:
                self.logger.warning(f"ConversationLayerMemory not available: {e}")
        return None

    def detect_platform(self, context_hints: Dict[str, Any]) -> ConversationPlatform:
        """Detect platform from context hints"""
        if context_hints.get("cursor", False) or context_hints.get("ide", False):
            return ConversationPlatform.CURSOR
        elif context_hints.get("claude", False) or context_hints.get("web", False):
            return ConversationPlatform.CLAUDE
        else:
            return ConversationPlatform.UNKNOWN

    def capture_conversation(
        self,
        user_input: str,
        ai_response: str,
        session_id: Optional[str] = None,
        platform_hints: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Capture a conversation turn and store it in the database.

        Args:
            user_input: User's input message
            ai_response: AI assistant's response
            session_id: Optional session identifier
            platform_hints: Optional platform detection hints

        Returns:
            True if conversation was captured and stored, False otherwise
        """
        try:
            # Detect platform
            platform = self.detect_platform(platform_hints or {})

            # Get appropriate capture strategy
            strategy = self.strategies.get(platform)
            if not strategy:
                self.logger.warning(f"No strategy available for platform: {platform}")
                return False

            # Check if conversation should be captured
            if not strategy.should_capture(user_input, ai_response):
                self.logger.debug("Conversation does not meet capture criteria")
                return False

            # Generate session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())

            # Detect persona and calculate metrics
            persona_detected = self.pattern_detector.detect_persona(ai_response)
            action_pattern_count = self.pattern_detector.count_action_patterns(
                user_input + " " + ai_response
            )
            strategic_context_score = (
                self.pattern_detector.calculate_strategic_context_score(
                    user_input + " " + ai_response
                )
            )

            # Extract platform-specific metadata
            metadata = strategy.extract_metadata(user_input, ai_response)

            # Create conversation capture object
            capture = ConversationCapture(
                session_id=session_id,
                user_input=user_input,
                assistant_response=ai_response,
                timestamp=time.time(),
                platform=platform,
                persona_detected=persona_detected,
                action_pattern_count=action_pattern_count,
                strategic_context_score=strategic_context_score,
                metadata=metadata,
            )

            # Store in database
            success = self._store_conversation(capture)

            # Notify observers
            if success:
                self._notify_observers(capture)

            return success

        except Exception as e:
            self.logger.error(f"Failed to capture conversation: {e}")
            return False

    def _store_conversation(self, capture: ConversationCapture) -> bool:
        """Store conversation capture in the database"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Insert into conversations table (validated schema from Phase A)
                cursor.execute(
                    """
                    INSERT INTO conversations (
                        session_id, user_input, assistant_response, timestamp,
                        action_pattern_count, strategic_context_score
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        capture.session_id,
                        capture.user_input,
                        capture.assistant_response,
                        capture.timestamp,
                        capture.action_pattern_count,
                        capture.strategic_context_score,
                    ),
                )

                # Insert session context if not exists
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO session_context (
                        session_id, session_type, active_personas, created_at
                    ) VALUES (?, ?, ?, ?)
                """,
                    (
                        capture.session_id,
                        capture.platform.value,
                        capture.persona_detected or "",
                        capture.timestamp,
                    ),
                )

                # Insert strategic insights if persona detected
                if capture.persona_detected:
                    cursor.execute(
                        """
                        INSERT INTO strategic_insights (
                            session_id, insight_type, insight_data, created_at
                        ) VALUES (?, ?, ?, ?)
                    """,
                        (
                            capture.session_id,
                            "persona_activation",
                            f"Persona: {capture.persona_detected}",
                            capture.timestamp,
                        ),
                    )

                self.logger.info(
                    f"Conversation stored successfully",
                    session_id=capture.session_id,
                    persona=capture.persona_detected,
                    platform=capture.platform.value,
                )
                return True

        except Exception as e:
            self.logger.error(f"Failed to store conversation in database: {e}")
            return False

    def add_observer(self, observer: Callable[[ConversationCapture], None]):
        """Add observer for conversation capture events"""
        self.observers.append(observer)

    def remove_observer(self, observer: Callable[[ConversationCapture], None]):
        """Remove observer for conversation capture events"""
        if observer in self.observers:
            self.observers.remove(observer)

    def _notify_observers(self, capture: ConversationCapture):
        """Notify all observers of conversation capture"""
        for observer in self.observers:
            try:
                observer(capture)
            except Exception as e:
                self.logger.warning(f"Observer notification failed: {e}")

    def get_conversation_history(
        self, session_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Retrieve conversation history for a session"""
        try:
            with self.db_manager.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_input, assistant_response, timestamp,
                           action_pattern_count, strategic_context_score
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """,
                    (session_id, limit),
                )

                results = cursor.fetchall()
                return [
                    {
                        "user_input": row[0],
                        "assistant_response": row[1],
                        "timestamp": row[2],
                        "action_pattern_count": row[3],
                        "strategic_context_score": row[4],
                    }
                    for row in results
                ]

        except Exception as e:
            self.logger.error(f"Failed to retrieve conversation history: {e}")
            return []

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about captured conversations"""
        try:
            with self.db_manager.get_cursor() as cursor:
                # Total conversations
                cursor.execute("SELECT COUNT(*) FROM conversations")
                total_conversations = cursor.fetchone()[0]

                # Unique sessions
                cursor.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
                unique_sessions = cursor.fetchone()[0]

                # Persona activations
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM strategic_insights
                    WHERE insight_type = 'persona_activation'
                """
                )
                persona_activations = cursor.fetchone()[0]

                return {
                    "total_conversations": total_conversations,
                    "unique_sessions": unique_sessions,
                    "persona_activations": persona_activations,
                    "database_healthy": True,
                }

        except Exception as e:
            self.logger.error(f"Failed to get session stats: {e}")
            return {"database_healthy": False, "error": str(e)}


# Singleton instance for global access
_conversation_bridge: Optional[ConversationPersistenceBridge] = None


def get_conversation_bridge(
    db_path: Optional[str] = None,
) -> ConversationPersistenceBridge:
    """Get singleton conversation persistence bridge instance"""
    global _conversation_bridge
    if _conversation_bridge is None:
        _conversation_bridge = ConversationPersistenceBridge(db_path)
    return _conversation_bridge


def capture_conversation_turn(
    user_input: str,
    ai_response: str,
    session_id: Optional[str] = None,
    platform_hints: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Convenient function to capture a conversation turn.

    This is the main entry point for conversation capture from external systems.
    """
    bridge = get_conversation_bridge()
    return bridge.capture_conversation(
        user_input, ai_response, session_id, platform_hints
    )


if __name__ == "__main__":
    # Test the conversation persistence bridge
    bridge = ConversationPersistenceBridge()

    # Test conversation capture
    test_user_input = (
        "How should we structure our engineering teams for better scalability?"
    )
    test_ai_response = """🎯 Diego | Engineering Leadership

    Great question! Let me apply Team Topologies framework to this challenge...

    I recommend implementing a platform team structure with clear boundaries..."""

    success = bridge.capture_conversation(
        test_user_input, test_ai_response, platform_hints={"cursor": True}
    )

    if success:
        print("✅ Test conversation captured successfully")
        stats = bridge.get_session_stats()
        print(f"📊 Database stats: {stats}")
    else:
        print("❌ Test conversation capture failed")
