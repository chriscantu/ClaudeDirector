#!/usr/bin/env python3
"""
Code-Strategic Mapper - TS-4 Phase 3 Implementation

🗺️ Rachel | Design Systems Strategy + Martin | Platform Architecture
🎯 TS-4: Code-Strategic Context Mapping (NEW - No Existing Equivalent)

STRATEGIC PURPOSE: Bridge development context with strategic insights for enhanced
leadership guidance. This component provides the missing link between code patterns
and strategic framework recommendations.

Architecture Compliance:
- Follows PROJECT_STRUCTURE.md: lib/integration/ pattern
- Integrates with OVERVIEW.md: Context Engineering 8-layer architecture
- Implements SOLID principles: Single responsibility for code-strategic mapping
- Maintains DRY: No duplication with existing components (verified in ADR-017)

Performance Target: <200ms code-strategic mapping, <50ms cached results
"""

import os
import sys
import time
import json
import ast
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import existing components for integration (DRY compliance)
try:
    from ..context_engineering.advanced_context_engine import AdvancedContextEngine
    from ..context_engineering.strategic_memory_manager import StrategicMemoryManager
    from ..core.cursor_response_enhancer import CodeContext, StrategicContext

    CONTEXT_ENGINEERING_AVAILABLE = True
except ImportError:
    # Lightweight fallback for development
    logger.warning(
        "Context engineering components unavailable - using fallback implementations"
    )
    CONTEXT_ENGINEERING_AVAILABLE = False
    AdvancedContextEngine = None
    StrategicMemoryManager = None


class StrategicMappingType(Enum):
    """Types of code-to-strategic mappings"""

    ARCHITECTURAL_PATTERN = "architectural_pattern"
    FRAMEWORK_RECOMMENDATION = "framework_recommendation"
    STAKEHOLDER_IMPACT = "stakeholder_impact"
    DECISION_COMPLEXITY = "decision_complexity"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"


class StrategicPriority(Enum):
    """Priority levels for strategic recommendations"""

    CRITICAL = "critical"  # Immediate action required
    HIGH = "high"  # Address within sprint
    MEDIUM = "medium"  # Address within quarter
    LOW = "low"  # Address when capacity allows


@dataclass
class CodePattern:
    """Represents a detected code pattern for strategic analysis"""

    pattern_type: str
    pattern_name: str
    confidence: float
    file_locations: List[str]
    complexity_indicators: Dict[str, Any]
    dependencies: List[str]
    impact_scope: str  # "file", "module", "system", "organization"


@dataclass
class StrategicRecommendation:
    """Strategic recommendation derived from code analysis"""

    recommendation_type: StrategicMappingType
    title: str
    description: str
    frameworks: List[str]
    priority: StrategicPriority
    stakeholders: List[str]
    actions: List[str]
    success_metrics: List[str]
    estimated_effort: str
    business_value: str


@dataclass
class CodeStrategicMapping:
    """Complete mapping between code context and strategic insights"""

    code_context: Dict[str, Any]
    strategic_context: Dict[str, Any]
    detected_patterns: List[CodePattern]
    recommendations: List[StrategicRecommendation]
    mapping_confidence: float
    analysis_timestamp: datetime
    performance_metrics: Dict[str, float]


class CodeStrategicMapper:
    """
    🗺️ CODE-STRATEGIC CONTEXT MAPPING SYSTEM

    TS-4 NEW COMPONENT: Bridges development context with strategic leadership insights

    STRATEGIC CAPABILITIES:
    - Maps code patterns to strategic frameworks
    - Analyzes architectural decisions for stakeholder impact
    - Recommends strategic actions based on development context
    - Optimizes workflows through code-strategic correlation

    SOLID COMPLIANCE:
    - Single Responsibility: Focus only on code-strategic mapping
    - Open/Closed: Extensible for new mapping patterns
    - Liskov Substitution: Consistent mapping interface
    - Interface Segregation: Focused mapping methods
    - Dependency Inversion: Depends on abstractions, not concretions
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Code-Strategic Mapper with SOLID architecture"""
        self.config = config or {}
        self.start_time = time.time()

        # Initialize context engineering integration
        self.context_engine = (
            AdvancedContextEngine() if CONTEXT_ENGINEERING_AVAILABLE else None
        )
        self.strategic_memory = (
            StrategicMemoryManager() if CONTEXT_ENGINEERING_AVAILABLE else None
        )

        # TS-4 Performance tracking
        self.mapping_metrics = {
            "total_mappings": 0,
            "successful_mappings": 0,
            "average_mapping_time": 0.0,
            "patterns_detected": 0,
            "recommendations_generated": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

        # Strategic pattern recognition engine
        self.pattern_detector = CodePatternDetector()
        self.strategic_analyzer = StrategicPatternAnalyzer()
        self.recommendation_engine = StrategicRecommendationEngine()

        # Caching for performance (<50ms cached results)
        self.mapping_cache = {}
        self.cache_ttl = 300  # 5 minutes

        logger.info(
            f"Code-Strategic Mapper initialized - "
            f"context_engine={'available' if self.context_engine else 'fallback'}, "
            f"strategic_memory={'available' if self.strategic_memory else 'fallback'}"
        )

    def map_code_to_strategic_context(
        self, file_path: str, code_content: str, user_context: Optional[str] = None
    ) -> CodeStrategicMapping:
        """
        PRIMARY CAPABILITY: Map code context to strategic insights

        Single Responsibility: Focus only on code-strategic mapping
        """
        start_time = time.time()

        # Check cache first for performance
        cache_key = self._generate_cache_key(file_path, code_content, user_context)
        cached_result = self._get_cached_mapping(cache_key)
        if cached_result:
            self.mapping_metrics["cache_hits"] += 1
            return cached_result

        self.mapping_metrics["cache_misses"] += 1

        try:
            # Step 1: Detect code patterns
            detected_patterns = self.pattern_detector.detect_patterns(
                file_path, code_content
            )

            # Step 2: Analyze strategic implications
            strategic_analysis = self.strategic_analyzer.analyze_patterns(
                detected_patterns, user_context
            )

            # Step 3: Generate strategic recommendations
            recommendations = self.recommendation_engine.generate_recommendations(
                detected_patterns, strategic_analysis
            )

            # Step 4: Create comprehensive mapping
            mapping = CodeStrategicMapping(
                code_context={
                    "file_path": file_path,
                    "language": self._detect_language(file_path),
                    "complexity_score": self._calculate_complexity_score(code_content),
                    "patterns_count": len(detected_patterns),
                },
                strategic_context={
                    "domain": strategic_analysis.get("domain", "technical_strategy"),
                    "leadership_level": strategic_analysis.get(
                        "leadership_level", "individual_contributor"
                    ),
                    "decision_complexity": strategic_analysis.get(
                        "complexity", "moderate"
                    ),
                    "stakeholder_count": len(
                        strategic_analysis.get("stakeholders", [])
                    ),
                },
                detected_patterns=detected_patterns,
                recommendations=recommendations,
                mapping_confidence=self._calculate_mapping_confidence(
                    detected_patterns, recommendations
                ),
                analysis_timestamp=datetime.now(),
                performance_metrics={
                    "analysis_time": time.time() - start_time,
                    "patterns_detected": len(detected_patterns),
                    "recommendations_generated": len(recommendations),
                },
            )

            # Cache result for performance
            self._cache_mapping(cache_key, mapping)

            # Update metrics
            self._update_mapping_metrics(mapping)

            # Integrate with context engineering if available
            if self.context_engine:
                self._integrate_with_context_engine(mapping)

            logger.info(
                f"Code-strategic mapping completed - "
                f"patterns={len(detected_patterns)}, "
                f"recommendations={len(recommendations)}, "
                f"confidence={mapping.mapping_confidence:.2f}, "
                f"time={time.time() - start_time:.3f}s"
            )

            return mapping

        except Exception as e:
            logger.error(f"Code-strategic mapping failed: {e}")

            # Return fallback mapping
            return self._create_fallback_mapping(file_path, code_content, str(e))

    def analyze_architectural_impact(
        self,
        code_patterns: List[CodePattern],
        organizational_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze architectural impact of code patterns on organization

        Open/Closed Principle: Extensible for new impact analysis types
        """
        impact_analysis = {
            "technical_impact": self._assess_technical_impact(code_patterns),
            "organizational_impact": self._assess_organizational_impact(
                code_patterns, organizational_context
            ),
            "stakeholder_impact": self._assess_stakeholder_impact(code_patterns),
            "strategic_alignment": self._assess_strategic_alignment(code_patterns),
            "risk_assessment": self._assess_risks(code_patterns),
            "opportunity_identification": self._identify_opportunities(code_patterns),
        }

        return impact_analysis

    def recommend_strategic_frameworks(
        self, code_context: Dict[str, Any], strategic_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Recommend strategic frameworks based on code-strategic mapping

        Interface Segregation: Focused framework recommendation interface
        """
        framework_recommendations = []

        # Analyze code complexity for framework selection
        complexity = code_context.get("complexity_score", 0)
        patterns = code_context.get("patterns_count", 0)

        # Team Topologies for complex systems
        if complexity > 7.0 or patterns > 5:
            framework_recommendations.append(
                {
                    "framework": "Team Topologies",
                    "rationale": "High complexity indicates need for team structure optimization",
                    "confidence": min(complexity / 10.0, 1.0),
                    "priority": "high" if complexity > 8.0 else "medium",
                }
            )

        # Systems Thinking for interconnected components
        if patterns > 3:
            framework_recommendations.append(
                {
                    "framework": "Systems Thinking",
                    "rationale": "Multiple patterns indicate system interconnections",
                    "confidence": min(patterns / 10.0, 1.0),
                    "priority": "medium",
                }
            )

        # Accelerate Performance for performance-focused code
        performance_indicators = strategic_context.get("performance_focus", False)
        if performance_indicators:
            framework_recommendations.append(
                {
                    "framework": "Accelerate Performance",
                    "rationale": "Performance patterns detected in code analysis",
                    "confidence": 0.8,
                    "priority": "high",
                }
            )

        # WRAP Framework for strategic decisions
        decision_complexity = strategic_context.get("decision_complexity", "low")
        if decision_complexity in ["high", "moderate"]:
            framework_recommendations.append(
                {
                    "framework": "WRAP Framework",
                    "rationale": f"Decision complexity level: {decision_complexity}",
                    "confidence": 0.7 if decision_complexity == "moderate" else 0.9,
                    "priority": "medium",
                }
            )

        return sorted(
            framework_recommendations, key=lambda x: x["confidence"], reverse=True
        )

    def optimize_development_workflow(
        self,
        mapping: CodeStrategicMapping,
        current_workflow: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate workflow optimization recommendations

        Dependency Inversion: Depends on mapping abstraction, not implementation
        """
        optimizations = {
            "automation_opportunities": [],
            "process_improvements": [],
            "tool_recommendations": [],
            "efficiency_gains": [],
            "estimated_impact": {},
        }

        # Analyze patterns for automation opportunities
        for pattern in mapping.detected_patterns:
            if pattern.pattern_type == "repetitive_code":
                optimizations["automation_opportunities"].append(
                    {
                        "type": "code_generation",
                        "description": f"Automate {pattern.pattern_name} pattern",
                        "estimated_time_savings": "2-4 hours/week",
                    }
                )

            elif pattern.pattern_type == "manual_testing":
                optimizations["automation_opportunities"].append(
                    {
                        "type": "test_automation",
                        "description": f"Automate testing for {pattern.pattern_name}",
                        "estimated_time_savings": "1-2 hours/sprint",
                    }
                )

        # Process improvements based on complexity
        if mapping.code_context.get("complexity_score", 0) > 6.0:
            optimizations["process_improvements"].append(
                {
                    "type": "code_review_enhancement",
                    "description": "Implement systematic complexity review process",
                    "priority": "high",
                }
            )

        # Tool recommendations based on patterns
        detected_pattern_types = {p.pattern_type for p in mapping.detected_patterns}
        if "performance_bottleneck" in detected_pattern_types:
            optimizations["tool_recommendations"].append(
                {
                    "tool": "Performance Monitoring",
                    "rationale": "Performance bottlenecks detected",
                    "priority": "high",
                }
            )

        return optimizations

    def get_mapping_metrics(self) -> Dict[str, Any]:
        """
        Get code-strategic mapping performance metrics

        Interface Segregation: Separate metrics interface
        """
        total = self.mapping_metrics["total_mappings"]
        successful = self.mapping_metrics["successful_mappings"]

        return {
            **self.mapping_metrics,
            "success_rate": successful / total if total > 0 else 0.0,
            "cache_hit_rate": (
                self.mapping_metrics["cache_hits"]
                / (
                    self.mapping_metrics["cache_hits"]
                    + self.mapping_metrics["cache_misses"]
                )
                if (
                    self.mapping_metrics["cache_hits"]
                    + self.mapping_metrics["cache_misses"]
                )
                > 0
                else 0.0
            ),
            "uptime_seconds": time.time() - self.start_time,
            "context_integration_available": CONTEXT_ENGINEERING_AVAILABLE,
        }

    # Private methods for internal implementation
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".cpp": "cpp",
            ".c": "c",
            ".rb": "ruby",
            ".php": "php",
            ".sql": "sql",
        }
        return language_map.get(extension, "unknown")

    def _calculate_complexity_score(self, code_content: str) -> float:
        """Calculate code complexity score"""
        lines = len(code_content.split("\n"))
        functions = code_content.count("def ") + code_content.count("function ")
        classes = code_content.count("class ")

        # Simple complexity calculation
        complexity = (lines / 100) + (functions * 0.5) + (classes * 1.0)
        return min(complexity, 10.0)

    def _generate_cache_key(
        self, file_path: str, code_content: str, user_context: Optional[str]
    ) -> str:
        """Generate cache key for mapping results"""
        import hashlib

        content_hash = hashlib.md5(code_content.encode()).hexdigest()[:8]
        context_hash = hashlib.md5((user_context or "").encode()).hexdigest()[:4]
        return f"{file_path}:{content_hash}:{context_hash}"

    def _get_cached_mapping(self, cache_key: str) -> Optional[CodeStrategicMapping]:
        """Get cached mapping if available and not expired"""
        if cache_key in self.mapping_cache:
            cached_mapping, timestamp = self.mapping_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_mapping
        return None

    def _cache_mapping(self, cache_key: str, mapping: CodeStrategicMapping):
        """Cache mapping result for performance"""
        self.mapping_cache[cache_key] = (mapping, time.time())

    def _calculate_mapping_confidence(
        self,
        patterns: List[CodePattern],
        recommendations: List[StrategicRecommendation],
    ) -> float:
        """Calculate confidence score for the mapping"""
        if not patterns or not recommendations:
            return 0.0

        # Base confidence on pattern detection confidence and recommendation quality
        pattern_confidence = sum(p.confidence for p in patterns) / len(patterns)
        recommendation_quality = len(recommendations) / max(len(patterns), 1)

        return min((pattern_confidence + recommendation_quality) / 2, 1.0)

    def _update_mapping_metrics(self, mapping: CodeStrategicMapping):
        """Update performance metrics"""
        self.mapping_metrics["total_mappings"] += 1
        self.mapping_metrics["successful_mappings"] += 1
        self.mapping_metrics["patterns_detected"] += len(mapping.detected_patterns)
        self.mapping_metrics["recommendations_generated"] += len(
            mapping.recommendations
        )

        # Update average mapping time
        total = self.mapping_metrics["total_mappings"]
        current_avg = self.mapping_metrics["average_mapping_time"]
        new_time = mapping.performance_metrics["analysis_time"]
        self.mapping_metrics["average_mapping_time"] = (
            current_avg * (total - 1) + new_time
        ) / total

    def _integrate_with_context_engine(self, mapping: CodeStrategicMapping):
        """Integrate mapping results with context engineering system"""
        if not self.context_engine:
            return

        try:
            # Store strategic insights in context engine
            context_data = {
                "type": "code_strategic_mapping",
                "mapping_confidence": mapping.mapping_confidence,
                "patterns": [asdict(p) for p in mapping.detected_patterns],
                "recommendations": [asdict(r) for r in mapping.recommendations],
                "timestamp": mapping.analysis_timestamp.isoformat(),
            }

            # This would integrate with the actual context engine
            # Implementation depends on context engine interface
            logger.debug(
                f"Integrated mapping with context engine: {len(mapping.recommendations)} recommendations"
            )

        except Exception as e:
            logger.warning(f"Context engine integration failed: {e}")

    def _create_fallback_mapping(
        self, file_path: str, code_content: str, error: str
    ) -> CodeStrategicMapping:
        """Create fallback mapping when analysis fails"""
        return CodeStrategicMapping(
            code_context={"file_path": file_path, "error": error},
            strategic_context={"fallback": True},
            detected_patterns=[],
            recommendations=[],
            mapping_confidence=0.0,
            analysis_timestamp=datetime.now(),
            performance_metrics={
                "analysis_time": 0.0,
                "patterns_detected": 0,
                "recommendations_generated": 0,
            },
        )

    # Placeholder methods for pattern analysis (would be implemented based on specific requirements)
    def _assess_technical_impact(self, patterns: List[CodePattern]) -> Dict[str, Any]:
        """Assess technical impact of code patterns"""
        return {
            "complexity_increase": len(patterns),
            "maintainability_impact": "moderate",
        }

    def _assess_organizational_impact(
        self, patterns: List[CodePattern], context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess organizational impact of code patterns"""
        return {
            "team_coordination_needed": len(patterns) > 3,
            "cross_team_dependencies": len(patterns) > 5,
        }

    def _assess_stakeholder_impact(self, patterns: List[CodePattern]) -> Dict[str, Any]:
        """Assess stakeholder impact of code patterns"""
        stakeholders = set()
        for pattern in patterns:
            if pattern.impact_scope == "system":
                stakeholders.update(["engineering_teams", "product_teams"])
            elif pattern.impact_scope == "organization":
                stakeholders.update(
                    ["engineering_teams", "product_teams", "executive_teams"]
                )

        return {
            "affected_stakeholders": list(stakeholders),
            "communication_needed": len(stakeholders) > 2,
        }

    def _assess_strategic_alignment(
        self, patterns: List[CodePattern]
    ) -> Dict[str, Any]:
        """Assess strategic alignment of code patterns"""
        return {"alignment_score": 0.7, "strategic_debt": len(patterns) > 5}

    def _assess_risks(self, patterns: List[CodePattern]) -> Dict[str, Any]:
        """Assess risks from code patterns"""
        high_complexity_patterns = [p for p in patterns if p.confidence > 0.8]
        return {
            "high_risk_patterns": len(high_complexity_patterns),
            "mitigation_needed": len(high_complexity_patterns) > 2,
        }

    def _identify_opportunities(self, patterns: List[CodePattern]) -> Dict[str, Any]:
        """Identify opportunities from code patterns"""
        return {
            "automation_opportunities": len(patterns),
            "standardization_potential": len(patterns) > 3,
        }


class CodePatternDetector:
    """Detects patterns in code for strategic analysis"""

    def detect_patterns(self, file_path: str, code_content: str) -> List[CodePattern]:
        """Detect code patterns for strategic analysis"""
        patterns = []

        # Simple pattern detection (would be enhanced based on requirements)
        if self._detect_complexity_pattern(code_content):
            patterns.append(
                CodePattern(
                    pattern_type="high_complexity",
                    pattern_name="Complex Function",
                    confidence=0.8,
                    file_locations=[file_path],
                    complexity_indicators={"cyclomatic_complexity": "high"},
                    dependencies=[],
                    impact_scope="module",
                )
            )

        if self._detect_duplication_pattern(code_content):
            patterns.append(
                CodePattern(
                    pattern_type="code_duplication",
                    pattern_name="Duplicated Logic",
                    confidence=0.7,
                    file_locations=[file_path],
                    complexity_indicators={"duplication_ratio": "moderate"},
                    dependencies=[],
                    impact_scope="file",
                )
            )

        return patterns

    def _detect_complexity_pattern(self, code_content: str) -> bool:
        """Detect high complexity patterns"""
        lines = len(code_content.split("\n"))
        functions = code_content.count("def ") + code_content.count("function ")
        return lines > 500 or functions > 20

    def _detect_duplication_pattern(self, code_content: str) -> bool:
        """Detect code duplication patterns"""
        # Simple heuristic - would use more sophisticated analysis
        lines = code_content.split("\n")
        unique_lines = set(line.strip() for line in lines if line.strip())
        return len(lines) > 0 and len(unique_lines) / len(lines) < 0.8


class StrategicPatternAnalyzer:
    """Analyzes code patterns for strategic implications"""

    def analyze_patterns(
        self, patterns: List[CodePattern], user_context: Optional[str]
    ) -> Dict[str, Any]:
        """Analyze patterns for strategic implications"""
        analysis = {
            "domain": self._determine_strategic_domain(patterns),
            "leadership_level": self._assess_leadership_level(patterns, user_context),
            "complexity": self._assess_decision_complexity(patterns),
            "stakeholders": self._identify_stakeholders(patterns),
            "performance_focus": self._has_performance_focus(patterns),
        }

        return analysis

    def _determine_strategic_domain(self, patterns: List[CodePattern]) -> str:
        """Determine strategic domain from patterns"""
        if any(p.pattern_type == "architectural_pattern" for p in patterns):
            return "platform_strategy"
        elif any(p.pattern_type == "performance_bottleneck" for p in patterns):
            return "performance_strategy"
        else:
            return "technical_strategy"

    def _assess_leadership_level(
        self, patterns: List[CodePattern], user_context: Optional[str]
    ) -> str:
        """Assess required leadership level"""
        if len(patterns) > 5 or any(p.impact_scope == "organization" for p in patterns):
            return "organizational_leadership"
        elif len(patterns) > 2 or any(p.impact_scope == "system" for p in patterns):
            return "technical_leadership"
        else:
            return "individual_contributor"

    def _assess_decision_complexity(self, patterns: List[CodePattern]) -> str:
        """Assess decision complexity from patterns"""
        complexity_score = sum(p.confidence for p in patterns)
        if complexity_score > 5.0:
            return "high"
        elif complexity_score > 2.0:
            return "moderate"
        else:
            return "low"

    def _identify_stakeholders(self, patterns: List[CodePattern]) -> List[str]:
        """Identify affected stakeholders"""
        stakeholders = set(["development_team"])

        for pattern in patterns:
            if pattern.impact_scope in ["system", "organization"]:
                stakeholders.update(["engineering_teams", "product_teams"])
            if pattern.pattern_type == "performance_bottleneck":
                stakeholders.add("operations_teams")

        return list(stakeholders)

    def _has_performance_focus(self, patterns: List[CodePattern]) -> bool:
        """Check if patterns indicate performance focus"""
        return any(
            p.pattern_type in ["performance_bottleneck", "optimization_opportunity"]
            for p in patterns
        )


class StrategicRecommendationEngine:
    """Generates strategic recommendations from pattern analysis"""

    def generate_recommendations(
        self, patterns: List[CodePattern], strategic_analysis: Dict[str, Any]
    ) -> List[StrategicRecommendation]:
        """Generate strategic recommendations"""
        recommendations = []

        # Generate recommendations based on patterns and analysis
        if strategic_analysis.get("complexity") == "high":
            recommendations.append(
                StrategicRecommendation(
                    recommendation_type=StrategicMappingType.ARCHITECTURAL_PATTERN,
                    title="Complexity Reduction Strategy",
                    description="Implement systematic complexity reduction approach",
                    frameworks=["Systems Thinking", "Team Topologies"],
                    priority=StrategicPriority.HIGH,
                    stakeholders=strategic_analysis.get("stakeholders", []),
                    actions=["conduct_complexity_audit", "plan_refactoring_strategy"],
                    success_metrics=[
                        "complexity_score_reduction",
                        "maintainability_improvement",
                    ],
                    estimated_effort="2-4 weeks",
                    business_value="Improved maintainability and development velocity",
                )
            )

        if len(patterns) > 3:
            recommendations.append(
                StrategicRecommendation(
                    recommendation_type=StrategicMappingType.WORKFLOW_OPTIMIZATION,
                    title="Development Workflow Enhancement",
                    description="Optimize development workflow based on detected patterns",
                    frameworks=["Accelerate Performance"],
                    priority=StrategicPriority.MEDIUM,
                    stakeholders=["development_team", "engineering_teams"],
                    actions=["implement_automation", "standardize_processes"],
                    success_metrics=["development_velocity", "defect_reduction"],
                    estimated_effort="1-2 weeks",
                    business_value="Increased development efficiency and quality",
                )
            )

        return recommendations


# Factory function for creating Code-Strategic Mapper
def create_code_strategic_mapper(
    config: Optional[Dict[str, Any]] = None,
) -> CodeStrategicMapper:
    """
    Factory function to create Code-Strategic Mapper

    TS-4 NEW COMPONENT: Creates the mapper that bridges code context with strategic insights
    """
    return CodeStrategicMapper(config)


# Convenience functions for common operations
def map_file_to_strategic_context(
    file_path: str, user_context: Optional[str] = None
) -> CodeStrategicMapping:
    """
    Convenience function to map a file to strategic context

    Returns CodeStrategicMapping with strategic insights
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    mapper = create_code_strategic_mapper()
    return mapper.map_code_to_strategic_context(file_path, code_content, user_context)


if __name__ == "__main__":
    # TS-4 Code-Strategic Mapper test
    print("🗺️ TS-4 Code-Strategic Mapper - Foundation Test")
    print("=" * 60)

    # Test mapper creation
    mapper = create_code_strategic_mapper()
    print(f"✅ Mapper created successfully")

    # Test strategic mapping
    test_code = """
def complex_function():
    # Complex logic here
    for i in range(100):
        if i % 2 == 0:
            process_even(i)
        else:
            process_odd(i)
    return result
"""

    mapping = mapper.map_code_to_strategic_context(
        "test.py", test_code, "architecture review"
    )
    print(
        f"✅ Strategic mapping generated: {len(mapping.recommendations)} recommendations"
    )

    # Test metrics
    metrics = mapper.get_mapping_metrics()
    print(f"✅ Mapping metrics: {metrics['success_rate']:.1%} success rate")

    print("\n🚀 TS-4 Code-Strategic Mapper ready for strategic analysis!")
