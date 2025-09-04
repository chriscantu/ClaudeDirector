#!/usr/bin/env python3
"""
Duplicate Pattern Detection Engine

🎯 STRATEGIC OBJECTIVE: Detect duplicate code patterns across the codebase
for surgical elimination and massive code reduction.

This engine uses AST analysis to identify duplicate patterns with high precision,
enabling safe elimination of redundant code while preserving functionality.

Author: Martin | Platform Architecture with Validator-Driven Elimination
"""

import ast
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class MethodPattern:
    """Represents a method pattern for duplicate detection"""

    file_path: str
    method_name: str
    class_name: Optional[str]
    ast_hash: str
    signature_hash: str
    body_lines: int
    start_line: int
    end_line: int
    variables: Set[str]
    function_calls: Set[str]
    control_structures: List[str]


@dataclass
class DuplicateGroup:
    """Group of duplicate patterns"""

    pattern_type: str
    similarity_score: float
    patterns: List[MethodPattern]
    canonical_pattern: MethodPattern
    elimination_potential: int  # lines that can be eliminated


class DuplicateDetector:
    """
    🔍 DUPLICATE PATTERN DETECTION ENGINE

    Uses AST analysis to detect duplicate code patterns across multiple files
    with configurable similarity thresholds and pattern types.
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.patterns: List[MethodPattern] = []
        self.duplicate_groups: List[DuplicateGroup] = []

    def analyze_files(self, file_paths: List[str]) -> List[DuplicateGroup]:
        """
        Analyze multiple files and detect duplicate patterns

        Args:
            file_paths: List of Python files to analyze

        Returns:
            List of duplicate groups found
        """
        logger.info(f"🔍 Analyzing {len(file_paths)} files for duplicate patterns")

        # Extract patterns from all files
        for file_path in file_paths:
            if Path(file_path).suffix == ".py":
                self._extract_patterns_from_file(file_path)

        logger.info(f"📊 Extracted {len(self.patterns)} method patterns")

        # Group similar patterns
        self._group_similar_patterns()

        logger.info(f"🎯 Found {len(self.duplicate_groups)} duplicate groups")

        return self.duplicate_groups

    def _extract_patterns_from_file(self, file_path: str) -> None:
        """Extract method patterns from a single file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    pattern = self._create_method_pattern(file_path, node, source)
                    if pattern:
                        self.patterns.append(pattern)

        except Exception as e:
            logger.warning(f"⚠️ Failed to analyze {file_path}: {e}")

    def _create_method_pattern(
        self, file_path: str, node: ast.FunctionDef, source: str
    ) -> Optional[MethodPattern]:
        """Create a MethodPattern from an AST node"""
        try:
            # Get class context if method is inside a class
            class_name = None
            for parent in ast.walk(ast.parse(source)):
                if isinstance(parent, ast.ClassDef):
                    for child in ast.walk(parent):
                        if child is node:
                            class_name = parent.name
                            break

            # Calculate hashes for similarity comparison
            ast_hash = self._calculate_ast_hash(node)
            signature_hash = self._calculate_signature_hash(node)

            # Extract variables and function calls
            variables = self._extract_variables(node)
            function_calls = self._extract_function_calls(node)
            control_structures = self._extract_control_structures(node)

            # Calculate line metrics
            body_lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 1

            return MethodPattern(
                file_path=file_path,
                method_name=node.name,
                class_name=class_name,
                ast_hash=ast_hash,
                signature_hash=signature_hash,
                body_lines=body_lines,
                start_line=node.lineno,
                end_line=node.end_lineno or node.lineno,
                variables=variables,
                function_calls=function_calls,
                control_structures=control_structures,
            )

        except Exception as e:
            logger.warning(f"⚠️ Failed to create pattern for {node.name}: {e}")
            return None

    def _calculate_ast_hash(self, node: ast.FunctionDef) -> str:
        """Calculate hash of AST structure (normalized)"""
        # Normalize AST by removing variable names and literals
        normalized = ast.dump(node, annotate_fields=False, include_attributes=False)
        return hashlib.md5(normalized.encode()).hexdigest()

    def _calculate_signature_hash(self, node: ast.FunctionDef) -> str:
        """Calculate hash of method signature"""
        signature_parts = [node.name]

        # Add argument types and defaults
        for arg in node.args.args:
            signature_parts.append(arg.arg)

        signature = "|".join(signature_parts)
        return hashlib.md5(signature.encode()).hexdigest()

    def _extract_variables(self, node: ast.FunctionDef) -> Set[str]:
        """Extract variable names from method"""
        variables = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                variables.add(child.id)
        return variables

    def _extract_function_calls(self, node: ast.FunctionDef) -> Set[str]:
        """Extract function call names from method"""
        calls = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.add(child.func.attr)
        return calls

    def _extract_control_structures(self, node: ast.FunctionDef) -> List[str]:
        """Extract control structure types from method"""
        structures = []
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                structures.append(type(child).__name__)
        return structures

    def _group_similar_patterns(self) -> None:
        """Group similar patterns into duplicate groups"""
        pattern_groups = defaultdict(list)

        # Group by signature hash first (same method signature)
        for pattern in self.patterns:
            key = f"{pattern.method_name}_{len(pattern.variables)}_{len(pattern.function_calls)}"
            pattern_groups[key].append(pattern)

        # Find duplicates within each group
        for group_patterns in pattern_groups.values():
            if len(group_patterns) < 2:
                continue

            duplicates = self._find_duplicates_in_group(group_patterns)
            self.duplicate_groups.extend(duplicates)

    def _find_duplicates_in_group(
        self, patterns: List[MethodPattern]
    ) -> List[DuplicateGroup]:
        """Find duplicate patterns within a group"""
        duplicates = []
        processed = set()

        for i, pattern1 in enumerate(patterns):
            if i in processed:
                continue

            similar_patterns = [pattern1]

            for j, pattern2 in enumerate(patterns[i + 1 :], i + 1):
                if j in processed:
                    continue

                similarity = self._calculate_similarity(pattern1, pattern2)

                if similarity >= self.similarity_threshold:
                    similar_patterns.append(pattern2)
                    processed.add(j)

            if len(similar_patterns) > 1:
                # Create duplicate group
                canonical = self._select_canonical_pattern(similar_patterns)
                elimination_potential = (
                    sum(p.body_lines for p in similar_patterns) - canonical.body_lines
                )

                duplicate_group = DuplicateGroup(
                    pattern_type=f"{similar_patterns[0].method_name}_pattern",
                    similarity_score=self._calculate_group_similarity(similar_patterns),
                    patterns=similar_patterns,
                    canonical_pattern=canonical,
                    elimination_potential=elimination_potential,
                )

                duplicates.append(duplicate_group)
                processed.add(i)

        return duplicates

    def _calculate_similarity(
        self, pattern1: MethodPattern, pattern2: MethodPattern
    ) -> float:
        """Calculate similarity score between two patterns"""
        # AST structure similarity (40%)
        ast_similarity = 1.0 if pattern1.ast_hash == pattern2.ast_hash else 0.0

        # Variable similarity (20%)
        var_intersection = len(pattern1.variables & pattern2.variables)
        var_union = len(pattern1.variables | pattern2.variables)
        var_similarity = var_intersection / var_union if var_union > 0 else 0.0

        # Function call similarity (30%)
        call_intersection = len(pattern1.function_calls & pattern2.function_calls)
        call_union = len(pattern1.function_calls | pattern2.function_calls)
        call_similarity = call_intersection / call_union if call_union > 0 else 0.0

        # Control structure similarity (10%)
        control_similarity = (
            1.0 if pattern1.control_structures == pattern2.control_structures else 0.0
        )

        # Weighted average
        total_similarity = (
            ast_similarity * 0.4
            + var_similarity * 0.2
            + call_similarity * 0.3
            + control_similarity * 0.1
        )

        return total_similarity

    def _calculate_group_similarity(self, patterns: List[MethodPattern]) -> float:
        """Calculate average similarity within a group"""
        if len(patterns) < 2:
            return 1.0

        total_similarity = 0.0
        comparisons = 0

        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                total_similarity += self._calculate_similarity(patterns[i], patterns[j])
                comparisons += 1

        return total_similarity / comparisons if comparisons > 0 else 0.0

    def _select_canonical_pattern(self, patterns: List[MethodPattern]) -> MethodPattern:
        """Select the canonical pattern (most complete/recent)"""
        # Prefer patterns with more comprehensive implementations
        return max(
            patterns,
            key=lambda p: (
                p.body_lines,  # More comprehensive
                len(p.function_calls),  # More functionality
                len(p.variables),  # More complete
                -p.start_line,  # More recent (assuming later = better)
            ),
        )

    def get_elimination_summary(self) -> Dict[str, int]:
        """Get summary of elimination potential"""
        return {
            "total_duplicate_groups": len(self.duplicate_groups),
            "total_elimination_potential": sum(
                g.elimination_potential for g in self.duplicate_groups
            ),
            "files_affected": len(
                set(p.file_path for g in self.duplicate_groups for p in g.patterns)
            ),
            "average_similarity": (
                sum(g.similarity_score for g in self.duplicate_groups)
                / len(self.duplicate_groups)
                if self.duplicate_groups
                else 0.0
            ),
        }


if __name__ == "__main__":
    # Example usage
    detector = DuplicateDetector(similarity_threshold=0.85)

    # Test with processor files
    processor_files = [
        ".claudedirector/lib/personas/personality_processor.py",
        ".claudedirector/lib/context_engineering/analytics_processor.py",
        ".claudedirector/lib/ai_intelligence/decision_processor.py",
        ".claudedirector/lib/p0_features/domains/strategic_metrics/business_intelligence_processor.py",
    ]

    duplicate_groups = detector.analyze_files(processor_files)
    summary = detector.get_elimination_summary()

    print("🎯 DUPLICATE DETECTION RESULTS:")
    print(f"   Duplicate Groups: {summary['total_duplicate_groups']}")
    print(f"   Elimination Potential: {summary['total_elimination_potential']} lines")
    print(f"   Files Affected: {summary['files_affected']}")
    print(f"   Average Similarity: {summary['average_similarity']:.2%}")
