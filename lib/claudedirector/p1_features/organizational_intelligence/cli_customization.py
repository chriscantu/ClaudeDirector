#!/usr/bin/env python3
"""
CLI Customization Interface for Organizational Leverage Intelligence
Easy configuration for directors to tailor the system to their specific context
"""

import click
import yaml
from typing import Dict, List, Optional
from pathlib import Path
from .director_profile_manager import DirectorProfileManager, DirectorRole


@click.group()
def org_intelligence():
    """Organizational Leverage Intelligence configuration commands"""
    pass


@org_intelligence.command()
@click.option(
    "--profile-type",
    type=click.Choice(
        ["platform_director", "backend_director", "product_director", "custom"]
    ),
    default="platform_director",
    help="Select director profile type",
)
@click.option(
    "--role-title", default="Director of Engineering", help="Your specific role title"
)
@click.option(
    "--primary-focus",
    default="Platform development and team enablement",
    help="Your primary organizational focus",
)
def setup(profile_type: str, role_title: str, primary_focus: str):
    """Initial setup of your organizational intelligence profile"""

    click.echo(f"🎯 Setting up Organizational Intelligence for {role_title}")
    click.echo(f"📋 Profile type: {profile_type}")
    click.echo(f"🔍 Primary focus: {primary_focus}")

    # Initialize profile manager
    manager = DirectorProfileManager()

    if profile_type == "custom":
        # Interactive custom setup
        click.echo("\n📝 Custom Profile Setup")

        strategic_priorities = []
        click.echo("\nEnter your strategic priorities (press Enter twice when done):")
        while True:
            priority = click.prompt(
                "Strategic priority", default="", show_default=False
            )
            if not priority:
                break
            strategic_priorities.append(priority)

        success_metrics = []
        click.echo("\nEnter your key success metrics (press Enter twice when done):")
        while True:
            metric = click.prompt("Success metric", default="", show_default=False)
            if not metric:
                break
            success_metrics.append(metric)

        # Update configuration file
        config_path = Path("config/p1_organizational_intelligence.yaml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        config["director_profile"] = {
            "profile_type": "custom",
            "custom_profile": {
                "role_title": role_title,
                "primary_focus": primary_focus,
                "strategic_priorities": strategic_priorities,
                "success_metrics": success_metrics,
            },
        }

        with open(config_path, "w") as f:
            yaml.dump(config, f, indent=2)

    else:
        # Use preset profile
        config_path = Path("config/p1_organizational_intelligence.yaml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        config["director_profile"]["profile_type"] = profile_type

        with open(config_path, "w") as f:
            yaml.dump(config, f, indent=2)

    click.echo(
        f"✅ Profile setup complete! Run 'claudedirector org-intelligence customize' to fine-tune."
    )


@org_intelligence.command()
def customize():
    """Interactive customization of your organizational intelligence profile"""

    manager = DirectorProfileManager()
    current_profile = manager.current_profile

    click.echo(f"🎯 Customizing profile for: {current_profile.role_title}")
    click.echo(f"📋 Current focus: {current_profile.primary_focus}")

    # Show current enabled domains
    click.echo(f"\n📊 Currently enabled measurement domains:")
    for domain_name in current_profile.enabled_domains.keys():
        click.echo(f"  ✅ {domain_name}")

    # Available domains
    config_path = Path("config/p1_organizational_intelligence.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    all_domains = (
        config.get("organizational_intelligence", {})
        .get("velocity_tracking", {})
        .get("measurement_domains", {})
    )
    available_domains = [
        name
        for name in all_domains.keys()
        if name not in current_profile.enabled_domains
    ]

    if available_domains:
        click.echo(f"\n📈 Available domains to enable:")
        for domain_name in available_domains:
            click.echo(f"  ⭕ {domain_name}")

        if click.confirm("\nWould you like to enable additional domains?"):
            for domain_name in available_domains:
                if click.confirm(f"Enable {domain_name}?"):
                    manager.customize_profile(enable_domains=[domain_name])
                    click.echo(f"✅ Enabled {domain_name}")

    # Customize weights
    if click.confirm("\nWould you like to adjust domain importance weights?"):
        click.echo("💡 Weights should total 1.0 across all enabled domains")

        new_weights = {}
        for domain_name in manager.current_profile.enabled_domains.keys():
            current_weight = 0.0
            if manager.current_profile.enabled_domains[domain_name]:
                current_weight = manager.current_profile.enabled_domains[domain_name][
                    0
                ].weight

            new_weight = click.prompt(
                f"Weight for {domain_name} (current: {current_weight})",
                type=float,
                default=current_weight,
            )
            new_weights[domain_name] = new_weight

        manager.customize_profile(update_weights=new_weights)
        click.echo("✅ Updated domain weights")

    # Save updated configuration
    updated_config = manager.generate_executive_summary()
    click.echo(f"\n📋 Updated Profile Summary:")
    click.echo(yaml.dump(updated_config, indent=2))

    click.echo("✅ Customization complete!")


@org_intelligence.command()
@click.option("--domain", help="Specific domain to configure")
def configure_domain(domain: Optional[str]):
    """Configure specific measurement domains"""

    manager = DirectorProfileManager()

    if domain:
        domains_to_configure = [domain]
    else:
        domains_to_configure = list(manager.current_profile.enabled_domains.keys())
        click.echo("🔧 Configuring all enabled domains...")

    config_path = Path("config/p1_organizational_intelligence.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    for domain_name in domains_to_configure:
        if domain_name not in manager.current_profile.enabled_domains:
            click.echo(
                f"⚠️  Domain {domain_name} is not enabled. Enable it first with 'customize' command."
            )
            continue

        click.echo(f"\n🎯 Configuring {domain_name}")

        domain_config = config["organizational_intelligence"]["velocity_tracking"][
            "measurement_domains"
        ][domain_name]

        # Configure targets
        targets = domain_config.get("targets", {})
        click.echo(f"📊 Current targets for {domain_name}:")
        for target_name, target_value in targets.items():
            click.echo(f"  {target_name}: {target_value}")

        if click.confirm(f"Update targets for {domain_name}?"):
            new_targets = {}
            for target_name, current_value in targets.items():
                new_value = click.prompt(
                    f"Target for {target_name} (current: {current_value})",
                    type=float,
                    default=current_value,
                )
                new_targets[target_name] = new_value

            # Update config
            config["organizational_intelligence"]["velocity_tracking"][
                "measurement_domains"
            ][domain_name]["targets"] = new_targets

    # Save updated configuration
    with open(config_path, "w") as f:
        yaml.dump(config, f, indent=2)

    click.echo("✅ Domain configuration updated!")


@org_intelligence.command()
def status():
    """Show current organizational intelligence configuration status"""

    manager = DirectorProfileManager()
    profile = manager.current_profile

    click.echo(f"🎯 Organizational Intelligence Status")
    click.echo(f"=" * 50)
    click.echo(f"👤 Role: {profile.role_title}")
    click.echo(f"🔍 Focus: {profile.primary_focus}")

    click.echo(f"\n📊 Enabled Measurement Domains ({len(profile.enabled_domains)}):")
    for domain_name, metrics in profile.enabled_domains.items():
        weight = metrics[0].weight if metrics else 0.0
        click.echo(f"  ✅ {domain_name} (weight: {weight:.2f})")

    click.echo(f"\n💰 Investment Categories ({len(profile.investment_categories)}):")
    for category_name, investment in profile.investment_categories.items():
        click.echo(f"  💼 {category_name} (priority: {investment.priority_weight:.2f})")

    click.echo(f"\n🎯 Strategic Priorities:")
    for priority in profile.strategic_priorities:
        click.echo(f"  • {priority}")

    click.echo(f"\n📈 Success Metrics:")
    for metric in profile.success_metrics:
        click.echo(f"  📊 {metric}")

    # Integration status
    enabled_integrations = [k for k, v in profile.integration_preferences.items() if v]
    click.echo(f"\n🔗 Active Integrations ({len(enabled_integrations)}):")
    for integration in enabled_integrations:
        click.echo(f"  🔌 {integration}")


@org_intelligence.command()
@click.option(
    "--template",
    type=click.Choice(
        [
            "design_system",
            "platform_infrastructure",
            "backend_services",
            "product_delivery",
        ]
    ),
    help="Use a predefined template",
)
def quick_setup(template: Optional[str]):
    """Quick setup using predefined templates for common director contexts"""

    templates = {
        "design_system": {
            "role_title": "Director of Engineering - UI Foundation",
            "primary_focus": "Web platform, design system, internationalization, developer experience",
            "enabled_domains": [
                "design_system_leverage",
                "platform_adoption",
                "developer_experience",
            ],
            "domain_weights": {
                "design_system_leverage": 0.35,
                "platform_adoption": 0.30,
                "developer_experience": 0.25,
                "knowledge_sharing": 0.10,
            },
            "strategic_priorities": [
                "Platform scalability and developer experience",
                "Design system adoption and consistency",
                "International expansion support",
                "Cross-team developer velocity",
            ],
        },
        "platform_infrastructure": {
            "role_title": "Director of Platform Engineering",
            "primary_focus": "Platform reliability, developer tooling, infrastructure scaling",
            "enabled_domains": [
                "platform_adoption",
                "api_service_efficiency",
                "developer_experience",
            ],
            "domain_weights": {
                "platform_adoption": 0.30,
                "api_service_efficiency": 0.35,
                "developer_experience": 0.25,
                "knowledge_sharing": 0.10,
            },
            "strategic_priorities": [
                "Platform reliability and scalability",
                "Developer productivity and tooling",
                "Infrastructure cost optimization",
                "Service performance and monitoring",
            ],
        },
        "backend_services": {
            "role_title": "Director of Backend Engineering",
            "primary_focus": "Service architecture, API design, system scalability",
            "enabled_domains": [
                "api_service_efficiency",
                "feature_delivery_impact",
                "knowledge_sharing",
            ],
            "domain_weights": {
                "api_service_efficiency": 0.40,
                "feature_delivery_impact": 0.35,
                "knowledge_sharing": 0.25,
            },
            "strategic_priorities": [
                "Service reliability and performance",
                "API design and integration quality",
                "System scalability and efficiency",
                "Cross-team service coordination",
            ],
        },
        "product_delivery": {
            "role_title": "Director of Product Engineering",
            "primary_focus": "Feature delivery, user experience, product quality",
            "enabled_domains": [
                "feature_delivery_impact",
                "developer_experience",
                "knowledge_sharing",
            ],
            "domain_weights": {
                "feature_delivery_impact": 0.40,
                "developer_experience": 0.30,
                "knowledge_sharing": 0.30,
            },
            "strategic_priorities": [
                "Feature delivery velocity and quality",
                "User experience and product outcomes",
                "Cross-functional team coordination",
                "Product-engineering alignment",
            ],
        },
    }

    if not template:
        click.echo("📋 Available quick setup templates:")
        for template_name, template_config in templates.items():
            click.echo(f"  🎯 {template_name}: {template_config['primary_focus']}")

        template = click.prompt(
            "Select template", type=click.Choice(list(templates.keys()))
        )

    template_config = templates[template]

    click.echo(f"🚀 Setting up with {template} template...")
    click.echo(f"📋 Role: {template_config['role_title']}")
    click.echo(f"🔍 Focus: {template_config['primary_focus']}")

    # Apply template to configuration
    config_path = Path("config/p1_organizational_intelligence.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Update director profile
    config["director_profile"] = {
        "profile_type": "custom",
        "custom_profile": {
            "role_title": template_config["role_title"],
            "primary_focus": template_config["primary_focus"],
            "strategic_priorities": template_config["strategic_priorities"],
            "success_metrics": list(template_config["enabled_domains"]),
        },
    }

    # Enable/disable domains based on template
    velocity_domains = config["organizational_intelligence"]["velocity_tracking"][
        "measurement_domains"
    ]
    for domain_name in velocity_domains.keys():
        if domain_name in template_config["enabled_domains"]:
            velocity_domains[domain_name]["enabled"] = True
            velocity_domains[domain_name]["weight"] = template_config[
                "domain_weights"
            ].get(domain_name, 0.1)
        else:
            velocity_domains[domain_name]["enabled"] = False

    # Save configuration
    with open(config_path, "w") as f:
        yaml.dump(config, f, indent=2)

    click.echo("✅ Quick setup complete!")
    click.echo(
        "💡 Run 'claudedirector org-intelligence status' to see your configuration"
    )
    click.echo("🔧 Run 'claudedirector org-intelligence customize' to fine-tune")


if __name__ == "__main__":
    org_intelligence()
