"""
Cursor Integration for First-Run Wizard
Seamlessly integrates role-based customization with Cursor IDE workflow.
"""

import logging
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

from .first_run_wizard import (
    FirstRunWizard, UserConfiguration, UserRole, OrganizationType, ChallengeFocus,
    get_user_personas_from_config, get_user_frameworks_from_config
)

logger = logging.getLogger(__name__)


class CursorWizardIntegration:
    """
    Cursor-specific integration for first-run wizard
    
    Enhances Cursor experience while maintaining full backward compatibility.
    """
    
    def __init__(self):
        self.wizard = FirstRunWizard()
        self.session_state = {
            'awaiting_wizard_response': False,
            'original_query': None,
            'wizard_shown': False
        }
    
    def should_show_wizard(self, user_input: str) -> bool:
        """
        Determine if first-run wizard should be shown
        
        Criteria:
        - User hasn't completed setup
        - Input looks like a strategic question
        - Not already in wizard flow
        """
        
        if not self.wizard.needs_first_run_setup():
            return False
        
        if self.session_state['wizard_shown']:
            return False
        
        # Check if input looks like a strategic question
        strategic_indicators = [
            'how should', 'what should', 'help me', 'need to', 'want to',
            'team', 'strategy', 'architecture', 'leadership', 'manage',
            'organize', 'structure', 'scale', 'improve', 'optimize',
            'communicate', 'align', 'coordinate', 'deliver', 'build'
        ]
        
        input_lower = user_input.lower()
        has_strategic_indicators = any(indicator in input_lower for indicator in strategic_indicators)
        is_question = '?' in user_input or any(word in input_lower for word in ['how', 'what', 'why', 'when', 'where'])
        is_substantial = len(user_input.split()) >= 4
        
        return has_strategic_indicators and (is_question or is_substantial)
    
    def process_user_input(self, user_input: str) -> Tuple[bool, str, Optional[str]]:
        """
        Process user input with wizard integration
        
        Returns:
            (is_wizard_interaction, response_text, persona_context)
        """
        
        user_input = user_input.strip()
        
        # Check if user is responding to wizard
        if self.session_state['awaiting_wizard_response']:
            return self._handle_wizard_response(user_input)
        
        # Check if wizard should be shown
        if self.should_show_wizard(user_input):
            return self._show_wizard(user_input)
        
        # Normal flow - return current configuration context
        config = self.wizard.get_current_config()
        if config:
            persona_context = self._generate_persona_context(config)
            return False, "", persona_context
        
        return False, "", None
    
    def _show_wizard(self, original_query: str) -> Tuple[bool, str, Optional[str]]:
        """Show the first-run wizard"""
        
        self.session_state['awaiting_wizard_response'] = True
        self.session_state['original_query'] = original_query
        self.session_state['wizard_shown'] = True
        
        wizard_prompt = self.wizard.get_wizard_prompt(original_query)
        
        return True, wizard_prompt, None
    
    def _handle_wizard_response(self, response: str) -> Tuple[bool, str, Optional[str]]:
        """Handle user's response to wizard"""
        
        original_query = self.session_state['original_query']
        
        success, message, config = self.wizard.process_wizard_response(response, original_query)
        
        if success:
            # Reset session state
            self.session_state['awaiting_wizard_response'] = False
            self.session_state['original_query'] = None
            
            # Generate persona context for the original query
            persona_context = self._generate_persona_context(config) if config else None
            
            # Combine wizard success message with instruction to continue
            full_response = f"""{message}

🔄 **Ready to proceed with your question!**

Please resubmit your original question and I'll provide customized strategic guidance."""
            
            return True, full_response, persona_context
        else:
            # Wizard failed, show error and keep wizard active
            return True, message, None
    
    def _generate_persona_context(self, config: UserConfiguration) -> str:
        """Generate persona context string for Cursor integration"""
        
        if not config:
            return ""
        
        # Get role-specific context
        role_descriptions = {
            UserRole.VP_SVP_ENGINEERING: "VP/SVP Engineering with executive strategy focus",
            UserRole.CTO: "CTO with technology vision and strategic leadership focus",
            UserRole.ENGINEERING_DIRECTOR: "Engineering Director with platform strategy and team coordination focus",
            UserRole.ENGINEERING_MANAGER: "Engineering Manager with team leadership and delivery focus",
            UserRole.STAFF_PRINCIPAL_ENGINEER: "Staff/Principal Engineer with technical strategy and influence focus",
            UserRole.PRODUCT_ENGINEERING_LEAD: "Product Engineering Lead with product-engineering alignment focus"
        }
        
        org_contexts = {
            OrganizationType.STARTUP: "startup environment (5-50 people) focused on resource optimization and scaling",
            OrganizationType.SCALE_UP: "scale-up environment (50-500 people) focused on platform building and processes",
            OrganizationType.ENTERPRISE: "enterprise environment (500+ people) focused on governance and coordination",
            OrganizationType.CONSULTING_AGENCY: "consulting/agency environment focused on client delivery and efficiency"
        }
        
        challenge_contexts = {
            ChallengeFocus.TEAM_LEADERSHIP: "team leadership and people management challenges",
            ChallengeFocus.TECHNICAL_STRATEGY: "technical strategy and architecture decisions",
            ChallengeFocus.EXECUTIVE_COMMUNICATION: "executive communication and stakeholder management",
            ChallengeFocus.CROSS_TEAM_COORDINATION: "cross-team coordination and dependencies",
            ChallengeFocus.PRODUCT_DELIVERY: "product delivery and user impact optimization"
        }
        
        context = f"""
USER CONFIGURATION CONTEXT:
Role: {role_descriptions.get(config.role, config.role.value)}
Organization: {org_contexts.get(config.organization_type, config.organization_type.value)}
Primary Challenge: {challenge_contexts.get(config.challenge_focus, config.challenge_focus.value)}

ACTIVE PERSONAS: {', '.join(config.primary_personas)}
RECOMMENDED FRAMEWORKS: {', '.join(config.recommended_frameworks[:5])}

Apply this configuration to provide highly relevant strategic guidance customized for this user's specific role and context.
"""
        return context
    
    def get_cursor_rules_enhancement(self) -> str:
        """
        Generate enhancement text for .cursorrules integration
        
        This can be dynamically injected into Cursor context
        """
        
        config = self.wizard.get_current_config()
        
        if not config:
            base_rules = """
# First-Run Wizard Integration
When a user asks their first strategic question, ClaudeDirector will show a role-based customization wizard.
This ensures strategic guidance is tailored to their specific role, organization, and challenges.

Default configuration active: Engineering Director with platform strategy focus.
"""
            return base_rules
        
        # Generate customized rules based on user configuration
        persona_context = self._generate_persona_context(config)
        
        enhanced_rules = f"""
# User-Customized ClaudeDirector Configuration
The following user configuration should be applied to all strategic interactions:

{persona_context}

This customization ensures all strategic guidance is specifically relevant to the user's role and context.
Users can reconfigure anytime using the /configure command.
"""
        return enhanced_rules
    
    def handle_configure_command(self) -> str:
        """Handle /configure command to restart wizard"""
        
        # Reset configuration to trigger wizard again
        if self.wizard.reset_configuration():
            # Reset session state to allow wizard to show again
            self.session_state = {
                'awaiting_wizard_response': False,
                'original_query': None,
                'wizard_shown': False
            }
            
            return """⚙️ **Configuration Reset**

Your ClaudeDirector setup has been reset. The next time you ask a strategic question, you'll see the customization wizard to update your preferences.

Ask any strategic question to begin reconfiguration!"""
        else:
            return "❌ Failed to reset configuration. Please try again."
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current status information for debugging/monitoring"""
        
        config = self.wizard.get_current_config()
        
        return {
            'wizard_completed': not self.wizard.needs_first_run_setup(),
            'awaiting_response': self.session_state['awaiting_wizard_response'],
            'current_role': config.role.value if config else None,
            'current_personas': config.primary_personas if config else None,
            'current_frameworks': config.recommended_frameworks[:3] if config else None,
            'config_date': config.customization_date if config else None
        }


# Cursor-specific helper functions
def initialize_cursor_integration() -> CursorWizardIntegration:
    """Initialize Cursor wizard integration"""
    return CursorWizardIntegration()


def process_cursor_input(integration: CursorWizardIntegration, user_input: str) -> Dict[str, Any]:
    """
    Process Cursor user input and return structured response
    
    Returns dictionary for easy integration with Cursor workflow
    """
    
    is_wizard, response_text, persona_context = integration.process_user_input(user_input)
    
    return {
        'is_wizard_interaction': is_wizard,
        'response_text': response_text,
        'persona_context': persona_context,
        'should_show_response': bool(response_text),
        'status': integration.get_status_info()
    }


def get_cursor_context_injection(integration: CursorWizardIntegration) -> str:
    """Get context text to inject into Cursor for current user configuration"""
    return integration.get_cursor_rules_enhancement()


if __name__ == "__main__":
    # Demo Cursor integration
    print("🧪 Cursor Wizard Integration Demo")
    print("=" * 50)
    
    integration = initialize_cursor_integration()
    
    # Test queries
    test_queries = [
        "How should I structure my engineering teams?",  # Should trigger wizard
        "B, 2, iii",  # Wizard response
        "What's the weather?",  # Non-strategic, should not trigger
        "/configure",  # Reconfigure command
    ]
    
    for query in test_queries:
        print(f"\nUser Input: '{query}'")
        result = process_cursor_input(integration, query)
        
        print(f"Is Wizard: {result['is_wizard_interaction']}")
        if result['should_show_response']:
            print(f"Response:\n{result['response_text']}")
        if result['persona_context']:
            print(f"Persona Context: {result['persona_context'][:100]}...")
        print(f"Status: {result['status']}")
        print("-" * 30)