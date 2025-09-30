# Generate Weekly Report Command

Execute the system weekly reporting tool to generate executive weekly reports with strategic insights.

## Instructions for Claude:

Execute the existing system weekly reporter: `python .claudedirector/lib/reporting/weekly_reporter.py`

## Expected Behavior:

- Direct CLI execution without code generation
- Fetch live Jira data for strategic initiatives and epics
- Generate executive-ready weekly report with strategic insights
- Apply MCP-enhanced analysis (Sequential Thinking + Context7 benchmarking)
- Save report to leadership-workspace/reports/ with timestamp
- Confirm successful report generation with file path

## Command Variations:

### Standard Report Generation
```bash
python .claudedirector/lib/reporting/weekly_reporter.py
```

### Dry Run (Preview without Jira fetch)
```bash
python .claudedirector/lib/reporting/weekly_reporter.py --dry-run
```

### Custom Output Path
```bash
python .claudedirector/lib/reporting/weekly_reporter.py --output /path/to/report.md
```

### Debug Mode
```bash
python .claudedirector/lib/reporting/weekly_reporter.py --debug
```

## Report Contents:

- **Executive Summary**: Strategic initiative status and portfolio overview
- **Strategic Initiative Updates**: L0/L2 initiatives with business impact analysis
- **Team Coverage**: Cross-functional team coordination insights
- **Strategic Focus Areas**: Platform engineering, design system, internationalization
- **MCP-Enhanced Insights**: Strategic reasoning trails and industry benchmarking

## Configuration:

Report generation uses configuration from:
- `.claudedirector/config/weekly_report_config.yaml`
- Jira connection settings
- JQL queries for strategic initiatives
- MCP integration settings

## Architecture Compliance:

- ✅ PROJECT_STRUCTURE.md: Uses existing system tool in .claudedirector/lib/reporting/
- ✅ BLOAT_PREVENTION_SYSTEM.md: No code duplication, calls existing implementation
- ✅ Native execution: Direct Python CLI call, no code generation required
- ✅ MCP Integration: Reuses existing MCPIntegrationManager, no duplicate MCP logic
