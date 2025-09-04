#!/usr/bin/env python3
"""
User Configuration Management for ClaudeDirector
Centralizes user identity and preferences with environment variable support.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict

# Try to import yaml, fall back to json if not available
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class UserIdentity:
    """User identity configuration with fallback hierarchy"""

    name: str = "User"
    work_name: str = ""
    full_name: str = ""
    role: str = ""
    organization: str = ""

    def get_name(self, context: str = "default") -> str:
        """
        Get appropriate name based on context

        Args:
            context: "default", "work", "full", "professional"

        Returns:
            str: Appropriate name for the context
        """
        if context == "work" and self.work_name:
            return self.work_name
        elif context == "full" and self.full_name:
            return self.full_name
        elif context == "professional":
            return self.work_name or self.name
        else:
            return self.name

    def get_attribution(self) -> str:
        """Get name for requirement attribution (e.g., 'Cantu's requirement')"""
        return f"{self.get_name('professional')}'s requirement"

    def get_possessive(self, context: str = "default") -> str:
        """Get possessive form of name (e.g., 'Cantu's')"""
        name = self.get_name(context)
        return f"{name}'s" if not name.endswith("s") else f"{name}'"


class UserConfigManager:
    """
    Manages user configuration with multiple sources and fallbacks

    Priority order:
    1. Environment variables
    2. Configuration file
    3. Defaults
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize user configuration manager

        Args:
            config_path: Optional path to config file, defaults to standard location
        """
        if config_path is None:
            config_path = (
                Path(__file__).parent.parent.parent / "config" / "user_identity.yaml"
            )

        self.config_path = config_path
        self.template_path = config_path.parent / "user_identity.yaml.template"
        self._user_identity: Optional[UserIdentity] = None

    def _load_from_file(self) -> Dict[str, Any]:
        """
        🏗️ STORY 2.2: UNIFIED CONFIG LOADER INTEGRATION
        Eliminates ~40 lines of duplicate YAML/JSON loading logic
        """
        from ..core.unified_config_loader import UnifiedConfigLoader

        loader = UnifiedConfigLoader(
            default_config_dir=self.config_path.parent,
            enable_templates=True,
            enable_env_vars=True,
        )

        result = loader.load_config(
            config_name=self.config_path.stem,
            config_path=self.config_path,
            template_name=(
                self.template_path.stem if self.template_path.exists() else None
            ),
            section="user",
        )

        if not result.success and result.error:
            print(
                f"Warning: Could not load user config from {self.config_path}: {result.error}"
            )

        return result.data

    def _create_config_from_template(self) -> None:
        """
        🏗️ STORY 2.2: DEPRECATED - Template creation now handled by UnifiedConfigLoader
        This method is kept for backwards compatibility but delegates to unified system
        """
        # Template creation is now handled automatically by UnifiedConfigLoader
        # This method is kept for backwards compatibility
        pass

    def _parse_simple_yaml(self, content: str) -> Dict[str, Any]:
        """
        🏗️ STORY 2.2: DEPRECATED - YAML parsing now handled by UnifiedConfigLoader
        This method is kept for backwards compatibility but delegates to unified system
        """
        # YAML parsing is now handled by UnifiedConfigLoader._parse_simple_yaml
        # This method is kept for backwards compatibility
        return {}

    def _load_from_env(self) -> Dict[str, str]:
        """
        🏗️ STORY 2.2: DEPRECATED - Environment variable handling now in UnifiedConfigLoader
        This method is kept for backwards compatibility but delegates to unified system
        """
        # Environment variable integration is now handled by UnifiedConfigLoader
        # This method is kept for backwards compatibility
        return {}

    def get_user_identity(self) -> UserIdentity:
        """
        Get user identity with full fallback hierarchy

        Returns:
            UserIdentity: Complete user identity configuration
        """
        if self._user_identity is None:
            # Start with defaults
            config = {}

            # Load from file
            file_config = self._load_from_file()
            config.update(file_config)

            # Override with environment variables
            env_config = self._load_from_env()
            config.update(env_config)

            # Create UserIdentity with defaults for missing values
            self._user_identity = UserIdentity(**config)

        return self._user_identity

    def save_user_config(self, user_identity: UserIdentity) -> bool:
        """
        Save user configuration to file

        Args:
            user_identity: UserIdentity to save

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare config structure
            config = {
                "user": asdict(user_identity),
                "# Configuration": "See comments in template for usage guidance",
            }

            # Write to file
            with open(self.config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)

            # Clear cached identity to force reload
            self._user_identity = None

            return True

        except Exception as e:
            print(f"Error saving user config: {e}")
            return False

    def configure_user_interactive(self) -> UserIdentity:
        """
        Interactive user configuration setup

        Returns:
            UserIdentity: Configured user identity
        """
        print("🎯 ClaudeDirector User Configuration Setup")
        print("=" * 50)
        print("This will personalize system messages and documentation.")
        print()

        current = self.get_user_identity()

        # Get user input with current values as defaults
        name = input(f"Primary name [{current.name}]: ").strip() or current.name
        work_name = (
            input(f"Work name (optional) [{current.work_name}]: ").strip()
            or current.work_name
        )
        full_name = (
            input(f"Full name (optional) [{current.full_name}]: ").strip()
            or current.full_name
        )
        role = (
            input(f"Role/title (optional) [{current.role}]: ").strip() or current.role
        )
        organization = (
            input(f"Organization (optional) [{current.organization}]: ").strip()
            or current.organization
        )

        # Create new identity
        new_identity = UserIdentity(
            name=name,
            work_name=work_name,
            full_name=full_name,
            role=role,
            organization=organization,
        )

        # Show preview
        print("\n📋 Configuration Preview:")
        print(f"  Default name: {new_identity.get_name('default')}")
        print(f"  Professional name: {new_identity.get_name('professional')}")
        print(f"  Attribution: {new_identity.get_attribution()}")
        if new_identity.role:
            print(f"  Role: {new_identity.role}")
        if new_identity.organization:
            print(f"  Organization: {new_identity.organization}")

        # Confirm and save
        confirm = input("\nSave this configuration? [Y/n]: ").strip().lower()
        if confirm in ("", "y", "yes"):
            if self.save_user_config(new_identity):
                print("✅ User configuration saved successfully!")
            else:
                print("❌ Failed to save configuration")

        return new_identity


# Global instance for easy access
_user_config_manager = None


def get_user_config_manager() -> UserConfigManager:
    """Get global user configuration manager instance"""
    global _user_config_manager
    if _user_config_manager is None:
        _user_config_manager = UserConfigManager()
    return _user_config_manager


def get_user_identity() -> UserIdentity:
    """Get current user identity configuration"""
    return get_user_config_manager().get_user_identity()


def get_user_name(context: str = "default") -> str:
    """Get user name for specified context"""
    return get_user_identity().get_name(context)


def get_user_attribution() -> str:
    """Get user attribution string (e.g., 'Cantu's requirement')"""
    return get_user_identity().get_attribution()


if __name__ == "__main__":
    # Interactive configuration when run directly
    manager = UserConfigManager()
    manager.configure_user_interactive()
