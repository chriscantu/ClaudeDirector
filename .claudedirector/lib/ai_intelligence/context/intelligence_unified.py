"""
Intelligence Unified - Phase 9 Consolidation

This module consolidates intelligence functionality from:
- intelligence/meeting.py
- intelligence/task.py
- intelligence/stakeholder.py (references Phase 2.1 consolidation)

Status: Phase 9 Architecture Cleanup - Intelligence Layer Consolidation
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import json
import logging
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Import consolidated stakeholder intelligence (Phase 2.1)
try:
    from ...context_engineering.stakeholder_intelligence_unified import (
        get_stakeholder_intelligence,
        StakeholderIntelligenceUnified,
    )

    STAKEHOLDER_INTELLIGENCE_AVAILABLE = True
except ImportError:
    STAKEHOLDER_INTELLIGENCE_AVAILABLE = False

# Import consolidated strategic memory (Phase 2.2)
try:
    from ...context_engineering.strategic_memory_manager import (
        get_strategic_memory_manager,
        StrategicMemoryManager,
    )

    STRATEGIC_MEMORY_AVAILABLE = True
except ImportError:
    STRATEGIC_MEMORY_AVAILABLE = False

# Phase 8 performance integration
try:
    from ...performance.cache_manager import get_cache_manager
    from ...performance.memory_optimizer import get_memory_optimizer
    from ...performance.response_optimizer import get_response_optimizer

    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False

# Legacy compatibility imports
try:
    from ...core.config import get_config
    from ...core.exceptions import AIDetectionError, DatabaseError

    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

    # Fallback minimal config
    class MinimalConfig:
        def __init__(self):
            project_root = Path(__file__).parent.parent.parent.parent.parent
            self.database_path = str(project_root / "data" / "strategic_memory.db")
            self.workspace_dir = str(project_root / "leadership-workspace")

        @property
        def workspace_path_obj(self):
            return Path(self.workspace_dir)

    def get_config():
        return MinimalConfig()

    class AIDetectionError(Exception):
        def __init__(self, message, detection_type=None):
            super().__init__(message)
            self.detection_type = detection_type

    class DatabaseError(Exception):
        pass


# Task-related enums and dataclasses
class TaskPriority(Enum):
    """Task priority classification"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task status tracking"""

    DISCOVERED = "discovered"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    """Task type classification"""

    ACTION_ITEM = "action_item"
    DECISION = "decision"
    RESEARCH = "research"
    COMMUNICATION = "communication"
    MILESTONE = "milestone"
    FOLLOWUP = "followup"


@dataclass
class TaskProfile:
    """Comprehensive task profile with intelligence"""

    task_id: str
    title: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    status: TaskStatus

    # Context information
    source_document: str
    stakeholders_involved: List[str]
    deadline: Optional[str]
    dependencies: List[str]

    # Intelligence fields
    detection_confidence: float
    auto_extracted: bool
    strategic_importance: float  # 0.0 to 1.0

    # Tracking
    created_timestamp: float
    updated_timestamp: float
    completed_timestamp: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with enum serialization"""
        data = asdict(self)
        data["task_type"] = self.task_type.value
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data


# Meeting-related enums and dataclasses
class MeetingType(Enum):
    """Meeting type classification"""

    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    STANDUP = "standup"
    REVIEW = "review"
    PLANNING = "planning"
    DECISION = "decision"
    STAKEHOLDER = "stakeholder"
    EXECUTIVE = "executive"


@dataclass
class MeetingProfile:
    """Comprehensive meeting profile with intelligence"""

    meeting_id: str
    title: str
    meeting_type: MeetingType
    date: str
    duration_minutes: int

    # Participants
    organizer: str
    participants: List[str]
    stakeholders_involved: List[str]

    # Content analysis
    agenda_items: List[str]
    decisions_made: List[str]
    action_items: List[str]
    key_topics: List[str]

    # Intelligence fields
    strategic_importance: float  # 0.0 to 1.0
    sentiment_score: float  # -1.0 to 1.0
    conflict_indicators: List[str]
    collaboration_score: float  # 0.0 to 1.0

    # Context
    source_document: str
    related_initiatives: List[str]

    # Tracking
    created_timestamp: float
    updated_timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with enum serialization"""
        data = asdict(self)
        data["meeting_type"] = self.meeting_type.value
        return data


class IntelligenceUnified:
    """
    Unified Intelligence System - Phase 9 Single Source of Truth

    Consolidates functionality from:
    - TaskIntelligence (intelligence layer)
    - MeetingIntelligence (intelligence layer)
    - StakeholderIntelligence integration (references Phase 2.1)

    Features:
    - AI-powered task detection and management
    - Meeting analysis and intelligence extraction
    - Strategic context integration
    - Performance-optimized operations
    - Complete backward compatibility
    """

    def __init__(
        self, config: Optional[Dict[str, Any]] = None, enable_performance: bool = True
    ):
        """Initialize unified intelligence system"""
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)
        self.enable_performance = enable_performance

        # Initialize performance components (Phase 8 integration)
        if self.enable_performance and PERFORMANCE_AVAILABLE:
            try:
                self.cache_manager = get_cache_manager()
                self.memory_optimizer = get_memory_optimizer()
                self.response_optimizer = get_response_optimizer()
                self.logger.info(
                    "Phase 8 performance optimization enabled for intelligence"
                )
            except Exception as e:
                self.logger.warning(f"Performance optimization unavailable: {e}")
                self.enable_performance = False

        # Initialize consolidated subsystems
        if STAKEHOLDER_INTELLIGENCE_AVAILABLE:
            self.stakeholder_intelligence = get_stakeholder_intelligence()
        else:
            self.stakeholder_intelligence = None

        if STRATEGIC_MEMORY_AVAILABLE:
            self.strategic_memory = get_strategic_memory_manager()
        else:
            self.strategic_memory = None

        # In-memory storage (Phase 9.1)
        # Phase 9.2 will add persistent storage with relationship analytics
        self.tasks: Dict[str, TaskProfile] = {}
        self.meetings: Dict[str, MeetingProfile] = {}

        # Legacy compatibility layer
        self._init_legacy_compatibility()

        self.logger.info(
            "IntelligenceUnified initialized - Phase 9 consolidation active"
        )

    def _init_legacy_compatibility(self) -> None:
        """Initialize legacy compatibility during migration"""
        try:
            # Migrate existing task data if available
            self._migrate_legacy_task_data()

            # Migrate existing meeting data if available
            self._migrate_legacy_meeting_data()
        except Exception as e:
            self.logger.warning(f"Legacy migration skipped: {e}")

    def _migrate_legacy_task_data(self) -> None:
        """Migrate task data from legacy systems during Phase 9"""
        # This will be implemented to preserve existing task intelligence
        # during the migration process
        pass

    def _migrate_legacy_meeting_data(self) -> None:
        """Migrate meeting data from legacy systems during Phase 9"""
        # This will be implemented to preserve existing meeting intelligence
        # during the migration process
        pass

    # === TASK INTELLIGENCE ===

    def detect_tasks_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        AI-powered task detection in content
        Consolidates functionality from TaskIntelligence

        Args:
            content: Text content to analyze
            context: Context information (file_path, category, etc.)

        Returns:
            List of detected task candidates with confidence scores
        """
        try:
            # Use cache for performance if available
            if self.enable_performance:
                cache_key = f"task_detection:{hash(content[:100])}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Enhanced AI detection logic
            candidates = self._analyze_content_for_tasks(content, context)

            # Cache results
            if self.enable_performance and candidates:
                self.cache_manager.set(cache_key, candidates, ttl=7200)  # 2 hour cache

            return candidates

        except Exception as e:
            raise AIDetectionError(f"Task detection failed: {e}", detection_type="task")

    def _analyze_content_for_tasks(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze content for task mentions and patterns"""
        candidates = []
        content_lower = content.lower()

        # Task pattern detection
        import re

        # Action item patterns
        action_patterns = [
            r"action item[s]?[:\-\s]*([^\n]+)",
            r"todo[s]?[:\-\s]*([^\n]+)",
            r"next step[s]?[:\-\s]*([^\n]+)",
            r"follow[- ]?up[s]?[:\-\s]*([^\n]+)",
            r"will\s+(\w+(?:\s+\w+)*)\s+(?:by|before|on)",
            r"need[s]?\s+to\s+([^\n\.]+)",
            r"should\s+([^\n\.]+)",
            r"must\s+([^\n\.]+)",
        ]

        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                task_text = match.strip()
                if (
                    len(task_text) > 5 and len(task_text) < 200
                ):  # Reasonable task length
                    candidates.append(
                        {
                            "title": task_text[:100],  # Truncate title
                            "description": task_text,
                            "task_type": "action_item",
                            "priority": self._determine_task_priority(
                                task_text, content
                            ),
                            "confidence": 0.7,
                            "detection_method": "action_pattern",
                            "source_document": context.get("file_path", ""),
                            "strategic_importance": self._calculate_task_importance(
                                task_text, content
                            ),
                        }
                    )

        # Decision patterns
        decision_patterns = [
            r"decision[:\-\s]*([^\n]+)",
            r"we decided[:\-\s]*([^\n]+)",
            r"conclusion[:\-\s]*([^\n]+)",
            r"agreed that[:\-\s]*([^\n]+)",
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                decision_text = match.strip()
                if len(decision_text) > 5 and len(decision_text) < 200:
                    candidates.append(
                        {
                            "title": f"Decision: {decision_text[:80]}",
                            "description": decision_text,
                            "task_type": "decision",
                            "priority": self._determine_task_priority(
                                decision_text, content
                            ),
                            "confidence": 0.8,
                            "detection_method": "decision_pattern",
                            "source_document": context.get("file_path", ""),
                            "strategic_importance": self._calculate_task_importance(
                                decision_text, content
                            ),
                        }
                    )

        # Remove duplicates and validate
        unique_candidates = []
        seen_titles = set()

        for candidate in candidates:
            title_key = candidate["title"].lower().strip()
            if title_key not in seen_titles and len(title_key) > 5:
                seen_titles.add(title_key)
                unique_candidates.append(candidate)

        return unique_candidates[:20]  # Limit to top 20 candidates

    def _determine_task_priority(self, task_text: str, content: str) -> str:
        """Determine task priority based on content"""
        task_lower = task_text.lower()
        content_lower = content.lower()

        # High priority indicators
        high_indicators = ["urgent", "critical", "asap", "immediately", "emergency"]
        if any(indicator in task_lower for indicator in high_indicators):
            return "high"

        # Medium priority indicators
        medium_indicators = ["important", "priority", "soon", "deadline"]
        if any(
            indicator in task_lower or indicator in content_lower
            for indicator in medium_indicators
        ):
            return "medium"

        return "low"  # Default

    def _calculate_task_importance(self, task_text: str, content: str) -> float:
        """Calculate strategic importance of task (0.0 to 1.0)"""
        importance_terms = [
            "strategic",
            "critical",
            "executive",
            "board",
            "revenue",
            "competitive",
            "market",
            "customer",
            "platform",
            "architecture",
        ]

        task_lower = task_text.lower()
        content_lower = content.lower()

        score = 0.3  # Base score

        # Boost for importance terms
        term_count = sum(
            1
            for term in importance_terms
            if term in task_lower or term in content_lower
        )
        boost = min(0.5, term_count * 0.1)

        return min(1.0, score + boost)

    def add_task(
        self, task_data: Dict[str, Any], source: str = "manual", confidence: float = 1.0
    ) -> bool:
        """
        Add or update task profile with enhanced intelligence

        Args:
            task_data: Comprehensive task information
            source: Source of the data (manual, ai_detection, file_analysis)
            confidence: Confidence level for AI-detected tasks

        Returns:
            True if successful, False otherwise
        """
        try:
            task_id = task_data.get("task_id") or f"task_{int(time.time())}"

            current_time = time.time()

            if task_id in self.tasks:
                # Update existing task
                task = self.tasks[task_id]
                for key, value in task_data.items():
                    if hasattr(task, key) and value is not None:
                        # Handle enum fields
                        if key == "task_type" and isinstance(value, str):
                            task.task_type = TaskType(value)
                        elif key == "priority" and isinstance(value, str):
                            task.priority = TaskPriority(value)
                        elif key == "status" and isinstance(value, str):
                            task.status = TaskStatus(value)
                        else:
                            setattr(task, key, value)

                task.updated_timestamp = current_time
            else:
                # Create new task
                task = TaskProfile(
                    task_id=task_id,
                    title=task_data.get("title", ""),
                    description=task_data.get("description", ""),
                    task_type=TaskType(task_data.get("task_type", "action_item")),
                    priority=TaskPriority(task_data.get("priority", "medium")),
                    status=TaskStatus(task_data.get("status", "discovered")),
                    source_document=task_data.get("source_document", ""),
                    stakeholders_involved=task_data.get("stakeholders_involved", []),
                    deadline=task_data.get("deadline"),
                    dependencies=task_data.get("dependencies", []),
                    detection_confidence=confidence,
                    auto_extracted=source != "manual",
                    strategic_importance=task_data.get("strategic_importance", 0.5),
                    created_timestamp=current_time,
                    updated_timestamp=current_time,
                    completed_timestamp=None,
                )
                self.tasks[task_id] = task

            # Cache invalidation for performance
            if self.enable_performance:
                self.cache_manager.delete_pattern("task_*")

            self.logger.debug(f"Added/updated task: {task_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add task: {e}")
            return False

    def get_task(self, task_id: str) -> Optional[TaskProfile]:
        """Get task profile by ID"""
        return self.tasks.get(task_id)

    def list_tasks(
        self, filter_by: Optional[Dict[str, Any]] = None, include_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List tasks with optional filtering

        Args:
            filter_by: Optional filters (status, priority, task_type, etc.)
            include_metadata: Include detection and timing metadata

        Returns:
            List of task profiles as dictionaries
        """
        try:
            # Use cached result if available
            if self.enable_performance:
                cache_key = f"task_list:{hash(str(sorted((filter_by or {}).items())))}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            tasks = list(self.tasks.values())

            # Apply filters
            if filter_by:
                tasks = self._apply_task_filters(tasks, filter_by)

            # Convert to dictionaries
            result = []
            for task in tasks:
                data = task.to_dict()
                if not include_metadata:
                    # Remove metadata for cleaner API
                    metadata_keys = [
                        "detection_confidence",
                        "auto_extracted",
                        "created_timestamp",
                        "updated_timestamp",
                    ]
                    for key in metadata_keys:
                        data.pop(key, None)
                result.append(data)

            # Cache result
            if self.enable_performance:
                self.cache_manager.set(cache_key, result, ttl=1800)  # 30 minute cache

            return result

        except Exception as e:
            self.logger.error(f"Failed to list tasks: {e}")
            return []

    def _apply_task_filters(
        self, tasks: List[TaskProfile], filters: Dict[str, Any]
    ) -> List[TaskProfile]:
        """Apply filters to task list"""
        filtered = tasks

        if "status" in filters:
            status_filter = filters["status"]
            if isinstance(status_filter, str):
                filtered = [t for t in filtered if t.status.value == status_filter]
            elif isinstance(status_filter, list):
                filtered = [t for t in filtered if t.status.value in status_filter]

        if "priority" in filters:
            priority_filter = filters["priority"]
            if isinstance(priority_filter, str):
                filtered = [t for t in filtered if t.priority.value == priority_filter]
            elif isinstance(priority_filter, list):
                filtered = [t for t in filtered if t.priority.value in priority_filter]

        if "task_type" in filters:
            type_filter = filters["task_type"]
            if isinstance(type_filter, str):
                filtered = [t for t in filtered if t.task_type.value == type_filter]
            elif isinstance(type_filter, list):
                filtered = [t for t in filtered if t.task_type.value in type_filter]

        return filtered

    # === MEETING INTELLIGENCE ===

    def detect_meetings_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        AI-powered meeting detection in content
        Consolidates functionality from MeetingIntelligence

        Args:
            content: Text content to analyze
            context: Context information (file_path, category, etc.)

        Returns:
            List of detected meeting candidates with analysis
        """
        try:
            # Use cache for performance if available
            if self.enable_performance:
                cache_key = f"meeting_detection:{hash(content[:100])}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Enhanced AI detection logic
            candidates = self._analyze_content_for_meetings(content, context)

            # Cache results
            if self.enable_performance and candidates:
                self.cache_manager.set(cache_key, candidates, ttl=7200)  # 2 hour cache

            return candidates

        except Exception as e:
            raise AIDetectionError(
                f"Meeting detection failed: {e}", detection_type="meeting"
            )

    def _analyze_content_for_meetings(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze content for meeting patterns and extract intelligence"""
        import re

        meeting_indicators = [
            "meeting",
            "standup",
            "sync",
            "review",
            "planning",
            "retrospective",
            "agenda",
            "attendees",
            "participants",
            "discussion",
            "minutes",
        ]

        content_lower = content.lower()

        # Check if content likely contains meeting information
        if not any(indicator in content_lower for indicator in meeting_indicators):
            return []

        # Extract meeting details
        meeting_data = {
            "title": self._extract_meeting_title(content),
            "meeting_type": self._classify_meeting_type(content),
            "participants": self._extract_participants(content),
            "agenda_items": self._extract_agenda_items(content),
            "decisions_made": self._extract_decisions(content),
            "action_items": self._extract_action_items(content),
            "key_topics": self._extract_key_topics(content),
            "strategic_importance": self._calculate_meeting_importance(content),
            "sentiment_score": self._analyze_meeting_sentiment(content),
            "collaboration_score": self._analyze_collaboration_quality(content),
            "source_document": context.get("file_path", ""),
            "confidence": 0.8 if "agenda" in content_lower else 0.6,
        }

        return [meeting_data] if meeting_data["title"] else []

    def _extract_meeting_title(self, content: str) -> str:
        """Extract meeting title from content"""
        lines = content.split("\n")

        # Look for title patterns
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not line.startswith("#") and len(line) < 100:
                # Skip obvious non-titles
                if not any(
                    skip in line.lower()
                    for skip in ["date:", "time:", "attendees:", "agenda:"]
                ):
                    return line

        return "Meeting"  # Fallback

    def _classify_meeting_type(self, content: str) -> str:
        """Classify meeting type based on content"""
        content_lower = content.lower()

        type_indicators = {
            "strategic": ["strategic", "vision", "roadmap", "planning"],
            "executive": ["executive", "leadership", "board", "ceo", "vp"],
            "standup": ["standup", "daily", "scrum", "sprint"],
            "review": ["review", "retrospective", "demo", "showcase"],
            "decision": ["decision", "approve", "vote", "consensus"],
            "stakeholder": ["stakeholder", "client", "customer", "partner"],
        }

        for meeting_type, indicators in type_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return meeting_type

        return "operational"  # Default

    def _extract_participants(self, content: str) -> List[str]:
        """Extract participant names from content"""
        import re

        participants = []

        # Look for attendees sections
        attendees_patterns = [
            r"attendees?[:\-\s]*([^\n]+)",
            r"participants?[:\-\s]*([^\n]+)",
            r"present[:\-\s]*([^\n]+)",
        ]

        for pattern in attendees_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                names = re.split(r"[,;|&]|\sand\s", match)
                for name in names:
                    name = name.strip()
                    if len(name) > 2 and len(name) < 50:
                        participants.append(name)

        return list(set(participants))  # Remove duplicates

    def _extract_agenda_items(self, content: str) -> List[str]:
        """Extract agenda items from content"""
        import re

        agenda_items = []

        # Look for agenda sections
        agenda_patterns = [
            r"agenda[:\-\s]*\n([^\n]+(?:\n[^\n]+)*)",
            r"topics?[:\-\s]*\n([^\n]+(?:\n[^\n]+)*)",
            r"discussion points?[:\-\s]*\n([^\n]+(?:\n[^\n]+)*)",
        ]

        for pattern in agenda_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                lines = match.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove bullet points and numbering
                        cleaned = re.sub(r"^[\-\*\+\d\.\)]\s*", "", line)
                        if len(cleaned) > 5:
                            agenda_items.append(cleaned)

        return agenda_items[:10]  # Limit to 10 items

    def _extract_decisions(self, content: str) -> List[str]:
        """Extract decisions made from content"""
        import re

        decisions = []

        decision_patterns = [
            r"decision[s]?[:\-\s]*([^\n]+)",
            r"decided[:\-\s]*([^\n]+)",
            r"agreed[:\-\s]*([^\n]+)",
            r"concluded[:\-\s]*([^\n]+)",
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                decision = match.strip()
                if len(decision) > 5:
                    decisions.append(decision)

        return decisions[:5]  # Limit to 5 decisions

    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items from meeting content"""
        # Reuse task detection logic
        context = {"category": "meeting_analysis"}
        task_candidates = self._analyze_content_for_tasks(content, context)

        action_items = []
        for candidate in task_candidates:
            if candidate["task_type"] == "action_item":
                action_items.append(candidate["description"])

        return action_items[:8]  # Limit to 8 action items

    def _extract_key_topics(self, content: str) -> List[str]:
        """Extract key topics discussed"""
        # Simple keyword extraction - can be enhanced with NLP
        words = content.lower().split()

        # Common business/technical terms
        topic_keywords = [
            "platform",
            "architecture",
            "strategy",
            "roadmap",
            "budget",
            "hiring",
            "performance",
            "security",
            "compliance",
            "metrics",
            "goals",
            "objectives",
            "launch",
            "release",
            "deployment",
            "migration",
            "refactor",
            "optimization",
        ]

        found_topics = []
        for keyword in topic_keywords:
            if keyword in words:
                found_topics.append(keyword.title())

        return found_topics[:6]  # Limit to 6 topics

    def _calculate_meeting_importance(self, content: str) -> float:
        """Calculate strategic importance of meeting (0.0 to 1.0)"""
        importance_terms = [
            "strategic",
            "critical",
            "executive",
            "board",
            "decision",
            "budget",
            "roadmap",
            "launch",
            "architecture",
            "transformation",
        ]

        content_lower = content.lower()
        term_count = sum(1 for term in importance_terms if term in content_lower)

        # Base score plus boost for importance terms
        score = 0.4 + min(0.5, term_count * 0.1)

        return min(1.0, score)

    def _analyze_meeting_sentiment(self, content: str) -> float:
        """Analyze meeting sentiment (-1.0 to 1.0)"""
        # Simple sentiment analysis - can be enhanced with NLP libraries
        positive_words = [
            "good",
            "great",
            "excellent",
            "success",
            "progress",
            "agree",
            "positive",
        ]
        negative_words = [
            "bad",
            "poor",
            "problem",
            "issue",
            "concern",
            "risk",
            "negative",
            "disagree",
        ]

        content_lower = content.lower()
        words = content_lower.split()

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        if positive_count + negative_count == 0:
            return 0.0  # Neutral

        sentiment = (positive_count - negative_count) / (
            positive_count + negative_count
        )
        return max(-1.0, min(1.0, sentiment))

    def _analyze_collaboration_quality(self, content: str) -> float:
        """Analyze collaboration quality (0.0 to 1.0)"""
        collaboration_indicators = [
            "agree",
            "consensus",
            "together",
            "collaborate",
            "team",
            "support",
            "shared",
            "aligned",
            "partnership",
            "cooperation",
        ]

        conflict_indicators = [
            "disagree",
            "conflict",
            "argument",
            "tension",
            "oppose",
            "resist",
            "block",
            "concern",
            "issue",
            "problem",
        ]

        content_lower = content.lower()

        collaboration_score = sum(
            1 for indicator in collaboration_indicators if indicator in content_lower
        )
        conflict_score = sum(
            1 for indicator in conflict_indicators if indicator in content_lower
        )

        # Calculate collaboration quality
        if collaboration_score + conflict_score == 0:
            return 0.5  # Neutral

        quality = collaboration_score / (collaboration_score + conflict_score)
        return max(0.0, min(1.0, quality))

    # === SYSTEM MANAGEMENT ===

    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive intelligence system statistics"""
        stats = {
            "total_tasks": len(self.tasks),
            "total_meetings": len(self.meetings),
            "performance_enabled": self.enable_performance,
            "stakeholder_intelligence_available": STAKEHOLDER_INTELLIGENCE_AVAILABLE,
            "strategic_memory_available": STRATEGIC_MEMORY_AVAILABLE,
            "last_updated": time.time(),
        }

        # Task statistics
        if self.tasks:
            task_list = list(self.tasks.values())
            stats["task_stats"] = {
                "by_status": self._count_by_field(task_list, "status"),
                "by_priority": self._count_by_field(task_list, "priority"),
                "by_type": self._count_by_field(task_list, "task_type"),
                "avg_importance": sum(t.strategic_importance for t in task_list)
                / len(task_list),
            }

        # Meeting statistics
        if self.meetings:
            meeting_list = list(self.meetings.values())
            stats["meeting_stats"] = {
                "by_type": self._count_by_field(meeting_list, "meeting_type"),
                "avg_importance": sum(m.strategic_importance for m in meeting_list)
                / len(meeting_list),
                "avg_sentiment": sum(m.sentiment_score for m in meeting_list)
                / len(meeting_list),
                "avg_collaboration": sum(m.collaboration_score for m in meeting_list)
                / len(meeting_list),
            }

        # Performance stats if available
        if self.enable_performance and PERFORMANCE_AVAILABLE:
            try:
                stats["performance_stats"] = {
                    "cache_stats": (
                        self.cache_manager.get_stats()
                        if hasattr(self.cache_manager, "get_stats")
                        else {}
                    ),
                    "memory_stats": (
                        self.memory_optimizer.get_memory_stats()
                        if hasattr(self.memory_optimizer, "get_memory_stats")
                        else {}
                    ),
                }
            except Exception as e:
                stats["performance_error"] = str(e)

        return stats

    def _count_by_field(self, items: List, field: str) -> Dict[str, int]:
        """Count items by enum field value"""
        counts = {}
        for item in items:
            field_value = getattr(item, field)
            value = (
                field_value.value if hasattr(field_value, "value") else str(field_value)
            )
            counts[value] = counts.get(value, 0) + 1
        return counts


# === BACKWARD COMPATIBILITY API ===


def get_intelligence_unified(
    config: Optional[Dict[str, Any]] = None, enable_performance: bool = True
) -> IntelligenceUnified:
    """Get unified intelligence instance"""
    return IntelligenceUnified(config=config, enable_performance=enable_performance)


# Legacy compatibility classes for migration period
class TaskIntelligence(IntelligenceUnified):
    """Legacy compatibility wrapper for TaskIntelligence"""

    def __init__(
        self,
        config=None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
    ):
        super().__init__(config, enable_performance)

    def detect_tasks_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return super().detect_tasks_in_content(content, context)

    def add_task(self, task_key: str, task_data: Dict[str, Any]) -> bool:
        task_data["task_id"] = task_key
        return super().add_task(task_data)

    def get_task(self, task_key: str) -> Optional[Dict[str, Any]]:
        task = super().get_task(task_key)
        return task.to_dict() if task else None

    def list_tasks(
        self, filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return super().list_tasks(filter_by)


class MeetingIntelligence(IntelligenceUnified):
    """Legacy compatibility wrapper for MeetingIntelligence"""

    def __init__(
        self,
        config=None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
    ):
        super().__init__(config, enable_performance)

    def detect_meetings_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return super().detect_meetings_in_content(content, context)

    def add_meeting(self, meeting_key: str, meeting_data: Dict[str, Any]) -> bool:
        meeting_data["meeting_id"] = meeting_key
        # Convert to MeetingProfile and store
        try:
            current_time = time.time()
            meeting = MeetingProfile(
                meeting_id=meeting_key,
                title=meeting_data.get("title", ""),
                meeting_type=MeetingType(
                    meeting_data.get("meeting_type", "operational")
                ),
                date=meeting_data.get("date", ""),
                duration_minutes=meeting_data.get("duration_minutes", 60),
                organizer=meeting_data.get("organizer", ""),
                participants=meeting_data.get("participants", []),
                stakeholders_involved=meeting_data.get("stakeholders_involved", []),
                agenda_items=meeting_data.get("agenda_items", []),
                decisions_made=meeting_data.get("decisions_made", []),
                action_items=meeting_data.get("action_items", []),
                key_topics=meeting_data.get("key_topics", []),
                strategic_importance=meeting_data.get("strategic_importance", 0.5),
                sentiment_score=meeting_data.get("sentiment_score", 0.0),
                conflict_indicators=meeting_data.get("conflict_indicators", []),
                collaboration_score=meeting_data.get("collaboration_score", 0.5),
                source_document=meeting_data.get("source_document", ""),
                related_initiatives=meeting_data.get("related_initiatives", []),
                created_timestamp=current_time,
                updated_timestamp=current_time,
            )
            self.meetings[meeting_key] = meeting
            return True
        except Exception as e:
            self.logger.error(f"Failed to add meeting: {e}")
            return False

    def get_meeting(self, meeting_key: str) -> Optional[Dict[str, Any]]:
        meeting = self.meetings.get(meeting_key)
        return meeting.to_dict() if meeting else None

    def list_meetings(
        self, filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            meetings = list(self.meetings.values())

            # Apply basic filters
            if filter_by:
                if "meeting_type" in filter_by:
                    type_filter = filter_by["meeting_type"]
                    meetings = [
                        m for m in meetings if m.meeting_type.value == type_filter
                    ]

            return [m.to_dict() for m in meetings]
        except Exception as e:
            self.logger.error(f"Failed to list meetings: {e}")
            return []


# Export for legacy StakeholderIntelligence compatibility
# (References Phase 2.1 consolidation)
def StakeholderIntelligence(*args, **kwargs):
    """Legacy compatibility - redirect to Phase 2.1 stakeholder consolidation"""
    if STAKEHOLDER_INTELLIGENCE_AVAILABLE:
        return get_stakeholder_intelligence()
    else:
        raise ImportError(
            "StakeholderIntelligence migrated to context_engineering - use stakeholder_intelligence_unified"
        )
