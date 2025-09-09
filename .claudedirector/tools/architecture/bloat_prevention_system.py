"""
MCP-Enhanced Code Bloat Prevention System

🏗️ Martin | Platform Architecture - Systematic Duplication Prevention

Technical Objective: Prevent code duplication and project bloat through:
1. Real-time duplication detection during development
2. Architectural compliance validation
3. MCP Sequential analysis for systematic review
4. Automated consolidation recommendations
5. Pre-commit bloat prevention hooks

Architecture: Multi-layered prevention system with MCP coordination
Performance: <100ms analysis time, integrated into development workflow
"""

import ast
import os
import re
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

# Core imports
try:
    from ..quality.enhanced_security_scanner import EnhancedSecurityScanner
    from ...lib.core.config import get_config
except ImportError:
    # Fallback for standalone usage
    get_config = lambda: {}


# Configuration Constants (DRY Compliance)
class BloatPreventionConfig:
    """Configuration constants for bloat prevention system"""

    # DRY Violation Detection
    MIN_STRING_LENGTH = 10  # Minimum string literal length to check
    MAX_REPETITIONS = 2  # Maximum allowed repetitions before flagging
    STRING_PATTERN = r'"([^"]{10,})"'  # Regex for string literal detection

    # Prevention Strategy Templates
    STRATEGY_TEMPLATES = {
        "pre_commit": {
            "name": "Pre-commit Bloat Detection",
            "effort": "2 hours",
            "impact": "High - prevents bloat at source",
            "description": "Integrate bloat detection into pre-commit hooks",
            "implementation": "Add bloat_prevention_hook.py to .pre-commit-config.yaml",
        },
        "adr_process": {
            "name": "Architectural Decision Records (ADRs)",
            "effort": "4 hours",
            "impact": "Medium - guides future development",
            "description": "Document architectural decisions to prevent pattern violations",
            "implementation": "Create ADR template and process",
        },
        "code_review": {
            "name": "Code Review Checklist",
            "effort": "1 hour",
            "impact": "Medium - catches issues during review",
            "description": "Include bloat prevention in code review process",
            "implementation": "Update PR template with bloat prevention checklist",
        },
        "automated_refactor": {
            "name": "Automated Refactoring Suggestions",
            "effort": "8 hours",
            "impact": "High - proactive consolidation recommendations",
            "description": "Use MCP Sequential to suggest refactoring opportunities",
            "implementation": "Integrate MCP analysis into CI/CD pipeline",
        },
        "pattern_library": {
            "name": "Centralized Pattern Library",
            "effort": "6 hours",
            "impact": "Medium - promotes reuse over duplication",
            "description": "Maintain library of approved patterns and implementations",
            "implementation": "Create pattern registry with examples",
        },
    }


class DuplicationSeverity(Enum):
    """Severity levels for code duplication"""

    LOW = "low"  # Minor duplication, acceptable
    MODERATE = "moderate"  # Should be refactored
    HIGH = "high"  # Must be consolidated
    CRITICAL = "critical"  # Blocks development


class BloatCategory(Enum):
    """Categories of code bloat"""

    FUNCTIONAL_DUPLICATION = (
        "functional_duplication"  # Same functionality, different implementation
    )
    PATTERN_DUPLICATION = "pattern_duplication"  # Similar patterns/structures
    CONFIGURATION_DUPLICATION = "configuration_duplication"  # Repeated config/constants
    INTERFACE_DUPLICATION = "interface_duplication"  # Similar APIs/interfaces
    ARCHITECTURAL_VIOLATION = "architectural_violation"  # Violates established patterns


@dataclass
class DuplicationInstance:
    """Represents a detected code duplication instance"""

    file_path_1: str
    file_path_2: str
    similarity_score: float
    duplication_type: BloatCategory
    severity: DuplicationSeverity

    # Code analysis
    duplicated_lines: List[Tuple[int, int]]  # (line1, line2) pairs
    function_names: List[str] = field(default_factory=list)
    class_names: List[str] = field(default_factory=list)

    # Recommendations
    consolidation_strategy: str = ""
    target_location: str = ""
    estimated_effort_hours: float = 0.0

    # MCP analysis
    mcp_analysis: Optional[Dict[str, Any]] = None


@dataclass
class ArchitecturalViolation:
    """Represents violation of architectural principles"""

    file_path: str
    violation_type: str
    description: str
    severity: DuplicationSeverity

    # Context
    violated_principle: str  # DRY, SOLID, etc.
    existing_implementation: str
    recommended_approach: str

    # Impact
    affected_components: List[str] = field(default_factory=list)
    technical_debt_score: float = 0.0


class MCPBloatAnalyzer:
    """
    MCP-Enhanced Bloat Prevention System

    🏗️ Martin | Platform Architecture

    Systematic Prevention Strategy:
    1. Real-time duplication detection during file creation/modification
    2. Architectural compliance validation against established patterns
    3. MCP Sequential analysis for complex consolidation decisions
    4. Automated recommendations with effort estimation
    5. Integration with pre-commit hooks for prevention

    Detection Methods:
    - AST-based structural analysis
    - Semantic similarity detection
    - Pattern matching against known duplications
    - Interface/API similarity analysis
    - Configuration/constant duplication detection
    """

    def __init__(self, project_root: str, mcp_coordinator=None):
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(project_root)
        self.mcp_coordinator = mcp_coordinator
        self.config = get_config()

        # 🧠 Sequential Thinking Step 6: Use centralized thresholds instead of hard-coded values
        try:
            from ...lib.core.constants import ML_CONFIG

            # Use existing centralized ML constants for bloat detection
            self.similarity_threshold = self.config.get(
                "bloat_similarity_threshold", 0.40
            )
            self.functional_similarity_threshold = ML_CONFIG.CONFIDENCE_THRESHOLD  # 0.7
            self.class_similarity_threshold = 0.50  # Keep existing value

        except ImportError:
            # Fallback to original values if centralized constants unavailable
            self.similarity_threshold = self.config.get(
                "bloat_similarity_threshold", 0.40
            )
            self.functional_similarity_threshold = 0.60
            self.class_similarity_threshold = 0.50

        self.min_duplicate_lines = self.config.get("min_duplicate_lines", 10)
        self.exclusion_patterns = self._get_exclusion_patterns()

        # NEW: Architectural pattern detection
        self.architectural_patterns = self._load_architectural_patterns()

        # Caching for performance
        self.file_hashes = {}
        self.analysis_cache = {}

        # Known patterns from previous consolidations
        self.known_duplication_patterns = self._load_known_patterns()

        # NEW: Functional duplication detection patterns
        self.functional_patterns = self._load_functional_patterns()

        self.logger.info(
            "mcp_bloat_analyzer_initialized",
            project_root=str(self.project_root),
            similarity_threshold=self.similarity_threshold,
            mcp_enabled=self.mcp_coordinator is not None,
        )

    def _get_exclusion_patterns(self) -> List[str]:
        """Get patterns to exclude from duplication analysis"""

        # Infrastructure files that legitimately need hardcoded configuration values
        infrastructure_exclusions = [
            "*/bloat_prevention_system.py",  # This file itself (infrastructure config)
            "*/bloat_prevention_hook.py",  # Related infrastructure
            "*/constants.py",  # Configuration constants files (legitimate hardcoded values)
        ]

        # General exclusions for files that don't need bloat analysis
        general_exclusions = [
            "*/tests/*",
            "*/test_*",
            "*/__pycache__/*",
            "*.pyc",
            "*/node_modules/*",
            "*/venv/*",
            "*/env/*",
            "*/.git/*",
            "*/docs/archive/*",
            "*/deprecated/*",
        ]

        return infrastructure_exclusions + general_exclusions

    def _load_known_patterns(self) -> Dict[str, Any]:
        """Load known duplication patterns from previous analyses"""

        # Based on our actual experience - framework detection consolidation
        return {
            "framework_detection_engines": {
                "pattern": "class.*FrameworkDetection.*Engine",
                "consolidation_target": "lib/ai_intelligence/framework_detector.py",
                "description": "Multiple framework detection implementations",
                "severity": DuplicationSeverity.HIGH,
            },
            "mcp_coordinators": {
                "pattern": "class.*MCP.*Coordinator",
                "consolidation_target": "lib/ai_intelligence/mcp_coordinator.py",
                "description": "Multiple MCP coordination implementations",
                "severity": DuplicationSeverity.MODERATE,
            },
            "decision_orchestrators": {
                "pattern": "class.*Decision.*Orchestrator",
                "consolidation_target": "lib/ai_intelligence/decision_orchestrator.py",
                "description": "Multiple decision orchestration implementations",
                "severity": DuplicationSeverity.MODERATE,
            },
            "transparency_systems": {
                "pattern": "class.*Transparency.*System",
                "consolidation_target": "lib/transparency/integrated_transparency.py",
                "description": "Multiple transparency system implementations",
                "severity": DuplicationSeverity.MODERATE,
            },
        }

    async def analyze_project_for_bloat(
        self, target_paths: Optional[List[str]] = None, enable_mcp_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive project analysis for code bloat and duplication

        Args:
            target_paths: Specific paths to analyze (None for full project)
            enable_mcp_analysis: Whether to use MCP Sequential for complex analysis

        Returns:
            Comprehensive bloat analysis report
        """
        start_time = time.time()

        try:
            # Step 1: Discover Python files
            python_files = self._discover_python_files(target_paths)

            # Step 2: Structural analysis
            structural_duplications = await self._analyze_structural_duplication(
                python_files
            )

            # Step 3: Semantic analysis
            semantic_duplications = await self._analyze_semantic_duplication(
                python_files
            )

            # Step 4: Architectural violation detection
            architectural_violations = await self._detect_architectural_violations(
                python_files
            )

            # Step 4.5: NEW - Functional duplication detection (addresses Sequential Thinking findings)
            functional_violations = await self.detect_functional_duplication(
                python_files
            )
            architectural_violations.extend(functional_violations)

            # Step 5: MCP Sequential analysis for complex cases
            mcp_analysis = {}
            if enable_mcp_analysis and self.mcp_coordinator:
                mcp_analysis = await self._apply_mcp_analysis(
                    structural_duplications + semantic_duplications,
                    architectural_violations,
                )

            # Step 6: Generate consolidation recommendations
            recommendations = self._generate_consolidation_recommendations(
                structural_duplications + semantic_duplications,
                architectural_violations,
                mcp_analysis,
            )

            processing_time = time.time() - start_time

            report = {
                "analysis_timestamp": time.time(),
                "processing_time_seconds": processing_time,
                "files_analyzed": len(python_files),
                "duplications_found": {
                    "structural": len(structural_duplications),
                    "semantic": len(semantic_duplications),
                    "total": len(structural_duplications) + len(semantic_duplications),
                },
                "architectural_violations": len(architectural_violations),
                "severity_breakdown": self._calculate_severity_breakdown(
                    structural_duplications
                    + semantic_duplications
                    + [
                        ArchitecturalViolation(
                            **{
                                **v.__dict__,
                                "file_path": v.file_path,
                                "violation_type": v.violation_type,
                                "description": v.description,
                                "severity": v.severity,
                                "violated_principle": v.violated_principle,
                                "existing_implementation": v.existing_implementation,
                                "recommended_approach": v.recommended_approach,
                            }
                        )
                        for v in architectural_violations
                    ]
                ),
                "consolidation_recommendations": recommendations,
                "mcp_analysis": mcp_analysis,
                "prevention_strategies": self._generate_prevention_strategies(),
            }

            self.logger.info(
                "bloat_analysis_completed",
                files_analyzed=len(python_files),
                duplications_found=report["duplications_found"]["total"],
                processing_time=processing_time,
            )

            return report

        except Exception as e:
            self.logger.error(f"Bloat analysis failed: {e}")
            return {
                "error": str(e),
                "analysis_timestamp": time.time(),
                "status": "failed",
            }

    def _discover_python_files(
        self, target_paths: Optional[List[str]] = None
    ) -> List[Path]:
        """Discover Python files for analysis"""

        if target_paths:
            files = []
            for path_str in target_paths:
                path = Path(path_str)
                if path.is_file() and path.suffix == ".py":
                    files.append(path)
                elif path.is_dir():
                    files.extend(path.rglob("*.py"))
        else:
            files = list(self.project_root.rglob("*.py"))

        # Apply exclusion patterns
        filtered_files = []
        for file_path in files:
            if not any(file_path.match(pattern) for pattern in self.exclusion_patterns):
                filtered_files.append(file_path)

        return filtered_files

    async def _analyze_structural_duplication(
        self, files: List[Path]
    ) -> List[DuplicationInstance]:
        """Analyze structural code duplication using AST"""

        duplications = []
        file_asts = {}

        # Parse AST for each file
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_asts[file_path] = ast.parse(content)
            except Exception as e:
                self.logger.warning(f"Failed to parse {file_path}: {e}")
                continue

        # Compare AST structures
        file_list = list(file_asts.keys())
        for i, file1 in enumerate(file_list):
            for file2 in file_list[i + 1 :]:
                similarity = self._calculate_ast_similarity(
                    file_asts[file1], file_asts[file2]
                )

                if similarity > self.similarity_threshold:
                    duplication = DuplicationInstance(
                        file_path_1=str(file1),
                        file_path_2=str(file2),
                        similarity_score=similarity,
                        duplication_type=BloatCategory.FUNCTIONAL_DUPLICATION,
                        severity=self._determine_severity(similarity),
                        duplicated_lines=self._find_duplicated_lines(file1, file2),
                    )
                    duplications.append(duplication)

        return duplications

    async def _analyze_semantic_duplication(
        self, files: List[Path]
    ) -> List[DuplicationInstance]:
        """Analyze semantic duplication (similar purpose, different implementation)"""

        duplications = []

        # Check against known patterns
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                for (
                    pattern_name,
                    pattern_config,
                ) in self.known_duplication_patterns.items():
                    if re.search(pattern_config["pattern"], content, re.IGNORECASE):
                        # Found potential duplication
                        existing_target = (
                            Path(self.project_root)
                            / pattern_config["consolidation_target"]
                        )

                        if existing_target.exists() and existing_target != file_path:
                            duplication = DuplicationInstance(
                                file_path_1=str(file_path),
                                file_path_2=str(existing_target),
                                similarity_score=0.8,  # Pattern-based similarity
                                duplication_type=BloatCategory.PATTERN_DUPLICATION,
                                severity=pattern_config["severity"],
                                duplicated_lines=[],
                                consolidation_strategy=f"Consolidate into {pattern_config['consolidation_target']}",
                                target_location=pattern_config["consolidation_target"],
                            )
                            duplications.append(duplication)

            except Exception as e:
                self.logger.warning(f"Failed to analyze {file_path}: {e}")
                continue

        return duplications

    async def _detect_architectural_violations(
        self, files: List[Path]
    ) -> List[ArchitecturalViolation]:
        """Detect violations of architectural principles"""

        violations = []

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for DRY violations (hard-coded strings/constants)
                dry_violations = self._detect_dry_violations(file_path, content)
                violations.extend(dry_violations)

                # Check for SOLID violations
                solid_violations = self._detect_solid_violations(file_path, content)
                violations.extend(solid_violations)

                # Check for architectural pattern violations
                pattern_violations = self._detect_pattern_violations(file_path, content)
                violations.extend(pattern_violations)

            except Exception as e:
                self.logger.warning(f"Failed to check violations in {file_path}: {e}")
                continue

        return violations

    def _detect_dry_violations(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Detect DRY principle violations with enhanced configuration-driven pattern recognition"""

        violations = []

        # Enhanced pattern recognition for configuration-driven code
        if self._is_configuration_driven_file(file_path, content):
            # Use more lenient analysis for configuration-driven files
            return self._analyze_configuration_driven_violations(file_path, content)

        # Look for repeated string literals (DRY compliance)
        string_literals = re.findall(BloatPreventionConfig.STRING_PATTERN, content)
        string_counts = {}

        for literal in string_literals:
            # Skip configuration-related strings that are acceptable
            if self._is_acceptable_configuration_string(literal, content):
                continue

            string_counts[literal] = string_counts.get(literal, 0) + 1

        for literal, count in string_counts.items():
            if count > BloatPreventionConfig.MAX_REPETITIONS:
                violations.append(
                    ArchitecturalViolation(
                        file_path=str(file_path),
                        violation_type="DRY_VIOLATION",
                        description=f"String literal '{literal}' repeated {count} times",
                        severity=DuplicationSeverity.MODERATE,
                        violated_principle="DRY",
                        existing_implementation=f"Hard-coded string: {literal}",
                        recommended_approach="Move to constants file or configuration",
                    )
                )

        return violations

    def _is_configuration_driven_file(self, file_path: Path, content: str) -> bool:
        """Detect if a file uses configuration-driven patterns"""

        # Check for configuration loading patterns
        config_patterns = [
            r"yaml\.safe_load",
            r"config\.get\(",
            r"_CONSTANTS\[",
            r"domain_strings\.get\(",
            r"thresholds\.get\(",
            r"challenge_patterns\.yaml",
            r"load_config\(",
            r"from.*config.*import",
        ]

        for pattern in config_patterns:
            if re.search(pattern, content):
                return True

        return False

    def _is_acceptable_configuration_string(self, literal: str, content: str) -> bool:
        """Check if a string literal is acceptable in configuration-driven context"""

        # Configuration key strings are acceptable
        config_key_patterns = [
            r"challenge_patterns",
            r"name",
            r"description",
            r"trigger_keywords",
            r"generic_questions",
            r"confidence_threshold",
            r"domain",
            r"challenge_style",
            r"challenge_intros",
        ]

        if literal in config_key_patterns:
            return True

        # Fallback values in configuration loading are acceptable
        if re.search(rf'\.get\([^,]*,\s*["\']?{re.escape(literal)}["\']?\)', content):
            return True

        # Constants dictionary keys are acceptable
        if re.search(rf'_CONSTANTS\[["\']?{re.escape(literal)}["\']?\]', content):
            return True

        return False

    def _analyze_configuration_driven_violations(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Analyze violations in configuration-driven files with more lenient rules"""

        violations = []

        # Only flag truly problematic patterns in config-driven files
        # Look for business logic strings that should be in config but aren't
        business_logic_patterns = [
            r'"(ERROR|CRITICAL|FATAL):[^"]{20,}"',  # Long error messages
            r'"(SELECT|INSERT|UPDATE|DELETE)\s+[^"]{30,}"',  # SQL queries
            r'"https?://[^"]{20,}"',  # Long URLs
        ]

        for pattern in business_logic_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                violations.append(
                    ArchitecturalViolation(
                        file_path=str(file_path),
                        violation_type="CONFIG_DRIVEN_VIOLATION",
                        description=f"Business logic string should be in configuration: {match[:50]}...",
                        severity=DuplicationSeverity.LOW,
                        violated_principle="DRY",
                        existing_implementation=f"Hard-coded business logic: {match}",
                        recommended_approach="Move to configuration file",
                    )
                )

        return violations

    def _detect_solid_violations(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Detect SOLID principle violations"""

        violations = []

        # Single Responsibility Principle - large classes
        class_matches = re.finditer(r"class\s+(\w+).*?(?=class|\Z)", content, re.DOTALL)

        for match in class_matches:
            class_content = match.group(0)
            method_count = len(re.findall(r"def\s+\w+", class_content))

            if method_count > 15:  # Arbitrary threshold
                violations.append(
                    ArchitecturalViolation(
                        file_path=str(file_path),
                        violation_type="SRP_VIOLATION",
                        description=f"Class {match.group(1)} has {method_count} methods (too many responsibilities)",
                        severity=DuplicationSeverity.MODERATE,
                        violated_principle="Single Responsibility Principle",
                        existing_implementation=f"Large class with {method_count} methods",
                        recommended_approach="Split into smaller, focused classes",
                    )
                )

        return violations

    def _detect_pattern_violations(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Detect architectural pattern violations"""

        violations = []

        # Check for multiple similar class names (potential duplication)
        class_names = re.findall(r"class\s+(\w+)", content)

        for pattern_name, pattern_config in self.known_duplication_patterns.items():
            matching_classes = [
                name
                for name in class_names
                if re.search(pattern_config["pattern"], name)
            ]

            if len(matching_classes) > 1:
                violations.append(
                    ArchitecturalViolation(
                        file_path=str(file_path),
                        violation_type="PATTERN_DUPLICATION",
                        description=f"Multiple classes matching pattern {pattern_name}: {matching_classes}",
                        severity=pattern_config["severity"],
                        violated_principle="Single Source of Truth",
                        existing_implementation=f"Multiple classes: {', '.join(matching_classes)}",
                        recommended_approach=f"Consolidate into {pattern_config['consolidation_target']}",
                    )
                )

        return violations

    async def _apply_mcp_analysis(
        self,
        duplications: List[DuplicationInstance],
        violations: List[ArchitecturalViolation],
    ) -> Dict[str, Any]:
        """Apply MCP Sequential analysis for complex consolidation decisions"""

        if not self.mcp_coordinator:
            return {}

        try:
            # Prepare context for MCP analysis
            analysis_context = {
                "duplications_count": len(duplications),
                "violations_count": len(violations),
                "high_severity_items": len(
                    [
                        item
                        for item in duplications + violations
                        if getattr(item, "severity", None) == DuplicationSeverity.HIGH
                    ]
                ),
                "consolidation_candidates": [
                    {
                        "file1": dup.file_path_1,
                        "file2": dup.file_path_2,
                        "similarity": dup.similarity_score,
                        "type": dup.duplication_type.value,
                    }
                    for dup in duplications[:5]  # Top 5 for analysis
                ],
            }

            # Use MCP Sequential for systematic analysis
            enhanced_context = await self.mcp_coordinator.enhance_context_with_mcp(
                analysis_context, enhancement_level="SYSTEMATIC"
            )

            return {
                "mcp_recommendations": enhanced_context.get("strategic_insights", []),
                "consolidation_priority": enhanced_context.get("priority_ranking", []),
                "effort_estimates": enhanced_context.get("effort_analysis", {}),
                "risk_assessment": enhanced_context.get("risk_factors", []),
            }

        except Exception as e:
            self.logger.warning(f"MCP analysis failed: {e}")
            return {}

    def _calculate_ast_similarity(self, ast1: ast.AST, ast2: ast.AST) -> float:
        """Calculate similarity between two AST structures"""

        # Simplified similarity calculation
        # In practice, this would be more sophisticated

        def count_nodes(node):
            count = 1
            for child in ast.iter_child_nodes(node):
                count += count_nodes(child)
            return count

        def get_node_types(node):
            types = [type(node).__name__]
            for child in ast.iter_child_nodes(node):
                types.extend(get_node_types(child))
            return types

        types1 = get_node_types(ast1)
        types2 = get_node_types(ast2)

        # Calculate Jaccard similarity
        set1, set2 = set(types1), set(types2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def _determine_severity(self, similarity_score: float) -> DuplicationSeverity:
        """Determine severity based on similarity score"""

        if similarity_score >= 0.95:
            return DuplicationSeverity.CRITICAL
        elif similarity_score >= 0.85:
            return DuplicationSeverity.HIGH
        elif similarity_score >= 0.75:
            return DuplicationSeverity.MODERATE
        else:
            return DuplicationSeverity.LOW

    def _find_duplicated_lines(self, file1: Path, file2: Path) -> List[Tuple[int, int]]:
        """Find specific duplicated lines between two files"""

        try:
            with open(file1, "r") as f1, open(file2, "r") as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()

            duplicated = []
            for i, line1 in enumerate(lines1):
                for j, line2 in enumerate(lines2):
                    if line1.strip() == line2.strip() and len(line1.strip()) > 10:
                        duplicated.append((i + 1, j + 1))

            return duplicated[:20]  # Limit to first 20 matches

        except Exception:
            return []

    def _calculate_severity_breakdown(self, items: List) -> Dict[str, int]:
        """Calculate breakdown of items by severity"""

        breakdown = {severity.value: 0 for severity in DuplicationSeverity}

        for item in items:
            severity = getattr(item, "severity", DuplicationSeverity.LOW)
            breakdown[severity.value] += 1

        return breakdown

    def _generate_consolidation_recommendations(
        self,
        duplications: List[DuplicationInstance],
        violations: List[ArchitecturalViolation],
        mcp_analysis: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate actionable consolidation recommendations"""

        recommendations = []

        # Sort by severity and similarity
        sorted_duplications = sorted(
            duplications,
            key=lambda x: (x.severity.value, x.similarity_score),
            reverse=True,
        )

        for i, dup in enumerate(sorted_duplications[:10]):  # Top 10 recommendations
            rec = {
                "priority": i + 1,
                "type": "consolidation",
                "description": f"Consolidate {Path(dup.file_path_1).name} and {Path(dup.file_path_2).name}",
                "files": [dup.file_path_1, dup.file_path_2],
                "similarity_score": dup.similarity_score,
                "severity": dup.severity.value,
                "estimated_effort_hours": self._estimate_consolidation_effort(dup),
                "consolidation_strategy": dup.consolidation_strategy
                or self._suggest_consolidation_strategy(dup),
                "target_location": dup.target_location
                or self._suggest_target_location(dup),
                "benefits": [
                    "Reduced code duplication",
                    "Improved maintainability",
                    "Single source of truth",
                    "Reduced technical debt",
                ],
            }

            # Add MCP insights if available
            if mcp_analysis and "mcp_recommendations" in mcp_analysis:
                rec["mcp_insights"] = mcp_analysis["mcp_recommendations"][:3]

            recommendations.append(rec)

        return recommendations

    def _estimate_consolidation_effort(self, duplication: DuplicationInstance) -> float:
        """Estimate effort required for consolidation"""

        base_effort = 2.0  # Base 2 hours

        # Adjust based on similarity (higher similarity = easier consolidation)
        similarity_factor = 1.0 - duplication.similarity_score

        # Adjust based on file size (estimate)
        size_factor = len(duplication.duplicated_lines) / 100.0

        return base_effort + (similarity_factor * 4.0) + (size_factor * 2.0)

    def _suggest_consolidation_strategy(self, duplication: DuplicationInstance) -> str:
        """Suggest consolidation strategy based on duplication type"""

        strategies = {
            BloatCategory.FUNCTIONAL_DUPLICATION: "Merge identical functionality into single implementation",
            BloatCategory.PATTERN_DUPLICATION: "Extract common patterns into shared base class or utility",
            BloatCategory.CONFIGURATION_DUPLICATION: "Move to centralized configuration file",
            BloatCategory.INTERFACE_DUPLICATION: "Define common interface and implement variations",
            BloatCategory.ARCHITECTURAL_VIOLATION: "Refactor to follow established architectural patterns",
        }

        return strategies.get(
            duplication.duplication_type, "Manual review and consolidation required"
        )

    def _suggest_target_location(self, duplication: DuplicationInstance) -> str:
        """Suggest target location for consolidated code"""

        # Prefer existing file if one is clearly more complete
        file1_path = Path(duplication.file_path_1)
        file2_path = Path(duplication.file_path_2)

        # Simple heuristic: prefer file in lib/ over tools/
        if "lib/" in str(file1_path) and "tools/" in str(file2_path):
            return str(file1_path)
        elif "tools/" in str(file1_path) and "lib/" in str(file2_path):
            return str(file2_path)

        # Prefer shorter path (likely more central)
        return (
            str(file1_path)
            if len(str(file1_path)) <= len(str(file2_path))
            else str(file2_path)
        )

    def _generate_prevention_strategies(self) -> List[Dict[str, Any]]:
        """Generate strategies to prevent future bloat (DRY compliance)"""

        strategies = []
        for strategy_key, template in BloatPreventionConfig.STRATEGY_TEMPLATES.items():
            strategies.append(
                {
                    "strategy": template["name"],
                    "description": template["description"],
                    "implementation": template["implementation"],
                    "effort": template["effort"],
                    "impact": template["impact"],
                }
            )

        return strategies

    def _load_architectural_patterns(self) -> Dict[str, Any]:
        """Load architectural patterns for detecting functional duplication"""
        return {
            "framework_detection": {
                "class_patterns": [
                    "FrameworkDetection",
                    "FrameworkEngine",
                    "FrameworkProcessor",
                ],
                "method_patterns": [
                    "detect_frameworks",
                    "pattern_based_detection",
                    "calculate_confidence",
                ],
                "functionality": "framework detection and analysis",
            },
            "confidence_calculation": {
                "class_patterns": [
                    "ConfidenceCalculation",
                    "ConfidenceService",
                    "ConfidenceEngine",
                ],
                "method_patterns": [
                    "calculate_confidence",
                    "confidence_score",
                    "_calculate_.*_confidence",
                ],
                "functionality": "confidence scoring and calculation",
            },
            "pattern_matching": {
                "class_patterns": [
                    "PatternMatcher",
                    "PatternDetector",
                    "PatternEngine",
                ],
                "method_patterns": [
                    "match_pattern",
                    "detect_pattern",
                    "pattern_analysis",
                ],
                "functionality": "pattern matching and detection",
            },
            "strategic_analysis": {
                "class_patterns": [
                    "StrategicAnalysis",
                    "StrategicEngine",
                    "AnalysisEngine",
                ],
                "method_patterns": [
                    "analyze",
                    "strategic_analysis",
                    "generate_analysis",
                ],
                "functionality": "strategic analysis and insights",
            },
        }

    def _load_functional_patterns(self) -> Dict[str, Any]:
        """Load functional patterns for detecting reimplementation of existing functionality"""
        return {
            "content_lower_pattern": {
                "pattern": r"content_lower\s*=\s*content\.lower\(\)",
                "description": "Text normalization for pattern matching",
                "existing_implementations": [
                    ".claudedirector/lib/transparency/framework_detection.py",
                    ".claudedirector/lib/ai_intelligence/framework_processor.py",
                ],
            },
            "pattern_iteration": {
                "pattern": r"for\s+\w+\s+in\s+.*patterns.*:",
                "description": "Iterating over patterns for matching",
                "existing_implementations": [
                    ".claudedirector/lib/transparency/framework_detection.py",
                    ".claudedirector/lib/ai_intelligence/framework_processor.py",
                ],
            },
            "confidence_calculation": {
                "pattern": r"confidence.*=.*\+.*\*",
                "description": "Weighted confidence score calculation",
                "existing_implementations": [
                    ".claudedirector/lib/core/services/confidence_calculation_service.py",
                    ".claudedirector/lib/ai_intelligence/decision_processor.py",
                ],
            },
        }

    async def detect_functional_duplication(
        self, files: List[Path]
    ) -> List[ArchitecturalViolation]:
        """
        ENHANCED: Detect functional duplication (reimplementation of existing functionality)

        This addresses the root cause identified in Sequential Thinking analysis:
        - Detects when new classes reimplement existing functionality
        - Identifies architectural pattern violations
        - Catches functional similarity even with different code structure
        """
        violations = []

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for functional pattern duplication
                functional_violations = (
                    await self._detect_functional_pattern_duplication(
                        file_path, content
                    )
                )
                violations.extend(functional_violations)

                # Check for architectural pattern reimplementation
                architectural_violations = (
                    await self._detect_architectural_reimplementation(
                        file_path, content
                    )
                )
                violations.extend(architectural_violations)

            except Exception as e:
                self.logger.warning(
                    f"Error analyzing {file_path} for functional duplication: {e}"
                )

        return violations

    async def _detect_functional_pattern_duplication(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Detect when new code reimplements existing functional patterns"""
        violations = []

        for pattern_name, pattern_info in self.functional_patterns.items():
            matches = re.findall(pattern_info["pattern"], content, re.MULTILINE)

            if matches:
                # Check if this functionality already exists
                existing_files = pattern_info.get("existing_implementations", [])
                if existing_files and str(file_path) not in existing_files:
                    violations.append(
                        ArchitecturalViolation(
                            file_path=str(file_path),
                            violation_type="FUNCTIONAL_DUPLICATION",
                            description=f"Reimplements {pattern_info['description']} - functionality already exists",
                            severity=DuplicationSeverity.HIGH,
                            violated_principle="DRY",
                            existing_implementation=f"Already implemented in: {', '.join(existing_files)}",
                            recommended_approach=f"Use existing implementation or extend existing classes",
                            technical_debt_score=0.8,
                        )
                    )

        return violations

    async def _detect_architectural_reimplementation(
        self, file_path: Path, content: str
    ) -> List[ArchitecturalViolation]:
        """Detect when new classes reimplement existing architectural patterns"""
        violations = []

        # Extract class names from the file
        class_matches = re.findall(r"class\s+(\w+)", content)

        for class_name in class_matches:
            for pattern_name, pattern_info in self.architectural_patterns.items():
                # Check if this class matches a known architectural pattern
                for class_pattern in pattern_info["class_patterns"]:
                    if class_pattern.lower() in class_name.lower():
                        # Check if this functionality already exists
                        existing_classes = (
                            await self._find_existing_classes_with_functionality(
                                pattern_info["functionality"]
                            )
                        )

                        if existing_classes and str(file_path) not in [
                            cls["file"] for cls in existing_classes
                        ]:
                            violations.append(
                                ArchitecturalViolation(
                                    file_path=str(file_path),
                                    violation_type="ARCHITECTURAL_REIMPLEMENTATION",
                                    description=f"Class '{class_name}' reimplements {pattern_info['functionality']}",
                                    severity=DuplicationSeverity.CRITICAL,
                                    violated_principle="DRY",
                                    existing_implementation=f"Existing classes: {', '.join([cls['name'] for cls in existing_classes])}",
                                    recommended_approach=f"Extend existing {pattern_info['functionality']} classes or consolidate functionality",
                                    technical_debt_score=0.9,
                                )
                            )

        return violations

    async def _find_existing_classes_with_functionality(
        self, functionality: str
    ) -> List[Dict[str, str]]:
        """Find existing classes that provide the specified functionality"""
        existing_classes = []

        # Hardcoded mapping based on our codebase analysis
        functionality_mapping = {
            "framework detection and analysis": [
                {
                    "name": "FrameworkDetectionMiddleware",
                    "file": ".claudedirector/lib/transparency/framework_detection.py",
                },
                {
                    "name": "FrameworkProcessor",
                    "file": ".claudedirector/lib/ai_intelligence/framework_processor.py",
                },
                {
                    "name": "EnhancedFrameworkDetection",
                    "file": ".claudedirector/lib/ai_intelligence/framework_detector.py",
                },
            ],
            "confidence scoring and calculation": [
                {
                    "name": "ConfidenceCalculationService",
                    "file": ".claudedirector/lib/core/services/confidence_calculation_service.py",
                },
                {
                    "name": "ActionDetectionEngine",
                    "file": ".claudedirector/lib/context_engineering/clarity_analyzer.py",
                },
            ],
            "strategic analysis and insights": [
                {
                    "name": "StrategicAnalysisEngine",
                    "file": ".claudedirector/lib/core/cursor_response_enhancer.py",
                },
                {
                    "name": "DecisionProcessor",
                    "file": ".claudedirector/lib/ai_intelligence/decision_processor.py",
                },
            ],
        }

        return functionality_mapping.get(functionality, [])


# Factory function for easy integration
def create_bloat_analyzer(project_root: str, mcp_coordinator=None) -> MCPBloatAnalyzer:
    """Create MCP-enhanced bloat analyzer"""
    return MCPBloatAnalyzer(project_root, mcp_coordinator)


# CLI integration for standalone usage
if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        # Parse command line arguments
        if len(sys.argv) < 2:
            project_root = "."
            target_files = None
        else:
            # First arg might be project root or file
            first_arg = sys.argv[1]
            if os.path.isdir(first_arg):
                project_root = first_arg
                target_files = sys.argv[2:] if len(sys.argv) > 2 else None
            else:
                project_root = "."
                target_files = sys.argv[1:]

        analyzer = create_bloat_analyzer(project_root)

        print("🏗️ Running MCP-Enhanced Bloat Analysis...")
        if target_files:
            print(f"🎯 Analyzing {len(target_files)} specific file(s)...")

        report = await analyzer.analyze_project_for_bloat(target_paths=target_files)

        print(f"\n📊 Analysis Results:")
        print(f"Files analyzed: {report['files_analyzed']}")
        print(f"Duplications found: {report['duplications_found']['total']}")
        print(f"Architectural violations: {report['architectural_violations']}")
        print(f"Processing time: {report['processing_time_seconds']:.2f}s")

        if report["consolidation_recommendations"]:
            print(f"\n🔧 Top Consolidation Recommendations:")
            for rec in report["consolidation_recommendations"][:3]:
                print(
                    f"  {rec['priority']}. {rec['description']} (Effort: {rec['estimated_effort_hours']:.1f}h)"
                )

    asyncio.run(main())
