#!/usr/bin/env python3
"""
Standardized Test Import Utility
Ensures consistent test environment regardless of execution context
"""

import sys
import importlib
import re
from pathlib import Path
from typing import Optional, List, Dict, Any


def setup_test_environment() -> Path:
    """
    Ensure consistent test environment regardless of execution context.

    Returns:
        Path: The lib directory path that was added to sys.path

    Raises:
        ImportError: If .claudedirector directory cannot be located
    """
    # Find claudedirector root by walking up from current file
    current = Path(__file__).resolve()
    while current.name != ".claudedirector" and current.parent != current:
        current = current.parent

    if current.name == ".claudedirector":
        lib_path = current / "lib"
        if str(lib_path) not in sys.path:
            sys.path.insert(0, str(lib_path))
        return lib_path
    else:
        raise ImportError("Could not locate .claudedirector directory")


def get_standard_imports():
    """
    Get standardized imports for common ClaudeDirector modules.

    Returns:
        dict: Dictionary of module aliases for consistent imports
    """
    # Ensure environment is set up first
    lib_path = setup_test_environment()

    # Standard import mappings with correct class names
    imports = {}

    try:
        module = importlib.import_module("core.enhanced_persona_manager")
        imports["EnhancedPersonaManager"] = getattr(module, "EnhancedPersonaManager")
    except (ImportError, AttributeError) as e:
        imports["EnhancedPersonaManager"] = None

    try:
        module = importlib.import_module("integrations.mcp_use_client")
        imports["MCPClient"] = getattr(module, "MCPUseClient")
    except (ImportError, AttributeError):
        imports["MCPClient"] = None

    try:
        module = importlib.import_module("transparency.framework_detection")
        imports["FrameworkDetector"] = getattr(module, "FrameworkDetectionMiddleware")
    except (ImportError, AttributeError):
        imports["FrameworkDetector"] = None

    try:
        module = importlib.import_module("core.complexity_analyzer")
        imports["ComplexityAnalyzer"] = getattr(module, "AnalysisComplexityDetector")
    except (ImportError, AttributeError):
        imports["ComplexityAnalyzer"] = None

    try:
        module = importlib.import_module("transparency.integrated_transparency")
        imports["TransparencyEngine"] = getattr(module, "IntegratedTransparencySystem")
    except (ImportError, AttributeError):
        imports["TransparencyEngine"] = None

    try:
        module = importlib.import_module("core.config")
        imports["Config"] = getattr(module, "ClaudeDirectorConfig")
    except (ImportError, AttributeError):
        imports["Config"] = None

    return imports


def validate_test_environment() -> dict:
    """
    Validate that the test environment is properly configured.

    Returns:
        dict: Validation results with status and available modules
    """
    results = {
        "environment_setup": False,
        "lib_path": None,
        "available_modules": {},
        "missing_modules": [],
        "errors": [],
    }

    try:
        lib_path = setup_test_environment()
        results["environment_setup"] = True
        results["lib_path"] = str(lib_path)
    except ImportError as e:
        results["errors"].append(f"Environment setup failed: {e}")
        return results

    # Test standard imports
    imports = get_standard_imports()
    for name, module in imports.items():
        if module is not None:
            results["available_modules"][name] = str(type(module))
        else:
            results["missing_modules"].append(name)

    return results


def safe_import(module_path: str, class_name: Optional[str] = None):
    """
    Safely import a module or class with proper error handling.

    Args:
        module_path: The module path (e.g., 'lib.core.config')
        class_name: Optional class name to import from module

    Returns:
        The imported module or class, or None if import fails
    """
    setup_test_environment()

    try:
        if class_name:
            module = __import__(module_path, fromlist=[class_name])
            return getattr(module, class_name)
        else:
            return __import__(module_path)
    except (ImportError, AttributeError) as e:
        print(f"⚠️ Import failed: {module_path}.{class_name or ''} - {e}")
        return None


# Convenience functions for common test patterns
def require_test_environment():
    """Decorator to ensure test environment is set up before test execution"""

    def decorator(test_func):
        def wrapper(*args, **kwargs):
            setup_test_environment()
            return test_func(*args, **kwargs)

        return wrapper

    return decorator


def skip_if_missing(*required_modules):
    """Decorator to skip test if required modules are not available"""

    def decorator(test_func):
        def wrapper(*args, **kwargs):
            imports = get_standard_imports()
            missing = [mod for mod in required_modules if imports.get(mod) is None]
            if missing:
                print(f"⏭️ Skipping test: Missing modules {missing}")
                return
            return test_func(*args, **kwargs)

        return wrapper

    return decorator


def analyze_file_imports(file_path: str) -> Dict[str, Any]:
    """
    🚀 ENHANCED: Batch file import analysis for MCP Missing Modules Orchestrator

    Analyzes Python file imports without AST overhead - lightweight regex approach.
    Added to support orchestrator DRY compliance without reimplementing functionality.

    Args:
        file_path: Path to Python file to analyze

    Returns:
        Dict containing import analysis results
    """
    setup_test_environment()

    results = {
        "file_path": file_path,
        "imports_found": [],
        "missing_modules": [],
        "available_modules": [],
        "analysis_success": False,
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract imports using lightweight regex patterns
        import_patterns = [
            r"^import\s+([^\s#;]+)",
            r"^from\s+([^\s#;]+)\s+import",
        ]

        imports_found = set()
        for line in content.split("\n"):
            line = line.strip()
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    module_name = match.group(1).split(".")[0]  # Get base module
                    if module_name and not module_name.startswith(
                        "."
                    ):  # Skip relative imports
                        imports_found.add(module_name)

        results["imports_found"] = list(imports_found)

        # Check module availability using existing safe_import functionality
        for module_name in imports_found:
            module = safe_import(module_name)
            if module is None:
                results["missing_modules"].append(module_name)
            else:
                results["available_modules"].append(module_name)

        results["analysis_success"] = True

    except Exception as e:
        results["error"] = str(e)

    return results


def batch_analyze_directory_imports(
    directory_path: str, recursive: bool = True
) -> Dict[str, Any]:
    """
    🚀 ENHANCED: Batch directory import analysis for MCP orchestrator

    Analyzes all Python files in directory for missing imports.
    Supports MCP Missing Modules Orchestrator without duplicating AST functionality.

    Args:
        directory_path: Directory to analyze
        recursive: Whether to analyze subdirectories

    Returns:
        Dict containing batch analysis results
    """
    setup_test_environment()

    results = {
        "directory_path": directory_path,
        "files_analyzed": 0,
        "total_imports": 0,
        "missing_modules_summary": {},
        "file_results": {},
        "analysis_success": False,
    }

    try:
        directory = Path(directory_path)

        # Find Python files
        if recursive:
            python_files = list(directory.rglob("*.py"))
        else:
            python_files = list(directory.glob("*.py"))

        # Analyze each file
        for py_file in python_files:
            try:
                file_result = analyze_file_imports(str(py_file))
                results["file_results"][str(py_file)] = file_result

                if file_result["analysis_success"]:
                    results["files_analyzed"] += 1
                    results["total_imports"] += len(file_result["imports_found"])

                    # Aggregate missing modules
                    for missing_module in file_result["missing_modules"]:
                        if missing_module not in results["missing_modules_summary"]:
                            results["missing_modules_summary"][missing_module] = []
                        results["missing_modules_summary"][missing_module].append(
                            str(py_file)
                        )

            except Exception as e:
                results["file_results"][str(py_file)] = {"error": str(e)}

        results["analysis_success"] = True

    except Exception as e:
        results["error"] = str(e)

    return results


if __name__ == "__main__":
    # Self-test when run directly
    print("🧪 Testing enhanced import utility...")

    results = validate_test_environment()

    print(f"Environment setup: {'✅' if results['environment_setup'] else '❌'}")
    print(f"Lib path: {results['lib_path']}")

    if results["available_modules"]:
        print("\n✅ Available modules:")
        for name, type_info in results["available_modules"].items():
            print(f"  • {name}: {type_info}")

    if results["missing_modules"]:
        print(f"\n⚠️ Missing modules: {', '.join(results['missing_modules'])}")

    if results["errors"]:
        print(f"\n❌ Errors: {', '.join(results['errors'])}")

    print(
        f"\n🎯 Test environment {'ready' if results['environment_setup'] else 'needs setup'}"
    )

    # Test enhanced batch analysis
    print("\n🚀 Testing enhanced batch analysis...")
    try:
        current_file_analysis = analyze_file_imports(__file__)
        print(
            f"✅ Current file analysis: {len(current_file_analysis['imports_found'])} imports found"
        )
    except Exception as e:
        print(f"❌ Enhanced analysis failed: {e}")
