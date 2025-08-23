"""
Business-Critical Regression Tests

Alvaro's comprehensive test suite for business-critical functionality
that must never regress. These tests protect core business value and
ensure system reliability for strategic decision making.

Test Categories:
- Configuration Persistence: User settings and customization data
- ROI Tracking: Investment analysis and business value measurement
- Performance: System performance under realistic executive load
- Security: Data protection and access control validation

BUSINESS IMPACT: Failures in these areas lead to:
- User frustration and abandonment
- Poor investment decisions
- System unreliability
- Data breaches and compliance violations
"""

from .test_configuration_persistence import TestConfigurationPersistence
from .test_roi_tracking import TestROITracking
from .test_performance import TestPerformance
from .test_security import TestSecurity

__all__ = [
    "TestConfigurationPersistence",
    "TestROITracking",
    "TestPerformance",
    "TestSecurity",
]
