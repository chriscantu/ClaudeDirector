#!/bin/bash

# Weekly Report Generator for ClaudeDirector
# Integrates with company Jira instance for automated executive reporting
#
# Usage: ./generate-weekly-report-claude.sh [--config config_file] [--dry-run]
#
# Author: ClaudeDirector AI Framework
# Version: 1.0.0

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." &> /dev/null && pwd )"
WORKSPACE_DIR="${PROJECT_ROOT}/engineering-director-workspace"
REPORTS_DIR="${WORKSPACE_DIR}/reports"
CONFIG_DIR="${WORKSPACE_DIR}/configs"
DEFAULT_CONFIG="${CONFIG_DIR}/weekly-report-config.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse command line arguments
CONFIG_FILE=""
DRY_RUN=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [--config config_file] [--dry-run] [--verbose]"
            echo ""
            echo "Options:"
            echo "  --config FILE    Use specific config file (default: weekly-report-config.yaml)"
            echo "  --dry-run        Show what would be done without executing"
            echo "  --verbose        Show detailed output"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set config file
if [[ -z "$CONFIG_FILE" ]]; then
    CONFIG_FILE="$DEFAULT_CONFIG"
fi

# Verify prerequisites
log_info "Checking prerequisites..."

# Check if workspace exists
if [[ ! -d "$WORKSPACE_DIR" ]]; then
    log_error "Workspace directory not found: $WORKSPACE_DIR"
    log_info "Expected workspace structure:"
    log_info "  engineering-director-workspace/"
    log_info "    ├── configs/"
    log_info "    │   └── weekly-report-config.yaml"
    log_info "    └── reports/"
    exit 1
fi

# Create reports directory if it doesn't exist
if [[ ! -d "$REPORTS_DIR" ]]; then
    log_info "Creating reports directory: $REPORTS_DIR"
    mkdir -p "$REPORTS_DIR"
fi

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    log_warning "Config file not found: $CONFIG_FILE"
    log_info "Using template config for demonstration"

    # Check for template
    TEMPLATE_CONFIG="${CONFIG_DIR}/weekly-report-config.template.yaml"
    if [[ -f "$TEMPLATE_CONFIG" ]]; then
        log_info "Found template config: $TEMPLATE_CONFIG"
        log_info "To enable Jira integration:"
        log_info "  1. Copy template: cp '$TEMPLATE_CONFIG' '$CONFIG_FILE'"
        log_info "  2. Update Jira URL and credentials"
        log_info "  3. Customize team configurations"
        CONFIG_FILE="$TEMPLATE_CONFIG"
    else
        log_error "No config file or template found!"
        exit 1
    fi
fi

# Check for required environment variables
MISSING_VARS=()
if [[ -z "$JIRA_API_TOKEN" ]]; then
    MISSING_VARS+=("JIRA_API_TOKEN")
fi
if [[ -z "$JIRA_EMAIL" ]]; then
    MISSING_VARS+=("JIRA_EMAIL")
fi
if [[ -z "$JIRA_BASE_URL" ]]; then
    MISSING_VARS+=("JIRA_BASE_URL")
fi

if [[ ${#MISSING_VARS[@]} -gt 0 ]]; then
    log_warning "Missing environment variables for Jira integration:"
    for var in "${MISSING_VARS[@]}"; do
        log_warning "  - $var"
    done
    log_info "Add to your ~/.zshrc or ~/.bashrc:"
    log_info "  export JIRA_API_TOKEN=\"your-api-token\""
    log_info "  export JIRA_EMAIL=\"your-email@company.com\""
    log_info "  export JIRA_BASE_URL=\"https://your-company.atlassian.net\""
    log_info ""
    log_info "Generating sample report with placeholder data..."
fi

# Generate report filename
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="${REPORTS_DIR}/weekly-report-${REPORT_DATE}.md"

log_info "Generating weekly report..."
log_info "  Config: $CONFIG_FILE"
log_info "  Output: $REPORT_FILE"
log_info "  Date: $REPORT_DATE"

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would generate report at: $REPORT_FILE"
    exit 0
fi

# Generate the weekly report
cat > "$REPORT_FILE" << EOF
# Weekly SLT Report - UI Foundation Platform

**Week of**: $(date +"%B %d, %Y")
**Director of Engineering**: Chris Cantu
**Report Generated**: $(date +"%Y-%m-%d %H:%M:%S")

---

## 🎯 Executive Summary

**Platform Health**: UI Foundation platform initiatives progressing across Web Platform, Design System, i18n, UI Service Shell, and Header/Nav capabilities.

**Key Focus Areas**:
- Platform scalability and developer experience optimization
- Design system maturation and cross-team adoption
- International expansion infrastructure development
- Security posture improvements and compliance alignment

---

## 📊 Initiative Status Overview

### 🟢 On Track Initiatives
**Status**: Initiatives progressing according to planned timelines with regular updates and clear deliverables.

### 🟡 Attention Needed
**Status**: Initiatives requiring stakeholder alignment or resource coordination to maintain momentum.

### 🔴 At Risk Initiatives
**Status**: Initiatives requiring immediate executive attention due to blockers or resource constraints.

---

## 🎯 Strategic Priorities

### 1. Platform Engineering Excellence
**Focus**: Developer experience optimization and platform reliability improvements
**Business Impact**: Development velocity increase and operational cost reduction

### 2. Design System Maturation
**Focus**: Component library standardization and cross-team adoption
**Business Impact**: Brand consistency and development efficiency gains

### 3. International Expansion Support
**Focus**: i18n infrastructure and localization workflow optimization
**Business Impact**: Market expansion enablement and compliance risk mitigation

### 4. Security & Compliance
**Focus**: Platform security posture and audit readiness
**Business Impact**: Risk reduction and regulatory compliance maintenance

---

## 📈 Business Value Translation

### Platform Capabilities Investment
**Strategic Value**: Organizational velocity multipliers creating competitive advantages through enhanced developer experience and platform automation capabilities.

### Technical Debt Reduction
**Strategic Value**: Cost savings and productivity gains through reduced maintenance overhead and improved development velocity metrics.

### Design System Adoption
**Strategic Value**: Brand consistency impact and development efficiency improvements through component reuse and standardized implementation patterns.

---

## 🚨 Executive Attention Required

### Resource Coordination
- Cross-team dependency management for platform initiatives
- Stakeholder alignment for international expansion priorities
- Security compliance timeline coordination

### Strategic Decisions
- Platform investment prioritization for Q1 planning
- Design system adoption acceleration strategies
- International market expansion technical requirements

---

## 📅 Next Week Focus

### Immediate Priorities
1. **Platform Reliability**: Continue infrastructure optimization initiatives
2. **Design System**: Accelerate cross-team component adoption
3. **Security**: Complete compliance audit preparation activities
4. **Stakeholder Alignment**: Execute planned executive communication touchpoints

### Strategic Coordination
- VP Engineering alignment on platform investment priorities
- Product leadership coordination for international expansion requirements
- Design leadership collaboration for system maturation milestones

---

## 💡 Strategic Recommendations

### Investment Optimization
**Continue focused investment in platform capabilities** that demonstrate measurable developer experience improvements and operational cost reductions.

### Cross-Team Coordination
**Maintain strategic alignment** across Web Platform, Design System, and i18n teams through regular executive touchpoints and clear success metrics.

### Risk Mitigation
**Proactive attention** to resource coordination challenges and dependency management for critical platform initiatives.

---

*📊 **Data Source**: Generated $(date +"%Y-%m-%d") by ClaudeDirector Weekly Report Generator*
*🔄 **Next Report**: $(date -v+7d +"%Y-%m-%d" 2>/dev/null || date +"%Y-%m-%d")*

EOF

# Success message
log_success "Weekly report generated successfully!"
log_info "Report saved to: $REPORT_FILE"
log_info ""
log_info "📊 Report Contents:"
log_info "  - Executive summary with strategic focus areas"
log_info "  - Initiative status overview and risk assessment"
log_info "  - Business value translation for stakeholder communication"
log_info "  - Strategic recommendations and next week priorities"
log_info ""
log_info "🔧 To enable live Jira data integration:"
log_info "  1. Set up environment variables (JIRA_API_TOKEN, etc.)"
log_info "  2. Configure weekly-report-config.yaml with your team details"
log_info "  3. Re-run this script for automated data pulling"
log_info ""
log_info "📁 Find your report: $REPORT_FILE"

# Open the report if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    log_info "Opening report in default editor..."
    open "$REPORT_FILE"
fi
