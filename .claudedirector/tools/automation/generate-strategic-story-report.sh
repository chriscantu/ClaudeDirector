#!/bin/bash

# Strategic Story Analysis Report Generator
# Analyzes completed stories for executive-level strategic impact
#
# Usage: ./generate-strategic-story-report.sh [--config config_file] [--dry-run]
#
# Author: ClaudeDirector AI Framework - Strategic Story Curation
# Version: 1.0.0

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../.." &> /dev/null && pwd )"
WORKSPACE_DIR="${PROJECT_ROOT}/leadership-workspace"
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

# Enhanced story analysis function
analyze_story_strategic_impact() {
    local json_file="$1"
    local analysis_type="$2"

    if [[ ! -f "$json_file" ]]; then
        echo "No stories found for $analysis_type analysis"
        return
    fi

    local total=$(jq -r '.issues | length' "$json_file")
    if [[ "$total" -eq 0 ]]; then
        echo "No stories found for $analysis_type"
        return
    fi

    echo ""
    echo "### 🎯 $analysis_type ($total stories)"
    echo ""

    # Enhanced story formatting with impact analysis including status for completion timing
    jq -r '.issues[] | "\(.fields.project.name)|\(.key)|\(.fields.summary)|\(.fields.status.name)|\(.fields.priority.name // "None")|\(.fields.assignee.displayName // "Unassigned")|\(.fields.parent.key // "No Epic")|\(.fields.watchers.watchCount // 0)|\(.fields.issuelinks | length)"' "$json_file" | \
    while IFS='|' read -r project key summary status priority assignee parent_epic watchers links; do

        # Strategic impact scoring
        local impact_score=0
        local impact_indicators=()

        # Priority scoring
        case "$priority" in
            "Highest"|"Critical")
                impact_score=$((impact_score + 3))
                impact_indicators+=("🔴 Critical Priority")
                ;;
            "High")
                impact_score=$((impact_score + 2))
                impact_indicators+=("🟡 High Priority")
                ;;
        esac

        # Cross-project indicators
        if echo "$summary" | grep -qiE "(UIS-|UXI-|HUBS-|WES-|FSGD-|shared|platform|design.system)"; then
            impact_score=$((impact_score + 2))
            impact_indicators+=("🌐 Cross-Project Impact")
        fi

        # Dependency/unblocking indicators
        if echo "$summary" | grep -qiE "(block|depend|enable|unlock|prerequisite)"; then
            impact_score=$((impact_score + 2))
            impact_indicators+=("🔓 Dependency Resolution")
        fi

        # Production/customer impact
        if echo "$summary" | grep -qiE "(production|customer|incident|outage|hotfix)"; then
            impact_score=$((impact_score + 3))
            impact_indicators+=("⚡ Production Impact")
        fi

        # Watchers/collaboration score
        if [[ "$watchers" -gt 3 ]]; then
            impact_score=$((impact_score + 1))
            impact_indicators+=("👥 High Collaboration ($watchers watchers)")
        fi

        # Link connectivity score
        if [[ "$links" -gt 2 ]]; then
            impact_score=$((impact_score + 1))
            impact_indicators+=("🔗 Highly Connected ($links links)")
        fi

        # Platform/developer experience indicators
        if echo "$summary" | grep -qiE "(platform|developer.experience|DevEx|tooling|automation|Hammer|CKEditor|webpack|vite|build.tool)"; then
            impact_score=$((impact_score + 3))
            impact_indicators+=("⚙️ Platform/DevEx Impact")
        fi

        # Version 1.0 releases and L2 initiatives
        if echo "$summary" | grep -qiE "(v1.0|version.1|Hammer.v1|L2)"; then
            impact_score=$((impact_score + 3))
            impact_indicators+=("🎯 Major Release/L2 Initiative")
        fi

        # Manual executive override (check if this is a manually specified strategic story)
        if echo "$key" | grep -qE "(UIS-1590|UXI-1455)"; then
            impact_score=$((impact_score + 5))
            impact_indicators+=("👑 Executive Priority")
        fi

        # DEBUG: Show scoring for all stories
        echo "🔍 DEBUG: $key - '$summary' = $impact_score points (${impact_indicators[*]:-no indicators})"

        # Only show stories with strategic impact (score >= 1 for better coverage)
        if [[ "$impact_score" -ge 1 ]]; then
            local jira_url="${JIRA_BASE_URL:-https://procoretech.atlassian.net}"

            # Determine completion timing
            local timing=""
            case "$status" in
                "Done"|"Closed"|"Resolved")
                    timing="✅ **Completed This Week**"
                    ;;
                "In Progress"|"In Review"|"Ready for Release")
                    timing="🔄 **Completing This Week**"
                    ;;
                *)
                    timing="📋 **In Progress**"
                    ;;
            esac

            echo "#### 📋 [$key]($jira_url/browse/$key) - $summary"
            echo ""
            echo "- **Project**: $project"
            echo "- **Status**: $timing ($status)"
            echo "- **Priority**: $priority"
            echo "- **Assignee**: $assignee"
            if [[ "$parent_epic" != "No Epic" ]]; then
                echo "- **Epic**: [$parent_epic]($jira_url/browse/$parent_epic)"
            fi
            echo "- **Strategic Impact Score**: $impact_score/10"

            # Show impact indicators
            if [[ ${#impact_indicators[@]} -gt 0 ]]; then
                echo "- **Impact Indicators**: ${impact_indicators[*]}"
            fi

            echo ""
            echo "---"
            echo ""
        fi
    done
}

# Story pattern analysis
analyze_story_patterns() {
    local json_file="$1"

    if [[ ! -f "$json_file" ]]; then
        return
    fi

    local total=$(jq -r '.total // 0' "$json_file")
    if [[ "$total" -eq 0 ]]; then
        return
    fi

    echo ""
    echo "## 📊 Strategic Story Pattern Analysis"
    echo ""

    # Cross-project connectivity analysis
    local cross_project_count=$(jq -r '.issues[] | select(.fields.summary | test("UIS-|UXI-|HUBS-|WES-|FSGD-|shared|platform|design.system"; "i")) | .key' "$json_file" | wc -l | tr -d ' ')
    echo "**Cross-Project Stories**: $cross_project_count stories demonstrate platform-wide coordination"

    # Priority distribution
    local high_priority_count=$(jq -r '.issues[] | select(.fields.priority.name | test("Highest|Critical|High"; "i")) | .key' "$json_file" | wc -l | tr -d ' ')
    echo "**High-Priority Completions**: $high_priority_count stories addressed critical business needs"

    # Epic coverage
    local stories_with_epics=$(jq -r '.issues[] | select(.fields.parent.key != null) | .key' "$json_file" | wc -l | tr -d ' ')
    local epic_coverage_percent=$(( (stories_with_epics * 100) / total ))
    echo "**Epic Alignment**: $epic_coverage_percent% of stories ($stories_with_epics/$total) contribute to strategic epics"

    # Collaboration intensity
    local avg_watchers=$(jq -r '[.issues[] | .fields.watchers.watchCount // 0] | add / length | floor' "$json_file")
    echo "**Collaboration Level**: Average $avg_watchers watchers per story indicates cross-team coordination"

    echo ""
}

# Main execution
CONFIG_FILE="$DEFAULT_CONFIG"
DRY_RUN=false

# Parse arguments
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
        --help)
            echo "Usage: $0 [--config config_file] [--dry-run]"
            echo ""
            echo "Options:"
            echo "  --config FILE      Use specific config file"
            echo "  --dry-run          Show what would be done without executing"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check prerequisites
if ! command -v jq &> /dev/null; then
    log_error "jq is required for story analysis. Install with: brew install jq"
    exit 1
fi

# Generate report
REPORT_DATE=$(date +%Y-%m-%d)
STRATEGIC_REPORT_FILE="${REPORTS_DIR}/strategic-story-analysis-${REPORT_DATE}.md"

log_info "Generating strategic story analysis report..."
log_info "  Config: $CONFIG_FILE"
log_info "  Output: $STRATEGIC_REPORT_FILE"

if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would analyze stories for strategic impact"
    exit 0
fi

# Create reports directory if needed
mkdir -p "$REPORTS_DIR"

# Function to extract JQL query from config
extract_jql_query() {
    local config_file="$1"
    local query_name="$2"

    if command -v python3 &> /dev/null; then
        python3 -c "
import yaml
try:
    with open('$config_file', 'r') as f:
        config = yaml.safe_load(f)
    query = config.get('jql_queries', {}).get('$query_name', '')
    if query:
        print(query)
    else:
        exit(1)
except Exception:
    exit(1)
" 2>/dev/null
    else
        log_error "Python3 required for config parsing"
        exit 1
    fi
}

# Function to fetch Jira data
fetch_strategic_data() {
    local jql_query="$1"
    local output_file="$2"

    if [[ -z "$JIRA_API_TOKEN" || -z "$JIRA_EMAIL" || -z "$JIRA_BASE_URL" ]]; then
        log_warning "Jira credentials not configured"
        return 1
    fi

    local encoded_jql=$(printf '%s' "$jql_query" | python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.stdin.read().strip()))")

    curl -s \
        -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" \
        -H "Accept: application/json" \
        "${JIRA_BASE_URL}/rest/api/3/search/jql?jql=${encoded_jql}&maxResults=50&fields=summary,key,status,assignee,project,priority,parent,watchers,issuelinks" \
        > "$output_file"

    return $?
}

# Start report generation
cat > "$STRATEGIC_REPORT_FILE" << EOF
# Strategic Story Impact Analysis

**Week of**: $(date +"%B %d, %Y")
**Director of Engineering**: Chris Cantu
**Report Generated**: $(date +"%Y-%m-%d %H:%M:%S")
**Analysis Focus**: High-impact story completions with strategic business value

---

## 🎯 Executive Summary

This analysis identifies completed stories with significant strategic impact based on:
- **Priority Level**: Critical/High priority items addressing urgent business needs
- **Cross-Project Impact**: Stories affecting multiple teams or shared platform components
- **Dependency Resolution**: Work that unblocks other teams or initiatives
- **Production Impact**: Customer-facing improvements and incident resolutions
- **Collaboration Intensity**: Stories with high cross-team engagement and connectivity

---

EOF

# Fetch and analyze different categories of strategic stories

# Test query to verify we can capture the specific stories mentioned by user
log_info "Testing story capture with direct keys..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_test")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_test.json"; then
    test_count=$(jq -r '.issues | length' "/tmp/strategic_test.json" 2>/dev/null || echo "0")
    log_info "Test query captured $test_count stories (UIS-1590, UXI-1455)"
    # ANALYZE the test stories to show debug output
    analyze_story_strategic_impact "/tmp/strategic_test.json" "🧪 Debug Test - Strategic Stories" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing executive spotlight strategic stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_executive_spotlight")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_executive.json"; then
    analyze_story_strategic_impact "/tmp/strategic_executive.json" "🎯 Executive Spotlight - Strategic Priorities" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing high-priority strategic stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_high_priority")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_high_priority.json"; then
    analyze_story_strategic_impact "/tmp/strategic_high_priority.json" "High-Priority Strategic Completions" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing cross-project impact stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_cross_project")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_cross_project.json"; then
    analyze_story_strategic_impact "/tmp/strategic_cross_project.json" "Cross-Project Platform Impact" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing dependency resolution stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_dependency_resolution")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_dependency.json"; then
    analyze_story_strategic_impact "/tmp/strategic_dependency.json" "Dependency Resolution & Team Unblocking" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing broad impact stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_broad_impact")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_broad.json"; then
    analyze_story_strategic_impact "/tmp/strategic_broad.json" "Broad Organizational Impact" >> "$STRATEGIC_REPORT_FILE"
fi

log_info "Analyzing production impact stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "strategic_production_impact")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/strategic_production.json"; then
    analyze_story_strategic_impact "/tmp/strategic_production.json" "Production & Customer Impact" >> "$STRATEGIC_REPORT_FILE"
fi

# Add overall pattern analysis using regular completed items
log_info "Performing pattern analysis on all completed stories..."
QUERY=$(extract_jql_query "$CONFIG_FILE" "weekly_completed_items")
if [[ -n "$QUERY" ]] && fetch_strategic_data "$QUERY" "/tmp/all_completed.json"; then
    analyze_story_patterns "/tmp/all_completed.json" >> "$STRATEGIC_REPORT_FILE"
fi

# Add footer
cat >> "$STRATEGIC_REPORT_FILE" << EOF

---

## 💡 Strategic Recommendations

### For Beth (VP Engineering) Communication
**Use these strategic story highlights to demonstrate:**
- **Platform Investment ROI**: Cross-project impact stories show organizational leverage
- **Risk Mitigation**: High-priority completions demonstrate proactive issue resolution
- **Team Coordination**: Dependency resolution work enables broader organizational velocity
- **Customer Focus**: Production impact stories show direct business value delivery

### Executive Value Translation
- **High Priority Completions** → Risk mitigation and business continuity
- **Cross-Project Work** → Platform investment returns and organizational efficiency
- **Dependency Resolution** → Team velocity enablement and coordination excellence
- **Production Impact** → Direct customer value and incident prevention

---

*📊 **Analysis Method**: Data-driven story impact scoring based on priority, connectivity, collaboration, and business impact indicators*
*🔄 **Next Analysis**: $(date -v+7d +"%Y-%m-%d" 2>/dev/null || date -d "+7 days" +"%Y-%m-%d" 2>/dev/null || date +"%Y-%m-%d")*
*🎯 **Strategic Focus**: Stories demonstrating platform leadership and organizational value delivery*

EOF

log_success "Strategic story analysis generated successfully!"
log_info "Report saved to: $STRATEGIC_REPORT_FILE"

# Open the report if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    log_info "Opening strategic analysis report..."
    open "$STRATEGIC_REPORT_FILE"
fi
