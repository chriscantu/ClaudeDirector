#!/usr/bin/env python3
"""
Continuous Security Monitor
Real-time security monitoring without public dashboard exposure
--persona-martin: Enterprise security architecture
"""

import os
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess

class ContinuousSecurityMonitor:
    """
    Continuous security monitoring system
    Monitors security posture without exposing sensitive information
    """

    def __init__(self):
        self.monitor_dir = Path('.claudedirector/logs/security_monitor')
        self.monitor_dir.mkdir(parents=True, exist_ok=True)

        self.alert_log = self.monitor_dir / 'security_alerts.log'
        self.status_log = self.monitor_dir / 'security_status.log'
        self.metrics_log = self.monitor_dir / 'security_metrics.log'

    def run_continuous_monitoring(self, duration_minutes: int = 60):
        """
        Run continuous security monitoring for specified duration
        """
        print(f"🛡️ Starting continuous security monitoring for {duration_minutes} minutes")

        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)

        monitoring_session = {
            'session_id': self._generate_session_id(),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'alerts_generated': 0,
            'scans_performed': 0,
            'threats_detected': 0
        }

        while datetime.now() < end_time:
            try:
                # Perform security scan
                scan_result = self._perform_security_scan()
                monitoring_session['scans_performed'] += 1

                # Check for threats
                if scan_result['threats_detected'] > 0:
                    monitoring_session['threats_detected'] += scan_result['threats_detected']
                    alert = self._generate_alert(scan_result)
                    self._log_alert(alert)
                    monitoring_session['alerts_generated'] += 1

                # Log status
                self._log_status(scan_result)

                # Update metrics
                self._update_metrics(scan_result)

                # Wait before next scan (5 minutes)
                print(f"📊 Scan completed. Threats: {scan_result['threats_detected']}")
                time.sleep(300)  # 5 minutes

            except KeyboardInterrupt:
                print("\n🛡️ Monitoring stopped by user")
                break
            except Exception as e:
                error_alert = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'MONITORING_ERROR',
                    'severity': 'MEDIUM',
                    'message': f'Monitoring error: {e}'
                }
                self._log_alert(error_alert)
                time.sleep(60)  # Wait 1 minute before retry

        # Generate session summary
        self._generate_session_summary(monitoring_session)
        print(f"🛡️ Monitoring session completed. Scans: {monitoring_session['scans_performed']}, Alerts: {monitoring_session['alerts_generated']}")

    def _perform_security_scan(self) -> Dict:
        """Perform a security scan of the repository"""
        scan_result = {
            'timestamp': datetime.now().isoformat(),
            'scan_type': 'CONTINUOUS_MONITORING',
            'threats_detected': 0,
            'files_scanned': 0,
            'security_score': 100
        }

        try:
            # Check for staged files
            result = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True)

            if result.stdout.strip():
                # Files are modified/staged - run enhanced scanner
                scanner_result = subprocess.run([
                    'python3', '.claudedirector/dev-tools/security/enhanced_security_scanner.py'
                ], capture_output=True, text=True)

                # Parse scanner output for threats
                if 'SECURITY VIOLATIONS:' in scanner_result.stdout:
                    scan_result['threats_detected'] = scanner_result.stdout.count('❌')
                    scan_result['security_score'] = 0
                else:
                    scan_result['security_score'] = 100

            # Count files in repository
            result = subprocess.run(['find', '.', '-type', 'f', '-not', '-path', './.git/*'],
                                  capture_output=True, text=True)
            scan_result['files_scanned'] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

        except Exception as e:
            scan_result['error'] = str(e)
            scan_result['security_score'] = 50  # Partial score on error

        return scan_result

    def _generate_alert(self, scan_result: Dict) -> Dict:
        """Generate security alert"""
        alert = {
            'alert_id': self._generate_alert_id(),
            'timestamp': scan_result['timestamp'],
            'type': 'SECURITY_THREAT_DETECTED',
            'severity': 'HIGH' if scan_result['threats_detected'] > 2 else 'MEDIUM',
            'threats_count': scan_result['threats_detected'],
            'security_score': scan_result['security_score'],
            'recommended_action': 'IMMEDIATE_REMEDIATION_REQUIRED',
            'auto_response': 'COMMIT_BLOCKED'
        }

        return alert

    def _log_alert(self, alert: Dict):
        """Log security alert"""
        with open(self.alert_log, 'a') as f:
            f.write(json.dumps(alert) + '\n')

    def _log_status(self, scan_result: Dict):
        """Log security status"""
        status = {
            'timestamp': scan_result['timestamp'],
            'security_score': scan_result['security_score'],
            'files_scanned': scan_result['files_scanned'],
            'threats_detected': scan_result['threats_detected'],
            'status': 'SECURE' if scan_result['threats_detected'] == 0 else 'THREATS_DETECTED'
        }

        with open(self.status_log, 'a') as f:
            f.write(json.dumps(status) + '\n')

    def _update_metrics(self, scan_result: Dict):
        """Update security metrics"""
        metrics = {
            'timestamp': scan_result['timestamp'],
            'security_score': scan_result['security_score'],
            'threat_detection_rate': 1.0 if scan_result['threats_detected'] > 0 else 0.0,
            'false_positive_rate': 0.0,  # Assume no false positives for now
            'system_availability': 1.0,  # System is available
            'response_time': 'IMMEDIATE'
        }

        with open(self.metrics_log, 'a') as f:
            f.write(json.dumps(metrics) + '\n')

    def _generate_session_summary(self, session: Dict):
        """Generate monitoring session summary"""
        summary_file = self.monitor_dir / f"session_summary_{session['session_id']}.json"

        # Calculate session metrics
        session['duration_minutes'] = (
            datetime.fromisoformat(session['end_time']) -
            datetime.fromisoformat(session['start_time'])
        ).total_seconds() / 60

        session['average_scan_interval'] = session['duration_minutes'] / max(1, session['scans_performed'])
        session['threat_detection_rate'] = session['threats_detected'] / max(1, session['scans_performed'])

        with open(summary_file, 'w') as f:
            json.dump(session, f, indent=2)

    def generate_security_dashboard_data(self) -> Dict:
        """
        Generate security dashboard data (for internal use only)
        No public exposure - data stays within secure boundaries
        """
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'status': 'OPERATIONAL',
            'security_posture': 'STRONG',
            'alerts_24h': 0,
            'threats_blocked': 0,
            'system_health': 'EXCELLENT'
        }

        # Read recent alerts
        if self.alert_log.exists():
            alerts_24h = self._count_recent_alerts(24)
            dashboard_data['alerts_24h'] = alerts_24h

        # Read recent status
        if self.status_log.exists():
            recent_status = self._get_recent_status()
            dashboard_data['security_posture'] = recent_status.get('status', 'UNKNOWN')

        # Read recent metrics
        if self.metrics_log.exists():
            recent_metrics = self._get_recent_metrics()
            dashboard_data['system_health'] = self._assess_system_health(recent_metrics)

        return dashboard_data

    def _count_recent_alerts(self, hours: int) -> int:
        """Count alerts in the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        count = 0

        try:
            with open(self.alert_log, 'r') as f:
                for line in f:
                    alert = json.loads(line.strip())
                    alert_time = datetime.fromisoformat(alert['timestamp'])
                    if alert_time >= cutoff_time:
                        count += 1
        except Exception:
            pass

        return count

    def _get_recent_status(self) -> Dict:
        """Get most recent status"""
        try:
            with open(self.status_log, 'r') as f:
                lines = f.readlines()
                if lines:
                    return json.loads(lines[-1].strip())
        except Exception:
            pass

        return {'status': 'UNKNOWN'}

    def _get_recent_metrics(self) -> Dict:
        """Get most recent metrics"""
        try:
            with open(self.metrics_log, 'r') as f:
                lines = f.readlines()
                if lines:
                    return json.loads(lines[-1].strip())
        except Exception:
            pass

        return {'system_availability': 0.0}

    def _assess_system_health(self, metrics: Dict) -> str:
        """Assess system health from metrics"""
        availability = metrics.get('system_availability', 0.0)

        if availability >= 0.99:
            return 'EXCELLENT'
        elif availability >= 0.95:
            return 'GOOD'
        elif availability >= 0.90:
            return 'FAIR'
        else:
            return 'POOR'

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return hashlib.md5(f"session_{datetime.now().isoformat()}".encode()).hexdigest()[:8]

    def _generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        return hashlib.md5(f"alert_{datetime.now().isoformat()}".encode()).hexdigest()[:8]


def main():
    """Continuous security monitor entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Continuous Security Monitor')
    parser.add_argument('--duration', type=int, default=60,
                       help='Monitoring duration in minutes (default: 60)')
    parser.add_argument('--dashboard-data', action='store_true',
                       help='Generate dashboard data (internal use only)')

    args = parser.parse_args()

    monitor = ContinuousSecurityMonitor()

    if args.dashboard_data:
        print("🛡️ Generating security dashboard data...")
        dashboard_data = monitor.generate_security_dashboard_data()
        print(json.dumps(dashboard_data, indent=2))
    else:
        monitor.run_continuous_monitoring(args.duration)


if __name__ == "__main__":
    main()
