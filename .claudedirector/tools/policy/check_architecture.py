#!/usr/bin/env python3
"""
Architecture Compliance Policy Enforcement
Ensures all code changes adhere to documented architectural principles.
"""

import sys
import ast
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple


class ArchitectureChecker:
    """Validates architectural compliance for Python code."""

    def __init__(self):
        self.violations = []
        self.allowed_imports = {
            # Core module import patterns
            "lib.core": ["lib.integrations", "lib.transparency", "lib.frameworks"],
            "lib.integrations": ["lib.core"],
            "lib.transparency": ["lib.core", "lib.integrations"],
            "lib.frameworks": ["lib.core"],
            "lib.mcp": ["lib.core", "lib.integrations"],
        }

    def check_import_compliance(self, file_path: Path, tree: ast.AST) -> List[str]:
        """Check if imports follow architectural boundaries."""
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    module_name = node.module

                    # Check for circular imports
                    if self._is_circular_import(file_path, module_name):
                        violations.append(f"Circular import detected: {module_name}")

                    # Check for layer violations
                    if self._is_layer_violation(file_path, module_name):
                        violations.append(
                            f"Layer violation: {module_name} not allowed from {file_path}"
                        )

        return violations

    def _is_circular_import(self, file_path: Path, module_name: str) -> bool:
        """Detect potential circular imports."""
        # Simplified circular import detection
        file_module = self._get_module_from_path(file_path)

        if file_module and module_name:
            # Check if importing from same module family
            if file_module.startswith("lib.") and module_name.startswith("lib."):
                file_base = (
                    file_module.split(".")[1] if len(file_module.split(".")) > 1 else ""
                )
                import_base = (
                    module_name.split(".")[1] if len(module_name.split(".")) > 1 else ""
                )

                # Prevent core from importing from itself through other modules
                if (
                    file_base == "core"
                    and import_base == "core"
                    and file_module != module_name
                ):
                    return True

        return False

    def _is_layer_violation(self, file_path: Path, module_name: str) -> bool:
        """Check if import violates architectural layers."""
        file_module = self._get_module_from_path(file_path)

        if not file_module or not module_name.startswith("lib."):
            return False

        # Get base module (e.g., 'lib.core' from 'lib.core.persona_manager')
        file_base = ".".join(file_module.split(".")[:2])
        import_base = ".".join(module_name.split(".")[:2])

        if file_base in self.allowed_imports:
            allowed = self.allowed_imports[file_base]
            if import_base not in allowed and import_base != file_base:
                return True

        return False

    def _get_module_from_path(self, file_path: Path) -> str:
        """Convert file path to module name."""
        try:
            # Convert path to module notation
            parts = file_path.parts

            # Find .claudedirector in path
            if ".claudedirector" in parts:
                claudedirector_idx = parts.index(".claudedirector")
                if (
                    claudedirector_idx + 1 < len(parts)
                    and parts[claudedirector_idx + 1] == "lib"
                ):
                    # Extract module path after lib/
                    module_parts = parts[claudedirector_idx + 2 :]
                    if module_parts:
                        # Remove .py extension
                        if module_parts[-1].endswith(".py"):
                            module_parts = module_parts[:-1] + (module_parts[-1][:-3],)
                        return "lib." + ".".join(module_parts)

        except Exception:
            pass

        return ""

    def check_file(self, file_path: Path) -> List[str]:
        """Check a single Python file for architectural compliance."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            violations = []

            # Check import compliance
            import_violations = self.check_import_compliance(file_path, tree)
            violations.extend(import_violations)

            return violations

        except SyntaxError as e:
            return [f"Syntax error: {e}"]
        except Exception as e:
            return [f"Error analyzing file: {e}"]


def main():
    """Main policy enforcement function."""
    if len(sys.argv) < 2:
        print("Usage: check_architecture.py <file1.py> [file2.py] ...")
        sys.exit(1)

    checker = ArchitectureChecker()
    total_violations = []
    total_files = 0

    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)

        if not file_path.exists() or not file_path.suffix == ".py":
            continue

        # Skip test files and __init__.py for now
        if "test" in str(file_path) or file_path.name == "__init__.py":
            continue

        total_files += 1
        violations = checker.check_file(file_path)

        if violations:
            total_violations.append((file_path, violations))

    # Report results
    if total_violations:
        print("🚨 ARCHITECTURE POLICY VIOLATIONS DETECTED")
        print("=" * 60)
        print("Policy: Code must follow documented architectural principles")
        print()

        for file_path, violations in total_violations:
            print(f"❌ {file_path}")
            for violation in violations:
                print(f"   • {violation}")
            print()

        print("💡 REMEDIATION REQUIRED:")
        print("- Review architectural layer boundaries in docs/architecture/")
        print("- Fix circular imports and layer violations")
        print("- Follow import patterns in existing compliant code")
        print("- See docs/DEVELOPMENT_POLICY.md for complete guidelines")
        print(
            "- Reference docs/development/guides/CORE_ARCHITECTURE.md for architectural principles"
        )
        print(
            "- Follow docs/development/guides/DEVELOPMENT_WORKFLOW.md for import standards"
        )
        print()
        print("🛡️ COMMIT BLOCKED: Fix violations before proceeding")
        sys.exit(1)
    else:
        if total_files > 0:
            print(
                f"✅ Architecture Policy: All {total_files} files comply with architectural principles"
            )
        sys.exit(0)


if __name__ == "__main__":
    main()
