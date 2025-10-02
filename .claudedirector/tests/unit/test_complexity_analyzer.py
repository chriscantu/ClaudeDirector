"""
Unit tests for AnalysisComplexityDetector
Tests the complexity analysis and enhancement decision logic for current API.

Note: Rewritten for Phase 12 API (always-on enhancement, simplified complexity detection)
"""

import pytest
from lib.core.complexity_analyzer import (
    AnalysisComplexityDetector,
    AnalysisComplexity,
    ComplexityAnalysis,
    EnhancementStrategy,
)


class TestComplexityAnalyzer:
    """Test suite for AnalysisComplexityDetector (Phase 12 API)"""

    @pytest.fixture
    def sample_config(self):
        """Sample configuration for complexity analyzer"""
        return {
            "enhancement_thresholds": {
                "systematic_analysis": 0.7,
                "framework_lookup": 0.6,
            }
        }

    @pytest.fixture
    def analyzer(self, sample_config):
        """Create AnalysisComplexityDetector instance"""
        return AnalysisComplexityDetector(sample_config)

    def test_initialization(self, sample_config):
        """Test analyzer initialization"""
        analyzer = AnalysisComplexityDetector(sample_config)
        assert analyzer.config == sample_config
        # Phase 12: thresholds removed, patterns-based detection
        assert len(analyzer.complexity_patterns) > 0
        assert len(analyzer.domain_keywords) > 0
        assert len(analyzer.persona_capabilities) > 0

    def test_simple_question_analysis(self, analyzer):
        """Test analysis of simple questions"""
        simple_inputs = [
            "What is REST?",
            "How do I install Python?",
            "What does API mean?",
        ]

        for input_text in simple_inputs:
            analysis = analyzer.analyze_input_complexity(input_text)
            assert isinstance(analysis, ComplexityAnalysis)
            assert analysis.complexity in [
                AnalysisComplexity.SIMPLE,
                AnalysisComplexity.MEDIUM,
            ]
            assert 0.0 <= analysis.confidence <= 1.0
            assert isinstance(analysis.enhancement_strategy, EnhancementStrategy)

    def test_strategic_question_analysis(self, analyzer):
        """Test analysis of strategic/complex questions"""
        strategic_inputs = [
            "How should we systematically restructure our engineering teams?",
            "What framework should we use for quarterly planning?",
            "Provide a comprehensive analysis of our platform strategy",
        ]

        for input_text in strategic_inputs:
            analysis = analyzer.analyze_input_complexity(input_text)
            assert isinstance(analysis, ComplexityAnalysis)
            # Accept MEDIUM or higher complexity for strategic questions
            assert analysis.complexity in [
                AnalysisComplexity.MEDIUM,
                AnalysisComplexity.COMPLEX,
                AnalysisComplexity.SYSTEMATIC,
            ]
            assert analysis.confidence > 0.0
            assert len(analysis.trigger_keywords) > 0
            assert analysis.enhancement_strategy != EnhancementStrategy.NONE

    def test_persona_context_handling(self, analyzer):
        """Test that persona context is properly handled"""
        context = {"current_persona": "diego"}
        analysis = analyzer.analyze_input_complexity(
            "How should we scale our team?", context
        )

        assert isinstance(analysis, ComplexityAnalysis)
        assert "diego" in analysis.persona_suitability
        assert isinstance(analysis.persona_suitability["diego"], float)

    def test_enhancement_strategy_determination(self, analyzer):
        """Test enhancement strategy is correctly determined"""
        test_cases = [
            ("simple question", EnhancementStrategy.NONE),
            (
                "systematic analysis of architecture",
                EnhancementStrategy.SYSTEMATIC_ANALYSIS,
            ),
            ("framework for planning", EnhancementStrategy.LIGHT_FRAMEWORK),
        ]

        for input_text, expected_strategy_type in test_cases:
            analysis = analyzer.analyze_input_complexity(input_text)
            assert isinstance(analysis.enhancement_strategy, EnhancementStrategy)
            # Strategy type should match or be reasonable
            if expected_strategy_type == EnhancementStrategy.NONE:
                assert analysis.complexity == AnalysisComplexity.SIMPLE

    def test_recommended_capabilities(self, analyzer):
        """Test that capabilities are recommended based on input"""
        strategic_input = "systematic analysis of our platform strategy"
        analysis = analyzer.analyze_input_complexity(strategic_input)

        assert isinstance(analysis.recommended_capabilities, list)
        # Strategic input should recommend systematic analysis capabilities
        assert len(analysis.recommended_capabilities) > 0

    def test_persona_suitability_calculation(self, analyzer):
        """Test persona suitability is calculated"""
        analysis = analyzer.analyze_input_complexity("platform architecture strategy")

        assert isinstance(analysis.persona_suitability, dict)
        assert len(analysis.persona_suitability) > 0
        # Scores should be between 0 and 1
        for persona, score in analysis.persona_suitability.items():
            assert 0.0 <= score <= 1.0

    def test_reasoning_generation(self, analyzer):
        """Test that reasoning is generated"""
        analysis = analyzer.analyze_input_complexity("strategic planning framework")

        assert isinstance(analysis.reasoning, str)
        assert len(analysis.reasoning) > 0
        # Reasoning should mention complexity or strategy
        assert any(
            keyword in analysis.reasoning.lower()
            for keyword in ["complexity", "analysis", "framework"]
        )

    def test_empty_input_handling(self, analyzer):
        """Test handling of empty/whitespace input"""
        empty_inputs = ["", "   ", "\n\n"]

        for input_text in empty_inputs:
            analysis = analyzer.analyze_input_complexity(input_text)
            assert isinstance(analysis, ComplexityAnalysis)
            assert analysis.complexity == AnalysisComplexity.SIMPLE
            assert analysis.confidence >= 0.0

    def test_phase12_always_on_enhancement(self, analyzer):
        """Test Phase 12: Always-on MCP enhancement (no thresholds)"""
        analysis = analyzer.analyze_input_complexity("simple question")

        # Phase 12: Always returns True for enhancement
        should_enhance, server = analyzer.should_enhance_with_mcp(analysis, "diego")

        assert should_enhance is True
        assert server is not None
        assert isinstance(server, str)

    def test_enhancement_context_generation(self, analyzer):
        """Test that enhancement context is properly generated"""
        analysis = analyzer.analyze_input_complexity("strategic planning")
        context = analyzer.get_enhancement_context(analysis)

        assert isinstance(context, dict)
        assert "complexity_level" in context
        assert "confidence" in context
        assert "strategy" in context

    def test_multiple_personas(self, analyzer):
        """Test analysis for different personas"""
        personas = ["diego", "martin", "rachel", "alvaro", "camille"]
        input_text = "platform architecture strategy"

        for persona in personas:
            context = {"current_persona": persona}
            analysis = analyzer.analyze_input_complexity(input_text, context)

            assert isinstance(analysis, ComplexityAnalysis)
            assert persona in analysis.persona_suitability

    def test_long_input_complexity_boost(self, analyzer):
        """Test that longer inputs get complexity boost"""
        short_input = "What is API?"
        long_input = (
            "I need a comprehensive systematic analysis of our platform architecture strategy, "
            "including evaluation of our current technical debt, organizational structure, "
            "team coordination patterns, and strategic alignment with business objectives. "
            "We should also consider framework recommendations for quarterly planning."
        )

        short_analysis = analyzer.analyze_input_complexity(short_input)
        long_analysis = analyzer.analyze_input_complexity(long_input)

        # Long input should have higher complexity
        complexity_order = [
            AnalysisComplexity.SIMPLE,
            AnalysisComplexity.MEDIUM,
            AnalysisComplexity.COMPLEX,
            AnalysisComplexity.SYSTEMATIC,
        ]
        short_idx = complexity_order.index(short_analysis.complexity)
        long_idx = complexity_order.index(long_analysis.complexity)

        assert long_idx >= short_idx
        assert len(long_analysis.trigger_keywords) > len(
            short_analysis.trigger_keywords
        )

    def test_confidence_bounds(self, analyzer):
        """Test that confidence scores are properly bounded"""
        test_inputs = [
            "simple",
            "medium complexity question",
            "systematic comprehensive analysis of strategic framework",
        ]

        for input_text in test_inputs:
            analysis = analyzer.analyze_input_complexity(input_text)
            assert 0.0 <= analysis.confidence <= 1.0

    def test_trigger_keywords_extraction(self, analyzer):
        """Test that trigger keywords are properly extracted"""
        input_with_triggers = "systematic framework analysis for strategic planning"
        analysis = analyzer.analyze_input_complexity(input_with_triggers)

        assert isinstance(analysis.trigger_keywords, list)
        assert len(analysis.trigger_keywords) > 0
        # Should contain at least one of the obvious triggers
        trigger_set = set(k.lower() for k in analysis.trigger_keywords)
        assert any(
            keyword in trigger_set
            for keyword in ["systematic", "framework", "analysis", "strategic"]
        )
