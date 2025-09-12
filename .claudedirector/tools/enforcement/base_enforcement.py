#!/usr/bin/env python3
"""
🚨 BASE ENFORCEMENT FRAMEWORK
Foundation classes for Real-Time Development Process Enforcement System

SOLID Principles Applied:
- Single Responsibility: Each class has one specific enforcement concern
- Open/Closed: Extensible through abstract interfaces, closed for modification
- Liskov Substitution: All enforcement gates implement common interface
- Interface Segregation: Separate interfaces for different enforcement concerns
- Dependency Inversion: Depends on abstractions, not concrete implementations

DRY Principle Applied:
- Single source of truth for enforcement patterns
- Reusable base classes eliminate duplication
- Common validation logic centralized

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import time
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from pathlib import Path


class EnforcementLevel(Enum):
    """
    Enforcement severity levels following DRY principle.
    Single source of truth for enforcement priorities.
    """

    MANDATORY = "MANDATORY"  # BLOCKS ALL OPERATIONS
    CRITICAL = "CRITICAL"  # BLOCKS COMMITS/DEPLOYMENTS
    WARNING = "WARNING"  # LOGS BUT ALLOWS
    INFO = "INFO"  # INFORMATIONAL ONLY


class ViolationType(Enum):
    """
    Types of enforcement violations following DRY principle.
    Single source of truth for violation categories.
    """

    SEQUENTIAL_THINKING = "SEQUENTIAL_THINKING"
    CONTEXT7_ENHANCEMENT = "CONTEXT7_ENHANCEMENT"
    SPEC_KIT_FORMAT = "SPEC_KIT_FORMAT"
    SOLID_PRINCIPLE = "SOLID_PRINCIPLE"
    DRY_PRINCIPLE = "DRY_PRINCIPLE"
    PROJECT_STRUCTURE = "PROJECT_STRUCTURE"
    BLOAT_PREVENTION = "BLOAT_PREVENTION"
    P0_PROTECTION = "P0_PROTECTION"
    SUCCESS_CRITERIA = "SUCCESS_CRITERIA"


@dataclass(frozen=True)
class EnforcementViolation:
    """
    Immutable violation record following SOLID Single Responsibility Principle.

    This class has ONE responsibility: represent a single enforcement violation
    with all necessary context for remediation.
    """

    rule_id: str
    violation_type: ViolationType
    level: EnforcementLevel
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    context: Dict[str, Any] = field(default_factory=dict)
    remediation_steps: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        """Validate violation data integrity"""
        if not self.rule_id:
            raise ValueError("rule_id cannot be empty")
        if not self.message:
            raise ValueError("message cannot be empty")
        if self.line_number is not None and self.line_number < 1:
            raise ValueError("line_number must be positive")


@dataclass(frozen=True)
class EnforcementResult:
    """
    Immutable enforcement validation result following SOLID Single Responsibility.

    This class has ONE responsibility: represent the outcome of an enforcement
    validation with all violations and metadata.
    """

    gate_name: str
    operation: str
    passed: bool
    violations: List[EnforcementViolation] = field(default_factory=list)
    execution_time_ms: float = 0.0
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        """Validate result data integrity"""
        if not self.gate_name:
            raise ValueError("gate_name cannot be empty")
        if not self.operation:
            raise ValueError("operation cannot be empty")
        if self.execution_time_ms < 0:
            raise ValueError("execution_time_ms cannot be negative")

    @property
    def blocking_violations(self) -> List[EnforcementViolation]:
        """Get violations that should block operations (MANDATORY level)"""
        return [v for v in self.violations if v.level == EnforcementLevel.MANDATORY]

    @property
    def should_block(self) -> bool:
        """Determine if this result should block the operation"""
        return not self.passed or len(self.blocking_violations) > 0

    def get_violations_by_type(
        self, violation_type: ViolationType
    ) -> List[EnforcementViolation]:
        """Get all violations of a specific type"""
        return [v for v in self.violations if v.violation_type == violation_type]


class EnforcementGate(ABC):
    """
    Abstract base class for all enforcement gates following SOLID principles.

    SOLID Compliance:
    - Single Responsibility: Each gate validates one specific concern
    - Open/Closed: Extensible through inheritance, closed for modification
    - Liskov Substitution: All gates can be used interchangeably
    - Interface Segregation: Minimal interface with only essential methods
    - Dependency Inversion: Depends on abstract interfaces

    DRY Compliance:
    - Common enforcement patterns centralized in base class
    - Eliminates duplication across specific gate implementations
    """

    def __init__(self, gate_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize enforcement gate with configuration.

        Args:
            gate_name: Unique identifier for this gate
            config: Optional configuration dictionary
        """
        if not gate_name:
            raise ValueError("gate_name cannot be empty")

        self._gate_name = gate_name
        self._config = config or {}
        self._enabled = self._config.get("enabled", True)

    @property
    def gate_name(self) -> str:
        """Get gate name (immutable)"""
        return self._gate_name

    @property
    def is_enabled(self) -> bool:
        """Check if gate is enabled"""
        return self._enabled

    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> EnforcementResult:
        """
        Validate enforcement rules against provided context.

        Args:
            context: Validation context with operation details

        Returns:
            EnforcementResult with validation outcome and violations

        Raises:
            NotImplementedError: Must be implemented by concrete gates
        """
        pass

    @abstractmethod
    def get_remediation_guidance(self, violation: EnforcementViolation) -> List[str]:
        """
        Get specific remediation guidance for a violation.

        Args:
            violation: The enforcement violation to remediate

        Returns:
            List of actionable remediation steps

        Raises:
            NotImplementedError: Must be implemented by concrete gates
        """
        pass

    def _create_violation(
        self,
        rule_id: str,
        violation_type: ViolationType,
        level: EnforcementLevel,
        message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
        remediation_steps: Optional[List[str]] = None,
    ) -> EnforcementViolation:
        """
        Create enforcement violation with consistent formatting.

        DRY Principle: Centralized violation creation eliminates duplication
        across all gate implementations.
        """
        return EnforcementViolation(
            rule_id=rule_id,
            violation_type=violation_type,
            level=level,
            message=message,
            file_path=file_path,
            line_number=line_number,
            context=context or {},
            remediation_steps=remediation_steps or [],
        )

    def _create_result(
        self,
        operation: str,
        passed: bool,
        violations: Optional[List[EnforcementViolation]] = None,
        execution_time_ms: float = 0.0,
        context: Optional[Dict[str, Any]] = None,
    ) -> EnforcementResult:
        """
        Create enforcement result with consistent formatting.

        DRY Principle: Centralized result creation eliminates duplication
        across all gate implementations.
        """
        return EnforcementResult(
            gate_name=self._gate_name,
            operation=operation,
            passed=passed,
            violations=violations or [],
            execution_time_ms=execution_time_ms,
            context=context or {},
        )

    def _measure_execution_time(self, start_time: float) -> float:
        """
        Measure execution time in milliseconds.

        DRY Principle: Common timing logic centralized.
        """
        return (time.time() - start_time) * 1000


class EnforcementOrchestrator:
    """
    Orchestrates multiple enforcement gates following SOLID principles.

    SOLID Compliance:
    - Single Responsibility: Coordinates enforcement gate execution
    - Open/Closed: Extensible by adding new gates, closed for modification
    - Liskov Substitution: Works with any EnforcementGate implementation
    - Interface Segregation: Clean interface for orchestration
    - Dependency Inversion: Depends on EnforcementGate abstraction

    DRY Compliance:
    - Single orchestration logic for all enforcement scenarios
    - Eliminates duplication of gate coordination code
    """

    def __init__(self, gates: Optional[List[EnforcementGate]] = None):
        """
        Initialize orchestrator with enforcement gates.

        Args:
            gates: List of enforcement gates to orchestrate
        """
        self._gates = gates or []
        self._results_cache: Dict[str, EnforcementResult] = {}

    def add_gate(self, gate: EnforcementGate) -> None:
        """
        Add enforcement gate to orchestrator.

        Args:
            gate: EnforcementGate to add

        Raises:
            ValueError: If gate is None or already exists
        """
        if gate is None:
            raise ValueError("gate cannot be None")

        if any(g.gate_name == gate.gate_name for g in self._gates):
            raise ValueError(f"Gate {gate.gate_name} already exists")

        self._gates.append(gate)

    def remove_gate(self, gate_name: str) -> bool:
        """
        Remove enforcement gate by name.

        Args:
            gate_name: Name of gate to remove

        Returns:
            True if gate was removed, False if not found
        """
        for i, gate in enumerate(self._gates):
            if gate.gate_name == gate_name:
                del self._gates[i]
                return True
        return False

    def validate_all(
        self, operation: str, context: Dict[str, Any], fail_fast: bool = False
    ) -> List[EnforcementResult]:
        """
        Validate all enforcement gates against context.

        Args:
            operation: Operation being validated
            context: Validation context
            fail_fast: Stop on first failure if True

        Returns:
            List of EnforcementResult from all gates
        """
        results = []

        for gate in self._gates:
            if not gate.is_enabled:
                continue

            try:
                result = gate.validate(context)
                results.append(result)

                # Fail fast on blocking violations
                if fail_fast and result.should_block:
                    break

            except Exception as e:
                # Create error result for gate failures
                error_violation = EnforcementViolation(
                    rule_id=f"{gate.gate_name}_GATE_ERROR",
                    violation_type=ViolationType.SEQUENTIAL_THINKING,  # Default type
                    level=EnforcementLevel.CRITICAL,
                    message=f"Gate {gate.gate_name} failed: {str(e)}",
                    context={"exception": str(e), "gate": gate.gate_name},
                )

                error_result = EnforcementResult(
                    gate_name=gate.gate_name,
                    operation=operation,
                    passed=False,
                    violations=[error_violation],
                    context=context,
                )

                results.append(error_result)

                if fail_fast:
                    break

        return results

    def get_blocking_violations(
        self, results: List[EnforcementResult]
    ) -> List[EnforcementViolation]:
        """
        Get all blocking violations from results.

        Args:
            results: List of enforcement results

        Returns:
            List of all blocking violations
        """
        blocking_violations = []
        for result in results:
            blocking_violations.extend(result.blocking_violations)
        return blocking_violations

    def should_block_operation(self, results: List[EnforcementResult]) -> bool:
        """
        Determine if operation should be blocked based on results.

        Args:
            results: List of enforcement results

        Returns:
            True if operation should be blocked
        """
        return len(self.get_blocking_violations(results)) > 0

    @property
    def gate_count(self) -> int:
        """Get number of registered gates"""
        return len(self._gates)

    @property
    def enabled_gate_count(self) -> int:
        """Get number of enabled gates"""
        return sum(1 for gate in self._gates if gate.is_enabled)


# Export public API following DRY principle
__all__ = [
    "EnforcementLevel",
    "ViolationType",
    "EnforcementViolation",
    "EnforcementResult",
    "EnforcementGate",
    "EnforcementOrchestrator",
]
