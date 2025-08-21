"""
ClaudeDirector Template Discovery Engine

Implements template discovery, validation, and selection functionality
for multi-domain engineering director templates.

Part of Phase 1 implementation addressing Martin's TD-1 and TD-3 requirements.
"""

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None

from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TemplateValidationError(Exception):
    """Raised when template validation fails"""



class TemplateDomain(Enum):
    """Supported director template domains"""

    PLATFORM = "platform_engineering"
    MOBILE = "mobile_platforms"
    BACKEND = "backend_services"
    INFRASTRUCTURE = "infrastructure_devops"
    DATA = "data_analytics_ml"
    PRODUCT = "product_engineering"
    SECURITY = "security_engineering"
    FRONTEND = "frontend_engineering"


@dataclass
class TemplateActivationKeywords:
    """Template activation keyword configuration"""

    keywords: Dict[str, float] = field(default_factory=dict)

    def get_confidence(self, text: str) -> float:
        """Calculate activation confidence for given text"""
        text_lower = text.lower()
        max_confidence = 0.0

        for keyword, confidence in self.keywords.items():
            if keyword.lower() in text_lower:
                max_confidence = max(max_confidence, confidence)

        return max_confidence


@dataclass
class TemplatePersonaConfig:
    """Template persona configuration"""

    primary: List[str] = field(default_factory=list)
    contextual: List[str] = field(default_factory=list)
    fallback: List[str] = field(default_factory=list)

    def get_all_personas(self) -> List[str]:
        """Get all personas in priority order"""
        return self.primary + self.contextual + self.fallback

    def get_primary_persona(self) -> Optional[str]:
        """Get the primary persona for this template"""
        return self.primary[0] if self.primary else None


@dataclass
class IndustryModifier:
    """Industry-specific template modifier"""

    priorities: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)


@dataclass
class TeamSizeContext:
    """Team size context configuration"""

    focus: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)


@dataclass
class DirectorTemplate:
    """
    Director template configuration

    Represents a complete template for a specific engineering director domain
    with industry modifiers, team size contexts, and persona configurations.
    """

    # Basic template metadata
    template_id: str
    domain: str
    display_name: str
    description: str

    # Configuration components
    personas: TemplatePersonaConfig = field(default_factory=TemplatePersonaConfig)
    activation_keywords: TemplateActivationKeywords = field(
        default_factory=TemplateActivationKeywords
    )

    # Context modifiers
    industry_modifiers: Dict[str, IndustryModifier] = field(default_factory=dict)
    team_size_contexts: Dict[str, TeamSizeContext] = field(default_factory=dict)

    # Strategic configuration
    strategic_priorities: List[str] = field(default_factory=list)
    metrics_focus: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate template after initialization"""
        self._validate()

    def _validate(self):
        """Validate template configuration"""
        if not self.template_id:
            raise TemplateValidationError("Template ID is required")

        if not self.domain:
            raise TemplateValidationError("Template domain is required")

        if not self.personas.primary:
            raise TemplateValidationError("At least one primary persona is required")

        # Validate domain is supported
        try:
            TemplateDomain(self.domain)
        except ValueError:
            raise TemplateValidationError(f"Unsupported template domain: {self.domain}")

    def get_activation_confidence(self, context: str) -> float:
        """Get activation confidence for given context"""
        return self.activation_keywords.get_confidence(context)

    def get_optimal_persona(self, context: str = "") -> str:
        """Get optimal persona for given context"""
        # For now, return primary persona
        # Future enhancement: ML-based context analysis
        return self.personas.get_primary_persona() or "camille"

    def apply_industry_modifier(self, industry: str) -> Dict[str, Any]:
        """Apply industry-specific modifications"""
        if industry not in self.industry_modifiers:
            return {}

        modifier = self.industry_modifiers[industry]
        return {
            "enhanced_priorities": self.strategic_priorities + modifier.priorities,
            "enhanced_metrics": self.metrics_focus + modifier.metrics,
        }

    def apply_team_size_context(self, team_size: str) -> Dict[str, Any]:
        """Apply team size context modifications"""
        if team_size not in self.team_size_contexts:
            return {}

        context = self.team_size_contexts[team_size]
        return {"focus_areas": context.focus, "key_challenges": context.challenges}


class TemplateDiscoveryEngine:
    """
    Template discovery and management engine

    Handles loading, validation, discovery, and selection of director templates.
    Implements Martin's TD-1 (Configuration System) and TD-3 (Discovery API).
    """

    def __init__(self, templates_config_path: Optional[Path] = None):
        """Initialize template discovery engine"""
        self.templates_config_path = templates_config_path or Path(
            "config/director_templates.yaml"
        )
        self.templates: Dict[str, DirectorTemplate] = {}
        self.global_settings: Dict[str, Any] = {}
        self._load_templates()

    def _load_templates(self):
        """Load templates from configuration file"""
        try:
            if not YAML_AVAILABLE:
                logger.warning(
                    "PyYAML not available. Template discovery disabled. "
                    "Install with: pip install PyYAML>=6.0.0"
                )
                return

            if not self.templates_config_path.exists():
                logger.warning(
                    f"Template config not found: {self.templates_config_path}"
                )
                return

            with open(self.templates_config_path, "r") as f:
                config = yaml.safe_load(f)

            self.global_settings = config.get("global_settings", {})
            templates_config = config.get("templates", {})

            for template_id, template_data in templates_config.items():
                try:
                    template = self._parse_template(template_id, template_data)
                    self.templates[template_id] = template
                    logger.info(f"Loaded template: {template_id}")
                except Exception as e:
                    logger.error(f"Failed to load template {template_id}: {e}")

        except Exception as e:
            logger.error(f"Failed to load templates config: {e}")

    def _parse_template(
        self, template_id: str, template_data: Dict[str, Any]
    ) -> DirectorTemplate:
        """Parse template data into DirectorTemplate object"""

        # Parse personas configuration
        personas_data = template_data.get("personas", {})
        personas = TemplatePersonaConfig(
            primary=personas_data.get("primary", []),
            contextual=personas_data.get("contextual", []),
            fallback=personas_data.get("fallback", []),
        )

        # Parse activation keywords
        keywords_data = template_data.get("activation_keywords", {})
        activation_keywords = TemplateActivationKeywords(keywords=keywords_data)

        # Parse industry modifiers
        industry_modifiers = {}
        for industry, modifier_data in template_data.get(
            "industry_modifiers", {}
        ).items():
            industry_modifiers[industry] = IndustryModifier(
                priorities=modifier_data.get("priorities", []),
                metrics=modifier_data.get("metrics", []),
            )

        # Parse team size contexts
        team_size_contexts = {}
        for size, context_data in template_data.get("team_size_contexts", {}).items():
            team_size_contexts[size] = TeamSizeContext(
                focus=context_data.get("focus", []),
                challenges=context_data.get("challenges", []),
            )

        return DirectorTemplate(
            template_id=template_id,
            domain=template_data["domain"],
            display_name=template_data["display_name"],
            description=template_data["description"],
            personas=personas,
            activation_keywords=activation_keywords,
            industry_modifiers=industry_modifiers,
            team_size_contexts=team_size_contexts,
            strategic_priorities=template_data.get("strategic_priorities", []),
            metrics_focus=template_data.get("metrics_focus", []),
        )

    def list_templates(
        self, domain_filter: Optional[str] = None
    ) -> List[DirectorTemplate]:
        """List available templates, optionally filtered by domain"""
        templates = list(self.templates.values())

        if domain_filter:
            templates = [t for t in templates if t.domain == domain_filter]

        return sorted(templates, key=lambda t: t.display_name)

    def get_template(self, template_id: str) -> Optional[DirectorTemplate]:
        """Get specific template by ID"""
        return self.templates.get(template_id)

    def discover_templates_by_context(
        self, context: str, threshold: float = 0.6
    ) -> List[Tuple[DirectorTemplate, float]]:
        """
        Discover templates based on context with confidence scores

        Returns list of (template, confidence) tuples sorted by confidence
        """
        results = []

        for template in self.templates.values():
            confidence = template.get_activation_confidence(context)
            if confidence >= threshold:
                results.append((template, confidence))

        # Sort by confidence (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_domains(self) -> List[str]:
        """Get list of available template domains"""
        domains = set(template.domain for template in self.templates.values())
        return sorted(list(domains))

    def get_available_industries(self, template_id: str) -> List[str]:
        """Get available industry modifiers for a template"""
        template = self.get_template(template_id)
        if not template:
            return []
        return list(template.industry_modifiers.keys())

    def get_available_team_sizes(self, template_id: str) -> List[str]:
        """Get available team size contexts for a template"""
        template = self.get_template(template_id)
        if not template:
            return []
        return list(template.team_size_contexts.keys())

    def validate_template_selection(
        self,
        template_id: str,
        industry: Optional[str] = None,
        team_size: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validate a template selection with optional modifiers"""
        template = self.get_template(template_id)
        if not template:
            return {"valid": False, "error": f"Template not found: {template_id}"}

        validation_result = {"valid": True, "template": template, "warnings": []}

        # Validate industry modifier
        if industry and industry not in template.industry_modifiers:
            validation_result["warnings"].append(
                f"Industry '{industry}' not specifically supported for this template"
            )

        # Validate team size context
        if team_size and team_size not in template.team_size_contexts:
            validation_result["warnings"].append(
                f"Team size '{team_size}' not specifically supported for this template"
            )

        return validation_result

    def generate_template_summary(
        self,
        template_id: str,
        industry: Optional[str] = None,
        team_size: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a comprehensive template summary for user review"""
        template = self.get_template(template_id)
        if not template:
            return {"error": f"Template not found: {template_id}"}

        summary = {
            "template_id": template_id,
            "display_name": template.display_name,
            "description": template.description,
            "domain": template.domain,
            "primary_personas": template.personas.primary,
            "strategic_priorities": template.strategic_priorities,
            "metrics_focus": template.metrics_focus,
        }

        # Apply industry modifier if specified
        if industry:
            industry_mods = template.apply_industry_modifier(industry)
            if industry_mods:
                summary["industry_enhancements"] = industry_mods

        # Apply team size context if specified
        if team_size:
            team_context = template.apply_team_size_context(team_size)
            if team_context:
                summary["team_size_context"] = team_context

        return summary

    def get_template_comparison(self, template_ids: List[str]) -> Dict[str, Any]:
        """Generate a comparison view between multiple templates"""
        if len(template_ids) > 4:
            return {"error": "Cannot compare more than 4 templates at once"}

        comparison = {
            "templates": {},
            "comparison_matrix": {
                "domains": {},
                "primary_personas": {},
                "strategic_priorities": {},
                "metrics_focus": {},
            },
        }

        for template_id in template_ids:
            template = self.get_template(template_id)
            if template:
                comparison["templates"][template_id] = {
                    "display_name": template.display_name,
                    "description": template.description,
                    "domain": template.domain,
                    "primary_personas": template.personas.primary,
                    "strategic_priorities": template.strategic_priorities[:5],  # Top 5
                    "metrics_focus": template.metrics_focus[:5],  # Top 5
                }

        return comparison
