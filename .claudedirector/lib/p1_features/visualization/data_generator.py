#!/usr/bin/env python3
"""
Data Generator for P1.1 Visualization
Follows Single Responsibility Principle - focused only on data generation
"""

from typing import Dict, List, Any
from .interfaces import (
    DataGeneratorInterface,
    ConfigManagerInterface,
    OrganizationalData,
)
from .config_manager import visualization_config


class SampleDataGenerator(DataGeneratorInterface):
    """
    Generates sample data for visualization demonstration
    Follows SRP - only responsible for data generation
    """

    def __init__(self, config_manager: ConfigManagerInterface = None):
        self.config = config_manager or visualization_config

    def generate_sample_data(self, profile_manager: Any) -> OrganizationalData:
        """
        Generate realistic sample data for demonstration
        All values now come from configuration (DRY compliance)
        """
        # Get sample metrics from config
        sample_metrics = self._get_sample_metrics()

        # Calculate impact score using profile manager
        impact_score = self._calculate_impact_score(profile_manager, sample_metrics)

        # Get the actual profile
        profile = (
            profile_manager.current_profile
            if hasattr(profile_manager, "current_profile")
            else profile_manager
        )

        # Generate domain data
        domains = self._generate_domain_data(profile)

        # Generate trend data
        trends = self._generate_trend_data()

        # Generate investment data
        investments = self._generate_investment_data(profile)

        return OrganizationalData(
            impact_score=max(
                impact_score, self.config.sample_data.minimum_impact_score
            ),
            domains=domains,
            trends=trends,
            investments=investments,
            sample_metrics=sample_metrics,
        )

    def collect_real_data(self, profile_manager: Any) -> OrganizationalData:
        """
        Collect real organizational data (placeholder for future integration)
        In production, this would integrate with actual data sources
        """
        # For now, return sample data
        # Mock implementation - integrate real data sources when available
        return self.generate_sample_data(profile_manager)

    def _get_sample_metrics(self) -> Dict[str, float]:
        """Get sample metrics from configuration"""
        return self.config.sample_data.metrics.copy()

    def _calculate_impact_score(
        self, profile_manager: Any, metrics: Dict[str, float]
    ) -> float:
        """Calculate impact score using profile manager"""
        # This delegates to the profile manager's calculation logic
        if hasattr(profile_manager, "calculate_organizational_impact_score"):
            return profile_manager.calculate_organizational_impact_score(metrics)
        else:
            # Fallback calculation if method not available
            return sum(metrics.values()) / len(metrics) if metrics else 0.0

    def _generate_domain_data(self, profile: Any) -> List[Dict[str, Any]]:
        """Generate domain performance data from profile and configuration"""
        domain_data = []

        if hasattr(profile, "enabled_domains"):
            for domain_name, metrics in profile.enabled_domains.items():
                if metrics:
                    weight = metrics[0].weight
                    target = (
                        metrics[0].target_value
                        if metrics[0].target_value > 0
                        else self._get_default_target()
                    )

                    # Get performance from configuration based on domain type
                    current = self._get_domain_current_performance(domain_name)

                    domain_data.append(
                        {
                            "name": domain_name,
                            "current": current,
                            "target": target,
                            "weight": weight,
                        }
                    )

        return domain_data

    def _get_default_target(self) -> float:
        """Get default target from configuration"""
        return self.config.sample_data.domain_performance["design_domains"][
            "default_target"
        ]

    def _get_domain_current_performance(self, domain_name: str) -> float:
        """Get current performance for domain from configuration"""
        domain_config = self.config.get_domain_performance(domain_name)
        return domain_config["current"]

    def _generate_trend_data(self) -> Dict[str, List[float]]:
        """Generate trend data from configuration"""
        return self.config.sample_data.trends.copy()

    def _generate_investment_data(self, profile: Any) -> List[Dict[str, Any]]:
        """Generate investment ROI data from profile and configuration"""
        investment_data = []

        if hasattr(profile, "investment_categories"):
            for name, investment in profile.investment_categories.items():
                # Get ROI multiplier from configuration
                roi_multiplier = self.config.get_investment_multiplier(name)

                invested = (
                    self.config.sample_data.investment_base * investment.priority_weight
                )
                projected_return = invested * roi_multiplier

                investment_data.append(
                    {
                        "name": name,
                        "invested": invested,
                        "projected_return": projected_return,
                        "measurement_period": investment.measurement_period_months,
                    }
                )

        return investment_data


class RealDataCollector(DataGeneratorInterface):
    """
    Collects real organizational data from external sources
    Future implementation for production data integration
    """

    def __init__(self, config_manager: ConfigManagerInterface = None):
        self.config = config_manager or visualization_config
        # TODO: Add real data source connections (APIs, databases, etc.)

    def generate_sample_data(self, profile_manager: Any) -> OrganizationalData:
        """Delegate to sample generator for now"""
        sample_generator = SampleDataGenerator(self.config)
        return sample_generator.generate_sample_data(profile_manager)

    def collect_real_data(self, profile_manager: Any) -> OrganizationalData:
        """
        Future implementation for real data collection
        Would integrate with:
        - Jira APIs for project metrics
        - GitHub APIs for development velocity
        - Design system usage analytics
        - Performance monitoring tools
        """
        # Mock implementation - integrate with actual monitoring tools
        # For now, delegate to sample data
        return self.generate_sample_data(profile_manager)
