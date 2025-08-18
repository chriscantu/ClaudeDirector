"""
First-Run Wizard for ClaudeDirector
Provides role-based customization for users with seamless Cursor integration.
"""

import json
import logging
import os
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User role types for customization"""
    VP_SVP_ENGINEERING = "vp_svp_engineering"
    CTO = "cto"
    ENGINEERING_DIRECTOR = "engineering_director"
    ENGINEERING_MANAGER = "engineering_manager"
    STAFF_PRINCIPAL_ENGINEER = "staff_principal_engineer"
    PRODUCT_ENGINEERING_LEAD = "product_engineering_lead"


class OrganizationType(Enum):
    """Organization size and type"""
    STARTUP = "startup"  # 5-50 people
    SCALE_UP = "scale_up"  # 50-500 people
    ENTERPRISE = "enterprise"  # 500+ people
    CONSULTING_AGENCY = "consulting_agency"  # Client-focused


class ChallengeFocus(Enum):
    """Primary challenge areas"""
    TEAM_LEADERSHIP = "team_leadership"
    TECHNICAL_STRATEGY = "technical_strategy"
    EXECUTIVE_COMMUNICATION = "executive_communication"
    CROSS_TEAM_COORDINATION = "cross_team_coordination"
    PRODUCT_DELIVERY = "product_delivery"


@dataclass
class UserConfiguration:
    """User's personalized ClaudeDirector configuration"""
    role: UserRole
    organization_type: OrganizationType
    challenge_focus: ChallengeFocus
    primary_personas: List[str]
    recommended_frameworks: List[str]
    customization_date: str
    has_completed_wizard: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'role': self.role.value,
            'organization_type': self.organization_type.value,
            'challenge_focus': self.challenge_focus.value,
            'primary_personas': self.primary_personas,
            'recommended_frameworks': self.recommended_frameworks,
            'customization_date': self.customization_date,
            'has_completed_wizard': self.has_completed_wizard
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserConfiguration':
        """Create from dictionary"""
        return cls(
            role=UserRole(data['role']),
            organization_type=OrganizationType(data['organization_type']),
            challenge_focus=ChallengeFocus(data['challenge_focus']),
            primary_personas=data['primary_personas'],
            recommended_frameworks=data['recommended_frameworks'],
            customization_date=data['customization_date'],
            has_completed_wizard=data.get('has_completed_wizard', True)
        )


class RolePersonaMapper:
    """Maps user roles to appropriate personas and frameworks"""
    
    ROLE_PERSONA_MAPPING = {
        UserRole.VP_SVP_ENGINEERING: {
            'primary_personas': ['camille', 'diego', 'alvaro'],
            'description': 'Executive strategy, board communication, organizational scaling',
            'frameworks': [
                'Good Strategy Bad Strategy',
                'Strategic Analysis Framework', 
                'Executive Communication',
                'Organizational Transformation',
                'Capital Allocation Framework'
            ]
        },
        UserRole.CTO: {
            'primary_personas': ['camille', 'martin', 'alvaro'],
            'description': 'Technology vision, strategic leadership, competitive positioning',
            'frameworks': [
                'Technical Strategy Framework',
                'Good Strategy Bad Strategy',
                'Competitive Analysis',
                'Platform Strategy Framework',
                'Evolutionary Architecture'
            ]
        },
        UserRole.ENGINEERING_DIRECTOR: {
            'primary_personas': ['diego', 'martin', 'marcus'],
            'description': 'Platform strategy, team coordination, cross-functional alignment',
            'frameworks': [
                'Team Topologies',
                'Strategic Platform Assessment',
                'Capital Allocation Framework',
                'Scaling Up Excellence',
                'Platform Strategy Framework'
            ]
        },
        UserRole.ENGINEERING_MANAGER: {
            'primary_personas': ['diego', 'marcus', 'rachel'],
            'description': 'Team leadership, delivery optimization, people management',
            'frameworks': [
                'Team Topologies',
                'Crucial Conversations',
                'Scaling Up Excellence',
                'Performance Management',
                'Change Management'
            ]
        },
        UserRole.STAFF_PRINCIPAL_ENGINEER: {
            'primary_personas': ['martin', 'diego', 'marcus'],
            'description': 'Technical strategy, influence without authority, system design',
            'frameworks': [
                'Technical Strategy Framework',
                'Evolutionary Architecture',
                'Influence Patterns',
                'Systems Thinking',
                'Architecture Decision Records'
            ]
        },
        UserRole.PRODUCT_ENGINEERING_LEAD: {
            'primary_personas': ['alvaro', 'rachel', 'diego'],
            'description': 'Product-engineering alignment, user impact, delivery optimization',
            'frameworks': [
                'User-Centered Design',
                'Lean Startup',
                'Product Strategy',
                'Team Topologies',
                'Accelerate'
            ]
        }
    }
    
    ORGANIZATION_CONTEXT = {
        OrganizationType.STARTUP: {
            'context': 'Resource optimization, scaling challenges, technical debt management',
            'framework_emphasis': ['Lean Startup', 'Capital Allocation Framework', 'Technical Strategy Framework']
        },
        OrganizationType.SCALE_UP: {
            'context': 'Platform building, team structure, process optimization',
            'framework_emphasis': ['Team Topologies', 'Scaling Up Excellence', 'Platform Strategy Framework']
        },
        OrganizationType.ENTERPRISE: {
            'context': 'Governance, compliance, cross-team coordination',
            'framework_emphasis': ['Organizational Transformation', 'Strategic Analysis Framework', 'Compliance Frameworks']
        },
        OrganizationType.CONSULTING_AGENCY: {
            'context': 'Client delivery, team efficiency, project management',
            'framework_emphasis': ['Crucial Conversations', 'Team Topologies', 'Delivery Optimization']
        }
    }
    
    CHALLENGE_FRAMEWORKS = {
        ChallengeFocus.TEAM_LEADERSHIP: [
            'Team Topologies', 'Crucial Conversations', 'Scaling Up Excellence'
        ],
        ChallengeFocus.TECHNICAL_STRATEGY: [
            'Technical Strategy Framework', 'Evolutionary Architecture', 'Systems Thinking'
        ],
        ChallengeFocus.EXECUTIVE_COMMUNICATION: [
            'Good Strategy Bad Strategy', 'Strategic Analysis Framework', 'Executive Communication'
        ],
        ChallengeFocus.CROSS_TEAM_COORDINATION: [
            'Team Topologies', 'Strategic Platform Assessment', 'Change Management'
        ],
        ChallengeFocus.PRODUCT_DELIVERY: [
            'Accelerate', 'Lean Startup', 'User-Centered Design'
        ]
    }
    
    @classmethod
    def get_configuration_for_role(cls, role: UserRole, org_type: OrganizationType, 
                                  challenge: ChallengeFocus) -> UserConfiguration:
        """Generate complete configuration based on role selection"""
        
        # Get base role configuration
        role_config = cls.ROLE_PERSONA_MAPPING[role]
        
        # Combine frameworks from role, organization, and challenge
        frameworks = set(role_config['frameworks'])
        frameworks.update(cls.ORGANIZATION_CONTEXT[org_type]['framework_emphasis'])
        frameworks.update(cls.CHALLENGE_FRAMEWORKS[challenge])
        
        return UserConfiguration(
            role=role,
            organization_type=org_type,
            challenge_focus=challenge,
            primary_personas=role_config['primary_personas'],
            recommended_frameworks=list(frameworks),
            customization_date=datetime.now().isoformat()
        )


class FirstRunWizard:
    """
    First-run wizard for role-based ClaudeDirector customization
    
    Designed for seamless Cursor integration with graceful degradation.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / '.claudedirector'
        self.config_file = self.config_dir / 'user_config.json'
        self.config_dir.mkdir(exist_ok=True)
        
        self.current_config: Optional[UserConfiguration] = None
        self._load_existing_config()
    
    def _load_existing_config(self) -> None:
        """Load existing user configuration if available"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.current_config = UserConfiguration.from_dict(data)
                    logger.info(f"Loaded existing configuration for role: {self.current_config.role.value}")
        except Exception as e:
            logger.warning(f"Could not load existing config: {e}")
            self.current_config = None
    
    def save_configuration(self, config: UserConfiguration) -> bool:
        """Save user configuration to persistent storage"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
            
            self.current_config = config
            logger.info(f"Saved configuration for role: {config.role.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def needs_first_run_setup(self) -> bool:
        """Check if user needs to complete first-run setup"""
        return self.current_config is None or not self.current_config.has_completed_wizard
    
    def get_wizard_prompt(self, original_query: str) -> str:
        """Generate first-run wizard prompt for user"""
        
        wizard_prompt = f"""🚀 **Welcome to ClaudeDirector!**

I see this is your first time asking a strategic question. Let me customize the experience for your specific role and challenges.

**Your question**: "{original_query}"

I'll answer this with personalized guidance after a quick 60-second setup:

## **Step 1: What's your role?** 🎯

**A.** VP/SVP Engineering - Executive strategy & board communication
**B.** CTO - Technology vision & strategic leadership  
**C.** Engineering Director - Platform & team coordination (current default)
**D.** Engineering Manager - Team leadership & delivery
**E.** Staff/Principal Engineer - Technical strategy & influence
**F.** Product Engineering Lead - Product-eng alignment & delivery

## **Step 2: What's your organization like?** 🏢

**1.** Startup (5-50 people) - Resource optimization & scaling
**2.** Scale-up (50-500) - Platform building & process
**3.** Enterprise (500+) - Governance & coordination
**4.** Consulting/Agency - Client delivery & team efficiency

## **Step 3: What's your biggest challenge?** 🎯

**i.** Team Leadership & People Management
**ii.** Technical Strategy & Architecture Decisions  
**iii.** Executive Communication & Stakeholder Management
**iv.** Cross-Team Coordination & Dependencies
**v.** Product Delivery & User Impact

**Please respond with your choices (e.g., "B, 2, iii" for CTO at Scale-up focused on Executive Communication)**

⏭️ **Skip Setup**: Type "skip" to use current defaults and get immediate guidance

---
*This setup takes 60 seconds and dramatically improves the relevance of all future strategic guidance.*"""

        return wizard_prompt
    
    def process_wizard_response(self, response: str, original_query: str) -> Tuple[bool, str, Optional[UserConfiguration]]:
        """
        Process user's wizard response and generate configuration
        
        Returns:
            (success, response_message, configuration)
        """
        
        response = response.strip().lower()
        
        # Handle skip
        if 'skip' in response:
            return self._handle_skip_setup(original_query)
        
        # Parse selection (e.g., "b, 2, iii" or "B,2,iii")
        try:
            parts = [part.strip() for part in response.replace(',', ' ').split()]
            
            if len(parts) != 3:
                return False, self._get_error_message(), None
            
            role_choice, org_choice, challenge_choice = parts
            
            # Parse role
            role_map = {
                'a': UserRole.VP_SVP_ENGINEERING,
                'b': UserRole.CTO,
                'c': UserRole.ENGINEERING_DIRECTOR,
                'd': UserRole.ENGINEERING_MANAGER,
                'e': UserRole.STAFF_PRINCIPAL_ENGINEER,
                'f': UserRole.PRODUCT_ENGINEERING_LEAD
            }
            
            # Parse organization
            org_map = {
                '1': OrganizationType.STARTUP,
                '2': OrganizationType.SCALE_UP,
                '3': OrganizationType.ENTERPRISE,
                '4': OrganizationType.CONSULTING_AGENCY
            }
            
            # Parse challenge
            challenge_map = {
                'i': ChallengeFocus.TEAM_LEADERSHIP,
                'ii': ChallengeFocus.TECHNICAL_STRATEGY,
                'iii': ChallengeFocus.EXECUTIVE_COMMUNICATION,
                'iv': ChallengeFocus.CROSS_TEAM_COORDINATION,
                'v': ChallengeFocus.PRODUCT_DELIVERY
            }
            
            if (role_choice not in role_map or 
                org_choice not in org_map or 
                challenge_choice not in challenge_map):
                return False, self._get_error_message(), None
            
            # Generate configuration
            config = RolePersonaMapper.get_configuration_for_role(
                role_map[role_choice],
                org_map[org_choice], 
                challenge_map[challenge_choice]
            )
            
            # Save configuration
            if self.save_configuration(config):
                success_message = self._generate_success_message(config, original_query)
                return True, success_message, config
            else:
                return False, "❌ Failed to save configuration. Using defaults for this session.", config
                
        except Exception as e:
            logger.error(f"Error processing wizard response: {e}")
            return False, self._get_error_message(), None
    
    def _handle_skip_setup(self, original_query: str) -> Tuple[bool, str, Optional[UserConfiguration]]:
        """Handle when user skips the setup"""
        
        # Create default configuration (Engineering Director)
        default_config = RolePersonaMapper.get_configuration_for_role(
            UserRole.ENGINEERING_DIRECTOR,
            OrganizationType.SCALE_UP,
            ChallengeFocus.TECHNICAL_STRATEGY
        )
        default_config.has_completed_wizard = False
        
        skip_message = f"""⏭️ **Setup Skipped** - Using defaults for now

I'll answer your question using Engineering Director defaults:
- **Personas**: Diego (Engineering Leadership), Martin (Architecture), Marcus (Change Management)
- **Focus**: Technical strategy and team coordination
- **Context**: Scale-up organization

💡 **Tip**: Run `/configure` anytime to customize for your specific role and get more relevant guidance.

---

**Now answering your question**: "{original_query}"
"""
        
        return True, skip_message, default_config
    
    def _generate_success_message(self, config: UserConfiguration, original_query: str) -> str:
        """Generate success message after configuration"""
        
        role_config = RolePersonaMapper.ROLE_PERSONA_MAPPING[config.role]
        org_context = RolePersonaMapper.ORGANIZATION_CONTEXT[config.organization_type]
        
        success_message = f"""✅ **Configuration Complete!**

🎯 **Activating your personalized ClaudeDirector experience:**

**Role**: {config.role.value.replace('_', ' ').title()}
- **Primary Personas**: {', '.join([p.title() for p in config.primary_personas])}
- **Focus**: {role_config['description']}

**Organization Context**: {config.organization_type.value.replace('_', ' ').title()}
- **Emphasis**: {org_context['context']}

**Challenge Focus**: {config.challenge_focus.value.replace('_', ' ').title()}
- **Top Frameworks**: {', '.join(config.recommended_frameworks[:3])}

💾 **This configuration is saved** and will enhance all future strategic guidance.

⚙️ **Reconfigure anytime** with `/configure` command

---

**Now answering your customized question**: "{original_query}"
"""
        
        return success_message
    
    def _get_error_message(self) -> str:
        """Get error message for invalid input"""
        return """❌ **Invalid selection**. Please respond with three choices like: **"B, 2, iii"**

**Examples**:
- "A, 1, i" = VP Engineering at Startup focused on Team Leadership  
- "D, 2, iv" = Engineering Manager at Scale-up focused on Cross-team Coordination
- "skip" = Use defaults for now

Please try again or type "skip" to proceed with defaults."""
    
    def get_current_config(self) -> Optional[UserConfiguration]:
        """Get current user configuration"""
        return self.current_config
    
    def reset_configuration(self) -> bool:
        """Reset configuration to trigger first-run wizard again"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            self.current_config = None
            logger.info("Configuration reset - will trigger first-run wizard")
            return True
        except Exception as e:
            logger.error(f"Failed to reset configuration: {e}")
            return False


# Convenience functions for integration
def create_first_run_wizard(config_dir: Optional[Path] = None) -> FirstRunWizard:
    """Create and initialize first-run wizard"""
    return FirstRunWizard(config_dir)


def get_user_personas_from_config(config: Optional[UserConfiguration]) -> List[str]:
    """Extract primary personas from user configuration"""
    if config and config.primary_personas:
        return config.primary_personas
    return ['diego']  # Default fallback


def get_user_frameworks_from_config(config: Optional[UserConfiguration]) -> List[str]:
    """Extract recommended frameworks from user configuration"""
    if config and config.recommended_frameworks:
        return config.recommended_frameworks
    return ['Team Topologies', 'Strategic Analysis Framework']  # Default fallback


if __name__ == "__main__":
    # Demo usage
    wizard = create_first_run_wizard()
    
    if wizard.needs_first_run_setup():
        print("🧪 First-Run Wizard Demo")
        print("=" * 50)
        
        original_query = "How should I structure my engineering teams for better scalability?"
        
        # Show wizard prompt
        wizard_prompt = wizard.get_wizard_prompt(original_query)
        print(wizard_prompt)
        print("\n" + "=" * 50)
        
        # Simulate user responses
        test_responses = [
            "B, 2, iii",  # CTO, Scale-up, Executive Communication
            "D, 1, i",    # Engineering Manager, Startup, Team Leadership  
            "skip"        # Skip setup
        ]
        
        for response in test_responses:
            print(f"\nUser Response: '{response}'")
            success, message, config = wizard.process_wizard_response(response, original_query)
            print(f"Success: {success}")
            print(f"Message:\n{message}")
            if config:
                print(f"Config: {config.role.value}, Personas: {config.primary_personas}")
            print("-" * 30)
    else:
        print("✅ User already configured!")
        config = wizard.get_current_config()
        if config:
            print(f"Role: {config.role.value}")
            print(f"Personas: {config.primary_personas}")
            print(f"Frameworks: {config.recommended_frameworks[:3]}")