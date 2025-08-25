"""
FrameworkMCPCoordinator - Phase 2 AI Intelligence

🏗️ Martin | Platform Architecture - Team Lead
🤖 Berny | Senior AI Developer

Coordinates multiple frameworks with MCP server capabilities for complex strategic scenarios.
Leverages existing MultiFrameworkIntegrationEngine and enhances it with MCP intelligence.

BUILDS ON EXISTING:
- MultiFrameworkIntegrationEngine: Framework synergies and integration patterns
- MCPEnhancedFrameworkEngine: Individual framework MCP enhancement
- RealMCPIntegrationHelper: MCP server coordination (Context7, Sequential, Magic)
- IntegratedTransparencySystem: Complete audit trail and disclosure

COORDINATION STRATEGY:
1. Multi-Framework Detection: Identify scenarios requiring multiple frameworks
2. Conflict Resolution: Handle competing framework recommendations
3. MCP Orchestration: Coordinate multiple MCP servers for complex analysis
4. Synthesis: Combine multiple enhanced frameworks into coherent guidance
5. Transparency: Full audit trail of coordination decisions

TARGET: Handle complex strategic scenarios with 3+ frameworks and multiple MCP servers
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import structlog

# Import existing infrastructure we're building on
from ..core.enhanced_framework_engine import (
    MultiFrameworkIntegrationEngine,
    MultiFrameworkAnalysis,
    FrameworkAnalysis,
    ConversationContext,
)
from ..transparency.real_mcp_integration import (
    RealMCPIntegrationHelper,
    EnhancedTransparentPersonaManager,
)
from ..transparency.integrated_transparency import (
    IntegratedTransparencySystem,
    TransparencyContext,
    MCPDisclosure,
)
from .mcp_enhanced_framework_engine import (
    MCPEnhancedFrameworkEngine,
    FrameworkDetectionResult,
)

logger = structlog.get_logger(__name__)


class CoordinationComplexity(Enum):
    """Framework coordination complexity levels"""

    SINGLE = "single"  # Single framework, no coordination needed
    DUAL = "dual"  # Two frameworks, simple coordination
    MULTI = "multi"  # 3-4 frameworks, complex coordination
    ENTERPRISE = "enterprise"  # 5+ frameworks, full orchestration


@dataclass
class FrameworkConflict:
    """Represents a conflict between framework recommendations"""

    framework_a: str
    framework_b: str
    conflict_type: str  # "recommendation", "priority", "approach"
    severity: float  # 0.0 to 1.0
    resolution_strategy: str
    mcp_resolution_needed: bool


@dataclass
class CoordinationResult:
    """Result of framework coordination with MCP enhancement"""

    primary_frameworks: List[str]
    supporting_frameworks: List[str]
    coordination_complexity: CoordinationComplexity
    conflicts_resolved: List[FrameworkConflict]
    mcp_enhancements_applied: List[str]
    synthesis_confidence: float
    processing_time_ms: float
    transparency_disclosures: List[MCPDisclosure]


class FrameworkMCPCoordinator:
    """
    🔧 Framework MCP Coordinator - Phase 2 Core Component

    Coordinates multiple frameworks with MCP server capabilities for complex strategic scenarios.
    Handles framework conflicts, MCP orchestration, and synthesis of multiple enhanced analyses.

    COORDINATION CAPABILITIES:
    1. Multi-Framework Detection: Identify scenarios requiring multiple frameworks
    2. Conflict Resolution: Resolve competing recommendations using MCP intelligence
    3. MCP Orchestration: Coordinate Context7 + Sequential + Magic servers
    4. Synthesis: Combine multiple enhanced frameworks into coherent guidance
    5. Transparency: Complete audit trail of all coordination decisions
    """

    def __init__(
        self,
        multi_framework_engine: MultiFrameworkIntegrationEngine,
        mcp_enhanced_engine: MCPEnhancedFrameworkEngine,
        mcp_helper: RealMCPIntegrationHelper,
        transparency_system: IntegratedTransparencySystem,
    ):
        """
        Initialize Framework MCP Coordinator

        Args:
            multi_framework_engine: Existing MultiFrameworkIntegrationEngine
            mcp_enhanced_engine: MCPEnhancedFrameworkEngine for individual enhancements
            mcp_helper: Real MCP server integration helper
            transparency_system: Integrated transparency system
        """
        self.multi_framework_engine = multi_framework_engine
        self.mcp_enhanced_engine = mcp_enhanced_engine
        self.mcp_helper = mcp_helper
        self.transparency_system = transparency_system

        # Coordination configuration
        self.coordination_thresholds = self._initialize_coordination_thresholds()
        self.conflict_resolution_strategies = self._initialize_conflict_strategies()
        self.mcp_orchestration_patterns = self._initialize_orchestration_patterns()

        # Performance tracking
        self.coordinator_metrics = {
            "coordinations_processed": 0,
            "conflicts_resolved": 0,
            "mcp_orchestrations_executed": 0,
            "avg_synthesis_confidence": 0.0,
            "avg_coordination_time_ms": 0.0,
        }

        logger.info(
            "framework_mcp_coordinator_initialized",
            coordination_capabilities=4,
            conflict_resolution_strategies=5,
            mcp_orchestration_patterns=3,
        )

    def _initialize_coordination_thresholds(self) -> Dict[str, float]:
        """Initialize thresholds for coordination complexity determination"""
        return {
            "single_framework_threshold": 0.85,  # Above this, single framework sufficient
            "dual_framework_threshold": 0.70,  # Below this, need dual frameworks
            "multi_framework_threshold": 0.55,  # Below this, need 3+ frameworks
            "enterprise_threshold": 0.40,  # Below this, need full orchestration
            "conflict_severity_threshold": 0.60,  # Above this, MCP resolution needed
            "synthesis_confidence_minimum": 0.75,  # Minimum acceptable synthesis confidence
        }

    def _initialize_conflict_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize conflict resolution strategies"""
        return {
            "recommendation_conflict": {
                "strategy": "mcp_sequential_analysis",
                "mcp_server": "sequential",
                "resolution_method": "systematic_comparison",
                "confidence_boost": 0.15,
            },
            "priority_conflict": {
                "strategy": "context_analysis",
                "mcp_server": "context7",
                "resolution_method": "stakeholder_alignment",
                "confidence_boost": 0.10,
            },
            "approach_conflict": {
                "strategy": "hybrid_synthesis",
                "mcp_server": "both",
                "resolution_method": "complementary_integration",
                "confidence_boost": 0.20,
            },
            "timeline_conflict": {
                "strategy": "phased_implementation",
                "mcp_server": "sequential",
                "resolution_method": "roadmap_optimization",
                "confidence_boost": 0.12,
            },
            "resource_conflict": {
                "strategy": "constraint_optimization",
                "mcp_server": "context7",
                "resolution_method": "capacity_analysis",
                "confidence_boost": 0.08,
            },
        }

    def _initialize_orchestration_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize MCP orchestration patterns for complex scenarios"""
        return {
            "sequential_then_context": {
                "description": "Sequential analysis followed by context validation",
                "servers": ["sequential", "context7"],
                "use_case": "Strategic decision with implementation details",
                "confidence_multiplier": 1.25,
            },
            "parallel_validation": {
                "description": "Parallel Context7 and Sequential analysis",
                "servers": ["context7", "sequential"],
                "use_case": "Complex framework conflicts requiring dual perspective",
                "confidence_multiplier": 1.30,
            },
            "full_orchestration": {
                "description": "All MCP servers with Magic visualization",
                "servers": ["sequential", "context7", "magic"],
                "use_case": "Enterprise-level strategic coordination",
                "confidence_multiplier": 1.40,
            },
        }

    async def coordinate_frameworks(
        self,
        user_input: str,
        session_id: str,
        persona: str,
        context: ConversationContext,
    ) -> CoordinationResult:
        """
        Coordinate multiple frameworks with MCP enhancement for complex strategic scenarios

        Args:
            user_input: User's strategic question or scenario
            session_id: Session identifier for tracking
            persona: Active persona (diego, camille, etc.)
            context: Conversation context for analysis

        Returns:
            CoordinationResult with enhanced multi-framework analysis
        """
        start_time = time.time()

        try:
            # Step 1: Determine coordination complexity
            complexity = await self._analyze_coordination_complexity(
                user_input, context
            )

            # Step 2: Detect required frameworks
            required_frameworks = await self._detect_required_frameworks(
                user_input, context, complexity
            )

            # Step 3: Identify potential conflicts
            conflicts = await self._identify_framework_conflicts(
                required_frameworks, user_input, context
            )

            # Step 4: Apply MCP enhancements to individual frameworks
            enhanced_frameworks = await self._enhance_frameworks_with_mcp(
                required_frameworks, user_input, session_id, persona
            )

            # Step 5: Resolve conflicts using MCP intelligence
            resolved_conflicts = await self._resolve_conflicts_with_mcp(
                conflicts, enhanced_frameworks, user_input, persona
            )

            # Step 6: Synthesize coordinated result
            synthesis_result = await self._synthesize_coordinated_frameworks(
                enhanced_frameworks, resolved_conflicts, complexity, persona
            )

            # Step 7: Generate transparency disclosures
            transparency_disclosures = self._generate_coordination_disclosures(
                complexity, resolved_conflicts, enhanced_frameworks, persona
            )

            processing_time = (time.time() - start_time) * 1000

            # Update metrics
            self._update_coordinator_metrics(
                complexity, len(resolved_conflicts), processing_time
            )

            return CoordinationResult(
                primary_frameworks=synthesis_result["primary_frameworks"],
                supporting_frameworks=synthesis_result["supporting_frameworks"],
                coordination_complexity=complexity,
                conflicts_resolved=resolved_conflicts,
                mcp_enhancements_applied=synthesis_result["mcp_enhancements"],
                synthesis_confidence=synthesis_result["confidence"],
                processing_time_ms=processing_time,
                transparency_disclosures=transparency_disclosures,
            )

        except Exception as e:
            logger.error(
                "framework_coordination_failed",
                error=str(e),
                user_input_length=len(user_input),
                persona=persona,
            )
            # Return fallback result
            return self._create_fallback_coordination_result(user_input, persona)

    async def _analyze_coordination_complexity(
        self, user_input: str, context: ConversationContext
    ) -> CoordinationComplexity:
        """Analyze the complexity level required for framework coordination"""
        # Analyze input complexity indicators
        complexity_indicators = {
            "strategic_keywords": len(
                [
                    word
                    for word in user_input.lower().split()
                    if word
                    in [
                        "strategic",
                        "organizational",
                        "transformation",
                        "platform",
                        "architecture",
                        "stakeholder",
                        "executive",
                        "cross-functional",
                    ]
                ]
            ),
            "question_complexity": len(user_input.split("?")),
            "context_richness": len(context.recent_interactions) if context else 0,
            "multi_domain_indicators": len(
                [
                    word
                    for word in user_input.lower().split()
                    if word
                    in [
                        "technical",
                        "business",
                        "people",
                        "process",
                        "technology",
                        "culture",
                    ]
                ]
            ),
        }

        # Calculate complexity score
        complexity_score = (
            complexity_indicators["strategic_keywords"] * 0.3
            + complexity_indicators["question_complexity"] * 0.2
            + complexity_indicators["context_richness"] * 0.1
            + complexity_indicators["multi_domain_indicators"] * 0.4
        ) / 10.0  # Normalize to 0-1

        # Map to complexity levels
        if complexity_score >= self.coordination_thresholds["enterprise_threshold"]:
            return CoordinationComplexity.ENTERPRISE
        elif (
            complexity_score
            >= self.coordination_thresholds["multi_framework_threshold"]
        ):
            return CoordinationComplexity.MULTI
        elif (
            complexity_score >= self.coordination_thresholds["dual_framework_threshold"]
        ):
            return CoordinationComplexity.DUAL
        else:
            return CoordinationComplexity.SINGLE

    async def _detect_required_frameworks(
        self,
        user_input: str,
        context: ConversationContext,
        complexity: CoordinationComplexity,
    ) -> List[str]:
        """Detect which frameworks are required based on input and complexity"""
        # Use existing MultiFrameworkIntegrationEngine to get base framework suggestions
        base_frameworks = (
            self.multi_framework_engine.base_engine.detect_applicable_frameworks(
                user_input
            )
        )

        # Adjust based on complexity
        if complexity == CoordinationComplexity.SINGLE:
            return base_frameworks[:1]
        elif complexity == CoordinationComplexity.DUAL:
            return base_frameworks[:2]
        elif complexity == CoordinationComplexity.MULTI:
            return base_frameworks[:4]
        else:  # ENTERPRISE
            return base_frameworks[:6]

    async def _identify_framework_conflicts(
        self,
        frameworks: List[str],
        user_input: str,
        context: ConversationContext,
    ) -> List[FrameworkConflict]:
        """Identify potential conflicts between selected frameworks"""
        conflicts = []

        for i, framework_a in enumerate(frameworks):
            for framework_b in frameworks[i + 1 :]:
                # Check for known conflicting patterns
                conflict = self._analyze_framework_pair_conflict(
                    framework_a, framework_b, user_input
                )
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _analyze_framework_pair_conflict(
        self, framework_a: str, framework_b: str, user_input: str
    ) -> Optional[FrameworkConflict]:
        """Analyze potential conflict between two frameworks"""
        # Known conflicting pairs and their characteristics
        conflict_patterns = {
            ("rumelt_strategy_kernel", "team_topologies"): {
                "type": "approach",
                "severity": 0.4,
                "strategy": "complementary_integration",
            },
            ("decisive_wrap_framework", "crucial_conversations"): {
                "type": "priority",
                "severity": 0.6,
                "strategy": "context_analysis",
            },
            ("accelerate_team_performance", "organizational_transformation"): {
                "type": "timeline",
                "severity": 0.5,
                "strategy": "phased_implementation",
            },
        }

        # Check both directions
        conflict_key = (framework_a, framework_b)
        reverse_key = (framework_b, framework_a)

        conflict_info = conflict_patterns.get(conflict_key) or conflict_patterns.get(
            reverse_key
        )

        if conflict_info:
            return FrameworkConflict(
                framework_a=framework_a,
                framework_b=framework_b,
                conflict_type=conflict_info["type"],
                severity=conflict_info["severity"],
                resolution_strategy=conflict_info["strategy"],
                mcp_resolution_needed=conflict_info["severity"]
                > self.coordination_thresholds["conflict_severity_threshold"],
            )

        return None

    async def _enhance_frameworks_with_mcp(
        self,
        frameworks: List[str],
        user_input: str,
        session_id: str,
        persona: str,
    ) -> Dict[str, FrameworkDetectionResult]:
        """Enhance individual frameworks using MCPEnhancedFrameworkEngine"""
        enhanced_results = {}

        for framework in frameworks:
            try:
                # Create framework-specific input for enhancement
                framework_input = f"Apply {framework} framework to: {user_input}"

                # Use MCPEnhancedFrameworkEngine for individual enhancement
                enhancement_result = (
                    await self.mcp_enhanced_engine.enhance_framework_detection(
                        framework_input, session_id, persona
                    )
                )

                enhanced_results[framework] = enhancement_result

            except Exception as e:
                logger.warning(
                    "framework_enhancement_failed",
                    framework=framework,
                    error=str(e),
                )
                # Create fallback result
                enhanced_results[framework] = FrameworkDetectionResult(
                    detected_frameworks=[framework],
                    confidence_scores={framework: 0.75},
                    mcp_enhancements_applied=[],
                    baseline_accuracy=0.875,
                    enhanced_accuracy=0.875,
                    improvement_percentage=0.0,
                )

        return enhanced_results

    async def _resolve_conflicts_with_mcp(
        self,
        conflicts: List[FrameworkConflict],
        enhanced_frameworks: Dict[str, FrameworkDetectionResult],
        user_input: str,
        persona: str,
    ) -> List[FrameworkConflict]:
        """Resolve framework conflicts using MCP intelligence"""
        resolved_conflicts = []

        for conflict in conflicts:
            if conflict.mcp_resolution_needed:
                try:
                    # Get resolution strategy
                    strategy = self.conflict_resolution_strategies.get(
                        conflict.conflict_type,
                        self.conflict_resolution_strategies["approach_conflict"],
                    )

                    # Apply MCP-based resolution
                    resolved_conflict = await self._apply_mcp_conflict_resolution(
                        conflict, strategy, user_input, persona
                    )

                    resolved_conflicts.append(resolved_conflict)

                except Exception as e:
                    logger.warning(
                        "conflict_resolution_failed",
                        conflict_type=conflict.conflict_type,
                        error=str(e),
                    )
                    # Keep original conflict with reduced severity
                    conflict.severity *= 0.7
                    resolved_conflicts.append(conflict)
            else:
                # Simple resolution without MCP
                conflict.resolution_strategy = "baseline_integration"
                resolved_conflicts.append(conflict)

        return resolved_conflicts

    async def _apply_mcp_conflict_resolution(
        self,
        conflict: FrameworkConflict,
        strategy: Dict[str, Any],
        user_input: str,
        persona: str,
    ) -> FrameworkConflict:
        """Apply MCP-based conflict resolution strategy"""
        # Create MCP query for conflict resolution
        resolution_query = f"""
        Resolve conflict between {conflict.framework_a} and {conflict.framework_b}
        Conflict type: {conflict.conflict_type}
        Context: {user_input}
        Strategy: {strategy['resolution_method']}
        """

        # Apply MCP enhancement based on strategy
        if strategy["mcp_server"] == "sequential":
            # Use Sequential MCP for systematic analysis
            mcp_result = await self.mcp_helper.enhance_with_sequential(
                resolution_query, persona, "conflict_resolution"
            )
        elif strategy["mcp_server"] == "context7":
            # Use Context7 MCP for pattern-based resolution
            mcp_result = await self.mcp_helper.enhance_with_context7(
                resolution_query, persona, "pattern_analysis"
            )
        else:  # both servers
            # Use both servers for comprehensive resolution
            sequential_result = await self.mcp_helper.enhance_with_sequential(
                resolution_query, persona, "systematic_analysis"
            )
            context7_result = await self.mcp_helper.enhance_with_context7(
                resolution_query, persona, "pattern_validation"
            )
            mcp_result = f"Sequential: {sequential_result}\nContext7: {context7_result}"

        # Update conflict with resolution
        conflict.resolution_strategy = f"mcp_{strategy['strategy']}"
        conflict.severity *= 0.5  # Reduce severity after MCP resolution
        conflict.mcp_resolution_needed = False

        return conflict

    async def _synthesize_coordinated_frameworks(
        self,
        enhanced_frameworks: Dict[str, FrameworkDetectionResult],
        resolved_conflicts: List[FrameworkConflict],
        complexity: CoordinationComplexity,
        persona: str,
    ) -> Dict[str, Any]:
        """Synthesize multiple enhanced frameworks into coordinated result"""
        # Determine primary and supporting frameworks based on confidence
        framework_scores = {
            name: max(result.confidence_scores.values())
            for name, result in enhanced_frameworks.items()
        }

        sorted_frameworks = sorted(
            framework_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Split into primary and supporting based on complexity
        if complexity == CoordinationComplexity.SINGLE:
            primary_frameworks = [sorted_frameworks[0][0]]
            supporting_frameworks = []
        elif complexity == CoordinationComplexity.DUAL:
            primary_frameworks = [f[0] for f in sorted_frameworks[:1]]
            supporting_frameworks = [f[0] for f in sorted_frameworks[1:2]]
        else:
            primary_frameworks = [f[0] for f in sorted_frameworks[:2]]
            supporting_frameworks = [f[0] for f in sorted_frameworks[2:]]

        # Calculate synthesis confidence
        base_confidence = sum(framework_scores.values()) / len(framework_scores)
        conflict_penalty = sum(c.severity for c in resolved_conflicts) * 0.1
        mcp_boost = (
            len(
                [
                    result
                    for result in enhanced_frameworks.values()
                    if result.mcp_enhancements_applied
                ]
            )
            * 0.05
        )

        synthesis_confidence = min(base_confidence - conflict_penalty + mcp_boost, 1.0)

        # Collect MCP enhancements applied
        mcp_enhancements = []
        for result in enhanced_frameworks.values():
            mcp_enhancements.extend(result.mcp_enhancements_applied)

        return {
            "primary_frameworks": primary_frameworks,
            "supporting_frameworks": supporting_frameworks,
            "confidence": synthesis_confidence,
            "mcp_enhancements": list(set(mcp_enhancements)),  # Remove duplicates
        }

    def _generate_coordination_disclosures(
        self,
        complexity: CoordinationComplexity,
        conflicts: List[FrameworkConflict],
        enhanced_frameworks: Dict[str, FrameworkDetectionResult],
        persona: str,
    ) -> List[MCPDisclosure]:
        """Generate transparency disclosures for coordination process"""
        disclosures = []

        # Complexity disclosure
        if complexity in [
            CoordinationComplexity.MULTI,
            CoordinationComplexity.ENTERPRISE,
        ]:
            disclosures.append(
                self.transparency_system.create_mcp_enhancement_disclosure(
                    server_name="coordination_engine",
                    capability="multi_framework_orchestration",
                    persona=persona,
                    processing_message=f"Coordinating {len(enhanced_frameworks)} frameworks with {complexity.value} complexity",
                )
            )

        # Conflict resolution disclosures
        mcp_resolved_conflicts = [
            c for c in conflicts if "mcp_" in c.resolution_strategy
        ]
        if mcp_resolved_conflicts:
            disclosures.append(
                self.transparency_system.create_mcp_enhancement_disclosure(
                    server_name="conflict_resolver",
                    capability="mcp_conflict_resolution",
                    persona=persona,
                    processing_message=f"Resolving {len(mcp_resolved_conflicts)} framework conflicts using MCP intelligence",
                )
            )

        return disclosures

    def _update_coordinator_metrics(
        self,
        complexity: CoordinationComplexity,
        conflicts_resolved: int,
        processing_time: float,
    ) -> None:
        """Update coordinator performance metrics"""
        self.coordinator_metrics["coordinations_processed"] += 1
        self.coordinator_metrics["conflicts_resolved"] += conflicts_resolved

        if complexity in [
            CoordinationComplexity.MULTI,
            CoordinationComplexity.ENTERPRISE,
        ]:
            self.coordinator_metrics["mcp_orchestrations_executed"] += 1

        # Update rolling averages
        current_count = self.coordinator_metrics["coordinations_processed"]
        current_avg_time = self.coordinator_metrics["avg_coordination_time_ms"]

        self.coordinator_metrics["avg_coordination_time_ms"] = (
            current_avg_time * (current_count - 1) + processing_time
        ) / current_count

    def _create_fallback_coordination_result(
        self, user_input: str, persona: str
    ) -> CoordinationResult:
        """Create fallback coordination result when main process fails"""
        return CoordinationResult(
            primary_frameworks=["rumelt_strategy_kernel"],  # Safe default
            supporting_frameworks=[],
            coordination_complexity=CoordinationComplexity.SINGLE,
            conflicts_resolved=[],
            mcp_enhancements_applied=[],
            synthesis_confidence=0.60,  # Lower confidence for fallback
            processing_time_ms=50.0,
            transparency_disclosures=[
                self.transparency_system.create_mcp_enhancement_disclosure(
                    server_name="fallback_coordinator",
                    capability="basic_framework_selection",
                    persona=persona,
                    processing_message="Using fallback coordination due to processing error",
                )
            ],
        )

    def get_coordinator_metrics(self) -> Dict[str, Any]:
        """Get current coordinator performance metrics"""
        return {
            **self.coordinator_metrics,
            "coordination_success_rate": (
                self.coordinator_metrics["coordinations_processed"]
                - len([m for m in self.coordinator_metrics if "fallback" in str(m)])
            )
            / max(self.coordinator_metrics["coordinations_processed"], 1),
            "avg_conflicts_per_coordination": (
                self.coordinator_metrics["conflicts_resolved"]
                / max(self.coordinator_metrics["coordinations_processed"], 1)
            ),
        }


def create_framework_mcp_coordinator(
    multi_framework_engine: MultiFrameworkIntegrationEngine,
    mcp_enhanced_engine: MCPEnhancedFrameworkEngine,
    mcp_helper: RealMCPIntegrationHelper,
    transparency_system: IntegratedTransparencySystem,
) -> FrameworkMCPCoordinator:
    """
    Factory function to create FrameworkMCPCoordinator with proper dependencies

    Args:
        multi_framework_engine: Existing MultiFrameworkIntegrationEngine
        mcp_enhanced_engine: MCPEnhancedFrameworkEngine for individual enhancements
        mcp_helper: Real MCP server integration helper
        transparency_system: Integrated transparency system

    Returns:
        Configured FrameworkMCPCoordinator instance
    """
    return FrameworkMCPCoordinator(
        multi_framework_engine=multi_framework_engine,
        mcp_enhanced_engine=mcp_enhanced_engine,
        mcp_helper=mcp_helper,
        transparency_system=transparency_system,
    )
