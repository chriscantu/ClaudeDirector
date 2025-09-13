"""
🎯 Placement Configuration Loader - Modular Configuration Management

🏗️ Martin | Platform Architecture - DRY Compliance & Modularization

ARCHITECTURAL COMPLIANCE:
✅ DRY: Eliminates hardcoded placement rules from StructureAwarePlacementEngine
✅ SOLID: Single responsibility for configuration loading and validation
✅ PROJECT_STRUCTURE.md: Placed in .claudedirector/lib/core/generation/
✅ BLOAT_PREVENTION_SYSTEM.md: Reduces code duplication through externalized config

MODULARIZATION BENEFITS:
- Eliminates ~400 lines of hardcoded rules from placement engine
- Enables runtime configuration updates without code changes
- Provides centralized configuration management
- Supports configuration validation and error handling

Author: Martin | Platform Architecture - Sequential Thinking modularization
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ComponentCategory(Enum):
    """Component categories for placement mapping"""

    CORE_FOUNDATIONAL = "core_foundational"
    VALIDATION = "validation"
    GENERATION = "generation"
    AI_INTELLIGENCE = "ai_intelligence"
    CONTEXT_ENGINEERING = "context_engineering"
    PERFORMANCE = "performance"
    P0_FEATURES = "p0_features"
    P1_FEATURES = "p1_features"
    P2_COMMUNICATION = "p2_communication"
    TRANSPARENCY = "transparency"
    INTEGRATION = "integration"
    CONFIG = "config"
    UTILS = "utils"
    TESTS_UNIT = "tests_unit"
    TESTS_REGRESSION = "tests_regression"
    TESTS_INTEGRATION = "tests_integration"
    TESTS_PERFORMANCE = "tests_performance"
    DOCS_ARCHITECTURE = "docs_architecture"
    DOCS_DEVELOPMENT = "docs_development"
    DOCS_REQUIREMENTS = "docs_requirements"
    TOOLS = "tools"


@dataclass
class PlacementRule:
    """Rule for component placement based on PROJECT_STRUCTURE.md"""

    category: ComponentCategory
    base_path: str
    patterns: List[str] = field(default_factory=list)
    description: str = ""
    examples: List[str] = field(default_factory=list)


class PlacementConfigLoader:
    """
    Configuration loader for placement rules and component patterns

    ELIMINATES hardcoded rules from StructureAwarePlacementEngine
    PROVIDES centralized configuration management
    ENABLES runtime configuration updates
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration loader"""
        if config_path is None:
            # Try different possible locations
            possible_paths = [
                Path("config/placement_rules.yaml"),  # From .claudedirector/
                Path(
                    ".claudedirector/config/placement_rules.yaml"
                ),  # From project root
                Path("../config/placement_rules.yaml"),  # From lib/
            ]

            for path in possible_paths:
                if path.exists():
                    self.config_path = path
                    break
            else:
                # Default to the standard location
                self.config_path = Path("config/placement_rules.yaml")
        else:
            self.config_path = config_path
        self._config_cache: Optional[Dict[str, Any]] = None

        logger.debug(
            f"PlacementConfigLoader initialized with config_path={self.config_path}"
        )

    def load_placement_rules(self) -> Dict[ComponentCategory, PlacementRule]:
        """
        Load placement rules from YAML configuration

        Returns:
            Dictionary mapping ComponentCategory to PlacementRule
        """
        config = self._load_config()
        placement_rules = {}

        for category_name, rule_config in config.get("placement_rules", {}).items():
            try:
                # Convert category name to enum
                category = ComponentCategory(category_name)

                # Create placement rule
                rule = PlacementRule(
                    category=category,
                    base_path=rule_config["base_path"],
                    patterns=rule_config.get("patterns", []),
                    description=rule_config.get("description", ""),
                    examples=rule_config.get("examples", []),
                )

                placement_rules[category] = rule

            except ValueError as e:
                logger.warning(f"Unknown component category '{category_name}': {e}")
                continue
            except KeyError as e:
                logger.error(
                    f"Missing required field in placement rule '{category_name}': {e}"
                )
                continue

        logger.info(f"Loaded {len(placement_rules)} placement rules from configuration")
        return placement_rules

    def load_component_patterns(self) -> Dict[str, ComponentCategory]:
        """
        Load component patterns from YAML configuration

        Returns:
            Dictionary mapping pattern strings to ComponentCategory
        """
        config = self._load_config()
        component_patterns = {}

        for pattern, category_name in config.get("component_patterns", {}).items():
            try:
                category = ComponentCategory(category_name)
                component_patterns[pattern] = category
            except ValueError as e:
                logger.warning(
                    f"Unknown component category '{category_name}' for pattern '{pattern}': {e}"
                )
                continue

        logger.info(
            f"Loaded {len(component_patterns)} component patterns from configuration"
        )
        return component_patterns

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file with caching

        Returns:
            Configuration dictionary
        """
        if self._config_cache is not None:
            return self._config_cache

        try:
            if not self.config_path.exists():
                logger.error(f"Configuration file not found: {self.config_path}")
                return {}

            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)

            if not isinstance(config, dict):
                logger.error(f"Invalid configuration format in {self.config_path}")
                return {}

            self._config_cache = config
            logger.debug(f"Configuration loaded successfully from {self.config_path}")
            return config

        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {self.config_path}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading configuration from {self.config_path}: {e}")
            return {}

    def reload_config(self) -> None:
        """Clear configuration cache to force reload on next access"""
        self._config_cache = None
        logger.info("Configuration cache cleared - will reload on next access")

    def validate_config(self) -> List[str]:
        """
        Validate configuration file and return list of errors

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        config = self._load_config()

        if not config:
            errors.append("Configuration file is empty or invalid")
            return errors

        # Validate placement_rules section
        if "placement_rules" not in config:
            errors.append("Missing 'placement_rules' section")
        else:
            for category_name, rule_config in config["placement_rules"].items():
                if not isinstance(rule_config, dict):
                    errors.append(
                        f"Invalid rule config for '{category_name}': must be dictionary"
                    )
                    continue

                if "base_path" not in rule_config:
                    errors.append(f"Missing 'base_path' for rule '{category_name}'")

                try:
                    ComponentCategory(category_name)
                except ValueError:
                    errors.append(f"Unknown component category '{category_name}'")

        # Validate component_patterns section
        if "component_patterns" not in config:
            errors.append("Missing 'component_patterns' section")
        else:
            for pattern, category_name in config["component_patterns"].items():
                try:
                    ComponentCategory(category_name)
                except ValueError:
                    errors.append(
                        f"Unknown component category '{category_name}' for pattern '{pattern}'"
                    )

        return errors


def create_placement_config_loader(
    config_path: Optional[Path] = None,
) -> PlacementConfigLoader:
    """
    Factory function for creating PlacementConfigLoader

    Args:
        config_path: Optional path to configuration file

    Returns:
        Configured PlacementConfigLoader instance
    """
    return PlacementConfigLoader(config_path)
