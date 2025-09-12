#!/usr/bin/env python3
"""
🚨 ENFORCEMENT ERROR HANDLING & RECOVERY SYSTEM
Robust error handling and graceful degradation for Real-Time Development Process Enforcement

🧠 SEQUENTIAL THINKING METHODOLOGY APPLIED:

🎯 Problem Definition:
Need robust error handling system for enforcement with graceful degradation,
automatic retry mechanisms, circuit breaker patterns, and recovery statistics.

🔍 Root Cause Analysis:
Without systematic error handling, enforcement system failures cascade, causing
complete system breakdown rather than graceful degradation. Need resilience
engineering patterns for enterprise-grade reliability.

🏗️ Solution Architecture:
Error handling framework with multiple recovery strategies (retry, fallback,
degrade, bypass), circuit breaker pattern, and comprehensive error context tracking.

⚡ Implementation Strategy:
1. Implement circuit breaker pattern for cascading failure prevention
2. Create multiple recovery strategies (retry, fallback, degrade, bypass)
3. Build comprehensive error context tracking and statistics
4. Add context manager for automatic error handling
5. Apply resilience engineering patterns

📈 Strategic Enhancement:
Error handling system ensures enforcement remains operational even during
partial failures, maintaining system reliability and preventing complete breakdowns.

📊 Success Metrics:
- <1% system downtime due to enforcement failures
- 95%+ successful error recovery rate
- Complete error context tracking for debugging

SOLID Principles Applied:
- Single Responsibility: Each class handles one specific error recovery concern
- Open/Closed: Extensible through RecoveryStrategy and ErrorHandler interfaces
- Liskov Substitution: All recovery strategies and handlers interchangeable
- Interface Segregation: Separate interfaces for different error handling concerns
- Dependency Inversion: Depends on abstract interfaces, not concrete implementations

DRY Principle Applied:
- Single error handling framework across all enforcement components
- Centralized retry logic eliminates duplication
- Reusable recovery patterns for all failure scenarios

🔧 Context7 MCP Integration:
Applies Context7 resilience engineering patterns for enterprise error handling
and systematic recovery methodologies.

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import time
import threading
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union, Type
from enum import Enum
from contextlib import contextmanager
from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    TimeoutError as FutureTimeoutError,
)

from .base_enforcement import (
    EnforcementResult,
    EnforcementViolation,
    EnforcementLevel,
    ViolationType,
)


class ErrorSeverity(Enum):
    """
    Error severity levels following DRY principle.
    Single source of truth for error classification.
    """

    LOW = "LOW"  # Minor issues, continue operation
    MEDIUM = "MEDIUM"  # Moderate issues, retry with degradation
    HIGH = "HIGH"  # Serious issues, fallback mode
    CRITICAL = "CRITICAL"  # System-threatening, emergency procedures


class RecoveryMode(Enum):
    """
    Recovery operation modes following DRY principle.
    Single source of truth for recovery strategies.
    """

    RETRY = "RETRY"  # Retry operation with backoff
    FALLBACK = "FALLBACK"  # Use alternative implementation
    DEGRADE = "DEGRADE"  # Reduce functionality gracefully
    BYPASS = "BYPASS"  # Skip non-critical validation
    EMERGENCY = "EMERGENCY"  # Emergency override mode
    FAIL_SAFE = "FAIL_SAFE"  # Safe failure mode


@dataclass(frozen=True)
class ErrorContext:
    """
    Immutable error context following SOLID Single Responsibility.

    This class has ONE responsibility: capture complete error context
    for recovery decision making.
    """

    error: Exception
    error_type: str
    severity: ErrorSeverity
    operation: str
    gate_name: Optional[str]
    timestamp: float
    retry_count: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None

    def __post_init__(self):
        """Initialize derived fields"""
        if not self.stack_trace:
            object.__setattr__(self, "stack_trace", traceback.format_exc())
        if not self.error_type:
            object.__setattr__(self, "error_type", type(self.error).__name__)


@dataclass(frozen=True)
class RecoveryResult:
    """
    Immutable recovery result following SOLID Single Responsibility.

    This class has ONE responsibility: represent the outcome of an error
    recovery attempt with all relevant metadata.
    """

    success: bool
    recovery_mode: RecoveryMode
    execution_time_ms: float
    message: str
    fallback_result: Optional[Any] = None
    should_retry: bool = False
    retry_delay_seconds: float = 0.0
    degraded_functionality: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate recovery result"""
        if self.execution_time_ms < 0:
            raise ValueError("execution_time_ms cannot be negative")
        if self.retry_delay_seconds < 0:
            raise ValueError("retry_delay_seconds cannot be negative")


class RecoveryStrategy(ABC):
    """
    Abstract recovery strategy interface following SOLID Interface Segregation.

    Single responsibility: Define recovery strategy for specific error types.
    """

    @abstractmethod
    def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if strategy can handle this error"""
        pass

    @abstractmethod
    def recover(self, error_context: ErrorContext) -> RecoveryResult:
        """Attempt recovery from error"""
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        """Recovery strategy priority (lower = higher priority)"""
        pass


class RetryRecoveryStrategy(RecoveryStrategy):
    """
    Retry-based recovery strategy following SOLID Single Responsibility.

    Single responsibility: Handle errors through retry with exponential backoff.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
        retryable_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        """
        Initialize retry recovery strategy.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
            max_delay: Maximum delay between retries
            backoff_multiplier: Exponential backoff multiplier
            retryable_exceptions: List of exception types that are retryable
        """
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._backoff_multiplier = backoff_multiplier
        self._retryable_exceptions = retryable_exceptions or [
            ConnectionError,
            TimeoutError,
            FutureTimeoutError,
            OSError,
        ]

    def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if error is retryable"""
        # Check retry count
        if error_context.retry_count >= self._max_retries:
            return False

        # Check if exception type is retryable
        return any(
            isinstance(error_context.error, exc_type)
            for exc_type in self._retryable_exceptions
        )

    def recover(self, error_context: ErrorContext) -> RecoveryResult:
        """Calculate retry parameters"""
        start_time = time.time()

        # Calculate exponential backoff delay
        delay = min(
            self._base_delay * (self._backoff_multiplier**error_context.retry_count),
            self._max_delay,
        )

        execution_time = (time.time() - start_time) * 1000

        return RecoveryResult(
            success=True,
            recovery_mode=RecoveryMode.RETRY,
            execution_time_ms=execution_time,
            message=f"Retry {error_context.retry_count + 1}/{self._max_retries} scheduled",
            should_retry=True,
            retry_delay_seconds=delay,
        )

    @property
    def priority(self) -> int:
        """High priority for retry strategy"""
        return 1


class FallbackRecoveryStrategy(RecoveryStrategy):
    """
    Fallback recovery strategy following SOLID Single Responsibility.

    Single responsibility: Provide alternative implementation when primary fails.
    """

    def __init__(
        self,
        fallback_implementations: Dict[str, Callable],
        fallback_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        """
        Initialize fallback recovery strategy.

        Args:
            fallback_implementations: Map of operation names to fallback functions
            fallback_exceptions: Exception types that trigger fallback
        """
        self._fallback_implementations = fallback_implementations
        self._fallback_exceptions = fallback_exceptions or [
            ImportError,
            ModuleNotFoundError,
            AttributeError,
            NotImplementedError,
        ]

    def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if fallback is available for this error"""
        # Check if exception type supports fallback
        if not any(
            isinstance(error_context.error, exc_type)
            for exc_type in self._fallback_exceptions
        ):
            return False

        # Check if fallback implementation exists
        return error_context.operation in self._fallback_implementations

    def recover(self, error_context: ErrorContext) -> RecoveryResult:
        """Execute fallback implementation"""
        start_time = time.time()

        try:
            fallback_func = self._fallback_implementations[error_context.operation]
            fallback_result = fallback_func(error_context.context)

            execution_time = (time.time() - start_time) * 1000

            return RecoveryResult(
                success=True,
                recovery_mode=RecoveryMode.FALLBACK,
                execution_time_ms=execution_time,
                message=f"Fallback implementation used for {error_context.operation}",
                fallback_result=fallback_result,
                degraded_functionality=[
                    f"Using fallback for {error_context.operation}"
                ],
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            return RecoveryResult(
                success=False,
                recovery_mode=RecoveryMode.FALLBACK,
                execution_time_ms=execution_time,
                message=f"Fallback implementation failed: {str(e)}",
            )

    @property
    def priority(self) -> int:
        """Medium priority for fallback strategy"""
        return 2


class GracefulDegradationStrategy(RecoveryStrategy):
    """
    Graceful degradation strategy following SOLID Single Responsibility.

    Single responsibility: Reduce functionality gracefully when errors occur.
    """

    def __init__(
        self,
        degradation_rules: Dict[str, Dict[str, Any]],
        degradable_severities: Optional[List[ErrorSeverity]] = None,
    ):
        """
        Initialize graceful degradation strategy.

        Args:
            degradation_rules: Rules for degrading functionality by operation
            degradable_severities: Error severities that allow degradation
        """
        self._degradation_rules = degradation_rules
        self._degradable_severities = degradable_severities or [
            ErrorSeverity.LOW,
            ErrorSeverity.MEDIUM,
        ]

    def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if error allows graceful degradation"""
        return (
            error_context.severity in self._degradable_severities
            and error_context.operation in self._degradation_rules
        )

    def recover(self, error_context: ErrorContext) -> RecoveryResult:
        """Apply graceful degradation"""
        start_time = time.time()

        degradation_rule = self._degradation_rules[error_context.operation]

        # Create degraded enforcement result
        degraded_result = EnforcementResult(
            gate_name=error_context.gate_name or "DEGRADED",
            operation=error_context.operation,
            passed=degradation_rule.get("allow_pass", False),
            violations=[],
            execution_time_ms=0.0,
            context={"degraded": True, "reason": str(error_context.error)},
        )

        execution_time = (time.time() - start_time) * 1000

        return RecoveryResult(
            success=True,
            recovery_mode=RecoveryMode.DEGRADE,
            execution_time_ms=execution_time,
            message=f"Graceful degradation applied to {error_context.operation}",
            fallback_result=degraded_result,
            degraded_functionality=degradation_rule.get("degraded_features", []),
        )

    @property
    def priority(self) -> int:
        """Lower priority for degradation strategy"""
        return 3


class CircuitBreakerRecoveryStrategy(RecoveryStrategy):
    """
    Circuit breaker recovery strategy following SOLID Single Responsibility.

    Single responsibility: Prevent cascading failures through circuit breaking.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3,
    ):
        """
        Initialize circuit breaker strategy.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time before attempting recovery
            half_open_max_calls: Max calls in half-open state
        """
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls

        # Circuit state tracking
        self._failure_counts: Dict[str, int] = {}
        self._last_failure_time: Dict[str, float] = {}
        self._circuit_states: Dict[str, str] = {}  # CLOSED, OPEN, HALF_OPEN
        self._half_open_calls: Dict[str, int] = {}
        self._lock = threading.Lock()

    def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if circuit breaker should handle this error"""
        operation_key = f"{error_context.gate_name}:{error_context.operation}"

        with self._lock:
            # Always handle if we're tracking this operation
            return (
                operation_key in self._circuit_states or error_context.retry_count > 0
            )

    def recover(self, error_context: ErrorContext) -> RecoveryResult:
        """Apply circuit breaker logic"""
        start_time = time.time()
        operation_key = f"{error_context.gate_name}:{error_context.operation}"

        with self._lock:
            # Initialize tracking for new operations
            if operation_key not in self._circuit_states:
                self._circuit_states[operation_key] = "CLOSED"
                self._failure_counts[operation_key] = 0
                self._half_open_calls[operation_key] = 0

            # Record failure
            self._failure_counts[operation_key] += 1
            self._last_failure_time[operation_key] = time.time()

            current_state = self._circuit_states[operation_key]

            # Determine new state
            if current_state == "CLOSED":
                if self._failure_counts[operation_key] >= self._failure_threshold:
                    self._circuit_states[operation_key] = "OPEN"
                    message = f"Circuit breaker OPENED for {operation_key}"
                    recovery_mode = RecoveryMode.FAIL_SAFE
                else:
                    message = f"Circuit breaker remains CLOSED for {operation_key}"
                    recovery_mode = RecoveryMode.RETRY

            elif current_state == "OPEN":
                # Check if recovery timeout has passed
                if (
                    time.time() - self._last_failure_time[operation_key]
                ) > self._recovery_timeout:
                    self._circuit_states[operation_key] = "HALF_OPEN"
                    self._half_open_calls[operation_key] = 0
                    message = f"Circuit breaker moved to HALF_OPEN for {operation_key}"
                    recovery_mode = RecoveryMode.RETRY
                else:
                    message = f"Circuit breaker remains OPEN for {operation_key}"
                    recovery_mode = RecoveryMode.FAIL_SAFE

            else:  # HALF_OPEN
                if self._half_open_calls[operation_key] < self._half_open_max_calls:
                    self._half_open_calls[operation_key] += 1
                    message = f"Circuit breaker HALF_OPEN trial {self._half_open_calls[operation_key]} for {operation_key}"
                    recovery_mode = RecoveryMode.RETRY
                else:
                    # Too many failures in half-open, back to open
                    self._circuit_states[operation_key] = "OPEN"
                    self._last_failure_time[operation_key] = time.time()
                    message = f"Circuit breaker back to OPEN for {operation_key}"
                    recovery_mode = RecoveryMode.FAIL_SAFE

            execution_time = (time.time() - start_time) * 1000

            return RecoveryResult(
                success=(recovery_mode != RecoveryMode.FAIL_SAFE),
                recovery_mode=recovery_mode,
                execution_time_ms=execution_time,
                message=message,
                should_retry=(recovery_mode == RecoveryMode.RETRY),
                retry_delay_seconds=1.0 if recovery_mode == RecoveryMode.RETRY else 0.0,
            )

    @property
    def priority(self) -> int:
        """High priority for circuit breaker"""
        return 0


class ErrorRecoveryManager:
    """
    Main error recovery manager following SOLID principles.

    SOLID Compliance:
    - Single Responsibility: Coordinates error recovery across enforcement system
    - Open/Closed: Extensible through RecoveryStrategy interface
    - Liskov Substitution: Works with any RecoveryStrategy implementation
    - Interface Segregation: Clean interface for error recovery
    - Dependency Inversion: Depends on RecoveryStrategy abstractions

    DRY Compliance:
    - Single error recovery coordination for all enforcement components
    - Eliminates duplication of error handling across gates
    """

    def __init__(
        self,
        strategies: Optional[List[RecoveryStrategy]] = None,
        default_max_retries: int = 3,
        enable_circuit_breaker: bool = True,
    ):
        """
        Initialize error recovery manager.

        Args:
            strategies: List of recovery strategies
            default_max_retries: Default maximum retry attempts
            enable_circuit_breaker: Whether to enable circuit breaker
        """
        self._strategies = strategies or []
        self._default_max_retries = default_max_retries
        self._recovery_history: List[ErrorContext] = []
        self._lock = threading.Lock()

        # Add default strategies if none provided
        if not self._strategies:
            self._add_default_strategies(enable_circuit_breaker)

        # Sort strategies by priority
        self._strategies.sort(key=lambda s: s.priority)

    def _add_default_strategies(self, enable_circuit_breaker: bool):
        """Add default recovery strategies"""
        if enable_circuit_breaker:
            self._strategies.append(CircuitBreakerRecoveryStrategy())

        self._strategies.append(
            RetryRecoveryStrategy(max_retries=self._default_max_retries)
        )

        # Add fallback implementations for common operations
        fallback_implementations = {
            "validation": lambda ctx: EnforcementResult(
                gate_name="FALLBACK",
                operation=ctx.get("operation", "unknown"),
                passed=False,
                violations=[
                    EnforcementViolation(
                        rule_id="FALLBACK_VALIDATION",
                        violation_type=ViolationType.SEQUENTIAL_THINKING,
                        level=EnforcementLevel.WARNING,
                        message="Using fallback validation due to error",
                    )
                ],
                execution_time_ms=0.0,
            )
        }

        self._strategies.append(FallbackRecoveryStrategy(fallback_implementations))

        # Add graceful degradation rules
        degradation_rules = {
            "sequential_thinking_validation": {
                "allow_pass": False,
                "degraded_features": ["Advanced pattern matching", "Context analysis"],
            },
            "bloat_prevention": {
                "allow_pass": True,
                "degraded_features": ["Real-time monitoring", "Detailed analysis"],
            },
        }

        self._strategies.append(GracefulDegradationStrategy(degradation_rules))

    def add_strategy(self, strategy: RecoveryStrategy) -> None:
        """
        Add recovery strategy.

        Args:
            strategy: RecoveryStrategy to add
        """
        with self._lock:
            self._strategies.append(strategy)
            self._strategies.sort(key=lambda s: s.priority)

    def recover_from_error(
        self,
        error: Exception,
        operation: str,
        gate_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> RecoveryResult:
        """
        Attempt to recover from error using available strategies.

        Args:
            error: Exception that occurred
            operation: Operation that failed
            gate_name: Name of the gate where error occurred
            context: Additional context for recovery
            retry_count: Current retry attempt count

        Returns:
            RecoveryResult with recovery outcome
        """
        # Classify error severity
        severity = self._classify_error_severity(error)

        # Create error context
        error_context = ErrorContext(
            error=error,
            error_type=type(error).__name__,
            severity=severity,
            operation=operation,
            gate_name=gate_name,
            timestamp=time.time(),
            retry_count=retry_count,
            context=context or {},
        )

        # Record error in history
        with self._lock:
            self._recovery_history.append(error_context)
            # Keep only recent history
            if len(self._recovery_history) > 1000:
                self._recovery_history = self._recovery_history[-500:]

        # Try recovery strategies in priority order
        for strategy in self._strategies:
            if strategy.can_handle(error_context):
                try:
                    result = strategy.recover(error_context)
                    if result.success:
                        return result
                except Exception as strategy_error:
                    # Strategy itself failed, try next one
                    continue

        # No strategy could handle the error
        return RecoveryResult(
            success=False,
            recovery_mode=RecoveryMode.FAIL_SAFE,
            execution_time_ms=0.0,
            message=f"No recovery strategy available for {type(error).__name__}",
        )

    def _classify_error_severity(self, error: Exception) -> ErrorSeverity:
        """Classify error severity based on exception type"""
        critical_errors = [SystemExit, KeyboardInterrupt, MemoryError]
        high_errors = [ImportError, ModuleNotFoundError, PermissionError]
        medium_errors = [ConnectionError, TimeoutError, OSError]

        if any(isinstance(error, exc_type) for exc_type in critical_errors):
            return ErrorSeverity.CRITICAL
        elif any(isinstance(error, exc_type) for exc_type in high_errors):
            return ErrorSeverity.HIGH
        elif any(isinstance(error, exc_type) for exc_type in medium_errors):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    @contextmanager
    def error_recovery_context(
        self,
        operation: str,
        gate_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None,
    ):
        """
        Context manager for automatic error recovery.

        Automatically handles retries and recovery strategies.
        """
        max_retries = max_retries or self._default_max_retries
        retry_count = 0

        while retry_count <= max_retries:
            try:
                yield retry_count
                break  # Success, exit retry loop

            except Exception as e:
                recovery_result = self.recover_from_error(
                    error=e,
                    operation=operation,
                    gate_name=gate_name,
                    context=context,
                    retry_count=retry_count,
                )

                if not recovery_result.should_retry or retry_count >= max_retries:
                    # No more retries or max retries reached
                    if recovery_result.fallback_result is not None:
                        # Use fallback result
                        yield recovery_result.fallback_result
                        break
                    else:
                        # Re-raise original exception
                        raise

                # Wait before retry
                if recovery_result.retry_delay_seconds > 0:
                    time.sleep(recovery_result.retry_delay_seconds)

                retry_count += 1

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get error recovery statistics"""
        with self._lock:
            if not self._recovery_history:
                return {
                    "total_errors": 0,
                    "error_types": {},
                    "severity_distribution": {},
                    "operations": {},
                }

            error_types = {}
            severity_distribution = {}
            operations = {}

            for error_context in self._recovery_history:
                # Count error types
                error_type = error_context.error_type
                error_types[error_type] = error_types.get(error_type, 0) + 1

                # Count severity distribution
                severity = error_context.severity.value
                severity_distribution[severity] = (
                    severity_distribution.get(severity, 0) + 1
                )

                # Count operations
                operation = error_context.operation
                operations[operation] = operations.get(operation, 0) + 1

            return {
                "total_errors": len(self._recovery_history),
                "error_types": error_types,
                "severity_distribution": severity_distribution,
                "operations": operations,
                "recent_errors": len(
                    [
                        ec
                        for ec in self._recovery_history
                        if time.time() - ec.timestamp < 3600  # Last hour
                    ]
                ),
            }

    def clear_history(self) -> None:
        """Clear error recovery history"""
        with self._lock:
            self._recovery_history.clear()


# Export public API following DRY principle
__all__ = [
    "ErrorSeverity",
    "RecoveryMode",
    "ErrorContext",
    "RecoveryResult",
    "RecoveryStrategy",
    "RetryRecoveryStrategy",
    "FallbackRecoveryStrategy",
    "GracefulDegradationStrategy",
    "CircuitBreakerRecoveryStrategy",
    "ErrorRecoveryManager",
]
