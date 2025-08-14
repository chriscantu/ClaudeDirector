"""
Integration tests for Enhanced Persona Manager
Tests the complete MCP integration workflow with persona enhancement.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import yaml

from claudedirector.integrations.enhanced_persona_manager import (
    EnhancedPersonaManager, EnhancedResponse, EnhancementStatus, TransparencyManager
)
from claudedirector.integrations.mcp_use_client import MCPResponse, ConnectionStatus
from claudedirector.integrations.complexity_analyzer import ComplexityAnalysis, ComplexityLevel


class TestTransparencyManager:
    """Test suite for TransparencyManager"""
    
    @pytest.fixture
    def transparency_manager(self):
        """Create TransparencyManager instance"""
        return TransparencyManager()
    
    def test_get_access_message(self, transparency_manager):
        """Test access message generation"""
        message = transparency_manager.get_access_message("diego", "sequential")
        assert isinstance(message, str)
        assert len(message) > 0
        assert "strategic analysis framework" in message.lower()
    
    def test_get_enhanced_message(self, transparency_manager):
        """Test enhanced response message"""
        message = transparency_manager.get_enhanced_message("diego", "sequential", 2.5)
        assert isinstance(message, str)
        assert "enhanced" in message.lower() or "framework" in message.lower()
    
    def test_get_fallback_messages(self, transparency_manager):
        """Test different fallback scenarios"""
        timeout_msg = transparency_manager.get_fallback_message("timeout after 5 seconds")
        assert "timeout" in timeout_msg.lower() or "longer than expected" in timeout_msg.lower()
        
        unavailable_msg = transparency_manager.get_fallback_message("server unavailable")
        assert "unavailable" in unavailable_msg.lower() or "temporarily" in unavailable_msg.lower()
        
        error_msg = transparency_manager.get_fallback_message("connection error")
        assert "error" in error_msg.lower() or "unavailable" in error_msg.lower()


class TestEnhancedPersonaManager:
    """Test suite for EnhancedPersonaManager"""
    
    @pytest.fixture
    def sample_config(self):
        """Sample MCP configuration for testing"""
        return {
            "servers": {
                "sequential": {
                    "command": "npx",
                    "args": ["-y", "@sequential/mcp-server"],
                    "connection_type": "stdio",
                    "capabilities": ["systematic_analysis"],
                    "personas": ["diego"]
                }
            },
            "enhancement_thresholds": {
                "systematic_analysis": 0.7
            }
        }
    
    @pytest.fixture
    def config_file(self, sample_config):
        """Create temporary config file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(sample_config, f)
            return f.name
    
    @pytest.fixture
    def persona_manager(self, config_file):
        """Create EnhancedPersonaManager instance"""
        return EnhancedPersonaManager(config_file)
    
    @pytest.mark.asyncio
    async def test_initialization_success(self, persona_manager):
        """Test successful initialization"""
        # Mock successful MCP connection
        with patch.object(persona_manager.mcp_client, 'is_available', True):
            with patch.object(persona_manager.mcp_client, 'initialize_connections') as mock_init:
                mock_init.return_value = ConnectionStatus(["sequential"], [], 1, 1.0)
                
                result = await persona_manager.initialize()
                assert result is True
                assert persona_manager.is_initialized is True
    
    @pytest.mark.asyncio
    async def test_initialization_graceful_degradation(self, persona_manager):
        """Test initialization with graceful degradation"""
        # Mock MCP unavailable
        with patch.object(persona_manager.mcp_client, 'is_available', False):
            result = await persona_manager.initialize()
            assert result is True
            assert persona_manager.is_initialized is True
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_success(self, persona_manager):
        """Test successful enhanced response generation"""
        await persona_manager.initialize()
        
        # Mock high complexity analysis that should trigger enhancement
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        # Mock successful MCP response
        mock_mcp_response = MCPResponse(
            content="Enhanced strategic analysis: This requires systematic organizational restructuring...",
            source_server="sequential",
            processing_time=2.5,
            success=True
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', True):
                with patch.object(persona_manager.mcp_client, 'is_server_available', return_value=True):
                    with patch.object(persona_manager.mcp_client, 'execute_analysis', return_value=mock_mcp_response):
                        
                        response = await persona_manager.get_enhanced_response(
                            "diego", 
                            "How should we restructure our platform teams?"
                        )
                        
                        assert isinstance(response, EnhancedResponse)
                        assert response.enhancement_status == EnhancementStatus.SUCCESS
                        assert response.persona == "diego"
                        assert response.mcp_server_used == "sequential"
                        assert response.processing_time > 0
                        assert "strategic" in response.content.lower()
                        assert response.transparency_message is not None
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_fallback_low_complexity(self, persona_manager):
        """Test fallback when complexity is too low"""
        await persona_manager.initialize()
        
        # Mock low complexity analysis
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.SIMPLE,
            confidence=0.3,
            triggers=[],
            recommended_enhancement=None,
            persona_specific_score=0.2
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            response = await persona_manager.get_enhanced_response(
                "diego",
                "What is REST?"
            )
            
            assert isinstance(response, EnhancedResponse)
            assert response.enhancement_status == EnhancementStatus.FALLBACK
            assert response.persona == "diego"
            assert response.mcp_server_used is None
            assert "complexity below enhancement threshold" in response.fallback_reason.lower()
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_mcp_unavailable(self, persona_manager):
        """Test fallback when MCP is unavailable"""
        await persona_manager.initialize()
        
        # Mock high complexity but MCP unavailable
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', False):
                
                response = await persona_manager.get_enhanced_response(
                    "diego",
                    "How should we restructure our platform teams?"
                )
                
                assert isinstance(response, EnhancedResponse)
                assert response.enhancement_status == EnhancementStatus.FALLBACK
                assert response.mcp_server_used is None
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_server_unavailable(self, persona_manager):
        """Test fallback when specific server is unavailable"""
        await persona_manager.initialize()
        
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', True):
                with patch.object(persona_manager.mcp_client, 'is_server_available', return_value=False):
                    
                    response = await persona_manager.get_enhanced_response(
                        "diego",
                        "How should we restructure our platform teams?"
                    )
                    
                    assert isinstance(response, EnhancedResponse)
                    assert response.enhancement_status == EnhancementStatus.FALLBACK
                    assert "not available" in response.fallback_reason
                    assert response.transparency_message is not None
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_timeout(self, persona_manager):
        """Test timeout handling"""
        await persona_manager.initialize()
        
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', True):
                with patch.object(persona_manager.mcp_client, 'is_server_available', return_value=True):
                    with patch.object(persona_manager.mcp_client, 'execute_analysis', side_effect=asyncio.TimeoutError):
                        
                        response = await persona_manager.get_enhanced_response(
                            "diego",
                            "How should we restructure our platform teams?"
                        )
                        
                        assert isinstance(response, EnhancedResponse)
                        assert response.enhancement_status == EnhancementStatus.FALLBACK
                        assert "timeout" in response.fallback_reason.lower()
                        assert "timeout" in response.transparency_message.lower() or "longer than expected" in response.transparency_message.lower()
    
    @pytest.mark.asyncio
    async def test_get_enhanced_response_mcp_error(self, persona_manager):
        """Test MCP error handling"""
        await persona_manager.initialize()
        
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        mock_mcp_response = MCPResponse(
            content="",
            source_server="sequential",
            processing_time=1.0,
            success=False,
            error_message="Connection failed"
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', True):
                with patch.object(persona_manager.mcp_client, 'is_server_available', return_value=True):
                    with patch.object(persona_manager.mcp_client, 'execute_analysis', return_value=mock_mcp_response):
                        
                        response = await persona_manager.get_enhanced_response(
                            "diego",
                            "How should we restructure our platform teams?"
                        )
                        
                        assert isinstance(response, EnhancedResponse)
                        assert response.enhancement_status == EnhancementStatus.FALLBACK
                        assert "Connection failed" in response.fallback_reason
    
    def test_should_enhance_logic(self, persona_manager):
        """Test enhancement decision logic"""
        # High complexity, correct enhancement type
        high_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        with patch.object(persona_manager.mcp_client, 'is_available', True):
            assert persona_manager._should_enhance("diego", high_complexity) is True
        
        # Low complexity
        low_complexity = ComplexityAnalysis(
            level=ComplexityLevel.SIMPLE,
            confidence=0.3,
            triggers=[],
            recommended_enhancement=None,
            persona_specific_score=0.2
        )
        
        assert persona_manager._should_enhance("diego", low_complexity) is False
        
        # MCP unavailable
        with patch.object(persona_manager.mcp_client, 'is_available', False):
            assert persona_manager._should_enhance("diego", high_complexity) is False
    
    def test_prepare_analysis_query(self, persona_manager):
        """Test analysis query preparation"""
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.8,
            triggers=["strategic_question", "organizational"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.7
        )
        
        query = persona_manager._prepare_analysis_query(
            "diego", 
            "How should we restructure our teams?",
            mock_complexity,
            None
        )
        
        assert isinstance(query, str)
        assert "organizational strategy challenge" in query.lower()
        assert "How should we restructure our teams?" in query
        assert "strategic_question" in query
    
    @pytest.mark.asyncio
    async def test_blend_response(self, persona_manager):
        """Test response blending with persona characteristics"""
        mcp_content = "Apply the Conway's Law principle and create cross-functional teams aligned with desired system architecture."
        
        blended = await persona_manager._blend_response(
            "diego",
            "How should we restructure our teams?",
            mcp_content,
            None
        )
        
        assert isinstance(blended, str)
        assert len(blended) > len(mcp_content)  # Should add persona context
        assert mcp_content in blended
        assert "organizational frameworks" in blended.lower() or "proven" in blended.lower()
    
    @pytest.mark.asyncio
    async def test_blend_response_empty_mcp_content(self, persona_manager):
        """Test response blending with empty MCP content"""
        blended = await persona_manager._blend_response(
            "diego",
            "How should we restructure our teams?",
            "",
            None
        )
        
        assert isinstance(blended, str)
        assert len(blended) > 0
        assert "systematically" in blended.lower() or "challenge" in blended.lower()
    
    @pytest.mark.asyncio
    async def test_get_standard_response(self, persona_manager):
        """Test standard response generation"""
        response = await persona_manager._get_standard_response(
            "diego",
            "How should we approach this challenge?",
            None
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "systematically" in response.lower()
        assert "How should we approach this challenge?" in response
    
    def test_get_server_status(self, persona_manager):
        """Test server status reporting"""
        # Test when MCP unavailable
        with patch.object(persona_manager.mcp_client, 'is_available', False):
            status = persona_manager.get_server_status()
            assert status["status"] == "unavailable"
            assert "mcp-use library not available" in status["reason"]
        
        # Test when servers available
        with patch.object(persona_manager.mcp_client, 'is_available', True):
            with patch.object(persona_manager.mcp_client, 'get_available_servers', return_value=["sequential", "context7"]):
                status = persona_manager.get_server_status()
                assert status["status"] == "available"
                assert "sequential" in status["available_servers"]
                assert "context7" in status["available_servers"]
                assert status["total_personas"] == 5
                assert len(status["enhanced_personas"]) > 0
    
    @pytest.mark.asyncio
    async def test_cleanup(self, persona_manager):
        """Test cleanup functionality"""
        # Mock cleanup
        with patch.object(persona_manager.mcp_client, 'cleanup_connections') as mock_cleanup:
            await persona_manager.cleanup()
            mock_cleanup.assert_called_once()


class TestMultiPersonaIntegration:
    """Integration tests across multiple personas"""
    
    @pytest.fixture
    def persona_manager(self):
        """Create persona manager for multi-persona testing"""
        return EnhancedPersonaManager()
    
    @pytest.mark.asyncio
    async def test_diego_systematic_analysis(self, persona_manager):
        """Test Diego-specific systematic analysis enhancement"""
        await persona_manager.initialize()
        
        # Mock high complexity organizational question
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.STRATEGIC,
            confidence=0.85,
            triggers=["organizational", "strategic_question"],
            recommended_enhancement="systematic_analysis",
            persona_specific_score=0.8
        )
        
        mock_mcp_response = MCPResponse(
            content="Systematic organizational analysis: 1) Assess current structure, 2) Define target state, 3) Plan transition phases...",
            source_server="sequential",
            processing_time=3.2,
            success=True
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            with patch.object(persona_manager.mcp_client, 'is_available', True):
                with patch.object(persona_manager.mcp_client, 'is_server_available', return_value=True):
                    with patch.object(persona_manager.mcp_client, 'execute_analysis', return_value=mock_mcp_response):
                        
                        response = await persona_manager.get_enhanced_response(
                            "diego",
                            "How should we restructure our platform teams to improve delivery velocity while maintaining quality?"
                        )
                        
                        assert response.enhancement_status == EnhancementStatus.SUCCESS
                        assert response.persona == "diego"
                        assert response.mcp_server_used == "sequential"
                        assert "organizational frameworks" in response.content.lower()
                        assert "systematic" in response.content.lower()
    
    @pytest.mark.asyncio
    async def test_performance_requirements(self, persona_manager):
        """Test performance requirements across personas"""
        await persona_manager.initialize()
        
        personas_to_test = ["diego", "martin", "rachel", "alvaro", "camille"]
        
        # Mock moderate complexity that should process quickly
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.MODERATE,
            confidence=0.5,
            triggers=[],
            recommended_enhancement=None,
            persona_specific_score=0.4
        )
        
        for persona in personas_to_test:
            with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
                start_time = asyncio.get_event_loop().time()
                
                response = await persona_manager.get_enhanced_response(
                    persona,
                    "Quick question about our approach"
                )
                
                processing_time = asyncio.get_event_loop().time() - start_time
                
                assert isinstance(response, EnhancedResponse)
                assert processing_time < 2.0  # Should be fast for standard responses
                assert response.processing_time >= 0
    
    @pytest.mark.asyncio  
    async def test_concurrent_persona_requests(self, persona_manager):
        """Test concurrent requests across multiple personas"""
        await persona_manager.initialize()
        
        # Mock setup for concurrent testing
        mock_complexity = ComplexityAnalysis(
            level=ComplexityLevel.MODERATE,
            confidence=0.5,
            triggers=[],
            recommended_enhancement=None,
            persona_specific_score=0.4
        )
        
        with patch.object(persona_manager.complexity_analyzer, 'analyze_complexity', return_value=mock_complexity):
            # Create concurrent requests
            tasks = []
            personas = ["diego", "martin", "rachel"]
            
            for i, persona in enumerate(personas):
                task = persona_manager.get_enhanced_response(
                    persona,
                    f"Question {i+1} for {persona}"
                )
                tasks.append(task)
            
            # Execute concurrently
            responses = await asyncio.gather(*tasks)
            
            # Validate all responses
            assert len(responses) == len(personas)
            for i, response in enumerate(responses):
                assert isinstance(response, EnhancedResponse)
                assert response.persona == personas[i]
                assert f"Question {i+1}" in response.content
