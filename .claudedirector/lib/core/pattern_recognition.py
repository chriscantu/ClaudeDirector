"""
Pattern Recognition System for ClaudeDirector Phase 2
Identifies user patterns and suggests templates and workflows
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

@dataclass
class WorkflowPattern:
    """Detected workflow pattern"""
    pattern_id: str
    pattern_name: str
    trigger_contexts: List[str]  # What contexts trigger this pattern
    typical_sequence: List[str]  # Typical file sequence
    frequency: str  # "daily", "weekly", "monthly", "quarterly"
    confidence: float
    business_value: str
    template_suggestion: str

@dataclass
class TemplateRecommendation:
    """Template recommendation based on patterns"""
    template_name: str
    context: str
    content_types: List[str]
    expected_outcome: str
    confidence: float
    usage_frequency: str

class PatternRecognitionEngine:
    """Recognizes patterns in user behavior and suggests optimizations"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.patterns_db = self.workspace_path / ".claudedirector" / "workflow_patterns.json"
        self.templates_db = self.workspace_path / ".claudedirector" / "template_recommendations.json"

        # Load existing patterns
        self.workflow_patterns = self._load_workflow_patterns()
        self.template_recommendations = self._load_template_recommendations()

        # Pattern detection thresholds
        self.min_pattern_occurrences = 3
        self.min_confidence_threshold = 0.7

    def _load_workflow_patterns(self) -> List[WorkflowPattern]:
        """Load detected workflow patterns"""
        if self.patterns_db.exists():
            try:
                with open(self.patterns_db, 'r') as f:
                    data = json.load(f)
                return [WorkflowPattern(**item) for item in data]
            except Exception:
                return []
        return []

    def _save_workflow_patterns(self) -> None:
        """Save workflow patterns"""
        self.patterns_db.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_db, 'w') as f:
            data = [asdict(pattern) for pattern in self.workflow_patterns]
            json.dump(data, f, indent=2)

    def _load_template_recommendations(self) -> List[TemplateRecommendation]:
        """Load template recommendations"""
        if self.templates_db.exists():
            try:
                with open(self.templates_db, 'r') as f:
                    data = json.load(f)
                return [TemplateRecommendation(**item) for item in data]
            except Exception:
                return []
        return []

    def _save_template_recommendations(self) -> None:
        """Save template recommendations"""
        self.templates_db.parent.mkdir(parents=True, exist_ok=True)
        with open(self.templates_db, 'w') as f:
            data = [asdict(rec) for rec in self.template_recommendations]
            json.dump(data, f, indent=2)

    def analyze_user_patterns(self, session_data: List[Dict[str, Any]]) -> List[WorkflowPattern]:
        """Analyze user behavior to identify patterns"""

        # Group sessions by time patterns
        daily_patterns = self._analyze_daily_patterns(session_data)
        weekly_patterns = self._analyze_weekly_patterns(session_data)
        monthly_patterns = self._analyze_monthly_patterns(session_data)

        # Detect content sequence patterns
        sequence_patterns = self._analyze_content_sequences(session_data)

        # Combine all detected patterns
        all_patterns = []
        all_patterns.extend(daily_patterns)
        all_patterns.extend(weekly_patterns)
        all_patterns.extend(monthly_patterns)
        all_patterns.extend(sequence_patterns)

        # Filter by confidence threshold
        high_confidence_patterns = [
            p for p in all_patterns
            if p.confidence >= self.min_confidence_threshold
        ]

        return high_confidence_patterns

    def _analyze_daily_patterns(self, session_data: List[Dict[str, Any]]) -> List[WorkflowPattern]:
        """Analyze daily workflow patterns"""
        patterns = []

        # Group by day of week
        daily_sessions = defaultdict(list)
        for session in session_data:
            session_date = datetime.fromisoformat(session['created_at'])
            day_of_week = session_date.strftime('%A')
            daily_sessions[day_of_week].append(session)

        # Analyze each day's patterns
        for day, sessions in daily_sessions.items():
            if len(sessions) >= self.min_pattern_occurrences:

                # Analyze content types for this day
                content_types = [s['content_type'] for s in sessions]
                content_counter = Counter(content_types)

                # Look for consistent patterns
                if content_counter.most_common(1)[0][1] >= 2:  # At least 2 occurrences
                    dominant_type = content_counter.most_common(1)[0][0]
                    confidence = content_counter[dominant_type] / len(sessions)

                    pattern = WorkflowPattern(
                        pattern_id=f"daily_{day.lower()}_{dominant_type}",
                        pattern_name=f"{day} {dominant_type.replace('_', ' ').title()}",
                        trigger_contexts=[day.lower(), dominant_type],
                        typical_sequence=[dominant_type],
                        frequency="weekly",
                        confidence=confidence,
                        business_value=f"Regular {day} {dominant_type.replace('_', ' ')} workflow",
                        template_suggestion=f"{day}_{dominant_type}_template"
                    )
                    patterns.append(pattern)

        return patterns

    def _analyze_weekly_patterns(self, session_data: List[Dict[str, Any]]) -> List[WorkflowPattern]:
        """Analyze weekly workflow patterns"""
        patterns = []

        # Group by week
        weekly_sessions = defaultdict(list)
        for session in session_data:
            session_date = datetime.fromisoformat(session['created_at'])
            week_key = session_date.strftime('%Y-W%U')
            weekly_sessions[week_key].append(session)

        # Look for weekly sequences
        for week, sessions in weekly_sessions.items():
            if len(sessions) >= 3:  # Minimum for weekly pattern

                # Analyze sequence of content types
                sequence = [s['content_type'] for s in sessions]

                # Look for common weekly sequences
                if 'meeting_prep' in sequence and 'strategic_analysis' in sequence:
                    pattern = WorkflowPattern(
                        pattern_id=f"weekly_planning_sequence",
                        pattern_name="Weekly Strategic Planning Sequence",
                        trigger_contexts=["weekly", "planning"],
                        typical_sequence=["meeting_prep", "strategic_analysis", "session_summary"],
                        frequency="weekly",
                        confidence=0.8,
                        business_value="Consistent weekly strategic planning workflow",
                        template_suggestion="weekly_planning_template"
                    )
                    patterns.append(pattern)

        return patterns

    def _analyze_monthly_patterns(self, session_data: List[Dict[str, Any]]) -> List[WorkflowPattern]:
        """Analyze monthly/quarterly patterns"""
        patterns = []

        # Look for quarterly planning patterns
        quarterly_sessions = []
        for session in session_data:
            if 'quarterly' in session.get('business_context', '').lower():
                quarterly_sessions.append(session)

        if len(quarterly_sessions) >= 2:
            pattern = WorkflowPattern(
                pattern_id="quarterly_planning_cycle",
                pattern_name="Quarterly Planning Cycle",
                trigger_contexts=["quarterly", "planning"],
                typical_sequence=["strategic_analysis", "quarterly_planning", "executive_presentation"],
                frequency="quarterly",
                confidence=0.9,
                business_value="Quarterly strategic planning and executive communication",
                template_suggestion="quarterly_cycle_template"
            )
            patterns.append(pattern)

        return patterns

    def _analyze_content_sequences(self, session_data: List[Dict[str, Any]]) -> List[WorkflowPattern]:
        """Analyze common content type sequences"""
        patterns = []

        # Group sessions by day to find sequences
        daily_sequences = defaultdict(list)
        for session in session_data:
            session_date = datetime.fromisoformat(session['created_at']).date()
            daily_sequences[session_date].append(session['content_type'])

        # Analyze common sequences
        sequence_counter: Counter[Tuple[str, ...]] = Counter()
        for date, sequence in daily_sequences.items():
            if len(sequence) >= 2:
                # Create sequence tuples
                for i in range(len(sequence) - 1):
                    seq_tuple: Tuple[str, ...] = tuple(sequence[i:i+2])
                    sequence_counter[seq_tuple] += 1

        # Identify frequent sequences
        for sequence, count in sequence_counter.items():
            if count >= self.min_pattern_occurrences:
                confidence = min(count / 10.0, 1.0)  # Normalize confidence

                pattern = WorkflowPattern(
                    pattern_id=f"sequence_{'_'.join(sequence)}",
                    pattern_name=f"{sequence[0].title()} → {sequence[1].title()} Workflow",
                    trigger_contexts=list(sequence),
                    typical_sequence=list(sequence),
                    frequency="regular",
                    confidence=confidence,
                    business_value=f"Common {' to '.join(sequence)} workflow",
                    template_suggestion=f"{'_'.join(sequence)}_template"
                )
                patterns.append(pattern)

        return patterns

    def generate_template_recommendations(self, patterns: List[WorkflowPattern]) -> List[TemplateRecommendation]:
        """Generate template recommendations based on detected patterns"""
        recommendations = []

        for pattern in patterns:
            # Generate template based on pattern
            template_rec = self._create_template_recommendation(pattern)
            if template_rec:
                recommendations.append(template_rec)

        return recommendations

    def _create_template_recommendation(self, pattern: WorkflowPattern) -> Optional[TemplateRecommendation]:
        """Create template recommendation from workflow pattern"""

        # Template mapping based on pattern types
        template_mappings = {
            "weekly_planning_sequence": {
                "name": "Weekly Strategic Planning Template",
                "context": "Weekly planning and review cycle",
                "outcome": "Structured weekly strategic planning with consistent format",
                "content_types": ["meeting_prep", "strategic_analysis", "session_summary"]
            },
            "quarterly_planning_cycle": {
                "name": "Quarterly Planning & Executive Communication Template",
                "context": "Quarterly strategic planning and stakeholder communication",
                "outcome": "Comprehensive quarterly planning with executive presentation ready",
                "content_types": ["strategic_analysis", "quarterly_planning", "executive_presentation"]
            },
            "daily_monday_meeting_prep": {
                "name": "Monday Meeting Preparation Template",
                "context": "Monday leadership meeting preparation",
                "outcome": "Consistent Monday meeting preparation with key talking points",
                "content_types": ["meeting_prep"]
            }
        }

        # Find matching template
        template_info = None
        for pattern_key, template_data in template_mappings.items():
            if pattern_key in pattern.pattern_id:
                template_info = template_data
                break

        if template_info:
            return TemplateRecommendation(
                template_name=template_info["name"],
                context=template_info["context"],
                content_types=template_info["content_types"],
                expected_outcome=template_info["outcome"],
                confidence=pattern.confidence,
                usage_frequency=pattern.frequency
            )

        return None

    def suggest_workflow_optimizations(self, patterns: List[WorkflowPattern]) -> List[str]:
        """Suggest workflow optimizations based on patterns"""
        suggestions = []

        for pattern in patterns:
            if pattern.confidence > 0.8:
                if pattern.frequency == "weekly":
                    suggestions.append(
                        f"💡 **Weekly Optimization**: Create a '{pattern.pattern_name}' template to streamline your {pattern.frequency} workflow"
                    )
                elif pattern.frequency == "quarterly":
                    suggestions.append(
                        f"🎯 **Quarterly Optimization**: Develop a '{pattern.pattern_name}' framework for consistent quarterly planning"
                    )
                elif "sequence" in pattern.pattern_id:
                    suggestions.append(
                        f"⚡ **Workflow Optimization**: Automate the {' → '.join(pattern.typical_sequence)} sequence with a combined template"
                    )

        # Add general suggestions based on pattern analysis
        if len(patterns) >= 3:
            suggestions.append(
                "📊 **Pattern Recognition**: Your workflow shows strong patterns. Consider creating custom templates for your most common sequences."
            )

        return suggestions

    def update_patterns_from_usage(self, session_data: List[Dict[str, Any]]) -> None:
        """Update patterns based on recent usage data"""

        # Analyze new patterns
        new_patterns = self.analyze_user_patterns(session_data)

        # Merge with existing patterns
        existing_pattern_ids = {p.pattern_id for p in self.workflow_patterns}

        for new_pattern in new_patterns:
            if new_pattern.pattern_id not in existing_pattern_ids:
                self.workflow_patterns.append(new_pattern)
            else:
                # Update existing pattern confidence
                for i, existing_pattern in enumerate(self.workflow_patterns):
                    if existing_pattern.pattern_id == new_pattern.pattern_id:
                        # Average confidence over time
                        self.workflow_patterns[i].confidence = (
                            existing_pattern.confidence + new_pattern.confidence
                        ) / 2

        # Update template recommendations
        new_recommendations = self.generate_template_recommendations(self.workflow_patterns)
        self.template_recommendations = new_recommendations

        # Save updated patterns
        self._save_workflow_patterns()
        self._save_template_recommendations()

    def get_pattern_insights(self) -> Dict[str, Any]:
        """Get insights about detected patterns"""
        insights = {
            "total_patterns": len(self.workflow_patterns),
            "high_confidence_patterns": len([p for p in self.workflow_patterns if p.confidence > 0.8]),
            "pattern_frequency_distribution": {},
            "top_patterns": [],
            "template_recommendations": len(self.template_recommendations)
        }

        # Frequency distribution
        freq_counter = Counter([p.frequency for p in self.workflow_patterns])
        insights["pattern_frequency_distribution"] = dict(freq_counter)

        # Top patterns by confidence
        top_patterns = sorted(self.workflow_patterns, key=lambda x: x.confidence, reverse=True)[:5]
        insights["top_patterns"] = [
            {
                "name": p.pattern_name,
                "confidence": p.confidence,
                "frequency": p.frequency,
                "business_value": p.business_value
            }
            for p in top_patterns
        ]

        return insights
