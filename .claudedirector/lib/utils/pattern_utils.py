#!/usr/bin/env python3
"""
Pattern Matching Utilities
Centralized pattern matching logic to eliminate duplication across the system.
"""

from typing import List, Dict, Any, Tuple
import re


def match_patterns_in_content(content: str, patterns: List[str]) -> int:
    """
    Count pattern matches in content using centralized logic.

    Args:
        content: Text content to search
        patterns: List of regex patterns to match

    Returns:
        Number of pattern matches found
    """
    if not content or not patterns:
        return 0

    content_lower = content.lower()
    match_count = 0

    for pattern in patterns:
        try:
            # Use case-insensitive matching
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            match_count += len(matches)
        except re.error:
            # Handle invalid regex patterns gracefully
            continue

    return match_count


def calculate_semantic_matches(content: str, semantic_concepts: List[str]) -> int:
    """
    Calculate semantic concept matches in content.

    Args:
        content: Text content to analyze
        semantic_concepts: List of semantic concepts to find

    Returns:
        Number of semantic concept matches
    """
    if not content or not semantic_concepts:
        return 0

    content_lower = content.lower()
    matches = 0

    for concept in semantic_concepts:
        if concept.lower() in content_lower:
            matches += 1

    return matches


def extract_key_phrases(content: str, min_length: int = 3) -> List[str]:
    """
    Extract key phrases from content for pattern analysis.

    Args:
        content: Text content to analyze
        min_length: Minimum phrase length

    Returns:
        List of key phrases found
    """
    if not content:
        return []

    # Simple phrase extraction - can be enhanced with NLP
    words = re.findall(r"\b\w+\b", content.lower())
    phrases = []

    # Extract multi-word phrases
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i + 1]}"
        if len(phrase) >= min_length:
            phrases.append(phrase)

    return list(set(phrases))  # Remove duplicates
