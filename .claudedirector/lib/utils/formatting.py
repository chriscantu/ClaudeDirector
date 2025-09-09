"""
ClaudeDirector Output Formatting and Pattern Utilities

Provides consistent formatting for CLI output across all commands.
Supports tables, lists, status messages, and various output formats.

CONSOLIDATED: Pattern matching utilities to eliminate duplicate pattern_utils.py
"""

from typing import List, Optional, Dict, Any, Tuple
import textwrap
import re


def format_table(
    headers: List[str], rows: List[List[str]], title: Optional[str] = None
) -> str:
    """Format data as a table with headers"""
    if not rows:
        return "No data to display"

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build table
    output = ""

    if title:
        output += f"\n{title}\n"
        output += "=" * len(title) + "\n\n"

    # Header row
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    output += header_row + "\n"

    # Separator
    separator = " | ".join("-" * col_widths[i] for i in range(len(headers)))
    output += separator + "\n"

    # Data rows
    for row in rows:
        data_row = " | ".join(
            (
                str(row[i]).ljust(col_widths[i])
                if i < len(row)
                else "".ljust(col_widths[i])
            )
            for i in range(len(headers))
        )
        output += data_row + "\n"

    return output


def format_list(items: List[str], style: str = "bullet") -> str:
    """Format a list of items with consistent styling"""
    if not items:
        return "None"

    if style == "bullet":
        return "\n".join(f"• {item}" for item in items)
    elif style == "numbered":
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
    elif style == "dash":
        return "\n".join(f"- {item}" for item in items)
    else:
        return "\n".join(items)


def format_success(message: str) -> str:
    """Format a success message"""
    return f"✅ {message}"


def format_warning(message: str) -> str:
    """Format a warning message"""
    return f"⚠️  {message}"


def format_error(message: str) -> str:
    """Format an error message"""
    return f"❌ {message}"


def format_info(message: str) -> str:
    """Format an info message"""
    return f"ℹ️  {message}"


def format_section(title: str, content: str, level: int = 1) -> str:
    """Format a section with title and content"""
    if level == 1:
        separator = "=" * len(title)
        return f"\n{title}\n{separator}\n\n{content}\n"
    elif level == 2:
        separator = "-" * len(title)
        return f"\n{title}\n{separator}\n\n{content}\n"
    else:
        return f"\n### {title}\n\n{content}\n"


def format_key_value_pairs(pairs: List[tuple], indent: int = 0) -> str:
    """Format key-value pairs consistently"""
    indent_str = " " * indent
    max_key_length = max(len(str(k)) for k, v in pairs) if pairs else 0

    formatted_pairs = []
    for key, value in pairs:
        padded_key = str(key).ljust(max_key_length)
        formatted_pairs.append(f"{indent_str}{padded_key}: {value}")

    return "\n".join(formatted_pairs)


def format_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Format a simple progress bar"""
    if total == 0:
        return "Progress: N/A"

    percentage = current / total
    filled_width = int(width * percentage)
    bar = "█" * filled_width + "░" * (width - filled_width)

    return f"Progress: [{bar}] {current}/{total} ({percentage:.1%})"


def format_status_indicator(status: str) -> str:
    """Format status with appropriate indicator"""
    status_lower = status.lower()

    if status_lower in ["completed", "success", "passed", "active"]:
        return f"✅ {status}"
    elif status_lower in ["pending", "waiting", "queued"]:
        return f"⏳ {status}"
    elif status_lower in ["failed", "error", "critical"]:
        return f"❌ {status}"
    elif status_lower in ["warning", "caution"]:
        return f"⚠️  {status}"
    elif status_lower in ["info", "information"]:
        return f"ℹ️  {status}"
    else:
        return f"• {status}"


def format_multiline_text(text: str, width: int = 80, indent: int = 0) -> str:
    """Format multiline text with consistent wrapping and indentation"""
    lines = text.split("\n")
    formatted_lines = []

    indent_str = " " * indent

    for line in lines:
        if not line.strip():
            formatted_lines.append("")
        else:
            wrapped = textwrap.fill(
                line,
                width=width - indent,
                initial_indent=indent_str,
                subsequent_indent=indent_str,
            )
            formatted_lines.append(wrapped)

    return "\n".join(formatted_lines)


def format_duration(seconds: float) -> str:
    """Format duration in a human-readable way"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_file_size(bytes_size: int) -> str:
    """Format file size in human-readable units"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def format_template_preview(template_data: dict) -> str:
    """Format template data for preview display"""
    output = f"**{template_data.get('display_name', 'Unknown Template')}**\n"
    output += f"Domain: {template_data.get('domain', 'Unknown')}\n"

    if "description" in template_data:
        description = format_multiline_text(
            template_data["description"], width=70, indent=0
        )
        output += f"Description: {description}\n"

    if "primary_personas" in template_data:
        personas = ", ".join(template_data["primary_personas"][:3])
        if len(template_data["primary_personas"]) > 3:
            personas += "..."
        output += f"Primary Personas: {personas}\n"

    return output


def format_comparison_table(comparison_data: dict) -> str:
    """Format template comparison data as a readable table"""
    templates = comparison_data.get("templates", {})

    if not templates:
        return "No templates to compare"

    # Extract template names for headers
    template_names = [templates[tid]["display_name"] for tid in templates.keys()]
    headers = ["Aspect"] + template_names

    rows = []

    # Domain comparison
    domains = [templates[tid]["domain"] for tid in templates.keys()]
    rows.append(["Domain"] + domains)

    # Primary personas comparison
    personas = []
    for tid in templates.keys():
        template_personas = templates[tid].get("primary_personas", [])
        persona_str = ", ".join(template_personas[:2])
        if len(template_personas) > 2:
            persona_str += "..."
        personas.append(persona_str)
    rows.append(["Primary Personas"] + personas)

    return format_table(headers, rows, title="Template Comparison")


def format_validation_result(result: dict) -> str:
    """Format template validation result"""
    if not result.get("valid", False):
        return format_error(
            f"Validation failed: {result.get('error', 'Unknown error')}"
        )

    output = format_success("Template selection is valid")

    warnings = result.get("warnings", [])
    if warnings:
        output += "\n\nWarnings:\n"
        for warning in warnings:
            output += f"  {format_warning(warning)}\n"

    return output


def format_discovery_results(results: List[tuple], context: str) -> str:
    """Format template discovery results"""
    if not results:
        return format_warning(f"No templates found for context: '{context}'")

    output = f"**Discovery Results for '{context}':**\n\n"

    for i, (template, confidence) in enumerate(results[:5], 1):
        confidence_pct = int(confidence * 100)
        output += f"{i}. **{template.display_name}** ({confidence_pct}% match)\n"
        output += f"   Domain: {template.domain}\n"
        output += f"   Personas: {', '.join(template.personas.primary[:3])}\n"

        # Truncate description if too long
        description = template.description
        if len(description) > 100:
            description = description[:97] + "..."
        output += f"   Description: {description}\n\n"

    if len(results) > 5:
        output += f"... and {len(results) - 5} more results\n"

    return output


# ===== CONSOLIDATED PATTERN MATCHING UTILITIES =====
# Eliminates duplicate pattern_utils.py (88 lines)

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
    words = re.findall(r"\\b\\w+\\b", content.lower())
    phrases = []
    
    # Extract multi-word phrases
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i + 1]}"
        if len(phrase) >= min_length:
            phrases.append(phrase)
            
    return list(set(phrases))  # Remove duplicates
