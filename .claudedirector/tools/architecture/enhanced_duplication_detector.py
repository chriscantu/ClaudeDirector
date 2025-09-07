#!/usr/bin/env python3
"""
Enhanced Duplication Detector - TS-4 Prevention System

🛡️ Martin | Platform Architecture - Systematic Duplication Prevention

CRITICAL PURPOSE: Prevent TS-4-style duplication violations through comprehensive
cross-directory analysis and mandatory architectural discovery enforcement.

This tool extends the existing bloat_prevention_system.py with:
- Cross-directory functional similarity analysis
- New file creation validation against existing components
- Mandatory ADR reference checking for new components
- Enhanced pre-commit integration

Architecture Compliance: Integrates with existing prevention systems
Performance Target: <10s analysis for full repository scan
"""

import os
import sys
import ast
import re
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import difflib

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from .claudedirector.lib.core.database import get_database_connection
    from .claudedirector.tools.architecture.bloat_prevention_system import (
        BloatPreventionSystem,
    )

    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False


@dataclass
class FunctionSignature:
    """Represents a function signature for similarity analysis"""

    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    body_hash: str
    complexity_score: float
    file_path: str
    line_number: int


@dataclass
class ComponentAnalysis:
    """Analysis result for a component or file"""

    file_path: str
    language: str
    functions: List[FunctionSignature]
    classes: List[str]
    imports: List[str]
    complexity_score: float
    purpose_keywords: List[str]
    architectural_patterns: List[str]


@dataclass
class DuplicationMatch:
    """Represents a detected duplication between components"""

    source_file: str
    target_file: str
    similarity_score: float
    match_type: str  # 'functional', 'structural', 'semantic'
    matched_functions: List[Tuple[str, str]]
    consolidation_recommendation: str
    severity: str  # 'CRITICAL', 'HIGH', 'MODERATE', 'LOW'


class EnhancedDuplicationDetector:
    """
    Enhanced duplication detection system for preventing TS-4-style violations

    Capabilities:
    - Cross-directory functional similarity analysis
    - New component validation against existing functionality
    - Mandatory ADR reference checking
    - Integration with existing bloat prevention system
    """

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = (
            Path(project_root)
            if project_root
            else Path(__file__).parent.parent.parent.parent
        )
        self.claudedirector_root = self.project_root / ".claudedirector"

        # Analysis caches for performance
        self.component_cache: Dict[str, ComponentAnalysis] = {}
        self.similarity_cache: Dict[Tuple[str, str], float] = {}

        # Configuration
        self.similarity_thresholds = {
            "CRITICAL": 0.95,  # Blocks commits
            "HIGH": 0.85,  # Blocks commits
            "MODERATE": 0.75,  # Warning
            "LOW": 0.60,  # Informational
        }

        # Patterns for architectural discovery
        self.integration_patterns = [
            "cursor",
            "integration",
            "bridge",
            "connector",
            "adapter",
            "processor",
            "handler",
            "manager",
            "engine",
            "coordinator",
        ]

        # Initialize existing bloat prevention system
        try:
            self.bloat_system = (
                BloatPreventionSystem()
                if "BloatPreventionSystem" in globals()
                else None
            )
        except:
            self.bloat_system = None

    def analyze_new_component_request(
        self, proposed_file: str, content: str
    ) -> Dict[str, Any]:
        """
        Analyze a proposed new component for duplication violations

        This is the main entry point for pre-commit validation
        """
        start_time = time.time()

        # Step 1: Analyze proposed component
        proposed_analysis = self._analyze_component_content(proposed_file, content)

        # Step 2: Find existing similar components
        similar_components = self._find_similar_existing_components(proposed_analysis)

        # Step 3: Check for ADR reference (if creating new component)
        adr_compliance = self._check_adr_compliance(proposed_file, content)

        # Step 4: Generate consolidation recommendations
        recommendations = self._generate_consolidation_recommendations(
            proposed_analysis, similar_components
        )

        # Step 5: Determine if commit should be blocked
        should_block = self._should_block_commit(similar_components, adr_compliance)

        analysis_time = time.time() - start_time

        return {
            "timestamp": time.time(),
            "analysis_time_seconds": analysis_time,
            "proposed_file": proposed_file,
            "should_block_commit": should_block,
            "adr_compliance": adr_compliance,
            "similar_components": [asdict(comp) for comp in similar_components],
            "recommendations": recommendations,
            "proposed_analysis": asdict(proposed_analysis),
            "summary": self._generate_analysis_summary(
                proposed_analysis, similar_components, should_block
            ),
        }

    def scan_repository_for_duplications(self) -> Dict[str, Any]:
        """
        Comprehensive repository scan for existing duplications

        Used for periodic analysis and cleanup planning
        """
        start_time = time.time()

        # Step 1: Analyze all components in lib/
        all_components = self._analyze_all_components()

        # Step 2: Find all duplication matches
        all_duplications = self._find_all_duplications(all_components)

        # Step 3: Prioritize by severity and consolidation potential
        prioritized_duplications = self._prioritize_duplications(all_duplications)

        # Step 4: Generate cleanup recommendations
        cleanup_plan = self._generate_cleanup_plan(prioritized_duplications)

        analysis_time = time.time() - start_time

        return {
            "timestamp": time.time(),
            "analysis_time_seconds": analysis_time,
            "components_analyzed": len(all_components),
            "duplications_found": len(all_duplications),
            "severity_breakdown": self._calculate_severity_breakdown(all_duplications),
            "prioritized_duplications": [
                asdict(dup) for dup in prioritized_duplications
            ],
            "cleanup_plan": cleanup_plan,
            "summary": self._generate_repository_summary(
                all_duplications, cleanup_plan
            ),
        }

    def _analyze_component_content(
        self, file_path: str, content: str
    ) -> ComponentAnalysis:
        """Analyze component content for similarity matching"""
        try:
            # Parse AST for structural analysis
            tree = ast.parse(content)

            # Extract functions
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_sig = self._extract_function_signature(node, content)
                    functions.append(func_sig)

            # Extract classes
            classes = [
                node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            ]

            # Extract imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    imports.extend([f"{module}.{alias.name}" for alias in node.names])

            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(
                content, functions, classes
            )

            # Extract purpose keywords
            purpose_keywords = self._extract_purpose_keywords(file_path, content)

            # Detect architectural patterns
            architectural_patterns = self._detect_architectural_patterns(content)

            return ComponentAnalysis(
                file_path=file_path,
                language="python",  # Assuming Python for now
                functions=functions,
                classes=classes,
                imports=imports,
                complexity_score=complexity_score,
                purpose_keywords=purpose_keywords,
                architectural_patterns=architectural_patterns,
            )

        except SyntaxError:
            # Handle non-Python files or syntax errors
            return ComponentAnalysis(
                file_path=file_path,
                language="unknown",
                functions=[],
                classes=[],
                imports=[],
                complexity_score=0.0,
                purpose_keywords=self._extract_purpose_keywords(file_path, content),
                architectural_patterns=[],
            )

    def _extract_function_signature(
        self, node: ast.FunctionDef, content: str
    ) -> FunctionSignature:
        """Extract detailed function signature for similarity analysis"""
        # Get function arguments
        args = [arg.arg for arg in node.args.args]

        # Get return type annotation if available
        returns = None
        if node.returns:
            returns = (
                ast.unparse(node.returns)
                if hasattr(ast, "unparse")
                else str(node.returns)
            )

        # Get docstring
        docstring = ast.get_docstring(node)

        # Calculate body hash for exact matching
        body_lines = content.split("\n")[node.lineno - 1 : node.end_lineno]
        body_content = "\n".join(body_lines)
        body_hash = hashlib.md5(body_content.encode()).hexdigest()

        # Calculate complexity score
        complexity_score = (
            len(args) + len([n for n in ast.walk(node) if isinstance(n, ast.If)]) * 2
        )

        return FunctionSignature(
            name=node.name,
            args=args,
            returns=returns,
            docstring=docstring,
            body_hash=body_hash,
            complexity_score=complexity_score,
            file_path="",  # Will be set by caller
            line_number=node.lineno,
        )

    def _find_similar_existing_components(
        self, proposed: ComponentAnalysis
    ) -> List[DuplicationMatch]:
        """Find existing components similar to proposed component"""
        similar_components = []

        # Scan all existing components in lib/
        for existing_file in self._get_all_python_files():
            if existing_file == proposed.file_path:
                continue

            try:
                with open(existing_file, "r", encoding="utf-8") as f:
                    existing_content = f.read()

                existing_analysis = self._analyze_component_content(
                    existing_file, existing_content
                )

                # Calculate similarity
                similarity_score = self._calculate_similarity(
                    proposed, existing_analysis
                )

                if similarity_score > self.similarity_thresholds["LOW"]:
                    match_type = self._determine_match_type(proposed, existing_analysis)
                    severity = self._determine_severity(similarity_score)

                    # Find matched functions
                    matched_functions = self._find_matched_functions(
                        proposed.functions, existing_analysis.functions
                    )

                    # Generate consolidation recommendation
                    consolidation_rec = self._generate_consolidation_recommendation(
                        proposed, existing_analysis, similarity_score
                    )

                    duplication_match = DuplicationMatch(
                        source_file=proposed.file_path,
                        target_file=existing_file,
                        similarity_score=similarity_score,
                        match_type=match_type,
                        matched_functions=matched_functions,
                        consolidation_recommendation=consolidation_rec,
                        severity=severity,
                    )

                    similar_components.append(duplication_match)

            except Exception as e:
                # Skip files that can't be analyzed
                continue

        # Sort by similarity score (highest first)
        similar_components.sort(key=lambda x: x.similarity_score, reverse=True)

        return similar_components

    def _calculate_similarity(
        self, comp1: ComponentAnalysis, comp2: ComponentAnalysis
    ) -> float:
        """Calculate similarity score between two components"""
        # Cache key for performance
        cache_key = (comp1.file_path, comp2.file_path)
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]

        similarity_factors = []

        # 1. Purpose keyword similarity (30% weight)
        purpose_similarity = self._calculate_keyword_similarity(
            comp1.purpose_keywords, comp2.purpose_keywords
        )
        similarity_factors.append(("purpose", purpose_similarity, 0.30))

        # 2. Function name similarity (25% weight)
        func1_names = [f.name for f in comp1.functions]
        func2_names = [f.name for f in comp2.functions]
        function_similarity = self._calculate_keyword_similarity(
            func1_names, func2_names
        )
        similarity_factors.append(("functions", function_similarity, 0.25))

        # 3. Class name similarity (20% weight)
        class_similarity = self._calculate_keyword_similarity(
            comp1.classes, comp2.classes
        )
        similarity_factors.append(("classes", class_similarity, 0.20))

        # 4. Import similarity (15% weight)
        import_similarity = self._calculate_keyword_similarity(
            comp1.imports, comp2.imports
        )
        similarity_factors.append(("imports", import_similarity, 0.15))

        # 5. Architectural pattern similarity (10% weight)
        pattern_similarity = self._calculate_keyword_similarity(
            comp1.architectural_patterns, comp2.architectural_patterns
        )
        similarity_factors.append(("patterns", pattern_similarity, 0.10))

        # Calculate weighted average
        total_similarity = sum(
            score * weight for _, score, weight in similarity_factors
        )

        # Cache result
        self.similarity_cache[cache_key] = total_similarity

        return total_similarity

    def _calculate_keyword_similarity(
        self, list1: List[str], list2: List[str]
    ) -> float:
        """Calculate similarity between two lists of keywords"""
        if not list1 and not list2:
            return 0.0
        if not list1 or not list2:
            return 0.0

        # Convert to sets for intersection/union operations
        set1 = set(keyword.lower() for keyword in list1)
        set2 = set(keyword.lower() for keyword in list2)

        # Jaccard similarity
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def _extract_purpose_keywords(self, file_path: str, content: str) -> List[str]:
        """Extract keywords that indicate the purpose of the component"""
        keywords = []

        # Extract from file name
        file_name = Path(file_path).stem
        keywords.extend(re.findall(r"[a-z]+", file_name.lower()))

        # Extract from docstrings and comments
        docstring_pattern = r'"""(.*?)"""'
        comment_pattern = r"#\s*(.*?)$"

        for match in re.finditer(docstring_pattern, content, re.DOTALL):
            text = match.group(1).lower()
            keywords.extend(re.findall(r"\b[a-z]{3,}\b", text))

        for match in re.finditer(comment_pattern, content, re.MULTILINE):
            text = match.group(1).lower()
            keywords.extend(re.findall(r"\b[a-z]{3,}\b", text))

        # Filter out common words and return unique keywords
        common_words = {
            "the",
            "and",
            "for",
            "with",
            "this",
            "that",
            "from",
            "are",
            "was",
        }
        unique_keywords = list(
            set(kw for kw in keywords if kw not in common_words and len(kw) > 2)
        )

        return unique_keywords[:20]  # Limit to top 20 keywords

    def _detect_architectural_patterns(self, content: str) -> List[str]:
        """Detect architectural patterns in the code"""
        patterns = []
        content_lower = content.lower()

        pattern_indicators = {
            "bridge": ["bridge", "adapter", "wrapper"],
            "factory": ["factory", "create", "builder"],
            "observer": ["observer", "listener", "event", "notify"],
            "singleton": ["singleton", "instance"],
            "strategy": ["strategy", "algorithm", "policy"],
            "decorator": ["decorator", "enhance", "wrap"],
            "facade": ["facade", "interface", "simplify"],
            "proxy": ["proxy", "placeholder", "surrogate"],
            "mvc": ["model", "view", "controller"],
            "repository": ["repository", "dao", "data access"],
        }

        for pattern, indicators in pattern_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                patterns.append(pattern)

        return patterns

    def _calculate_complexity_score(
        self, content: str, functions: List[FunctionSignature], classes: List[str]
    ) -> float:
        """Calculate complexity score for the component"""
        lines = len(content.split("\n"))
        function_count = len(functions)
        class_count = len(classes)

        # Simple complexity calculation
        complexity = (lines / 100) + (function_count * 0.5) + (class_count * 1.0)

        # Add complexity from function complexity scores
        if functions:
            avg_func_complexity = sum(f.complexity_score for f in functions) / len(
                functions
            )
            complexity += avg_func_complexity

        return min(complexity, 20.0)  # Cap at 20.0

    def _get_all_python_files(self) -> List[str]:
        """Get all Python files in the lib/ directory"""
        lib_dir = self.claudedirector_root / "lib"
        python_files = []

        for root, dirs, files in os.walk(lib_dir):
            # Skip cache and test directories
            dirs[:] = [
                d for d in dirs if not d.startswith("__pycache__") and d != "tests"
            ]

            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    python_files.append(os.path.join(root, file))

        return python_files

    def _check_adr_compliance(self, proposed_file: str, content: str) -> Dict[str, Any]:
        """Check if new component has proper ADR reference"""
        adr_compliance = {
            "has_adr_reference": False,
            "adr_file": None,
            "compliance_score": 0.0,
            "missing_requirements": [],
        }

        # Check if this is a new file
        if not os.path.exists(proposed_file):
            # Look for ADR reference in content
            adr_pattern = r"ADR-(\d+)"
            adr_matches = re.findall(adr_pattern, content)

            if adr_matches:
                adr_number = adr_matches[0]
                adr_file = f"docs/architecture/ADR-{adr_number}-*.md"

                # Check if ADR file exists
                adr_files = list(
                    self.project_root.glob(f"docs/architecture/ADR-{adr_number}-*.md")
                )

                if adr_files:
                    adr_compliance["has_adr_reference"] = True
                    adr_compliance["adr_file"] = str(adr_files[0])
                    adr_compliance["compliance_score"] = 1.0
                else:
                    adr_compliance["missing_requirements"].append(
                        f"ADR file not found: {adr_file}"
                    )
            else:
                adr_compliance["missing_requirements"].append(
                    "No ADR reference found in new component"
                )
        else:
            # Existing file modification - no ADR required
            adr_compliance["compliance_score"] = 1.0

        return adr_compliance

    def _should_block_commit(
        self, similar_components: List[DuplicationMatch], adr_compliance: Dict[str, Any]
    ) -> bool:
        """Determine if commit should be blocked based on duplication and ADR compliance"""
        # Block if any CRITICAL or HIGH similarity found
        for match in similar_components:
            if match.severity in ["CRITICAL", "HIGH"]:
                return True

        # Block if new component without proper ADR
        if adr_compliance["compliance_score"] < 1.0:
            return True

        return False

    def _generate_consolidation_recommendation(
        self,
        proposed: ComponentAnalysis,
        existing: ComponentAnalysis,
        similarity: float,
    ) -> str:
        """Generate specific consolidation recommendation"""
        if similarity > 0.95:
            return f"CRITICAL: Enhance existing component {existing.file_path} instead of creating duplicate"
        elif similarity > 0.85:
            return f"HIGH: Consider enhancing {existing.file_path} or create focused extension"
        elif similarity > 0.75:
            return f"MODERATE: Review {existing.file_path} for potential consolidation opportunities"
        else:
            return f"LOW: Monitor for future consolidation with {existing.file_path}"

    def _determine_match_type(
        self, comp1: ComponentAnalysis, comp2: ComponentAnalysis
    ) -> str:
        """Determine the type of match between components"""
        # Check for functional similarity (same function names)
        func1_names = set(f.name for f in comp1.functions)
        func2_names = set(f.name for f in comp2.functions)
        func_overlap = len(func1_names.intersection(func2_names)) / max(
            len(func1_names), len(func2_names), 1
        )

        if func_overlap > 0.7:
            return "functional"
        elif len(set(comp1.classes).intersection(set(comp2.classes))) > 0:
            return "structural"
        else:
            return "semantic"

    def _determine_severity(self, similarity_score: float) -> str:
        """Determine severity level based on similarity score"""
        if similarity_score >= self.similarity_thresholds["CRITICAL"]:
            return "CRITICAL"
        elif similarity_score >= self.similarity_thresholds["HIGH"]:
            return "HIGH"
        elif similarity_score >= self.similarity_thresholds["MODERATE"]:
            return "MODERATE"
        else:
            return "LOW"

    def _find_matched_functions(
        self, functions1: List[FunctionSignature], functions2: List[FunctionSignature]
    ) -> List[Tuple[str, str]]:
        """Find matched functions between two components"""
        matches = []

        for f1 in functions1:
            for f2 in functions2:
                # Exact name match
                if f1.name == f2.name:
                    matches.append((f1.name, f2.name))
                # Similar name match (edit distance)
                elif self._calculate_string_similarity(f1.name, f2.name) > 0.8:
                    matches.append((f1.name, f2.name))

        return matches

    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings using difflib"""
        return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def _generate_analysis_summary(
        self,
        proposed: ComponentAnalysis,
        similar_components: List[DuplicationMatch],
        should_block: bool,
    ) -> Dict[str, Any]:
        """Generate human-readable analysis summary"""
        return {
            "decision": "BLOCK_COMMIT" if should_block else "ALLOW_COMMIT",
            "similar_components_found": len(similar_components),
            "highest_similarity": max(
                [m.similarity_score for m in similar_components], default=0.0
            ),
            "critical_matches": len(
                [m for m in similar_components if m.severity == "CRITICAL"]
            ),
            "high_matches": len(
                [m for m in similar_components if m.severity == "HIGH"]
            ),
            "recommendation": self._get_primary_recommendation(
                similar_components, should_block
            ),
        }

    def _get_primary_recommendation(
        self, similar_components: List[DuplicationMatch], should_block: bool
    ) -> str:
        """Get primary recommendation for the developer"""
        if should_block:
            if similar_components:
                top_match = similar_components[0]
                return f"Enhance existing component {top_match.target_file} instead of creating new component"
            else:
                return "Create ADR document before implementing new component"
        else:
            return "Proceed with implementation - no significant duplication detected"

    # Additional methods for repository scanning would go here...
    def _analyze_all_components(self) -> List[ComponentAnalysis]:
        """Analyze all components in the repository"""
        # Implementation for full repository analysis
        pass

    def _find_all_duplications(
        self, components: List[ComponentAnalysis]
    ) -> List[DuplicationMatch]:
        """Find all duplications in the repository"""
        # Implementation for finding all duplications
        pass

    def _prioritize_duplications(
        self, duplications: List[DuplicationMatch]
    ) -> List[DuplicationMatch]:
        """Prioritize duplications by severity and consolidation potential"""
        # Implementation for prioritization
        pass

    def _generate_cleanup_plan(
        self, duplications: List[DuplicationMatch]
    ) -> Dict[str, Any]:
        """Generate cleanup plan for existing duplications"""
        # Implementation for cleanup planning
        pass

    def _calculate_severity_breakdown(
        self, duplications: List[DuplicationMatch]
    ) -> Dict[str, int]:
        """Calculate breakdown of duplications by severity"""
        breakdown = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
        for dup in duplications:
            breakdown[dup.severity] += 1
        return breakdown

    def _generate_repository_summary(
        self, duplications: List[DuplicationMatch], cleanup_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate repository-wide duplication summary"""
        # Implementation for repository summary
        pass


def main():
    """Main entry point for enhanced duplication detection"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced Duplication Detection System"
    )
    parser.add_argument("--file", help="Analyze specific file for duplication")
    parser.add_argument("--content", help="Content to analyze (for pre-commit hooks)")
    parser.add_argument(
        "--scan-repository", action="store_true", help="Scan entire repository"
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )

    args = parser.parse_args()

    detector = EnhancedDuplicationDetector()

    if args.file and args.content:
        # Pre-commit analysis mode
        result = detector.analyze_new_component_request(args.file, args.content)

        if args.output_format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Analysis Result: {result['summary']['decision']}")
            print(
                f"Similar Components: {result['summary']['similar_components_found']}"
            )
            print(f"Recommendation: {result['summary']['recommendation']}")

            if result["should_block_commit"]:
                sys.exit(1)  # Block commit

    elif args.scan_repository:
        # Repository scan mode
        result = detector.scan_repository_for_duplications()

        if args.output_format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Repository Analysis Complete")
            print(f"Components Analyzed: {result['components_analyzed']}")
            print(f"Duplications Found: {result['duplications_found']}")
            print(f"Analysis Time: {result['analysis_time_seconds']:.2f}s")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
