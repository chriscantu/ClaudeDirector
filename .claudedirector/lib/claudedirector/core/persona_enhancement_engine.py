"""
Persona Enhancement Engine for MCP Integration
Coordinates MCP servers with persona personalities to provide enhanced capabilities
while preserving authentic persona characteristics.

Author: Martin (Principal Platform Architect)
"""

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
import structlog

from .mcp_client import MCPClient, MCPRequest, MCPResponse, MCPServerConfig
from .complexity_analyzer import (
    AnalysisComplexityDetector, 
    ComplexityAnalysis, 
    EnhancementStrategy,
    AnalysisComplexity
)

# Configure logging
logger = structlog.get_logger(__name__)


@dataclass
class EnhancementContext:
    """Context for persona enhancement"""
    persona_name: str
    user_input: str
    base_response: str
    complexity_analysis: ComplexityAnalysis
    enhancement_server: Optional[str]
    conversation_context: Optional[Dict[str, Any]] = None


@dataclass
class EnhancementResult:
    """Result of persona enhancement"""
    enhanced_response: str
    enhancement_applied: bool
    server_used: Optional[str]
    analysis_data: Optional[Dict[str, Any]]
    processing_time_ms: int
    fallback_reason: Optional[str] = None


class PersonaEnhancementEngine:
    """
    Coordinates MCP servers with persona personalities.
    
    Provides systematic analysis while preserving persona authenticity.
    Handles server routing, response integration, and graceful degradation.
    """
    
    def __init__(
        self, 
        mcp_client: MCPClient,
        complexity_detector: AnalysisComplexityDetector,
        config: Optional[Dict] = None
    ):
        self.mcp_client = mcp_client
        self.complexity_detector = complexity_detector
        self.config = config or {}
        
        # Persona personality filters - preserve authentic voice
        self.persona_filters = {
            "diego": {
                "voice_characteristics": [
                    "warm and engaging", "collaborative", "multinational perspective",
                    "emotionally intelligent", "pragmatic", "solution-focused"
                ],
                "communication_patterns": {
                    "opening_style": ["Great to connect!", "I'm excited about this challenge", "Let's dive into this"],
                    "transition_phrases": ["Here's what I'm thinking", "From my experience", "Let me share what's worked"],
                    "analytical_markers": ["Looking at this systematically", "Breaking this down", "Here's the framework I'd use"],
                    "personal_touches": ["😊", "What's your gut feeling?", "Let's get real about this"],
                    "closure_style": ["What resonates most?", "How does this land?", "Let's build on this together"]
                },
                "systematic_integration": {
                    "prefix_patterns": [
                        "Let me work through this systematically...",
                        "I've been thinking about frameworks for this...",
                        "Here's how I'd approach this step-by-step..."
                    ],
                    "framework_intro": [
                        "Using proven strategic planning approaches...",
                        "Drawing from organizational analysis frameworks...",
                        "Following systematic methodology..."
                    ],
                    "analysis_wrapping": [
                        "What this analysis tells us is...",
                        "The systematic approach suggests...",
                        "Based on this framework..."
                    ]
                }
            },
            "martin": {
                "voice_characteristics": [
                    "thoughtful", "measured", "precise", "pattern-focused", 
                    "evolutionary thinking", "principled"
                ],
                "communication_patterns": {
                    "opening_style": ["Let me think about this", "There's an interesting pattern here", "This reminds me of"],
                    "analytical_markers": ["The trade-offs are", "Evolutionarily", "From an architectural perspective"],
                    "framework_integration": ["This follows the pattern of", "Using established principles", "The framework suggests"]
                }
            },
            "rachel": {
                "voice_characteristics": [
                    "collaborative", "user-centered", "systems thinking",
                    "inclusive", "practical", "empathetic"
                ],
                "communication_patterns": {
                    "opening_style": ["Let's think about the user experience", "I love where this is going", "How does this feel for teams?"],
                    "framework_integration": ["Design systems research shows", "User-centered frameworks suggest", "Cross-team patterns indicate"]
                }
            }
        }
        
        # Enhancement quality thresholds
        self.quality_thresholds = {
            "minimum_enhancement_value": 0.3,  # Don't enhance unless adding significant value
            "personality_preservation": 0.8,   # Must maintain persona authenticity
            "response_coherence": 0.7,         # Enhanced response must be coherent
            "processing_timeout": 10.0         # Maximum time for enhancement (seconds)
        }
    
    async def enhance_response(
        self,
        persona_name: str,
        user_input: str,
        base_response: str,
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> EnhancementResult:
        """
        Enhance persona response with MCP server capabilities.
        
        Args:
            persona_name: Name of the persona providing response
            user_input: Original user input/question
            base_response: Standard persona response
            conversation_context: Optional conversation history and context
            
        Returns:
            EnhancementResult with enhanced response or fallback reasoning
        """
        start_time = time.time()
        
        try:
            # Analyze input complexity
            complexity_analysis = self.complexity_detector.analyze_input_complexity(
                user_input, 
                context={"current_persona": persona_name, **conversation_context or {}}
            )
            
            # Determine if enhancement should be applied
            should_enhance, server_name = self.complexity_detector.should_enhance_with_mcp(
                complexity_analysis,
                persona_name,
                self.config.get("enhancement_thresholds")
            )
            
            if not should_enhance:
                processing_time = int((time.time() - start_time) * 1000)
                return EnhancementResult(
                    enhanced_response=base_response,
                    enhancement_applied=False,
                    server_used=None,
                    analysis_data=None,
                    processing_time_ms=processing_time,
                    fallback_reason="Below enhancement threshold or persona not suitable"
                )
            
            # Create enhancement context
            context = EnhancementContext(
                persona_name=persona_name,
                user_input=user_input,
                base_response=base_response,
                complexity_analysis=complexity_analysis,
                enhancement_server=server_name,
                conversation_context=conversation_context
            )
            
            # Attempt MCP enhancement
            enhanced_response = await self._apply_mcp_enhancement(context)
            
            if enhanced_response:
                processing_time = int((time.time() - start_time) * 1000)
                
                logger.info(
                    "persona_enhancement_success",
                    persona=persona_name,
                    server=server_name,
                    complexity=complexity_analysis.complexity.value,
                    strategy=complexity_analysis.enhancement_strategy.value,
                    processing_time_ms=processing_time
                )
                
                return EnhancementResult(
                    enhanced_response=enhanced_response,
                    enhancement_applied=True,
                    server_used=server_name,
                    analysis_data=self._extract_analysis_metadata(complexity_analysis),
                    processing_time_ms=processing_time
                )
            else:
                # Fallback to base response
                processing_time = int((time.time() - start_time) * 1000)
                return EnhancementResult(
                    enhanced_response=base_response,
                    enhancement_applied=False,
                    server_used=None,
                    analysis_data=None,
                    processing_time_ms=processing_time,
                    fallback_reason="MCP server enhancement failed"
                )
                
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            logger.error(
                "persona_enhancement_error",
                persona=persona_name,
                error=str(e),
                processing_time_ms=processing_time
            )
            
            return EnhancementResult(
                enhanced_response=base_response,
                enhancement_applied=False,
                server_used=None,
                analysis_data=None,
                processing_time_ms=processing_time,
                fallback_reason=f"Enhancement error: {str(e)}"
            )
    
    async def _apply_mcp_enhancement(self, context: EnhancementContext) -> Optional[str]:
        """Apply MCP server enhancement to persona response"""
        
        # Create MCP request based on enhancement strategy
        mcp_request = self._create_mcp_request(context)
        if not mcp_request:
            return None
        
        # Send request to MCP server
        mcp_response = await self.mcp_client.send_request(
            context.enhancement_server,
            mcp_request
        )
        
        if not mcp_response or not mcp_response.success:
            logger.warning(
                "mcp_enhancement_failed",
                persona=context.persona_name,
                server=context.enhancement_server,
                error=mcp_response.error if mcp_response else "No response"
            )
            return None
        
        # Integrate MCP response with persona personality
        enhanced_response = self._integrate_with_persona(context, mcp_response)
        
        return enhanced_response
    
    def _create_mcp_request(self, context: EnhancementContext) -> Optional[MCPRequest]:
        """Create appropriate MCP request based on enhancement context"""
        
        strategy = context.complexity_analysis.enhancement_strategy
        
        if strategy == EnhancementStrategy.SYSTEMATIC_ANALYSIS:
            return self._create_systematic_analysis_request(context)
        elif strategy == EnhancementStrategy.LIGHT_FRAMEWORK:
            return self._create_framework_request(context)
        elif strategy == EnhancementStrategy.VISUAL_ENHANCEMENT:
            return self._create_visual_request(context)
        else:
            return None
    
    def _create_systematic_analysis_request(self, context: EnhancementContext) -> MCPRequest:
        """Create request for systematic analysis"""
        
        analysis_context = {
            "user_question": context.user_input,
            "complexity_level": context.complexity_analysis.complexity.value,
            "domains": context.complexity_analysis.recommended_capabilities,
            "persona_context": {
                "name": context.persona_name,
                "specialties": self._get_persona_specialties(context.persona_name),
                "communication_style": "collaborative and warm"
            },
            "enhancement_goal": "systematic_strategic_analysis",
            "output_format": "structured_insights_with_recommendations"
        }
        
        return MCPRequest(
            method="analyze_systematically",
            params={
                "analysis_type": "strategic_organizational",
                "context": analysis_context,
                "depth": "comprehensive",
                "include_frameworks": True,
                "include_recommendations": True,
                "include_implementation_steps": True
            }
        )
    
    def _create_framework_request(self, context: EnhancementContext) -> MCPRequest:
        """Create request for framework lookup"""
        
        framework_context = {
            "user_question": context.user_input,
            "domain": self._determine_primary_domain(context.complexity_analysis),
            "persona_expertise": context.persona_name,
            "application_context": "engineering_leadership"
        }
        
        return MCPRequest(
            method="lookup_framework",
            params={
                "framework_type": "leadership_methodology",
                "domain": framework_context["domain"],
                "context": framework_context,
                "depth": "practical_application",
                "include_adaptation_guidance": True
            }
        )
    
    def _create_visual_request(self, context: EnhancementContext) -> MCPRequest:
        """Create request for visual enhancement"""
        
        visual_context = {
            "content": context.user_input,
            "persona_style": context.persona_name,
            "audience": "engineering_leaders",
            "format_preference": "professional_diagram"
        }
        
        return MCPRequest(
            method="generate_visual",
            params={
                "visual_type": "strategic_diagram",
                "context": visual_context,
                "style": "executive_presentation",
                "include_annotations": True
            }
        )
    
    def _integrate_with_persona(
        self, 
        context: EnhancementContext, 
        mcp_response: MCPResponse
    ) -> str:
        """Integrate MCP server response with persona personality"""
        
        # Extract systematic insights from MCP response
        systematic_insights = self._extract_insights(mcp_response)
        if not systematic_insights:
            return context.base_response
        
        # Get persona voice characteristics
        persona_filter = self.persona_filters.get(context.persona_name, {})
        
        # Apply persona-specific integration
        if context.persona_name == "diego":
            return self._integrate_diego_response(context, systematic_insights, persona_filter)
        elif context.persona_name == "martin":
            return self._integrate_martin_response(context, systematic_insights, persona_filter)
        elif context.persona_name == "rachel":
            return self._integrate_rachel_response(context, systematic_insights, persona_filter)
        else:
            # Generic integration for other personas
            return self._integrate_generic_response(context, systematic_insights, persona_filter)
    
    def _integrate_diego_response(
        self, 
        context: EnhancementContext, 
        insights: Dict[str, Any],
        persona_filter: Dict[str, Any]
    ) -> str:
        """Integrate systematic analysis with Diego's warm, collaborative personality"""
        
        # Diego's communication patterns
        patterns = persona_filter.get("communication_patterns", {})
        systematic = persona_filter.get("systematic_integration", {})
        
        # Build enhanced response preserving Diego's voice
        response_parts = []
        
        # Diego's warm opening
        opening = self._select_random(patterns.get("opening_style", ["Great question!"]))
        response_parts.append(f"{opening} {self._add_diego_energy()}")
        
        # Introduce systematic approach naturally
        systematic_intro = self._select_random(systematic.get("prefix_patterns", [
            "Let me work through this systematically..."
        ]))
        response_parts.append(systematic_intro)
        
        # Present systematic insights with Diego's collaborative style
        if insights.get("framework"):
            framework_intro = self._select_random(systematic.get("framework_intro", [
                "Using proven strategic approaches..."
            ]))
            response_parts.append(f"{framework_intro}")
            
            # Add framework content with Diego's interpretation
            framework_content = self._format_framework_for_diego(insights["framework"])
            response_parts.append(framework_content)
        
        # Add systematic analysis with Diego's warmth
        if insights.get("analysis"):
            analysis_intro = self._select_random(systematic.get("analysis_wrapping", [
                "What this analysis tells us is..."
            ]))
            response_parts.append(f"{analysis_intro}")
            
            # Format analysis with Diego's collaborative perspective
            analysis_content = self._format_analysis_for_diego(insights["analysis"])
            response_parts.append(analysis_content)
        
        # Add implementation recommendations with Diego's pragmatic style
        if insights.get("recommendations"):
            response_parts.append("\n**Here's how I'd move forward:**")
            recommendations = self._format_recommendations_for_diego(insights["recommendations"])
            response_parts.append(recommendations)
        
        # Diego's engaging closure
        closure = self._select_random(patterns.get("closure_style", ["What resonates most?"]))
        response_parts.append(f"\n{closure} {self._add_diego_personal_touch()}")
        
        return "\n\n".join(response_parts)
    
    def _integrate_martin_response(
        self, 
        context: EnhancementContext, 
        insights: Dict[str, Any],
        persona_filter: Dict[str, Any]
    ) -> str:
        """Integrate framework access with Martin's thoughtful, architectural perspective"""
        
        patterns = persona_filter.get("communication_patterns", {})
        
        response_parts = []
        
        # Martin's thoughtful opening
        opening = self._select_random(patterns.get("opening_style", ["Let me think about this..."]))
        response_parts.append(opening)
        
        # Present frameworks with Martin's architectural lens
        if insights.get("patterns"):
            response_parts.append("This follows established architectural patterns...")
            pattern_content = self._format_patterns_for_martin(insights["patterns"])
            response_parts.append(pattern_content)
        
        # Martin's trade-off analysis
        if insights.get("tradeoffs"):
            response_parts.append("The key trade-offs to consider:")
            tradeoffs_content = self._format_tradeoffs_for_martin(insights["tradeoffs"])
            response_parts.append(tradeoffs_content)
        
        return "\n\n".join(response_parts)
    
    def _integrate_rachel_response(
        self, 
        context: EnhancementContext, 
        insights: Dict[str, Any],
        persona_filter: Dict[str, Any]
    ) -> str:
        """Integrate design frameworks with Rachel's collaborative, user-centered approach"""
        
        patterns = persona_filter.get("communication_patterns", {})
        
        response_parts = []
        
        # Rachel's collaborative opening
        opening = self._select_random(patterns.get("opening_style", ["Let's think about this together..."]))
        response_parts.append(opening)
        
        # Present design frameworks with user impact focus
        if insights.get("user_impact"):
            response_parts.append("From a user experience perspective...")
            user_impact_content = self._format_user_impact_for_rachel(insights["user_impact"])
            response_parts.append(user_impact_content)
        
        return "\n\n".join(response_parts)
    
    def _integrate_generic_response(
        self, 
        context: EnhancementContext, 
        insights: Dict[str, Any],
        persona_filter: Dict[str, Any]
    ) -> str:
        """Generic integration for personas without specific filters"""
        
        response_parts = [context.base_response]
        
        if insights.get("additional_insights"):
            response_parts.append("\n**Additional systematic analysis:**")
            response_parts.append(insights["additional_insights"])
        
        return "\n\n".join(response_parts)
    
    # Helper methods for Diego-specific formatting
    
    def _add_diego_energy(self) -> str:
        """Add Diego's characteristic energy markers"""
        return self._select_random(["😊", "Let's dive in!", "I'm excited to explore this with you."])
    
    def _add_diego_personal_touch(self) -> str:
        """Add Diego's personal connection style"""
        return self._select_random([
            "I'd love to hear your thoughts on this approach.",
            "What part of this resonates most with your situation?",
            "How does this framework feel for your team context?"
        ])
    
    def _format_framework_for_diego(self, framework: Dict[str, Any]) -> str:
        """Format framework content with Diego's collaborative interpretation"""
        if not framework:
            return ""
        
        parts = []
        if framework.get("name"):
            parts.append(f"I'm drawing from **{framework['name']}** here - it's been really effective for similar challenges.")
        
        if framework.get("steps"):
            parts.append("Here's how we can break this down:")
            for i, step in enumerate(framework["steps"], 1):
                parts.append(f"{i}. {step} (This helps us build momentum while staying systematic)")
        
        return "\n".join(parts)
    
    def _format_analysis_for_diego(self, analysis: Dict[str, Any]) -> str:
        """Format systematic analysis with Diego's warm, practical style"""
        if not analysis:
            return ""
        
        parts = []
        if analysis.get("key_insights"):
            parts.append("**Key insights that stand out:**")
            for insight in analysis["key_insights"]:
                parts.append(f"• {insight}")
        
        if analysis.get("critical_factors"):
            parts.append("\n**Critical factors we need to consider:**")
            for factor in analysis["critical_factors"]:
                parts.append(f"• {factor}")
        
        return "\n".join(parts)
    
    def _format_recommendations_for_diego(self, recommendations: List[str]) -> str:
        """Format recommendations with Diego's action-oriented, supportive style"""
        if not recommendations:
            return ""
        
        parts = []
        for i, rec in enumerate(recommendations, 1):
            parts.append(f"{i}. {rec}")
            if i == 1:
                parts.append("   (I'd start here - builds confidence and shows early value)")
            elif i == len(recommendations):
                parts.append("   (This is where the real transformation happens)")
        
        return "\n".join(parts)
    
    # Utility methods
    
    def _extract_insights(self, mcp_response: MCPResponse) -> Optional[Dict[str, Any]]:
        """Extract structured insights from MCP server response"""
        if not mcp_response or not mcp_response.result:
            return None
        
        try:
            return mcp_response.result.get("insights", mcp_response.result)
        except Exception as e:
            logger.error("failed_to_extract_insights", error=str(e))
            return None
    
    def _select_random(self, options: List[str]) -> str:
        """Select random option from list (deterministic for testing)"""
        if not options:
            return ""
        # Use hash for deterministic "randomness" in testing
        return options[hash(str(options)) % len(options)]
    
    def _get_persona_specialties(self, persona_name: str) -> List[str]:
        """Get specialties for persona from complexity detector"""
        persona_info = self.complexity_detector.persona_capabilities.get(persona_name, {})
        return persona_info.get("specialties", [])
    
    def _determine_primary_domain(self, analysis: ComplexityAnalysis) -> str:
        """Determine primary domain from complexity analysis"""
        if not analysis.recommended_capabilities:
            return "general"
        
        # Map capabilities to domains
        capability_domain_map = {
            "systematic_analysis": "strategic",
            "framework_application": "process",
            "strategic_planning": "strategic",
            "organizational_analysis": "organizational",
            "pattern_access": "technical",
            "architectural_patterns": "technical",
            "design_frameworks": "design"
        }
        
        domains = [capability_domain_map.get(cap, "general") for cap in analysis.recommended_capabilities]
        # Return most common domain
        if domains:
            return max(set(domains), key=domains.count)
        return "general"
    
    def _extract_analysis_metadata(self, analysis: ComplexityAnalysis) -> Dict[str, Any]:
        """Extract metadata from complexity analysis for tracking"""
        return {
            "complexity": analysis.complexity.value,
            "confidence": analysis.confidence,
            "strategy": analysis.enhancement_strategy.value,
            "capabilities": analysis.recommended_capabilities,
            "trigger_keywords": analysis.trigger_keywords,
            "reasoning": analysis.reasoning
        }
    
    def _format_patterns_for_martin(self, patterns: List[Dict[str, Any]]) -> str:
        """Format architectural patterns for Martin's style"""
        if not patterns:
            return ""
        
        parts = []
        for pattern in patterns:
            if pattern.get("name"):
                parts.append(f"**{pattern['name']}**: {pattern.get('description', '')}")
                if pattern.get("trade_offs"):
                    parts.append(f"  *Trade-offs*: {pattern['trade_offs']}")
        
        return "\n".join(parts)
    
    def _format_tradeoffs_for_martin(self, tradeoffs: List[Dict[str, Any]]) -> str:
        """Format trade-offs analysis for Martin's architectural perspective"""
        if not tradeoffs:
            return ""
        
        parts = []
        for tradeoff in tradeoffs:
            if tradeoff.get("factor"):
                parts.append(f"• **{tradeoff['factor']}**: {tradeoff.get('analysis', '')}")
        
        return "\n".join(parts)
    
    def _format_user_impact_for_rachel(self, user_impact: Dict[str, Any]) -> str:
        """Format user impact analysis for Rachel's UX focus"""
        if not user_impact:
            return ""
        
        parts = []
        if user_impact.get("experience_improvements"):
            parts.append("**How this improves the user experience:**")
            for improvement in user_impact["experience_improvements"]:
                parts.append(f"• {improvement}")
        
        if user_impact.get("team_impact"):
            parts.append("\n**Impact on teams:**")
            for impact in user_impact["team_impact"]:
                parts.append(f"• {impact}")
        
        return "\n".join(parts)
