"""
Centralized exception handling for ClaudeDirector
"""

from typing import Optional, Any


class ClaudeDirectorError(Exception):
    """Base exception for all ClaudeDirector errors"""

    def __init__(self, message: str, component: Optional[str] = None, **kwargs: Any) -> None:
        self.message = message
        self.component = component
        self.context = kwargs
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.component:
            return f"[{self.component}] {self.message}"
        return self.message


class DatabaseError(ClaudeDirectorError):
    """Database-related errors"""

    def __init__(self, message: str, db_path: Optional[str] = None, **kwargs: Any) -> None:
        self.db_path = db_path
        super().__init__(message, component="database", db_path=db_path, **kwargs)


class AIDetectionError(ClaudeDirectorError):
    """AI detection and processing errors"""

    def __init__(
        self, message: str, detection_type: Optional[str] = None, confidence: Optional[float] = None, **kwargs: Any
    ) -> None:
        self.detection_type = detection_type
        self.confidence = confidence
        super().__init__(
            message,
            component="ai_detection",
            detection_type=detection_type,
            confidence=confidence,
            **kwargs,
        )


class ConfigurationError(ClaudeDirectorError):
    """Configuration-related errors"""

    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs: Any) -> None:
        self.config_key = config_key
        super().__init__(message, component="configuration", config_key=config_key, **kwargs)


class WorkspaceError(ClaudeDirectorError):
    """Workspace processing errors"""

    def __init__(self, message: str, workspace_path: Optional[str] = None, **kwargs: Any) -> None:
        self.workspace_path = workspace_path
        super().__init__(message, component="workspace", workspace_path=workspace_path, **kwargs)


class SetupError(ClaudeDirectorError):
    """Setup and initialization errors"""

    def __init__(self, message: str, setup_component: Optional[str] = None, **kwargs: Any) -> None:
        self.setup_component = setup_component
        super().__init__(message, component="setup", setup_component=setup_component, **kwargs)
