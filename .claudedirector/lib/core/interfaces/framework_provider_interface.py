"""
Framework Provider Interface - SOLID Refactoring Phase 1

Defines the core abstractions for framework providers and analysis services.
This addresses Dependency Inversion Principle (DIP) by creating abstractions
that high-level modules can depend on instead of concrete implementations.

Author: Martin (SOLID Refactoring Implementation)
"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Protocol
from enum import Enum
from ..config import ClaudeDirectorConfig, get_config


class FrameworkDomain(Enum):
    """Framework application domains"""

    STRATEGIC = "strategic"
    ORGANIZATIONAL = "organizational"
    TECHNICAL = "technical"
    DESIGN = "design"
    FINANCIAL = "financial"


class AnalysisComplexity:
    """Analysis complexity levels"""

    def __init__(self, config: Optional[ClaudeDirectorConfig] = None):
        self.config = config or get_config()

    @property
    def LOW(self) -> str:
        return self.config.get_enum_values("priority_levels")[3]  # "low"

    @property
    def MEDIUM(self) -> str:
        return self.config.get_enum_values("priority_levels")[2]  # "medium"

    @property
    def HIGH(self) -> str:
        return self.config.get_enum_values("priority_levels")[1]  # "high"


@dataclass
class FrameworkContext:
    """Context information for framework selection and analysis"""

    user_input: str
    domain_hints: List[FrameworkDomain]
    complexity_level: AnalysisComplexity
    stakeholder_context: Optional[Dict[str, Any]] = None
    organizational_context: Optional[Dict[str, Any]] = None
    session_history: Optional[List[str]] = None


@dataclass
class FrameworkDefinition:
    """Definition of a strategic framework"""

    name: str
    description: str
    domains: List[FrameworkDomain]
    keywords: List[str]
    analysis_components: Dict[str, Any]
    confidence_threshold: float = 0.7


@dataclass
class AnalysisInsight:
    """Individual insight from framework analysis"""

    category: str
    insight: str
    evidence: List[str]
    confidence: float
    actionable: bool = True


@dataclass
class FrameworkRecommendation:
    """Strategic recommendation from framework analysis"""

    title: str
    description: str
    priority: (
        str  # Configured via ClaudeDirectorConfig.get_enum_values('priority_levels')
    )
    implementation_effort: (
        str  # Configured via ClaudeDirectorConfig.get_enum_values('priority_levels')
    )
    expected_impact: (
        str  # Configured via ClaudeDirectorConfig.get_enum_values('priority_levels')
    )
    dependencies: List[str]
    timeline: Optional[str] = None


@dataclass
class ImplementationStep:
    """Concrete implementation step"""

    step_number: int
    title: str
    description: str
    owner: Optional[str] = None
    timeline: Optional[str] = None
    dependencies: List[int] = None  # Step numbers this depends on
    success_criteria: List[str] = None


class IFrameworkProvider(Protocol):
    """
    Interface for framework providers.

    Defines the contract for providing framework definitions and metadata.
    This enables the Open/Closed Principle (OCP) by allowing new framework
    providers without modifying existing code.
    """

    @abstractmethod
    def get_framework_definition(
        self, framework_name: str
    ) -> Optional[FrameworkDefinition]:
        """Get definition for a specific framework"""

    @abstractmethod
    def get_available_frameworks(self) -> List[str]:
        """Get list of all available framework names"""

    @abstractmethod
    def get_frameworks_for_domain(self, domain: FrameworkDomain) -> List[str]:
        """Get frameworks applicable to a specific domain"""

    @abstractmethod
    def get_frameworks_by_keywords(self, keywords: List[str]) -> List[str]:
        """Get frameworks matching specific keywords"""


class IFrameworkSelector(Protocol):
    """
    Interface for framework selection strategies.

    Enables different selection algorithms while maintaining the same interface.
    Supports the Strategy pattern and Interface Segregation Principle (ISP).
    """

    @abstractmethod
    def select_framework(
        self, context: FrameworkContext, available_frameworks: List[str]
    ) -> Optional[str]:
        """Select the most appropriate framework for the given context"""

    @abstractmethod
    def calculate_framework_relevance(
        self, framework_name: str, context: FrameworkContext
    ) -> float:
        """Calculate relevance score (0.0-1.0) for a framework given context"""


class IFrameworkAnalyzer(Protocol):
    """
    Interface for framework analysis execution.

    Defines the contract for analyzing user input using a specific framework.
    Supports the Single Responsibility Principle (SRP) by focusing only on analysis.
    """

    @abstractmethod
    def analyze_with_framework(
        self, framework_name: str, context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Analyze context using the specified framework"""

    @abstractmethod
    def generate_recommendations(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[FrameworkRecommendation]:
        """Generate strategic recommendations from analysis insights"""

    @abstractmethod
    def create_implementation_plan(
        self, recommendations: List[FrameworkRecommendation], context: FrameworkContext
    ) -> List[ImplementationStep]:
        """Create concrete implementation steps from recommendations"""


class IInsightGenerator(Protocol):
    """
    Interface for insight generation services.

    Focuses specifically on generating insights from raw analysis data.
    Supports Single Responsibility Principle (SRP).
    """

    @abstractmethod
    def generate_insights(
        self, framework_definition: FrameworkDefinition, context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Generate insights using framework components"""

    @abstractmethod
    def enrich_insights_with_patterns(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Enrich insights with pattern matching and additional context"""


class IConfidenceCalculator(Protocol):
    """
    Interface for confidence calculation services.

    Focuses specifically on calculating confidence scores for analysis results.
    Supports Single Responsibility Principle (SRP).
    """

    @abstractmethod
    def calculate_insight_confidence(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> float:
        """Calculate confidence score for an individual insight"""

    @abstractmethod
    def calculate_overall_confidence(
        self, insights: List[AnalysisInsight], framework_relevance: float
    ) -> float:
        """Calculate overall confidence for the complete analysis"""


class IPersonaIntegrator(Protocol):
    """
    Interface for persona integration services.

    Handles integration of framework analysis with persona personalities.
    Supports Interface Segregation Principle (ISP) by providing focused interface.
    """

    @abstractmethod
    def integrate_with_persona(
        self,
        insights: List[AnalysisInsight],
        recommendations: List[FrameworkRecommendation],
        persona_name: str,
        context: FrameworkContext,
    ) -> str:
        """Integrate analysis results with persona personality"""

    @abstractmethod
    def get_persona_voice_characteristics(self, persona_name: str) -> Dict[str, Any]:
        """Get voice characteristics for a specific persona"""


# Result classes for the refactored architecture


@dataclass
class FrameworkAnalysisResult:
    """Complete result of framework analysis - replaces FrameworkAnalysis"""

    framework_name: str
    insights: List[AnalysisInsight]
    recommendations: List[FrameworkRecommendation]
    implementation_steps: List[ImplementationStep]
    overall_confidence: float
    analysis_metadata: Dict[str, Any]


@dataclass
class SystematicAnalysisResult:
    """Complete systematic analysis result - replaces SystematicResponse"""

    analysis_result: FrameworkAnalysisResult
    persona_integrated_response: str
    processing_time_ms: int
    framework_applied: str
    selection_confidence: float
    context_used: FrameworkContext
