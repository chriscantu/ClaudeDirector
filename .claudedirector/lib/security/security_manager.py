#!/usr/bin/env python3
"""
Security Manager for ClaudeDirector
Consolidates security validation, monitoring, and scanning into unified BaseManager.
Refactored to inherit from BaseManager for DRY compliance.
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import BaseManager infrastructure
try:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from ..core.manager_factory import register_manager_type
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from core.manager_factory import register_manager_type


class SecurityManager(BaseManager):
    """
    Unified security management for ClaudeDirector

    Consolidates functionality from:
    - EnhancedSecurityScanner
    - SecurityValidationSystem
    - ContinuousSecurityMonitor
    - SensitiveDataScanner

    Features:
    - Comprehensive security validation
    - Real-time security monitoring
    - Threat pattern detection
    - Trust rebuilding through verification
    - Data protection and validation

    Refactored to inherit from BaseManager for DRY compliance.
    Eliminates duplicate logging, metrics, and configuration patterns.
    """

    def __init__(
        self,
        config: Optional[BaseManagerConfig] = None,
        cache: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        if config is None:
            config = BaseManagerConfig(
                manager_name="security_manager",
                manager_type=ManagerType.SECURITY,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                performance_tracking=True,
                custom_config={
                    "validation_log_dir": ".claudedirector/logs/security",
                    "monitoring_enabled": True,
                    "threat_detection_enabled": True,
                    "trust_rebuilding_mode": True,
                },
            )

        super().__init__(config, cache, metrics, logger_name="SecurityManager")

        # Initialize security subsystems
        self.validation_log_dir = Path(
            self.config.custom_config.get(
                "validation_log_dir", ".claudedirector/logs/security"
            )
        )
        self.validation_log_dir.mkdir(parents=True, exist_ok=True)

        # Trust rebuilding metrics
        self.trust_metrics = {
            "total_validations": 0,
            "violations_prevented": 0,
            "false_positives": 0,
            "system_bypasses": 0,  # Must always be 0
            "confidence_score": 0.0,
        }

        # Enhanced threat patterns (consolidated from multiple scanners)
        self.threat_patterns = {
            "stakeholder_patterns": [
                r"(?i)\b(john|jane|smith|doe)\s+(doe|smith)\b",
                r"(?i)\b(ceo|cto|vp)\s+[a-z]+\b",
                r"(?i)\b(director|manager)\s+[a-z]+\b",
            ],
            "strategic_patterns": [
                r"(?i)\b(confidential|secret|internal)\b",
                r"(?i)\b(strategic|roadmap|budget)\b",
                r"(?i)\b(acquisition|merger|layoff)\b",
                r"(?i)\b(revenue|profit|cost)\s+\$?\d+",
            ],
            "sensitive_data_patterns": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
                r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
                r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # Credit card
                r"\b(api[_-]?key|token|secret)[:\s=]\s*['\"][^'\"]+['\"]",  # API keys
            ],
        }

        self.logger.info(
            "Security manager initialized",
            validation_log_dir=str(self.validation_log_dir),
            monitoring_enabled=self.config.custom_config.get(
                "monitoring_enabled", True
            ),
            threat_patterns_loaded=len(self.threat_patterns),
        )

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Implement BaseManager abstract method for security operations
        """
        import time

        start_time = time.time()

        try:
            if operation == "comprehensive_scan":
                result = self.comprehensive_security_scan(*args, **kwargs)
            elif operation == "validate_files":
                result = self.validate_staged_files(*args, **kwargs)
            elif operation == "monitor_security":
                result = self.run_security_monitoring(*args, **kwargs)
            elif operation == "check_threats":
                result = self.detect_threats(*args, **kwargs)
            elif operation == "validate_trust":
                result = self.validate_trust_metrics()
            elif operation == "scan_sensitive_data":
                result = self.scan_for_sensitive_data(*args, **kwargs)
            else:
                raise ValueError(f"Unknown security operation: {operation}")

            duration = time.time() - start_time
            self._update_metrics(operation, duration, True)

            return result

        except Exception as e:
            duration = time.time() - start_time
            self._update_metrics(operation, duration, False)

            self.logger.error(
                "Security operation failed",
                operation=operation,
                error=str(e),
                args=args,
                kwargs=kwargs,
            )
            raise

    def comprehensive_security_scan(
        self, files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run comprehensive security scan with trust rebuilding focus
        Consolidates functionality from EnhancedSecurityScanner
        """
        scan_result = {
            "scan_id": self._generate_scan_id(),
            "timestamp": datetime.now().isoformat(),
            "scan_type": "COMPREHENSIVE_SECURITY_SCAN",
            "files_scanned": 0,
            "threats_detected": 0,
            "violations": [],
            "trust_score": 0,
            "verifiable_proof": {},
        }

        try:
            # Get files to scan
            if files is None:
                files = self._get_staged_files()

            scan_result["files_scanned"] = len(files)

            # Scan each file for threats
            for file_path in files:
                file_violations = self._scan_file_for_threats(file_path)
                if file_violations:
                    scan_result["violations"].extend(file_violations)
                    scan_result["threats_detected"] += len(file_violations)

            # Calculate trust score
            scan_result["trust_score"] = self._calculate_trust_score(scan_result)

            # Generate verifiable proof
            scan_result["verifiable_proof"] = self._generate_trust_proof(scan_result)

            # Update trust metrics
            self.trust_metrics["total_validations"] += 1
            if scan_result["threats_detected"] > 0:
                self.trust_metrics["violations_prevented"] += scan_result[
                    "threats_detected"
                ]

            # Log scan results
            self._log_security_event("comprehensive_scan", scan_result)

            self.logger.info(
                "Comprehensive security scan completed",
                files_scanned=scan_result["files_scanned"],
                threats_detected=scan_result["threats_detected"],
                trust_score=scan_result["trust_score"],
            )

            return scan_result

        except Exception as e:
            self.logger.error("Comprehensive security scan failed", error=str(e))
            raise

    def validate_staged_files(self) -> bool:
        """
        Validate staged git files for security violations
        Returns True if all files pass validation
        """
        scan_result = self.comprehensive_security_scan()
        return scan_result["threats_detected"] == 0

    def run_security_monitoring(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Run continuous security monitoring
        Consolidates functionality from ContinuousSecurityMonitor
        """
        monitoring_result = {
            "monitoring_id": self._generate_scan_id(),
            "start_time": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
            "alerts_generated": 0,
            "status": "monitoring",
        }

        self.logger.info(
            "Starting security monitoring",
            duration_minutes=duration_minutes,
            monitoring_id=monitoring_result["monitoring_id"],
        )

        # This would normally run continuous monitoring
        # For now, we'll do a point-in-time security check
        scan_result = self.comprehensive_security_scan()

        if scan_result["threats_detected"] > 0:
            monitoring_result["alerts_generated"] = scan_result["threats_detected"]
            monitoring_result["status"] = "alerts_active"
        else:
            monitoring_result["status"] = "secure"

        monitoring_result["end_time"] = datetime.now().isoformat()

        self._log_security_event("monitoring", monitoring_result)

        return monitoring_result

    def detect_threats(self, content: str) -> List[Dict[str, Any]]:
        """
        Detect security threats in content using consolidated threat patterns
        """
        threats = []

        for category, patterns in self.threat_patterns.items():
            for pattern in patterns:
                import re

                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    threats.append(
                        {
                            "category": category,
                            "pattern": pattern,
                            "match": match.group(),
                            "start": match.start(),
                            "end": match.end(),
                            "severity": self._get_threat_severity(category),
                        }
                    )

        return threats

    def scan_for_sensitive_data(
        self, files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Scan for sensitive data patterns
        Consolidates functionality from SensitiveDataScanner
        """
        if files is None:
            files = self._get_staged_files()

        sensitive_data_result = {
            "scan_id": self._generate_scan_id(),
            "timestamp": datetime.now().isoformat(),
            "files_scanned": len(files),
            "sensitive_data_found": 0,
            "violations": [],
        }

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    threats = self.detect_threats(content)
                    sensitive_threats = [
                        t for t in threats if t["category"] == "sensitive_data_patterns"
                    ]

                    if sensitive_threats:
                        sensitive_data_result["sensitive_data_found"] += len(
                            sensitive_threats
                        )
                        sensitive_data_result["violations"].extend(
                            [
                                {
                                    "file": file_path,
                                    "threat": threat,
                                }
                                for threat in sensitive_threats
                            ]
                        )
            except Exception as e:
                self.logger.warning(f"Could not scan file {file_path}: {e}")

        return sensitive_data_result

    def validate_trust_metrics(self) -> Dict[str, Any]:
        """
        Validate and return current trust metrics
        """
        # Calculate confidence score
        total_operations = max(1, self.trust_metrics["total_validations"])
        success_rate = (
            total_operations - self.trust_metrics["false_positives"]
        ) / total_operations

        self.trust_metrics["confidence_score"] = min(1.0, success_rate * 0.9 + 0.1)

        return {
            "trust_metrics": self.trust_metrics.copy(),
            "validation_timestamp": datetime.now().isoformat(),
            "system_integrity": self.trust_metrics["system_bypasses"] == 0,
        }

    def _scan_file_for_threats(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan a single file for security threats"""
        violations = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                threats = self.detect_threats(content)

                for threat in threats:
                    violations.append(
                        {
                            "file": file_path,
                            "line": content[: threat["start"]].count("\n") + 1,
                            "category": threat["category"],
                            "severity": threat["severity"],
                            "match": threat["match"],
                            "pattern": (
                                threat["pattern"][:50] + "..."
                                if len(threat["pattern"]) > 50
                                else threat["pattern"]
                            ),
                        }
                    )

        except Exception as e:
            self.logger.warning(f"Could not scan file {file_path}: {e}")

        return violations

    def _get_staged_files(self) -> List[str]:
        """Get list of staged git files"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            return [f.strip() for f in result.stdout.split("\n") if f.strip()]
        except subprocess.CalledProcessError:
            return []

    def _generate_scan_id(self) -> str:
        """Generate unique scan ID"""
        return hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8]

    def _calculate_trust_score(self, scan_result: Dict[str, Any]) -> float:
        """Calculate trust score based on scan results"""
        if scan_result["files_scanned"] == 0:
            return 1.0

        violation_rate = scan_result["threats_detected"] / scan_result["files_scanned"]
        return max(0.0, 1.0 - violation_rate)

    def _generate_trust_proof(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate verifiable proof of security scan"""
        proof_data = {
            "scan_timestamp": scan_result["timestamp"],
            "files_scanned": scan_result["files_scanned"],
            "threats_detected": scan_result["threats_detected"],
        }

        proof_hash = hashlib.sha256(
            json.dumps(proof_data, sort_keys=True).encode()
        ).hexdigest()

        return {
            "proof_hash": proof_hash,
            "verification_data": proof_data,
            "scanner_version": "SecurityManager-BaseManager-v1.0",
        }

    def _get_threat_severity(self, category: str) -> str:
        """Get threat severity based on category"""
        severity_map = {
            "stakeholder_patterns": "HIGH",
            "strategic_patterns": "HIGH",
            "sensitive_data_patterns": "CRITICAL",
        }
        return severity_map.get(category, "MEDIUM")

    def _log_security_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log security event to validation log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": event_data,
        }

        log_file = self.validation_log_dir / f"security_{event_type}.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


# Register SecurityManager with the factory system
try:
    register_manager_type(
        manager_type=ManagerType.SECURITY,
        manager_class=SecurityManager,
        description="Unified security management with validation, monitoring, and threat detection",
    )
except Exception:
    pass
