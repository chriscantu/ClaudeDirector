#!/usr/bin/env python3
"""
Director Profile Manager - P1 Organizational Leverage Intelligence
Flexible, configuration-driven system for different director contexts
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import yaml
from pathlib import Path


class DirectorRole(Enum):
    PLATFORM_DIRECTOR = "platform_director"
    BACKEND_DIRECTOR = "backend_director"
    PRODUCT_DIRECTOR = "product_director"
    DESIGN_DIRECTOR = "design_director"
    CUSTOM = "custom"


@dataclass
class MetricDefinition:
    """Configurable metric definition"""

    name: str
    enabled: bool
    weight: float
    target_value: float
    measurement_method: str
    annual_value_per_percent: Optional[float] = None


@dataclass
class InvestmentCategory:
    """Configurable investment tracking"""

    name: str
    enabled: bool
    priority_weight: float
    roi_calculation_method: str
    measurement_period_months: int
    success_criteria: List[Dict[str, Any]]


@dataclass
class DirectorProfile:
    """Flexible director profile configuration"""

    role_title: str
    primary_focus: str
    strategic_priorities: List[str]
    success_metrics: List[str]
    enabled_domains: Dict[str, MetricDefinition]
    investment_categories: Dict[str, InvestmentCategory]
    dashboard_config: Dict[str, Any]
    integration_preferences: Dict[str, bool]


class DirectorProfileManager:
    """Manages flexible director profile configurations"""

    def __init__(self, config_path: str = "config/p1_organizational_intelligence.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_configuration()
        self.current_profile = self._initialize_profile()

    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {self.config_path}")

    def _initialize_profile(self) -> DirectorProfile:
        """Initialize director profile from configuration"""
        profile_config = self.config.get("director_profile", {})
        profile_type = profile_config.get("profile_type", "custom")

        if profile_type == "custom":
            return self._create_custom_profile(profile_config.get("custom_profile", {}))
        else:
            return self._create_preset_profile(profile_type)

    def _create_custom_profile(self, custom_config: Dict[str, Any]) -> DirectorProfile:
        """Create profile from custom configuration"""
        org_intel = self.config.get("organizational_intelligence", {})

        # Parse enabled domains with metrics
        enabled_domains = {}
        velocity_domains = org_intel.get("velocity_tracking", {}).get(
            "measurement_domains", {}
        )

        for domain_name, domain_config in velocity_domains.items():
            if domain_config.get("enabled", False):
                metrics = []
                for metric_name in domain_config.get("metrics", []):
                    metric = MetricDefinition(
                        name=metric_name,
                        enabled=True,
                        weight=domain_config.get("weight", 0.0),
                        target_value=domain_config.get("targets", {}).get(
                            metric_name.split("_")[0], 0.0
                        ),
                        measurement_method=domain_name,
                    )
                    metrics.append(metric)

                enabled_domains[domain_name] = metrics

        # Parse investment categories
        investment_categories = {}
        investment_config = org_intel.get("investment_intelligence", {}).get(
            "investment_categories", {}
        )

        for category_name, category_config in investment_config.items():
            if category_config.get("enabled", False):
                investment = InvestmentCategory(
                    name=category_name,
                    enabled=True,
                    priority_weight=category_config.get("priority_weight", 0.0),
                    roi_calculation_method=category_config.get(
                        "roi_calculation_method", "default"
                    ),
                    measurement_period_months=category_config.get(
                        "measurement_period_months", 6
                    ),
                    success_criteria=category_config.get("success_criteria", []),
                )
                investment_categories[category_name] = investment

        return DirectorProfile(
            role_title=custom_config.get("role_title", "Director"),
            primary_focus=custom_config.get("primary_focus", ""),
            strategic_priorities=custom_config.get("strategic_priorities", []),
            success_metrics=custom_config.get("success_metrics", []),
            enabled_domains=enabled_domains,
            investment_categories=investment_categories,
            dashboard_config=self.config.get("dashboard", {}),
            integration_preferences=self._extract_integration_preferences(),
        )

    def _create_preset_profile(self, profile_type: str) -> DirectorProfile:
        """Create profile from preset configuration"""
        preset_config = self.config.get("preset_profiles", {}).get(profile_type, {})

        if not preset_config:
            raise ValueError(f"Unknown preset profile type: {profile_type}")

        # Build profile based on preset focus areas
        focus_areas = preset_config.get("focus_areas", [])
        enabled_domains = self._build_domains_from_focus_areas(focus_areas)

        return DirectorProfile(
            role_title=f"{profile_type.replace('_', ' ').title()}",
            primary_focus=", ".join(focus_areas),
            strategic_priorities=preset_config.get("strategic_priorities", []),
            success_metrics=preset_config.get("key_metrics", []),
            enabled_domains=enabled_domains,
            investment_categories=self._build_investments_from_focus_areas(focus_areas),
            dashboard_config={
                "layout": preset_config.get("dashboard_layout", "default")
            },
            integration_preferences=self._extract_integration_preferences(),
        )

    def _build_domains_from_focus_areas(
        self, focus_areas: List[str]
    ) -> Dict[str, List[MetricDefinition]]:
        """Build enabled domains based on focus areas"""
        enabled_domains = {}
        org_intel = self.config.get("organizational_intelligence", {})
        velocity_domains = org_intel.get("velocity_tracking", {}).get(
            "measurement_domains", {}
        )

        for focus_area in focus_areas:
            if focus_area in velocity_domains:
                domain_config = velocity_domains[focus_area]
                metrics = []

                for metric_name in domain_config.get("metrics", []):
                    metric = MetricDefinition(
                        name=metric_name,
                        enabled=True,
                        weight=domain_config.get("weight", 0.0),
                        target_value=domain_config.get("targets", {}).get(
                            metric_name.split("_")[0], 0.0
                        ),
                        measurement_method=focus_area,
                    )
                    metrics.append(metric)

                enabled_domains[focus_area] = metrics

        return enabled_domains

    def _build_investments_from_focus_areas(
        self, focus_areas: List[str]
    ) -> Dict[str, InvestmentCategory]:
        """Build investment categories based on focus areas"""
        investment_categories = {}
        investment_config = (
            self.config.get("organizational_intelligence", {})
            .get("investment_intelligence", {})
            .get("investment_categories", {})
        )

        # Map focus areas to investment categories
        focus_to_investment_mapping = {
            "platform_adoption": "platform_infrastructure",
            "design_system_leverage": "design_system_enhancement",
            "developer_experience": "developer_experience",
            "api_service_efficiency": "platform_infrastructure",
            "feature_delivery_impact": "cross_team_tooling",
        }

        for focus_area in focus_areas:
            investment_key = focus_to_investment_mapping.get(focus_area)
            if investment_key and investment_key in investment_config:
                category_config = investment_config[investment_key]
                investment = InvestmentCategory(
                    name=investment_key,
                    enabled=True,
                    priority_weight=category_config.get("priority_weight", 0.0),
                    roi_calculation_method=category_config.get(
                        "roi_calculation_method", "default"
                    ),
                    measurement_period_months=category_config.get(
                        "measurement_period_months", 6
                    ),
                    success_criteria=category_config.get("success_criteria", []),
                )
                investment_categories[investment_key] = investment

        return investment_categories

    def _extract_integration_preferences(self) -> Dict[str, bool]:
        """Extract integration preferences from configuration"""
        integrations = self.config.get("integrations", {})
        preferences = {}

        for category, tools in integrations.items():
            for tool_name, tool_config in tools.items():
                preferences[f"{category}_{tool_name}"] = tool_config.get(
                    "enabled", False
                )

        return preferences

    def customize_profile(
        self,
        role_title: Optional[str] = None,
        enable_domains: Optional[List[str]] = None,
        disable_domains: Optional[List[str]] = None,
        update_weights: Optional[Dict[str, float]] = None,
        update_targets: Optional[Dict[str, float]] = None,
    ) -> None:
        """Customize the current profile dynamically"""

        if role_title:
            self.current_profile.role_title = role_title

        if enable_domains:
            # Add domains from configuration
            org_intel = self.config.get("organizational_intelligence", {})
            velocity_domains = org_intel.get("velocity_tracking", {}).get(
                "measurement_domains", {}
            )

            for domain_name in enable_domains:
                if (
                    domain_name in velocity_domains
                    and domain_name not in self.current_profile.enabled_domains
                ):
                    domain_config = velocity_domains[domain_name]
                    metrics = []

                    for metric_name in domain_config.get("metrics", []):
                        metric = MetricDefinition(
                            name=metric_name,
                            enabled=True,
                            weight=domain_config.get("weight", 0.0),
                            target_value=domain_config.get("targets", {}).get(
                                metric_name.split("_")[0], 0.0
                            ),
                            measurement_method=domain_name,
                        )
                        metrics.append(metric)

                    self.current_profile.enabled_domains[domain_name] = metrics

        if disable_domains:
            for domain_name in disable_domains:
                self.current_profile.enabled_domains.pop(domain_name, None)

        if update_weights:
            for domain_name, new_weight in update_weights.items():
                if domain_name in self.current_profile.enabled_domains:
                    for metric in self.current_profile.enabled_domains[domain_name]:
                        metric.weight = new_weight

        if update_targets:
            for domain_name, new_target in update_targets.items():
                if domain_name in self.current_profile.enabled_domains:
                    for metric in self.current_profile.enabled_domains[domain_name]:
                        metric.target_value = new_target

    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration for current profile"""
        return self.current_profile.dashboard_config

    def get_enabled_metrics(self) -> Dict[str, List[MetricDefinition]]:
        """Get all enabled metrics for current profile"""
        return self.current_profile.enabled_domains

    def get_investment_priorities(self) -> Dict[str, InvestmentCategory]:
        """Get investment priorities for current profile"""
        return self.current_profile.investment_categories

    def calculate_organizational_impact_score(
        self, current_metrics: Dict[str, float]
    ) -> float:
        """Calculate overall organizational impact score based on current profile"""
        total_weighted_score = 0.0
        total_weight = 0.0

        for domain_name, metrics in self.current_profile.enabled_domains.items():
            for metric in metrics:
                if metric.name in current_metrics:
                    # Calculate metric achievement percentage
                    current_value = current_metrics[metric.name]
                    achievement_ratio = (
                        min(current_value / metric.target_value, 1.0)
                        if metric.target_value > 0
                        else 0.0
                    )

                    weighted_score = achievement_ratio * metric.weight
                    total_weighted_score += weighted_score
                    total_weight += metric.weight

        return total_weighted_score / total_weight if total_weight > 0 else 0.0

    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary based on current profile"""
        return {
            "director_profile": {
                "role": self.current_profile.role_title,
                "focus": self.current_profile.primary_focus,
                "strategic_priorities": self.current_profile.strategic_priorities,
            },
            "enabled_domains": list(self.current_profile.enabled_domains.keys()),
            "investment_priorities": [
                {
                    "category": inv.name,
                    "priority_weight": inv.priority_weight,
                    "measurement_period": inv.measurement_period_months,
                }
                for inv in self.current_profile.investment_categories.values()
            ],
            "success_metrics": self.current_profile.success_metrics,
        }


# Example usage for your design system context
def create_platform_director_example():
    """Example of how you would configure for your specific context"""

    profile_manager = DirectorProfileManager()

    # Customize for your specific needs
    profile_manager.customize_profile(
        role_title="Director of Engineering - UI Foundation",
        enable_domains=[
            "design_system_leverage",
            "platform_adoption",
            "developer_experience",
        ],
        update_weights={
            "design_system_leverage": 0.35,  # Higher weight for your context
            "platform_adoption": 0.30,
            "developer_experience": 0.25,
        },
        update_targets={
            "design_system_leverage": 0.85,  # 85% design system consistency
            "platform_adoption": 0.80,  # 80% platform adoption
            "developer_experience": 4.5,  # 4.5/5 satisfaction score
        },
    )

    return profile_manager


if __name__ == "__main__":
    # Test the configuration system
    manager = create_platform_director_example()
    summary = manager.generate_executive_summary()
    print("Director Profile Summary:")
    print(yaml.dump(summary, indent=2))
