"""
Performance Monitor for Real-Time Metrics

Prometheus-compatible metrics collection and enterprise monitoring.
"""

import time
import asyncio
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
import threading


@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    alert_type: str
    threshold: float
    current_value: float
    severity: str  # INFO, WARNING, CRITICAL
    message: str
    timestamp: float
    component: str


@dataclass
class MetricPoint:
    """Single metric data point"""
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: float
    unit: str = "ms"


class PerformanceMonitor:
    """
    Enterprise-grade performance monitoring for ClaudeDirector

    Features:
    - Real-time metrics collection
    - Prometheus-compatible format
    - Configurable alerting thresholds
    - Performance trend analysis
    - Health check endpoints
    - <5 minute issue detection
    """

    def __init__(self, retention_hours: int = 24, alert_cooldown_seconds: int = 300):
        self.retention_hours = retention_hours
        self.alert_cooldown_seconds = alert_cooldown_seconds
        self.logger = logging.getLogger(__name__)

        # Metrics storage (time-series data)
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))

        # Performance thresholds
        self.thresholds = {
            "response_time_ms": {"warning": 400, "critical": 800},
            "memory_usage_mb": {"warning": 45, "critical": 50},
            "cache_hit_rate": {"warning": 0.7, "critical": 0.5},
            "error_rate": {"warning": 0.01, "critical": 0.05},
            "queue_depth": {"warning": 100, "critical": 500},
            "gc_time_ms": {"warning": 100, "critical": 500},
        }

        # Alert tracking
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_history: List[PerformanceAlert] = []
        self.last_alert_times: Dict[str, float] = {}

        # Performance counters
        self.counters = {
            "requests_total": 0,
            "requests_slow": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors_total": 0,
            "gc_collections": 0,
        }

        # System health status
        self.health_status = "healthy"  # healthy, degraded, critical
        self.health_checks = {}

        # Background monitoring
        self._monitoring_tasks = []
        self._start_monitoring()

    def _start_monitoring(self):
        """Start background monitoring tasks"""
        try:
            loop = asyncio.get_running_loop()

            # Metrics cleanup task
            self._monitoring_tasks.append(
                loop.create_task(self._cleanup_old_metrics())
            )

            # Health monitoring task
            self._monitoring_tasks.append(
                loop.create_task(self._monitor_system_health())
            )

        except RuntimeError:
            # No event loop running
            pass

    async def _cleanup_old_metrics(self):
        """Remove metrics older than retention period"""
        while True:
            try:
                await asyncio.sleep(300)  # Cleanup every 5 minutes

                cutoff_time = time.time() - (self.retention_hours * 3600)

                for metric_name, points in self.metrics.items():
                    # Remove old points
                    while points and points[0].timestamp < cutoff_time:
                        points.popleft()

                # Cleanup old alerts
                self.alert_history = [
                    alert for alert in self.alert_history
                    if alert.timestamp > cutoff_time
                ]

                self.logger.debug("Cleaned up old metrics and alerts")

            except Exception as e:
                self.logger.error(f"Metrics cleanup error: {e}")

    async def _monitor_system_health(self):
        """Monitor overall system health"""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds

                # Check all health indicators
                health_issues = []

                # Check response time health
                avg_response_time = self.get_average_metric("response_time_ms", window_seconds=300)
                if avg_response_time and avg_response_time > self.thresholds["response_time_ms"]["critical"]:
                    health_issues.append("response_time_critical")

                # Check memory health
                current_memory = self.get_latest_metric("memory_usage_mb")
                if current_memory and current_memory > self.thresholds["memory_usage_mb"]["critical"]:
                    health_issues.append("memory_critical")

                # Check error rate health
                error_rate = self.calculate_error_rate(window_seconds=300)
                if error_rate > self.thresholds["error_rate"]["critical"]:
                    health_issues.append("error_rate_critical")

                # Update health status
                if health_issues:
                    if any("critical" in issue for issue in health_issues):
                        self.health_status = "critical"
                    else:
                        self.health_status = "degraded"
                else:
                    self.health_status = "healthy"

                self.health_checks["last_check"] = time.time()
                self.health_checks["issues"] = health_issues

            except Exception as e:
                self.logger.error(f"System health monitoring error: {e}")

    def record_metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
        unit: str = "ms"
    ):
        """Record a metric data point"""
        if labels is None:
            labels = {}

        metric_point = MetricPoint(
            name=name,
            value=value,
            labels=labels,
            timestamp=time.time(),
            unit=unit
        )

        self.metrics[name].append(metric_point)

        # Check for alerts
        self._check_metric_thresholds(name, value)

    def increment_counter(self, counter_name: str, amount: int = 1):
        """Increment a performance counter"""
        self.counters[counter_name] = self.counters.get(counter_name, 0) + amount

    def _check_metric_thresholds(self, metric_name: str, value: float):
        """Check if metric exceeds thresholds and trigger alerts"""
        if metric_name not in self.thresholds:
            return

        thresholds = self.thresholds[metric_name]
        alert_key = f"{metric_name}_threshold"

        # Check for cooldown period
        if alert_key in self.last_alert_times:
            time_since_last = time.time() - self.last_alert_times[alert_key]
            if time_since_last < self.alert_cooldown_seconds:
                return

        # Determine alert severity
        severity = None
        threshold_value = None

        if value > thresholds.get("critical", float('inf')):
            severity = "CRITICAL"
            threshold_value = thresholds["critical"]
        elif value > thresholds.get("warning", float('inf')):
            severity = "WARNING"
            threshold_value = thresholds["warning"]

        # Create alert if threshold exceeded
        if severity:
            alert = PerformanceAlert(
                alert_type="threshold_exceeded",
                threshold=threshold_value,
                current_value=value,
                severity=severity,
                message=f"{metric_name} exceeded {severity.lower()} threshold: {value:.2f} > {threshold_value}",
                timestamp=time.time(),
                component=metric_name
            )

            self._trigger_alert(alert_key, alert)

    def _trigger_alert(self, alert_key: str, alert: PerformanceAlert):
        """Trigger a performance alert"""
        self.active_alerts[alert_key] = alert
        self.alert_history.append(alert)
        self.last_alert_times[alert_key] = alert.timestamp

        # Log alert
        log_method = self.logger.critical if alert.severity == "CRITICAL" else self.logger.warning
        log_method(f"Performance Alert [{alert.severity}]: {alert.message}")

        # Keep alert history manageable
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

    def clear_alert(self, alert_key: str):
        """Clear an active alert"""
        if alert_key in self.active_alerts:
            del self.active_alerts[alert_key]
            self.logger.info(f"Cleared alert: {alert_key}")

    def get_latest_metric(self, metric_name: str) -> Optional[float]:
        """Get the latest value for a metric"""
        if metric_name in self.metrics and self.metrics[metric_name]:
            return self.metrics[metric_name][-1].value
        return None

    def get_average_metric(self, metric_name: str, window_seconds: int = 300) -> Optional[float]:
        """Get average metric value over time window"""
        if metric_name not in self.metrics:
            return None

        cutoff_time = time.time() - window_seconds
        recent_points = [
            point.value for point in self.metrics[metric_name]
            if point.timestamp >= cutoff_time
        ]

        if recent_points:
            return sum(recent_points) / len(recent_points)
        return None

    def get_metric_percentile(self, metric_name: str, percentile: float, window_seconds: int = 300) -> Optional[float]:
        """Get percentile value for a metric over time window"""
        if metric_name not in self.metrics:
            return None

        cutoff_time = time.time() - window_seconds
        recent_values = [
            point.value for point in self.metrics[metric_name]
            if point.timestamp >= cutoff_time
        ]

        if recent_values:
            sorted_values = sorted(recent_values)
            index = int(len(sorted_values) * percentile)
            return sorted_values[min(index, len(sorted_values) - 1)]
        return None

    def calculate_error_rate(self, window_seconds: int = 300) -> float:
        """Calculate error rate over time window"""
        total_requests = self.counters.get("requests_total", 0)
        total_errors = self.counters.get("errors_total", 0)

        if total_requests == 0:
            return 0.0

        return total_errors / total_requests

    def get_prometheus_metrics(self) -> str:
        """Generate Prometheus-compatible metrics format"""
        lines = []

        # Add help and type information
        lines.append("# HELP claudedirector_response_time_ms Response time in milliseconds")
        lines.append("# TYPE claudedirector_response_time_ms histogram")

        # Add counter metrics
        for counter_name, value in self.counters.items():
            lines.append(f"# HELP claudedirector_{counter_name} Total count")
            lines.append(f"# TYPE claudedirector_{counter_name} counter")
            lines.append(f"claudedirector_{counter_name} {value}")

        # Add gauge metrics
        for metric_name in ["response_time_ms", "memory_usage_mb", "cache_hit_rate"]:
            latest_value = self.get_latest_metric(metric_name)
            if latest_value is not None:
                lines.append(f"# HELP claudedirector_{metric_name} Current {metric_name}")
                lines.append(f"# TYPE claudedirector_{metric_name} gauge")
                lines.append(f"claudedirector_{metric_name} {latest_value}")

        # Add percentile metrics
        for metric_name in ["response_time_ms"]:
            for percentile in [0.5, 0.95, 0.99]:
                value = self.get_metric_percentile(metric_name, percentile)
                if value is not None:
                    p_label = str(int(percentile * 100))
                    lines.append(f"claudedirector_{metric_name}_p{p_label} {value}")

        return "\n".join(lines) + "\n"

    def get_health_check(self) -> Dict[str, Any]:
        """Get health check status for load balancers"""
        return {
            "status": self.health_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": self.health_checks,
            "active_alerts": len(self.active_alerts),
            "uptime_seconds": time.time() - getattr(self, '_start_time', time.time())
        }

    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data"""
        # Calculate key metrics
        avg_response_time = self.get_average_metric("response_time_ms", 300)
        p95_response_time = self.get_metric_percentile("response_time_ms", 0.95, 300)
        p99_response_time = self.get_metric_percentile("response_time_ms", 0.99, 300)

        current_memory = self.get_latest_metric("memory_usage_mb")
        cache_hit_rate = self.get_latest_metric("cache_hit_rate")
        error_rate = self.calculate_error_rate(300)

        # Recent alerts
        recent_alerts = [
            asdict(alert) for alert in self.alert_history[-10:]
        ]

        return {
            "health": {
                "status": self.health_status,
                "last_check": self.health_checks.get("last_check"),
                "issues": self.health_checks.get("issues", []),
            },
            "performance": {
                "response_time": {
                    "average_ms": avg_response_time,
                    "p95_ms": p95_response_time,
                    "p99_ms": p99_response_time,
                    "target_ms": 500,
                },
                "memory": {
                    "current_mb": current_memory,
                    "target_mb": 50,
                },
                "cache": {
                    "hit_rate": cache_hit_rate,
                    "target_rate": 0.8,
                },
                "errors": {
                    "rate": error_rate,
                    "target_rate": 0.01,
                },
            },
            "counters": self.counters,
            "alerts": {
                "active": len(self.active_alerts),
                "recent": recent_alerts,
            },
            "thresholds": self.thresholds,
        }

    def set_threshold(self, metric_name: str, warning: float, critical: float):
        """Set custom threshold for a metric"""
        self.thresholds[metric_name] = {
            "warning": warning,
            "critical": critical
        }
        self.logger.info(f"Updated thresholds for {metric_name}: warning={warning}, critical={critical}")

    def register_health_check(self, check_name: str, check_func: Callable[[], bool]):
        """Register a custom health check function"""
        self.health_checks[check_name] = {
            "function": check_func,
            "last_result": None,
            "last_check": None,
        }

    async def cleanup(self):
        """Cleanup monitoring resources"""
        # Cancel background tasks
        for task in self._monitoring_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self.logger.info("Performance monitor cleaned up")


# Global performance monitor instance
_performance_monitor = None

def get_performance_monitor(retention_hours: int = 24) -> PerformanceMonitor:
    """Get global performance monitor instance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor(retention_hours=retention_hours)
        _performance_monitor._start_time = time.time()
    return _performance_monitor


# Convenient monitoring decorators
def monitor_performance(metric_name: str = None):
    """Decorator to automatically monitor function performance"""
    def decorator(func):
        actual_metric_name = metric_name or f"{func.__module__}.{func.__name__}"

        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                monitor = get_performance_monitor()
                start_time = time.time()

                try:
                    result = await func(*args, **kwargs)
                    monitor.increment_counter("requests_total")
                    return result
                except Exception as e:
                    monitor.increment_counter("errors_total")
                    raise
                finally:
                    response_time = (time.time() - start_time) * 1000
                    monitor.record_metric(actual_metric_name, response_time)

                    if response_time > 500:
                        monitor.increment_counter("requests_slow")

            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                monitor = get_performance_monitor()
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    monitor.increment_counter("requests_total")
                    return result
                except Exception as e:
                    monitor.increment_counter("errors_total")
                    raise
                finally:
                    response_time = (time.time() - start_time) * 1000
                    monitor.record_metric(actual_metric_name, response_time)

                    if response_time > 500:
                        monitor.increment_counter("requests_slow")

            return sync_wrapper

    return decorator
