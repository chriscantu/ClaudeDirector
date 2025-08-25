"""
Unit Tests for MCPEnhancedFrameworkEngine - Phase 2 AI Intelligence

🏗️ Martin | Platform Architecture - Team Lead
🤖 Berny | Senior AI Developer

Comprehensive test coverage for MCPEnhancedFrameworkEngine ensuring:
- 95%+ framework detection accuracy target
- MCP server integration reliability
- Performance requirements (<200ms latency)
- Complete transparency and audit trail
- Graceful fallback to baseline detection

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
    from claudedirector.lib.ai_intelligence.mcp_enhanced_framework_engine import (
        MCPEnhancedFrameworkEngine,
        EnhancedFrameworkUsage,
        FrameworkDetectionResult,
        FrameworkConfidenceLevel,
        create_mcp_enhanced_framework_engine,
    )
    from claudedirector.lib.transparency.framework_detection import (
        FrameworkDetectionMiddleware,
        FrameworkUsage,
    )
    from claudedirector.lib.transparency.integrated_transparency import (
        TransparencyContext,
    )
except ImportError:
    sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector"))
    from lib.ai_intelligence.mcp_enhanced_framework_engine import (
        MCPEnhancedFrameworkEngine,
        EnhancedFrameworkUsage,
        FrameworkDetectionResult,
        FrameworkConfidenceLevel,
        create_mcp_enhanced_framework_engine,
    )
    from lib.transparency.framework_detection import (
        FrameworkDetectionMiddleware,
        FrameworkUsage,
    )
    from lib.transparency.integrated_transparency import TransparencyContext


class TestMCPEnhancedFrameworkEngine:
    """Comprehensive test suite for MCPEnhancedFrameworkEngine"""

    def setup_method(self):
        """Setup test fixtures"""
        # Mock baseline detector
        self.mock_baseline_detector = Mock(spec=FrameworkDetectionMiddleware)

        # Mock MCP helper
        self.mock_mcp_helper = AsyncMock()

        # Mock transparency context
        self.mock_transparency_context = Mock(spec=TransparencyContext)
        self.mock_transparency_context.persona = "diego"

        # Create engine instance
        self.engine = MCPEnhancedFrameworkEngine(
            baseline_detector=self.mock_baseline_detector,
            mcp_helper=self.mock_mcp_helper,
            transparency_context=self.mock_transparency_context,
        )

    def test_engine_initialization(self):
        """Test MCPEnhancedFrameworkEngine initialization"""

        # Verify engine is properly initialized
        assert self.engine.baseline_detector == self.mock_baseline_detector
        assert self.engine.mcp_helper == self.mock_mcp_helper
        assert self.engine.transparency_context == self.mock_transparency_context

        # Verify configuration is set up
        assert "low_confidence" in self.engine.confidence_thresholds
        assert "strategic" in self.engine.mcp_server_mapping
        assert "low_confidence" in self.engine.enhancement_strategies

        # Verify metrics are initialized
        assert self.engine.engine_metrics["detections_processed"] == 0
        assert self.engine.engine_metrics["mcp_enhancements_applied"] == 0

    def test_confidence_level_determination(self):
        """Test confidence level determination for MCP routing"""

        # Test low confidence
        assert (
            self.engine._determine_confidence_level(0.5) == FrameworkConfidenceLevel.LOW
        )
        assert (
            self.engine._determine_confidence_level(0.69)
            == FrameworkConfidenceLevel.LOW
        )

        # Test medium confidence
        assert (
            self.engine._determine_confidence_level(0.7)
            == FrameworkConfidenceLevel.MEDIUM
        )
        assert (
            self.engine._determine_confidence_level(0.85)
            == FrameworkConfidenceLevel.MEDIUM
        )

        # Test high confidence
        assert (
            self.engine._determine_confidence_level(0.9)
            == FrameworkConfidenceLevel.HIGH
        )
        assert (
            self.engine._determine_confidence_level(0.95)
            == FrameworkConfidenceLevel.HIGH
        )

    @pytest.mark.asyncio
    async def test_baseline_detection_integration(self):
        """Test integration with existing FrameworkDetectionMiddleware"""

        # Setup baseline detection mock
        baseline_frameworks = [
            FrameworkUsage(
                framework_name="Team Topologies",
                confidence_score=0.8,
                matched_patterns=["team structure", "cognitive load"],
                framework_type="organizational",
            ),
            FrameworkUsage(
                framework_name="WRAP Framework",
                confidence_score=0.6,  # Low confidence - should trigger MCP
                matched_patterns=["wrap decision"],
                framework_type="decision",
            ),
        ]
        self.mock_baseline_detector.detect_frameworks_used.return_value = (
            baseline_frameworks
        )

        # Setup MCP enhancement mocks
        self.mock_mcp_helper.call_mcp_server.return_value = Mock(confidence=0.9)

        # Test detection
        content = "We need to restructure teams using team topologies and apply wrap decision framework"
        result = await self.engine.detect_frameworks_enhanced(content)

        # Verify baseline detector was called
        self.mock_baseline_detector.detect_frameworks_used.assert_called_once_with(
            content
        )

        # Verify result structure
        assert isinstance(result, FrameworkDetectionResult)
        assert len(result.detected_frameworks) == 2
        assert result.baseline_accuracy == 0.875  # Expected baseline
        assert result.enhanced_accuracy > result.baseline_accuracy
        assert result.processing_time_ms > 0

    @pytest.mark.asyncio
    async def test_mcp_enhancement_low_confidence(self):
        """Test MCP enhancement for low confidence frameworks"""

        # Create low confidence framework
        framework = FrameworkUsage(
            framework_name="Good Strategy Bad Strategy",
            confidence_score=0.5,  # Low confidence
            matched_patterns=["strategy kernel"],
            framework_type="strategic",
        )

        # Setup MCP mocks for low confidence enhancement
        context7_result = Mock(confidence=0.85)
        sequential_result = Mock(confidence=0.9)

        self.mock_mcp_helper.call_mcp_server.side_effect = [
            context7_result,  # Context7 call
            sequential_result,  # Sequential call
        ]

        # Test enhancement
        enhanced = await self.engine._enhance_framework_detection(
            framework, "test content", {"context": "strategic"}
        )

        # Verify MCP servers were called
        assert self.mock_mcp_helper.call_mcp_server.call_count == 2

        # Verify enhancement results
        assert enhanced.mcp_validated == True
        assert enhanced.mcp_server_used == "context7"  # Primary server
        assert enhanced.confidence_score > framework.confidence_score  # Improved
        assert enhanced.mcp_enhancement_confidence is not None

    @pytest.mark.asyncio
    async def test_mcp_enhancement_medium_confidence(self):
        """Test MCP enhancement for medium confidence frameworks"""

        # Create medium confidence framework
        framework = FrameworkUsage(
            framework_name="Design Thinking",
            confidence_score=0.8,  # Medium confidence
            matched_patterns=["design thinking", "empathize"],
            framework_type="innovation",
        )

        # Setup MCP mock for medium confidence enhancement
        context7_result = Mock(confidence=0.9)
        self.mock_mcp_helper.call_mcp_server.return_value = context7_result

        # Test enhancement
        enhanced = await self.engine._enhance_framework_detection(
            framework, "test content", None
        )

        # Verify only Context7 was called (not Sequential)
        assert self.mock_mcp_helper.call_mcp_server.call_count == 1
        self.mock_mcp_helper.call_mcp_server.assert_called_with(
            "context7",
            "framework_pattern_validation",
            framework_name="Design Thinking",
            content="test content",
            patterns=["design thinking", "empathize"],
        )

        # Verify enhancement
        assert enhanced.mcp_validated == True
        assert enhanced.confidence_score > framework.confidence_score

    @pytest.mark.asyncio
    async def test_mcp_enhancement_high_confidence(self):
        """Test that high confidence frameworks skip MCP enhancement"""

        # Create high confidence framework
        framework = FrameworkUsage(
            framework_name="Porter's Five Forces",
            confidence_score=0.95,  # High confidence
            matched_patterns=["porter's five forces", "competitive analysis"],
            framework_type="strategic",
        )

        # Test enhancement
        enhanced = await self.engine._enhance_framework_detection(
            framework, "test content", None
        )

        # Verify no MCP calls were made
        assert self.mock_mcp_helper.call_mcp_server.call_count == 0

        # Verify framework unchanged except for type conversion
        assert enhanced.framework_name == framework.framework_name
        assert enhanced.confidence_score == framework.confidence_score
        assert enhanced.mcp_validated == False
        assert enhanced.mcp_server_used is None

    @pytest.mark.asyncio
    async def test_framework_discovery(self):
        """Test MCP-driven discovery of additional frameworks"""

        # Setup existing frameworks
        existing_frameworks = [
            EnhancedFrameworkUsage(
                framework_name="Team Topologies",
                confidence_score=0.9,
                matched_patterns=["team structure"],
                framework_type="organizational",
            )
        ]

        # Setup MCP discovery mock
        discovery_result = Mock()
        discovery_result.recommended_frameworks = [
            Mock(
                name="Conway's Law",
                confidence=0.8,
                patterns=["conway's law", "organizational structure"],
                type="organizational",
            ),
            Mock(
                name="Accelerate Framework",
                confidence=0.85,
                patterns=["accelerate", "deployment frequency"],
                type="technical",
            ),
        ]

        self.mock_mcp_helper.call_mcp_server.return_value = discovery_result

        # Test discovery
        discovered = await self.engine._discover_additional_frameworks(
            "content about organizational structure and deployment practices",
            existing_frameworks,
            {"context": "technical"},
        )

        # Verify MCP server was called for discovery
        self.mock_mcp_helper.call_mcp_server.assert_called_once_with(
            "sequential",
            "framework_recommendation",
            content="content about organizational structure and deployment practices",
            context={"context": "technical"},
            exclude_frameworks=["Team Topologies"],
        )

        # Verify discovered frameworks
        assert len(discovered) == 2
        assert discovered[0].framework_name == "Conway's Law"
        assert discovered[1].framework_name == "Accelerate Framework"
        assert all(fw.mcp_validated for fw in discovered)
        assert all(fw.mcp_server_used == "sequential" for fw in discovered)

    @pytest.mark.asyncio
    async def test_result_synthesis(self):
        """Test synthesis and deduplication of framework results"""

        # Create frameworks with duplicates and varying confidence
        frameworks = [
            EnhancedFrameworkUsage(
                framework_name="Team Topologies",
                confidence_score=0.8,
                matched_patterns=["team structure"],
                framework_type="organizational",
            ),
            EnhancedFrameworkUsage(
                framework_name="WRAP Framework",
                confidence_score=0.9,
                matched_patterns=["wrap decision"],
                framework_type="decision",
            ),
            EnhancedFrameworkUsage(
                framework_name="Team Topologies",  # Duplicate with higher confidence
                confidence_score=0.95,
                matched_patterns=["team structure", "cognitive load"],
                framework_type="organizational",
                mcp_validated=True,
            ),
        ]

        # Test synthesis
        synthesized = self.engine._synthesize_framework_results(frameworks)

        # Verify deduplication and sorting
        assert len(synthesized) == 2  # Duplicates removed
        assert (
            synthesized[0].framework_name == "Team Topologies"
        )  # Higher confidence first
        assert synthesized[0].confidence_score == 0.95  # Higher confidence version kept
        assert synthesized[1].framework_name == "WRAP Framework"

    @pytest.mark.asyncio
    async def test_performance_requirements(self):
        """Test that engine meets <200ms performance requirement"""

        # Setup minimal baseline detection
        self.mock_baseline_detector.detect_frameworks_used.return_value = [
            FrameworkUsage(
                framework_name="Test Framework",
                confidence_score=0.9,  # High confidence - no MCP calls
                matched_patterns=["test"],
                framework_type="test",
            )
        ]

        # Test performance
        start_time = time.time()
        result = await self.engine.detect_frameworks_enhanced("test content")
        end_time = time.time()

        # Verify performance requirement
        actual_time_ms = (end_time - start_time) * 1000
        assert (
            actual_time_ms < 200
        ), f"Performance requirement failed: {actual_time_ms:.1f}ms > 200ms"
        assert result.processing_time_ms < 200

    @pytest.mark.asyncio
    async def test_accuracy_improvement_calculation(self):
        """Test accuracy improvement calculation and metrics"""

        # Setup baseline frameworks
        baseline_frameworks = [
            FrameworkUsage(
                framework_name="Framework 1",
                confidence_score=0.7,
                matched_patterns=["pattern1"],
                framework_type="strategic",
            )
        ]
        self.mock_baseline_detector.detect_frameworks_used.return_value = (
            baseline_frameworks
        )

        # Setup MCP enhancement
        self.mock_mcp_helper.call_mcp_server.return_value = Mock(confidence=0.9)

        # Test detection
        result = await self.engine.detect_frameworks_enhanced("test content")

        # Verify accuracy calculations
        assert result.baseline_accuracy == 0.875  # Expected baseline
        assert result.enhanced_accuracy > result.baseline_accuracy
        assert result.improvement_percentage > 0

        # Verify metrics were updated
        assert self.engine.engine_metrics["detections_processed"] == 1
        assert self.engine.engine_metrics["mcp_enhancements_applied"] == 1

    @pytest.mark.asyncio
    async def test_mcp_failure_fallback(self):
        """Test graceful fallback when MCP servers fail"""

        # Setup baseline detection
        baseline_frameworks = [
            FrameworkUsage(
                framework_name="Test Framework",
                confidence_score=0.5,  # Low confidence - should trigger MCP
                matched_patterns=["test"],
                framework_type="test",
            )
        ]
        self.mock_baseline_detector.detect_frameworks_used.return_value = (
            baseline_frameworks
        )

        # Setup MCP failure
        self.mock_mcp_helper.call_mcp_server.side_effect = Exception(
            "MCP server unavailable"
        )

        # Test fallback behavior
        result = await self.engine.detect_frameworks_enhanced("test content")

        # Verify fallback to baseline
        assert len(result.detected_frameworks) == 1
        assert result.detected_frameworks[0].framework_name == "Test Framework"
        assert result.detected_frameworks[0].mcp_validated == False
        assert (
            result.baseline_accuracy == result.enhanced_accuracy
        )  # No improvement due to failure
        assert len(result.mcp_servers_used) == 0

    @pytest.mark.asyncio
    async def test_complete_detection_pipeline(self):
        """Test complete end-to-end detection pipeline"""

        # Setup comprehensive baseline detection
        baseline_frameworks = [
            FrameworkUsage(
                "Team Topologies", 0.6, ["team structure"], "organizational"
            ),  # Low - MCP
            FrameworkUsage(
                "Design Thinking", 0.8, ["design thinking"], "innovation"
            ),  # Medium - MCP
            FrameworkUsage(
                "Porter's Five Forces", 0.95, ["porter's"], "strategic"
            ),  # High - no MCP
        ]
        self.mock_baseline_detector.detect_frameworks_used.return_value = (
            baseline_frameworks
        )

        # Setup MCP enhancement responses
        self.mock_mcp_helper.call_mcp_server.return_value = Mock(confidence=0.9)

        # Setup MCP discovery
        discovery_result = Mock()
        discovery_result.recommended_frameworks = [
            Mock(
                name="WRAP Framework",
                confidence=0.85,
                patterns=["wrap"],
                type="decision",
            )
        ]
        # First calls for enhancement, last call for discovery
        self.mock_mcp_helper.call_mcp_server.side_effect = [
            Mock(confidence=0.9),  # Context7 for Team Topologies
            Mock(confidence=0.85),  # Sequential for Team Topologies
            Mock(confidence=0.9),  # Context7 for Design Thinking
            discovery_result,  # Sequential for discovery
        ]

        # Test complete pipeline
        content = """
        We need to restructure our teams using team topologies principles.
        Apply design thinking methodology for user research.
        Porter's five forces analysis shows competitive pressure.
        """

        result = await self.engine.detect_frameworks_enhanced(
            content, {"domain": "organizational", "complexity": "high"}
        )

        # Verify comprehensive results
        assert len(result.detected_frameworks) == 4  # 3 baseline + 1 discovered
        assert result.enhanced_accuracy > result.baseline_accuracy
        assert result.improvement_percentage > 0
        assert len(result.mcp_servers_used) > 0

        # Verify framework names
        framework_names = [fw.framework_name for fw in result.detected_frameworks]
        assert "Team Topologies" in framework_names
        assert "Design Thinking" in framework_names
        assert "Porter's Five Forces" in framework_names
        assert "WRAP Framework" in framework_names

        # Verify MCP enhancements
        enhanced_frameworks = [
            fw for fw in result.detected_frameworks if fw.mcp_validated
        ]
        assert len(enhanced_frameworks) >= 2  # Low and medium confidence + discovered

    def test_factory_function(self):
        """Test factory function for creating MCPEnhancedFrameworkEngine"""

        # Mock dependencies
        mock_mcp_client = Mock()
        mock_transparency_context = Mock(spec=TransparencyContext)

        # Test factory function
        with patch(
            "lib.ai_intelligence.mcp_enhanced_framework_engine.FrameworkDetectionMiddleware"
        ) as mock_detector, patch(
            "lib.ai_intelligence.mcp_enhanced_framework_engine.RealMCPIntegrationHelper"
        ) as mock_helper:

            engine = create_mcp_enhanced_framework_engine(
                mock_mcp_client, mock_transparency_context
            )

            # Verify engine creation
            assert isinstance(engine, MCPEnhancedFrameworkEngine)
            mock_detector.assert_called_once()
            mock_helper.assert_called_once()


class TestEnhancedFrameworkUsage:
    """Test EnhancedFrameworkUsage dataclass"""

    def test_enhanced_framework_creation(self):
        """Test creation of EnhancedFrameworkUsage"""

        framework = EnhancedFrameworkUsage(
            framework_name="Test Framework",
            confidence_score=0.8,
            matched_patterns=["test", "framework"],
            framework_type="test",
            mcp_validated=True,
            mcp_server_used="context7",
            mcp_enhancement_confidence=0.9,
        )

        assert framework.framework_name == "Test Framework"
        assert framework.confidence_score == 0.8
        assert framework.mcp_validated == True
        assert framework.mcp_server_used == "context7"
        assert framework.mcp_enhancement_confidence == 0.9


class TestFrameworkDetectionResult:
    """Test FrameworkDetectionResult dataclass"""

    def test_detection_result_creation(self):
        """Test creation of FrameworkDetectionResult"""

        frameworks = [
            EnhancedFrameworkUsage(
                framework_name="Test Framework",
                confidence_score=0.9,
                matched_patterns=["test"],
                framework_type="test",
            )
        ]

        result = FrameworkDetectionResult(
            detected_frameworks=frameworks,
            detection_confidence=0.92,
            processing_time_ms=150,
            mcp_servers_used=["context7"],
            baseline_accuracy=0.875,
            enhanced_accuracy=0.92,
            improvement_percentage=5.1,
        )

        assert len(result.detected_frameworks) == 1
        assert result.detection_confidence == 0.92
        assert result.processing_time_ms == 150
        assert result.mcp_servers_used == ["context7"]
        assert result.improvement_percentage == 5.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
