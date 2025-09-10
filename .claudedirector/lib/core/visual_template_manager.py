"""
Visual Template Manager - Phase 12 Magic MCP Enhancement
Persona-specific visual enhancement templates for always-on Magic MCP integration

🎯 STORY 9.5.3: VISUAL TEMPLATE MANAGER - BaseManager Enhanced
PHASE 3 CONSOLIDATION: Converted to BaseManager for DRY compliance
ELIMINATES duplicate infrastructure patterns while maintaining visual template functionality
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# STORY 9.5.3: BaseManager import for consolidation
from .base_manager import BaseManager, BaseManagerConfig, ManagerType


class VisualType(Enum):
    """Types of visual enhancements"""

    ORG_CHART = "org_chart"
    ARCHITECTURE_DIAGRAM = "architecture_diagram"
    DESIGN_SYSTEM = "design_system"
    BUSINESS_CHART = "business_chart"
    STRATEGIC_ROADMAP = "strategic_roadmap"
    USER_FLOW = "user_flow"
    PROCESS_FLOW = "process_flow"
    SYSTEM_DESIGN = "system_design"


@dataclass
class VisualTemplate:
    """Template for persona-specific visual enhancement"""

    visual_type: VisualType
    magic_prompt_prefix: str
    style: str
    persona: str
    description: str


class VisualTemplateManager(BaseManager):
    """
    🎯 STORY 9.5.3: VISUAL TEMPLATE MANAGER - BaseManager Enhanced

    PHASE 3 CONSOLIDATION: Converted to BaseManager for DRY compliance
    ELIMINATES duplicate infrastructure patterns while maintaining visual template functionality

    PHASE 12: Persona-specific visual template manager for Magic MCP

    Maps personas to their specialized visual enhancement templates,
    ensuring automatic Magic MCP routing with domain-optimized outputs.

    ARCHITECTURAL BENEFITS:
    - BaseManager infrastructure eliminates duplicate logging/caching/metrics
    - Unified configuration and error handling patterns
    - Performance optimized with BaseManager caching
    """

    def __init__(self):
        """Initialize with BaseManager consolidation"""
        # STORY 9.5.3: BaseManager initialization eliminates duplicate infrastructure
        config = BaseManagerConfig(
            manager_name="visual_template_manager",
            manager_type=ManagerType.CONFIGURATION,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
        )
        super().__init__(config)

        self.persona_templates = self._initialize_persona_templates()
        self.visual_keywords = self._initialize_visual_keywords()

        self.logger.info(
            "VisualTemplateManager initialized with BaseManager consolidation",
            persona_count=len(self.persona_templates),
            template_count=sum(
                len(templates) for templates in self.persona_templates.values()
            ),
            visual_types=len(self.visual_keywords),
        )

    def _initialize_persona_templates(self) -> Dict[str, List[VisualTemplate]]:
        """Initialize persona-specific visual templates"""
        return {
            "diego": [
                VisualTemplate(
                    visual_type=VisualType.ORG_CHART,
                    magic_prompt_prefix="Create professional organizational chart showing",
                    style="executive_presentation",
                    persona="diego",
                    description="Team structures and reporting relationships",
                ),
                VisualTemplate(
                    visual_type=VisualType.PROCESS_FLOW,
                    magic_prompt_prefix="Create systematic process flow diagram for",
                    style="leadership_documentation",
                    persona="diego",
                    description="Cross-team coordination and workflow processes",
                ),
                VisualTemplate(
                    visual_type=VisualType.STRATEGIC_ROADMAP,
                    magic_prompt_prefix="Create strategic roadmap visualization of",
                    style="executive_presentation",
                    persona="diego",
                    description="Organizational transformation and strategic initiatives",
                ),
            ],
            "martin": [
                VisualTemplate(
                    visual_type=VisualType.ARCHITECTURE_DIAGRAM,
                    magic_prompt_prefix="Create technical architecture diagram showing",
                    style="engineering_documentation",
                    persona="martin",
                    description="System architecture and technical component relationships",
                ),
                VisualTemplate(
                    visual_type=VisualType.SYSTEM_DESIGN,
                    magic_prompt_prefix="Create platform system design diagram for",
                    style="technical_specification",
                    persona="martin",
                    description="Platform architecture and integration patterns",
                ),
                VisualTemplate(
                    visual_type=VisualType.PROCESS_FLOW,
                    magic_prompt_prefix="Create technical workflow diagram showing",
                    style="engineering_documentation",
                    persona="martin",
                    description="Development processes and technical workflows",
                ),
            ],
            "rachel": [
                VisualTemplate(
                    visual_type=VisualType.DESIGN_SYSTEM,
                    magic_prompt_prefix="Create design system visualization showing",
                    style="design_system_consistency",
                    persona="rachel",
                    description="Component libraries and design pattern relationships",
                ),
                VisualTemplate(
                    visual_type=VisualType.USER_FLOW,
                    magic_prompt_prefix="Create user experience flow diagram for",
                    style="user_centered_design",
                    persona="rachel",
                    description="User journeys and interaction patterns",
                ),
                VisualTemplate(
                    visual_type=VisualType.PROCESS_FLOW,
                    magic_prompt_prefix="Create design process workflow showing",
                    style="design_methodology",
                    persona="rachel",
                    description="Design methodology and cross-functional collaboration",
                ),
            ],
            "camille": [
                VisualTemplate(
                    visual_type=VisualType.STRATEGIC_ROADMAP,
                    magic_prompt_prefix="Create strategic technology roadmap for",
                    style="executive_technology_presentation",
                    persona="camille",
                    description="Technology strategy and competitive positioning",
                ),
                VisualTemplate(
                    visual_type=VisualType.ARCHITECTURE_DIAGRAM,
                    magic_prompt_prefix="Create strategic technology architecture showing",
                    style="executive_technical_documentation",
                    persona="camille",
                    description="High-level technology ecosystem and integration",
                ),
                VisualTemplate(
                    visual_type=VisualType.BUSINESS_CHART,
                    magic_prompt_prefix="Create strategic analysis chart showing",
                    style="executive_presentation",
                    persona="camille",
                    description="Technology investment and competitive analysis",
                ),
            ],
            "alvaro": [
                VisualTemplate(
                    visual_type=VisualType.BUSINESS_CHART,
                    magic_prompt_prefix="Create ROI analysis dashboard showing",
                    style="business_intelligence",
                    persona="alvaro",
                    description="Investment returns and business value metrics",
                ),
                VisualTemplate(
                    visual_type=VisualType.STRATEGIC_ROADMAP,
                    magic_prompt_prefix="Create business strategy roadmap for",
                    style="executive_business_presentation",
                    persona="alvaro",
                    description="Business development and market positioning",
                ),
                VisualTemplate(
                    visual_type=VisualType.PROCESS_FLOW,
                    magic_prompt_prefix="Create business process diagram showing",
                    style="business_process_optimization",
                    persona="alvaro",
                    description="Business workflows and value stream optimization",
                ),
            ],
        }

    def _initialize_visual_keywords(self) -> Dict[VisualType, List[str]]:
        """Initialize visual type detection keywords"""
        return {
            VisualType.ORG_CHART: [
                "org chart",
                "organizational chart",
                "team structure",
                "reporting structure",
                "hierarchy",
                "organization",
            ],
            VisualType.ARCHITECTURE_DIAGRAM: [
                "architecture diagram",
                "system architecture",
                "technical architecture",
                "platform architecture",
                "infrastructure diagram",
            ],
            VisualType.DESIGN_SYSTEM: [
                "design system",
                "component library",
                "style guide",
                "design patterns",
                "ui components",
            ],
            VisualType.BUSINESS_CHART: [
                "chart",
                "dashboard",
                "metrics",
                "roi",
                "analysis",
                "business chart",
                "performance chart",
            ],
            VisualType.STRATEGIC_ROADMAP: [
                "roadmap",
                "strategy",
                "timeline",
                "phases",
                "strategic plan",
                "initiative roadmap",
            ],
            VisualType.USER_FLOW: [
                "user flow",
                "user journey",
                "wireframe",
                "mockup",
                "user experience",
                "interaction flow",
            ],
            VisualType.PROCESS_FLOW: [
                "process flow",
                "workflow",
                "process diagram",
                "flowchart",
                "process map",
            ],
            VisualType.SYSTEM_DESIGN: [
                "system design",
                "technical design",
                "platform design",
                "integration diagram",
                "service architecture",
            ],
        }

    def detect_visual_request(self, user_input: str) -> bool:
        """
        PHASE 12: Detect if user input requests visual enhancement

        Returns True for any visual-related keywords to trigger Magic MCP
        """
        input_lower = user_input.lower()

        # Check all visual keywords across all types
        for visual_type, keywords in self.visual_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                return True

        # Additional generic visual keywords
        generic_visual_keywords = [
            "diagram",
            "chart",
            "visual",
            "draw",
            "show me",
            "visualize",
            "create",
            "layout",
            "sketch",
            "blueprint",
            "presentation",
        ]

        return any(keyword in input_lower for keyword in generic_visual_keywords)

    def get_template_for_persona_and_request(
        self, persona: str, user_input: str
    ) -> Optional[VisualTemplate]:
        """
        PHASE 12: Get best visual template for persona and request

        Args:
            persona: Persona name
            user_input: User's visual request

        Returns:
            Best matching visual template or None
        """
        persona_templates = self.persona_templates.get(persona, [])
        if not persona_templates:
            # Fallback to generic template for unknown personas
            return self._get_fallback_template(user_input)

        input_lower = user_input.lower()

        # Find best matching template based on visual type keywords
        for template in persona_templates:
            template_keywords = self.visual_keywords.get(template.visual_type, [])
            if any(keyword in input_lower for keyword in template_keywords):
                return template

        # Return first template as default for this persona
        return persona_templates[0]

    def _get_fallback_template(self, user_input: str) -> VisualTemplate:
        """Get fallback template for unknown personas"""
        return VisualTemplate(
            visual_type=VisualType.PROCESS_FLOW,
            magic_prompt_prefix="Create professional diagram showing",
            style="professional_documentation",
            persona="default",
            description="General purpose visual enhancement",
        )

    def get_magic_mcp_enhancement_context(
        self, persona: str, user_input: str
    ) -> Dict[str, Any]:
        """
        PHASE 12: Get Magic MCP enhancement context for persona and request

        Returns context dictionary for Magic MCP server with persona-specific
        template and style preferences.
        """
        template = self.get_template_for_persona_and_request(persona, user_input)

        if not template:
            template = self._get_fallback_template(user_input)

        return {
            "persona": persona,
            "visual_type": template.visual_type.value,
            "magic_prompt_prefix": template.magic_prompt_prefix,
            "style": template.style,
            "description": template.description,
            "enhancement_type": "visual_generation",
            "server": "magic",
            "processing_time_target": 0.05,  # <50ms requirement
        }

    def get_available_templates_for_persona(self, persona: str) -> List[VisualTemplate]:
        """Get all available visual templates for a persona"""
        return self.persona_templates.get(persona, [])

    def get_supported_visual_types(self) -> List[VisualType]:
        """Get all supported visual types"""
        return list(VisualType)

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Delegates to visual template operations
        """
        if operation == "get_template":
            return self.get_template_for_context(*args, **kwargs)
        elif operation == "detect_visual_intent":
            return self.detect_visual_intent(*args, **kwargs)
        elif operation == "get_persona_templates":
            return self.get_available_templates_for_persona(*args, **kwargs)
        elif operation == "get_visual_types":
            return self.get_supported_visual_types(*args, **kwargs)
        else:
            self.logger.warning(f"Unknown visual template operation: {operation}")
            return None
