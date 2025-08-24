#!/usr/bin/env python3
"""
Standardized Test Import Utility
Ensures consistent test environment regardless of execution context
"""

import sys
import importlib
from pathlib import Path
from typing import Optional


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
    while current.name != '.claudedirector' and current.parent != current:
        current = current.parent

    if current.name == '.claudedirector':
        lib_path = current / 'lib'
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
        module = importlib.import_module('core.enhanced_persona_manager')
        imports['EnhancedPersonaManager'] = getattr(module, 'EnhancedPersonaManager')
    except (ImportError, AttributeError) as e:
        imports['EnhancedPersonaManager'] = None

    try:
        module = importlib.import_module('integrations.mcp_use_client')
        imports['MCPClient'] = getattr(module, 'MCPUseClient')
    except (ImportError, AttributeError):
        imports['MCPClient'] = None

    try:
        module = importlib.import_module('transparency.framework_detection')
        imports['FrameworkDetector'] = getattr(module, 'FrameworkDetectionMiddleware')
    except (ImportError, AttributeError):
        imports['FrameworkDetector'] = None

    try:
        module = importlib.import_module('core.complexity_analyzer')
        imports['ComplexityAnalyzer'] = getattr(module, 'AnalysisComplexityDetector')
    except (ImportError, AttributeError):
        imports['ComplexityAnalyzer'] = None

    try:
        module = importlib.import_module('transparency.integrated_transparency')
        imports['TransparencyEngine'] = getattr(module, 'IntegratedTransparencySystem')
    except (ImportError, AttributeError):
        imports['TransparencyEngine'] = None

    try:
        module = importlib.import_module('core.config')
        imports['Config'] = getattr(module, 'ClaudeDirectorConfig')
    except (ImportError, AttributeError):
        imports['Config'] = None

    return imports


def validate_test_environment() -> dict:
    """
    Validate that the test environment is properly configured.

    Returns:
        dict: Validation results with status and available modules
    """
    results = {
        'environment_setup': False,
        'lib_path': None,
        'available_modules': {},
        'missing_modules': [],
        'errors': []
    }

    try:
        lib_path = setup_test_environment()
        results['environment_setup'] = True
        results['lib_path'] = str(lib_path)
    except ImportError as e:
        results['errors'].append(f"Environment setup failed: {e}")
        return results

    # Test standard imports
    imports = get_standard_imports()
    for name, module in imports.items():
        if module is not None:
            results['available_modules'][name] = str(type(module))
        else:
            results['missing_modules'].append(name)

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


if __name__ == "__main__":
    # Self-test when run directly
    print("🧪 Testing standardized import utility...")

    results = validate_test_environment()

    print(f"Environment setup: {'✅' if results['environment_setup'] else '❌'}")
    print(f"Lib path: {results['lib_path']}")

    if results['available_modules']:
        print("\n✅ Available modules:")
        for name, type_info in results['available_modules'].items():
            print(f"  • {name}: {type_info}")

    if results['missing_modules']:
        print(f"\n⚠️ Missing modules: {', '.join(results['missing_modules'])}")

    if results['errors']:
        print(f"\n❌ Errors: {', '.join(results['errors'])}")

    print(f"\n🎯 Test environment {'ready' if results['environment_setup'] else 'needs setup'}")
