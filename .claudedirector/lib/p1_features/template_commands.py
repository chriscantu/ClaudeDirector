"""
ClaudeDirector Template Management CLI Commands

Provides command-line interface for template discovery, selection, and management.
Integrates with the existing claudedirector command system.

Part of Phase 1 implementation for director template expansion.
"""

import json
from typing import Optional, List
import click

from ..core.template_engine import TemplateDiscoveryEngine
from ..utils.formatting import (
    format_table,
    format_list,
    format_success,
    format_warning,
    format_error,
)

# Configuration constants
DEFAULT_CONFIDENCE_THRESHOLD = 0.6


class TemplateCommands:
    """Template management command implementations"""

    def __init__(self, template_engine=None):
        self.template_engine = template_engine or TemplateDiscoveryEngine()

    def list_templates(
        self, domain: Optional[str] = None, format_type: str = "table"
    ) -> str:
        """List available director templates"""
        try:
            templates = self.template_engine.list_templates(domain_filter=domain)

            if not templates:
                filter_msg = f" for domain '{domain}'" if domain else ""
                return format_warning(f"No templates found{filter_msg}")

            if format_type == "json":
                template_data = [
                    {
                        "id": t.template_id,
                        "name": t.display_name,
                        "domain": t.domain,
                        "description": t.description,
                        "primary_personas": t.personas.primary,
                    }
                    for t in templates
                ]
                return json.dumps(template_data, indent=2)

            # Table format
            headers = ["Template ID", "Display Name", "Domain", "Primary Personas"]
            rows = [
                [
                    t.template_id,
                    t.display_name,
                    t.domain,
                    ", ".join(t.personas.primary[:2])
                    + ("..." if len(t.personas.primary) > 2 else ""),
                ]
                for t in templates
            ]

            return format_table(headers, rows, title="Available Director Templates")

        except Exception as e:
            return format_error(f"Failed to list templates: {e}")

    def get_template_details(self, template_id: str, format_type: str = "yaml") -> str:
        """Get detailed information about a specific template"""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                return format_error(f"Template not found: {template_id}")

            if format_type == "json":
                details = {
                    "template_id": template.template_id,
                    "display_name": template.display_name,
                    "domain": template.domain,
                    "description": template.description,
                    "personas": {
                        "primary": template.personas.primary,
                        "contextual": template.personas.contextual,
                        "fallback": template.personas.fallback,
                    },
                    "strategic_priorities": template.strategic_priorities,
                    "metrics_focus": template.metrics_focus,
                    "industry_modifiers": list(template.industry_modifiers.keys()),
                    "team_size_contexts": list(template.team_size_contexts.keys()),
                }
                return json.dumps(details, indent=2)

            # YAML format (default)
            output = f"""
# {template.display_name}
## Template Details

**Template ID**: {template.template_id}
**Domain**: {template.domain}
**Description**: {template.description}

## Personas
- **Primary**: {', '.join(template.personas.primary)}
- **Contextual**: {', '.join(template.personas.contextual)}
- **Fallback**: {', '.join(template.personas.fallback)}

## Strategic Priorities
{format_list(template.strategic_priorities)}

## Metrics Focus
{format_list(template.metrics_focus)}

## Available Industry Modifiers
{format_list(list(template.industry_modifiers.keys())) if template.industry_modifiers else "None"}

## Available Team Size Contexts
{format_list(list(template.team_size_contexts.keys())) if template.team_size_contexts else "None"}
"""
            return output.strip()

        except Exception as e:
            return format_error(f"Failed to get template details: {e}")

    def discover_by_context(
        self, context: str, threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    ) -> str:
        """Discover templates based on context keywords"""
        try:
            results = self.template_engine.discover_templates_by_context(
                context, threshold
            )

            if not results:
                return format_warning(f"No templates found for context: '{context}'")

            output = f"**Template Discovery Results for**: '{context}'\n\n"

            for i, (template, confidence) in enumerate(results[:5], 1):  # Top 5 results
                confidence_percent = int(confidence * 100)
                output += (
                    f"**{i}. {template.display_name}** ({confidence_percent}% match)\n"
                )
                output += f"   - **Domain**: {template.domain}\n"
                output += f"   - **Primary Personas**: {', '.join(template.personas.primary)}\n"
                output += f"   - **Description**: {template.description}\n"
                output += "\n"

            if len(results) > 5:
                output += f"... and {len(results) - 5} more results\n"

            return output

        except Exception as e:
            return format_error(f"Failed to discover templates: {e}")

    def validate_selection(
        self,
        template_id: str,
        industry: Optional[str] = None,
        team_size: Optional[str] = None,
    ) -> str:
        """Validate a template selection"""
        try:
            result = self.template_engine.validate_template_selection(
                template_id, industry, team_size
            )

            if not result["valid"]:
                return format_error(result["error"])

            template = result["template"]
            output = format_success(
                f"✅ Template selection valid: {template.display_name}"
            )

            if result.get("warnings"):
                output += "\n\n**Warnings:**\n"
                for warning in result["warnings"]:
                    output += f"⚠️  {warning}\n"

            return output

        except Exception as e:
            return format_error(f"Failed to validate selection: {e}")

    def generate_summary(
        self,
        template_id: str,
        industry: Optional[str] = None,
        team_size: Optional[str] = None,
    ) -> str:
        """Generate comprehensive template summary"""
        try:
            summary = self.template_engine.generate_template_summary(
                template_id, industry, team_size
            )

            if "error" in summary:
                return format_error(summary["error"])

            output = f"""
# {summary['display_name']} - Configuration Summary

**Template ID**: {summary['template_id']}
**Domain**: {summary['domain']}
**Description**: {summary['description']}

## Primary Personas
{format_list(summary['primary_personas'])}

## Strategic Priorities
{format_list(summary['strategic_priorities'])}

## Metrics Focus
{format_list(summary['metrics_focus'])}
"""

            # Add industry enhancements if present
            if "industry_enhancements" in summary:
                enhancements = summary["industry_enhancements"]
                output += "\n## Industry-Specific Enhancements\n"
                if "enhanced_priorities" in enhancements:
                    output += f"**Enhanced Priorities**: {format_list(enhancements['enhanced_priorities'][-3:])}\n"  # Last 3 additions
                if "enhanced_metrics" in enhancements:
                    output += f"**Enhanced Metrics**: {format_list(enhancements['enhanced_metrics'][-3:])}\n"  # Last 3 additions

            # Add team size context if present
            if "team_size_context" in summary:
                context = summary["team_size_context"]
                output += "\n## Team Size Context\n"
                if "focus_areas" in context:
                    output += (
                        f"**Focus Areas**: {format_list(context['focus_areas'])}\n"
                    )
                if "key_challenges" in context:
                    output += f"**Key Challenges**: {format_list(context['key_challenges'])}\n"

            return output.strip()

        except Exception as e:
            return format_error(f"Failed to generate summary: {e}")

    def compare_templates(self, template_ids: List[str]) -> str:
        """Compare multiple templates side by side"""
        try:
            comparison = self.template_engine.get_template_comparison(template_ids)

            if "error" in comparison:
                return format_error(comparison["error"])

            output = "# Template Comparison\n\n"

            # Create comparison table
            templates = comparison["templates"]
            if not templates:
                return format_warning("No valid templates found for comparison")

            headers = ["Aspect"] + [
                templates[tid]["display_name"]
                for tid in template_ids
                if tid in templates
            ]

            rows = []

            # Domain comparison
            domain_row = ["Domain"] + [
                templates[tid]["domain"] for tid in template_ids if tid in templates
            ]
            rows.append(domain_row)

            # Primary personas comparison
            personas_row = ["Primary Personas"] + [
                ", ".join(templates[tid]["primary_personas"][:2])
                + ("..." if len(templates[tid]["primary_personas"]) > 2 else "")
                for tid in template_ids
                if tid in templates
            ]
            rows.append(personas_row)

            output += format_table(headers, rows, title="Template Comparison")

            # Individual template details
            output += "\n## Template Details\n\n"
            for template_id in template_ids:
                if template_id in templates:
                    template_data = templates[template_id]
                    output += f"### {template_data['display_name']}\n"
                    output += f"**Description**: {template_data['description']}\n"
                    output += f"**Strategic Priorities**: {', '.join(template_data['strategic_priorities'])}\n"
                    output += f"**Metrics Focus**: {', '.join(template_data['metrics_focus'])}\n\n"

            return output

        except Exception as e:
            return format_error(f"Failed to compare templates: {e}")

    def list_domains(self) -> str:
        """List available template domains"""
        try:
            domains = self.template_engine.get_domains()

            if not domains:
                return format_warning("No template domains found")

            output = "**Available Template Domains:**\n\n"
            for domain in domains:
                # Count templates in this domain
                templates = self.template_engine.list_templates(domain_filter=domain)
                template_count = len(templates)
                output += f"- **{domain}** ({template_count} template{'s' if template_count != 1 else ''})\n"

            return output

        except Exception as e:
            return format_error(f"Failed to list domains: {e}")


# CLI command integration functions
def create_template_commands():
    """Create template management CLI commands for integration with claudedirector"""
    template_commands = TemplateCommands()

    @click.group()
    def templates():
        """Director template management commands"""

    @templates.command()
    @click.option("--domain", help="Filter by template domain")
    @click.option(
        "--format",
        "format_type",
        default="table",
        type=click.Choice(["table", "json"]),
        help="Output format",
    )
    def list(domain, format_type):
        """List available director templates"""
        result = template_commands.list_templates(domain, format_type)
        click.echo(result)

    @templates.command()
    @click.argument("template_id")
    @click.option(
        "--format",
        "format_type",
        default="yaml",
        type=click.Choice(["yaml", "json"]),
        help="Output format",
    )
    def show(template_id, format_type):
        """Show detailed information about a template"""
        result = template_commands.get_template_details(template_id, format_type)
        click.echo(result)

    @templates.command()
    @click.argument("context")
    @click.option(
        "--threshold",
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        type=float,
        help="Confidence threshold (0.0-1.0)",
    )
    def discover(context, threshold):
        """Discover templates based on context keywords"""
        result = template_commands.discover_by_context(context, threshold)
        click.echo(result)

    @templates.command()
    @click.argument("template_id")
    @click.option("--industry", help="Industry modifier")
    @click.option("--team-size", help="Team size context")
    def validate(template_id, industry, team_size):
        """Validate a template selection"""
        result = template_commands.validate_selection(template_id, industry, team_size)
        click.echo(result)

    @templates.command()
    @click.argument("template_id")
    @click.option("--industry", help="Industry modifier")
    @click.option("--team-size", help="Team size context")
    def summary(template_id, industry, team_size):
        """Generate template configuration summary"""
        result = template_commands.generate_summary(template_id, industry, team_size)
        click.echo(result)

    @templates.command()
    @click.argument("template_ids", nargs=-1, required=True)
    def compare(template_ids):
        """Compare multiple templates side by side"""
        if len(template_ids) < 2:
            click.echo(format_error("Need at least 2 templates to compare"))
            return
        result = template_commands.compare_templates(list(template_ids))
        click.echo(result)

    @templates.command()
    def domains():
        """List available template domains"""
        result = template_commands.list_domains()
        click.echo(result)

    return templates
