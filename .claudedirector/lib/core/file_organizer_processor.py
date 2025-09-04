"""
File Organizer Processor - Sequential Thinking Phase 5.2.6

🏗️ DRY Principle Consolidation: All smart file organizer logic consolidated into single processor.
Eliminates duplicate code patterns across SmartFileOrganizer class (~640 lines of complex logic).

This processor consolidates from smart_file_organizer.py:
- Session patterns management (_load_session_patterns, _save_session_patterns ~30 lines)
- File analysis and grouping logic (_group_files_* methods ~120 lines)
- Consolidation analysis workflows (_analyze_*_groups methods ~150 lines)
- Business context detection and processing (_detect_business_contexts, _determine_primary_outcome ~80 lines)
- Cross-session insights and analytics (generate_cross_session_insights, _analyze_* trends ~120 lines)
- File consolidation execution (consolidate_files, _create_consolidated_content ~80 lines)
- Pattern recognition and optimization (detect_session_patterns, suggest_workflow_optimizations ~60 lines)

Following proven Sequential Thinking patterns from Story 5.2.1, 5.2.2, 5.2.3, 5.2.4, 5.2.5 success.
Author: Martin | Platform Architecture with DRY principle enforcement
"""

import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, Counter

# Import essential components for file organization processing
try:
    from .file_lifecycle_manager import (
        FileLifecycleManager,
        FileMetadata,
        FileRetentionStatus,
    )
    from .advanced_archiving import AdvancedArchivingSystem
    from .pattern_recognition import PatternRecognitionEngine
except ImportError:
    # Lightweight fallback stubs following OVERVIEW.md patterns
    class FileLifecycleManager:
        def __init__(self, workspace_path):
            self.workspace_path = workspace_path
            self.metadata_store = {}

    class FileMetadata:
        def __init__(self):
            self.created_at = datetime.now()
            self.retention_status = None

    class FileRetentionStatus:
        ARCHIVED = "archived"

    class AdvancedArchivingSystem:
        def __init__(self, workspace_path):
            pass

    class PatternRecognitionEngine:
        def __init__(self, workspace_path):
            pass


# File organization model classes
@dataclass
class SessionPattern:
    """Detected pattern in user's strategic sessions"""

    pattern_type: (
        str  # "weekly_planning", "quarterly_review", "stakeholder_meeting", etc.
    )
    frequency: str  # "weekly", "monthly", "quarterly", "ad_hoc"
    content_types: List[str]
    naming_pattern: str
    business_context: str
    confidence_score: float


@dataclass
class ConsolidationOpportunity:
    """Identified opportunity for file consolidation"""

    files: List[str]
    suggested_name: str
    business_value: str
    consolidation_type: (
        str  # "session_summary", "quarterly_package", "stakeholder_package"
    )
    priority: str  # "high", "medium", "low"
    size_reduction: float  # Estimated cognitive load reduction


class FileOrganizerProcessor:
    """
    🏗️ CONSOLIDATED FILE ORGANIZATION PROCESSING ENGINE

    Sequential Thinking Phase 5.2.6 - DRY Principle Implementation
    Consolidates all smart file organizer logic into single, reusable processor.

    ELIMINATES DUPLICATE PATTERNS:
    - Session patterns management scattered across load/save methods
    - File analysis and grouping logic repeated across multiple grouping methods
    - Consolidation analysis workflows duplicated in different analysis contexts
    - Business context detection patterns repeated across organization logic
    - Cross-session insights and analytics spread across multiple trend analysis methods
    - File consolidation execution logic scattered across consolidation workflows
    - Pattern recognition optimization duplicated across pattern methods
    """

    def __init__(self, lifecycle_manager: FileLifecycleManager):
        """Initialize consolidated file organizer processor with dependencies"""
        self.lifecycle_manager = lifecycle_manager
        self.workspace_path = Path(lifecycle_manager.workspace_path)

        # File paths for persistence
        self.patterns_file = (
            self.workspace_path / ".claudedirector" / "session_patterns.json"
        )
        self.insights_file = (
            self.workspace_path / ".claudedirector" / "cross_session_insights.json"
        )

        # Initialize advanced systems
        self.advanced_archiving = AdvancedArchivingSystem(str(self.workspace_path))
        self.pattern_engine = PatternRecognitionEngine(str(self.workspace_path))

        # Load existing data
        self.session_patterns = self._load_session_patterns()
        self.cross_session_insights = self._load_cross_session_insights()

        # Consolidated business context configuration
        self.business_contexts = self._initialize_business_contexts()

    def _initialize_business_contexts(self) -> Dict[str, List[str]]:
        """
        🎯 CONSOLIDATED: Business context configuration (was scattered across methods)
        Single source of truth for all business context keywords and patterns
        """
        return {
            "platform": ["platform", "infrastructure", "architecture", "scaling"],
            "team": ["team", "hiring", "org", "structure", "performance"],
            "strategy": ["strategy", "roadmap", "vision", "planning", "objectives"],
            "stakeholder": [
                "stakeholder",
                "executive",
                "board",
                "leadership",
                "communication",
            ],
            "budget": ["budget", "cost", "roi", "investment", "financial"],
            "quarterly": ["q1", "q2", "q3", "q4", "quarterly", "okr", "goals"],
            "technical": [
                "technical",
                "debt",
                "migration",
                "upgrade",
                "implementation",
            ],
            "process": ["process", "workflow", "methodology", "framework", "adoption"],
        }

    def _load_session_patterns(self) -> List[SessionPattern]:
        """
        🎯 CONSOLIDATED: Session patterns loading (was scattered across 30+ lines)
        Single method for all session pattern persistence with consistent error handling
        """
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r") as f:
                    data = json.load(f)
                return [SessionPattern(**item) for item in data]
            except Exception:
                return []
        return []

    def _save_session_patterns(self):
        """
        🎯 CONSOLIDATED: Session patterns saving (unified persistence logic)
        Single method for all session pattern persistence with consistent structure
        """
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_file, "w") as f:
            data = [vars(pattern) for pattern in self.session_patterns]
            json.dump(data, f, indent=2)

    def _load_cross_session_insights(self) -> Dict[str, Any]:
        """
        🎯 CONSOLIDATED: Cross-session insights loading (unified data loading)
        Single method for loading insights with consistent error handling
        """
        if self.insights_file.exists():
            try:
                with open(self.insights_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cross_session_insights(self):
        """
        🎯 CONSOLIDATED: Cross-session insights saving (unified persistence)
        Single method for saving insights with consistent structure
        """
        self.insights_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.insights_file, "w") as f:
            json.dump(self.cross_session_insights, f, indent=2)

    def detect_business_contexts(self, text: str) -> List[str]:
        """
        🎯 CONSOLIDATED: Business context detection (was scattered across 80+ lines)
        Single method for all business context analysis with unified keyword matching
        """
        contexts = []
        text_lower = text.lower()

        for context_type, keywords in self.business_contexts.items():
            if any(keyword in text_lower for keyword in keywords):
                contexts.append(context_type)

        return contexts

    def determine_primary_outcome(self, contexts: List[str], content_type: str) -> str:
        """
        🎯 CONSOLIDATED: Primary outcome determination (was complex scattered logic)
        Single algorithm for determining primary outcomes from contexts
        """
        if not contexts:
            return "general"

        # Priority-based outcome determination
        outcome_priorities = {
            "strategy": 10,
            "quarterly": 9,
            "stakeholder": 8,
            "budget": 7,
            "platform": 6,
            "team": 5,
            "technical": 4,
            "process": 3,
        }

        # Find highest priority context
        prioritized_contexts = sorted(
            contexts, key=lambda c: outcome_priorities.get(c, 0), reverse=True
        )

        return prioritized_contexts[0] if prioritized_contexts else "general"

    def get_recent_files(self, days: int = 7) -> List[Tuple[str, FileMetadata]]:
        """
        🎯 CONSOLIDATED: Recent file retrieval (was scattered across file analysis)
        Single method for getting recent files with consistent filtering logic
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_files = []

        for filepath, metadata in self.lifecycle_manager.metadata_store.items():
            if (
                metadata.created_at > cutoff_date
                and metadata.retention_status != FileRetentionStatus.ARCHIVED
                and Path(filepath).exists()
            ):
                recent_files.append((filepath, metadata))

        return recent_files

    def group_files_by_session(
        self, files: List[Tuple[str, FileMetadata]]
    ) -> Dict[str, List[str]]:
        """
        🎯 CONSOLIDATED: Session-based file grouping (was scattered across 120+ lines)
        Single method for all session-based grouping with consistent logic
        """
        session_groups = defaultdict(list)

        for filepath, metadata in files:
            # Extract session indicators from filename and metadata
            filename = Path(filepath).stem.lower()

            # Group by date-based sessions
            date_str = metadata.created_at.strftime("%Y-%m-%d")

            # Look for meeting/session patterns
            if any(
                keyword in filename
                for keyword in ["meeting", "session", "standup", "review"]
            ):
                session_key = f"session_{date_str}"
            elif any(keyword in filename for keyword in ["weekly", "daily", "sprint"]):
                session_key = f"recurring_{date_str}"
            elif any(
                keyword in filename for keyword in ["quarterly", "q1", "q2", "q3", "q4"]
            ):
                session_key = f"quarterly_{metadata.created_at.strftime('%Y-Q%q')}"
            else:
                session_key = f"general_{date_str}"

            session_groups[session_key].append(filepath)

        # Filter groups with multiple files
        return {k: v for k, v in session_groups.items() if len(v) > 1}

    def group_files_by_business_context(
        self, files: List[Tuple[str, FileMetadata]]
    ) -> Dict[str, List[str]]:
        """
        🎯 CONSOLIDATED: Context-based file grouping (unified context analysis)
        Single method for grouping files by business context with consistent patterns
        """
        context_groups = defaultdict(list)

        for filepath, metadata in files:
            filename = Path(filepath).stem.lower()

            # Detect contexts in filename
            detected_contexts = self.detect_business_contexts(filename)

            if detected_contexts:
                # Use primary context for grouping
                primary_context = self.determine_primary_outcome(
                    detected_contexts, "file"
                )
                context_groups[primary_context].append(filepath)
            else:
                context_groups["general"].append(filepath)

        # Filter groups with multiple files
        return {k: v for k, v in context_groups.items() if len(v) > 1}

    def group_files_by_time_period(
        self, files: List[Tuple[str, FileMetadata]]
    ) -> Dict[str, List[str]]:
        """
        🎯 CONSOLIDATED: Time-based file grouping (unified temporal analysis)
        Single method for temporal grouping with consistent time period logic
        """
        temporal_groups = defaultdict(list)

        for filepath, metadata in files:
            # Group by week and month
            week_key = f"week_{metadata.created_at.strftime('%Y-W%U')}"
            month_key = f"month_{metadata.created_at.strftime('%Y-%m')}"

            temporal_groups[week_key].append(filepath)
            temporal_groups[month_key].append(filepath)

        # Filter groups with multiple files
        return {k: v for k, v in temporal_groups.items() if len(v) > 2}

    def analyze_session_groups(
        self, session_groups: Dict[str, List[str]]
    ) -> List[ConsolidationOpportunity]:
        """
        🎯 CONSOLIDATED: Session group analysis (was scattered across 150+ lines)
        Single method for analyzing session groups with unified opportunity detection
        """
        opportunities = []

        for session_key, files in session_groups.items():
            if len(files) < 2:
                continue

            # Analyze session business value
            business_value = self._determine_session_business_value(files)

            # Generate consolidation opportunity
            suggested_name = f"{session_key.replace('_', '-')}-summary"

            opportunity = ConsolidationOpportunity(
                files=files,
                suggested_name=suggested_name,
                business_value=business_value,
                consolidation_type="session_summary",
                priority="high" if len(files) > 3 else "medium",
                size_reduction=len(files)
                * 0.3,  # 30% cognitive load reduction per file
            )

            opportunities.append(opportunity)

        return opportunities

    def analyze_context_groups(
        self, context_groups: Dict[str, List[str]]
    ) -> List[ConsolidationOpportunity]:
        """
        🎯 CONSOLIDATED: Context group analysis (unified business context analysis)
        Single method for analyzing context groups with consistent priority logic
        """
        opportunities = []

        for context, files in context_groups.items():
            if len(files) < 2:
                continue

            # Context-specific business value
            context_values = {
                "strategy": "Strategic alignment and roadmap clarity",
                "stakeholder": "Stakeholder communication efficiency",
                "quarterly": "Quarterly review consolidation",
                "platform": "Platform architecture documentation",
                "team": "Team coordination and structure",
                "budget": "Financial planning consolidation",
            }

            business_value = context_values.get(context, "Organizational efficiency")
            suggested_name = f"{context}-package-{datetime.now().strftime('%Y-%m')}"

            opportunity = ConsolidationOpportunity(
                files=files,
                suggested_name=suggested_name,
                business_value=business_value,
                consolidation_type="context_package",
                priority="high" if context in ["strategy", "quarterly"] else "medium",
                size_reduction=len(files) * 0.25,  # 25% cognitive load reduction
            )

            opportunities.append(opportunity)

        return opportunities

    def analyze_temporal_groups(
        self, temporal_groups: Dict[str, List[str]]
    ) -> List[ConsolidationOpportunity]:
        """
        🎯 CONSOLIDATED: Temporal group analysis (unified time-based analysis)
        Single method for analyzing temporal groups with consistent time-based logic
        """
        opportunities = []

        for time_period, files in temporal_groups.items():
            if len(files) < 3:  # Require more files for temporal grouping
                continue

            business_value = "Temporal organization and archive preparation"
            suggested_name = f"archive-{time_period.replace('_', '-')}"

            opportunity = ConsolidationOpportunity(
                files=files,
                suggested_name=suggested_name,
                business_value=business_value,
                consolidation_type="temporal_archive",
                priority="low",
                size_reduction=len(files) * 0.2,  # 20% cognitive load reduction
            )

            opportunities.append(opportunity)

        return opportunities

    def identify_consolidation_opportunities(self) -> List[ConsolidationOpportunity]:
        """
        🎯 CONSOLIDATED: Consolidation opportunity identification (was complex orchestration)
        Single method orchestrating all consolidation analysis with unified prioritization
        """
        opportunities = []

        # Get recent files for analysis
        recent_files = self.get_recent_files(days=7)

        # Group files by different patterns
        session_groups = self.group_files_by_session(recent_files)
        context_groups = self.group_files_by_business_context(recent_files)
        temporal_groups = self.group_files_by_time_period(recent_files)

        # Analyze each group type
        opportunities.extend(self.analyze_session_groups(session_groups))
        opportunities.extend(self.analyze_context_groups(context_groups))
        opportunities.extend(self.analyze_temporal_groups(temporal_groups))

        # Sort by priority and impact
        opportunities.sort(
            key=lambda x: (
                {"high": 3, "medium": 2, "low": 1}[x.priority],
                x.size_reduction,
            ),
            reverse=True,
        )

        return opportunities

    def create_consolidated_content(
        self, files: List[str], consolidation_type: str
    ) -> str:
        """
        🎯 CONSOLIDATED: Content consolidation (was scattered across 80+ lines)
        Single method for creating consolidated content with consistent formatting
        """
        content_sections = []
        content_sections.append(f"# Consolidated {consolidation_type.title()}")
        content_sections.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        content_sections.append("=" * 50)

        for i, filepath in enumerate(files, 1):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    file_content = f.read()

                filename = Path(filepath).name
                content_sections.append(f"\n## Section {i}: {filename}")
                content_sections.append("-" * 30)

                # Extract key sections
                key_sections = self._extract_key_sections(file_content)
                content_sections.append(key_sections)

            except Exception as e:
                content_sections.append(f"\n## Section {i}: {Path(filepath).name}")
                content_sections.append(f"Error reading file: {str(e)}")

        content_sections.append(f"\n## Summary")
        content_sections.append(f"Consolidated {len(files)} files into single document")
        content_sections.append(f"Consolidation type: {consolidation_type}")

        return "\n".join(content_sections)

    def generate_cross_session_insights(self) -> Dict[str, Any]:
        """
        🎯 CONSOLIDATED: Cross-session insights generation (was scattered across 120+ lines)
        Single method for comprehensive insights analysis with unified analytics
        """
        insights = {}

        # Analyze productivity trends
        productivity_trends = self._analyze_productivity_trends()
        insights["productivity_trends"] = productivity_trends

        # Analyze content evolution
        content_evolution = self._analyze_content_evolution()
        insights["content_evolution"] = content_evolution

        # Analyze business focus
        business_focus = self._analyze_business_focus()
        insights["business_focus"] = business_focus

        # Analyze workflow efficiency
        workflow_efficiency = self._analyze_workflow_efficiency()
        insights["workflow_efficiency"] = workflow_efficiency

        # Update timestamp
        insights["last_updated"] = datetime.now().isoformat()
        insights["analysis_period"] = "last_30_days"

        return insights

    def detect_session_patterns(self):
        """
        🎯 CONSOLIDATED: Session pattern detection (unified pattern analysis)
        Single method for detecting patterns with consistent analysis logic
        """
        # Get recent files for pattern analysis
        recent_files = self.get_recent_files(days=30)

        # Analyze patterns
        session_analysis = {
            "weekly_patterns": [],
            "content_types": [],
            "business_contexts": [],
        }

        # Group by weeks to detect weekly patterns
        weekly_groups = defaultdict(list)
        for filepath, metadata in recent_files:
            week_key = metadata.created_at.strftime("%Y-W%U")
            weekly_groups[week_key].append((filepath, metadata))

        # Detect consistent weekly patterns
        for week, files in weekly_groups.items():
            if len(files) >= 3:  # Threshold for pattern detection
                contexts = []
                for filepath, _ in files:
                    filename_contexts = self.detect_business_contexts(
                        Path(filepath).stem
                    )
                    contexts.extend(filename_contexts)

                if contexts:
                    most_common_context = Counter(contexts).most_common(1)[0][0]
                    session_analysis["weekly_patterns"].append(
                        {
                            "week": week,
                            "file_count": len(files),
                            "primary_context": most_common_context,
                            "confidence": len(
                                [c for c in contexts if c == most_common_context]
                            )
                            / len(contexts),
                        }
                    )

        # Update session patterns
        self._update_session_patterns(session_analysis)

    # Helper methods (consolidated internal logic)
    def _determine_session_business_value(self, files: List[str]) -> str:
        """Determine business value of a session consolidation"""
        contexts = []
        for filepath in files:
            filename = Path(filepath).stem.lower()
            file_contexts = self.detect_business_contexts(filename)
            contexts.extend(file_contexts)

        if not contexts:
            return "General organizational efficiency"

        primary_context = Counter(contexts).most_common(1)[0][0]

        value_mapping = {
            "strategy": "Strategic clarity and decision alignment",
            "stakeholder": "Stakeholder communication consolidation",
            "quarterly": "Quarterly review efficiency",
            "platform": "Platform decision documentation",
            "team": "Team coordination improvement",
            "budget": "Financial planning consolidation",
        }

        return value_mapping.get(
            primary_context, "Organizational efficiency improvement"
        )

    def _extract_key_sections(self, content: str) -> str:
        """Extract key sections from file content"""
        # Simplified key section extraction
        lines = content.split("\n")
        key_lines = []

        for line in lines[:50]:  # First 50 lines
            line = line.strip()
            if line and not line.startswith("#"):
                # Include lines that look like key content
                if len(line) > 20 and any(
                    keyword in line.lower()
                    for keyword in [
                        "action",
                        "decision",
                        "outcome",
                        "next",
                        "follow",
                        "key",
                        "important",
                    ]
                ):
                    key_lines.append(line)

        return "\n".join(key_lines[:20])  # Top 20 key lines

    def _analyze_productivity_trends(self) -> Dict[str, Any]:
        """Analyze productivity trends from recent files"""
        recent_files = self.get_recent_files(days=30)

        # Group by weeks for trend analysis
        weekly_counts = defaultdict(int)
        for filepath, metadata in recent_files:
            week_key = metadata.created_at.strftime("%Y-W%U")
            weekly_counts[week_key] += 1

        # Calculate trend
        weeks = sorted(weekly_counts.keys())
        if len(weeks) >= 2:
            trend = (
                "increasing"
                if weekly_counts[weeks[-1]] > weekly_counts[weeks[0]]
                else "decreasing"
            )
        else:
            trend = "stable"

        return {
            "weekly_file_creation": dict(weekly_counts),
            "trend": trend,
            "average_files_per_week": sum(weekly_counts.values())
            / max(1, len(weekly_counts)),
        }

    def _analyze_content_evolution(self) -> Dict[str, Any]:
        """Analyze how content types and contexts evolve over time"""
        recent_files = self.get_recent_files(days=30)

        # Track context evolution
        context_timeline = []
        for filepath, metadata in recent_files:
            contexts = self.detect_business_contexts(Path(filepath).stem)
            if contexts:
                context_timeline.append(
                    {
                        "date": metadata.created_at.strftime("%Y-%m-%d"),
                        "contexts": contexts,
                    }
                )

        # Find most common contexts
        all_contexts = []
        for entry in context_timeline:
            all_contexts.extend(entry["contexts"])

        context_frequency = Counter(all_contexts)

        return {
            "context_timeline": context_timeline[-10:],  # Last 10 entries
            "top_contexts": dict(context_frequency.most_common(5)),
            "context_diversity": len(context_frequency),
        }

    def _analyze_business_focus(self) -> Dict[str, Any]:
        """Analyze current business focus areas"""
        recent_files = self.get_recent_files(days=14)  # Recent focus

        # Collect all contexts
        all_contexts = []
        for filepath, metadata in recent_files:
            contexts = self.detect_business_contexts(Path(filepath).stem)
            all_contexts.extend(contexts)

        if not all_contexts:
            return {"primary_focus": "general", "focus_areas": {}}

        context_counts = Counter(all_contexts)
        total_contexts = len(all_contexts)

        # Calculate focus percentages
        focus_areas = {
            context: {"count": count, "percentage": (count / total_contexts) * 100}
            for context, count in context_counts.items()
        }

        return {
            "primary_focus": context_counts.most_common(1)[0][0],
            "focus_areas": focus_areas,
            "focus_diversity_score": len(context_counts) / max(1, total_contexts),
        }

    def _analyze_workflow_efficiency(self) -> Dict[str, Any]:
        """Analyze workflow efficiency metrics"""
        recent_files = self.get_recent_files(days=30)

        # Calculate efficiency metrics
        total_files = len(recent_files)

        # Group by days to see daily patterns
        daily_counts = defaultdict(int)
        for filepath, metadata in recent_files:
            day_key = metadata.created_at.strftime("%Y-%m-%d")
            daily_counts[day_key] += 1

        # Calculate statistics
        daily_values = list(daily_counts.values())
        avg_daily_files = sum(daily_values) / max(1, len(daily_values))

        return {
            "total_files_30_days": total_files,
            "average_files_per_day": avg_daily_files,
            "active_days": len(daily_counts),
            "efficiency_score": min(
                1.0, avg_daily_files / 5.0
            ),  # Normalized to 5 files/day max
        }

    def _update_session_patterns(self, session_analysis: Dict[str, List[Dict]]):
        """Update session patterns based on analysis"""
        # Create new session patterns from analysis
        new_patterns = []

        for pattern_data in session_analysis.get("weekly_patterns", []):
            if pattern_data["confidence"] > 0.6:  # Confidence threshold
                pattern = SessionPattern(
                    pattern_type="weekly_pattern",
                    frequency="weekly",
                    content_types=["mixed"],
                    naming_pattern=f"{pattern_data['primary_context']}_weekly",
                    business_context=pattern_data["primary_context"],
                    confidence_score=pattern_data["confidence"],
                )
                new_patterns.append(pattern)

        # Update stored patterns (keep recent ones, add new ones)
        self.session_patterns.extend(new_patterns)

        # Keep only last 50 patterns to avoid infinite growth
        self.session_patterns = self.session_patterns[-50:]

        # Save updated patterns
        self._save_session_patterns()


# Factory function for backward compatibility
def create_file_organizer_processor(
    lifecycle_manager: FileLifecycleManager,
) -> FileOrganizerProcessor:
    """
    🏗️ Factory function for FileOrganizerProcessor creation
    Maintains backward compatibility while providing consolidated processing
    """
    return FileOrganizerProcessor(lifecycle_manager)
