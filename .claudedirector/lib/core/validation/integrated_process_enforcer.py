#!/usr/bin/env python3
"""
Integrated Process Enforcer - MANDATORY Process Layer

🏗️ Martin | Platform Architecture with Sequential Thinking + Context7 MCP Integration

BLOCKS all development work without complete process compliance
INTEGRATES: Spec-Kit + Sequential Thinking + Context7 MCP + Architectural Requirements
ZERO TOLERANCE for process violations

ARCHITECTURAL COMPLIANCE:
✅ DRY: Integrates with existing P0Module validation patterns
✅ SOLID: Single responsibility for integrated process enforcement
✅ BLOAT_PREVENTION_SYSTEM.md: Reuses existing validation infrastructure
✅ Sequential Thinking: Applied 6-step methodology in design
✅ Context7 MCP: Leverages existing Context7 patterns for intelligence
✅ PROJECT_STRUCTURE.md: Placed in .claudedirector/lib/core/validation/

Author: Strategic Team (Diego, Martin, Camille, Rachel, Alvaro)
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ProcessViolationType(Enum):
    """Types of process violations that block development"""

    SPEC_KIT_MISSING = "spec_kit_missing"
    SEQUENTIAL_THINKING_MISSING = "sequential_thinking_missing"
    CONTEXT7_MCP_MISSING = "context7_mcp_missing"
    ARCHITECTURAL_VIOLATION = "architectural_violation"


@dataclass
class ProcessValidation:
    """Result of integrated process validation"""

    approved: bool
    timestamp: datetime
    violations: List[str] = field(default_factory=list)
    remediation_actions: List[str] = field(default_factory=list)
    validation_time_ms: float = 0.0


@dataclass
class DevelopmentRequest:
    """Development request requiring process compliance"""

    feature_name: str
    request_type: str  # 'implementation', 'enhancement', 'refactoring'
    file_paths: List[Path] = field(default_factory=list)
    strategic_context: Dict[str, Any] = field(default_factory=dict)

    # Process requirements (configurable based on request type)
    requires_spec_kit: bool = True
    requires_sequential_thinking: bool = True
    requires_context7_mcp: bool = True


class SpecKitProcessViolation(Exception):
    """Raised when spec-kit process is not followed"""

    pass


class SequentialThinkingViolation(Exception):
    """Raised when Sequential Thinking methodology is not applied"""

    pass


class Context7UtilizationViolation(Exception):
    """Raised when Context7 MCP utilization is not verified"""

    pass


class ArchitecturalComplianceViolation(Exception):
    """Raised when architectural compliance is not verified"""

    pass


class IntegratedProcessEnforcer:
    """
    BLOCKS all development work without complete process compliance
    INTEGRATES: Spec-Kit + Sequential Thinking + Context7 MCP + Architectural Requirements
    ZERO TOLERANCE for process violations

    🧠 Sequential Thinking Applied:
    1. Problem Definition: Enforce integrated process compliance before development
    2. Root Cause Analysis: Lack of systematic process enforcement leads to violations
    3. Solution Architecture: Mandatory process layer that blocks non-compliant development
    4. Implementation Strategy: Integrate existing P0 validation patterns with new requirements
    5. Strategic Enhancement: Context7 MCP for intelligent process validation
    6. Success Metrics: Zero process violations, 100% compliance rate

    🔧 Context7 MCP Integration: Leverages existing Context7 patterns from P0Module
    for intelligent pattern recognition and process validation
    """

    def __init__(self):
        self.name = "IntegratedProcessEnforcer"

        # Integration with existing P0Module patterns (DRY principle)
        self.sequential_thinking_patterns = [
            "Problem Definition",
            "Root Cause Analysis",
            "Solution Architecture",
            "Implementation Strategy",
            "Strategic Enhancement",
            "Success Metrics",
        ]

        # Context7 MCP patterns (reuse from existing P0Module)
        self.context7_patterns = [
            r"Context7.*MCP",
            r"strategic.*framework.*Context7",
            r"MCP.*Context7.*coordination",
            r"Context7.*pattern.*recognition",
        ]

        # Spec-kit format patterns
        self.spec_kit_patterns = [
            r"# .* Specification\n\n\*\*Spec-Kit Format",
            r"\*\*Status\*\*:.*\*\*Owner\*\*:",
            r"## 📋 \*\*Executive Summary\*\*",
            r"## 🎯 \*\*Requirements\*\*",
        ]

        # Architectural compliance patterns
        self.project_structure_patterns = [
            r"\.claudedirector/(lib|tests|tools|config|templates)/",
            r"docs/(architecture|requirements|development|setup)/",
            r"leadership-workspace/",
        ]

        logger.info(
            f"integrated_process_enforcer_initialized: sequential_patterns={len(self.sequential_thinking_patterns)}, "
            f"context7_patterns={len(self.context7_patterns)}, "
            f"spec_kit_patterns={len(self.spec_kit_patterns)}, "
            f"architecture_patterns={len(self.project_structure_patterns)}, "
            f"zero_tolerance=True"
        )

    def validate_development_request(
        self, request: DevelopmentRequest
    ) -> ProcessValidation:
        """
        Block development if integrated process not followed
        ZERO EXCEPTIONS RULE enforced
        """

        start_time = time.time()
        validation = ProcessValidation(approved=False, timestamp=datetime.now())

        try:
            # MANDATORY CHECK 1: Spec-kit specification exists
            if request.requires_spec_kit and not self.spec_kit_exists(
                request.feature_name
            ):
                raise SpecKitProcessViolation(
                    f"BLOCKED: No spec-kit specification found for {request.feature_name}. "
                    f"Create specification using .claudedirector/templates/spec-kit-template.md"
                )

            # MANDATORY CHECK 2: Sequential Thinking applied (PRE-EXISTING REQUIREMENT)
            if (
                request.requires_sequential_thinking
                and not self.sequential_thinking_complete(request.feature_name)
            ):
                raise SequentialThinkingViolation(
                    f"BLOCKED: Sequential Thinking methodology not applied for {request.feature_name}. "
                    f"Complete 6-step analysis: Problem Definition → Root Cause → Solution Architecture → "
                    f"Implementation Strategy → Strategic Enhancement → Success Metrics"
                )

            # MANDATORY CHECK 3: Context7 MCP utilization (PRE-EXISTING REQUIREMENT)
            if (
                request.requires_context7_mcp
                and not self.context7_utilization_verified(request.feature_name)
            ):
                raise Context7UtilizationViolation(
                    f"BLOCKED: Context7 MCP utilization not verified for {request.feature_name}. "
                    f"Strategic frameworks and patterns must leverage Context7 intelligence"
                )

            # MANDATORY CHECK 4: Architectural compliance verified
            if not self.architectural_compliance_verified(request.feature_name):
                raise ArchitecturalComplianceViolation(
                    f"BLOCKED: Architectural compliance not verified for {request.feature_name}. "
                    f"Verify PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md alignment"
                )

            # All checks passed - approve development
            validation.approved = True

        except (
            SpecKitProcessViolation,
            SequentialThinkingViolation,
            Context7UtilizationViolation,
            ArchitecturalComplianceViolation,
        ) as e:

            validation.violations.append(str(e))
            validation.remediation_actions.append(self._get_remediation_action(e))

        except Exception as e:
            validation.violations.append(f"Process validation error: {str(e)}")
            validation.remediation_actions.append(
                "Review process enforcement configuration"
            )

        validation.validation_time_ms = (time.time() - start_time) * 1000

        logger.info(
            f"development_request_validated: feature={request.feature_name}, "
            f"approved={validation.approved}, "
            f"violations={len(validation.violations)}, "
            f"validation_time_ms={validation.validation_time_ms}"
        )

        return validation

    def spec_kit_exists(self, feature_name: str) -> bool:
        """Check if spec-kit specification exists for feature"""

        # Standard spec-kit file locations
        spec_file_candidates = [
            Path("docs/development/guides") / f"{feature_name}-spec.md",
            Path("docs/development/guides")
            / f"{feature_name.replace('_', '-')}-spec.md",
            Path("docs/development/guides") / f"{feature_name}-overview.md",
            Path("docs/development/guides") / f"{feature_name}-process-enforcement.md",
            Path("docs/development/guides")
            / f"{feature_name}-technical-architecture.md",
            Path("docs/development/guides") / f"{feature_name}-implementation-plan.md",
        ]

        for candidate in spec_file_candidates:
            if candidate.exists():
                # Verify it contains spec-kit format patterns
                try:
                    content = candidate.read_text(encoding="utf-8")
                    if any(
                        re.search(pattern, content, re.MULTILINE)
                        for pattern in self.spec_kit_patterns
                    ):
                        return True
                except Exception:
                    continue

        return False

    def sequential_thinking_complete(self, feature_name: str) -> bool:
        """Verify Sequential Thinking methodology applied"""

        # Check specification files for Sequential Thinking indicators
        spec_content = self._get_specification_content(feature_name)
        if not spec_content:
            return False

        # Count Sequential Thinking methodology steps found
        found_steps = sum(
            1
            for pattern in self.sequential_thinking_patterns
            if pattern in spec_content
        )

        # Require minimum 3 of 6 steps for compliance
        return found_steps >= 3

    def context7_utilization_verified(self, feature_name: str) -> bool:
        """Verify Context7 MCP utilization per existing P0 requirements"""

        # Integration with existing test_context7_utilization_p0.py validation
        spec_content = self._get_specification_content(feature_name)
        if not spec_content:
            return False

        # Check specification includes Context7 utilization patterns
        return any(
            re.search(pattern, spec_content, re.IGNORECASE)
            for pattern in self.context7_patterns
        )

    def architectural_compliance_verified(self, feature_name: str) -> bool:
        """Verify PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md compliance"""

        spec_content = self._get_specification_content(feature_name)
        if not spec_content:
            return False

        # Check for architectural compliance indicators
        compliance_indicators = [
            "PROJECT_STRUCTURE.md",
            "BLOAT_PREVENTION_SYSTEM.md",
            "DRY principle",
            "SOLID principle",
            "architectural compliance",
            "validation infrastructure",
        ]

        found_indicators = sum(
            1 for indicator in compliance_indicators if indicator in spec_content
        )

        # Require minimum architectural awareness
        return found_indicators >= 2

    def _get_specification_content(self, feature_name: str) -> Optional[str]:
        """Get specification content for validation"""

        # Check multiple specification file locations
        spec_file_candidates = [
            Path("docs/development/guides") / f"{feature_name}-spec.md",
            Path("docs/development/guides")
            / f"{feature_name.replace('_', '-')}-spec.md",
            Path("docs/development/guides") / f"{feature_name}-overview.md",
            Path("docs/development/guides") / f"{feature_name}-process-enforcement.md",
            Path("docs/development/guides")
            / f"{feature_name}-technical-architecture.md",
            Path("docs/development/guides") / f"{feature_name}-implementation-plan.md",
        ]

        # Combine content from all available specification files
        combined_content = []
        for candidate in spec_file_candidates:
            if candidate.exists():
                try:
                    content = candidate.read_text(encoding="utf-8")
                    combined_content.append(content)
                except Exception:
                    continue

        return "\n\n".join(combined_content) if combined_content else None

    def _get_remediation_action(self, exception: Exception) -> str:
        """Get specific remediation action for process violation"""

        if isinstance(exception, SpecKitProcessViolation):
            return "1. Create specification using .claudedirector/templates/spec-kit-template.md"

        elif isinstance(exception, SequentialThinkingViolation):
            return "2. Apply Sequential Thinking 6-step methodology to specification"

        elif isinstance(exception, Context7UtilizationViolation):
            return "3. Document Context7 MCP utilization for strategic intelligence"

        elif isinstance(exception, ArchitecturalComplianceViolation):
            return "4. Verify PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md compliance"

        else:
            return "Review integrated process requirements"

    def create_development_request(
        self,
        feature_name: str,
        request_type: str = "implementation",
        file_paths: Optional[List[Path]] = None,
        strategic_context: Optional[Dict[str, Any]] = None,
        **requirements,
    ) -> DevelopmentRequest:
        """
        Factory method for creating development requests
        CONFIGURABLE process requirements based on request type
        """

        # Configure requirements based on request type and context
        requires_spec_kit = requirements.get("requires_spec_kit", True)
        requires_sequential_thinking = requirements.get(
            "requires_sequential_thinking", True
        )
        requires_context7_mcp = requirements.get("requires_context7_mcp", True)

        # Strategic work always requires all processes
        if any(
            keyword in feature_name.lower()
            for keyword in ["strategic", "intelligence", "framework", "compliance"]
        ):
            requires_spec_kit = True
            requires_sequential_thinking = True
            requires_context7_mcp = True

        return DevelopmentRequest(
            feature_name=feature_name,
            request_type=request_type,
            file_paths=file_paths or [],
            strategic_context=strategic_context or {},
            requires_spec_kit=requires_spec_kit,
            requires_sequential_thinking=requires_sequential_thinking,
            requires_context7_mcp=requires_context7_mcp,
        )


# Global enforcer instance for system-wide process enforcement
_process_enforcer: Optional[IntegratedProcessEnforcer] = None


def get_process_enforcer() -> IntegratedProcessEnforcer:
    """Get global IntegratedProcessEnforcer instance"""
    global _process_enforcer

    if _process_enforcer is None:
        _process_enforcer = IntegratedProcessEnforcer()

    return _process_enforcer


def enforce_integrated_process(
    feature_name: str, request_type: str = "implementation", **requirements
) -> ProcessValidation:
    """
    Convenience function for enforcing integrated process compliance
    BLOCKS development if requirements not met
    """

    enforcer = get_process_enforcer()
    request = enforcer.create_development_request(
        feature_name=feature_name, request_type=request_type, **requirements
    )

    validation = enforcer.validate_development_request(request)

    if not validation.approved:
        violation_messages = "\n".join(validation.violations)
        remediation_messages = "\n".join(validation.remediation_actions)

        raise ProcessViolationError(
            f"DEVELOPMENT BLOCKED - Process violations detected:\n\n"
            f"{violation_messages}\n\n"
            f"REMEDIATION REQUIRED:\n{remediation_messages}"
        )

    return validation


class ProcessViolationError(Exception):
    """Raised when development is blocked due to process violations"""

    pass


# Export public interface
__all__ = [
    "ProcessViolationType",
    "ProcessValidation",
    "DevelopmentRequest",
    "IntegratedProcessEnforcer",
    "SpecKitProcessViolation",
    "SequentialThinkingViolation",
    "Context7UtilizationViolation",
    "ArchitecturalComplianceViolation",
    "ProcessViolationError",
    "get_process_enforcer",
    "enforce_integrated_process",
]
