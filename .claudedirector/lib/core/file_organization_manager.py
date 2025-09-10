"""
🎯 STORY 9.5.4: FILE ORGANIZATION MANAGER - PHASE 3 DECOMPOSITION

SOLID COMPLIANCE ACHIEVED:
- Single Responsibility: File organization and categorization only
- Open/Closed: Extensible through BaseManager inheritance
- Liskov Substitution: Proper BaseManager implementation
- Interface Segregation: Focused organization interface
- Dependency Inversion: Depends on BaseManager abstraction

EXTRACTED FROM: UnifiedFileManager (867 lines) → Specialized Manager (~200 lines)
ELIMINATES: SRP violations by focusing solely on organization operations

Sequential Thinking Phase 9.5.4 - Manager decomposition for SOLID compliance.
Author: Martin | Platform Architecture
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
from enum import Enum

# STORY 9.5.4: BaseManager inheritance for SOLID compliance
from .base_manager import BaseManager, BaseManagerConfig, ManagerType


class GenerationMode(Enum):
    """File generation modes for organization preferences"""

    MINIMAL = "minimal"  # Strategic analysis only, consolidated files
    PROFESSIONAL = "professional"  # + Meeting prep, quarterly organization
    RESEARCH = "research"  # + Framework docs, methodology materials


class FileOrganizationManager(BaseManager):
    """
    🎯 STORY 9.5.4: FILE ORGANIZATION MANAGER - SOLID Compliant

    SINGLE RESPONSIBILITY: File organization and categorization only
    - Workspace file organization by business context
    - Outcome-focused filename generation
    - Session pattern analysis and detection
    - Strategic file categorization and tagging

    ELIMINATES SRP VIOLATIONS from UnifiedFileManager mega-class.
    Focused interface for organization operations only.
    """

    def __init__(self, workspace_path: str, metadata_manager=None) -> None:
        """
        🎯 STORY 9.5.4: SOLID compliant initialization
        """
        # BaseManager initialization for infrastructure
        config = BaseManagerConfig(
            manager_name="file_organization_manager",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        self.workspace_path = Path(workspace_path)
        self.metadata_manager = metadata_manager  # Dependency injection

        # Business contexts for strategic file organization
        self.business_contexts = {
            "strategic_planning": ["strategy", "roadmap", "vision", "goals", "okr"],
            "team_management": ["team", "people", "1on1", "performance", "hiring"],
            "technical_architecture": ["architecture", "design", "technical", "system"],
            "product_development": ["product", "feature", "requirements", "specs"],
            "stakeholder_communication": [
                "meeting",
                "presentation",
                "communication",
                "update",
            ],
            "process_improvement": [
                "process",
                "workflow",
                "improvement",
                "optimization",
            ],
            "research_analysis": ["research", "analysis", "investigation", "study"],
        }

        self.logger.info(
            f"FileOrganizationManager initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Focused organization operation delegation
        """
        if operation == "organize_files":
            return self.organize_workspace_files(*args, **kwargs)
        elif operation == "generate_filename":
            return self.generate_outcome_focused_filename(*args, **kwargs)
        elif operation == "analyze_patterns":
            return self.analyze_session_patterns(*args, **kwargs)
        elif operation == "categorize_file":
            return self.categorize_file_by_context(*args, **kwargs)
        elif operation == "health_check":
            return self.organization_health_check()
        else:
            self.logger.warning(f"Unknown organization operation: {operation}")
            return None

    def organize_workspace_files(
        self, mode: GenerationMode = GenerationMode.PROFESSIONAL
    ) -> Dict[str, Any]:
        """
        🎯 STORY 9.5.4: Method Length Compliance - Decomposed from 85-line method

        Organize workspace files by business context and strategic value.
        """
        organization_results = {
            "files_organized": 0,
            "categories_created": 0,
            "business_contexts": {},
            "organization_actions": [],
        }

        try:
            # Phase 1: Analyze existing files
            files_by_context = self._analyze_files_by_context()

            # Phase 2: Create organization structure
            structure_created = self._create_organization_structure(
                files_by_context, mode
            )
            organization_results["categories_created"] = len(structure_created)

            # Phase 3: Move files to organized structure
            move_results = self._move_files_to_organized_structure(files_by_context)
            organization_results.update(move_results)

            # Phase 4: Update metadata with organization info
            self._update_organization_metadata(files_by_context)

            self.logger.info(
                f"Workspace organization completed: {organization_results}"
            )
            return organization_results

        except Exception as e:
            self.logger.error(f"Error during workspace organization: {e}")
            return organization_results

    def generate_outcome_focused_filename(
        self, content_summary: str, context: str = "", strategic_value: float = 0.0
    ) -> str:
        """Generate outcome-focused filename based on content and context"""
        try:
            # Extract key elements from content
            key_elements = self._extract_key_elements(content_summary)

            # Determine business context
            business_context = self._determine_business_context(
                content_summary, context
            )

            # Generate timestamp for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d")

            # Construct filename with strategic focus
            if strategic_value >= 7.0:
                prefix = "STRATEGIC"
            elif strategic_value >= 5.0:
                prefix = "HIGH_IMPACT"
            elif strategic_value >= 3.0:
                prefix = "OPERATIONAL"
            else:
                prefix = "TACTICAL"

            # Clean and format elements
            clean_elements = [
                self._clean_filename_element(elem) for elem in key_elements[:3]
            ]
            filename_parts = [
                prefix,
                business_context.upper(),
                timestamp,
            ] + clean_elements

            filename = "_".join(filter(None, filename_parts)) + ".md"

            self.logger.debug(f"Generated filename: {filename}")
            return filename

        except Exception as e:
            self.logger.error(f"Error generating filename: {e}")
            return f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    def analyze_session_patterns(self) -> Dict[str, Any]:
        """
        🎯 STORY 9.5.4: Method Length Compliance - Decomposed from 42-line method

        Analyze file creation patterns across sessions.
        """
        if not self.metadata_manager:
            return {"error": "No metadata manager available"}

        try:
            # Get all metadata for analysis
            metadata_store = self.metadata_manager.get_all_metadata()

            # Group files by session patterns
            session_groups = self._group_files_by_session(metadata_store)

            # Analyze patterns within sessions
            pattern_analysis = self._analyze_session_content_patterns(session_groups)

            # Generate session insights
            insights = self._generate_session_insights(pattern_analysis)

            results = {
                "total_sessions": len(session_groups),
                "patterns_detected": pattern_analysis,
                "session_insights": insights,
                "recommendations": self._generate_organization_recommendations(
                    insights
                ),
            }

            self.logger.info(
                f"Session pattern analysis completed: {len(session_groups)} sessions analyzed"
            )
            return results

        except Exception as e:
            self.logger.error(f"Error analyzing session patterns: {e}")
            return {"error": str(e)}

    def categorize_file_by_context(
        self, file_path: Path, content_hint: str = ""
    ) -> str:
        """Categorize file by business context"""
        try:
            # Use filename and content hint for categorization
            filename = file_path.name.lower()
            combined_text = f"{filename} {content_hint}".lower()

            # Score against business contexts
            context_scores = {}
            for context, keywords in self.business_contexts.items():
                score = sum(1 for keyword in keywords if keyword in combined_text)
                if score > 0:
                    context_scores[context] = score

            # Return highest scoring context or default
            if context_scores:
                best_context = max(context_scores.items(), key=lambda x: x[1])[0]
                self.logger.debug(f"Categorized {file_path} as {best_context}")
                return best_context

            return "general"

        except Exception as e:
            self.logger.error(f"Error categorizing file {file_path}: {e}")
            return "general"

    def organization_health_check(self) -> Dict[str, Any]:
        """Check organization health and suggest improvements"""
        health_report = {
            "organization_score": 0.0,
            "issues_detected": [],
            "recommendations": [],
            "file_distribution": {},
        }

        try:
            if not self.metadata_manager:
                health_report["issues_detected"].append("No metadata manager available")
                return health_report

            metadata_store = self.metadata_manager.get_all_metadata()

            # Analyze file distribution
            context_distribution = defaultdict(int)
            uncategorized_files = 0

            for file_path_str, metadata in metadata_store.items():
                context = metadata.get("business_context")
                if context:
                    context_distribution[context] += 1
                else:
                    uncategorized_files += 1

            health_report["file_distribution"] = dict(context_distribution)

            # Calculate organization score
            total_files = len(metadata_store)
            if total_files > 0:
                categorized_ratio = (total_files - uncategorized_files) / total_files
                balance_score = self._calculate_distribution_balance(
                    context_distribution
                )
                health_report["organization_score"] = (
                    categorized_ratio * 0.7 + balance_score * 0.3
                ) * 100

            # Generate recommendations
            if uncategorized_files > total_files * 0.2:
                health_report["recommendations"].append(
                    "Consider categorizing uncategorized files"
                )

            if len(context_distribution) < 3:
                health_report["recommendations"].append(
                    "Diversify business contexts for better organization"
                )

            return health_report

        except Exception as e:
            self.logger.error(f"Error in organization health check: {e}")
            health_report["issues_detected"].append(f"Health check error: {e}")
            return health_report

    # ===== PRIVATE HELPER METHODS =====

    def _analyze_files_by_context(self) -> Dict[str, List[Path]]:
        """Analyze files and group by business context"""
        files_by_context = defaultdict(list)

        for file_path in self.workspace_path.rglob("*.md"):
            if file_path.is_file():
                context = self.categorize_file_by_context(file_path)
                files_by_context[context].append(file_path)

        return dict(files_by_context)

    def _create_organization_structure(
        self, files_by_context: Dict[str, List[Path]], mode: GenerationMode
    ) -> List[Path]:
        """Create directory structure for organization"""
        created_dirs = []

        for context in files_by_context.keys():
            context_dir = self.workspace_path / "organized" / context
            if not context_dir.exists():
                context_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.append(context_dir)

        return created_dirs

    def _move_files_to_organized_structure(
        self, files_by_context: Dict[str, List[Path]]
    ) -> Dict[str, int]:
        """Move files to organized directory structure"""
        move_results = {"files_organized": 0, "organization_actions": []}

        for context, files in files_by_context.items():
            context_dir = self.workspace_path / "organized" / context

            for file_path in files:
                try:
                    new_path = context_dir / file_path.name
                    if not new_path.exists():
                        file_path.rename(new_path)
                        move_results["files_organized"] += 1
                        move_results["organization_actions"].append(
                            f"Moved {file_path.name} to {context}"
                        )
                except Exception as e:
                    self.logger.warning(f"Could not move {file_path}: {e}")

        return move_results

    def _update_organization_metadata(
        self, files_by_context: Dict[str, List[Path]]
    ) -> None:
        """Update metadata with organization information"""
        if not self.metadata_manager:
            return

        for context, files in files_by_context.items():
            for file_path in files:
                updates = {
                    "business_context": context,
                    "organized_at": datetime.now().isoformat(),
                }
                self.metadata_manager.update_file_metadata(file_path, updates)

    def _extract_key_elements(self, content_summary: str) -> List[str]:
        """Extract key elements from content for filename generation"""
        # Simple extraction - can be enhanced with NLP
        words = re.findall(r"\b\w+\b", content_summary.lower())
        # Filter out common words and keep meaningful terms
        stop_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }
        meaningful_words = [
            word for word in words if len(word) > 3 and word not in stop_words
        ]
        return meaningful_words[:5]  # Return top 5 elements

    def _determine_business_context(self, content: str, context_hint: str) -> str:
        """Determine business context from content and hint"""
        combined_text = f"{content} {context_hint}".lower()

        for context, keywords in self.business_contexts.items():
            if any(keyword in combined_text for keyword in keywords):
                return context

        return "general"

    def _clean_filename_element(self, element: str) -> str:
        """Clean element for filename usage"""
        # Remove special characters and limit length
        cleaned = re.sub(r"[^\w\-_]", "", element)
        return cleaned[:15] if cleaned else ""

    def _group_files_by_session(
        self, metadata_store: Dict[str, Dict]
    ) -> Dict[str, List[str]]:
        """Group files by session time windows"""
        sessions = defaultdict(list)

        for file_path_str, metadata in metadata_store.items():
            try:
                created_at = datetime.fromisoformat(metadata["created_at"])
                # Group by hour for session detection
                session_key = created_at.strftime("%Y%m%d_%H")
                sessions[session_key].append(file_path_str)
            except (KeyError, ValueError):
                continue

        return dict(sessions)

    def _analyze_session_content_patterns(
        self, session_groups: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Analyze content patterns within sessions"""
        patterns = {
            "common_contexts": Counter(),
            "session_sizes": [],
            "context_transitions": [],
        }

        for session_files in session_groups.values():
            patterns["session_sizes"].append(len(session_files))

            session_contexts = []
            for file_path_str in session_files:
                file_path = Path(file_path_str)
                context = self.categorize_file_by_context(file_path)
                session_contexts.append(context)
                patterns["common_contexts"][context] += 1

            # Track context transitions within session
            for i in range(len(session_contexts) - 1):
                transition = f"{session_contexts[i]} -> {session_contexts[i+1]}"
                patterns["context_transitions"].append(transition)

        return patterns

    def _generate_session_insights(self, pattern_analysis: Dict[str, Any]) -> List[str]:
        """Generate insights from session pattern analysis"""
        insights = []

        # Average session size insight
        if pattern_analysis["session_sizes"]:
            avg_size = sum(pattern_analysis["session_sizes"]) / len(
                pattern_analysis["session_sizes"]
            )
            insights.append(f"Average session creates {avg_size:.1f} files")

        # Most common context insight
        if pattern_analysis["common_contexts"]:
            top_context = pattern_analysis["common_contexts"].most_common(1)[0]
            insights.append(
                f"Most common context: {top_context[0]} ({top_context[1]} files)"
            )

        return insights

    def _generate_organization_recommendations(self, insights: List[str]) -> List[str]:
        """Generate organization recommendations based on insights"""
        recommendations = []

        for insight in insights:
            if "Average session creates" in insight:
                recommendations.append("Consider session-based organization templates")
            elif "Most common context" in insight:
                recommendations.append("Optimize workflow for most common context")

        return recommendations

    def _calculate_distribution_balance(
        self, context_distribution: Dict[str, int]
    ) -> float:
        """Calculate how balanced the file distribution is across contexts"""
        if not context_distribution:
            return 0.0

        values = list(context_distribution.values())
        if len(values) == 1:
            return 1.0

        # Calculate coefficient of variation (lower is more balanced)
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance**0.5
        cv = std_dev / mean_val if mean_val > 0 else 1.0

        # Convert to balance score (higher is more balanced)
        return max(0.0, 1.0 - cv)
