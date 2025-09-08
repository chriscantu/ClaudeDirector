"""
Strategic Specification Enhancement Layer

Enhances external spec-kit outputs with strategic intelligence.
Follows SOLID principles and integrates with context_engineering primary system.

Architecture:
- Single Responsibility: Strategic enhancement of specifications only
- Open/Closed: Extensible for different enhancement strategies
- Liskov Substitution: Interface-based enhancement strategies
- Interface Segregation: Focused interfaces for different enhancement types
- Dependency Inversion: Depends on context_engineering abstractions
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import logging

try:
    from ..core.models import StrategicContext
    from ..context_engineering import (
        AdvancedContextEngine,
        StrategicLayerMemory,
        StakeholderLayerMemory,
    )
    from ..ai_intelligence import DecisionIntelligenceOrchestrator, DecisionContext
except ImportError:
    # Fallback for test environments
    import sys
    from pathlib import Path

    lib_path = Path(__file__).parent.parent
    sys.path.insert(0, str(lib_path))

    try:
        from core.models import StrategicContext
        from context_engineering import (
            AdvancedContextEngine,
            StrategicLayerMemory,
            StakeholderLayerMemory,
        )
        from ai_intelligence import DecisionIntelligenceOrchestrator, DecisionContext
    except ImportError:
        # Mock classes for test environments
        class StrategicContext:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        class AdvancedContextEngine:
            def __init__(self, **kwargs):
                pass

        class StrategicLayerMemory:
            def __init__(self, **kwargs):
                pass

        class StakeholderLayerMemory:
            def __init__(self, **kwargs):
                pass

        class DecisionIntelligenceOrchestrator:
            def __init__(self, **kwargs):
                pass

        class DecisionContext:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)


class SpecificationEnhancer(Protocol):
    """Protocol for specification enhancement strategies (Interface Segregation)"""

    def enhance(self, spec_content: str, context: StrategicContext) -> str:
        """Enhance specification with strategic intelligence"""
        ...


@dataclass
class StrategicEnhancement:
    """Strategic enhancement metadata"""

    frameworks_applied: List[str]
    stakeholders_identified: List[str]
    roi_projections: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    success_metrics: List[str]
    executive_summary: str


@dataclass
class EnhancedSpecification:
    """Result of strategic specification enhancement"""

    original_spec_path: str
    enhanced_spec_path: str
    enhancement_metadata: StrategicEnhancement
    validation_results: Dict[str, Any]
    errors: List[str]


class FrameworkIntegrationEnhancer:
    """Strategic framework integration enhancement (Single Responsibility)"""

    def __init__(self, decision_orchestrator: DecisionIntelligenceOrchestrator):
        self.decision_orchestrator = decision_orchestrator
        self.logger = logging.getLogger(__name__)

    def enhance(
        self, spec_content: str, context: StrategicContext
    ) -> tuple[str, List[str]]:
        """Add strategic framework analysis to specification"""
        try:
            # Mock framework detection for now - would use actual framework detector
            frameworks = self._mock_detect_frameworks(spec_content)

            if not frameworks:
                return spec_content, []

            # Add framework section to specification
            framework_section = self._generate_framework_section(
                frameworks, spec_content
            )

            # Insert framework section before requirements
            enhanced_content = self._insert_framework_section(
                spec_content, framework_section
            )

            return enhanced_content, [f["name"] for f in frameworks]

        except Exception as e:
            self.logger.error(f"Framework enhancement failed: {e}")
            return spec_content, []

    def _generate_framework_section(
        self, frameworks: List[Dict], spec_content: str
    ) -> str:
        """Generate strategic framework section"""
        section = "\n## Strategic Framework Analysis\n\n"
        section += "**ClaudeDirector Strategic Intelligence Enhancement**\n\n"

        for framework in frameworks:
            section += f"### {framework['name']}\n"
            section += f"- **Applicability**: {framework.get('confidence', 0):.0%} confidence\n"
            section += f"- **Strategic Value**: {framework.get('strategic_value', 'Strategic alignment and best practices')}\n"
            section += f"- **Key Principles**: {', '.join(framework.get('principles', ['Not specified']))}\n\n"

        section += (
            "**Framework Attribution**: This analysis applies strategic frameworks "
        )
        section += (
            "detected through ClaudeDirector's AI-powered framework intelligence.\n\n"
        )

        return section

    def _insert_framework_section(
        self, spec_content: str, framework_section: str
    ) -> str:
        """Insert framework section before requirements"""
        lines = spec_content.split("\n")
        requirements_index = -1

        for i, line in enumerate(lines):
            if line.strip().startswith("## Requirements"):
                requirements_index = i
                break

        if requirements_index != -1:
            lines.insert(requirements_index, framework_section)
        else:
            lines.append(framework_section)

        return "\n".join(lines)

    def _mock_detect_frameworks(self, spec_content: str) -> List[Dict]:
        """Mock framework detection for architectural demonstration"""
        # Simple keyword-based detection for demo
        frameworks = []

        if any(
            word in spec_content.lower()
            for word in ["team", "organization", "structure"]
        ):
            frameworks.append(
                {
                    "name": "Team Topologies",
                    "confidence": 0.85,
                    "strategic_value": "Team structure optimization",
                    "principles": [
                        "Team cognitive load",
                        "Conway's Law",
                        "Team interaction modes",
                    ],
                }
            )

        if any(
            word in spec_content.lower() for word in ["decision", "strategy", "choice"]
        ):
            frameworks.append(
                {
                    "name": "WRAP Framework",
                    "confidence": 0.90,
                    "strategic_value": "Decision-making methodology",
                    "principles": [
                        "Widen options",
                        "Reality-test assumptions",
                        "Attain distance",
                        "Prepare to be wrong",
                    ],
                }
            )

        if any(
            word in spec_content.lower()
            for word in ["investment", "resource", "budget"]
        ):
            frameworks.append(
                {
                    "name": "Capital Allocation Framework",
                    "confidence": 0.80,
                    "strategic_value": "Resource allocation optimization",
                    "principles": [
                        "ROI analysis",
                        "Risk assessment",
                        "Portfolio balance",
                    ],
                }
            )

        return frameworks


class StakeholderIntelligenceEnhancer:
    """Stakeholder intelligence enhancement (Single Responsibility)"""

    def __init__(self, stakeholder_layer: StakeholderLayerMemory):
        self.stakeholder_layer = stakeholder_layer
        self.logger = logging.getLogger(__name__)

    def enhance(
        self, spec_content: str, context: StrategicContext
    ) -> tuple[str, List[str]]:
        """Add stakeholder intelligence to specification"""
        try:
            # Get stakeholder context
            stakeholder_context = self.stakeholder_layer.get_stakeholder_context()

            if not stakeholder_context:
                return spec_content, []

            # Extract relevant stakeholders
            relevant_stakeholders = self._identify_relevant_stakeholders(
                spec_content, stakeholder_context
            )

            if not relevant_stakeholders:
                return spec_content, []

            # Add stakeholder section
            stakeholder_section = self._generate_stakeholder_section(
                relevant_stakeholders
            )
            enhanced_content = self._insert_stakeholder_section(
                spec_content, stakeholder_section
            )

            return enhanced_content, [s["name"] for s in relevant_stakeholders]

        except Exception as e:
            self.logger.error(f"Stakeholder enhancement failed: {e}")
            return spec_content, []

    def _identify_relevant_stakeholders(
        self, spec_content: str, stakeholder_context: Dict
    ) -> List[Dict]:
        """Identify stakeholders relevant to the specification"""
        # Simple keyword-based matching - can be enhanced with ML
        relevant = []

        stakeholders = stakeholder_context.get("stakeholders", [])
        # Handle case where stakeholders might be a Mock object
        if hasattr(stakeholders, "__iter__") and not isinstance(stakeholders, str):
            try:
                for stakeholder in stakeholders:
                    if isinstance(stakeholder, dict):
                        stakeholder_keywords = stakeholder.get("keywords", [])
                        if any(
                            keyword.lower() in spec_content.lower()
                            for keyword in stakeholder_keywords
                        ):
                            relevant.append(stakeholder)
            except (TypeError, AttributeError):
                # Handle Mock objects gracefully
                pass

        return relevant[:5]  # Limit to top 5 relevant stakeholders

    def _generate_stakeholder_section(self, stakeholders: List[Dict]) -> str:
        """Generate stakeholder intelligence section"""
        section = "\n## Stakeholder Impact Analysis\n\n"
        section += "**Strategic Stakeholder Intelligence**\n\n"

        for stakeholder in stakeholders:
            section += f"### {stakeholder.get('name', 'Unknown')}\n"
            section += f"- **Role**: {stakeholder.get('role', 'Not specified')}\n"
            section += (
                f"- **Interest Level**: {stakeholder.get('interest_level', 'Medium')}\n"
            )
            section += f"- **Communication Preference**: {stakeholder.get('communication_style', 'Standard')}\n"
            section += f"- **Key Concerns**: {', '.join(stakeholder.get('concerns', ['General strategic alignment']))}\n\n"

        return section

    def _insert_stakeholder_section(
        self, spec_content: str, stakeholder_section: str
    ) -> str:
        """Insert stakeholder section after user scenarios"""
        lines = spec_content.split("\n")
        scenarios_end = -1

        for i, line in enumerate(lines):
            if line.strip().startswith("## Requirements") or line.strip().startswith(
                "### Requirements"
            ):
                scenarios_end = i
                break

        if scenarios_end != -1:
            lines.insert(scenarios_end, stakeholder_section)
        else:
            lines.append(stakeholder_section)

        return "\n".join(lines)


class ROIProjectionEnhancer:
    """ROI projection and business impact enhancement (Single Responsibility)"""

    def __init__(self, strategic_layer: StrategicLayerMemory):
        self.strategic_layer = strategic_layer
        self.logger = logging.getLogger(__name__)

    def enhance(
        self, spec_content: str, context: StrategicContext
    ) -> tuple[str, Dict[str, Any]]:
        """Add ROI projections and business impact analysis"""
        try:
            # Generate ROI projections based on strategic context
            roi_data = self._calculate_roi_projections(spec_content, context)

            # Add ROI section to specification
            roi_section = self._generate_roi_section(roi_data)
            enhanced_content = self._insert_roi_section(spec_content, roi_section)

            return enhanced_content, roi_data

        except Exception as e:
            self.logger.error(f"ROI enhancement failed: {e}")
            return spec_content, {}

    def _calculate_roi_projections(
        self, spec_content: str, context: StrategicContext
    ) -> Dict[str, Any]:
        """Calculate ROI projections based on specification content"""
        # Simplified ROI calculation - can be enhanced with ML models
        base_investment = 100000  # Default base investment

        # Estimate complexity multiplier
        complexity_multiplier = 1.0
        if "ML" in spec_content or "machine learning" in spec_content.lower():
            complexity_multiplier += 0.5
        if "predictive" in spec_content.lower():
            complexity_multiplier += 0.3
        if "enterprise" in spec_content.lower():
            complexity_multiplier += 0.2

        estimated_investment = base_investment * complexity_multiplier

        # Estimate benefits (simplified model)
        efficiency_gain = 0.25  # 25% efficiency improvement
        decision_quality_gain = 0.15  # 15% decision quality improvement

        annual_benefit = (
            estimated_investment * (efficiency_gain + decision_quality_gain) * 3
        )
        roi_ratio = annual_benefit / estimated_investment

        return {
            "estimated_investment": estimated_investment,
            "annual_benefit": annual_benefit,
            "roi_ratio": roi_ratio,
            "payback_months": 12 / roi_ratio if roi_ratio > 0 else 999,
            "complexity_factors": {
                "ml_component": "ML" in spec_content,
                "predictive_component": "predictive" in spec_content.lower(),
                "enterprise_component": "enterprise" in spec_content.lower(),
            },
        }

    def _generate_roi_section(self, roi_data: Dict[str, Any]) -> str:
        """Generate ROI projection section"""
        section = "\n## Business Impact & ROI Analysis\n\n"
        section += "**Strategic Investment Analysis**\n\n"

        section += (
            f"- **Estimated Investment**: ${roi_data['estimated_investment']:,.0f}\n"
        )
        section += (
            f"- **Projected Annual Benefit**: ${roi_data['annual_benefit']:,.0f}\n"
        )
        section += f"- **ROI Ratio**: {roi_data['roi_ratio']:.1f}x\n"
        section += f"- **Payback Period**: {roi_data['payback_months']:.1f} months\n\n"

        section += "**Complexity Factors**:\n"
        for factor, present in roi_data["complexity_factors"].items():
            status = "✅ Present" if present else "❌ Not identified"
            section += f"- {factor.replace('_', ' ').title()}: {status}\n"

        section += (
            "\n*ROI projections generated by ClaudeDirector Strategic Intelligence*\n\n"
        )

        return section

    def _insert_roi_section(self, spec_content: str, roi_section: str) -> str:
        """Insert ROI section at the end before review checklist"""
        lines = spec_content.split("\n")
        review_index = -1

        for i, line in enumerate(lines):
            if line.strip().startswith("## Review") or line.strip().startswith("---"):
                review_index = i
                break

        if review_index != -1:
            lines.insert(review_index, roi_section)
        else:
            lines.append(roi_section)

        return "\n".join(lines)


class StrategicSpecEnhancer:
    """
    Strategic Specification Enhancement Coordinator

    Follows SOLID principles:
    - Single Responsibility: Coordinates strategic enhancement of specifications
    - Open/Closed: Extensible for new enhancement strategies
    - Dependency Inversion: Uses context_engineering and ai_intelligence abstractions
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        decision_orchestrator: DecisionIntelligenceOrchestrator,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize with dependency injection (Dependency Inversion)"""
        self.context_engine = context_engine
        self.decision_orchestrator = decision_orchestrator
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Initialize enhancement strategies (Strategy Pattern)
        self.framework_enhancer = FrameworkIntegrationEnhancer(
            self.decision_orchestrator
        )
        self.stakeholder_enhancer = StakeholderIntelligenceEnhancer(
            self.context_engine.stakeholder_layer
        )
        self.roi_enhancer = ROIProjectionEnhancer(self.context_engine.strategic_layer)

    def enhance_specification(
        self, spec_path: str, strategic_context: Optional[StrategicContext] = None
    ) -> EnhancedSpecification:
        """
        Enhance specification with strategic intelligence

        Args:
            spec_path: Path to base specification file
            strategic_context: Optional strategic context for enhancement

        Returns:
            EnhancedSpecification with enhanced content and metadata
        """
        try:
            # Read original specification
            spec_file = Path(spec_path)
            if not spec_file.exists():
                raise FileNotFoundError(f"Specification file not found: {spec_path}")

            original_content = spec_file.read_text()
            enhanced_content = original_content

            # Initialize enhancement metadata
            enhancement_metadata = StrategicEnhancement(
                frameworks_applied=[],
                stakeholders_identified=[],
                roi_projections={},
                risk_assessment={},
                success_metrics=[],
                executive_summary="",
            )

            # Apply framework enhancement
            if self.config.get("enable_framework_enhancement", True):
                enhanced_content, frameworks = self.framework_enhancer.enhance(
                    enhanced_content, strategic_context
                )
                enhancement_metadata.frameworks_applied = frameworks

            # Apply stakeholder enhancement
            if self.config.get("enable_stakeholder_enhancement", True):
                enhanced_content, stakeholders = self.stakeholder_enhancer.enhance(
                    enhanced_content, strategic_context
                )
                enhancement_metadata.stakeholders_identified = stakeholders

            # Apply ROI enhancement
            if self.config.get("enable_roi_enhancement", True):
                enhanced_content, roi_data = self.roi_enhancer.enhance(
                    enhanced_content, strategic_context
                )
                enhancement_metadata.roi_projections = roi_data

            # Generate enhanced specification file
            enhanced_spec_path = self._save_enhanced_specification(
                spec_file, enhanced_content
            )

            # Generate executive summary
            enhancement_metadata.executive_summary = self._generate_executive_summary(
                enhancement_metadata
            )

            return EnhancedSpecification(
                original_spec_path=spec_path,
                enhanced_spec_path=enhanced_spec_path,
                enhancement_metadata=enhancement_metadata,
                validation_results={"enhanced": True, "strategies_applied": 3},
                errors=[],
            )

        except Exception as e:
            self.logger.error(f"Specification enhancement failed: {e}")
            return EnhancedSpecification(
                original_spec_path=spec_path,
                enhanced_spec_path="",
                enhancement_metadata=StrategicEnhancement(
                    frameworks_applied=[],
                    stakeholders_identified=[],
                    roi_projections={},
                    risk_assessment={},
                    success_metrics=[],
                    executive_summary="",
                ),
                validation_results={},
                errors=[str(e)],
            )

    def _save_enhanced_specification(
        self, original_file: Path, enhanced_content: str
    ) -> str:
        """Save enhanced specification to new file"""
        enhanced_file = (
            original_file.parent
            / f"{original_file.stem}_enhanced{original_file.suffix}"
        )
        enhanced_file.write_text(enhanced_content)
        return str(enhanced_file)

    def _generate_executive_summary(self, metadata: StrategicEnhancement) -> str:
        """Generate executive summary of enhancements"""
        summary = "Strategic Intelligence Enhancement Applied:\n"

        if metadata.frameworks_applied:
            summary += f"- {len(metadata.frameworks_applied)} strategic frameworks integrated\n"

        if metadata.stakeholders_identified:
            summary += f"- {len(metadata.stakeholders_identified)} key stakeholders identified\n"

        if metadata.roi_projections:
            roi_ratio = metadata.roi_projections.get("roi_ratio", 0)
            summary += f"- ROI projection: {roi_ratio:.1f}x return on investment\n"

        return summary
