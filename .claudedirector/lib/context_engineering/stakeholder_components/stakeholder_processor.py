"""
Stakeholder Processor - Phase 3A.3.5 AGGRESSIVE CODE REDUCTION
Single Responsibility: Complete stakeholder processing including detection, content analysis, and relationships

Consolidated from over-engineered components:
- StakeholderDetectionEngine (167 lines) → Merged
- ContentProcessor (383 lines) → Merged
- RelationshipAnalyzer (478 lines) → Merged
Result: ~400 lines instead of 1,028 lines (60% reduction)

Author: Martin | Platform Architecture - DRY over SOLID ceremony
"""

import re
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import types
from ..stakeholder_intelligence_types import StakeholderProfile


class StakeholderProcessor:
    """
    Consolidated stakeholder processing engine

    Handles detection, content analysis, workspace processing, and relationship tracking
    in a single cohesive component focused on code reduction over fragmentation.
    """

    def __init__(
        self,
        repository=None,
        cache_manager=None,
        enable_performance: bool = True,
        interaction_retention_days: int = 365,
    ):
        """Initialize consolidated stakeholder processor"""
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.cache_manager = cache_manager
        self.enable_performance = enable_performance and cache_manager is not None
        self.interaction_retention_days = interaction_retention_days

        # Content processing configuration
        self.supported_extensions = {
            ".md",
            ".txt",
            ".py",
            ".js",
            ".ts",
            ".json",
            ".yaml",
            ".yml",
        }
        self.max_file_size = 1024 * 1024  # 1MB
        self.max_workers = 4

        # Detection patterns (consolidated from StakeholderDetectionEngine)
        self.executive_patterns = [
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:VP|CTO|Director|SVP|Chief)",
            r"\b(?:VP|CTO|Director|SVP|Chief)\s*([A-Z][a-z]+ [A-Z][a-z]+)",
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*leads?\s*(?:engineering|product|design)",
        ]

        self.role_indicators = {
            "engineering_manager": ["engineering manager", "eng manager", "team lead"],
            "product_manager": ["product manager", "pm", "product owner"],
            "designer": ["design lead", "ux lead", "ui designer"],
            "engineer": ["software engineer", "developer", "programmer"],
        }

        # In-memory storage for interactions
        self.interactions: List[Dict[str, Any]] = []

    # === STAKEHOLDER DETECTION (consolidated from StakeholderDetectionEngine) ===

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """AI-powered stakeholder detection in content"""
        try:
            # Use performance optimization if available
            if self.enable_performance:
                cache_key = f"stakeholder_detection:{hash(content)}:{hash(str(sorted(context.items())))}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            candidates = self._analyze_content_for_stakeholders(content, context)

            # Cache results
            if self.enable_performance and candidates:
                self.cache_manager.set(cache_key, candidates, ttl=7200)

            return candidates

        except Exception as e:
            self.logger.error(f"Stakeholder detection failed: {e}")
            return []

    def _analyze_content_for_stakeholders(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze content for stakeholder mentions and patterns"""
        candidates = []
        content_lower = content.lower()

        # Executive pattern detection
        for pattern in self.executive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                name = match if isinstance(match, str) else " ".join(match)
                if len(name.strip()) > 3:
                    candidates.append(
                        {
                            "name": name.strip(),
                            "role": "executive",
                            "confidence": 0.8,
                            "detection_method": "pattern_match",
                            "context": context.get("category", "general"),
                            "source_file": context.get("file_path", ""),
                            "influence_level": "high",
                        }
                    )

        # Role-based detection
        for role, indicators in self.role_indicators.items():
            for indicator in indicators:
                if indicator in content_lower:
                    role_pattern = rf"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:is|as|our|the)?\s*{re.escape(indicator)}"
                    matches = re.findall(role_pattern, content, re.IGNORECASE)
                    for name in matches:
                        if len(name.strip()) > 3:
                            candidates.append(
                                {
                                    "name": name.strip(),
                                    "role": role,
                                    "confidence": 0.6,
                                    "detection_method": "role_indicator",
                                    "context": context.get("category", "general"),
                                    "source_file": context.get("file_path", ""),
                                    "influence_level": "medium",
                                }
                            )

        # Remove duplicates and validate
        unique_candidates = []
        seen_names = set()
        for candidate in candidates:
            name_key = candidate["name"].lower().strip()
            if name_key not in seen_names and len(name_key) > 3:
                seen_names.add(name_key)
                unique_candidates.append(candidate)

        return unique_candidates[:10]  # Limit to top 10 candidates

    # === CONTENT PROCESSING (consolidated from ContentProcessor) ===

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any], auto_create: bool = True
    ) -> Dict[str, Any]:
        """Process content and automatically handle stakeholder detection and creation"""
        try:
            if not self.repository:
                self.logger.error("Repository required for content processing")
                return {"error": "Missing repository dependency"}

            # Detect stakeholder candidates (using consolidated detection)
            candidates = self.detect_stakeholders_in_content(content, context)
            candidates_detected = len(candidates)
            auto_created = 0
            profiling_needed = 0

            if auto_create:
                for candidate in candidates:
                    stakeholder_id = candidate["name"].lower().replace(" ", "_")
                    if not self.repository.get_stakeholder(stakeholder_id):
                        stakeholder_data = {
                            "name": candidate["name"],
                            "role": candidate["role"],
                            "influence_level": candidate.get(
                                "influence_level", "medium"
                            ),
                            "detection_confidence": candidate["confidence"],
                            "source_files": [context.get("file_path", "")],
                        }
                        if self.repository.add_stakeholder(
                            stakeholder_data,
                            source="ai_detection",
                            confidence=candidate["confidence"],
                        ):
                            auto_created += 1
                            if candidate["confidence"] > 0.7:
                                profiling_needed += 1

            return {
                "candidates_detected": candidates_detected,
                "auto_created": auto_created,
                "profiling_needed": profiling_needed,
                "candidates": candidates,
                "processing_timestamp": time.time(),
            }

        except Exception as e:
            self.logger.error(f"Content processing failed: {e}")
            return {"error": str(e)}

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process entire workspace for stakeholder detection with performance optimization"""
        try:
            workspace_dir = Path(workspace_path) if workspace_path else Path.cwd()

            # Find relevant files
            all_files = []
            for ext in [".md", ".txt"]:  # Focus on documentation files
                all_files.extend(workspace_dir.rglob(f"*{ext}"))

            relevant_files = [
                f for f in all_files if 10 < f.stat().st_size < self.max_file_size
            ]
            if not relevant_files:
                return {
                    "files_processed": 0,
                    "stakeholders_detected": 0,
                    "auto_created": 0,
                    "processing_time": 0.0,
                }

            # Process files with optimization
            if self.enable_performance and len(relevant_files) > 5:
                return self._process_files_parallel(relevant_files, workspace_dir)
            else:
                return self._process_files_sequential(relevant_files, workspace_dir)

        except Exception as e:
            self.logger.error(f"Workspace processing failed: {e}")
            return {"error": str(e)}

    def _process_files_parallel(
        self, files: List[Path], workspace_dir: Path
    ) -> Dict[str, Any]:
        """Process files using parallel processing"""
        start_time = time.time()
        total_stakeholders = total_auto_created = total_needs_profiling = (
            files_processed
        ) = 0

        def process_file(file_path: Path) -> Optional[Dict[str, Any]]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if len(content.strip()) < 20:
                    return None
                context = self._build_file_context(file_path, workspace_dir)
                result = self.process_content_for_stakeholders(content, context)
                return {"file_path": str(file_path), "result": result}
            except Exception as e:
                self.logger.warning(f"File processing error: {file_path} - {e}")
                return None

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(process_file, file_path): file_path
                for file_path in files
            }
            for future in as_completed(future_to_file):
                result = future.result()
                if result and "result" in result:
                    file_result = result["result"]
                    total_stakeholders += file_result.get("candidates_detected", 0)
                    total_auto_created += file_result.get("auto_created", 0)
                    total_needs_profiling += file_result.get("profiling_needed", 0)
                    files_processed += 1

        return {
            "files_processed": files_processed,
            "stakeholders_detected": total_stakeholders,
            "auto_created": total_auto_created,
            "needs_profiling": total_needs_profiling,
            "processing_time": time.time() - start_time,
            "optimization_used": True,
        }

    def _process_files_sequential(
        self, files: List[Path], workspace_dir: Path
    ) -> Dict[str, Any]:
        """Process files sequentially for smaller datasets"""
        start_time = time.time()
        total_stakeholders = total_auto_created = total_needs_profiling = (
            files_processed
        ) = 0

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if len(content.strip()) < 20:
                    continue
                context = self._build_file_context(file_path, workspace_dir)
                result = self.process_content_for_stakeholders(content, context)
                total_stakeholders += result.get("candidates_detected", 0)
                total_auto_created += result.get("auto_created", 0)
                total_needs_profiling += result.get("profiling_needed", 0)
                files_processed += 1
            except Exception as e:
                self.logger.warning(f"File processing error: {file_path} - {e}")

        return {
            "files_processed": files_processed,
            "stakeholders_detected": total_stakeholders,
            "auto_created": total_auto_created,
            "needs_profiling": total_needs_profiling,
            "processing_time": time.time() - start_time,
            "optimization_used": False,
        }

    def _build_file_context(
        self, file_path: Path, workspace_dir: Path
    ) -> Dict[str, Any]:
        """Build context for file analysis"""
        try:
            relative_path = file_path.relative_to(workspace_dir)
        except ValueError:
            relative_path = file_path

        context = {
            "file_path": str(file_path),
            "relative_path": str(relative_path),
            "category": "general",
        }
        path_parts = relative_path.parts

        if any(part in ["meeting-prep", "meetings"] for part in path_parts):
            context["category"] = "meeting_prep"
        elif any(
            part in ["initiatives", "projects", "current-initiatives"]
            for part in path_parts
        ):
            context["category"] = "current_initiatives"
        elif any(part in ["strategic", "strategy"] for part in path_parts):
            context["category"] = "strategic_docs"

        return context

    # === RELATIONSHIP ANALYSIS (consolidated from RelationshipAnalyzer) ===

    def record_interaction(
        self,
        stakeholder_id: str,
        interaction_type: str,
        context: Dict[str, Any],
        outcome: Optional[str] = None,
    ) -> bool:
        """Record stakeholder interaction with outcome tracking"""
        try:
            if not self.repository:
                self.logger.error("Repository required for interaction recording")
                return False

            # Verify stakeholder exists
            stakeholder = self.repository.get_stakeholder(stakeholder_id)
            if not stakeholder:
                self.logger.warning(
                    f"Cannot record interaction for unknown stakeholder: {stakeholder_id}"
                )
                return False

            interaction = {
                "stakeholder_id": stakeholder_id,
                "type": interaction_type,
                "timestamp": time.time(),
                "context": context,
                "outcome": outcome,
                "session_id": context.get("session_id", "default"),
            }

            self.interactions.append(interaction)

            # Update stakeholder profile based on interaction
            self._update_stakeholder_from_interaction(stakeholder, interaction)

            # Cleanup old interactions
            self._cleanup_old_interactions()

            # Cache invalidation
            if self.enable_performance:
                self.cache_manager.delete_pattern("stakeholder_context_*")
                self.cache_manager.delete_pattern("relationship_health_*")

            return True

        except Exception as e:
            self.logger.error(f"Failed to record interaction: {e}")
            return False

    def get_relationship_context(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Get comprehensive relationship context for strategic guidance"""
        try:
            if self.enable_performance:
                cache_key = f"stakeholder_context:{hash(query)}:{limit}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Extract stakeholder mentions from query
            mentioned_stakeholders = self._extract_stakeholder_mentions(query)

            # Get relevant stakeholder profiles
            relevant_profiles = []
            if self.repository:
                for stakeholder_id in mentioned_stakeholders[:limit]:
                    stakeholder = self.repository.get_stakeholder(stakeholder_id)
                    if stakeholder:
                        relevant_profiles.append(
                            stakeholder.to_dict()
                            if hasattr(stakeholder, "to_dict")
                            else stakeholder
                        )

            # Get recent interactions
            recent_interactions = self._get_recent_interactions(mentioned_stakeholders)

            result = {
                "relevant_stakeholders": relevant_profiles,
                "recent_interactions": recent_interactions,
                "context_generated_at": time.time(),
            }

            # Cache result
            if self.enable_performance:
                self.cache_manager.set(cache_key, result, ttl=1800)

            return result

        except Exception as e:
            self.logger.error(f"Failed to get relationship context: {e}")
            return {"relevant_stakeholders": [], "error": str(e)}

    def _extract_stakeholder_mentions(self, text: str) -> List[str]:
        """Extract potential stakeholder mentions from text"""
        if not self.repository:
            return []

        text_lower = text.lower()
        mentioned = []

        # Check for explicit stakeholder names (simplified)
        try:
            stakeholders = self.repository.get_all_stakeholders()
            for stakeholder in stakeholders:
                stakeholder_name = getattr(
                    stakeholder, "name", str(stakeholder)
                ).lower()
                if stakeholder_name in text_lower:
                    mentioned.append(getattr(stakeholder, "id", str(stakeholder)))
        except Exception as e:
            self.logger.warning(f"Error extracting mentions: {e}")

        return list(set(mentioned))  # Remove duplicates

    def _get_recent_interactions(
        self, stakeholder_ids: List[str], days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get recent interactions for specific stakeholders"""
        cutoff_time = time.time() - (days * 24 * 3600)
        recent = [
            interaction
            for interaction in self.interactions
            if interaction.get("timestamp", 0) > cutoff_time
            and interaction.get("stakeholder_id") in stakeholder_ids
        ]
        recent.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return recent[:10]

    def _update_stakeholder_from_interaction(
        self, stakeholder: Any, interaction: Dict[str, Any]
    ) -> None:
        """Update stakeholder profile based on interaction data"""
        try:
            # Update interaction frequency and relationship quality
            if hasattr(stakeholder, "interaction_frequency"):
                stakeholder.interaction_frequency = (
                    stakeholder.interaction_frequency * 0.8
                ) + (1.0 * 0.2)
            if hasattr(stakeholder, "last_interaction"):
                stakeholder.last_interaction = time.time()
        except Exception as e:
            self.logger.warning(f"Error updating stakeholder from interaction: {e}")

    def _cleanup_old_interactions(self) -> None:
        """Remove interactions older than retention period"""
        cutoff_time = time.time() - (self.interaction_retention_days * 24 * 3600)
        self.interactions = [
            interaction
            for interaction in self.interactions
            if interaction.get("timestamp", time.time()) > cutoff_time
        ]

    # === UTILITY METHODS ===

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            "total_interactions": len(self.interactions),
            "performance_enabled": self.enable_performance,
            "supported_extensions": list(self.supported_extensions),
            "detection_patterns": len(self.executive_patterns)
            + len(self.role_indicators),
        }
