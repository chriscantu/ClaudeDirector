"""
Dynamic Persona Activation Engine - Phase 2.1 Implementation

Implements intelligent persona activation based on user context analysis.
Follows Martin's ADR-004 architecture for context analysis, persona selection,
template activation, and conversation state management.

Part of Phase 2.1: Core Engine Development
"""

import re
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from .template_engine import (
    TemplateDiscoveryEngine,
    DirectorTemplate,
)

logger = logging.getLogger(__name__)


class ConfidenceLevel(Enum):
    """Confidence levels for persona activation"""

    HIGH = "high"  # >= 0.8 - Direct activation
    MEDIUM = "medium"  # >= 0.6 - Suggest with confirmation
    LOW = "low"  # >= 0.4 - Show multiple options
    NONE = "none"  # < 0.4 - Use fallback


@dataclass
class ContextResult:
    """Result of context analysis with confidence and extracted information"""

    # Primary analysis results
    domain: Optional[str] = None
    confidence: float = 0.0
    suggested_template: Optional[str] = None

    # Extracted context information
    keywords: List[str] = field(default_factory=list)
    detected_industry: Optional[str] = None
    detected_team_size: Optional[str] = None

    # Analysis metadata
    analysis_time_ms: int = 0
    confidence_level: ConfidenceLevel = ConfidenceLevel.NONE

    def __post_init__(self):
        """Determine confidence level based on confidence score"""
        if self.confidence >= 0.8:
            self.confidence_level = ConfidenceLevel.HIGH
        elif self.confidence >= 0.6:
            self.confidence_level = ConfidenceLevel.MEDIUM
        elif self.confidence >= 0.4:
            self.confidence_level = ConfidenceLevel.LOW
        else:
            self.confidence_level = ConfidenceLevel.NONE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "domain": self.domain,
            "confidence": self.confidence,
            "suggested_template": self.suggested_template,
            "keywords": self.keywords,
            "detected_industry": self.detected_industry,
            "detected_team_size": self.detected_team_size,
            "analysis_time_ms": self.analysis_time_ms,
            "confidence_level": self.confidence_level.value,
        }


@dataclass
class PersonaSelection:
    """Result of persona selection with rationale and alternatives"""

    # Selected persona information
    primary: str
    template_id: str
    confidence: float

    # Alternative personas for context
    contextual: List[str] = field(default_factory=list)
    fallback: str = "camille"

    # Selection rationale
    rationale: str = ""
    selection_method: str = "automatic"  # automatic, fallback, manual

    # Metadata
    selection_time_ms: int = 0
    alternatives_considered: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "primary": self.primary,
            "template_id": self.template_id,
            "confidence": self.confidence,
            "contextual": self.contextual,
            "fallback": self.fallback,
            "rationale": self.rationale,
            "selection_method": self.selection_method,
            "selection_time_ms": self.selection_time_ms,
            "alternatives_considered": self.alternatives_considered,
        }


@dataclass
class PersonaActivation:
    """Record of persona activation for conversation state tracking"""

    persona: str
    template_id: str
    context: ContextResult
    confidence: float
    timestamp: datetime
    user_input: str = ""
    activation_method: str = "automatic"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "persona": self.persona,
            "template_id": self.template_id,
            "context": self.context.to_dict(),
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "user_input": self.user_input,
            "activation_method": self.activation_method,
        }


class ContextAnalysisEngine:
    """
    Context Analysis Engine - Phase 2.1

    Analyzes user input to determine appropriate template and persona activation.
    Uses hybrid approach: keyword matching + confidence scoring + domain classification.

    Performance target: <500ms analysis time
    Accuracy target: 90% correct domain detection
    """

    def __init__(self, template_discovery: TemplateDiscoveryEngine):
        """Initialize context analysis engine"""
        self.template_discovery = template_discovery

        # Industry detection patterns
        self.industry_patterns = {
            "fintech": [
                r"\b(fintech|financial|banking|payment|transaction|crypto|blockchain)\b",
                r"\b(regulatory|compliance|PCI|SOX|GDPR)\b",
                r"\b(trading|investment|insurance|lending)\b",
            ],
            "healthcare": [
                r"\b(healthcare|medical|patient|clinical|HIPAA)\b",
                r"\b(hospital|clinic|pharma|biotech)\b",
                r"\b(medical device|health records|telemedicine)\b",
            ],
            "saas": [
                r"\b(SaaS|subscription|multi.?tenant|cloud.?native)\b",
                r"\b(customer retention|churn|MAU|ARR|MRR)\b",
                r"\b(freemium|enterprise|self.?service)\b",
            ],
            "ecommerce": [
                r"\b(ecommerce|e.?commerce|retail|marketplace)\b",
                r"\b(shopping|cart|checkout|inventory|fulfillment)\b",
                r"\b(conversion|recommendation|personalization)\b",
            ],
            "gaming": [
                r"\b(gaming|game|player|leaderboard|tournament)\b",
                r"\b(real.?time|multiplayer|session|matchmaking)\b",
                r"\b(monetization|in.?app|virtual currency)\b",
            ],
        }

        # Team size detection patterns
        self.team_size_patterns = {
            "startup": [
                r"\b(startup|early.?stage|seed|pre.?series)\b",
                r"\b(small team|limited resources|MVP|prototype)\b",
                r"\b([1-9]|1[0-5])\s*(engineer|developer|person|people)\b",
            ],
            "scale": [
                r"\b(scale|scaling|growth|series [AB])\b",
                r"\b(medium team|growing|expanding)\b",
                r"\b((1[6-9]|[2-4][0-9]|50)\s*(engineer|developer|person|people))\b",
            ],
            "enterprise": [
                r"\b(enterprise|large.?scale|fortune|corporation)\b",
                r"\b(hundreds|thousand|legacy|governance)\b",
                r"\b(([5-9][0-9]|[1-9][0-9]{2,})\s*(engineer|developer|person|people))\b",
            ],
        }

    def analyze_context(self, user_input: str) -> ContextResult:
        """
        Analyze user input to determine context and template suggestions

        Args:
            user_input: User's message or query

        Returns:
            ContextResult with domain, confidence, and extracted context
        """
        start_time = time.time()

        try:
            # Multi-layer analysis
            keyword_results = self._analyze_keywords(user_input)
            domain_results = self._classify_domain(user_input)
            template_results = self._match_templates(user_input)

            # Extract additional context
            industry = self._detect_industry(user_input)
            team_size = self._detect_team_size(user_input)

            # Calculate weighted confidence
            total_confidence = self._calculate_weighted_confidence(
                keyword_results, domain_results, template_results
            )

            # Determine best template
            suggested_template = self._determine_best_template(
                keyword_results, domain_results, template_results
            )

            # Create result
            result = ContextResult(
                domain=domain_results.get("domain"),
                confidence=total_confidence,
                suggested_template=suggested_template,
                keywords=keyword_results.get("keywords", []),
                detected_industry=industry,
                detected_team_size=team_size,
                analysis_time_ms=int((time.time() - start_time) * 1000),
            )

            logger.info(
                f"Context analysis completed in {result.analysis_time_ms}ms, "
                f"confidence: {result.confidence:.2f}, domain: {result.domain}"
            )

            return result

        except Exception as e:
            logger.error(f"Context analysis failed: {e}")
            # Return low-confidence fallback result
            return ContextResult(
                analysis_time_ms=int((time.time() - start_time) * 1000)
            )

    def _analyze_keywords(self, text: str) -> Dict[str, Any]:
        """Analyze text for template-specific keywords"""
        keywords_found = []
        template_scores = {}

        # Get all templates and check activation keywords
        templates = self.template_discovery.list_templates()

        for template in templates:
            template_confidence = template.get_activation_confidence(text)
            if template_confidence > 0:
                template_scores[template.template_id] = template_confidence

                # Extract matching keywords
                for keyword, _ in template.activation_keywords.keywords.items():
                    if keyword.lower() in text.lower():
                        keywords_found.append(keyword)

        # Find best matching template
        best_template = (
            max(template_scores.items(), key=lambda x: x[1])
            if template_scores
            else None
        )
        best_confidence = best_template[1] if best_template else 0.0

        return {
            "keywords": list(set(keywords_found)),
            "template_scores": template_scores,
            "best_template": best_template[0] if best_template else None,
            "confidence": best_confidence,
        }

    def _classify_domain(self, text: str) -> Dict[str, Any]:
        """Classify text into engineering director domains"""
        domain_scores = {}
        text_lower = text.lower()

        # Domain classification patterns
        domain_patterns = {
            "mobile_platforms": [
                "mobile",
                "ios",
                "android",
                "app store",
                "react native",
                "flutter",
                "swift",
                "kotlin",
                "mobile app",
            ],
            "product_engineering": [
                "product strategy",
                "user experience",
                "feature",
                "customer",
                "product roadmap",
                "user research",
                "product analytics",
                "conversion",
            ],
            "platform_engineering": [
                "platform",
                "developer tools",
                "internal tools",
                "ci/cd",
                "developer productivity",
                "tooling",
                "automation",
                "infrastructure as code",
            ],
            "backend_services": [
                "backend",
                "microservices",
                "api",
                "database",
                "scalability",
                "service mesh",
                "distributed systems",
                "data consistency",
            ],
            "infrastructure_devops": [
                "infrastructure",
                "devops",
                "kubernetes",
                "docker",
                "cloud",
                "monitoring",
                "reliability",
                "sre",
                "deployment",
            ],
            "data_analytics_ml": [
                "data",
                "analytics",
                "machine learning",
                "ml",
                "data pipeline",
                "data warehouse",
                "business intelligence",
                "data science",
            ],
        }

        for domain, patterns in domain_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1

            if score > 0:
                domain_scores[domain] = score / len(
                    patterns
                )  # Normalize by pattern count

        # Find best domain
        best_domain = (
            max(domain_scores.items(), key=lambda x: x[1]) if domain_scores else None
        )

        return {
            "domain": best_domain[0] if best_domain else None,
            "confidence": best_domain[1] if best_domain else 0.0,
            "all_scores": domain_scores,
        }

    def _match_templates(self, text: str) -> Dict[str, Any]:
        """Match text against available templates using discovery engine"""
        try:
            results = self.template_discovery.discover_templates_by_context(
                text, threshold=0.1
            )

            if not results:
                return {"confidence": 0.0, "best_template": None}

            # Get best result
            best_template, best_confidence = results[0]

            return {
                "confidence": best_confidence,
                "best_template": best_template.template_id,
                "all_results": [(t.template_id, c) for t, c in results[:3]],  # Top 3
            }

        except Exception as e:
            logger.error(f"Template matching failed: {e}")
            return {"confidence": 0.0, "best_template": None}

    def _detect_industry(self, text: str) -> Optional[str]:
        """Detect industry context from text"""
        text_lower = text.lower()

        for industry, patterns in self.industry_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    logger.debug(
                        f"Detected industry '{industry}' from pattern '{pattern}'"
                    )
                    return industry

        return None

    def _detect_team_size(self, text: str) -> Optional[str]:
        """Detect team size context from text"""
        text_lower = text.lower()

        for size, patterns in self.team_size_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    logger.debug(
                        f"Detected team size '{size}' from pattern '{pattern}'"
                    )
                    return size

        return None

    def _calculate_weighted_confidence(
        self, keyword_results: Dict, domain_results: Dict, template_results: Dict
    ) -> float:
        """Calculate weighted confidence score from multiple analysis methods"""

        # Weights from global settings (matching ADR specification)
        keyword_weight = 0.4
        domain_weight = 0.4
        template_weight = 0.2

        keyword_confidence = keyword_results.get("confidence", 0.0)
        domain_confidence = domain_results.get("confidence", 0.0)
        template_confidence = template_results.get("confidence", 0.0)

        total_confidence = (
            keyword_confidence * keyword_weight
            + domain_confidence * domain_weight
            + template_confidence * template_weight
        )

        return min(total_confidence, 1.0)  # Cap at 1.0

    def _determine_best_template(
        self, keyword_results: Dict, domain_results: Dict, template_results: Dict
    ) -> Optional[str]:
        """Determine the best template based on analysis results"""

        # Priority order: keyword matching > template matching > domain classification
        keyword_template = keyword_results.get("best_template")
        template_match = template_results.get("best_template")
        domain = domain_results.get("domain")

        # Use keyword result if high confidence
        if keyword_template and keyword_results.get("confidence", 0) >= 0.7:
            return keyword_template

        # Use template matching result if available
        if template_match and template_results.get("confidence", 0) >= 0.6:
            return template_match

        # Fall back to domain-based template selection
        if domain:
            domain_template_map = {
                "mobile_platforms": "mobile_director",
                "product_engineering": "product_engineering_director",
                "platform_engineering": "platform_director",
                "backend_services": "backend_director",
                "infrastructure_devops": "infrastructure_director",
                "data_analytics_ml": "data_director",
            }
            return domain_template_map.get(domain)

        return None


class PersonaSelectionEngine:
    """
    Persona Selection Engine - Phase 2.1

    Selects optimal persona based on context analysis and template configuration.
    Uses primary persona with contextual backup strategy from Martin's ADR.

    Performance target: <300ms selection time
    """

    def __init__(self, template_discovery: TemplateDiscoveryEngine):
        """Initialize persona selection engine"""
        self.template_discovery = template_discovery

    def select_persona(
        self, context: ContextResult, override_template: Optional[str] = None
    ) -> PersonaSelection:
        """
        Select optimal persona based on context analysis

        Args:
            context: Result from context analysis
            override_template: Optional template override

        Returns:
            PersonaSelection with primary persona and alternatives
        """
        start_time = time.time()

        try:
            # Determine template to use
            template_id = override_template or context.suggested_template

            if not template_id:
                # Use fallback strategy
                return self._create_fallback_selection(context, start_time)

            # Get template
            template = self.template_discovery.get_template(template_id)
            if not template:
                logger.warning(f"Template {template_id} not found, using fallback")
                return self._create_fallback_selection(context, start_time)

            # Select persona based on confidence level
            if context.confidence >= 0.8:
                # High confidence - use primary persona
                primary_persona = self._select_from_primary(context, template)
                selection_method = "automatic_high_confidence"
                rationale = f"High confidence ({context.confidence:.2f}) match for {template.display_name}"

            elif context.confidence >= 0.6:
                # Medium confidence - use contextual persona
                primary_persona = self._select_from_contextual(context, template)
                selection_method = "automatic_medium_confidence"
                rationale = f"Medium confidence ({context.confidence:.2f}) match for {template.display_name}"

            else:
                # Low confidence - use fallback
                primary_persona = (
                    template.personas.fallback[0]
                    if template.personas.fallback
                    else "camille"
                )
                selection_method = "fallback_low_confidence"
                rationale = (
                    f"Low confidence ({context.confidence:.2f}), using fallback persona"
                )

            # Get contextual and fallback personas
            contextual_personas = self._get_relevant_contextual(context, template)
            fallback_persona = (
                template.personas.fallback[0]
                if template.personas.fallback
                else "camille"
            )

            # Create selection result
            selection = PersonaSelection(
                primary=primary_persona,
                template_id=template_id,
                confidence=context.confidence,
                contextual=contextual_personas,
                fallback=fallback_persona,
                rationale=rationale,
                selection_method=selection_method,
                selection_time_ms=int((time.time() - start_time) * 1000),
                alternatives_considered=template.personas.get_all_personas(),
            )

            logger.info(
                f"Persona selection completed: {primary_persona} "
                f"({selection_method}) in {selection.selection_time_ms}ms"
            )

            return selection

        except Exception as e:
            logger.error(f"Persona selection failed: {e}")
            return self._create_fallback_selection(context, start_time)

    def _select_from_primary(
        self, context: ContextResult, template: DirectorTemplate
    ) -> str:
        """Select persona from template's primary personas"""
        if not template.personas.primary:
            return "camille"  # Ultimate fallback

        # For now, return first primary persona
        # Future enhancement: ML-based selection based on context nuances
        return template.personas.primary[0]

    def _select_from_contextual(
        self, context: ContextResult, template: DirectorTemplate
    ) -> str:
        """Select persona from template's contextual personas"""
        if not template.personas.contextual:
            # Fall back to primary if no contextual available
            return self._select_from_primary(context, template)

        # For now, return first contextual persona
        # Future enhancement: Context-specific selection
        return template.personas.contextual[0]

    def _get_relevant_contextual(
        self, context: ContextResult, template: DirectorTemplate
    ) -> List[str]:
        """Get relevant contextual personas based on context"""
        # Return all contextual personas for now
        # Future enhancement: Filter based on context.keywords, industry, etc.
        return template.personas.contextual

    def _create_fallback_selection(
        self, context: ContextResult, start_time: float
    ) -> PersonaSelection:
        """Create fallback persona selection when template-based selection fails"""
        return PersonaSelection(
            primary="camille",  # Global fallback persona
            template_id="fallback",
            confidence=0.0,
            contextual=["diego", "alvaro"],  # Global contextual fallbacks
            fallback="camille",
            rationale="Fallback selection due to low confidence or missing template",
            selection_method="global_fallback",
            selection_time_ms=int((time.time() - start_time) * 1000),
            alternatives_considered=["camille", "diego", "alvaro"],
        )


class ConversationStateEngine:
    """
    Conversation State Engine - Phase 2.1

    Manages conversation state, persona transitions, and activation history.
    Maintains context across turns and tracks persona usage patterns.
    """

    def __init__(self):
        """Initialize conversation state engine"""
        self.current_template: Optional[DirectorTemplate] = None
        self.current_template_id: Optional[str] = None
        self.active_persona: Optional[str] = None
        self.conversation_context: Dict[str, Any] = {}
        self.activation_history: List[PersonaActivation] = []

        # State tracking
        self.session_start_time = datetime.now()
        self.total_activations = 0
        self.persona_usage_count: Dict[str, int] = {}

    def update_state(
        self,
        persona_selection: PersonaSelection,
        context: ContextResult,
        user_input: str = "",
    ) -> None:
        """
        Update conversation state with new persona activation

        Args:
            persona_selection: Result of persona selection
            context: Context analysis result
            user_input: Original user input
        """
        try:
            # Create activation record
            activation = PersonaActivation(
                persona=persona_selection.primary,
                template_id=persona_selection.template_id,
                context=context,
                confidence=persona_selection.confidence,
                timestamp=datetime.now(),
                user_input=user_input,
                activation_method=persona_selection.selection_method,
            )

            # Add to history
            self.activation_history.append(activation)

            # Update current state
            self.active_persona = persona_selection.primary
            self.current_template_id = persona_selection.template_id

            # Update conversation context
            self.conversation_context.update(context.to_dict())

            # Update usage statistics
            self.total_activations += 1
            self.persona_usage_count[persona_selection.primary] = (
                self.persona_usage_count.get(persona_selection.primary, 0) + 1
            )

            logger.info(
                f"State updated: {persona_selection.primary} active, "
                f"total activations: {self.total_activations}"
            )

        except Exception as e:
            logger.error(f"Failed to update conversation state: {e}")

    def get_current_state(self) -> Dict[str, Any]:
        """Get current conversation state summary"""
        return {
            "active_persona": self.active_persona,
            "current_template_id": self.current_template_id,
            "total_activations": self.total_activations,
            "session_duration_minutes": (
                datetime.now() - self.session_start_time
            ).total_seconds()
            / 60,
            "persona_usage_count": self.persona_usage_count.copy(),
            "recent_context": self.conversation_context.copy(),
            "last_activation_time": (
                self.activation_history[-1].timestamp.isoformat()
                if self.activation_history
                else None
            ),
        }

    def get_activation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activation history"""
        recent_activations = (
            self.activation_history[-limit:] if limit > 0 else self.activation_history
        )
        return [activation.to_dict() for activation in recent_activations]

    def suggest_persona_switch(self, context: ContextResult) -> Optional[str]:
        """
        Suggest persona switch if current persona doesn't match new context

        Args:
            context: New context analysis result

        Returns:
            Suggested persona or None if current persona is appropriate
        """
        if not self.active_persona or not context.suggested_template:
            return None

        # Check if context suggests different template
        if (
            context.suggested_template != self.current_template_id
            and context.confidence >= 0.7
        ):
            logger.info(
                f"Context suggests template switch: {self.current_template_id} -> {context.suggested_template}"
            )
            return context.suggested_template

        return None

    def reset_session(self) -> None:
        """Reset conversation state for new session"""
        self.current_template = None
        self.current_template_id = None
        self.active_persona = None
        self.conversation_context.clear()
        self.activation_history.clear()
        self.session_start_time = datetime.now()
        self.total_activations = 0
        self.persona_usage_count.clear()

        logger.info("Conversation state reset for new session")
