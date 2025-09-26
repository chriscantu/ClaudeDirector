# Daily Plan Help Command

Execute the PersonalDailyPlanningAgent to show available daily planning commands.

## Instructions for Claude:

1. Import and initialize the PersonalDailyPlanningAgent
2. Execute the `/daily-plan help` command using the agent
3. Display all available daily planning commands
4. Provide usage examples and descriptions
5. Show integration with strategic planning workflow

## Implementation:

Use the PersonalDailyPlanningAgent located at `.claudedirector/lib/agents/personal_daily_planning_agent.py` with the fixed absolute imports.

Execute: `agent.process_request({'command': '/daily-plan help', 'user_id': 'chris.cantu', 'user_input': ''})`

## Expected Behavior:

- List all available `/daily-plan` commands
- Show usage examples for each command
- Explain the strategic planning workflow
- Provide quick start guidance
