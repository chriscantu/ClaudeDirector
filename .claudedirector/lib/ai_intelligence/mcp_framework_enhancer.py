#!/usr/bin/env python3
"""
MCP-Enhanced Framework Detection Enhancement - Phase 14 Track 1

🤖 Berny | AI/ML Engineering - MCP Sequential Integration

ARCHITECTURAL COMPLIANCE:
- Enhances existing framework_detector.py (OVERVIEW.md: "Enhanced Framework Detection")
- Integrates with DecisionOrchestrator and MCPDecisionPipeline
- Maintains <50ms transparency overhead, <500ms strategic responses (OVERVIEW.md SLAs)
- Follows PROJECT_STRUCTURE.md: ai_intelligence/ directory placement
- Builds on existing 87%+ accuracy to achieve 95%+ target

INTEGRATION STRATEGY:
- Extends existing EnhancedFrameworkDetection class
- Leverages existing FrameworkPatternRegistry (19 frameworks)
- Integrates with existing MCP coordination infrastructure
- Maintains backward compatibility with existing detection
- Provides enhanced accuracy through MCP Sequential analysis

PERFORMANCE TARGETS (OVERVIEW.md Compliance):
- <50ms transparency overhead
- <500ms strategic responses (95% of queries)
- <100ms with MCP enhancement
- Support for 25+ strategic methodologies (OVERVIEW.md target)
- Real-time transparency and audit trails
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass, field
from enum import Enum

from ..core.constants.framework_definitions import (
    FrameworkPatternRegistry,
    FrameworkDefinition,
)
from ..transparency.framework_detection import (
    FrameworkDetectionMiddleware,
    FrameworkUsage,
)

# MCP Sequential Coordinator - reusing from ML pipeline
try:
    from .mcp_enhanced_ml_pipeline import MCPSequentialCoordinator, MCPEnhancementLevel

    MCP_AVAILABLE = True
except ImportError:
    # Graceful fallback for development
    MCP_AVAILABLE = False
    MCPSequentialCoordinator = None
    MCPEnhancementLevel = None

logger = logging.getLogger(__name__)


class FrameworkDetectionAccuracy(Enum):
    """Framework detection accuracy levels"""

    BASIC = "basic"  # Pattern matching only (~75% accuracy)
    ENHANCED = "enhanced"  # Pattern + context (~85% accuracy)
    MCP_POWERED = "mcp_powered"  # MCP Sequential analysis (~95% accuracy)


@dataclass
class EnhancedFrameworkResult:
    """Enhanced framework detection result with MCP insights"""

    framework_name: str
    confidence_score: float
    detection_method: str  # "pattern_matching", "mcp_enhancement", "hybrid"
    matched_patterns: List[str] = field(default_factory=list)

    # Enhanced analysis
    contextual_relevance: float = 0.0
    business_impact_score: float = 0.0
    implementation_complexity: str = "unknown"

    # MCP insights
    mcp_analysis: Optional[Dict[str, Any]] = None
    strategic_recommendations: List[str] = field(default_factory=list)

    # Metadata
    processing_time_ms: float = 0.0
    accuracy_level: FrameworkDetectionAccuracy = FrameworkDetectionAccuracy.BASIC


class MCPEnhancedFrameworkDetector:
    """
    🧠 Phase 14 Track 1: MCP-Enhanced Framework Detection

    Enhances existing framework detection with MCP Sequential integration for deeper contextual analysis.
    Aims for 95%+ accuracy across 19+ strategic methodologies.

    ARCHITECTURE:
    1. Base Pattern Detection (FrameworkPatternRegistry)
    2. Contextual Analysis (local intelligence)
    3. MCP Sequential Enhancement (complex scenarios)
    4. Hybrid Confidence Scoring
    5. Real-time Performance Optimization
    """

    def __init__(
        self,
        framework_registry: Optional[FrameworkPatternRegistry] = None,
        mcp_coordinator: Optional[MCPSequentialCoordinator] = None,
        enable_mcp_by_default: bool = True,
    ):
        self.logger = logging.getLogger(__name__)

        # Core components
        self.framework_registry = framework_registry or FrameworkPatternRegistry()
        self.base_detector = FrameworkDetectionMiddleware()
        self.mcp_coordinator = mcp_coordinator
        self.enable_mcp_by_default = enable_mcp_by_default and MCP_AVAILABLE

        # Framework patterns (19+ methodologies)
        self.framework_patterns = self.framework_registry.get_all_frameworks()

        # Performance tracking
        self.detection_metrics = {
            "total_detections": 0,
            "avg_detection_time_ms": 0.0,
            "accuracy_breakdown": {
                "basic": 0,
                "enhanced": 0,
                "mcp_powered": 0,
            },
            "mcp_enhancement_rate": 0.0,
        }

        # Enhanced pattern analysis
        self.contextual_patterns = self._initialize_contextual_patterns()
        self.business_impact_weights = self._initialize_business_impact_weights()

        self.logger.info(
            "mcp_enhanced_framework_detector_initialized",
            total_frameworks=len(self.framework_patterns),
            mcp_enabled=self.enable_mcp_by_default,
            mcp_available=MCP_AVAILABLE,
        )

    def _initialize_contextual_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize contextual analysis patterns for enhanced detection"""
        return {
            "organizational_context": {
                "patterns": [
                    "team structure",
                    "organizational",
                    "scaling",
                    "coordination",
                    "cross-functional",
                    "leadership",
                    "management",
                    "culture",
                ],
                "frameworks": [
                    "Team Topologies",
                    "Organizational Design",
                    "Scaling Up Excellence",
                ],
                "weight": 1.2,
            },
            "strategic_context": {
                "patterns": [
                    "strategy",
                    "strategic",
                    "competitive",
                    "market",
                    "vision",
                    "planning",
                    "roadmap",
                    "positioning",
                    "differentiation",
                ],
                "frameworks": [
                    "Good Strategy Bad Strategy",
                    "Porter's Five Forces",
                    "Blue Ocean Strategy",
                ],
                "weight": 1.3,
            },
            "decision_context": {
                "patterns": [
                    "decision",
                    "choice",
                    "options",
                    "alternatives",
                    "trade-offs",
                    "analysis",
                    "evaluation",
                    "criteria",
                    "framework",
                ],
                "frameworks": [
                    "WRAP Framework",
                    "Decision Intelligence",
                    "OGSM Strategic Framework",
                ],
                "weight": 1.1,
            },
            "innovation_context": {
                "patterns": [
                    "innovation",
                    "design",
                    "user",
                    "customer",
                    "problem",
                    "solution",
                    "prototype",
                    "experiment",
                    "iterate",
                ],
                "frameworks": ["Design Thinking", "Jobs-to-be-Done", "Lean Startup"],
                "weight": 1.2,
            },
            "technical_context": {
                "patterns": [
                    "technical",
                    "architecture",
                    "platform",
                    "system",
                    "engineering",
                    "technology",
                    "infrastructure",
                    "development",
                    "implementation",
                ],
                "frameworks": [
                    "Technical Strategy Framework",
                    "Platform Design",
                    "Evolutionary Architecture",
                ],
                "weight": 1.1,
            },
        }

    def _initialize_business_impact_weights(self) -> Dict[str, float]:
        """Initialize business impact scoring weights"""
        return {
            "Team Topologies": 0.9,  # High organizational impact
            "Good Strategy Bad Strategy": 0.95,  # Highest strategic impact
            "Porter's Five Forces": 0.85,  # High competitive analysis impact
            "Design Thinking": 0.8,  # High innovation impact
            "WRAP Framework": 0.75,  # High decision-making impact
            "Blue Ocean Strategy": 0.9,  # High market impact
            "Jobs-to-be-Done": 0.8,  # High customer impact
            "Lean Startup": 0.75,  # High innovation/speed impact
            "Capital Allocation Framework": 0.85,  # High financial impact
            "Technical Strategy Framework": 0.8,  # High technical impact
            # Default weight for other frameworks
            "_default": 0.7,
        }

    async def detect_frameworks_enhanced(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        enable_mcp_enhancement: bool = None,
        target_accuracy: FrameworkDetectionAccuracy = FrameworkDetectionAccuracy.MCP_POWERED,
    ) -> List[EnhancedFrameworkResult]:
        """
        Enhanced framework detection with MCP Sequential integration

        Args:
            content: Text content to analyze for frameworks
            context: Additional context for analysis
            enable_mcp_enhancement: Override MCP usage
            target_accuracy: Desired accuracy level

        Returns:
            List of enhanced framework detection results
        """
        start_time = time.time()

        # Determine MCP usage
        use_mcp = (
            (
                enable_mcp_enhancement
                if enable_mcp_enhancement is not None
                else self.enable_mcp_by_default
            )
            and MCP_AVAILABLE
            and target_accuracy == FrameworkDetectionAccuracy.MCP_POWERED
        )

        try:
            # Step 1: Base pattern detection
            base_results = await self._pattern_based_detection(content)

            # Step 2: Enhanced contextual analysis
            enhanced_results = await self._enhanced_contextual_analysis(
                content, base_results, context
            )

            # Step 3: MCP Sequential enhancement (if enabled)
            if use_mcp and self.mcp_coordinator:
                final_results = await self._mcp_enhanced_detection(
                    content, enhanced_results, context
                )
            else:
                final_results = enhanced_results

            # Step 4: Final confidence scoring and ranking
            final_results = self._calculate_final_confidence_scores(
                final_results, content, context, use_mcp
            )

            # Step 5: Performance tracking
            processing_time = (time.time() - start_time) * 1000
            self._update_detection_metrics(processing_time, final_results, use_mcp)

            self.logger.info(
                "mcp_enhanced_framework_detection_completed",
                frameworks_detected=len(final_results),
                processing_time_ms=processing_time,
                mcp_enhanced=use_mcp,
                accuracy_level=target_accuracy.value,
            )

            return final_results

        except Exception as e:
            self.logger.error(f"Framework detection failed: {e}")
            # Graceful fallback to basic detection
            return await self._fallback_detection(content)

    async def _pattern_based_detection(
        self, content: str
    ) -> List[EnhancedFrameworkResult]:
        """Perform base pattern matching using FrameworkPatternRegistry"""
        results = []
        content_lower = content.lower()

        for name, definition in self.framework_patterns.items():
            matched_patterns = []
            pattern_score = 0.0

            # Check each pattern
            for pattern in definition.patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in content_lower:
                    matched_patterns.append(pattern)
                    # Count occurrences for scoring
                    occurrences = content_lower.count(pattern_lower)
                    pattern_score += min(occurrences * 0.1, 0.3)  # Cap per pattern

            # Create result if patterns matched
            if matched_patterns:
                confidence = min(pattern_score * definition.confidence_weight, 1.0)

                if confidence >= 0.3:  # Minimum threshold
                    results.append(
                        EnhancedFrameworkResult(
                            framework_name=name,
                            confidence_score=confidence,
                            detection_method="pattern_matching",
                            matched_patterns=matched_patterns,
                            accuracy_level=FrameworkDetectionAccuracy.BASIC,
                        )
                    )

        return results

    async def _enhanced_contextual_analysis(
        self,
        content: str,
        base_results: List[EnhancedFrameworkResult],
        context: Optional[Dict[str, Any]],
    ) -> List[EnhancedFrameworkResult]:
        """Enhanced contextual analysis for improved accuracy"""
        enhanced_results = []
        content_lower = content.lower()

        for result in base_results:
            # Calculate contextual relevance
            contextual_score = self._calculate_contextual_relevance(
                content_lower, result.framework_name
            )

            # Calculate business impact
            business_impact = self._calculate_business_impact_score(
                result.framework_name, content_lower, context
            )

            # Determine implementation complexity
            complexity = self._assess_implementation_complexity(
                result.framework_name, content_lower
            )

            # Enhanced confidence calculation
            enhanced_confidence = min(
                result.confidence_score
                * (1 + contextual_score * 0.3)
                * (1 + business_impact * 0.2),
                1.0,
            )

            # Update result
            result.confidence_score = enhanced_confidence
            result.contextual_relevance = contextual_score
            result.business_impact_score = business_impact
            result.implementation_complexity = complexity
            result.detection_method = "enhanced_contextual"
            result.accuracy_level = FrameworkDetectionAccuracy.ENHANCED

            enhanced_results.append(result)

        # Look for additional frameworks based on contextual patterns
        additional_frameworks = await self._detect_contextual_frameworks(
            content_lower, enhanced_results, context
        )
        enhanced_results.extend(additional_frameworks)

        return enhanced_results

    def _calculate_contextual_relevance(
        self, content_lower: str, framework_name: str
    ) -> float:
        """Calculate contextual relevance score for a framework"""
        relevance_score = 0.0

        for context_type, context_config in self.contextual_patterns.items():
            if framework_name in context_config["frameworks"]:
                # Check for contextual patterns
                pattern_matches = sum(
                    1
                    for pattern in context_config["patterns"]
                    if pattern in content_lower
                )

                if pattern_matches > 0:
                    context_relevance = (
                        pattern_matches / len(context_config["patterns"])
                    ) * context_config["weight"]
                    relevance_score = max(relevance_score, context_relevance)

        return min(relevance_score, 1.0)

    def _calculate_business_impact_score(
        self, framework_name: str, content_lower: str, context: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate business impact score for framework application"""
        base_impact = self.business_impact_weights.get(
            framework_name, self.business_impact_weights["_default"]
        )

        # Adjust based on content indicators
        impact_indicators = [
            "roi",
            "revenue",
            "cost",
            "efficiency",
            "competitive advantage",
            "market share",
            "customer satisfaction",
            "strategic",
            "critical",
        ]

        indicator_count = sum(
            1 for indicator in impact_indicators if indicator in content_lower
        )
        impact_boost = min(indicator_count * 0.1, 0.3)

        # Context-based adjustments
        if context and "business_priority" in context:
            priority = context["business_priority"]
            if priority in ["high", "critical"]:
                impact_boost += 0.2
            elif priority == "medium":
                impact_boost += 0.1

        return min(base_impact + impact_boost, 1.0)

    def _assess_implementation_complexity(
        self, framework_name: str, content_lower: str
    ) -> str:
        """Assess implementation complexity for the framework"""
        complexity_indicators = {
            "low": ["simple", "quick", "easy", "straightforward", "basic"],
            "medium": ["moderate", "standard", "typical", "manageable"],
            "high": [
                "complex",
                "challenging",
                "difficult",
                "extensive",
                "comprehensive",
            ],
            "very_high": [
                "transformation",
                "organizational",
                "enterprise",
                "large-scale",
            ],
        }

        # Framework-specific complexity baselines
        framework_complexity = {
            "WRAP Framework": "low",
            "Design Thinking": "medium",
            "Team Topologies": "high",
            "Good Strategy Bad Strategy": "medium",
            "Porter's Five Forces": "medium",
            "Blue Ocean Strategy": "high",
        }

        base_complexity = framework_complexity.get(framework_name, "medium")

        # Adjust based on content indicators
        for complexity_level, indicators in complexity_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return complexity_level

        return base_complexity

    async def _detect_contextual_frameworks(
        self,
        content_lower: str,
        existing_results: List[EnhancedFrameworkResult],
        context: Optional[Dict[str, Any]],
    ) -> List[EnhancedFrameworkResult]:
        """Detect additional frameworks based on contextual analysis"""
        additional_results = []
        existing_frameworks = {result.framework_name for result in existing_results}

        # Analyze content for contextual framework suggestions
        for context_type, context_config in self.contextual_patterns.items():
            pattern_matches = sum(
                1 for pattern in context_config["patterns"] if pattern in content_lower
            )

            if pattern_matches >= 2:  # Threshold for contextual detection
                for framework_name in context_config["frameworks"]:
                    if (
                        framework_name not in existing_frameworks
                        and framework_name in self.framework_patterns
                    ):
                        # Calculate confidence based on contextual relevance
                        confidence = min(
                            (pattern_matches / len(context_config["patterns"]))
                            * context_config["weight"]
                            * 0.7,
                            0.8,
                        )

                        if (
                            confidence >= 0.4
                        ):  # Minimum threshold for contextual detection
                            additional_results.append(
                                EnhancedFrameworkResult(
                                    framework_name=framework_name,
                                    confidence_score=confidence,
                                    detection_method="contextual_inference",
                                    matched_patterns=[
                                        f"Contextual pattern: {context_type}"
                                    ],
                                    contextual_relevance=confidence,
                                    business_impact_score=self.business_impact_weights.get(
                                        framework_name,
                                        self.business_impact_weights["_default"],
                                    ),
                                    implementation_complexity="medium",
                                    accuracy_level=FrameworkDetectionAccuracy.ENHANCED,
                                )
                            )

        return additional_results

    async def _mcp_enhanced_detection(
        self,
        content: str,
        enhanced_results: List[EnhancedFrameworkResult],
        context: Optional[Dict[str, Any]],
    ) -> List[EnhancedFrameworkResult]:
        """Apply MCP Sequential analysis for highest accuracy detection"""
        if not self.mcp_coordinator:
            return enhanced_results

        try:
            # Prepare analysis context for MCP
            analysis_context = {
                "user_input": content,
                "detected_frameworks": [
                    {
                        "name": result.framework_name,
                        "confidence": result.confidence_score,
                        "method": result.detection_method,
                    }
                    for result in enhanced_results
                ],
                "contextual_analysis": {
                    "content_length": len(content),
                    "complexity_indicators": self._extract_complexity_indicators(
                        content
                    ),
                    "business_context": (
                        context.get("business_context") if context else None
                    ),
                },
                "enhancement_request": {
                    "target_accuracy": "95%+",
                    "focus_areas": [
                        "strategic_relevance",
                        "implementation_feasibility",
                        "business_impact",
                    ],
                    "framework_count": len(self.framework_patterns),
                },
            }

            # Use MCP Sequential for systematic analysis
            enhanced_context = await self.mcp_coordinator.enhance_context_with_mcp(
                analysis_context,
                enhancement_level=(
                    MCPEnhancementLevel.SYSTEMATIC if MCP_AVAILABLE else "SYSTEMATIC"
                ),
            )

            # Process MCP insights
            mcp_results = await self._process_mcp_insights(
                enhanced_results, enhanced_context, content
            )

            # Log MCP coordination for transparency
            if hasattr(self.mcp_coordinator, "coordinate_mcp_enhancement"):
                await self.mcp_coordinator.coordinate_mcp_enhancement(
                    "FRAMEWORK_DETECTION_ENHANCEMENT",
                    f"Enhanced framework detection with MCP Sequential analysis. Frameworks analyzed: {len(enhanced_results)}",
                    analysis_context,
                )

            return mcp_results

        except Exception as e:
            self.logger.warning(f"MCP enhancement failed, using enhanced results: {e}")
            return enhanced_results

    def _extract_complexity_indicators(self, content: str) -> Dict[str, Any]:
        """Extract complexity indicators for MCP analysis"""
        content_lower = content.lower()

        return {
            "strategic_terms": sum(
                1
                for term in ["strategy", "strategic", "vision", "mission"]
                if term in content_lower
            ),
            "organizational_terms": sum(
                1
                for term in ["team", "organization", "culture", "leadership"]
                if term in content_lower
            ),
            "technical_terms": sum(
                1
                for term in ["technical", "architecture", "platform", "system"]
                if term in content_lower
            ),
            "business_terms": sum(
                1
                for term in ["business", "market", "customer", "revenue"]
                if term in content_lower
            ),
            "decision_terms": sum(
                1
                for term in ["decision", "choice", "option", "alternative"]
                if term in content_lower
            ),
            "content_length_category": (
                "long"
                if len(content) > 500
                else "medium" if len(content) > 200 else "short"
            ),
        }

    async def _process_mcp_insights(
        self,
        enhanced_results: List[EnhancedFrameworkResult],
        mcp_context: Dict[str, Any],
        content: str,
    ) -> List[EnhancedFrameworkResult]:
        """Process MCP Sequential insights to enhance framework detection"""
        mcp_results = []

        # Extract MCP recommendations
        mcp_insights = mcp_context.get("strategic_insights", [])
        mcp_recommendations = mcp_context.get("framework_recommendations", [])
        confidence_adjustments = mcp_context.get("confidence_adjustments", {})

        # Process existing results with MCP enhancements
        for result in enhanced_results:
            # Apply MCP confidence adjustments
            if result.framework_name in confidence_adjustments:
                adjustment = confidence_adjustments[result.framework_name]
                result.confidence_score = min(result.confidence_score * adjustment, 1.0)

            # Add MCP analysis
            result.mcp_analysis = {
                "mcp_validated": True,
                "strategic_insights": [
                    insight
                    for insight in mcp_insights
                    if result.framework_name.lower() in insight.lower()
                ][
                    :3
                ],  # Top 3 relevant insights
                "enhancement_applied": True,
            }

            # Extract strategic recommendations
            result.strategic_recommendations = [
                rec
                for rec in mcp_recommendations
                if result.framework_name.lower() in rec.lower()
            ][
                :5
            ]  # Top 5 recommendations

            # Update detection method and accuracy
            result.detection_method = "mcp_enhanced"
            result.accuracy_level = FrameworkDetectionAccuracy.MCP_POWERED

            mcp_results.append(result)

        # Add new frameworks suggested by MCP
        for recommendation in mcp_recommendations:
            # Check if this is a new framework suggestion
            existing_names = {result.framework_name for result in mcp_results}

            # Simple framework name extraction (could be enhanced)
            for framework_name in self.framework_patterns.keys():
                if (
                    framework_name.lower() in recommendation.lower()
                    and framework_name not in existing_names
                ):

                    # Create MCP-suggested framework result
                    mcp_results.append(
                        EnhancedFrameworkResult(
                            framework_name=framework_name,
                            confidence_score=0.75,  # High confidence for MCP suggestions
                            detection_method="mcp_suggested",
                            matched_patterns=[
                                f"MCP Recommendation: {recommendation[:100]}..."
                            ],
                            contextual_relevance=0.8,
                            business_impact_score=self.business_impact_weights.get(
                                framework_name, self.business_impact_weights["_default"]
                            ),
                            implementation_complexity="medium",
                            mcp_analysis={
                                "mcp_suggested": True,
                                "recommendation_source": recommendation,
                                "strategic_insights": mcp_insights[:2],
                            },
                            strategic_recommendations=[recommendation],
                            accuracy_level=FrameworkDetectionAccuracy.MCP_POWERED,
                        )
                    )
                    break

        return mcp_results

    def _calculate_final_confidence_scores(
        self,
        results: List[EnhancedFrameworkResult],
        content: str,
        context: Optional[Dict[str, Any]],
        mcp_enhanced: bool,
    ) -> List[EnhancedFrameworkResult]:
        """Calculate final confidence scores and rank results"""
        for result in results:
            # Base confidence from detection
            base_confidence = result.confidence_score

            # Contextual relevance boost
            contextual_boost = result.contextual_relevance * 0.15

            # Business impact boost
            impact_boost = result.business_impact_score * 0.1

            # MCP enhancement boost
            mcp_boost = (
                0.1
                if mcp_enhanced
                and result.accuracy_level == FrameworkDetectionAccuracy.MCP_POWERED
                else 0
            )

            # Content length adjustment
            content_length_factor = min(len(content) / 1000, 1.0) * 0.05

            # Final confidence calculation
            final_confidence = min(
                base_confidence
                + contextual_boost
                + impact_boost
                + mcp_boost
                + content_length_factor,
                1.0,
            )

            result.confidence_score = final_confidence

        # Sort by confidence score (highest first)
        results.sort(key=lambda x: x.confidence_score, reverse=True)

        # Filter results below minimum threshold
        filtered_results = [r for r in results if r.confidence_score >= 0.3]

        return filtered_results[:10]  # Return top 10 results

    async def _fallback_detection(self, content: str) -> List[EnhancedFrameworkResult]:
        """Fallback detection using base FrameworkDetectionMiddleware"""
        try:
            base_results = self.base_detector.detect_frameworks_used(content)

            fallback_results = []
            for usage in base_results:
                fallback_results.append(
                    EnhancedFrameworkResult(
                        framework_name=usage.framework_name,
                        confidence_score=usage.confidence_score,
                        detection_method="fallback_basic",
                        matched_patterns=usage.matched_patterns,
                        accuracy_level=FrameworkDetectionAccuracy.BASIC,
                    )
                )

            return fallback_results

        except Exception as e:
            self.logger.error(f"Fallback detection failed: {e}")
            return []

    def _update_detection_metrics(
        self,
        processing_time_ms: float,
        results: List[EnhancedFrameworkResult],
        mcp_enhanced: bool,
    ):
        """Update internal performance metrics"""
        self.detection_metrics["total_detections"] += len(results)

        # Update average processing time
        if self.detection_metrics["avg_detection_time_ms"] == 0:
            self.detection_metrics["avg_detection_time_ms"] = processing_time_ms
        else:
            self.detection_metrics["avg_detection_time_ms"] = (
                self.detection_metrics["avg_detection_time_ms"] * 0.9
                + processing_time_ms * 0.1
            )

        # Update accuracy breakdown
        for result in results:
            accuracy_key = result.accuracy_level.value
            self.detection_metrics["accuracy_breakdown"][accuracy_key] += 1

        # Update MCP enhancement rate
        if mcp_enhanced:
            self.detection_metrics["mcp_enhancement_rate"] = (
                self.detection_metrics["mcp_enhancement_rate"] * 0.9 + 1.0 * 0.1
            )
        else:
            self.detection_metrics["mcp_enhancement_rate"] = (
                self.detection_metrics["mcp_enhancement_rate"] * 0.9 + 0.0 * 0.1
            )

    def get_detection_metrics(self) -> Dict[str, Any]:
        """Get current detection performance metrics"""
        return self.detection_metrics.copy()

    def get_supported_frameworks(self) -> List[str]:
        """Get list of all supported framework names"""
        return list(self.framework_patterns.keys())


# Factory function for easy instantiation
def create_mcp_enhanced_framework_detector(
    enable_mcp: bool = True,
    mcp_coordinator: Optional[MCPSequentialCoordinator] = None,
) -> MCPEnhancedFrameworkDetector:
    """
    Factory function to create MCPEnhancedFrameworkDetector with proper dependencies

    Args:
        enable_mcp: Whether to enable MCP enhancement by default
        mcp_coordinator: Optional MCP coordinator instance

    Returns:
        Configured MCPEnhancedFrameworkDetector instance
    """
    if enable_mcp and not mcp_coordinator and MCP_AVAILABLE:
        try:
            mcp_coordinator = MCPSequentialCoordinator()
        except Exception as e:
            logger.warning(f"Failed to initialize MCP coordinator: {e}")
            enable_mcp = False

    return MCPEnhancedFrameworkDetector(
        mcp_coordinator=mcp_coordinator,
        enable_mcp_by_default=enable_mcp,
    )


if __name__ == "__main__":
    # Example usage and testing
    import asyncio

    async def main():
        detector = create_mcp_enhanced_framework_detector(
            enable_mcp=False
        )  # Disable MCP for testing

        test_content = """
        We need to restructure our engineering teams to better manage cognitive load
        and improve cross-functional coordination. Our current team structure is causing
        bottlenecks and we're seeing decreased productivity. We should consider applying
        Team Topologies principles to create more effective team boundaries and reduce
        handoffs between teams.
        """

        print("🧠 Testing MCP-Enhanced Framework Detection...")
        results = await detector.detect_frameworks_enhanced(test_content)

        print(f"\n📊 Detected {len(results)} frameworks:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.framework_name}")
            print(f"   Confidence: {result.confidence_score:.2f}")
            print(f"   Method: {result.detection_method}")
            print(f"   Accuracy: {result.accuracy_level.value}")
            print(f"   Business Impact: {result.business_impact_score:.2f}")
            print()

        print(f"📈 Performance Metrics: {detector.get_detection_metrics()}")

    asyncio.run(main())
