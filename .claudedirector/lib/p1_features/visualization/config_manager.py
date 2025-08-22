#!/usr/bin/env python3
"""
Configuration Manager for P1.1 Visualization
Addresses DRY violations by centralizing all configuration values
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
from dataclasses import dataclass


@dataclass
class SampleDataConfig:
    """Sample data configuration for visualization testing"""

    metrics: Dict[str, float]
    domain_performance: Dict[str, Dict[str, float]]
    trends: Dict[str, List[float]]
    investment_multipliers: Dict[str, float]
    investment_base: float
    minimum_impact_score: float


@dataclass
class DesignSystemConfig:
    """Design system configuration values"""

    performance_thresholds: Dict[str, float]
    threshold_names: Dict[str, str]
    shadow_opacities: Dict[str, float]


@dataclass
class ROIStatusConfig:
    """ROI status configuration"""

    thresholds: Dict[str, float]
    labels: Dict[str, str]


class VisualizationConfigManager:
    """
    Central configuration manager following DRY principles
    Eliminates hard-coded values throughout visualization system
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or "config/p1_visualization_config.yaml")
        self._config_data: Optional[Dict[str, Any]] = None
        self._sample_data_config: Optional[SampleDataConfig] = None
        self._design_system_config: Optional[DesignSystemConfig] = None
        self._roi_status_config: Optional[ROIStatusConfig] = None

    @property
    def config_data(self) -> Dict[str, Any]:
        """Lazy load configuration data"""
        if self._config_data is None:
            self._load_config()
        return self._config_data

    def _load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config_data = yaml.safe_load(f)
        except FileNotFoundError:
            # Fallback to default configuration
            self._config_data = self._get_default_config()
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file {self.config_path}: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration if file not found"""
        return {
            "sample_data": {
                "metrics": {
                    "component_usage_consistency": 0.78,
                    "design_debt_reduction": 0.12,
                    "cross_team_design_velocity": 0.22,
                    "adoption_rate_percentage": 0.75,
                    "developer_satisfaction_score": 4.3,
                    "time_to_onboard_new_teams": 2.8,
                    "api_response_times": 180,
                    "service_dependency_health": 0.95,
                },
                "domain_performance": {
                    "design_domains": {"current": 0.78, "default_target": 0.8},
                    "platform_domains": {"current": 0.75, "default_target": 0.8},
                    "api_domains": {"current": 0.85, "default_target": 0.8},
                    "other_domains": {"current": 0.70, "default_target": 0.8},
                },
                "trends": {
                    "design_system_leverage": [
                        0.65,
                        0.68,
                        0.71,
                        0.73,
                        0.75,
                        0.77,
                        0.78,
                        0.78,
                    ],
                    "platform_adoption": [
                        0.68,
                        0.70,
                        0.71,
                        0.72,
                        0.73,
                        0.74,
                        0.75,
                        0.75,
                    ],
                    "api_service_efficiency": [
                        0.80,
                        0.82,
                        0.83,
                        0.84,
                        0.85,
                        0.85,
                        0.85,
                        0.85,
                    ],
                },
                "investment_multipliers": {
                    "design_system_enhancement": 1.25,
                    "platform_infrastructure": 1.18,
                    "developer_experience": 1.30,
                    "cross_team_tooling": 1.15,
                    "default": 1.20,
                },
                "investment_base": 50000,
                "minimum_impact_score": 0.65,
            },
            "design_system": {
                "performance_thresholds": {
                    "excellent": 0.95,
                    "good": 0.8,
                    "moderate": 0.6,
                    "poor": 0.0,
                },
                "threshold_names": {
                    "excellent": "excellent",
                    "good": "good",
                    "moderate": "moderate",
                    "poor": "poor",
                },
                "shadow_opacities": {
                    "sm": 0.05,
                    "md": 0.1,
                    "lg": 0.1,
                    "xl": 0.1,
                },
            },
            "roi_status": {
                "thresholds": {
                    "excellent": 20,
                    "good": 10,
                    "moderate": 0,
                },
                "labels": {
                    "excellent": "Excellent",
                    "good": "Good",
                    "moderate": "Moderate",
                    "poor": "Poor",
                },
            },
            "defaults": {
                "target_fallback": 0.0,
                "division_by_zero_fallback": 0.0,
            },
            "threshold_keys": {
                "excellent_key": "excellent",
                "good_key": "good",
                "moderate_key": "moderate",
                "poor_key": "poor",
            },
        }

    @property
    def sample_data(self) -> SampleDataConfig:
        """Get sample data configuration"""
        if self._sample_data_config is None:
            data = self.config_data["sample_data"]
            self._sample_data_config = SampleDataConfig(
                metrics=data["metrics"],
                domain_performance=data["domain_performance"],
                trends=data["trends"],
                investment_multipliers=data["investment_multipliers"],
                investment_base=data["investment_base"],
                minimum_impact_score=data["minimum_impact_score"],
            )
        return self._sample_data_config

    @property
    def design_system(self) -> DesignSystemConfig:
        """Get design system configuration"""
        if self._design_system_config is None:
            data = self.config_data["design_system"]
            self._design_system_config = DesignSystemConfig(
                performance_thresholds=data["performance_thresholds"],
                threshold_names=data["threshold_names"],
                shadow_opacities=data["shadow_opacities"],
            )
        return self._design_system_config

    @property
    def roi_status(self) -> ROIStatusConfig:
        """Get ROI status configuration"""
        if self._roi_status_config is None:
            data = self.config_data["roi_status"]
            self._roi_status_config = ROIStatusConfig(
                thresholds=data["thresholds"],
                labels=data["labels"],
            )
        return self._roi_status_config

    def get_sample_metric(self, metric_name: str) -> float:
        """Get specific sample metric value"""
        return self.sample_data.metrics.get(metric_name, 0.0)

    def get_domain_performance(self, domain_type: str) -> Dict[str, float]:
        """Get domain performance configuration"""
        domain_configs = self.sample_data.domain_performance

        # Map domain types to config keys
        if "design" in domain_type.lower():
            return domain_configs["design_domains"]
        elif "platform" in domain_type.lower():
            return domain_configs["platform_domains"]
        elif "api" in domain_type.lower():
            return domain_configs["api_domains"]
        else:
            return domain_configs["other_domains"]

    def get_trend_data(self, trend_name: str) -> List[float]:
        """Get trend data for specific metric"""
        return self.sample_data.trends.get(trend_name, [])

    def get_investment_multiplier(self, investment_name: str) -> float:
        """Get ROI multiplier for investment type"""
        multipliers = self.sample_data.investment_multipliers
        return multipliers.get(investment_name, multipliers["default"])

    def get_performance_threshold(self, level: str) -> float:
        """Get performance threshold for given level"""
        return self.design_system.performance_thresholds.get(level, 0.0)

    def get_shadow_opacity(self, size: str) -> float:
        """Get shadow opacity for given size"""
        return self.design_system.shadow_opacities.get(size, 0.1)

    def get_threshold_name(self, level: str) -> str:
        """Get threshold name for given level"""
        return self.design_system.threshold_names.get(level, level)

    def get_roi_threshold(self, level: str) -> float:
        """Get ROI threshold for given level"""
        return self.roi_status.thresholds.get(level, 0.0)

    def get_roi_label(self, level: str) -> str:
        """Get ROI label for given level"""
        return self.roi_status.labels.get(level, "Unknown")

    def get_default_value(self, key: str) -> float:
        """Get default value to avoid hard-coding"""
        defaults = self.config_data.get("defaults", {})
        return defaults.get(key, 0.0)

    def get_threshold_key(self, level: str) -> str:
        """Get threshold key to avoid hard-coding threshold names"""
        keys = self.config_data.get("threshold_keys", {})
        return keys.get(f"{level}_key", level)


# Global configuration manager instance
visualization_config = VisualizationConfigManager()
