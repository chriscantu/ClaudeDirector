"""
Refactored Framework Engine - SOLID Compliant Architecture

This is the new SOLID-compliant version of EmbeddedFrameworkEngine that orchestrates
specialized services instead of implementing all logic in a monolithic class.

SOLID Principles Applied:
- Single Responsibility: Engine only orchestrates, services handle specific tasks
- Open/Closed: New frameworks/strategies can be added without modifying core engine
- Liskov Substitution: All services implement interfaces and are substitutable
- Interface Segregation: Clients depend only on interfaces they need
- Dependency Inversion: Engine depends on abstractions, not concrete implementations

Author: Martin (SOLID Refactoring Implementation)
"""

import time
from typing import Dict, List, Optional, Any
import structlog
from .config import ClaudeDirectorConfig, get_config

from .interfaces.framework_provider_interface import (
    IFrameworkProvider,
    IFrameworkSelector,
    IFrameworkAnalyzer,
    IInsightGenerator,
    IConfidenceCalculator,
    IPersonaIntegrator,
    FrameworkContext,
    FrameworkAnalysisResult,
    SystematicAnalysisResult,
    AnalysisComplexity,
    FrameworkDomain,
)

from .services.framework_selection_service import FrameworkSelectionService
from .services.framework_analysis_service import FrameworkAnalysisService
from .services.insight_generation_service import InsightGenerationService
from .services.confidence_calculation_service import ConfidenceCalculationService

# Import shared types to avoid circular imports
from .framework_types import FrameworkAnalysis

logger = structlog.get_logger(__name__)


class DefaultFrameworkProvider:
    """
    Default implementation of IFrameworkProvider using the original framework definitions.

    This provides backward compatibility while allowing for future framework providers
    that could load from databases, APIs, or other sources.
    """

    def __init__(self):
        """Initialize with static framework definitions to avoid circular dependencies"""
        # Import static framework definitions to avoid circular dependency
        from .framework_definitions import get_strategic_frameworks
        from .interfaces.framework_provider_interface import (
            FrameworkDefinition,
            FrameworkDomain,
        )

        # Convert static definitions to FrameworkDefinition objects
        static_definitions = get_strategic_frameworks()
        self.framework_definitions = {}

        for name, definition in static_definitions.items():
            # Create FrameworkDefinition object
            framework_def = FrameworkDefinition(
                name=name,
                description=definition["description"],
                domains=[FrameworkDomain.STRATEGIC],  # Default to strategic for all
                keywords=definition["keywords"],
                analysis_components=definition["analysis_components"],
                confidence_threshold=definition["confidence_threshold"],
            )
            self.framework_definitions[name] = framework_def

    def get_framework_definition(self, framework_name: str):
        """Get definition for a specific framework"""
        return self.framework_definitions.get(framework_name)

    def get_available_frameworks(self) -> List[str]:
        """Get list of all available framework names"""
        return list(self.framework_definitions.keys())

    def get_frameworks_for_domain(self, domain: FrameworkDomain) -> List[str]:
        """Get frameworks applicable to a specific domain"""
        matching_frameworks = []
        for name, definition in self.framework_definitions.items():
            if domain in definition.domains:
                matching_frameworks.append(name)
        return matching_frameworks

    def get_frameworks_by_keywords(self, keywords: List[str]) -> List[str]:
        """Get frameworks matching specific keywords"""
        matching_frameworks = []
        keywords_lower = [k.lower() for k in keywords]

        for name, definition in self.framework_definitions.items():
            framework_keywords = [k.lower() for k in definition.keywords]
            if any(keyword in framework_keywords for keyword in keywords_lower):
                matching_frameworks.append(name)

        return matching_frameworks

    def _convert_framework_definitions(
        self, original_frameworks: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert original framework definitions to new format"""
        # This is a simplified conversion - in a full implementation,
        # we would properly convert to FrameworkDefinition objects
        converted = {}

        for framework_key, framework_data in original_frameworks.items():
            # Extract basic information
            name = framework_data.get("name", framework_key)
            domains = [FrameworkDomain(d) for d in framework_data.get("domains", [])]

            # Extract keywords from various sources
            keywords = []
            if "keywords" in framework_data:
                keywords.extend(framework_data["keywords"])

            # Add keywords from analysis components
            analysis_components = framework_data.get("analysis_components", {})
            for component_name, component_data in analysis_components.items():
                keywords.append(component_name.replace("_", " "))
                if "questions" in component_data:
                    for question in component_data["questions"]:
                        # Extract key terms from questions
                        question_words = question.lower().split()
                        keywords.extend([w for w in question_words if len(w) > 4])

            # Create simplified framework definition
            converted[framework_key] = type(
                "FrameworkDefinition",
                (),
                {
                    "name": name,
                    "description": f"Strategic framework: {name}",
                    "domains": domains,
                    "keywords": list(set(keywords))[:20],  # Limit to 20 keywords
                    "analysis_components": analysis_components,
                    "confidence_threshold": self.config.get_threshold(
                        "stakeholder_profiling_threshold"
                    ),
                },
            )()

        return converted


class RefactoredFrameworkEngine:
    """
    SOLID-compliant framework engine that orchestrates specialized services.

    This engine follows all SOLID principles:
    - SRP: Only responsible for orchestration and coordination
    - OCP: Open for extension through service injection
    - LSP: All services are substitutable through interfaces
    - ISP: Depends only on needed interfaces
    - DIP: Depends on abstractions, not concrete implementations
    """

    def __init__(
        self,
        framework_provider: Optional[IFrameworkProvider] = None,
        framework_selector: Optional[IFrameworkSelector] = None,
        framework_analyzer: Optional[IFrameworkAnalyzer] = None,
        insight_generator: Optional[IInsightGenerator] = None,
        confidence_calculator: Optional[IConfidenceCalculator] = None,
        persona_integrator: Optional[IPersonaIntegrator] = None,
        config: Optional[ClaudeDirectorConfig] = None,
    ):
        """
        Initialize with dependency injection of all services.

        This constructor demonstrates Dependency Inversion Principle (DIP)
        by accepting abstractions rather than concrete implementations.
        """
        self.config = config or get_config()

        # Initialize services with dependency injection
        self.framework_provider = framework_provider or DefaultFrameworkProvider()
        self.insight_generator = insight_generator or InsightGenerationService()
        self.confidence_calculator = (
            confidence_calculator or ConfidenceCalculationService()
        )

        # Services that depend on the framework provider
        self.framework_selector = framework_selector or FrameworkSelectionService(
            self.framework_provider
        )
        self.framework_analyzer = framework_analyzer or FrameworkAnalysisService(
            self.framework_provider, self.insight_generator
        )

        # Persona integrator (would be injected in full implementation)
        self.persona_integrator = persona_integrator  # Optional for now

        # Configuration
        self.enable_confidence_calculation = self.config.get(
            "enable_confidence_calculation", True
        )
        self.enable_persona_integration = self.config.get(
            "enable_persona_integration", True
        )
        self.max_analysis_time_ms = self.config.get("max_analysis_time_ms", 5000)

        logger.info(
            "Refactored Framework Engine initialized",
            services_injected={
                "framework_provider": type(self.framework_provider).__name__,
                "framework_selector": type(self.framework_selector).__name__,
                "framework_analyzer": type(self.framework_analyzer).__name__,
                "insight_generator": type(self.insight_generator).__name__,
                "confidence_calculator": type(self.confidence_calculator).__name__,
                "persona_integrator": (
                    type(self.persona_integrator).__name__
                    if self.persona_integrator
                    else None
                ),
            },
        )

    def analyze_systematically(
        self,
        user_input: str,
        persona_context: Optional[Dict] = None,
        session_id: str = "default",
        domain_focus: Optional[List[str]] = None,
        **kwargs,
    ) -> SystematicAnalysisResult:
        """
        Perform systematic analysis using the orchestrated services.

        This method demonstrates Single Responsibility Principle (SRP) by
        focusing only on orchestration rather than implementing analysis logic.

        Args:
            user_input: User input to analyze
            persona_context: Optional persona context for integration
            session_id: Session identifier for context tracking

        Returns:
            Complete systematic analysis result
        """
        start_time = time.time()

        try:
            logger.info(
                "Starting systematic analysis",
                input_length=len(user_input),
                session_id=session_id,
                persona_context_provided=persona_context is not None,
            )

            # Step 1: Create analysis context
            context = self._create_analysis_context(
                user_input, persona_context, session_id
            )

            # Step 2: Select appropriate framework
            selected_framework = self.framework_selector.select_framework(context)

            if not selected_framework:
                logger.warning("No suitable framework found for analysis")
                return self._create_fallback_response(user_input, start_time)

            # Step 3: Calculate framework relevance for confidence calculation
            framework_relevance = self.framework_selector.calculate_framework_relevance(
                selected_framework, context
            )

            # Step 4: Perform framework analysis
            insights = self.framework_analyzer.analyze_with_framework(
                selected_framework, context
            )

            # Step 5: Generate recommendations
            recommendations = self.framework_analyzer.generate_recommendations(
                insights, context
            )

            # Step 6: Create implementation plan
            implementation_steps = self.framework_analyzer.create_implementation_plan(
                recommendations, context
            )

            # Step 7: Calculate confidence scores
            overall_confidence = self.config.get_threshold(
                "quality_threshold"
            )  # Default
            if self.enable_confidence_calculation and insights:
                # Update individual insight confidences
                for insight in insights:
                    insight.confidence = (
                        self.confidence_calculator.calculate_insight_confidence(
                            insight, context
                        )
                    )

                # Calculate overall confidence
                overall_confidence = (
                    self.confidence_calculator.calculate_overall_confidence(
                        insights, framework_relevance
                    )
                )

            # Step 8: Create analysis result
            analysis_result = FrameworkAnalysisResult(
                framework_name=selected_framework,
                insights=insights,
                recommendations=recommendations,
                implementation_steps=implementation_steps,
                overall_confidence=overall_confidence,
                analysis_metadata={
                    "framework_relevance": framework_relevance,
                    "context_complexity": context.complexity_level.value,
                    "insights_count": len(insights),
                    "recommendations_count": len(recommendations),
                },
            )

            # Step 9: Integrate with persona (if available)
            persona_response = ""
            if (
                self.enable_persona_integration
                and self.persona_integrator
                and persona_context
            ):
                persona_name = persona_context.get("persona_name", "diego")
                persona_response = self.persona_integrator.integrate_with_persona(
                    insights, recommendations, persona_name, context
                )
            else:
                # Fallback persona response
                persona_response = self._create_fallback_persona_response(
                    analysis_result, persona_context
                )

            # Step 10: Create final result
            processing_time_ms = int((time.time() - start_time) * 1000)

            result = SystematicAnalysisResult(
                analysis_result=analysis_result,
                persona_integrated_response=persona_response,
                processing_time_ms=processing_time_ms,
                framework_applied=selected_framework,
                selection_confidence=framework_relevance,
                context_used=context,
            )

            logger.info(
                "Systematic analysis completed",
                framework_applied=selected_framework,
                insights_generated=len(insights),
                processing_time_ms=processing_time_ms,
                overall_confidence=overall_confidence,
            )

            return result

        except Exception as e:
            logger.error("Systematic analysis failed", error=str(e))
            return self._create_error_response(user_input, str(e), start_time)

    # Backward compatibility methods

    def _select_framework(
        self, user_input: str, persona_context: Optional[Dict] = None
    ) -> Optional[str]:
        """Backward compatibility method for framework selection"""
        context = self._create_analysis_context(user_input, persona_context)
        return self.framework_selector.select_framework(context)

    def _apply_framework(
        self, framework_name: str, user_input: str
    ) -> FrameworkAnalysis:
        """Backward compatibility method for framework application"""
        context = self._create_analysis_context(user_input)
        insights = self.framework_analyzer.analyze_with_framework(
            framework_name, context
        )
        recommendations = self.framework_analyzer.generate_recommendations(
            insights, context
        )
        implementation_steps = self.framework_analyzer.create_implementation_plan(
            recommendations, context
        )

        # Convert to old format for compatibility
        return FrameworkAnalysis(
            framework_name=framework_name,
            structured_insights={
                "insights": [
                    {
                        "category": i.category,
                        "insight": i.insight,
                        "evidence": i.evidence,
                    }
                    for i in insights
                ],
                "recommendations": [
                    {
                        "title": r.title,
                        "description": r.description,
                        "priority": r.priority,
                    }
                    for r in recommendations
                ],
            },
            recommendations=[r.description for r in recommendations],
            implementation_steps=[s.description for s in implementation_steps],
            key_considerations=[
                i.insight for i in insights if i.category == "risk_mitigation"
            ],
            analysis_confidence=(
                sum(i.confidence for i in insights) / len(insights)
                if insights
                else self.config.get_threshold("performance_degradation_limit") * 10
            ),
        )

    # Private helper methods

    def _create_analysis_context(
        self,
        user_input: str,
        persona_context: Optional[Dict] = None,
        session_id: str = "default",
    ) -> FrameworkContext:
        """Create analysis context from input parameters"""

        # Determine complexity based on input characteristics
        complexity = self._determine_complexity(user_input)

        # Extract domain hints from input
        domain_hints = self._extract_domain_hints(user_input)

        # Extract stakeholder and organizational context
        stakeholder_context = None
        organizational_context = None

        if persona_context:
            stakeholder_context = persona_context.get("stakeholder_context")
            organizational_context = persona_context.get("organizational_context")

        return FrameworkContext(
            user_input=user_input,
            domain_hints=domain_hints,
            complexity_level=complexity,
            stakeholder_context=stakeholder_context,
            organizational_context=organizational_context,
            session_history=None,  # Would be populated from session management
        )

    def _determine_complexity(self, user_input: str) -> AnalysisComplexity:
        """Determine analysis complexity from user input"""
        input_length = len(user_input)

        # Simple heuristic based on length and complexity indicators
        complexity_indicators = [
            "multiple",
            "complex",
            "various",
            "several",
            "different",
            "stakeholder",
            "organization",
            "system",
            "process",
            "strategy",
        ]

        indicator_count = sum(
            1 for indicator in complexity_indicators if indicator in user_input.lower()
        )

        if input_length > 200 or indicator_count >= 3:
            return AnalysisComplexity.HIGH
        elif input_length > 100 or indicator_count >= 2:
            return AnalysisComplexity.MEDIUM
        else:
            return AnalysisComplexity.LOW

    def _extract_domain_hints(self, user_input: str) -> List[FrameworkDomain]:
        """Extract domain hints from user input"""
        input_lower = user_input.lower()
        domains = []

        # Domain keyword mapping
        domain_keywords = {
            FrameworkDomain.STRATEGIC: [
                "strategy",
                "strategic",
                "planning",
                "roadmap",
                "vision",
                "goals",
            ],
            FrameworkDomain.ORGANIZATIONAL: [
                "team",
                "organization",
                "people",
                "culture",
                "management",
                "stakeholder",
            ],
            FrameworkDomain.TECHNICAL: [
                "technical",
                "architecture",
                "system",
                "platform",
                "technology",
                "engineering",
            ],
            FrameworkDomain.DESIGN: [
                "design",
                "user",
                "experience",
                "interface",
                "usability",
                "accessibility",
            ],
            FrameworkDomain.FINANCIAL: [
                "budget",
                "cost",
                "investment",
                "roi",
                "financial",
                "resource",
            ],
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                domains.append(domain)

        # Default to strategic if no specific domain detected
        if not domains:
            domains.append(FrameworkDomain.STRATEGIC)

        return domains

    def _create_fallback_response(
        self, user_input: str, start_time: float
    ) -> SystematicAnalysisResult:
        """Create fallback response when no framework is selected"""
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Create minimal analysis result
        analysis_result = FrameworkAnalysisResult(
            framework_name="general_analysis",
            insights=[],
            recommendations=[],
            implementation_steps=[],
            overall_confidence=0.3,
            analysis_metadata={"fallback": True},
        )

        # Create basic persona response
        persona_response = (
            "I notice this is a strategic question that could benefit from systematic analysis. "
            "While I couldn't identify a specific framework match, let me provide some general guidance based on the context you've shared."
        )

        context = self._create_analysis_context(user_input)

        return SystematicAnalysisResult(
            analysis_result=analysis_result,
            persona_integrated_response=persona_response,
            processing_time_ms=processing_time_ms,
            framework_applied="general_analysis",
            selection_confidence=0.3,
            context_used=context,
        )

    def _create_error_response(
        self, user_input: str, error_message: str, start_time: float
    ) -> SystematicAnalysisResult:
        """Create error response when analysis fails"""
        processing_time_ms = int((time.time() - start_time) * 1000)

        analysis_result = FrameworkAnalysisResult(
            framework_name="error_fallback",
            insights=[],
            recommendations=[],
            implementation_steps=[],
            overall_confidence=0.1,
            analysis_metadata={"error": error_message},
        )

        persona_response = (
            "I encountered an issue while analyzing your strategic question. "
            "Let me provide a direct response based on the context you've shared."
        )

        context = self._create_analysis_context(user_input)

        return SystematicAnalysisResult(
            analysis_result=analysis_result,
            persona_integrated_response=persona_response,
            processing_time_ms=processing_time_ms,
            framework_applied="error_fallback",
            selection_confidence=0.1,
            context_used=context,
        )

    def _create_fallback_persona_response(
        self, analysis_result: FrameworkAnalysisResult, persona_context: Optional[Dict]
    ) -> str:
        """Create fallback persona response when persona integrator is not available"""

        framework_name = analysis_result.framework_name
        insights_count = len(analysis_result.insights)
        recommendations_count = len(analysis_result.recommendations)

        response = f"Based on my analysis using the {framework_name} framework, "

        if insights_count > 0:
            response += f"I've identified {insights_count} key insights "

        if recommendations_count > 0:
            response += f"and {recommendations_count} strategic recommendations "

        response += "for your consideration. "

        if analysis_result.overall_confidence > self.config.get_threshold(
            "quality_threshold"
        ):
            response += "I have high confidence in this analysis based on the strategic patterns I've identified."
        elif (
            analysis_result.overall_confidence
            > self.config.get_threshold("performance_degradation_limit") * 10
        ):
            response += "This analysis provides a solid foundation, though some areas may benefit from additional context."
        else:
            response += "While this provides initial insights, I'd recommend gathering additional context for a more comprehensive analysis."

        return response
