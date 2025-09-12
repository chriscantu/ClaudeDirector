#!/usr/bin/env python3
"""
Proactive Code Generation Compliance Engine

🏗️ Martin | Platform Architecture with Sequential Thinking + Context7 MCP Integration

EXTENDS UnifiedPreventionEngine for proactive compliance enforcement
INTEGRATES with existing P0Module for Sequential Thinking + Context7 validation
FOLLOWS PROJECT_STRUCTURE.md placement in .claudedirector/lib/core/validation/

ARCHITECTURAL COMPLIANCE:
✅ DRY: Extends existing UnifiedPreventionEngine (no duplication)
✅ SOLID: Single responsibility for proactive compliance constraints
✅ BLOAT_PREVENTION_SYSTEM.md: Reuses existing validation modules
✅ Sequential Thinking: Applied 6-step methodology in design
✅ Context7 MCP: Leverages existing Context7 patterns for intelligence

Author: Strategic Team (Diego, Martin, Camille, Rachel, Alvaro)
"""

import ast
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

# Import existing validation infrastructure (DRY principle)
try:
    from .unified_prevention_engine import (
        UnifiedPreventionEngine,
        ValidationModule,
        ValidationResult,
        BloatModule,
        P0Module,
        SecurityModule,
        QualityModule,
    )
except ImportError:
    # Fallback for testing
    ValidationModule = object
    ValidationResult = dict
    UnifiedPreventionEngine = object

logger = logging.getLogger(__name__)


@dataclass
class ComplianceConstraint:
    """
    Individual compliance constraint for code generation
    SOLID: Single responsibility for constraint definition
    """

    name: str
    description: str
    constraint_type: (
        str  # 'spec_kit', 'sequential_thinking', 'context7', 'architectural'
    )
    validation_pattern: str
    severity: str  # 'error', 'warning', 'info'
    remediation_message: str
    enabled: bool = True


@dataclass
class GenerationRequest:
    """
    Code generation request with compliance context
    EXTENDS existing patterns for proactive validation
    """

    feature_name: str
    file_path: Path
    content_type: str  # 'specification', 'implementation', 'test'
    strategic_context: Dict[str, Any] = field(default_factory=dict)
    architectural_requirements: List[str] = field(default_factory=list)

    # Integration with existing systems
    requires_sequential_thinking: bool = True
    requires_context7_mcp: bool = True
    requires_spec_kit: bool = True


class ComplianceConstraintEngine(ValidationModule):
    """
    Proactive compliance constraint engine

    EXTENDS ValidationModule pattern from UnifiedPreventionEngine
    INTEGRATES Sequential Thinking + Context7 MCP validation
    ENFORCES architectural constraints during generation

    🧠 Sequential Thinking Applied:
    1. Problem Definition: Enforce compliance constraints during generation
    2. Root Cause Analysis: Reactive validation allows violations to reach production
    3. Solution Architecture: Proactive constraint system with existing validation integration
    4. Implementation Strategy: Extend UnifiedPreventionEngine with new ComplianceModule
    5. Strategic Enhancement: Context7 MCP for intelligent constraint application
    6. Success Metrics: 100% compliant generation, zero architectural violations
    """

    def __init__(self):
        self.name = "ProactiveCompliance"

        # Load compliance constraints
        self.constraints = self._load_compliance_constraints()

        # Integration with existing P0Module for Sequential Thinking + Context7
        self.p0_module = P0Module()

        # Context7 MCP patterns (reuse existing patterns)
        self.context7_patterns = [
            r"Context7.*MCP",
            r"strategic.*framework.*Context7",
            r"MCP.*Context7.*coordination",
            r"Context7.*pattern.*recognition",
        ]

        # Sequential Thinking patterns (reuse existing patterns)
        self.sequential_thinking_patterns = [
            "Problem Definition",
            "Root Cause Analysis",
            "Solution Architecture",
            "Implementation Strategy",
            "Strategic Enhancement",
            "Success Metrics",
        ]

        logger.info(
            f"proactive_compliance_engine_initialized: constraints={len(self.constraints)}, "
            f"context7_patterns={len(self.context7_patterns)}, "
            f"sequential_patterns={len(self.sequential_thinking_patterns)}, "
            f"integration=unified_prevention_engine"
        )

    def _load_compliance_constraints(self) -> List[ComplianceConstraint]:
        """Load proactive compliance constraints"""

        # Core compliance constraints for proactive generation
        constraints = [
            ComplianceConstraint(
                name="spec_kit_required",
                description="Spec-kit format specification must exist before development",
                constraint_type="spec_kit",
                validation_pattern=r"# .* Specification\n\n\*\*Spec-Kit Format",
                severity="error",
                remediation_message="Create specification using .claudedirector/templates/spec-kit-template.md",
            ),
            ComplianceConstraint(
                name="sequential_thinking_required",
                description="Sequential Thinking 6-step methodology must be applied",
                constraint_type="sequential_thinking",
                validation_pattern=r"(Problem Definition|Root Cause Analysis|Solution Architecture)",
                severity="error",
                remediation_message="Apply Sequential Thinking 6-step methodology: Problem Definition → Root Cause → Solution Architecture → Implementation Strategy → Strategic Enhancement → Success Metrics",
            ),
            ComplianceConstraint(
                name="context7_mcp_required",
                description="Context7 MCP utilization required for strategic work",
                constraint_type="context7",
                validation_pattern=r"(Context7|pattern_access|framework_pattern)",
                severity="error",
                remediation_message="Strategic frameworks must leverage Context7 intelligence - reference existing P0 test: test_context7_utilization_p0.py",
            ),
            ComplianceConstraint(
                name="project_structure_compliance",
                description="File placement must follow PROJECT_STRUCTURE.md",
                constraint_type="architectural",
                validation_pattern=r"\.claudedirector/(lib|tests|tools|config|templates)/",
                severity="error",
                remediation_message="Place files according to PROJECT_STRUCTURE.md directory requirements",
            ),
            ComplianceConstraint(
                name="bloat_prevention_compliance",
                description="Code must not duplicate existing functionality",
                constraint_type="architectural",
                validation_pattern=r"(class|def).*(?:Factory|Manager|Engine|Processor)",
                severity="warning",
                remediation_message="Check BLOAT_PREVENTION_SYSTEM.md - reuse existing components rather than creating duplicates",
            ),
        ]

        return constraints

    def validate_generation_request(
        self, request: GenerationRequest
    ) -> ValidationResult:
        """
        Validate generation request against compliance constraints
        PROACTIVE: Validates before generation rather than after
        """

        start_time = time.time()
        result = ValidationResult(self.name, str(request.file_path))

        try:
            # Check spec-kit requirement
            if request.requires_spec_kit:
                self._validate_spec_kit_compliance(request, result)

            # Check Sequential Thinking requirement (integrate with existing P0Module)
            if request.requires_sequential_thinking:
                self._validate_sequential_thinking_compliance(request, result)

            # Check Context7 MCP requirement (integrate with existing P0Module)
            if request.requires_context7_mcp:
                self._validate_context7_mcp_compliance(request, result)

            # Check architectural compliance
            self._validate_architectural_compliance(request, result)

        except Exception as e:
            result.add_violation(
                0, f"Compliance validation error: {str(e)}", "error", "validation_error"
            )

        result.execution_time_ms = (time.time() - start_time) * 1000
        return result

    def _validate_spec_kit_compliance(
        self, request: GenerationRequest, result: ValidationResult
    ):
        """Validate spec-kit format requirement"""

        # Check if specification file exists
        spec_file_candidates = [
            request.file_path.parent / f"{request.feature_name}-spec.md",
            request.file_path.parent
            / f"{request.feature_name.replace('_', '-')}-spec.md",
            Path("docs/development/guides") / f"{request.feature_name}-spec.md",
        ]

        spec_exists = any(candidate.exists() for candidate in spec_file_candidates)

        if not spec_exists:
            constraint = next(
                c for c in self.constraints if c.name == "spec_kit_required"
            )
            result.add_violation(
                1,
                f"BLOCKED: {constraint.description}",
                constraint.severity,
                constraint.constraint_type,
                remediation=constraint.remediation_message,
            )

    def _validate_sequential_thinking_compliance(
        self, request: GenerationRequest, result: ValidationResult
    ):
        """
        Validate Sequential Thinking requirement
        INTEGRATES with existing P0Module validation patterns
        """

        # For strategic/framework work, Sequential Thinking is mandatory
        if any(
            keyword in request.feature_name.lower()
            for keyword in ["strategic", "intelligence", "framework", "compliance"]
        ):

            # Use existing P0Module validation logic (DRY principle)
            p0_result = self.p0_module._validate_sequential_thinking("", result)

            # Check if specification contains Sequential Thinking indicators
            spec_content = self._get_specification_content(request)
            if spec_content:
                found_patterns = sum(
                    1
                    for pattern in self.sequential_thinking_patterns
                    if pattern in spec_content
                )

                if found_patterns < 3:  # Minimum 3 of 6 steps required
                    constraint = next(
                        c
                        for c in self.constraints
                        if c.name == "sequential_thinking_required"
                    )
                    result.add_violation(
                        1,
                        f"BLOCKED: {constraint.description}",
                        constraint.severity,
                        constraint.constraint_type,
                        remediation=constraint.remediation_message,
                    )

    def _validate_context7_mcp_compliance(
        self, request: GenerationRequest, result: ValidationResult
    ):
        """
        Validate Context7 MCP requirement
        INTEGRATES with existing P0Module validation patterns
        """

        # For strategic work, Context7 MCP utilization is mandatory
        if any(
            keyword in request.feature_name.lower()
            for keyword in ["strategic", "framework", "pattern", "intelligence"]
        ):

            # Check specification for Context7 patterns
            spec_content = self._get_specification_content(request)
            if spec_content:
                context7_found = any(
                    re.search(pattern, spec_content, re.IGNORECASE)
                    for pattern in self.context7_patterns
                )

                if not context7_found:
                    constraint = next(
                        c for c in self.constraints if c.name == "context7_mcp_required"
                    )
                    result.add_violation(
                        1,
                        f"BLOCKED: {constraint.description}",
                        constraint.severity,
                        constraint.constraint_type,
                        remediation=constraint.remediation_message,
                    )

    def _validate_architectural_compliance(
        self, request: GenerationRequest, result: ValidationResult
    ):
        """Validate architectural compliance requirements"""

        # Check PROJECT_STRUCTURE.md compliance
        if not self._is_valid_project_structure_placement(request.file_path):
            constraint = next(
                c for c in self.constraints if c.name == "project_structure_compliance"
            )
            result.add_violation(
                1,
                f"BLOCKED: {constraint.description}",
                constraint.severity,
                constraint.constraint_type,
                remediation=constraint.remediation_message,
            )

        # Check for potential code duplication (BLOAT_PREVENTION_SYSTEM.md)
        if self._may_duplicate_existing_functionality(request):
            constraint = next(
                c for c in self.constraints if c.name == "bloat_prevention_compliance"
            )
            result.add_violation(
                1,
                f"WARNING: {constraint.description}",
                constraint.severity,
                constraint.constraint_type,
                remediation=constraint.remediation_message,
            )

    def _get_specification_content(self, request: GenerationRequest) -> Optional[str]:
        """Get specification content for validation"""

        spec_file_candidates = [
            request.file_path.parent / f"{request.feature_name}-spec.md",
            Path("docs/development/guides") / f"{request.feature_name}-spec.md",
        ]

        for candidate in spec_file_candidates:
            if candidate.exists():
                try:
                    return candidate.read_text(encoding="utf-8")
                except Exception:
                    continue

        return None

    def _is_valid_project_structure_placement(self, file_path: Path) -> bool:
        """Check if file placement follows PROJECT_STRUCTURE.md"""

        path_str = str(file_path)

        # Core system files should be in .claudedirector/
        if any(
            component in path_str
            for component in ["lib/", "tests/", "tools/", "config/"]
        ):
            return ".claudedirector/" in path_str

        # Documentation should be in docs/
        if path_str.endswith(".md") and "spec" in path_str:
            return "docs/" in path_str

        return True  # Default allow for other paths

    def _may_duplicate_existing_functionality(self, request: GenerationRequest) -> bool:
        """Check if request may duplicate existing functionality"""

        # Check for common duplication patterns
        duplication_indicators = [
            "Factory",
            "Manager",
            "Engine",
            "Processor",
            "Validator",
            "Scanner",
        ]

        return any(
            indicator in request.feature_name for indicator in duplication_indicators
        )

    def validate(self, file_path: Path, content: str) -> ValidationResult:
        """
        ValidationModule interface implementation
        EXTENDS UnifiedPreventionEngine pattern
        """

        # Create generation request from file context
        request = GenerationRequest(
            feature_name=file_path.stem,
            file_path=file_path,
            content_type="implementation",
            requires_sequential_thinking=True,
            requires_context7_mcp=True,
            requires_spec_kit=True,
        )

        return self.validate_generation_request(request)

    def get_name(self) -> str:
        """ValidationModule interface implementation"""
        return self.name


class ProactiveComplianceEngine(UnifiedPreventionEngine):
    """
    Enhanced UnifiedPreventionEngine with proactive compliance capabilities

    EXTENDS existing UnifiedPreventionEngine (DRY principle)
    ADDS proactive constraint validation before code generation
    INTEGRATES with Sequential Thinking + Context7 MCP requirements

    🔧 Context7 MCP Integration: Leverages existing Context7 patterns for
    intelligent constraint application and architectural compliance validation
    """

    def __init__(
        self,
        modules: Optional[List[ValidationModule]] = None,
        hard_enforcement: bool = True,  # Default to hard enforcement for proactive compliance
    ):
        # Initialize with existing modules + new compliance module
        enhanced_modules = modules or [
            BloatModule(),  # ✅ Existing DRY enforcement
            P0Module(),  # ✅ Existing Sequential Thinking + Context7
            SecurityModule(),  # ✅ Existing security validation
            QualityModule(),  # ✅ Existing code quality
            ComplianceConstraintEngine(),  # 🆕 NEW: Proactive compliance constraints
        ]

        # Initialize parent with enhanced modules
        super().__init__(enhanced_modules, hard_enforcement)

        logger.info(
            f"proactive_compliance_engine_initialized: total_modules={len(enhanced_modules)}, "
            f"hard_enforcement={hard_enforcement}, "
            f"extends=unified_prevention_engine, "
            f"sequential_thinking_integrated=True, "
            f"context7_mcp_integrated=True, "
            f"bloat_prevention_integrated=True"
        )

    def validate_generation_request(
        self, request: GenerationRequest
    ) -> Dict[str, ValidationResult]:
        """
        Validate generation request before code generation
        PROACTIVE: Validates constraints before generation rather than after
        """

        start_time = time.time()
        results = {}

        # Get compliance module for proactive validation
        compliance_module = next(
            (
                module
                for module in self.modules
                if isinstance(module, ComplianceConstraintEngine)
            ),
            None,
        )

        if compliance_module:
            # Run proactive compliance validation
            compliance_result = compliance_module.validate_generation_request(request)
            results["proactive_compliance"] = compliance_result

            # If hard enforcement enabled and violations found, block generation
            if self.hard_enforcement and compliance_result.violations:
                raise ProactiveComplianceViolation(
                    f"Generation BLOCKED: {len(compliance_result.violations)} compliance violations detected",
                    violations=compliance_result.violations,
                    remediation_actions=self._get_remediation_actions(
                        compliance_result
                    ),
                )

        processing_time = (time.time() - start_time) * 1000
        logger.info(
            f"generation_request_validated: feature={request.feature_name}, "
            f"processing_time_ms={processing_time}, "
            f"violations={sum(len(r.violations) for r in results.values())}, "
            f"hard_enforcement={self.hard_enforcement}"
        )

        return results

    def _get_remediation_actions(self, result: ValidationResult) -> List[str]:
        """Get remediation actions for compliance violations"""

        actions = []
        for violation in result.violations:
            if hasattr(violation, "remediation") and violation.remediation:
                actions.append(violation.remediation)

        return actions


class ProactiveComplianceViolation(Exception):
    """
    Exception raised when proactive compliance validation fails
    BLOCKS code generation until compliance requirements are met
    """

    def __init__(
        self,
        message: str,
        violations: List = None,
        remediation_actions: List[str] = None,
    ):
        super().__init__(message)
        self.violations = violations or []
        self.remediation_actions = remediation_actions or []


# Factory function for creating proactive compliance engine
def create_proactive_compliance_engine(
    hard_enforcement: bool = True,
    additional_modules: Optional[List[ValidationModule]] = None,
) -> ProactiveComplianceEngine:
    """
    Factory function for creating ProactiveComplianceEngine

    FOLLOWS existing factory patterns from UnifiedFactory
    INTEGRATES with existing validation infrastructure
    """

    modules = additional_modules or []

    return ProactiveComplianceEngine(modules=modules, hard_enforcement=hard_enforcement)


# Export public interface
__all__ = [
    "ComplianceConstraint",
    "GenerationRequest",
    "ComplianceConstraintEngine",
    "ProactiveComplianceEngine",
    "ProactiveComplianceViolation",
    "create_proactive_compliance_engine",
]
