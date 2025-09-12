#!/usr/bin/env python3
"""
P0 Test: Proactive Code Generation Compliance System

🛡️ BUSINESS-CRITICAL: Ensures proactive compliance system blocks non-compliant development
🏗️ Martin | Platform Architecture with Sequential Thinking + Context7 MCP Integration

P0 PROTECTION SCOPE:
✅ IntegratedProcessEnforcer blocks development without spec-kit
✅ Sequential Thinking methodology validation (PRE-EXISTING REQUIREMENT)
✅ Context7 MCP utilization verification (PRE-EXISTING REQUIREMENT)
✅ Architectural compliance enforcement (PROJECT_STRUCTURE.md + BLOAT_PREVENTION_SYSTEM.md)
✅ ProactiveComplianceEngine integration with existing UnifiedPreventionEngine

INTEGRATION VALIDATION:
✅ Extends existing P0Module patterns (DRY compliance)
✅ Leverages existing Context7 patterns from P0 tests
✅ Maintains UnifiedPreventionEngine compatibility
✅ Zero regression risk for existing validation systems

Author: Strategic Team (Diego, Martin, Camille, Rachel, Alvaro)
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    # Import from claudedirector package
    from .claudedirector.lib.core.validation.proactive_compliance_engine import (
        ComplianceConstraintEngine,
        ProactiveComplianceEngine,
        ProactiveComplianceViolation,
        GenerationRequest,
        create_proactive_compliance_engine,
    )
    from .claudedirector.lib.core.validation.integrated_process_enforcer import (
        IntegratedProcessEnforcer,
        DevelopmentRequest,
        ProcessValidation,
        SpecKitProcessViolation,
        SequentialThinkingViolation,
        Context7UtilizationViolation,
        ArchitecturalComplianceViolation,
        enforce_integrated_process,
        ProcessViolationError,
    )
    from .claudedirector.lib.core.unified_factory import (
        ComponentType,
        create_compliance_constraint_engine,
        create_proactive_compliance_engine as factory_create_proactive_engine,
    )
except ImportError as e:
    # Try alternative import path
    try:
        sys.path.insert(0, str(project_root / ".claudedirector"))
        from lib.core.validation.proactive_compliance_engine import (
            ComplianceConstraintEngine,
            ProactiveComplianceEngine,
            ProactiveComplianceViolation,
            GenerationRequest,
            create_proactive_compliance_engine,
        )
        from lib.core.validation.integrated_process_enforcer import (
            IntegratedProcessEnforcer,
            DevelopmentRequest,
            ProcessValidation,
            SpecKitProcessViolation,
            SequentialThinkingViolation,
            Context7UtilizationViolation,
            ArchitecturalComplianceViolation,
            enforce_integrated_process,
            ProcessViolationError,
        )
        from lib.core.unified_factory import (
            ComponentType,
            create_compliance_constraint_engine,
            create_proactive_compliance_engine as factory_create_proactive_engine,
        )
    except ImportError as e2:
        # Fallback imports for testing - create mock implementations
        print(f"Import errors: {e}, {e2}")

        # Mock implementations for testing when imports fail
        class MockEngine:
            def __init__(self):
                self.name = "MockEngine"
                self.constraints = []

        class MockEnforcer:
            def __init__(self):
                self.name = "MockEnforcer"

        class MockException(Exception):
            pass

        # Assign mocks to expected names
        ComplianceConstraintEngine = MockEngine
        ProactiveComplianceEngine = MockEngine
        IntegratedProcessEnforcer = MockEnforcer
        ProactiveComplianceViolation = MockException
        GenerationRequest = dict
        DevelopmentRequest = dict
        ProcessValidation = dict
        SpecKitProcessViolation = MockException
        SequentialThinkingViolation = MockException
        Context7UtilizationViolation = MockException
        ArchitecturalComplianceViolation = MockException
        ProcessViolationError = MockException
        ComponentType = object

        def mock_function(*args, **kwargs):
            return MockEngine()

        create_proactive_compliance_engine = mock_function
        enforce_integrated_process = mock_function
        create_compliance_constraint_engine = mock_function
        factory_create_proactive_engine = mock_function


class TestProactiveComplianceSystemP0:
    """
    P0 Business-Critical Tests for Proactive Compliance System

    CRITICAL BUSINESS IMPACT: Prevents architectural violations from reaching production
    ZERO TOLERANCE: All tests must pass for system deployment
    """

    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.temp_dir / "docs" / "development" / "guides"
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        # Create mock spec-kit specification
        self.spec_content = """# Proactive Code Generation Compliance Specification

**Spec-Kit Format v1.0** | **Status**: Draft | **Owner**: Martin | Platform Architecture

---

## 📋 **Executive Summary**

**Business Impact**: Transforms development from reactive validation to proactive compliance.

## 🧠 **Sequential Thinking Applied**

### **1. Problem Definition**
Enforce compliance constraints during code generation rather than after.

### **2. Root Cause Analysis**
Reactive validation allows violations to reach production.

### **3. Solution Architecture**
Proactive constraint system with existing validation integration.

### **4. Implementation Strategy**
Extend UnifiedPreventionEngine with new ComplianceModule.

### **5. Strategic Enhancement**
🔧 Context7 MCP for intelligent constraint application and architectural compliance validation.

### **6. Success Metrics**
100% compliant generation, zero architectural violations.

## 🎯 **Requirements**

**Context7 MCP Integration**: Strategic frameworks must leverage Context7 intelligence for pattern recognition.

**Architectural Compliance**: Must follow PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md requirements.
"""

    def teardown_method(self):
        """Cleanup test environment"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_compliance_constraint_engine_initialization_p0(self):
        """P0: ComplianceConstraintEngine initializes with required constraints"""

        engine = ComplianceConstraintEngine()

        # CRITICAL: Engine must initialize successfully
        assert engine is not None
        assert engine.name == "ProactiveCompliance"

        # CRITICAL: Must have all required constraint types
        constraint_types = {c.constraint_type for c in engine.constraints}
        required_types = {
            "spec_kit",
            "sequential_thinking",
            "context7",
            "architectural",
        }

        assert required_types.issubset(
            constraint_types
        ), f"Missing required constraint types: {required_types - constraint_types}"

        # CRITICAL: Must integrate with existing P0Module patterns
        assert hasattr(engine, "p0_module")
        assert hasattr(engine, "context7_patterns")
        assert hasattr(engine, "sequential_thinking_patterns")

    def test_integrated_process_enforcer_blocks_missing_spec_kit_p0(self):
        """P0: IntegratedProcessEnforcer blocks development without spec-kit"""

        enforcer = IntegratedProcessEnforcer()

        # Create development request without spec-kit
        request = DevelopmentRequest(
            feature_name="test_feature_without_spec",
            request_type="implementation",
            requires_spec_kit=True,
        )

        # CRITICAL: Must block development without spec-kit
        validation = enforcer.validate_development_request(request)

        assert not validation.approved, "Must block development without spec-kit"
        assert len(validation.violations) > 0
        assert any(
            "spec-kit" in violation.lower() for violation in validation.violations
        )
        assert any("BLOCKED" in violation for violation in validation.violations)

    def test_integrated_process_enforcer_blocks_missing_sequential_thinking_p0(self):
        """P0: IntegratedProcessEnforcer blocks development without Sequential Thinking"""

        enforcer = IntegratedProcessEnforcer()

        # Create spec file without Sequential Thinking patterns
        spec_file = self.docs_dir / "test-feature-spec.md"
        spec_file.write_text(
            """# Test Feature Specification

**Spec-Kit Format v1.0** | **Status**: Draft | **Owner**: Test

Basic specification without Sequential Thinking methodology.
"""
        )

        request = DevelopmentRequest(
            feature_name="test_feature",
            request_type="implementation",
            requires_sequential_thinking=True,
        )

        # CRITICAL: Must block development without Sequential Thinking
        validation = enforcer.validate_development_request(request)

        assert (
            not validation.approved
        ), "Must block development without Sequential Thinking"
        assert any(
            "Sequential Thinking" in violation for violation in validation.violations
        )

    def test_integrated_process_enforcer_blocks_missing_context7_p0(self):
        """P0: IntegratedProcessEnforcer blocks development without Context7 MCP"""

        enforcer = IntegratedProcessEnforcer()

        # Create spec file without Context7 patterns
        spec_file = self.docs_dir / "strategic-feature-spec.md"
        spec_file.write_text(
            """# Strategic Feature Specification

**Spec-Kit Format v1.0** | **Status**: Draft | **Owner**: Test

## 📋 **Executive Summary**
Strategic feature without Context7 MCP integration.

## 🧠 **Sequential Thinking Applied**
### **1. Problem Definition**
Test problem definition.

### **2. Root Cause Analysis**
Test root cause analysis.

### **3. Solution Architecture**
Test solution architecture.
"""
        )

        request = DevelopmentRequest(
            feature_name="strategic_feature",
            request_type="implementation",
            requires_context7_mcp=True,
        )

        # CRITICAL: Must block strategic development without Context7 MCP
        validation = enforcer.validate_development_request(request)

        assert (
            not validation.approved
        ), "Must block strategic development without Context7 MCP"
        assert any("Context7" in violation for violation in validation.violations)

    def test_integrated_process_enforcer_approves_compliant_request_p0(self):
        """P0: IntegratedProcessEnforcer approves fully compliant development request"""

        enforcer = IntegratedProcessEnforcer()

        # Create compliant spec file
        spec_file = self.docs_dir / "compliant-feature-spec.md"
        spec_file.write_text(self.spec_content)

        request = DevelopmentRequest(
            feature_name="compliant_feature",
            request_type="implementation",
            requires_spec_kit=True,
            requires_sequential_thinking=True,
            requires_context7_mcp=True,
        )

        # CRITICAL: Must approve fully compliant request
        validation = enforcer.validate_development_request(request)

        assert (
            validation.approved
        ), f"Must approve compliant request. Violations: {validation.violations}"
        assert len(validation.violations) == 0

    def test_proactive_compliance_engine_extends_unified_prevention_engine_p0(self):
        """P0: ProactiveComplianceEngine properly extends UnifiedPreventionEngine"""

        engine = ProactiveComplianceEngine()

        # CRITICAL: Must extend existing UnifiedPreventionEngine
        assert hasattr(engine, "modules")
        assert hasattr(engine, "hard_enforcement")
        assert hasattr(engine, "validate_file")

        # CRITICAL: Must include ComplianceConstraintEngine
        compliance_modules = [
            module
            for module in engine.modules
            if isinstance(module, ComplianceConstraintEngine)
        ]
        assert (
            len(compliance_modules) == 1
        ), "Must include exactly one ComplianceConstraintEngine"

        # CRITICAL: Must maintain existing validation modules (DRY compliance)
        module_names = {module.get_name() for module in engine.modules}
        required_modules = {
            "BloatPrevention",
            "P0Enforcement",
            "Security",
            "QualityAssurance",
        }

        assert required_modules.issubset(
            module_names
        ), f"Missing required validation modules: {required_modules - module_names}"

    def test_proactive_compliance_engine_blocks_non_compliant_generation_p0(self):
        """P0: ProactiveComplianceEngine blocks non-compliant code generation"""

        engine = ProactiveComplianceEngine(hard_enforcement=True)

        # Create non-compliant generation request
        request = GenerationRequest(
            feature_name="non_compliant_feature",
            file_path=Path("test_file.py"),
            content_type="implementation",
            requires_spec_kit=True,
            requires_sequential_thinking=True,
            requires_context7_mcp=True,
        )

        # CRITICAL: Must block non-compliant generation with hard enforcement
        with pytest.raises(ProactiveComplianceViolation) as exc_info:
            engine.validate_generation_request(request)

        assert "BLOCKED" in str(exc_info.value)
        assert "compliance violations" in str(exc_info.value)

    def test_unified_factory_integration_p0(self):
        """P0: UnifiedFactory integration with proactive compliance components"""

        # CRITICAL: Factory must create ComplianceConstraintEngine
        constraint_engine = create_compliance_constraint_engine()
        assert constraint_engine is not None
        assert hasattr(constraint_engine, "validate_generation_request")

        # CRITICAL: Factory must create ProactiveComplianceEngine
        compliance_engine = factory_create_proactive_engine(hard_enforcement=True)
        assert compliance_engine is not None
        assert hasattr(compliance_engine, "validate_generation_request")
        assert compliance_engine.hard_enforcement is True

    def test_enforce_integrated_process_convenience_function_p0(self):
        """P0: enforce_integrated_process convenience function blocks violations"""

        # CRITICAL: Must block development for non-compliant feature
        with pytest.raises(ProcessViolationError) as exc_info:
            enforce_integrated_process(
                feature_name="non_compliant_test_feature", request_type="implementation"
            )

        assert "DEVELOPMENT BLOCKED" in str(exc_info.value)
        assert "Process violations detected" in str(exc_info.value)
        assert "REMEDIATION REQUIRED" in str(exc_info.value)

    def test_existing_p0_module_integration_p0(self):
        """P0: Integration with existing P0Module validation patterns"""

        engine = ComplianceConstraintEngine()

        # CRITICAL: Must reuse existing P0Module patterns (DRY compliance)
        assert hasattr(engine, "p0_module")

        # CRITICAL: Must use existing Sequential Thinking patterns
        expected_st_patterns = [
            "Problem Definition",
            "Root Cause Analysis",
            "Solution Architecture",
            "Implementation Strategy",
            "Strategic Enhancement",
            "Success Metrics",
        ]

        for pattern in expected_st_patterns:
            assert pattern in engine.sequential_thinking_patterns

        # CRITICAL: Must use existing Context7 patterns
        expected_context7_patterns = [
            r"Context7.*MCP",
            r"strategic.*framework.*Context7",
            r"MCP.*Context7.*coordination",
            r"Context7.*pattern.*recognition",
        ]

        for pattern in expected_context7_patterns:
            assert pattern in engine.context7_patterns

    def test_zero_regression_existing_validation_p0(self):
        """P0: Proactive compliance system must not break existing validation"""

        engine = ProactiveComplianceEngine()

        # CRITICAL: Must maintain all existing validation capabilities
        test_file = self.temp_dir / "test_validation.py"
        test_file.write_text(
            """
# Test file for validation
def test_function():
    password = "hardcoded_password"  # Security violation
    return "duplicate string", "duplicate string"  # DRY violation
"""
        )

        # CRITICAL: Must detect existing violation types
        results = engine.validate_file(test_file)

        # Must have results from existing modules
        assert len(results) > 0

        # Must detect security violations (existing SecurityModule)
        security_results = [r for name, r in results.items() if "Security" in name]
        if security_results:
            assert any(len(r.violations) > 0 for r in security_results)

    def test_performance_requirements_p0(self):
        """P0: Proactive compliance system must meet performance requirements"""

        import time

        engine = ProactiveComplianceEngine()
        enforcer = IntegratedProcessEnforcer()

        # Create test request
        request = DevelopmentRequest(
            feature_name="performance_test_feature", request_type="implementation"
        )

        # CRITICAL: Validation must complete within 2 seconds
        start_time = time.time()
        validation = enforcer.validate_development_request(request)
        end_time = time.time()

        processing_time = (end_time - start_time) * 1000  # Convert to ms

        assert (
            processing_time < 2000
        ), f"Validation took {processing_time}ms, must be <2000ms"
        assert validation.validation_time_ms < 2000


# P0 Test execution validation
def test_p0_test_execution():
    """Validate that all P0 tests can be executed"""

    # This test ensures the P0 test suite itself is functional
    test_instance = TestProactiveComplianceSystemP0()
    test_instance.setup_method()

    try:
        # Run a basic validation to ensure system is operational
        test_instance.test_compliance_constraint_engine_initialization_p0()
    finally:
        test_instance.teardown_method()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
