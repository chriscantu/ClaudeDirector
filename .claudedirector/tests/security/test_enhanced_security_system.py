#!/usr/bin/env python3
"""
Comprehensive tests for enhanced security system
Verifies trust rebuilding architecture
"""

import unittest
import tempfile
import sys
from pathlib import Path

# Add security modules to path
sys.path.append(".claudedirector/dev-tools/security")

from enhanced_security_scanner import EnhancedSecurityScanner
from security_validation_system import SecurityValidationSystem
from continuous_security_monitor import ContinuousSecurityMonitor


class TestEnhancedSecuritySystem(unittest.TestCase):
    """Test suite for enhanced security system"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = EnhancedSecurityScanner()
        self.validator = SecurityValidationSystem()
        self.monitor = ContinuousSecurityMonitor()

    def test_stakeholder_pattern_detection(self):
        """Test that scanner detects stakeholder intelligence threats"""
        test_content = """
        # Test file with stakeholder threats
        director_x = "sensitive information"
        slt_member_y = "strategic data"
        test_executive = "confidential meeting notes"
        sensitive_stakeholder_info = "threat pattern"
        """

        test_file = Path(self.temp_dir) / "test_stakeholder.py"
        test_file.write_text(test_content)

        violations = self.scanner._scan_stakeholder_data(str(test_file))

        # Should detect multiple violations
        self.assertGreater(
            len(violations), 0, "Scanner should detect stakeholder threats"
        )

        # Check for critical severity
        critical_violations = [v for v in violations if v["severity"] == "CRITICAL"]
        self.assertGreater(
            len(critical_violations), 0, "Should detect critical violations"
        )

    def test_strategic_intelligence_detection(self):
        """Test that scanner detects strategic intelligence threats"""
        test_content = """
        # Strategic intelligence threats
        quarterly_business_metrics = "sensitive business data"
        market_analysis_data = "market analysis"
        strategy_document_internal = "confidential strategy"
        """

        test_file = Path(self.temp_dir) / "test_strategic.py"
        test_file.write_text(test_content)

        violations = self.scanner._scan_strategic_intelligence(str(test_file))

        # Should detect strategic threats
        self.assertGreater(
            len(violations), 0, "Scanner should detect strategic intelligence"
        )

    def test_comprehensive_scan_scoring(self):
        """Test comprehensive scan and security scoring"""
        # Create test file with no threats
        clean_file = Path(self.temp_dir) / "clean_file.py"
        clean_file.write_text("# Clean file with no threats\nprint('hello world')")

        # Mock staged files to include our clean file
        original_get_staged = self.scanner._get_staged_files
        self.scanner._get_staged_files = lambda: [str(clean_file)]

        scan_report = self.scanner.comprehensive_scan()

        # Restore original method
        self.scanner._get_staged_files = original_get_staged

        # Should have high security score for clean file
        self.assertEqual(
            scan_report["security_score"], 100, "Clean file should have perfect score"
        )
        self.assertEqual(
            scan_report["threats_detected"], 0, "Clean file should have no threats"
        )

    def test_security_validation_system(self):
        """Test security validation system functionality"""
        validation_result = self.validator.run_comprehensive_validation()

        # Should have validation ID and timestamp
        self.assertIn("validation_id", validation_result)
        self.assertIn("timestamp", validation_result)
        self.assertIn("trust_score", validation_result)

        # Should validate multiple components
        self.assertGreaterEqual(len(validation_result["components_validated"]), 3)

        # Should generate verifiable proof
        self.assertGreater(len(validation_result["verifiable_proof"]), 0)

    def test_trust_score_calculation(self):
        """Test trust score calculation logic"""
        # Mock validation result with mixed results
        mock_validation = {
            "components_validated": [
                {"trust_impact": 45, "status": "PASSED"},  # Good component
                {"trust_impact": -20, "status": "FAILED"},  # Failed component
                {"trust_impact": 50, "status": "PASSED"},  # Another good component
            ]
        }

        trust_score = self.validator._calculate_trust_score(mock_validation)

        # Should be a reasonable score (0-100)
        self.assertGreaterEqual(trust_score, 0)
        self.assertLessEqual(trust_score, 100)

    def test_continuous_monitor_dashboard_data(self):
        """Test continuous monitor dashboard data generation"""
        dashboard_data = self.monitor.generate_security_dashboard_data()

        # Should have required fields
        required_fields = [
            "timestamp",
            "status",
            "security_posture",
            "alerts_24h",
            "system_health",
        ]
        for field in required_fields:
            self.assertIn(field, dashboard_data, f"Dashboard should include {field}")

    def test_verifiable_proof_generation(self):
        """Test that verifiable proof is properly generated"""
        validation_result = self.validator.run_comprehensive_validation()

        proof = validation_result["verifiable_proof"]

        # Should have multiple proof types
        proof_types = [p["proof_type"] for p in proof]
        expected_types = [
            "SYSTEMATIC_VALIDATION",
            "UNBYPASSABLE_ARCHITECTURE",
            "CONTINUOUS_MONITORING",
        ]

        for expected_type in expected_types:
            self.assertIn(
                expected_type, proof_types, f"Should include {expected_type} proof"
            )

    def test_scanner_self_exclusion(self):
        """Test that scanner properly excludes security files from scanning"""
        # Create a security file with patterns that would normally trigger
        security_file = Path(self.temp_dir) / "security_file.py"
        security_file.write_text(
            """
        # This is a security file
        stakeholder_patterns = ['exec_x', 'exec_y']
        sensitive_stakeholder_info = "test pattern"
        """
        )

        # Test exclusion by making the path look like a security file
        security_file_path = ".claudedirector/dev-tools/security/test_security.py"
        security_file = Path(self.temp_dir) / "test_security.py"
        security_file.write_text(
            """
        # This is a security file
        stakeholder_patterns = ['director_x', 'slt_member_y']
        sensitive_stakeholder_info = "test pattern"
        """
        )

        violations = self.scanner._scan_stakeholder_data(security_file_path)

        # Should not detect violations in excluded security files
        self.assertEqual(
            len(violations), 0, "Security files should be excluded from scanning"
        )

    def test_threat_pattern_comprehensiveness(self):
        """Test that threat patterns are comprehensive"""
        # Check stakeholder patterns
        self.assertGreater(
            len(self.scanner.stakeholder_patterns),
            5,
            "Should have comprehensive stakeholder patterns",
        )

        # Check strategic intelligence patterns
        self.assertGreater(
            len(self.scanner.strategic_intelligence_patterns),
            5,
            "Should have comprehensive strategic patterns",
        )

        # Verify patterns are real (not just placeholders)
        stakeholder_pattern_text = "".join(self.scanner.stakeholder_patterns)
        self.assertGreater(
            len(stakeholder_pattern_text),
            200,
            "Patterns should be substantial, not just placeholders",
        )

    def test_security_report_generation(self):
        """Test security report generation"""
        # Create mock scan report
        mock_scan = {
            "scan_id": "test123",
            "timestamp": "2025-01-01T00:00:00",
            "scanner_version": "2.0-test",
            "violations": [],
            "files_scanned": 5,
            "threats_detected": 0,
            "security_score": 100,
            "verifiable_proof": [{"verification_type": "TEST_PROOF", "verified": True}],
        }

        report = self.scanner.generate_security_report(mock_scan)

        # Should contain key sections
        self.assertIn("ENHANCED SECURITY SCANNER REPORT", report)
        self.assertIn("SCAN RESULTS:", report)
        self.assertIn("VERIFIABLE PROOF:", report)
        self.assertIn("Security Score: 100/100", report)

    def tearDown(self):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
