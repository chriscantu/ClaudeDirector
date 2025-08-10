# P1 Organizational Intelligence Setup Guide

**Complete setup workflows for different director types**

## Quick Start (5 Minutes)

### 1. Prerequisites
```bash
# Ensure you're in the ClaudeDirector project root
cd /path/to/claudedirector

# Verify CLI is available
./claudedirector --help
```

### 2. Choose Your Director Profile

#### Platform Director (UI Foundation, Design Systems)
```bash
./claudedirector org-intelligence quick-setup --template design_system
```

#### Backend Director (Services, APIs, Infrastructure)
```bash
./claudedirector org-intelligence quick-setup --template backend_services
```

#### Product Director (Features, User Experience)
```bash
./claudedirector org-intelligence quick-setup --template product_delivery
```

#### Platform Infrastructure Director (DevOps, Tooling)
```bash
./claudedirector org-intelligence quick-setup --template platform_infrastructure
```

### 3. Verify Setup
```bash
./claudedirector org-intelligence status
```

Expected output:
```
🎯 Organizational Intelligence Status
==================================================
👤 Role: Director of Engineering - UI Foundation
🔍 Focus: Web platform, design system, internationalization
📊 Enabled Measurement Domains (3):
  ✅ design_system_leverage (weight: 0.35)
  ✅ platform_adoption (weight: 0.30)
  ✅ developer_experience (weight: 0.25)
```

## Detailed Setup Workflows

### Platform Director Setup

**Use Case**: You lead web platform, design systems, UI foundation, or frontend infrastructure.

#### Step 1: Quick Template Setup
```bash
./claudedirector org-intelligence quick-setup --template design_system
```

This configures:
- **Role**: Director of Engineering - UI Foundation
- **Focus**: Web platform, design system, internationalization, developer experience
- **Domains**: Design system leverage (35%), Platform adoption (30%), Developer experience (25%), Knowledge sharing (10%)

#### Step 2: Customize for Your Context
```bash
./claudedirector org-intelligence customize
```

Interactive prompts will guide you through:
- **Enable Additional Domains**: API service efficiency, feature delivery impact
- **Adjust Weights**: Increase design system focus to 40%, reduce others proportionally
- **Set Custom Targets**: Component adoption 90%, platform adoption 85%

#### Step 3: Configure Domain Details
```bash
./claudedirector org-intelligence configure-domain --domain design_system_leverage
```

Set specific targets:
- **Component Usage Consistency**: 85% → 90% (higher standard)
- **Design Debt Reduction**: 15% → 20% (aggressive improvement)
- **Cross-Team Design Velocity**: 20% → 25% (ambitious growth)

#### Platform Director Example Configuration
```yaml
director_profile:
  profile_type: "custom"
  custom_profile:
    role_title: "Director of Engineering - UI Foundation"
    primary_focus: "Web platform, design system, internationalization"
    strategic_priorities:
      - "Platform scalability and developer experience"
      - "Design system adoption and consistency"
      - "International expansion support"
      - "Cross-team developer velocity"

organizational_intelligence:
  velocity_tracking:
    measurement_domains:
      design_system_leverage:
        enabled: true
        weight: 0.40  # Higher focus on design systems
        targets:
          component_usage_consistency: 0.90
          design_debt_reduction: 0.20
      platform_adoption:
        enabled: true
        weight: 0.30
        targets:
          adoption_rate_percentage: 0.85
          developer_satisfaction_score: 4.5
      developer_experience:
        enabled: true
        weight: 0.20
        targets:
          onboarding_efficiency: 0.65
          productivity_metrics: 0.80
      knowledge_sharing:
        enabled: true
        weight: 0.10
        targets:
          cross_team_learning_index: 0.75
```

### Backend Director Setup

**Use Case**: You lead backend services, APIs, microservices, data infrastructure.

#### Step 1: Backend Template
```bash
./claudedirector org-intelligence quick-setup --template backend_services
```

#### Step 2: Service-Specific Customization
```bash
./claudedirector org-intelligence customize
```

Focus areas to enable:
- **API Service Efficiency** (40% weight) - Core backend responsibility
- **Feature Delivery Impact** (35% weight) - Business value delivery
- **Knowledge Sharing** (25% weight) - Cross-team coordination

#### Step 3: Performance Targets
```bash
./claudedirector org-intelligence configure-domain --domain api_service_efficiency
```

Backend-specific targets:
- **API Response Times**: 200ms average, 500ms p95
- **Service Uptime**: 99.9% availability target
- **Integration Success**: 95% first-time success rate
- **Throughput**: Handle 10x current load with linear scaling

#### Backend Director Example Configuration
```yaml
organizational_intelligence:
  velocity_tracking:
    measurement_domains:
      api_service_efficiency:
        enabled: true
        weight: 0.40
        metrics: ["api_response_times", "service_uptime", "throughput", "error_rates"]
        targets:
          api_response_times: 200  # milliseconds
          service_uptime: 0.999    # 99.9%
          throughput: 1000         # requests/second
          error_rates: 0.001       # 0.1%

      feature_delivery_impact:
        enabled: true
        weight: 0.35
        targets:
          delivery_velocity: 0.85
          integration_success: 0.95

      knowledge_sharing:
        enabled: true
        weight: 0.25
        targets:
          cross_team_coordination: 0.80
          documentation_quality: 0.85
```

### Product Director Setup

**Use Case**: You lead product engineering, feature delivery, user-facing development.

#### Step 1: Product Template
```bash
./claudedirector org-intelligence quick-setup --template product_delivery
```

#### Step 2: Product-Focused Domains
Key areas:
- **Feature Delivery Impact** (40%) - Primary responsibility
- **Developer Experience** (30%) - Team productivity
- **Knowledge Sharing** (30%) - Cross-functional coordination

#### Product Director Example Configuration
```yaml
organizational_intelligence:
  velocity_tracking:
    measurement_domains:
      feature_delivery_impact:
        enabled: true
        weight: 0.40
        targets:
          feature_velocity: 0.85
          quality_score: 0.90
          user_satisfaction_impact: 4.5

      developer_experience:
        enabled: true
        weight: 0.30
        targets:
          team_satisfaction: 4.5
          productivity_metrics: 0.80

      knowledge_sharing:
        enabled: true
        weight: 0.30
        targets:
          cross_functional_alignment: 0.80
          product_engineering_sync: 0.85
```

### Custom Director Setup

**Use Case**: Unique role, multiple responsibilities, or specialized focus areas.

#### Step 1: Custom Profile Creation
```bash
./claudedirector org-intelligence setup --profile-type custom \
  --role-title "Your Specific Title" \
  --primary-focus "Your primary organizational focus"
```

#### Step 2: Interactive Domain Selection
The system will prompt for:
- **Strategic Priorities**: Enter 3-5 key priorities
- **Success Metrics**: Define measurable outcomes
- **Measurement Domains**: Choose from available domains
- **Weight Distribution**: Allocate importance across domains

#### Step 3: Advanced Configuration
```bash
./claudedirector org-intelligence customize
```

Available domains for custom configuration:
- `design_system_leverage` - Component usage, design consistency
- `platform_adoption` - Tool adoption, developer satisfaction
- `api_service_efficiency` - Performance, reliability, scalability
- `feature_delivery_impact` - Velocity, quality, user satisfaction
- `developer_experience` - Productivity, onboarding, satisfaction
- `knowledge_sharing` - Cross-team learning, documentation, coordination

## Configuration File Management

### Location
```bash
config/p1_organizational_intelligence.yaml
```

### Backup and Version Control
```bash
# Backup current configuration
cp config/p1_organizational_intelligence.yaml config/backup-$(date +%Y%m%d).yaml

# Track configuration changes
git add config/p1_organizational_intelligence.yaml
git commit -m "Update director profile configuration"
```

### Sharing Configuration Templates
```bash
# Export your configuration as a template
./claudedirector org-intelligence export-template --name "my-platform-director"

# Import a shared template
./claudedirector org-intelligence import-template --file "shared-backend-template.yaml"
```

## Integration Setup

### GitHub Integration
```bash
# Configure GitHub API access
export GITHUB_API_KEY="your-token-here"

# Test GitHub connectivity
./claudedirector metrics test-github-connection
```

### Jira Integration
```bash
# Configure Jira API access
export JIRA_API_KEY="your-token-here"
export JIRA_BASE_URL="https://yourcompany.atlassian.net"

# Test Jira connectivity
./claudedirector metrics test-jira-connection
```

### Custom Metrics Integration
```yaml
# Add custom metric sources
integrations:
  custom_metrics:
    deployment_frequency:
      source: "jenkins_api"
      endpoint: "https://jenkins.company.com/api/metrics"
      auth_method: "api_key"
```

## Validation and Testing

### Profile Validation
```bash
# Validate configuration syntax
./claudedirector org-intelligence validate

# Test profile functionality
./claudedirector org-intelligence test-profile
```

### Sample Data Testing
```bash
# Generate sample metrics for testing
./claudedirector org-intelligence generate-sample-data

# Calculate sample impact score
./claudedirector metrics calculate-impact --sample-data
```

### Dashboard Preview
```bash
# Preview dashboard with current configuration
./claudedirector dashboard preview

# Generate sample executive summary
./claudedirector reports executive-summary --sample-data
```

## Migration and Updates

### Migrating Between Profiles
```bash
# Backup current configuration
./claudedirector org-intelligence backup-profile

# Switch to new profile type
./claudedirector org-intelligence quick-setup --template backend_services

# Import selected domains from backup
./claudedirector org-intelligence import-domains --from-backup
```

### Profile Updates
```bash
# Update weights based on changing priorities
./claudedirector org-intelligence update-weights \
  --design-system=0.30 \
  --platform-adoption=0.35 \
  --developer-experience=0.35

# Add new domain to existing profile
./claudedirector org-intelligence add-domain --domain api_service_efficiency --weight 0.15
```

## Troubleshooting

### Common Setup Issues

#### Configuration File Not Found
```bash
# Create default configuration
./claudedirector org-intelligence init

# Verify file location
ls -la config/p1_organizational_intelligence.yaml
```

#### Permission Issues
```bash
# Fix configuration file permissions
chmod 644 config/p1_organizational_intelligence.yaml

# Ensure directory permissions
chmod 755 config/
```

#### YAML Syntax Errors
```bash
# Validate YAML syntax
./claudedirector org-intelligence validate-config

# Reset to default configuration
./claudedirector org-intelligence reset-config --confirm
```

### Profile Validation Errors

#### Invalid Weight Distribution
Error: "Weights must sum to 1.0"
```bash
./claudedirector org-intelligence normalize-weights
```

#### Missing Required Domains
Error: "At least one measurement domain must be enabled"
```bash
./claudedirector org-intelligence quick-setup --template platform_infrastructure
```

#### Invalid Target Values
Error: "Target values must be positive and realistic"
```bash
./claudedirector org-intelligence configure-domain --domain design_system_leverage
# Reset targets to recommended defaults
```

## Next Steps

1. **Complete Profile Setup**: Choose and configure your director profile
2. **Test Configuration**: Validate setup and generate sample data
3. **Connect Integrations**: Link GitHub, Jira, and other data sources
4. **Monitor Progress**: Track organizational intelligence metrics
5. **Optimize Performance**: Adjust domains, weights, and targets based on results

Your P1 Organizational Intelligence setup is now complete and ready for strategic decision-making! 🚀
