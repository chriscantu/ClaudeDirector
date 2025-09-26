# Daily Plan Review Command

Execute the system daily planning CLI to review recent daily plans and strategic insights.

## Instructions for Claude:

Execute the existing system CLI tool: `.claudedirector/tools/bin/daily-plan review`

## Expected Behavior:

- Direct CLI execution without code generation
- Show recent daily plans (last 7 days)
- Display priorities and strategic balance for each day
- Show "No daily plans found" if none exist
- Provide strategic insights about planning patterns
- Suggest creating first plan if needed

## Architecture Compliance:

- ✅ PROJECT_STRUCTURE.md: Uses existing system tool in .claudedirector/tools/bin/
- ✅ BLOAT_PREVENTION_SYSTEM.md: No code duplication, calls existing implementation
- ✅ Native execution: Direct CLI call, no Python code generation required
