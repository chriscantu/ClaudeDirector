#!/usr/bin/env python3
"""
SOLID Principle Validator

Martin's automated governance tool preventing SOLID violations.
Runs as pre-commit hook to enforce architectural principles.
"""

import ast
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Violation:
    file_path: str
    line_number: int
    principle: str
    message: str
    severity: str  # 'error', 'warning'


class SOLIDValidator:
    """Validates SOLID principles in Python code"""

    def __init__(self):
        self.violations: List[Violation] = []

        # Hard-coded string patterns that indicate violations
        self.hardcode_patterns = [
            r"['\"](?:urgent|high|medium|low)['\"]",  # Priority levels
            r"['\"](?:excellent|healthy|at_risk|failing)['\"]",  # Health statuses
            r"['\"](?:strategic|operational|technical|organizational)['\"]",  # Decision types
            r"0\.\d+\s*[,)]",  # Threshold values like 0.85, 0.70
            r"['\"][^'\"]*(?:decision|risk|health|stakeholder)[^'\"]*['\"]",  # Domain strings
        ]

        # Allowed hard-coded strings (exceptions)
        self.allowed_patterns = [
            r"['\"]test[^'\"]*['\"]",  # Test strings
            r"['\"]mock[^'\"]*['\"]",  # Mock strings
            r"['\"]unknown['\"]",  # Default unknown value
            r"['\"]error['\"]",  # Error messages
        ]

    def validate_file(self, file_path: Path) -> List[Violation]:
        """Validate a single Python file for SOLID violations"""
        self.violations = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)

            # Check each SOLID principle
            self._check_single_responsibility(tree, file_path)
            self._check_open_closed(tree, file_path)
            self._check_interface_segregation(tree, file_path)
            self._check_dependency_inversion(tree, file_path)
            self._check_hardcoded_strings(content, file_path)

        except SyntaxError as e:
            self.violations.append(
                Violation(
                    file_path=str(file_path),
                    line_number=e.lineno or 0,
                    principle="SYNTAX",
                    message=f"Syntax error: {e.msg}",
                    severity="error",
                )
            )
        except Exception as e:
            self.violations.append(
                Violation(
                    file_path=str(file_path),
                    line_number=0,
                    principle="VALIDATION",
                    message=f"Validation error: {str(e)}",
                    severity="warning",
                )
            )

        return self.violations

    def _check_single_responsibility(self, tree: ast.AST, file_path: Path):
        """Check Single Responsibility Principle violations"""
        class_visitor = ClassAnalyzer()
        class_visitor.visit(tree)

        for class_info in class_visitor.classes:
            # Check for classes doing too many things
            if len(class_info["methods"]) > 15:  # Configurable threshold
                self.violations.append(
                    Violation(
                        file_path=str(file_path),
                        line_number=class_info["line"],
                        principle="SRP",
                        message=f"Class '{class_info['name']}' has {len(class_info['methods'])} methods. Consider splitting responsibilities.",
                        severity="warning",
                    )
                )

            # Check for classes with mixed concerns
            method_names = [m["name"] for m in class_info["methods"]]
            concerns = self._identify_concerns(method_names)
            if len(concerns) > 2:  # More than 2 distinct concerns
                self.violations.append(
                    Violation(
                        file_path=str(file_path),
                        line_number=class_info["line"],
                        principle="SRP",
                        message=f"Class '{class_info['name']}' handles multiple concerns: {', '.join(concerns)}",
                        severity="warning",
                    )
                )

    def _check_open_closed(self, tree: ast.AST, file_path: Path):
        """Check Open/Closed Principle violations"""
        # Look for switch statements or long if-elif chains
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                elif_count = 0
                current = node
                while hasattr(current, "orelse") and current.orelse:
                    if isinstance(current.orelse[0], ast.If):
                        elif_count += 1
                        current = current.orelse[0]
                    else:
                        break

                if elif_count > 5:  # Configurable threshold
                    self.violations.append(
                        Violation(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            principle="OCP",
                            message=f"Long if-elif chain ({elif_count} conditions). Consider using polymorphism or strategy pattern.",
                            severity="warning",
                        )
                    )

    def _check_interface_segregation(self, tree: ast.AST, file_path: Path):
        """Check Interface Segregation Principle violations"""
        class_visitor = ClassAnalyzer()
        class_visitor.visit(tree)

        for class_info in class_visitor.classes:
            # Check for large interfaces (many abstract methods)
            abstract_methods = [
                m
                for m in class_info["methods"]
                if any(
                    d.id == "abstractmethod"
                    for d in m.get("decorators", [])
                    if isinstance(d, ast.Name)
                )
            ]

            if len(abstract_methods) > 8:  # Configurable threshold
                self.violations.append(
                    Violation(
                        file_path=str(file_path),
                        line_number=class_info["line"],
                        principle="ISP",
                        message=f"Interface '{class_info['name']}' has {len(abstract_methods)} abstract methods. Consider splitting into smaller interfaces.",
                        severity="warning",
                    )
                )

    def _check_dependency_inversion(self, tree: ast.AST, file_path: Path):
        """Check Dependency Inversion Principle violations"""
        # Look for direct instantiation of concrete classes
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                # Check for direct instantiation patterns that indicate DIP violations
                class_name = node.func.id
                if (
                    class_name.endswith("Engine")
                    or class_name.endswith("Service")
                    or class_name.endswith("Manager")
                ) and not class_name.startswith("Mock"):

                    # Allow factory methods and dependency injection patterns
                    if not self._is_factory_pattern(
                        node
                    ) and not self._is_dependency_injection(node):
                        self.violations.append(
                            Violation(
                                file_path=str(file_path),
                                line_number=node.lineno,
                                principle="DIP",
                                message=f"Direct instantiation of '{class_name}'. Consider using dependency injection or factory pattern.",
                                severity="warning",
                            )
                        )

    def _check_hardcoded_strings(self, content: str, file_path: Path):
        """Check for hard-coded strings that should be in configuration"""
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Skip comments and test files
            if line.strip().startswith("#") or "test" in str(file_path).lower():
                continue

            for pattern in self.hardcode_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Check if this is an allowed pattern
                    is_allowed = any(
                        re.search(allowed, match.group(), re.IGNORECASE)
                        for allowed in self.allowed_patterns
                    )

                    if not is_allowed:
                        self.violations.append(
                            Violation(
                                file_path=str(file_path),
                                line_number=line_num,
                                principle="DRY",
                                message=f"Hard-coded string detected: {match.group()}. Move to configuration.",
                                severity="error",
                            )
                        )

    def _identify_concerns(self, method_names: List[str]) -> Set[str]:
        """Identify different concerns/responsibilities from method names"""
        concerns = set()

        concern_patterns = {
            "data": ["load", "save", "read", "write", "store", "retrieve"],
            "validation": ["validate", "check", "verify", "ensure"],
            "processing": ["process", "transform", "convert", "parse"],
            "monitoring": ["monitor", "track", "record", "log"],
            "inference": ["predict", "analyze", "detect", "classify"],
            "configuration": ["configure", "setup", "initialize", "config"],
        }

        for method in method_names:
            method_lower = method.lower()
            for concern, patterns in concern_patterns.items():
                if any(pattern in method_lower for pattern in patterns):
                    concerns.add(concern)
                    break

        return concerns

    def _is_factory_pattern(self, node: ast.Call) -> bool:
        """Check if this is a factory pattern instantiation"""
        # Check for factory method patterns
        if hasattr(node.func, "attr") and "create" in node.func.attr.lower():
            return True

        # Check for factory class patterns
        if hasattr(node.func, "id") and "factory" in node.func.id.lower():
            return True

        return False

    def _is_dependency_injection(self, node: ast.Call) -> bool:
        """Check if this is dependency injection pattern"""
        # Look for constructor parameters or configuration-based creation
        if node.args or node.keywords:
            # Check if passing configuration or dependencies
            for keyword in node.keywords:
                if keyword.arg in ["config", "dependency", "service", "factory"]:
                    return True

        return False


class ClassAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze class structure"""

    def __init__(self):
        self.classes = []
        self.current_class = None

    def visit_ClassDef(self, node):
        class_info = {
            "name": node.name,
            "line": node.lineno,
            "methods": [],
            "decorators": node.decorator_list,
        }

        self.current_class = class_info
        self.classes.append(class_info)

        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            method_info = {
                "name": node.name,
                "line": node.lineno,
                "decorators": node.decorator_list,
            }
            self.current_class["methods"].append(method_info)


def main():
    """Main entry point for pre-commit hook"""
    if len(sys.argv) < 2:
        print("Usage: solid_validator.py <file1> [file2] ...")
        sys.exit(1)

    validator = SOLIDValidator()
    total_violations = 0

    for file_path in sys.argv[1:]:
        path = Path(file_path)
        if path.suffix == ".py" and path.exists():
            violations = validator.validate_file(path)

            for violation in violations:
                severity_symbol = "❌" if violation.severity == "error" else "⚠️"
                print(
                    f"{severity_symbol} {violation.file_path}:{violation.line_number} "
                    f"[{violation.principle}] {violation.message}"
                )
                total_violations += 1

    if total_violations > 0:
        print(f"\n🏗️ SOLID Validation: {total_violations} violations found")
        # Only fail on errors, not warnings
        error_count = sum(1 for v in validator.violations if v.severity == "error")
        if error_count > 0:
            print(f"❌ {error_count} errors must be fixed before commit")
            sys.exit(1)
        else:
            print("⚠️ Warnings detected - consider fixing for better architecture")
    else:
        print("✅ SOLID Validation: No violations found")

    sys.exit(0)


if __name__ == "__main__":
    main()
