# Retrospective Create Command

Execute the PersonalRetrospectiveAgent to start an interactive weekly retrospective session.

## Instructions for Claude:

1. Import and initialize the PersonalRetrospectiveAgent
2. Execute the `/retrospective create` command using the agent
3. Start the interactive 4-question retrospective session
4. Guide user through the complete retrospective flow
5. Save the completed retrospective to the database

## Implementation:

Use the PersonalRetrospectiveAgent located at `.claudedirector/lib/agents/personal_retrospective_agent.py`.

Execute: `agent.process_request({'command': '/retrospective create', 'user_id': '***REMOVED***', 'user_input': ''})`

## Expected Behavior:

- Start interactive retrospective session for current date
- Present 4 questions in sequence:
  1. What went well this week?
  2. What could have gone better?
  3. What will I focus on next week?
  4. How would I rate this week on a scale of 1-10?
- Save completed retrospective with rating
- Provide confirmation and next steps

## Session Management:

- Handle user responses during active session
- Validate rating input (1-10, default to 5 if invalid)
- Complete session and clean up when finished
- Show success message with completion confirmation
