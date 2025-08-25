"""
Unit Tests for FrameworkMCPCoordinator - Phase 2 AI Intelligence

🏗️ Martin | Platform Architecture - Team Lead
🤖 Berny | Senior AI Developer

Comprehensive test coverage for FrameworkMCPCoordinator ensuring:
- Multi-framework coordination with MCP enhancement
- Conflict resolution using MCP intelligence
- Complex orchestration scenarios (3+ frameworks)
- Performance requirements (<300ms coordination latency)
- Complete transparency and audit trail
- Graceful fallback for coordination failures

DO NOT SKIP - MANDATORY P0 COVERAGE
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import sys

# Handle import paths for test environment
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from claudedirector.lib.ai_intelligence.framework_mcp_coordinator import (
        FrameworkMCPCoordinator,
        CoordinationComplexity,
        FrameworkConflict,
        CoordinationResult,
        create_framework_mcp_coordinator,
    )
    from claudedirector.lib.core.enhanced_framework_engine import (
        MultiFrameworkIntegrationEngine,
        ConversationContext,
    )
    from claudedirector.lib.ai_intelligence.mcp_enhanced_framework_engine import (
        MCPEnhancedFrameworkEngine,
        FrameworkDetectionResult,
    )
    from claudedirector.lib.transparency.integrated_transparency import (
        IntegratedTransparencySystem,
        MCPDisclosure,
    )
except ImportError:
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    from lib.ai_intelligence.framework_mcp_coordinator import (
        FrameworkMCPCoordinator,
        CoordinationComplexity,
        FrameworkConflict,
        CoordinationResult,
        create_framework_mcp_coordinator,
    )
    from lib.core.enhanced_framework_engine import (
        MultiFrameworkIntegrationEngine,
        ConversationContext,
    )
    from lib.ai_intelligence.mcp_enhanced_framework_engine import (
        MCPEnhancedFrameworkEngine,
        FrameworkDetectionResult,
    )
    from lib.transparency.integrated_transparency import (
        IntegratedTransparencySystem,
        MCPDisclosure,
    )


class TestFrameworkMCPCoordinator:
    """Test suite for FrameworkMCPCoordinator"""

    def setup_method(self):
        """Set up test fixtures"""
        # Mock dependencies
        self.mock_multi_framework_engine = Mock(spec=MultiFrameworkIntegrationEngine)
        self.mock_mcp_enhanced_engine = Mock(spec=MCPEnhancedFrameworkEngine)
        self.mock_mcp_helper = Mock()
        self.mock_transparency_system = Mock(spec=IntegratedTransparencySystem)

        # Configure mock base engine
        mock_base_engine = Mock()
        mock_base_engine.detect_applicable_frameworks.return_value = [
            "rumelt_strategy_kernel",
            "team_topologies",
            "decisive_wrap_framework",
            "accelerate_team_performance",
        ]
        self.mock_multi_framework_engine.base_engine = mock_base_engine

        # Configure mock MCP enhanced engine
        mock_detection_result = FrameworkDetectionResult(
            detected_frameworks=["rumelt_strategy_kernel"],
            confidence_scores={"rumelt_strategy_kernel": 0.92},
            mcp_enhancements_applied=["context7_validation"],
            baseline_accuracy=0.875,
            enhanced_accuracy=0.92,
            improvement_percentage=5.1,
        )
        self.mock_mcp_enhanced_engine.enhance_framework_detection = AsyncMock(
            return_value=mock_detection_result
        )

        # Configure mock MCP helper
        self.mock_mcp_helper.enhance_with_sequential = AsyncMock(
            return_value="Sequential MCP analysis result"
        )
        self.mock_mcp_helper.enhance_with_context7 = AsyncMock(
            return_value="Context7 MCP analysis result"
        )

        # Configure mock transparency system
        mock_disclosure = MCPDisclosure(
            server_name="test_server",
            capability="test_capability",
            persona="diego",
            processing_message="Test processing",
        )
        self.mock_transparency_system.create_mcp_enhancement_disclosure.return_value = (
            mock_disclosure
        )

        # Create coordinator instance
        self.coordinator = FrameworkMCPCoordinator(
            multi_framework_engine=self.mock_multi_framework_engine,
            mcp_enhanced_engine=self.mock_mcp_enhanced_engine,
            mcp_helper=self.mock_mcp_helper,
            transparency_system=self.mock_transparency_system,
        )

        # Test context
        self.test_context = ConversationContext(
            session_id="test_session",
            recent_interactions=[],
            conversation_themes=set(),
            complexity_progression=[],
        )

    def test_coordinator_initialization(self):
        """Test FrameworkMCPCoordinator initialization"""
        assert (
            self.coordinator.multi_framework_engine == self.mock_multi_framework_engine
        )
        assert self.coordinator.mcp_enhanced_engine == self.mock_mcp_enhanced_engine
        assert self.coordinator.mcp_helper == self.mock_mcp_helper
        assert self.coordinator.transparency_system == self.mock_transparency_system

        # Check configuration initialization
        assert "single_framework_threshold" in self.coordinator.coordination_thresholds
        assert (
            "recommendation_conflict" in self.coordinator.conflict_resolution_strategies
        )
        assert "sequential_then_context" in self.coordinator.mcp_orchestration_patterns

        # Check metrics initialization
        assert self.coordinator.coordinator_metrics["coordinations_processed"] == 0
        assert self.coordinator.coordinator_metrics["conflicts_resolved"] == 0

    def test_complexity_analysis_single_framework(self):
        """Test coordination complexity analysis for single framework scenarios"""
        simple_input = "What is team topologies?"

        complexity = asyncio.run(
            self.coordinator._analyze_coordination_complexity(
                simple_input, self.test_context
            )
        )

        assert complexity == CoordinationComplexity.SINGLE

    def test_complexity_analysis_multi_framework(self):
        """Test coordination complexity analysis for multi-framework scenarios"""
        complex_input = """
        How should we approach organizational transformation while implementing
        platform architecture changes and managing stakeholder alignment across
        technical and business domains?
        """

        complexity = asyncio.run(
            self.coordinator._analyze_coordination_complexity(
                complex_input, self.test_context
            )
        )

        assert complexity in [
            CoordinationComplexity.MULTI,
            CoordinationComplexity.ENTERPRISE,
        ]

    def test_framework_detection_based_on_complexity(self):
        """Test framework detection adjusts based on complexity level"""
        test_input = "Strategic platform assessment"

        # Test single complexity
        single_frameworks = asyncio.run(
            self.coordinator._detect_required_frameworks(
                test_input, self.test_context, CoordinationComplexity.SINGLE
            )
        )
        assert len(single_frameworks) == 1

        # Test multi complexity
        multi_frameworks = asyncio.run(
            self.coordinator._detect_required_frameworks(
                test_input, self.test_context, CoordinationComplexity.MULTI
            )
        )
        assert len(multi_frameworks) <= 4
        assert len(multi_frameworks) > len(single_frameworks)

    def test_conflict_identification(self):
        """Test framework conflict identification"""
        frameworks = [
            "rumelt_strategy_kernel",
            "team_topologies",
            "decisive_wrap_framework",
        ]

        conflicts = asyncio.run(
            self.coordinator._identify_framework_conflicts(
                frameworks, "test input", self.test_context
            )
        )

        # Should identify some conflicts between these frameworks
        assert isinstance(conflicts, list)
        # Verify conflict structure if any found
        for conflict in conflicts:
            assert hasattr(conflict, "framework_a")
            assert hasattr(conflict, "framework_b")
            assert hasattr(conflict, "conflict_type")
            assert hasattr(conflict, "severity")

    def test_mcp_framework_enhancement(self):
        """Test MCP enhancement of individual frameworks"""
        frameworks = ["rumelt_strategy_kernel", "team_topologies"]
        test_input = "Strategic organizational change"

        enhanced_results = asyncio.run(
            self.coordinator._enhance_frameworks_with_mcp(
                frameworks, test_input, "test_session", "diego"
            )
        )

        assert len(enhanced_results) == len(frameworks)
        for framework in frameworks:
            assert framework in enhanced_results
            result = enhanced_results[framework]
            assert isinstance(result, FrameworkDetectionResult)
            assert result.enhanced_accuracy >= result.baseline_accuracy

        # Verify MCP enhanced engine was called for each framework
        assert (
            self.mock_mcp_enhanced_engine.enhance_framework_detection.call_count
            == len(frameworks)
        )

    def test_conflict_resolution_with_mcp(self):
        """Test MCP-based conflict resolution"""
        # Create test conflict requiring MCP resolution
        test_conflict = FrameworkConflict(
            framework_a="rumelt_strategy_kernel",
            framework_b="team_topologies",
            conflict_type="approach",
            severity=0.7,  # Above threshold for MCP resolution
            resolution_strategy="initial",
            mcp_resolution_needed=True,
        )

        enhanced_frameworks = {
            "rumelt_strategy_kernel": FrameworkDetectionResult(
                detected_frameworks=["rumelt_strategy_kernel"],
                confidence_scores={"rumelt_strategy_kernel": 0.90},
                mcp_enhancements_applied=["sequential_analysis"],
                baseline_accuracy=0.875,
                enhanced_accuracy=0.90,
                improvement_percentage=2.9,
            )
        }

        resolved_conflicts = asyncio.run(
            self.coordinator._resolve_conflicts_with_mcp(
                [test_conflict], enhanced_frameworks, "test input", "diego"
            )
        )

        assert len(resolved_conflicts) == 1
        resolved_conflict = resolved_conflicts[0]
        assert resolved_conflict.severity < test_conflict.severity  # Should be reduced
        assert "mcp_" in resolved_conflict.resolution_strategy
        assert not resolved_conflict.mcp_resolution_needed

        # Verify MCP helper was called
        assert (
            self.mock_mcp_helper.enhance_with_sequential.called
            or self.mock_mcp_helper.enhance_with_context7.called
        )

    def test_framework_synthesis(self):
        """Test synthesis of multiple enhanced frameworks"""
        enhanced_frameworks = {
            "rumelt_strategy_kernel": FrameworkDetectionResult(
                detected_frameworks=["rumelt_strategy_kernel"],
                confidence_scores={"rumelt_strategy_kernel": 0.92},
                mcp_enhancements_applied=["sequential_analysis"],
                baseline_accuracy=0.875,
                enhanced_accuracy=0.92,
                improvement_percentage=5.1,
            ),
            "team_topologies": FrameworkDetectionResult(
                detected_frameworks=["team_topologies"],
                confidence_scores={"team_topologies": 0.88},
                mcp_enhancements_applied=["context7_validation"],
                baseline_accuracy=0.875,
                enhanced_accuracy=0.88,
                improvement_percentage=0.6,
            ),
        }

        resolved_conflicts = []

        synthesis_result = asyncio.run(
            self.coordinator._synthesize_coordinated_frameworks(
                enhanced_frameworks,
                resolved_conflicts,
                CoordinationComplexity.DUAL,
                "diego",
            )
        )

        assert "primary_frameworks" in synthesis_result
        assert "supporting_frameworks" in synthesis_result
        assert "confidence" in synthesis_result
        assert "mcp_enhancements" in synthesis_result

        # Primary framework should be highest confidence
        assert synthesis_result["primary_frameworks"][0] == "rumelt_strategy_kernel"
        assert synthesis_result["confidence"] > 0.75  # Should meet minimum threshold

    def test_full_coordination_workflow(self):
        """Test complete coordination workflow"""
        test_input = """
        How should we approach organizational transformation while implementing
        platform architecture changes and managing cross-functional alignment?
        """

        result = asyncio.run(
            self.coordinator.coordinate_frameworks(
                user_input=test_input,
                session_id="test_session",
                persona="diego",
                context=self.test_context,
            )
        )

        # Verify result structure
        assert isinstance(result, CoordinationResult)
        assert isinstance(result.primary_frameworks, list)
        assert isinstance(result.supporting_frameworks, list)
        assert isinstance(result.coordination_complexity, CoordinationComplexity)
        assert isinstance(result.conflicts_resolved, list)
        assert isinstance(result.mcp_enhancements_applied, list)
        assert 0.0 <= result.synthesis_confidence <= 1.0
        assert result.processing_time_ms > 0
        assert isinstance(result.transparency_disclosures, list)

        # Verify metrics were updated
        assert self.coordinator.coordinator_metrics["coordinations_processed"] == 1

    def test_coordination_performance_requirement(self):
        """Test coordination meets performance requirements (<300ms)"""
        test_input = "Strategic platform assessment with stakeholder alignment"

        start_time = time.time()
        result = asyncio.run(
            self.coordinator.coordinate_frameworks(
                user_input=test_input,
                session_id="perf_test",
                persona="diego",
                context=self.test_context,
            )
        )
        end_time = time.time()

        actual_time_ms = (end_time - start_time) * 1000

        # Performance requirement: <300ms coordination latency
        assert (
            actual_time_ms < 300
        ), f"Coordination took {actual_time_ms}ms, exceeds 300ms requirement"
        assert result.processing_time_ms < 300

    def test_transparency_disclosure_generation(self):
        """Test transparency disclosure generation"""
        enhanced_frameworks = {
            "rumelt_strategy_kernel": FrameworkDetectionResult(
                detected_frameworks=["rumelt_strategy_kernel"],
                confidence_scores={"rumelt_strategy_kernel": 0.92},
                mcp_enhancements_applied=["sequential_analysis"],
                baseline_accuracy=0.875,
                enhanced_accuracy=0.92,
                improvement_percentage=5.1,
            )
        }

        conflicts = [
            FrameworkConflict(
                framework_a="rumelt_strategy_kernel",
                framework_b="team_topologies",
                conflict_type="approach",
                severity=0.4,
                resolution_strategy="mcp_hybrid_synthesis",
                mcp_resolution_needed=False,
            )
        ]

        disclosures = self.coordinator._generate_coordination_disclosures(
            CoordinationComplexity.MULTI, conflicts, enhanced_frameworks, "diego"
        )

        assert isinstance(disclosures, list)
        assert len(disclosures) > 0

        # Verify transparency system was called
        assert self.mock_transparency_system.create_mcp_enhancement_disclosure.called

    def test_fallback_coordination_result(self):
        """Test fallback coordination when main process fails"""
        fallback_result = self.coordinator._create_fallback_coordination_result(
            "test input", "diego"
        )

        assert isinstance(fallback_result, CoordinationResult)
        assert len(fallback_result.primary_frameworks) == 1
        assert (
            fallback_result.primary_frameworks[0] == "rumelt_strategy_kernel"
        )  # Safe default
        assert fallback_result.synthesis_confidence == 0.60  # Lower confidence
        assert len(fallback_result.transparency_disclosures) > 0

    def test_coordinator_metrics_tracking(self):
        """Test coordinator metrics tracking and calculation"""
        # Initial metrics
        initial_metrics = self.coordinator.get_coordinator_metrics()
        assert initial_metrics["coordinations_processed"] == 0

        # Simulate coordination
        self.coordinator._update_coordinator_metrics(
            CoordinationComplexity.MULTI, 2, 150.0
        )

        updated_metrics = self.coordinator.get_coordinator_metrics()
        assert updated_metrics["coordinations_processed"] == 1
        assert updated_metrics["conflicts_resolved"] == 2
        assert updated_metrics["mcp_orchestrations_executed"] == 1
        assert updated_metrics["avg_coordination_time_ms"] == 150.0

    def test_factory_function(self):
        """Test factory function for creating coordinator"""
        coordinator = create_framework_mcp_coordinator(
            multi_framework_engine=self.mock_multi_framework_engine,
            mcp_enhanced_engine=self.mock_mcp_enhanced_engine,
            mcp_helper=self.mock_mcp_helper,
            transparency_system=self.mock_transparency_system,
        )

        assert isinstance(coordinator, FrameworkMCPCoordinator)
        assert coordinator.multi_framework_engine == self.mock_multi_framework_engine
        assert coordinator.mcp_enhanced_engine == self.mock_mcp_enhanced_engine

    def test_error_handling_and_graceful_degradation(self):
        """Test error handling and graceful degradation"""
        # Configure mock to raise exception
        self.mock_mcp_enhanced_engine.enhance_framework_detection.side_effect = (
            Exception("MCP enhancement failed")
        )

        test_input = "Strategic platform assessment"

        # Should not raise exception, should return fallback result
        result = asyncio.run(
            self.coordinator.coordinate_frameworks(
                user_input=test_input,
                session_id="error_test",
                persona="diego",
                context=self.test_context,
            )
        )

        # Should get fallback result
        assert isinstance(result, CoordinationResult)
        assert result.synthesis_confidence == 0.60  # Fallback confidence
        assert len(result.transparency_disclosures) > 0

    def test_complex_enterprise_coordination(self):
        """Test complex enterprise-level coordination scenario"""
        enterprise_input = """
        We need to coordinate organizational transformation across multiple business units
        while implementing platform architecture changes, managing stakeholder alignment,
        optimizing team topologies, and ensuring accelerated performance delivery.
        This involves technical, business, people, process, and technology considerations
        with executive visibility and cross-functional coordination requirements.
        """

        result = asyncio.run(
            self.coordinator.coordinate_frameworks(
                user_input=enterprise_input,
                session_id="enterprise_test",
                persona="camille",
                context=self.test_context,
            )
        )

        # Should handle enterprise complexity
        assert result.coordination_complexity in [
            CoordinationComplexity.MULTI,
            CoordinationComplexity.ENTERPRISE,
        ]
        assert len(result.primary_frameworks) >= 1
        assert len(result.primary_frameworks) + len(result.supporting_frameworks) >= 2
        assert (
            result.synthesis_confidence >= 0.60
        )  # Should maintain reasonable confidence
        assert len(result.transparency_disclosures) > 0  # Should have transparency


if __name__ == "__main__":
    pytest.main([__file__])
