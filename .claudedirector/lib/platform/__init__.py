"""
Platform Management Module - Phase 14 Track 2

Enterprise-grade platform capabilities for ClaudeDirector multi-tenant support.
Implements multi-organization isolation, configuration management, and scalability.

Architecture Integration:
- Extends existing context_engineering 8-layer architecture
- Builds on performance optimization foundation (<500ms → <50ms)
- Maintains P0 test protection and architectural compliance
- Integrates with existing MCP enhancement and transparency systems
"""

from .multi_tenant_manager import (
    MultiTenantManager,
    OrganizationConfig,
    TenantContext,
    OrganizationProfile,
    create_multi_tenant_manager,
)

from .enterprise_config import (
    EnterpriseConfigManager,
    FeatureFlag,
    ConfigurationProfile,
    EnvironmentProfile,
)

__all__ = [
    "MultiTenantManager",
    "OrganizationConfig",
    "TenantContext",
    "OrganizationProfile",
    "create_multi_tenant_manager",
    "EnterpriseConfigManager",
    "FeatureFlag",
    "ConfigurationProfile",
    "EnvironmentProfile",
]
