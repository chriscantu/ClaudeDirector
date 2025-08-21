"""
Smart File Organizer for ClaudeDirector Phase 2
Intelligent file consolidation, outcome-focused naming, and pattern recognition
"""

import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, Counter

from .file_lifecycle_manager import FileLifecycleManager, FileMetadata, FileRetentionStatus
from .advanced_archiving import AdvancedArchivingSystem
from .pattern_recognition import PatternRecognitionEngine

@dataclass
class SessionPattern:
    """Detected pattern in user's strategic sessions"""
    pattern_type: str  # "weekly_planning", "quarterly_review", "stakeholder_meeting", etc.
    frequency: str     # "weekly", "monthly", "quarterly", "ad_hoc"
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
    consolidation_type: str  # "session_summary", "quarterly_package", "stakeholder_package"
    priority: str  # "high", "medium", "low"
    size_reduction: float  # Estimated cognitive load reduction

class SmartFileOrganizer:
    """Phase 2: Intelligent file organization and consolidation"""

    def __init__(self, lifecycle_manager: FileLifecycleManager):
        self.lifecycle_manager = lifecycle_manager
        self.workspace_path = Path(lifecycle_manager.workspace_path)
        self.patterns_file = self.workspace_path / ".claudedirector" / "session_patterns.json"
        self.insights_file = self.workspace_path / ".claudedirector" / "cross_session_insights.json"

        # Initialize advanced archiving system
        self.advanced_archiving = AdvancedArchivingSystem(str(self.workspace_path))

        # Initialize pattern recognition engine
        self.pattern_engine = PatternRecognitionEngine(str(self.workspace_path))

        # Load existing patterns and insights
        self.session_patterns = self._load_session_patterns()
        self.cross_session_insights = self._load_cross_session_insights()

        # Business context keywords for outcome-focused naming
        self.business_contexts = {
            "platform": ["platform", "infrastructure", "architecture", "scaling"],
            "team": ["team", "hiring", "org", "structure", "performance"],
            "strategy": ["strategy", "roadmap", "vision", "planning", "objectives"],
            "stakeholder": ["stakeholder", "executive", "board", "leadership", "communication"],
            "budget": ["budget", "cost", "roi", "investment", "financial"],
            "quarterly": ["q1", "q2", "q3", "q4", "quarterly", "okr", "goals"],
            "technical": ["technical", "debt", "migration", "upgrade", "implementation"],
            "process": ["process", "workflow", "methodology", "framework", "adoption"]
        }

    def _load_session_patterns(self) -> List[SessionPattern]:
        """Load detected session patterns"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    data = json.load(f)
                return [SessionPattern(**item) for item in data]
            except Exception:
                return []
        return []

    def _save_session_patterns(self):
        """Save session patterns to file"""
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_file, 'w') as f:
            data = [vars(pattern) for pattern in self.session_patterns]
            json.dump(data, f, indent=2)

    def _load_cross_session_insights(self) -> Dict[str, Any]:
        """Load cross-session insights"""
        if self.insights_file.exists():
            try:
                with open(self.insights_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cross_session_insights(self):
        """Save cross-session insights"""
        self.insights_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.insights_file, 'w') as f:
            json.dump(self.cross_session_insights, f, indent=2)

    def generate_outcome_focused_filename(
        self,
        content_preview: str,
        content_type: str,
        business_context: str,
        persona: Optional[str] = None
    ) -> str:
        """Generate filename based on business outcome rather than technical type"""

        # Extract business context from content
        detected_contexts = self._detect_business_contexts(content_preview + " " + business_context)

        # Determine primary business outcome
        primary_outcome = self._determine_primary_outcome(detected_contexts, content_type)

        # Generate time-based component
        timestamp = datetime.now()
        quarter = f"Q{(timestamp.month - 1) // 3 + 1}"
        date_str = timestamp.strftime("%Y-%m-%d")

        # Build outcome-focused filename
        filename_parts = []

        # Add quarter for strategic content
        if primary_outcome in ["strategy", "quarterly", "budget"]:
            filename_parts.append(quarter.lower())

        # Add primary business outcome
        filename_parts.append(primary_outcome)

        # Add specific context if detected
        if detected_contexts:
            specific_context = self._extract_specific_context(content_preview, detected_contexts)
            if specific_context:
                filename_parts.append(specific_context)

        # Add persona context for clarity
        if persona and persona in ["alvaro", "rachel", "diego", "camille"]:
            persona_context = {
                "alvaro": "strategy",
                "rachel": "ux",
                "diego": "engineering",
                "camille": "technology"
            }
            if persona_context[persona] not in filename_parts:
                filename_parts.append(persona_context[persona])

        # Add date
        filename_parts.append(date_str)

        # Construct final filename
        base_name = "-".join(filename_parts)
        return f"{base_name}.md"

    def _detect_business_contexts(self, text: str) -> List[str]:
        """Detect business contexts in text content"""
        text_lower = text.lower()
        detected = []

        for context, keywords in self.business_contexts.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(context)

        return detected

    def _determine_primary_outcome(self, contexts: List[str], content_type: str) -> str:
        """Determine primary business outcome from contexts"""

        # Priority mapping for business outcomes
        priority_map = {
            "quarterly": 10,
            "strategy": 9,
            "stakeholder": 8,
            "budget": 7,
            "platform": 6,
            "team": 5,
            "technical": 4,
            "process": 3
        }

        # Find highest priority context
        if contexts:
            primary = max(contexts, key=lambda x: priority_map.get(x, 0))
            return primary

        # Fallback based on content type
        content_type_mapping = {
            "strategic_analysis": "analysis",
            "meeting_prep": "meeting",
            "executive_presentation": "presentation",
            "quarterly_planning": "planning",
            "framework_research": "research",
            "session_summary": "summary"
        }

        return content_type_mapping.get(content_type, "document")

    def _extract_specific_context(self, text: str, contexts: List[str]) -> Optional[str]:
        """Extract specific context details from text"""
        text_lower = text.lower()

        # Platform-specific extractions
        if "platform" in contexts:
            platform_terms = ["migration", "scaling", "architecture", "infrastructure"]
            for term in platform_terms:
                if term in text_lower:
                    return term

        # Team-specific extractions
        if "team" in contexts:
            team_terms = ["hiring", "performance", "structure", "growth"]
            for term in team_terms:
                if term in text_lower:
                    return term

        # Extract specific initiatives or projects
        initiative_patterns = [
            r"initiative[:\s]+([a-zA-Z\-]+)",
            r"project[:\s]+([a-zA-Z\-]+)",
            r"epic[:\s]+([a-zA-Z\-]+)"
        ]

        for pattern in initiative_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).replace(" ", "-")

        return None

    def identify_consolidation_opportunities(self) -> List[ConsolidationOpportunity]:
        """Identify opportunities for file consolidation"""
        opportunities = []

        # Get files from last 7 days for session-based consolidation
        recent_files = self._get_recent_files(days=7)

        # Group files by potential consolidation patterns
        session_groups = self._group_files_by_session(recent_files)
        context_groups = self._group_files_by_business_context(recent_files)
        temporal_groups = self._group_files_by_time_period(recent_files)

        # Analyze each group for consolidation opportunities
        opportunities.extend(self._analyze_session_groups(session_groups))
        opportunities.extend(self._analyze_context_groups(context_groups))
        opportunities.extend(self._analyze_temporal_groups(temporal_groups))

        # Sort by priority and potential impact
        opportunities.sort(key=lambda x: (
            {"high": 3, "medium": 2, "low": 1}[x.priority],
            x.size_reduction
        ), reverse=True)

        return opportunities

    def _get_recent_files(self, days: int = 7) -> List[Tuple[str, FileMetadata]]:
        """Get files created within the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_files = []

        for filepath, metadata in self.lifecycle_manager.metadata_store.items():
            if (metadata.created_at > cutoff_date and
                metadata.retention_status != FileRetentionStatus.ARCHIVED and
                Path(filepath).exists()):
                recent_files.append((filepath, metadata))

        return recent_files

    def _group_files_by_session(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, List[Tuple[str, FileMetadata]]]:
        """Group files by session ID"""
        groups = defaultdict(list)

        for filepath, metadata in files:
            session_id = metadata.session_id or "no_session"
            groups[session_id].append((filepath, metadata))

        # Only return groups with multiple files
        return {k: v for k, v in groups.items() if len(v) > 1}

    def _group_files_by_business_context(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, List[Tuple[str, FileMetadata]]]:
        """Group files by detected business context"""
        groups = defaultdict(list)

        for filepath, metadata in files:
            # Read file content to detect context
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                contexts = self._detect_business_contexts(content)
                primary_context = contexts[0] if contexts else "general"
                groups[primary_context].append((filepath, metadata))

            except Exception:
                groups["general"].append((filepath, metadata))

        return {k: v for k, v in groups.items() if len(v) > 1}

    def _group_files_by_time_period(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, List[Tuple[str, FileMetadata]]]:
        """Group files by time period (daily, weekly)"""
        groups = defaultdict(list)

        for filepath, metadata in files:
            # Group by day
            day_key = metadata.created_at.strftime("%Y-%m-%d")
            groups[f"daily_{day_key}"].append((filepath, metadata))

            # Group by week
            week_start = metadata.created_at - timedelta(days=metadata.created_at.weekday())
            week_key = week_start.strftime("%Y-W%U")
            groups[f"weekly_{week_key}"].append((filepath, metadata))

        return {k: v for k, v in groups.items() if len(v) > 2}

    def _analyze_session_groups(self, groups: Dict[str, List[Tuple[str, FileMetadata]]]) -> List[ConsolidationOpportunity]:
        """Analyze session groups for consolidation opportunities"""
        opportunities = []

        for session_id, files in groups.items():
            if len(files) >= 3:  # Consolidate sessions with 3+ files
                file_paths = [f[0] for f in files]

                # Determine business context
                content_types = [f[1].content_type for f in files]
                business_value = self._determine_session_business_value(files)

                suggested_name = f"session-summary-{session_id}-{datetime.now().strftime('%Y-%m-%d')}.md"

                opportunity = ConsolidationOpportunity(
                    files=file_paths,
                    suggested_name=suggested_name,
                    business_value=business_value,
                    consolidation_type="session_summary",
                    priority="high",
                    size_reduction=len(files) * 0.7  # Estimated cognitive load reduction
                )
                opportunities.append(opportunity)

        return opportunities

    def _analyze_context_groups(self, groups: Dict[str, List[Tuple[str, FileMetadata]]]) -> List[ConsolidationOpportunity]:
        """Analyze business context groups for consolidation"""
        opportunities = []

        for context, files in groups.items():
            if len(files) >= 2 and context != "general":
                file_paths = [f[0] for f in files]

                suggested_name = f"{context}-analysis-{datetime.now().strftime('%Y-%m-%d')}.md"
                business_value = f"Consolidated {context} strategic analysis"

                opportunity = ConsolidationOpportunity(
                    files=file_paths,
                    suggested_name=suggested_name,
                    business_value=business_value,
                    consolidation_type="context_package",
                    priority="medium",
                    size_reduction=len(files) * 0.5
                )
                opportunities.append(opportunity)

        return opportunities

    def _analyze_temporal_groups(self, groups: Dict[str, List[Tuple[str, FileMetadata]]]) -> List[ConsolidationOpportunity]:
        """Analyze temporal groups for consolidation"""
        opportunities = []

        for period_key, files in groups.items():
            if len(files) >= 4:  # Only consolidate if 4+ files in period
                file_paths = [f[0] for f in files]

                if period_key.startswith("weekly_"):
                    suggested_name = f"weekly-summary-{period_key.split('_')[1]}.md"
                    business_value = "Weekly strategic activities summary"
                    consolidation_type = "weekly_package"
                    priority = "medium"
                elif period_key.startswith("daily_"):
                    suggested_name = f"daily-summary-{period_key.split('_')[1]}.md"
                    business_value = "Daily strategic session summary"
                    consolidation_type = "daily_package"
                    priority = "low"
                else:
                    continue

                opportunity = ConsolidationOpportunity(
                    files=file_paths,
                    suggested_name=suggested_name,
                    business_value=business_value,
                    consolidation_type=consolidation_type,
                    priority=priority,
                    size_reduction=len(files) * 0.4
                )
                opportunities.append(opportunity)

        return opportunities

    def _determine_session_business_value(self, files: List[Tuple[str, FileMetadata]]) -> str:
        """Determine business value of a session based on files"""
        content_types = [f[1].content_type for f in files]

        if "executive_presentation" in content_types:
            return "Executive stakeholder communication package"
        elif "quarterly_planning" in content_types:
            return "Quarterly strategic planning session"
        elif "meeting_prep" in content_types:
            return "Strategic meeting preparation package"
        else:
            return "Strategic analysis session summary"

    def consolidate_files(
        self,
        opportunity: ConsolidationOpportunity,
        user_approved: bool = True
    ) -> Optional[str]:
        """Consolidate files based on opportunity"""

        if not user_approved:
            return None

        try:
            # Create consolidated content
            consolidated_content = self._create_consolidated_content(opportunity)

            # Determine target directory
            target_dir = self.workspace_path / "analysis-results"
            target_dir.mkdir(parents=True, exist_ok=True)

            # Create consolidated file
            consolidated_path = target_dir / opportunity.suggested_name

            with open(consolidated_path, 'w', encoding='utf-8') as f:
                f.write(consolidated_content)

            # Register with lifecycle manager
            self.lifecycle_manager.register_file(
                str(consolidated_path),
                "session_summary",
                session_id=f"consolidated_{datetime.now().strftime('%Y%m%d')}"
            )

            # Archive original files with enhanced indexing
            for file_path in opportunity.files:
                # Get metadata for enhanced archiving
                metadata = self.lifecycle_manager.metadata_store.get(file_path)
                content_type = metadata.content_type if metadata else "strategic_analysis"
                session_id = metadata.session_id if metadata else None

                # Use advanced archiving system
                self.advanced_archiving.archive_file_with_indexing(
                    file_path, content_type, session_id
                )

            print(f"✅ Consolidated {len(opportunity.files)} files → {opportunity.suggested_name}")
            print(f"🎯 Business value: {opportunity.business_value}")

            return str(consolidated_path)

        except Exception as e:
            print(f"⚠️ Consolidation failed: {e}")
            return None

    def _create_consolidated_content(self, opportunity: ConsolidationOpportunity) -> str:
        """Create consolidated content from multiple files"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        content = f"""# {opportunity.business_value}
*Consolidated: {timestamp}*
*Files: {len(opportunity.files)}*
*Type: {opportunity.consolidation_type}*

---

## 📋 Executive Summary

[Consolidated insights from {len(opportunity.files)} strategic documents]

---

## 📊 Strategic Analysis

"""

        # Process each file and extract key content
        for i, file_path in enumerate(opportunity.files, 1):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                filename = Path(file_path).name
                content += f"\n### {i}. {filename}\n\n"

                # Extract key sections from the file
                key_sections = self._extract_key_sections(file_content)
                content += key_sections + "\n\n---\n"

            except Exception as e:
                content += f"\n### {i}. {Path(file_path).name}\n\n*[Error reading file: {e}]*\n\n---\n"

        content += f"""
## 🚀 Consolidated Action Items

[Strategic action items across all analyzed areas]

## 🎯 Key Success Metrics

[Measurable outcomes and success indicators]

---

*This document consolidates insights from {len(opportunity.files)} strategic files for enhanced leadership perspective.*
"""

        return content

    def _extract_key_sections(self, content: str) -> str:
        """Extract key sections from file content"""
        lines = content.split('\n')
        key_content = []

        # Look for important sections
        important_markers = [
            "# ", "## ", "### ",  # Headers
            "**", "*", "- ",     # Formatting
            "action", "decision", "recommendation",  # Key terms
            "risk", "opportunity", "next steps"
        ]

        for line in lines:
            line_lower = line.lower()
            if any(marker in line_lower for marker in important_markers):
                key_content.append(line)
            elif line.strip() and not line.startswith('---'):
                # Include non-empty, non-separator lines
                key_content.append(line)

        # Return first 10 lines of key content
        return '\n'.join(key_content[:10])

    def suggest_consolidation_opportunities(self) -> bool:
        """Proactively suggest consolidation opportunities to user"""
        opportunities = self.identify_consolidation_opportunities()

        if not opportunities:
            return False

        print(f"\n💡 **Smart Organization Opportunities Found**")
        print(f"📊 Identified {len(opportunities)} consolidation opportunities")

        for i, opp in enumerate(opportunities[:3], 1):  # Show top 3
            print(f"\n{i}. **{opp.consolidation_type.replace('_', ' ').title()}**")
            print(f"   Files: {len(opp.files)}")
            print(f"   Business Value: {opp.business_value}")
            print(f"   Priority: {opp.priority}")
            print(f"   Cognitive Load Reduction: {opp.size_reduction:.1f}x")

        response = input(f"\nProceed with smart consolidation? [y/n/details]: ").strip().lower()

        if response == 'y':
            return self._execute_consolidation_batch(opportunities[:3])
        elif response == 'details':
            return self._show_detailed_opportunities(opportunities)

        return False

    def _execute_consolidation_batch(self, opportunities: List[ConsolidationOpportunity]) -> bool:
        """Execute a batch of consolidation opportunities"""
        consolidated_count = 0

        for opp in opportunities:
            print(f"\n📦 Consolidating: {opp.business_value}")
            result = self.consolidate_files(opp, user_approved=True)
            if result:
                consolidated_count += 1

        if consolidated_count > 0:
            print(f"\n🎉 Successfully consolidated {consolidated_count} file groups!")
            print(f"🧠 Reduced cognitive load and improved organization")
            return True

        return False

    def _show_detailed_opportunities(self, opportunities: List[ConsolidationOpportunity]) -> bool:
        """Show detailed consolidation opportunities"""
        for i, opp in enumerate(opportunities, 1):
            print(f"\n📋 **Opportunity {i}: {opp.business_value}**")
            print(f"Type: {opp.consolidation_type}")
            print(f"Priority: {opp.priority}")
            print(f"Files to consolidate ({len(opp.files)}):")

            for file_path in opp.files:
                filename = Path(file_path).name
                print(f"  - {filename}")

            print(f"Suggested name: {opp.suggested_name}")

            response = input(f"Consolidate this group? [y/n/skip]: ").strip().lower()

            if response == 'y':
                result = self.consolidate_files(opp, user_approved=True)
                if result:
                    print(f"✅ Consolidated successfully!")
            elif response == 'skip':
                continue
            else:
                print(f"Skipped consolidation")

        return True

    def search_archived_files(self, query: str, limit: int = 10) -> List[Any]:
        """Search archived files using advanced search capabilities"""
        return self.advanced_archiving.search_archived_files(query, limit)

    def get_pattern_insights(self) -> Dict[str, Any]:
        """Get insights about user patterns and workflow optimization"""
        return self.pattern_engine.get_pattern_insights()

    def suggest_workflow_optimizations(self) -> List[str]:
        """Suggest workflow optimizations based on detected patterns"""
        patterns = self.pattern_engine.workflow_patterns
        return self.pattern_engine.suggest_workflow_optimizations(patterns)

    def get_archive_statistics(self) -> Dict[str, Any]:
        """Get statistics about archived files"""
        return self.advanced_archiving.get_archive_statistics()

    def generate_cross_session_insights(self) -> Dict[str, Any]:
        """Generate insights across multiple sessions"""

        # Get recent files for analysis
        recent_files = self._get_recent_files(days=30)

        insights = {
            "productivity_trends": self._analyze_productivity_trends(recent_files),
            "content_type_evolution": self._analyze_content_evolution(recent_files),
            "business_context_focus": self._analyze_business_focus(recent_files),
            "workflow_efficiency": self._analyze_workflow_efficiency(recent_files),
            "pattern_recommendations": self.suggest_workflow_optimizations()
        }

        # Update cross-session insights
        self.cross_session_insights.update(insights)
        self._save_cross_session_insights()

        return insights

    def _analyze_productivity_trends(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, Any]:
        """Analyze productivity trends over time"""

        # Group files by week
        weekly_counts = defaultdict(int)
        for filepath, metadata in files:
            week_key = metadata.created_at.strftime('%Y-W%U')
            weekly_counts[week_key] += 1

        # Calculate trend
        weeks = sorted(weekly_counts.keys())
        if len(weeks) >= 2:
            recent_avg = sum(weekly_counts[w] for w in weeks[-2:]) / 2
            earlier_avg = sum(weekly_counts[w] for w in weeks[:-2]) / max(1, len(weeks) - 2)
            trend = "increasing" if recent_avg > earlier_avg else "stable" if recent_avg == earlier_avg else "decreasing"
        else:
            trend = "insufficient_data"

        return {
            "weekly_file_counts": dict(weekly_counts),
            "trend": trend,
            "total_files_30_days": len(files),
            "average_files_per_week": sum(weekly_counts.values()) / max(1, len(weekly_counts))
        }

    def _analyze_content_evolution(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, Any]:
        """Analyze how content types evolve over time"""

        # Group by content type and time
        content_evolution = defaultdict(lambda: defaultdict(int))

        for filepath, metadata in files:
            month_key = metadata.created_at.strftime('%Y-%m')
            content_evolution[metadata.content_type][month_key] += 1

        # Find trends in content types
        trends = {}
        for content_type, monthly_counts in content_evolution.items():
            months = sorted(monthly_counts.keys())
            if len(months) >= 2:
                recent = monthly_counts[months[-1]]
                earlier = sum(monthly_counts[m] for m in months[:-1]) / max(1, len(months) - 1)
                if recent > earlier * 1.2:
                    trends[content_type] = "increasing"
                elif recent < earlier * 0.8:
                    trends[content_type] = "decreasing"
                else:
                    trends[content_type] = "stable"

        return {
            "content_type_evolution": dict(content_evolution),
            "content_trends": trends,
            "dominant_content_type": max(
                Counter(m.content_type for _, m in files).items(),
                key=lambda x: x[1]
            )[0] if files else None
        }

    def _analyze_business_focus(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, Any]:
        """Analyze business context focus areas"""

        # Extract business contexts from filenames and content
        business_contexts = []
        for filepath, metadata in files:
            filename = Path(filepath).name
            contexts = self._detect_business_contexts(filename)
            business_contexts.extend(contexts)

        # Analyze focus areas
        context_counter = Counter(business_contexts)

        return {
            "top_business_contexts": dict(context_counter.most_common(5)),
            "primary_focus": context_counter.most_common(1)[0][0] if context_counter else None,
            "focus_diversity": len(set(business_contexts)),
            "context_distribution": dict(context_counter)
        }

    def _analyze_workflow_efficiency(self, files: List[Tuple[str, FileMetadata]]) -> Dict[str, Any]:
        """Analyze workflow efficiency metrics"""

        # Group by session to analyze session efficiency
        session_groups = defaultdict(list)
        for filepath, metadata in files:
            session_id = metadata.session_id or "no_session"
            session_groups[session_id].append((filepath, metadata))

        # Calculate efficiency metrics
        session_sizes = [len(files) for files in session_groups.values()]
        avg_session_size = sum(session_sizes) / len(session_sizes) if session_sizes else 0

        # Analyze consolidation opportunities
        opportunities = self.identify_consolidation_opportunities()
        total_reduction = sum(opp.size_reduction for opp in opportunities)

        return {
            "average_session_size": avg_session_size,
            "total_sessions": len(session_groups),
            "consolidation_opportunities": len(opportunities),
            "potential_efficiency_gain": total_reduction,
            "workflow_score": min(10, max(1, 10 - (avg_session_size - 3)))  # Optimal around 3 files per session
        }

    def detect_session_patterns(self):
        """Detect patterns in user's strategic sessions for future optimization"""
        recent_files = self._get_recent_files(days=30)

        # Analyze content types by session
        session_analysis = defaultdict(list)

        for filepath, metadata in recent_files:
            session_id = metadata.session_id or "no_session"
            session_analysis[session_id].append({
                'content_type': metadata.content_type,
                'filename': Path(filepath).name,
                'created_at': metadata.created_at,
                'business_context': self._detect_business_contexts(Path(filepath).name)
            })

        # Update patterns based on analysis
        self._update_session_patterns(session_analysis)
        self._save_session_patterns()

    def _update_session_patterns(self, session_analysis: Dict[str, List[Dict]]):
        """Update detected session patterns"""
        # Analyze patterns and update self.session_patterns
        # This is a placeholder for more sophisticated pattern detection

        pattern_candidates = []

        for session_id, files in session_analysis.items():
            if len(files) >= 2:
                content_types = [f['content_type'] for f in files]
                business_contexts = []
                for f in files:
                    business_contexts.extend(f.get('business_context', []))

                # Detect pattern type
                if 'quarterly_planning' in content_types:
                    pattern_type = 'quarterly_review'
                    frequency = 'quarterly'
                elif 'meeting_prep' in content_types:
                    pattern_type = 'stakeholder_meeting'
                    frequency = 'weekly'
                else:
                    pattern_type = 'strategic_analysis'
                    frequency = 'ad_hoc'

                pattern = SessionPattern(
                    pattern_type=pattern_type,
                    frequency=frequency,
                    content_types=list(set(content_types)),
                    naming_pattern=f"{pattern_type}_{frequency}",
                    business_context=', '.join(set(business_contexts)) if business_contexts else 'general',
                    confidence_score=min(len(files) / 5.0, 1.0)  # Confidence based on file count
                )

                pattern_candidates.append(pattern)

        # Update session patterns (simple replacement for now)
        self.session_patterns = pattern_candidates

        # Update pattern recognition engine with new data
        session_data = []
        for session_id, files in session_analysis.items():
            for file_info in files:
                session_data.append({
                    'session_id': session_id,
                    'content_type': file_info['content_type'],
                    'created_at': file_info['created_at'].isoformat(),
                    'business_context': ', '.join(file_info.get('business_context', []))
                })

        self.pattern_engine.update_patterns_from_usage(session_data)
