"""
Stakeholder Detection Engine - Phase 3A.3.4 SOLID Extraction
Single Responsibility: AI-powered stakeholder detection in content

Extracted from StakeholderIntelligenceUnified for SOLID compliance
Author: Martin | Platform Architecture with Sequential7 methodology
"""

import re
import logging
from typing import Dict, List, Any, Optional


class StakeholderDetectionEngine:
    """
    AI-powered stakeholder detection engine

    Single Responsibility: Detect and analyze stakeholder mentions in content
    with pattern matching, role identification, and confidence scoring.
    """

    def __init__(self, cache_manager=None, enable_performance: bool = True):
        """Initialize detection engine"""
        self.logger = logging.getLogger(__name__)
        self.cache_manager = cache_manager
        self.enable_performance = enable_performance and cache_manager is not None

        # Detection patterns
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

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        AI-powered stakeholder detection in content

        Args:
            content: Text content to analyze
            context: Context information (file_path, category, etc.)

        Returns:
            List of detected stakeholder candidates with confidence scores
        """
        try:
            # Use performance optimization if available
            if self.enable_performance:
                cache_key = f"stakeholder_detection:{hash(content)}:{hash(str(sorted(context.items())))}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Enhanced AI detection logic
            candidates = self._analyze_content_for_stakeholders(content, context)

            # Cache results
            if self.enable_performance and candidates:
                self.cache_manager.set(cache_key, candidates, ttl=7200)  # 2 hour cache

            return candidates

        except Exception as e:
            self.logger.error(f"Stakeholder detection failed: {e}")
            # Return empty list instead of raising to maintain graceful degradation
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
                if isinstance(match, tuple):
                    name = " ".join(match)
                else:
                    name = match

                if len(name.strip()) > 3:  # Basic validation
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
                    # Try to extract name near the role mention
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
        return self._deduplicate_candidates(candidates)

    def _deduplicate_candidates(
        self, candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate candidates and validate"""
        unique_candidates = []
        seen_names = set()

        for candidate in candidates:
            name_key = candidate["name"].lower().strip()
            if name_key not in seen_names and len(name_key) > 3:
                seen_names.add(name_key)
                unique_candidates.append(candidate)

        return unique_candidates[:10]  # Limit to top 10 candidates

    def get_detection_patterns(self) -> Dict[str, Any]:
        """Get current detection patterns for debugging/configuration"""
        return {
            "executive_patterns": self.executive_patterns,
            "role_indicators": self.role_indicators,
        }

    def add_custom_pattern(self, pattern_type: str, pattern: str) -> bool:
        """Add custom detection pattern"""
        try:
            if pattern_type == "executive":
                self.executive_patterns.append(pattern)
            elif pattern_type in self.role_indicators:
                self.role_indicators[pattern_type].append(pattern)
            else:
                # Create new role category
                self.role_indicators[pattern_type] = [pattern]

            return True
        except Exception as e:
            self.logger.error(f"Failed to add custom pattern: {e}")
            return False
