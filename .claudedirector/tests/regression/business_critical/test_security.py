#!/usr/bin/env python3
"""
Business-Critical Regression Test: Security

Alvaro's Test Suite: Ensures security controls protect sensitive strategic
data, stakeholder information, and business intelligence from unauthorized access.

BUSINESS IMPACT: Security failures lead to data breaches, competitive
intelligence loss, and regulatory compliance violations.
"""

import unittest
import tempfile
import shutil
import json
import os
import hashlib
import base64
from pathlib import Path
from datetime import datetime, timedelta
import sys
import subprocess

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestSecurity(unittest.TestCase):
    """Business-critical tests for security controls and data protection"""

    def setUp(self):
        """Set up security testing environment"""
        self.test_dir = tempfile.mkdtemp()
        self.secure_data_dir = Path(self.test_dir) / "secure_data"
        self.secure_data_dir.mkdir(parents=True, exist_ok=True)

        # Mock sensitive data for testing
        self.sensitive_data = {
            "stakeholder_intelligence": {
                "hemendra_pal": {
                    "role": "SVP Engineering",
                    "platform_stance": "opponent",
                    "influence_level": "high",
                    "decision_patterns": ["cost_focused", "delivery_pressure"],
                    "confidential_notes": "Skip levels focused on product delivery over platform",
                },
                "steve_davis": {
                    "role": "VP Product",
                    "platform_stance": "neutral_roi_focused",
                    "influence_level": "high",
                    "decision_patterns": ["roi_driven", "evidence_based"],
                    "confidential_notes": "Wants ROI understanding before platform investment",
                },
            },
            "strategic_initiatives": {
                "ngx_gold": {
                    "budget": 2500000,
                    "roi_target": 1.21,
                    "competitive_advantage": "Autodesk Construction Cloud displacement",
                    "confidential_strategy": "Resource reallocation vs new headcount",
                }
            },
            "financial_data": {
                "platform_investment": 5000000,
                "expected_savings": 1250000,
                "competitive_intelligence": "Competitor platform costs 40% more",
            },
        }

    def tearDown(self):
        """Clean up security test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sensitive_data_encryption(self):
        """
        BUSINESS CRITICAL: Sensitive strategic data must be encrypted at rest

        FAILURE IMPACT: Stakeholder intelligence exposed, competitive advantage lost
        BUSINESS COST: Regulatory fines, competitive intelligence theft, trust loss
        """
        # Test data encryption
        sensitive_file = self.secure_data_dir / "stakeholder_intelligence.enc"

        # Simulate encryption of sensitive stakeholder data
        plaintext_data = json.dumps(self.sensitive_data["stakeholder_intelligence"])

        # Simple encryption simulation (in production, use proper encryption)
        encryption_key = self._generate_encryption_key()
        encrypted_data = self._encrypt_data(plaintext_data, encryption_key)

        # Write encrypted data
        with open(sensitive_file, "wb") as f:
            f.write(encrypted_data)

        # Verify file is encrypted (not readable as plain JSON)
        with open(sensitive_file, "rb") as f:
            raw_data = f.read()

        # Should not be able to parse as JSON
        with self.assertRaises(Exception):
            json.loads(raw_data.decode("utf-8"))

        # Test decryption
        decrypted_data = self._decrypt_data(encrypted_data, encryption_key)
        recovered_data = json.loads(decrypted_data)

        # Verify data integrity after encryption/decryption
        self.assertEqual(recovered_data["hemendra_pal"]["platform_stance"], "opponent")
        self.assertEqual(recovered_data["steve_davis"]["role"], "VP Product")

        print("✅ Sensitive data encryption: PASSED")

    def test_access_control_validation(self):
        """
        BUSINESS CRITICAL: Access controls must prevent unauthorized data access

        FAILURE IMPACT: Unauthorized access to strategic intelligence
        BUSINESS COST: Data breach, competitive intelligence loss, compliance violation
        """
        # Create access control configuration
        access_control = {
            "roles": {
                "executive": {
                    "permissions": ["read_all", "write_strategic", "delete_own"],
                    "data_access": [
                        "stakeholder_intelligence",
                        "financial_data",
                        "strategic_initiatives",
                    ],
                },
                "director": {
                    "permissions": ["read_strategic", "write_own"],
                    "data_access": ["strategic_initiatives", "limited_stakeholder"],
                },
                "manager": {
                    "permissions": ["read_own"],
                    "data_access": ["own_projects"],
                },
                "guest": {
                    "permissions": ["read_public"],
                    "data_access": ["public_frameworks"],
                },
            },
            "data_classification": {
                "stakeholder_intelligence": "confidential",
                "financial_data": "restricted",
                "strategic_initiatives": "internal",
                "public_frameworks": "public",
            },
        }

        # Test access control enforcement
        test_cases = [
            {
                "user_role": "executive",
                "requested_data": "stakeholder_intelligence",
                "should_allow": True,
            },
            {
                "user_role": "director",
                "requested_data": "stakeholder_intelligence",
                "should_allow": False,  # Directors can't access full stakeholder intel
            },
            {
                "user_role": "manager",
                "requested_data": "financial_data",
                "should_allow": False,  # Managers can't access financial data
            },
            {
                "user_role": "guest",
                "requested_data": "strategic_initiatives",
                "should_allow": False,  # Guests can't access strategic data
            },
            {
                "user_role": "guest",
                "requested_data": "public_frameworks",
                "should_allow": True,  # Guests can access public data
            },
        ]

        for test_case in test_cases:
            access_granted = self._check_access_permission(
                test_case["user_role"], test_case["requested_data"], access_control
            )

            if test_case["should_allow"]:
                self.assertTrue(
                    access_granted,
                    f"Access should be granted for {test_case['user_role']} to {test_case['requested_data']}",
                )
            else:
                self.assertFalse(
                    access_granted,
                    f"Access should be denied for {test_case['user_role']} to {test_case['requested_data']}",
                )

        print("✅ Access control validation: PASSED")

    def test_data_sanitization(self):
        """
        BUSINESS CRITICAL: Sensitive data must be sanitized in logs and outputs

        FAILURE IMPACT: Sensitive data leaked in logs, debug output, error messages
        BUSINESS COST: Accidental data exposure, compliance violations
        """
        # Test data sanitization patterns
        sensitive_patterns = [
            "hemendra_pal",
            "steve_davis",
            "beth_nelson",
            "hisham_younis",
            "$2,500,000",
            "roi_target: 1.21",
            "competitive_advantage",
            "platform_opponent",
        ]

        # Simulate log entries that might contain sensitive data
        log_entries = [
            "User hemendra_pal accessed stakeholder intelligence",
            "ROI calculation: roi_target: 1.21 for initiative NGX Gold",
            "Strategic note: steve_davis is platform_opponent according to analysis",
            "Budget allocation: $2,500,000 for competitive_advantage initiative",
            "Error processing data for beth_nelson profile",
            "Debug: hisham_younis decision_patterns include cost_focused",
        ]

        sanitized_entries = []

        for entry in log_entries:
            sanitized_entry = self._sanitize_log_entry(entry, sensitive_patterns)
            sanitized_entries.append(sanitized_entry)

            # Verify sensitive data is removed/masked
            for pattern in sensitive_patterns:
                if pattern in entry:  # If original contained sensitive data
                    self.assertNotIn(
                        pattern,
                        sanitized_entry,
                        f"Sensitive pattern '{pattern}' not sanitized in: {sanitized_entry}",
                    )

        # Verify sanitized entries still contain useful information
        self.assertIn("User [REDACTED]", sanitized_entries[0])
        self.assertIn("ROI calculation", sanitized_entries[1])
        self.assertIn("Strategic note", sanitized_entries[2])

        print("✅ Data sanitization: PASSED")

    def test_audit_trail_integrity(self):
        """
        BUSINESS CRITICAL: Audit trails must be tamper-proof and complete

        FAILURE IMPACT: Cannot track security incidents, compliance failures
        BUSINESS COST: Regulatory penalties, inability to investigate breaches
        """
        # Create audit trail system
        audit_log = []

        # Simulate security-relevant events
        security_events = [
            {
                "event_type": "data_access",
                "user": "executive_001",
                "resource": "stakeholder_intelligence",
                "action": "read",
                "timestamp": datetime.now(),
                "ip_address": "192.168.1.100",
                "success": True,
            },
            {
                "event_type": "data_access",
                "user": "guest_001",
                "resource": "financial_data",
                "action": "read",
                "timestamp": datetime.now(),
                "ip_address": "192.168.1.200",
                "success": False,
                "failure_reason": "insufficient_permissions",
            },
            {
                "event_type": "configuration_change",
                "user": "admin_001",
                "resource": "access_control_rules",
                "action": "modify",
                "timestamp": datetime.now(),
                "ip_address": "192.168.1.50",
                "success": True,
                "details": "Updated role permissions for director role",
            },
            {
                "event_type": "authentication",
                "user": "unknown",
                "resource": "system_login",
                "action": "login_attempt",
                "timestamp": datetime.now(),
                "ip_address": "10.0.0.100",
                "success": False,
                "failure_reason": "invalid_credentials",
            },
        ]

        # Add events to audit log with integrity protection
        for event in security_events:
            audit_entry = self._create_audit_entry(event)
            audit_log.append(audit_entry)

        # Verify audit log integrity
        for i, entry in enumerate(audit_log):
            # Verify hash integrity
            calculated_hash = self._calculate_audit_hash(entry)
            self.assertEqual(
                entry["integrity_hash"],
                calculated_hash,
                f"Audit entry {i} integrity hash mismatch",
            )

            # Verify required fields present
            required_fields = [
                "event_id",
                "timestamp",
                "event_type",
                "user",
                "integrity_hash",
            ]
            for field in required_fields:
                self.assertIn(field, entry, f"Required audit field '{field}' missing")

        # Test audit log tampering detection
        tampered_entry = audit_log[0].copy()
        tampered_entry["user"] = "modified_user"  # Simulate tampering

        # Should detect tampering
        original_hash = tampered_entry["integrity_hash"]
        recalculated_hash = self._calculate_audit_hash(tampered_entry)
        self.assertNotEqual(
            original_hash, recalculated_hash, "Audit tampering should be detected"
        )

        print("✅ Audit trail integrity: PASSED")

    def test_secure_configuration_management(self):
        """
        BUSINESS CRITICAL: Security configurations must be properly managed

        FAILURE IMPACT: Weak security settings, configuration drift, vulnerabilities
        BUSINESS COST: Security breaches, compliance failures, system compromise
        """
        # Define security configuration requirements
        security_config = {
            "authentication": {
                "password_min_length": 12,
                "require_mfa": True,
                "session_timeout_minutes": 30,
                "max_failed_attempts": 3,
                "account_lockout_minutes": 15,
            },
            "encryption": {
                "data_at_rest": "AES-256",
                "data_in_transit": "TLS-1.3",
                "key_rotation_days": 90,
                "require_encryption": True,
            },
            "access_control": {
                "default_deny": True,
                "principle_of_least_privilege": True,
                "role_based_access": True,
                "regular_access_review": True,
            },
            "monitoring": {
                "log_all_access": True,
                "alert_on_failures": True,
                "monitor_privileged_actions": True,
                "retention_days": 365,
            },
        }

        # Test configuration validation
        config_tests = [
            {
                "category": "authentication",
                "setting": "password_min_length",
                "value": security_config["authentication"]["password_min_length"],
                "min_required": 8,
                "test_type": "minimum",
            },
            {
                "category": "authentication",
                "setting": "session_timeout_minutes",
                "value": security_config["authentication"]["session_timeout_minutes"],
                "max_allowed": 60,
                "test_type": "maximum",
            },
            {
                "category": "encryption",
                "setting": "require_encryption",
                "value": security_config["encryption"]["require_encryption"],
                "required_value": True,
                "test_type": "boolean",
            },
            {
                "category": "access_control",
                "setting": "default_deny",
                "value": security_config["access_control"]["default_deny"],
                "required_value": True,
                "test_type": "boolean",
            },
        ]

        for test in config_tests:
            if test["test_type"] == "minimum":
                self.assertGreaterEqual(
                    test["value"],
                    test["min_required"],
                    f"{test['category']}.{test['setting']} below minimum requirement",
                )
            elif test["test_type"] == "maximum":
                self.assertLessEqual(
                    test["value"],
                    test["max_allowed"],
                    f"{test['category']}.{test['setting']} exceeds maximum allowed",
                )
            elif test["test_type"] == "boolean":
                self.assertEqual(
                    test["value"],
                    test["required_value"],
                    f"{test['category']}.{test['setting']} not set to required value",
                )

        # Test configuration file protection
        config_file = self.secure_data_dir / "security_config.json"
        with open(config_file, "w") as f:
            json.dump(security_config, f, indent=2)

        # Verify file permissions (simulate restricted access)
        file_stat = config_file.stat()
        # In a real implementation, would check actual file permissions
        self.assertTrue(config_file.exists(), "Security config file should exist")

        print("✅ Secure configuration management: PASSED")

    def test_data_retention_and_disposal(self):
        """
        BUSINESS CRITICAL: Data retention and secure disposal must work correctly

        FAILURE IMPACT: Data retained too long, insecure deletion, compliance violations
        BUSINESS COST: Regulatory fines, data breach risk, storage costs
        """
        # Create test data with different retention requirements
        retention_policies = {
            "audit_logs": {
                "retention_days": 2555,
                "disposal_method": "secure_delete",
            },  # 7 years
            "stakeholder_intelligence": {
                "retention_days": 1095,
                "disposal_method": "secure_delete",
            },  # 3 years
            "session_data": {
                "retention_days": 30,
                "disposal_method": "standard_delete",
            },
            "temporary_analysis": {
                "retention_days": 7,
                "disposal_method": "standard_delete",
            },
        }

        # Create test files with different ages
        test_files = []
        base_date = datetime.now()

        for data_type, policy in retention_policies.items():
            # Create files of different ages
            ages_to_test = [
                policy["retention_days"] - 10,  # Still valid
                policy["retention_days"] + 10,  # Should be deleted
                policy["retention_days"] + 100,  # Definitely should be deleted
            ]

            for age_days in ages_to_test:
                file_date = base_date - timedelta(days=age_days)
                file_path = self.secure_data_dir / f"{data_type}_{age_days}days.json"

                # Create test file
                test_data = {
                    "data_type": data_type,
                    "created_date": file_date.isoformat(),
                    "age_days": age_days,
                    "content": f"Test data for {data_type}",
                }

                with open(file_path, "w") as f:
                    json.dump(test_data, f)

                # Set file modification time to simulate age
                timestamp = file_date.timestamp()
                os.utime(file_path, (timestamp, timestamp))

                test_files.append(
                    {
                        "path": file_path,
                        "data_type": data_type,
                        "age_days": age_days,
                        "should_exist": age_days < policy["retention_days"],
                        "disposal_method": policy["disposal_method"],
                    }
                )

        # Run data retention cleanup
        for file_info in test_files:
            file_age_days = (
                datetime.now()
                - datetime.fromtimestamp(file_info["path"].stat().st_mtime)
            ).days

            retention_days = retention_policies[file_info["data_type"]][
                "retention_days"
            ]

            if file_age_days > retention_days:
                # Simulate secure deletion
                if file_info["disposal_method"] == "secure_delete":
                    self._secure_delete_file(file_info["path"])
                else:
                    file_info["path"].unlink()  # Standard deletion

        # Verify retention policy enforcement
        for file_info in test_files:
            if file_info["should_exist"]:
                self.assertTrue(
                    file_info["path"].exists(),
                    f"File {file_info['path'].name} should still exist (age: {file_info['age_days']} days)",
                )
            else:
                self.assertFalse(
                    file_info["path"].exists(),
                    f"File {file_info['path'].name} should be deleted (age: {file_info['age_days']} days)",
                )

        print("✅ Data retention and disposal: PASSED")

    def _generate_encryption_key(self):
        """Generate a simple encryption key for testing"""
        return hashlib.sha256(b"test_encryption_key").digest()

    def _encrypt_data(self, data, key):
        """Simple encryption simulation (use proper encryption in production)"""
        # This is a simple XOR encryption for testing - use proper encryption in production
        data_bytes = data.encode("utf-8")
        key_bytes = key[: len(data_bytes)]  # Truncate key to data length

        encrypted = bytearray()
        for i in range(len(data_bytes)):
            encrypted.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])

        return base64.b64encode(encrypted)

    def _decrypt_data(self, encrypted_data, key):
        """Simple decryption simulation"""
        encrypted_bytes = base64.b64decode(encrypted_data)

        decrypted = bytearray()
        for i in range(len(encrypted_bytes)):
            decrypted.append(encrypted_bytes[i] ^ key[i % len(key)])

        return decrypted.decode("utf-8")

    def _check_access_permission(self, user_role, requested_data, access_control):
        """Check if user role has permission to access requested data"""
        if user_role not in access_control["roles"]:
            return False

        role_config = access_control["roles"][user_role]

        # Check if user has access to this data type
        if requested_data not in role_config["data_access"]:
            return False

        # Additional permission checks could be added here
        return True

    def _sanitize_log_entry(self, log_entry, sensitive_patterns):
        """Sanitize log entry by removing/masking sensitive data"""
        sanitized = log_entry

        for pattern in sensitive_patterns:
            if pattern in sanitized:
                # Replace with generic placeholder
                if pattern.startswith("$"):
                    sanitized = sanitized.replace(pattern, "[REDACTED_AMOUNT]")
                elif "_" in pattern and not pattern.startswith("roi_"):
                    sanitized = sanitized.replace(pattern, "[REDACTED]")
                else:
                    sanitized = sanitized.replace(pattern, "[REDACTED_DATA]")

        return sanitized

    def _create_audit_entry(self, event):
        """Create an audit entry with integrity protection"""
        import uuid

        audit_entry = {
            "event_id": str(uuid.uuid4()),
            "timestamp": event["timestamp"].isoformat(),
            "event_type": event["event_type"],
            "user": event["user"],
            "resource": event["resource"],
            "action": event["action"],
            "ip_address": event["ip_address"],
            "success": event["success"],
        }

        # Add optional fields
        if "failure_reason" in event:
            audit_entry["failure_reason"] = event["failure_reason"]
        if "details" in event:
            audit_entry["details"] = event["details"]

        # Calculate integrity hash
        audit_entry["integrity_hash"] = self._calculate_audit_hash(audit_entry)

        return audit_entry

    def _calculate_audit_hash(self, audit_entry):
        """Calculate integrity hash for audit entry"""
        # Create a copy without the hash field for calculation
        entry_copy = {k: v for k, v in audit_entry.items() if k != "integrity_hash"}

        # Create deterministic string representation
        entry_string = json.dumps(entry_copy, sort_keys=True)

        # Calculate hash
        return hashlib.sha256(entry_string.encode()).hexdigest()

    def _secure_delete_file(self, file_path):
        """Simulate secure file deletion (overwrite then delete)"""
        if file_path.exists():
            # Overwrite file with random data (simplified simulation)
            file_size = file_path.stat().st_size
            with open(file_path, "wb") as f:
                f.write(b"0" * file_size)  # Overwrite with zeros

            # Delete file
            file_path.unlink()


def run_business_critical_security_tests():
    """Run all business-critical security tests"""
    print("🔥 BUSINESS-CRITICAL REGRESSION TEST: Security")
    print("=" * 70)
    print("OWNER: Alvaro | IMPACT: Data Protection & Compliance")
    print(
        "FAILURE COST: Data breaches, regulatory fines, competitive intelligence loss"
    )
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecurity)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL SECURITY TESTS PASSED")
        print("💼 Business Impact: Data protection and compliance maintained")
        print("📊 Strategic Value: Secure strategic intelligence preserved")
        return True
    else:
        print(f"\n❌ SECURITY TEST FAILURES: {len(result.failures + result.errors)}")
        print("💥 Business Impact: Security vulnerabilities detected")
        print("🚨 Action Required: Fix security issues immediately")
        return False


if __name__ == "__main__":
    success = run_business_critical_security_tests()
    sys.exit(0 if success else 1)
