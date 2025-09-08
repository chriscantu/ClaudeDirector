"""
External Spec-Kit Integration Component

Follows SOLID principles and DRY methodology for external tool coordination.
Integrates with GitHub Spec-Kit while maintaining architectural compliance.

Architecture:
- Single Responsibility: External spec-kit tool coordination only
- Open/Closed: Extensible for other specification tools
- Liskov Substitution: Interface-based design for tool swapping
- Interface Segregation: Focused interfaces for different tool aspects
- Dependency Inversion: Depends on abstractions, not concrete tools
"""

import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

try:
    from ..core.validation import ValidationError
    from ..core.models import StrategicContext
    from ..context_engineering import AdvancedContextEngine
except ImportError:
    # Fallback for test environments
    import sys
    from pathlib import Path

    # Add lib directory to path
    lib_path = Path(__file__).parent.parent
    sys.path.insert(0, str(lib_path))

    try:
        from core.validation import ValidationError
        from core.models import StrategicContext
        from context_engineering import AdvancedContextEngine
    except ImportError:
        # Final fallback with mock classes
        class ValidationError(Exception):
            pass

        class StrategicContext:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        class AdvancedContextEngine:
            def __init__(self, **kwargs):
                pass


class SpecificationTool(Protocol):
    """Protocol for specification tool integration (Interface Segregation)"""

    def generate_specification(
        self, description: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate base specification from description"""
        ...

    def validate_specification(self, spec_path: str) -> bool:
        """Validate specification format and completeness"""
        ...


class ExternalToolError(Exception):
    """External tool integration errors"""

    pass


@dataclass
class SpecificationResult:
    """Result from specification generation"""

    success: bool
    spec_path: Optional[str]
    metadata: Dict[str, Any]
    errors: List[str]


class GitHubSpecKit:
    """Concrete implementation for GitHub Spec-Kit integration"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.temp_dir: Optional[Path] = None

    def _ensure_spec_kit_available(self) -> bool:
        """Verify spec-kit is available (Dependency Inversion)"""
        try:
            result = subprocess.run(
                ["npx", "@github/spec-kit", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def generate_specification(
        self, description: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate specification using GitHub Spec-Kit"""
        if not self._ensure_spec_kit_available():
            raise ExternalToolError(
                "GitHub Spec-Kit not available. Install with: npm install -g @github/spec-kit"
            )

        # Create temporary workspace (Clean Architecture)
        self.temp_dir = Path(tempfile.mkdtemp(prefix="claudedirector_spec_"))

        try:
            # Run spec-kit specification generation
            cmd = [
                "npx",
                "@github/spec-kit",
                "specify",
                description,
                "--output",
                str(self.temp_dir),
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60, cwd=self.temp_dir
            )

            if result.returncode != 0:
                raise ExternalToolError(f"Spec-kit failed: {result.stderr}")

            # Parse generated specification
            spec_files = list(self.temp_dir.glob("**/*.md"))
            if not spec_files:
                raise ExternalToolError("No specification files generated")

            return {
                "spec_path": str(spec_files[0]),
                "temp_dir": str(self.temp_dir),
                "generated_files": [str(f) for f in spec_files],
                "stdout": result.stdout,
                "metadata": self._extract_metadata(spec_files[0]),
            }

        except subprocess.TimeoutExpired:
            raise ExternalToolError("Spec-kit generation timed out")
        except Exception as e:
            self._cleanup_temp_dir()
            raise ExternalToolError(f"Spec generation failed: {e}")

    def validate_specification(self, spec_path: str) -> bool:
        """Validate specification using spec-kit validation"""
        try:
            result = subprocess.run(
                ["npx", "@github/spec-kit", "validate", spec_path],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _extract_metadata(self, spec_file: Path) -> Dict[str, Any]:
        """Extract metadata from generated specification"""
        try:
            content = spec_file.read_text()
            # Basic metadata extraction - can be enhanced
            return {
                "file_size": len(content),
                "line_count": len(content.splitlines()),
                "has_requirements": "## Requirements" in content,
                "has_scenarios": "## User Scenarios" in content,
            }
        except Exception as e:
            self.logger.warning(f"Failed to extract metadata: {e}")
            return {}

    def _cleanup_temp_dir(self):
        """Clean up temporary directory"""
        if self.temp_dir and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                self.logger.warning(f"Failed to cleanup temp dir: {e}")


class SpecKitIntegrator:
    """
    External Spec-Kit Integration Coordinator

    Follows SOLID principles:
    - Single Responsibility: Coordinates external spec tool usage
    - Open/Closed: Extensible for other specification tools
    - Dependency Inversion: Uses abstractions for tool integration
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize with context engine integration (Dependency Injection)"""
        self.context_engine = context_engine
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Initialize spec tool (Strategy Pattern)
        self.spec_tool = GitHubSpecKit(self.config.get("spec_kit", {}))

        # Configuration
        self.preserve_temp_files = self.config.get("preserve_temp_files", False)
        self.validation_enabled = self.config.get("validation_enabled", True)

    def generate_base_specification(
        self, description: str, strategic_context: Optional[StrategicContext] = None
    ) -> SpecificationResult:
        """
        Generate base specification using external spec-kit

        Args:
            description: Strategic feature description
            strategic_context: Optional strategic context for enhancement

        Returns:
            SpecificationResult with generated spec details
        """
        try:
            # Enhance description with strategic context if available
            enhanced_description = self._enhance_description_with_context(
                description, strategic_context
            )

            # Generate specification using external tool
            result = self.spec_tool.generate_specification(
                enhanced_description, self.config
            )

            # Validate if enabled
            if self.validation_enabled and result.get("spec_path"):
                is_valid = self.spec_tool.validate_specification(result["spec_path"])
                if not is_valid:
                    self.logger.warning("Generated specification failed validation")

            return SpecificationResult(
                success=True,
                spec_path=result.get("spec_path"),
                metadata=result.get("metadata", {}),
                errors=[],
            )

        except ExternalToolError as e:
            self.logger.error(f"Spec generation failed: {e}")
            return SpecificationResult(
                success=False, spec_path=None, metadata={}, errors=[str(e)]
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in spec generation: {e}")
            return SpecificationResult(
                success=False,
                spec_path=None,
                metadata={},
                errors=[f"Unexpected error: {e}"],
            )

    def _enhance_description_with_context(
        self, description: str, strategic_context: Optional[StrategicContext]
    ) -> str:
        """Enhance description with strategic context (Single Responsibility)"""
        if not strategic_context:
            return description

        # Add strategic context to description
        enhanced = f"{description}\n\n"
        enhanced += "Strategic Context:\n"

        if hasattr(strategic_context, "stakeholders"):
            enhanced += f"- Stakeholders: {', '.join(strategic_context.stakeholders)}\n"

        if hasattr(strategic_context, "frameworks"):
            enhanced += (
                f"- Applicable Frameworks: {', '.join(strategic_context.frameworks)}\n"
            )

        if hasattr(strategic_context, "constraints"):
            enhanced += f"- Constraints: {', '.join(strategic_context.constraints)}\n"

        return enhanced

    def cleanup_temporary_files(self):
        """Clean up any temporary files created during spec generation"""
        if hasattr(self.spec_tool, "_cleanup_temp_dir"):
            self.spec_tool._cleanup_temp_dir()

    def get_supported_tools(self) -> List[str]:
        """Get list of supported specification tools (Open/Closed Principle)"""
        return ["github-spec-kit"]

    def validate_tool_availability(self, tool_name: str = "github-spec-kit") -> bool:
        """Validate that specified tool is available"""
        if tool_name == "github-spec-kit":
            return self.spec_tool._ensure_spec_kit_available()
        return False
