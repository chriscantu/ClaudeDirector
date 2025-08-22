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
        """Load configuration from YAML or JSON file"""
        try:
            # If config file doesn't exist but template does, create config from template
            if not self.config_path.exists() and self.template_path.exists():
                self._create_config_from_template()

            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    if YAML_AVAILABLE and self.config_path.suffix == ".yaml":
                        config = yaml.safe_load(f)
                        return config.get("user", {}) if config else {}
                    else:
                        # Try to parse as JSON or simple key-value
                        content = f.read().strip()
                        if content.startswith("{"):
                            config = json.loads(content)
                            return config.get("user", {})
                        else:
                            # Simple manual parsing for YAML-like content
                            return self._parse_simple_yaml(content)
        except Exception as e:
            print(f"Warning: Could not load user config from {self.config_path}: {e}")

        return {}

    def _create_config_from_template(self) -> None:
        """Create user config from template if it doesn't exist"""
        try:
            if self.template_path.exists():
                import shutil

                shutil.copy2(self.template_path, self.config_path)
                print(f"Created user config from template: {self.config_path}")
        except Exception as e:
            print(f"Warning: Could not create config from template: {e}")

    def _parse_simple_yaml(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for basic user config"""
        config = {}
        in_user_section = False

        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("user:"):
                in_user_section = True
                continue

            if in_user_section and line and not line.startswith("#"):
                if line.startswith("name:"):
                    config["name"] = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("work_name:"):
                    config["work_name"] = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("full_name:"):
                    config["full_name"] = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("role:"):
                    config["role"] = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("organization:"):
                    config["organization"] = line.split(":", 1)[1].strip().strip("\"'")
                elif not line.startswith(" ") and line.endswith(":"):
                    # New section, exit user section
                    break

        return config

    def _load_from_env(self) -> Dict[str, str]:
        """Load configuration from environment variables"""
        env_mapping = {
            "name": "CLAUDEDIRECTOR_USER_NAME",
            "work_name": "CLAUDEDIRECTOR_WORK_NAME",
            "full_name": "CLAUDEDIRECTOR_FULL_NAME",
            "role": "CLAUDEDIRECTOR_USER_ROLE",
            "organization": "CLAUDEDIRECTOR_ORGANIZATION",
        }

        env_config = {}
        for key, env_var in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                env_config[key] = value

        return env_config

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
