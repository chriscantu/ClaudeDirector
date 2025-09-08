"""
Core Validation Module

Provides validation utilities and error classes for ClaudeDirector.
Follows SOLID principles with focused validation responsibilities.
"""

from typing import Any, Dict, List, Optional, Union
import re
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Base validation error"""

    pass


class InputValidationError(ValidationError):
    """Input validation specific error"""

    pass


class ConfigurationValidationError(ValidationError):
    """Configuration validation specific error"""

    pass


class Validator:
    """Base validator class following Single Responsibility Principle"""

    def validate(self, value: Any) -> bool:
        """Validate a value, return True if valid"""
        return True  # Base implementation accepts all values

    def get_error_message(self, value: Any) -> str:
        """Get error message for invalid value"""
        return f"Validation failed for value: {value}"


class StringValidator(Validator):
    """String validation with length and pattern constraints"""

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = 1000,
        pattern: Optional[str] = None,
        required: bool = True,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None
        self.required = required

    def validate(self, value: Any) -> bool:
        """Validate string value"""
        if value is None:
            return not self.required

        if not isinstance(value, str):
            return False

        if len(value) < self.min_length or len(value) > self.max_length:
            return False

        if self.pattern and not self.pattern.match(value):
            return False

        return True

    def get_error_message(self, value: Any) -> str:
        if value is None and self.required:
            return "Required string value is missing"
        if not isinstance(value, str):
            return f"Expected string, got {type(value).__name__}"
        if len(value) < self.min_length:
            return f"String too short: {len(value)} < {self.min_length}"
        if len(value) > self.max_length:
            return f"String too long: {len(value)} > {self.max_length}"
        if self.pattern and not self.pattern.match(value):
            return f"String does not match required pattern: {self.pattern.pattern}"
        return "String validation failed"


class NumericValidator(Validator):
    """Numeric validation with range constraints"""

    def __init__(
        self,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        allow_int: bool = True,
        allow_float: bool = True,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.allow_int = allow_int
        self.allow_float = allow_float

    def validate(self, value: Any) -> bool:
        """Validate numeric value"""
        if not isinstance(value, (int, float)):
            return False

        if isinstance(value, int) and not self.allow_int:
            return False

        if isinstance(value, float) and not self.allow_float:
            return False

        if self.min_value is not None and value < self.min_value:
            return False

        if self.max_value is not None and value > self.max_value:
            return False

        return True

    def get_error_message(self, value: Any) -> str:
        if not isinstance(value, (int, float)):
            return f"Expected numeric value, got {type(value).__name__}"
        if isinstance(value, int) and not self.allow_int:
            return "Integer values not allowed"
        if isinstance(value, float) and not self.allow_float:
            return "Float values not allowed"
        if self.min_value is not None and value < self.min_value:
            return f"Value too small: {value} < {self.min_value}"
        if self.max_value is not None and value > self.max_value:
            return f"Value too large: {value} > {self.max_value}"
        return "Numeric validation failed"


class ListValidator(Validator):
    """List validation with length and element constraints"""

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = 100,
        element_validator: Optional[Validator] = None,
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.element_validator = element_validator

    def validate(self, value: Any) -> bool:
        """Validate list value"""
        if not isinstance(value, list):
            return False

        if len(value) < self.min_length or len(value) > self.max_length:
            return False

        if self.element_validator:
            for element in value:
                if not self.element_validator.validate(element):
                    return False

        return True

    def get_error_message(self, value: Any) -> str:
        if not isinstance(value, list):
            return f"Expected list, got {type(value).__name__}"
        if len(value) < self.min_length:
            return f"List too short: {len(value)} < {self.min_length}"
        if len(value) > self.max_length:
            return f"List too long: {len(value)} > {self.max_length}"
        return "List validation failed"


class DictValidator(Validator):
    """Dictionary validation with key/value constraints"""

    def __init__(
        self,
        required_keys: Optional[List[str]] = None,
        optional_keys: Optional[List[str]] = None,
        key_validator: Optional[Validator] = None,
        value_validator: Optional[Validator] = None,
    ):
        self.required_keys = required_keys or []
        self.optional_keys = optional_keys or []
        self.key_validator = key_validator
        self.value_validator = value_validator

    def validate(self, value: Any) -> bool:
        """Validate dictionary value"""
        if not isinstance(value, dict):
            return False

        # Check required keys
        for key in self.required_keys:
            if key not in value:
                return False

        # Check for unexpected keys
        allowed_keys = set(self.required_keys + self.optional_keys)
        if allowed_keys and not set(value.keys()).issubset(allowed_keys):
            return False

        # Validate keys and values
        for key, val in value.items():
            if self.key_validator and not self.key_validator.validate(key):
                return False
            if self.value_validator and not self.value_validator.validate(val):
                return False

        return True

    def get_error_message(self, value: Any) -> str:
        if not isinstance(value, dict):
            return f"Expected dictionary, got {type(value).__name__}"

        missing_keys = [k for k in self.required_keys if k not in value]
        if missing_keys:
            return f"Missing required keys: {missing_keys}"

        return "Dictionary validation failed"


def validate_strategic_context(context: Dict[str, Any]) -> None:
    """Validate strategic context dictionary"""
    required_fields = ["stakeholders", "frameworks", "constraints", "objectives"]

    for field in required_fields:
        if field not in context:
            raise ValidationError(
                f"Missing required field in strategic context: {field}"
            )

        if not isinstance(context[field], list):
            raise ValidationError(f"Field {field} must be a list")

    # Validate specific field constraints
    if len(context["stakeholders"]) == 0:
        raise ValidationError("At least one stakeholder must be specified")

    if len(context["objectives"]) == 0:
        raise ValidationError("At least one objective must be specified")


def validate_specification_content(content: str) -> None:
    """Validate specification content structure"""
    if not content or not content.strip():
        raise ValidationError("Specification content cannot be empty")

    required_sections = ["## Requirements", "## User Scenarios"]

    for section in required_sections:
        if section not in content:
            raise ValidationError(f"Missing required section: {section}")

    # Check minimum length
    if len(content.strip()) < 100:
        raise ValidationError(
            "Specification content too short (minimum 100 characters)"
        )


def validate_file_path(file_path: str) -> None:
    """Validate file path format and safety"""
    if not file_path:
        raise ValidationError("File path cannot be empty")

    # Check for path traversal attempts
    if ".." in file_path or file_path.startswith("/"):
        raise ValidationError("Invalid file path: potential security risk")

    # Check file extension
    allowed_extensions = [".md", ".txt", ".yaml", ".yml", ".json"]
    if not any(file_path.endswith(ext) for ext in allowed_extensions):
        raise ValidationError(
            f"File extension not allowed. Allowed: {allowed_extensions}"
        )


def validate_config(config: Dict[str, Any]) -> None:
    """Validate configuration dictionary"""
    if not isinstance(config, dict):
        raise ConfigurationValidationError("Configuration must be a dictionary")

    # Validate boolean configurations
    bool_configs = [
        "validation_enabled",
        "preserve_temp_files",
        "enable_framework_enhancement",
    ]
    for key in bool_configs:
        if key in config and not isinstance(config[key], bool):
            raise ConfigurationValidationError(f"Configuration {key} must be boolean")

    # Validate numeric configurations
    numeric_configs = {"timeout": (1, 300), "max_retries": (0, 10)}
    for key, (min_val, max_val) in numeric_configs.items():
        if key in config:
            value = config[key]
            if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                raise ConfigurationValidationError(
                    f"Configuration {key} must be numeric between {min_val} and {max_val}"
                )
