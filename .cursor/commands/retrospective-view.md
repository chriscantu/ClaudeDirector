# Retrospective View Command

Execute the PersonalRetrospectiveAgent to view recent retrospective entries.

## Instructions for Claude:

1. Import and initialize the PersonalRetrospectiveAgent
2. Execute the `/retrospective view` command using the agent
3. Display recent retrospective entries with ratings
4. Show formatted retrospective history
5. Provide insights and patterns from past retrospectives

## Implementation:

Use the PersonalRetrospectiveAgent located at `.claudedirector/lib/agents/personal_retrospective_agent.py`.

Execute: `agent.process_request({'command': '/retrospective view', 'user_id': '***REMOVED***', 'user_input': ''})`

## Expected Behavior:

- Retrieve recent retrospective entries (default: 5 most recent)
- Display each entry with:
  - Date
  - What went well
  - What could have gone better
  - Next week's focus
  - Rating (1-10 scale)
- Show formatted, readable output
- Provide quick access to retrospective history

## Data Display:

Format each retrospective entry clearly with:
- **Date**: YYYY-MM-DD format
- **Rating**: X/10 scale
- **Wins**: What went well
- **Improvements**: What could have gone better
- **Focus**: Next week's priorities
