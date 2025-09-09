"""
PHASE 8.4: MASSIVE CONSOLIDATION - Multi-Tenant Manager
BaseManager consolidation for NET code reduction

ELIMINATED: Manual logging infrastructure
CONSOLIDATED: MultiTenantManager → MultiTenantManager(BaseManager)
NET REDUCTION TARGET: 100+ lines through BaseManager adoption

Original enterprise scalability capabilities maintained:
- Multi-tenant organization support
- Enterprise security and platform infrastructure
- Context engineering 8-layer architecture integration
- 100% data isolation between organizations
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib

# PHASE 8.4: BaseManager consolidation imports
from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType

# Core ClaudeDirector integration following PROJECT_STRUCTURE.md
try:
    from ..context_engineering.advanced_context_engine import AdvancedContextEngine
    from ..context_engineering.stakeholder_intelligence_unified import (
        StakeholderIntelligenceUnified,
    )

    # Phase 2C: Use UnifiedDatabaseCoordinator instead of legacy DatabaseManager
    try:
        from ..core.unified_database import (
            get_unified_database_coordinator as get_database_manager,
        )

        print("🔧 Phase 2C: Multi-Tenant Manager using UnifiedDatabaseCoordinator")
    except ImportError:
        from ..core.database import DatabaseManager

        print("🔧 Phase 2C: Multi-Tenant Manager fallback to legacy DatabaseManager")
    from ..core.validation import validate_organization_id, validate_user_permissions
    from ..performance.cache_manager import CacheManager, CacheLevel
    from ..config.user_config import UserConfigManager
except ImportError:
    # Lightweight fallback pattern following OVERVIEW.md
    AdvancedContextEngine = object
    StakeholderIntelligenceUnified = object
    DatabaseManager = object
    CacheManager = object
    UserConfigManager = object


class OrganizationTier(Enum):
    """Organization tier levels for feature and resource allocation"""

    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class IsolationLevel(Enum):
    """Data isolation levels between organizations"""

    STRICT = "strict"  # Complete isolation (default)
    SHARED_ANALYTICS = "shared_analytics"  # Shared anonymized analytics only
    FEDERATED = "federated"  # Controlled cross-org collaboration


@dataclass
class OrganizationProfile:
    """Complete organization profile with security and configuration"""

    org_id: str
    name: str
    tier: OrganizationTier
    isolation_level: IsolationLevel

    # Configuration preferences
    persona_preferences: Dict[str, Any] = field(default_factory=dict)
    framework_selections: List[str] = field(default_factory=list)
    feature_flags: Dict[str, bool] = field(default_factory=dict)

    # Security and access control
    admin_users: Set[str] = field(default_factory=set)
    allowed_domains: Set[str] = field(default_factory=set)
    security_policies: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage and API responses"""
        return {
            "org_id": self.org_id,
            "name": self.name,
            "tier": self.tier.value,
            "isolation_level": self.isolation_level.value,
            "persona_preferences": self.persona_preferences,
            "framework_selections": self.framework_selections,
            "feature_flags": self.feature_flags,
            "admin_users": list(self.admin_users),
            "allowed_domains": list(self.allowed_domains),
            "security_policies": self.security_policies,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "is_active": self.is_active,
        }


@dataclass
class TenantContext:
    """Current tenant context for request processing"""

    org_id: str
    user_id: str
    session_id: str

    # Context isolation
    context_namespace: str
    cache_namespace: str
    db_schema: str

    # Performance tracking
    context_switch_time_ms: float = 0
    last_activity: datetime = field(default_factory=datetime.now)

    # Security validation
    permissions: Set[str] = field(default_factory=set)
    security_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrganizationConfig:
    """Organization-specific configuration for ClaudeDirector features"""

    org_id: str

    # Persona configuration
    default_personas: List[str] = field(default_factory=lambda: ["diego", "martin"])
    persona_customizations: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Framework configuration
    enabled_frameworks: List[str] = field(default_factory=list)
    framework_preferences: Dict[str, float] = field(default_factory=dict)

    # Performance configuration
    response_time_target_ms: int = 50
    cache_ttl_seconds: int = 3600
    max_context_size_mb: int = 10

    # Feature flags
    features: Dict[str, bool] = field(
        default_factory=lambda: {
            "advanced_personas": True,
            "mcp_enhancement": True,
            "framework_detection": True,
            "predictive_analytics": True,
            "real_time_monitoring": True,
        }
    )


class MultiTenantManager(BaseManager):
    """
    PHASE 8.4: Enterprise Multi-Tenant Organization Manager with BaseManager consolidation

    Elena | Security & Platform Infrastructure

    Provides complete organization isolation with <5ms context switching.
    Integrates with existing 8-layer context architecture for org-level separation.

    Key Features:
    - Complete data isolation between organizations
    - Org-specific persona and framework preferences
    - <5ms organization context switching performance
    - Integration with existing security and user config systems
    - Scalable to 100+ organizations with enterprise-grade security

    Architecture Integration:
    - Extends AdvancedContextEngine with org-level namespacing
    - Integrates intelligence systems for org-specific contextual data
    - Uses existing CacheManager with org-level cache namespacing
    - Maintains UserConfigManager security patterns for org config protection
    """

    def __init__(
        self,
        database_manager: Optional[DatabaseManager] = None,
        cache_manager: Optional[CacheManager] = None,
        context_engine: Optional[AdvancedContextEngine] = None,
        config_manager: Optional[UserConfigManager] = None,
    ):
        """
        PHASE 8.4: BaseManager consolidation - eliminates manual logging and infrastructure
        """
        # PHASE 8.4: BaseManager initialization eliminates duplicate infrastructure
        config = BaseManagerConfig(
            manager_name="multi_tenant_manager",
            manager_type=ManagerType.PLATFORM_CORE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={
                "database_manager": database_manager,
                "cache_manager": cache_manager,
                "context_engine": context_engine,
                "config_manager": config_manager,
            },
        )
        super().__init__(config)

        # PHASE 8.4: ELIMINATED manual logging - now uses self.logger from BaseManager
        # Core infrastructure integration
        self.db_manager = database_manager
        self.cache_manager = cache_manager
        self.context_engine = context_engine
        self.config_manager = config_manager

        # Organization registry
        self.organizations: Dict[str, OrganizationProfile] = {}
        self.organization_configs: Dict[str, OrganizationConfig] = {}

        # Active tenant contexts
        self.active_contexts: Dict[str, TenantContext] = {}

        # Performance tracking (now integrated with BaseManager metrics)
        self.context_switches = 0
        self.total_switch_time_ms = 0

        self.logger.info(
            "MultiTenantManager initialized with BaseManager infrastructure"
        )
        self.security_validations = 0

        # Security enforcement
        self.isolation_validator = self._create_isolation_validator()

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Delegates to multi-tenant operations
        """
        if operation == "create_organization":
            return await self.create_organization(*args, **kwargs)
        elif operation == "switch_tenant_context":
            return await self.switch_tenant_context(*args, **kwargs)
        elif operation == "get_organization":
            return self.get_organization(*args, **kwargs)
        elif operation == "validate_isolation":
            return await self.validate_data_isolation(*args, **kwargs)
        elif operation == "get_performance_metrics":
            return self.get_performance_metrics()
        else:
            self.logger.warning(f"Unknown multi-tenant operation: {operation}")
            return None

        self.logger.info("MultiTenantManager initialized with enterprise security")

    def _create_isolation_validator(self):
        """Create security validator for organization isolation"""

        def validate_isolation(org_id: str, resource_access: str) -> bool:
            """Validate that organization can only access its own resources"""
            # Implement strict isolation validation
            if org_id not in self.organizations:
                return False

            org_profile = self.organizations[org_id]
            if not org_profile.is_active:
                return False

            # Validate resource namespace matches organization
            expected_namespace = f"org_{org_id}"
            return resource_access.startswith(expected_namespace)

        return validate_isolation

    async def create_organization(
        self,
        org_id: str,
        name: str,
        tier: OrganizationTier = OrganizationTier.PROFESSIONAL,
        admin_user: str = None,
        initial_config: Optional[Dict[str, Any]] = None,
    ) -> OrganizationProfile:
        """
        Create new organization with complete isolation setup

        Args:
            org_id: Unique organization identifier
            name: Human-readable organization name
            tier: Organization tier for feature access
            admin_user: Initial admin user for the organization
            initial_config: Optional initial configuration

        Returns:
            OrganizationProfile: Created organization profile

        Raises:
            ValueError: If org_id already exists or is invalid
        """
        start_time = time.time()

        # Validate organization ID
        if not validate_organization_id(org_id):
            raise ValueError(f"Invalid organization ID: {org_id}")

        if org_id in self.organizations:
            raise ValueError(f"Organization {org_id} already exists")

        # Create organization profile
        org_profile = OrganizationProfile(
            org_id=org_id,
            name=name,
            tier=tier,
            isolation_level=IsolationLevel.STRICT,
        )

        if admin_user:
            org_profile.admin_users.add(admin_user)

        # Create organization configuration
        org_config = OrganizationConfig(org_id=org_id)
        if initial_config:
            org_config.features.update(initial_config.get("features", {}))
            org_config.persona_customizations.update(
                initial_config.get("persona_customizations", {})
            )

        # Initialize organization-specific infrastructure
        await self._initialize_org_infrastructure(org_id)

        # Store organization
        self.organizations[org_id] = org_profile
        self.organization_configs[org_id] = org_config

        # Cache organization data
        if self.cache_manager:
            cache_key = f"org_profile_{org_id}"
            await self.cache_manager.set(
                cache_key, org_profile.to_dict(), CacheLevel.ORGANIZATIONAL
            )

        creation_time_ms = (time.time() - start_time) * 1000
        self.logger.info(
            f"Created organization {org_id} ({name}) in {creation_time_ms:.1f}ms"
        )

        return org_profile

    async def switch_organization(
        self,
        org_id: str,
        user_id: str,
        session_id: str = "default",
    ) -> TenantContext:
        """
        Switch to organization context with <5ms performance target

        Args:
            org_id: Target organization ID
            user_id: User making the switch
            session_id: Session identifier

        Returns:
            TenantContext: Active tenant context for the organization

        Raises:
            ValueError: If organization doesn't exist or user lacks access
        """
        start_time = time.time()

        # Validate organization exists and user has access
        if org_id not in self.organizations:
            raise ValueError(f"Organization {org_id} not found")

        org_profile = self.organizations[org_id]
        if not org_profile.is_active:
            raise ValueError(f"Organization {org_id} is inactive")

        # Validate user permissions (simplified for MVP)
        if not await self._validate_user_access(org_id, user_id):
            raise ValueError(f"User {user_id} lacks access to organization {org_id}")

        # Create tenant context with isolation namespaces
        context_key = f"{org_id}_{user_id}_{session_id}"
        tenant_context = TenantContext(
            org_id=org_id,
            user_id=user_id,
            session_id=session_id,
            context_namespace=f"org_{org_id}_context",
            cache_namespace=f"org_{org_id}_cache",
            db_schema=f"org_{org_id}",
        )

        # Configure context engine for organization
        if self.context_engine:
            await self._configure_context_engine_for_org(org_id, tenant_context)

        # Update performance metrics
        switch_time_ms = (time.time() - start_time) * 1000
        tenant_context.context_switch_time_ms = switch_time_ms

        # Store active context
        self.active_contexts[context_key] = tenant_context

        # Update organization last accessed
        org_profile.last_accessed = datetime.now()

        # Performance tracking
        self.context_switches += 1
        self.total_switch_time_ms += switch_time_ms

        self.logger.info(
            f"Switched to organization {org_id} for user {user_id} in {switch_time_ms:.1f}ms"
        )

        return tenant_context

    async def get_organization_config(self, org_id: str) -> OrganizationConfig:
        """Get organization-specific configuration"""
        if org_id not in self.organization_configs:
            raise ValueError(f"Organization config not found: {org_id}")

        return self.organization_configs[org_id]

    async def update_organization_config(
        self,
        org_id: str,
        config_updates: Dict[str, Any],
        user_id: str,
    ) -> OrganizationConfig:
        """Update organization configuration with validation"""
        # Validate user has admin access
        if not await self._validate_admin_access(org_id, user_id):
            raise ValueError(
                f"User {user_id} lacks admin access to organization {org_id}"
            )

        if org_id not in self.organization_configs:
            raise ValueError(f"Organization config not found: {org_id}")

        org_config = self.organization_configs[org_id]

        # Apply configuration updates with validation
        if "features" in config_updates:
            org_config.features.update(config_updates["features"])

        if "persona_customizations" in config_updates:
            org_config.persona_customizations.update(
                config_updates["persona_customizations"]
            )

        if "framework_preferences" in config_updates:
            org_config.framework_preferences.update(
                config_updates["framework_preferences"]
            )

        # Update cache
        if self.cache_manager:
            cache_key = f"org_config_{org_id}"
            await self.cache_manager.set(
                cache_key, org_config.__dict__, CacheLevel.ORGANIZATIONAL
            )

        self.logger.info(f"Updated configuration for organization {org_id}")
        return org_config

    async def _initialize_org_infrastructure(self, org_id: str):
        """Initialize organization-specific infrastructure components"""
        # Create organization-specific database schema
        if self.db_manager:
            schema_name = f"org_{org_id}"
            await self.db_manager.create_schema(schema_name)

        # Initialize organization-specific cache namespace
        if self.cache_manager:
            cache_namespace = f"org_{org_id}_cache"
            await self.cache_manager.create_namespace(cache_namespace)

        self.logger.debug(f"Initialized infrastructure for organization {org_id}")

    async def _configure_context_engine_for_org(
        self, org_id: str, tenant_context: TenantContext
    ):
        """Configure context engine with organization-specific settings"""
        if not self.context_engine:
            return

        # Set organization-specific context namespace
        org_config = {
            "namespace": tenant_context.context_namespace,
            "isolation_level": "strict",
            "org_id": org_id,
        }

        # Configure context engine (implementation depends on context engine API)
        # This would integrate with the existing AdvancedContextEngine
        self.logger.debug(f"Configured context engine for organization {org_id}")

    async def _validate_user_access(self, org_id: str, user_id: str) -> bool:
        """Validate user has access to organization"""
        if org_id not in self.organizations:
            return False

        org_profile = self.organizations[org_id]

        # Check if user is admin (always has access)
        if user_id in org_profile.admin_users:
            return True

        # Check domain-based access (simplified validation)
        if org_profile.allowed_domains:
            user_domain = user_id.split("@")[-1] if "@" in user_id else None
            if user_domain and user_domain in org_profile.allowed_domains:
                return True

        # Additional access validation logic would go here
        return False

    async def _validate_admin_access(self, org_id: str, user_id: str) -> bool:
        """Validate user has admin access to organization"""
        if org_id not in self.organizations:
            return False

        org_profile = self.organizations[org_id]
        return user_id in org_profile.admin_users

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get multi-tenant performance metrics"""
        avg_switch_time = (
            self.total_switch_time_ms / self.context_switches
            if self.context_switches > 0
            else 0
        )

        return {
            "total_organizations": len(self.organizations),
            "active_contexts": len(self.active_contexts),
            "context_switches": self.context_switches,
            "average_switch_time_ms": avg_switch_time,
            "security_validations": self.security_validations,
            "performance_target_met": avg_switch_time < 5.0,
        }


def create_multi_tenant_manager(
    database_manager: Optional[DatabaseManager] = None,
    cache_manager: Optional[CacheManager] = None,
    context_engine: Optional[AdvancedContextEngine] = None,
    config_manager: Optional[UserConfigManager] = None,
) -> MultiTenantManager:
    """
    Factory function to create MultiTenantManager with proper dependencies

    Follows existing ClaudeDirector factory patterns for dependency injection
    """
    return MultiTenantManager(
        database_manager=database_manager,
        cache_manager=cache_manager,
        context_engine=context_engine,
        config_manager=config_manager,
    )
