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

# Jira API integration functions
fetch_jira_data() {
    local jql_query="$1"
    local max_results="${2:-100}"

    if [[ -z "$JIRA_API_TOKEN" || -z "$JIRA_EMAIL" || -z "$JIRA_BASE_URL" ]]; then
        log_warning "Jira credentials not configured - using template data"
        return 1
    fi

    log_info "Fetching data from Jira..."
    log_info "Query: $jql_query"

    # Encode the JQL query for URL
    local encoded_jql=$(printf '%s' "$jql_query" | jq -sRr @uri)

    # Make API call to Jira
    local response=$(curl -s \
        -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
        -H "Accept: application/json" \
        "${JIRA_BASE_URL}/rest/api/3/search?jql=${encoded_jql}&maxResults=${max_results}&fields=key,summary,status,assignee,project,priority,updated,parent")

    if [[ $? -eq 0 ]]; then
        echo "$response" > /tmp/jira_data.json
        log_success "Successfully fetched $(echo "$response" | jq -r '.total // 0') issues from Jira"
        return 0
    else
        log_error "Failed to fetch data from Jira API"
        return 1
    fi
}

format_jira_issues() {
    local json_file="$1"
    local section_title="$2"

    if [[ ! -f "$json_file" ]]; then
        echo "No data available"
        return
    fi

    local total=$(jq -r '.total // 0' "$json_file")
    if [[ "$total" -eq 0 ]]; then
        echo "No issues found"
        return
    fi

    echo ""
    echo "**Total: $total issues**"
    echo ""

    # Group by project and format
    jq -r '.issues[] | "\(.fields.project.name)|\(.key)|\(.fields.summary)|\(.fields.status.name)|\(.fields.assignee.displayName // "Unassigned")|\(.fields.priority.name // "None")|\(.fields.updated)"' "$json_file" | \
    while IFS='|' read -r project key summary status assignee priority updated; do
        # Format the date
        formatted_date=$(echo "$updated" | cut -d'T' -f1)

        # Determine status emoji
        case "$status" in
            "Done"|"Closed"|"Resolved") status_emoji="✅" ;;
            "In Progress"|"In Review") status_emoji="🔄" ;;
            "Blocked"|"On Hold") status_emoji="🔴" ;;
            *) status_emoji="📋" ;;
        esac

        echo "- **[$key]** $summary"
        echo "  - 📂 Project: $project"
        echo "  - $status_emoji Status: $status"
        echo "  - 👤 Assignee: $assignee"
        echo "  - ⚡ Priority: $priority"
        echo "  - 📅 Updated: $formatted_date"
        echo ""
    done
}

# Parse command line arguments
CONFIG_FILE=""
DRY_RUN=false
VERBOSE=false
JQL_QUERY_NAME="weekly_completed_items"

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
        --query)
            JQL_QUERY_NAME="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--config config_file] [--dry-run] [--verbose] [--query query_name]"
            echo ""
            echo "Options:"
            echo "  --config FILE      Use specific config file (default: weekly-report-config.yaml)"
            echo "  --dry-run          Show what would be done without executing"
            echo "  --verbose          Show detailed output"
            echo "  --query NAME       Use specific JQL query from config (default: weekly_completed_items)"
            echo "                     Available: weekly_completed_items, at_risk_items, current_sprint_items"
            echo "  --help             Show this help message"
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

# Check for required tools
if ! command -v jq &> /dev/null; then
    log_warning "jq is not installed. Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    log_info "Jira integration will be disabled without jq"
fi

if ! command -v curl &> /dev/null; then
    log_error "curl is not installed. Please install curl to enable Jira integration."
fi

# Function to extract JQL query from config file
extract_jql_query() {
    local config_file="$1"
    local query_name="${2:-weekly_completed_items}"

    if ! [[ -f "$config_file" ]]; then
        log_error "Config file not found: $config_file"
        return 1
    fi

    # Try using yq if available (preferred method)
    if command -v yq &> /dev/null; then
        local query=$(yq eval ".jql_queries.${query_name}" "$config_file" 2>/dev/null)
        if [[ "$query" != "null" && -n "$query" ]]; then
            echo "$query"
            return 0
        fi
    fi

    # Fallback: Python-based YAML parsing (more reliable)
    if command -v python3 &> /dev/null; then
        local query=$(python3 -c "
import yaml
import sys
try:
    with open('$config_file', 'r') as f:
        config = yaml.safe_load(f)
    query = config.get('jql_queries', {}).get('$query_name', '')
    if query:
        print(query)
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    sys.exit(1)
" 2>/dev/null)

        if [[ $? -eq 0 && -n "$query" ]]; then
            echo "$query"
            return 0
        fi
    fi

    # Last resort: grep/awk extraction for simple cases
    local query=$(awk "/^[[:space:]]*${query_name}:/ { getline; gsub(/^[[:space:]]*['\"]?/, \"\"); gsub(/['\"]?[[:space:]]*$/, \"\"); print }" "$config_file")

    if [[ -n "$query" ]]; then
        echo "$query"
        return 0
    else
        log_error "Could not extract JQL query '$query_name' from config file"
        log_error "Available extraction methods failed. Consider installing 'yq' for better YAML parsing."
        return 1
    fi
}

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

# Extract JQL query from config file (even in dry-run to validate config)
log_info "Reading JQL query '$JQL_QUERY_NAME' from config file: $CONFIG_FILE"
JQL_QUERY=$(extract_jql_query "$CONFIG_FILE" "$JQL_QUERY_NAME")

if [[ $? -ne 0 || -z "$JQL_QUERY" ]]; then
    log_error "Failed to extract JQL query from config file"
    log_info "Please ensure your config file contains:"
    log_info "  jql_queries:"
    log_info "    weekly_completed_items: 'YOUR_JQL_QUERY_HERE'"
    exit 1
fi

# Show JQL query in verbose mode or dry-run
if [[ "$VERBOSE" == "true" || "$DRY_RUN" == "true" ]]; then
    log_info "Using JQL Query: $JQL_QUERY"
fi

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would generate report at: $REPORT_FILE"
    log_info "DRY RUN: Config validation successful - JQL query extracted successfully"
    exit 0
fi

# Fetch live data from Jira

if fetch_jira_data "$JQL_QUERY" 100; then
    log_info "Successfully connected to Jira - generating report with live data"
    USE_LIVE_DATA=true
else
    log_warning "Could not connect to Jira - generating template report"
    USE_LIVE_DATA=false
fi

# Generate the weekly report with live or template data
if [[ "$USE_LIVE_DATA" == "true" ]]; then
    # Generate report with live Jira data
    cat > "$REPORT_FILE" << EOF
# Weekly SLT Report - UI Foundation Platform

**Week of**: $(date +"%B %d, %Y")
**Director of Engineering**: Chris Cantu
**Report Generated**: $(date +"%Y-%m-%d %H:%M:%S")
**Data Source**: Live Jira Data

---

## 🎯 Executive Summary

**Platform Health**: UI Foundation platform initiatives with **$(jq -r '.total // 0' /tmp/jira_data.json) completed deliverables** this week across Web Platform, Design System, i18n, UI Service Shell, and Header/Nav capabilities.

**Key Achievements This Week**:
$(jq -r '.issues[] | .fields.project.name' /tmp/jira_data.json | sort | uniq -c | sed 's/^[ ]*/- /' | sed 's/\([0-9]*\) \(.*\)/\1 items completed in \2/')

---

## 📊 Completed Deliverables This Week

### Items Delivered ($(jq -r '.total // 0' /tmp/jira_data.json) total)

$(format_jira_issues "/tmp/jira_data.json" "Completed Items")

---

## 🎯 Strategic Impact Analysis

### Platform Engineering Excellence
**This Week**: $(jq -r '.issues[] | select(.fields.project.name | contains("Web Platform")) | .key' /tmp/jira_data.json | wc -l | tr -d ' ') Web Platform deliverables completed
**Business Impact**: Development velocity improvements and operational efficiency gains

### Design System Maturation
**This Week**: $(jq -r '.issues[] | select(.fields.project.name | contains("Design Systems")) | .key' /tmp/jira_data.json | wc -l | tr -d ' ') Design System deliverables completed
**Business Impact**: Brand consistency and development efficiency improvements

### Experience & Onboarding
**This Week**: $(jq -r '.issues[] | select(.fields.project.name | test("Experience|Onboarding|Hubs")) | .key' /tmp/jira_data.json | wc -l | tr -d ' ') user experience deliverables completed
**Business Impact**: User satisfaction and onboarding optimization

### Global Expansion
**This Week**: $(jq -r '.issues[] | select(.fields.project.name | contains("Globalizers")) | .key' /tmp/jira_data.json | wc -l | tr -d ' ') internationalization deliverables completed
**Business Impact**: Market expansion enablement and localization improvements

---

## 📈 Business Value Translation

### Velocity Achievements
**Delivered**: $(jq -r '.total // 0' /tmp/jira_data.json) completed initiatives demonstrating **strong execution velocity** across all UI Foundation platform capabilities.

### Cross-Team Coordination
**Platform Coverage**: $(jq -r '.issues[] | .fields.project.name' /tmp/jira_data.json | sort | uniq | wc -l | tr -d ' ') active project areas with synchronized delivery execution.

### Quality & Reliability
**Systematic Delivery**: All completed items follow **Honorably Discharged** exclusion criteria, ensuring quality-focused completion standards.

---

## 🚨 Executive Highlights

### Week's Major Accomplishments
$(jq -r '.issues[] | select(.fields.priority.name == "Critical" or .fields.priority.name == "High") | "- **[\(.key)]** \(.fields.summary) (\(.fields.project.name))"' /tmp/jira_data.json 2>/dev/null || echo "- Strong execution across all priority levels")

### Resource Utilization
**Team Distribution**: Deliverables completed across $(jq -r '.issues[] | .fields.assignee.displayName // "Unassigned"' /tmp/jira_data.json | grep -v "Unassigned" | sort | uniq | wc -l | tr -d ' ') team members, demonstrating **effective resource allocation**.

---

## 📅 Strategic Outlook

### Momentum Indicators
✅ **$(jq -r '.total // 0' /tmp/jira_data.json) deliverables completed** - Strong execution velocity
✅ **$(jq -r '.issues[] | .fields.project.name' /tmp/jira_data.json | sort | uniq | wc -l | tr -d ' ') project areas active** - Broad platform coverage
✅ **Quality-first completion** - All items meet discharge criteria

### Next Week Focus
- **Continue momentum** across high-performing platform areas
- **Stakeholder alignment** on completed deliverable business impact
- **Resource optimization** based on this week's successful execution patterns

---

## 💡 Strategic Recommendations

### Leverage Success Patterns
**Replicate high-velocity approaches** demonstrated in this week's $(jq -r '.total // 0' /tmp/jira_data.json) completed deliverables across future initiative planning.

### Cross-Platform Synergy
**Maintain coordination** across $(jq -r '.issues[] | .fields.project.name' /tmp/jira_data.json | sort | uniq | wc -l | tr -d ' ') active project areas to sustain integrated platform advancement.

### Executive Communication
**Highlight business impact** of completed platform capabilities to demonstrate strategic investment ROI to senior leadership.

---

*📊 **Data Source**: Live Jira API Query - $(date +"%Y-%m-%d %H:%M:%S")*
*🔄 **Next Report**: $(date -v+7d +"%Y-%m-%d" 2>/dev/null || date +"%Y-%m-%d")*
*🎯 **Query**: Items completed in last 7 days across UI Foundation projects*

EOF
else
    # Generate template report (fallback)
    cat > "$REPORT_FILE" << EOF
# Weekly SLT Report - UI Foundation Platform

**Week of**: $(date +"%B %d, %Y")
**Director of Engineering**: Chris Cantu
**Report Generated**: $(date +"%Y-%m-%d %H:%M:%S")
**Data Source**: Template Data (Jira connection unavailable)

---

## 🎯 Executive Summary

**Platform Health**: UI Foundation platform initiatives progressing across Web Platform, Design System, i18n, UI Service Shell, and Header/Nav capabilities.

**Note**: This report uses template data. To enable live Jira integration:
1. Set environment variables: JIRA_API_TOKEN, JIRA_EMAIL, JIRA_BASE_URL
2. Ensure API token has proper permissions
3. Re-run report generation

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

## 💡 Strategic Recommendations

### Enable Live Reporting
**Next Step**: Configure Jira API credentials to unlock automated weekly reporting with live project data.

### Cross-Team Coordination
**Maintain strategic alignment** across Web Platform, Design System, and i18n teams through regular executive touchpoints and clear success metrics.

---

*📊 **Data Source**: Template Data - Configure Jira API for live reporting*
*🔄 **Next Report**: $(date -v+7d +"%Y-%m-%d" 2>/dev/null || date +"%Y-%m-%d")*

EOF
fi

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
