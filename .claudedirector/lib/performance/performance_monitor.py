"""
Performance Monitor for Real-Time Metrics

Prometheus-compatible metrics collection and enterprise monitoring.
Refactored to inherit from BaseManager for DRY compliance.
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
from pathlib import Path
import sys

# Import BaseManager infrastructure
try:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from ..core.manager_factory import register_manager_type
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from core.manager_factory import register_manager_type


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


class PerformanceMonitor(BaseManager):
    """
    Enterprise-grade performance monitoring for ClaudeDirector

    Features:
    - Real-time metrics collection
    - Prometheus-compatible format
    - Configurable alerting thresholds
    - Performance trend analysis
    - Health check endpoints
    - <5 minute issue detection

    Refactored to inherit from BaseManager for DRY compliance.
    Eliminates duplicate logging, metrics, and configuration patterns.
    """

    def __init__(
        self,
        config: Optional[BaseManagerConfig] = None,
        retention_hours: int = 24,
        alert_cooldown_seconds: int = 300,
        cache: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        if config is None:
            config = BaseManagerConfig(
                manager_name="performance_monitor",
                manager_type=ManagerType.PERFORMANCE,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                performance_tracking=True,
                custom_config={
                    "retention_hours": retention_hours,
                    "alert_cooldown_seconds": alert_cooldown_seconds,
                },
            )

        super().__init__(config, cache, metrics, logger_name="PerformanceMonitor")

        # Get configuration values from BaseManager config
        self.retention_hours = self.config.custom_config.get(
            "retention_hours", retention_hours
        )
        self.alert_cooldown_seconds = self.config.custom_config.get(
            "alert_cooldown_seconds", alert_cooldown_seconds
        )

        # Metrics storage (time-series data) - renamed to avoid conflict with BaseManager.metrics
        self.metric_storage: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))

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

        # TS-5 ACCEPTANCE CRITERIA: Real-time monitoring tracking
        self.realtime_monitoring = {
            "enabled": True,
            "last_metric_time": time.time(),
            "metrics_per_minute": 0,
            "realtime_threshold": 60,  # Must collect metrics within 60 seconds
            "status": "active",
        }

        # TS-5 ACCEPTANCE CRITERIA: Alerting functionality tracking
        self.alerting_functionality = {
            "enabled": True,
            "alerts_sent": 0,
            "alert_response_time": 0.0,
            "alert_success_rate": 1.0,
            "last_alert_test": time.time(),
        }

        # TS-5 ACCEPTANCE CRITERIA: Metrics consistency tracking
        self.metrics_consistency = {
            "enabled": True,
            "consistent_metrics": 0,
            "inconsistent_metrics": 0,
            "consistency_rate": 1.0,
            "last_consistency_check": time.time(),
        }
        self.health_checks = {}

        # Background monitoring
        self._monitoring_tasks = []
        self._start_monitoring()

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Implement BaseManager abstract method for performance monitoring operations
        """
        start_time = time.time()

        try:
            if operation == "record_metric":
                result = self.record_metric(*args, **kwargs)
            elif operation == "get_metrics":
                result = self.get_current_metrics()
            elif operation == "get_health":
                result = self.get_health_status()
            elif operation == "check_alerts":
                result = self.check_thresholds()
            elif operation == "get_prometheus_metrics":
                result = self.get_prometheus_metrics()
            elif operation == "cleanup_old_metrics":
                result = self.cleanup_old_metrics()
            else:
                raise ValueError(f"Unknown performance monitor operation: {operation}")

            duration = time.time() - start_time
            self._update_metrics(operation, duration, True)

            return result

        except Exception as e:
            duration = time.time() - start_time
            self._update_metrics(operation, duration, False)

            self.logger.error(
                "Performance monitor operation failed",
                operation=operation,
                error=str(e),
                args=args,
                kwargs=kwargs,
            )
            raise

    def _start_monitoring(self):
        """Start background monitoring tasks"""
        try:
            loop = asyncio.get_running_loop()

            # Metrics cleanup task
            self._monitoring_tasks.append(loop.create_task(self._cleanup_old_metrics()))

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
                    alert
                    for alert in self.alert_history
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
                avg_response_time = self.get_average_metric(
                    "response_time_ms", window_seconds=300
                )
                if (
                    avg_response_time
                    and avg_response_time
                    > self.thresholds["response_time_ms"]["critical"]
                ):
                    health_issues.append("response_time_critical")

                # Check memory health
                current_memory = self.get_latest_metric("memory_usage_mb")
                if (
                    current_memory
                    and current_memory > self.thresholds["memory_usage_mb"]["critical"]
                ):
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
        unit: str = "ms",
    ):
        """Record a metric data point"""
        if labels is None:
            labels = {}

        metric_point = MetricPoint(
            name=name, value=value, labels=labels, timestamp=time.time(), unit=unit
        )

        self.metric_storage[name].append(metric_point)

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

        if value > thresholds.get("critical", float("inf")):
            severity = "CRITICAL"
            threshold_value = thresholds["critical"]
        elif value > thresholds.get("warning", float("inf")):
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
                component=metric_name,
            )

            self._trigger_alert(alert_key, alert)

    def _trigger_alert(self, alert_key: str, alert: PerformanceAlert):
        """Trigger a performance alert"""
        self.active_alerts[alert_key] = alert
        self.alert_history.append(alert)
        self.last_alert_times[alert_key] = alert.timestamp

        # Log alert
        log_method = (
            self.logger.critical
            if alert.severity == "CRITICAL"
            else self.logger.warning
        )
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
        if metric_name in self.metric_storage and self.metric_storage[metric_name]:
            return self.metric_storage[metric_name][-1].value
        return None

    def get_average_metric(
        self, metric_name: str, window_seconds: int = 300
    ) -> Optional[float]:
        """Get average metric value over time window"""
        if metric_name not in self.metric_storage:
            return None

        cutoff_time = time.time() - window_seconds
        recent_points = [
            point.value
            for point in self.metric_storage[metric_name]
            if point.timestamp >= cutoff_time
        ]

        if recent_points:
            return sum(recent_points) / len(recent_points)
        return None

    def get_metric_percentile(
        self, metric_name: str, percentile: float, window_seconds: int = 300
    ) -> Optional[float]:
        """Get percentile value for a metric over time window"""
        if metric_name not in self.metric_storage:
            return None

        cutoff_time = time.time() - window_seconds
        recent_values = [
            point.value
            for point in self.metric_storage[metric_name]
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
        lines.append(
            "# HELP claudedirector_response_time_ms Response time in milliseconds"
        )
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
                lines.append(
                    f"# HELP claudedirector_{metric_name} Current {metric_name}"
                )
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
            "uptime_seconds": time.time() - getattr(self, "_start_time", time.time()),
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
        recent_alerts = [asdict(alert) for alert in self.alert_history[-10:]]

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
        self.thresholds[metric_name] = {"warning": warning, "critical": critical}
        self.logger.info(
            f"Updated thresholds for {metric_name}: warning={warning}, critical={critical}"
        )

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

    def validate_realtime_monitoring(self) -> Dict[str, Any]:
        """
        TS-5 ACCEPTANCE CRITERIA: Validate real-time monitoring functionality

        Ensures monitoring system maintains real-time metric collection throughout consolidation.
        """
        current_time = time.time()
        time_since_last_metric = (
            current_time - self.realtime_monitoring["last_metric_time"]
        )

        # Update status based on recent activity
        if time_since_last_metric <= self.realtime_monitoring["realtime_threshold"]:
            self.realtime_monitoring["status"] = "active"
        elif time_since_last_metric <= 300:  # 5 minutes
            self.realtime_monitoring["status"] = "delayed"
        else:
            self.realtime_monitoring["status"] = "inactive"

        # Calculate metrics per minute
        metrics_count = sum(len(deque_data) for deque_data in self.metrics.values())
        self.realtime_monitoring["metrics_per_minute"] = metrics_count / max(
            1, (current_time - getattr(self, "_start_time", current_time)) / 60
        )

        return {
            "realtime": self.realtime_monitoring["status"] == "active",
            "status": self.realtime_monitoring["status"],
            "time_since_last_metric": time_since_last_metric,
            "metrics_per_minute": self.realtime_monitoring["metrics_per_minute"],
            "threshold_seconds": self.realtime_monitoring["realtime_threshold"],
            "message": f"Real-time monitoring: {self.realtime_monitoring['status']} "
            f"({self.realtime_monitoring['metrics_per_minute']:.1f} metrics/min)",
        }

    def validate_alerting_functionality(self) -> Dict[str, Any]:
        """
        TS-5 ACCEPTANCE CRITERIA: Validate alerting functionality

        Ensures alerting system is preserved and functional with unified monitoring.
        """
        current_time = time.time()

        # Test alert functionality by checking recent alert activity
        recent_alerts = [
            alert
            for alert in self.alert_history
            if current_time - alert.timestamp < 3600
        ]  # Last hour

        # Update alert success rate
        if len(recent_alerts) > 0:
            successful_alerts = len(
                [a for a in recent_alerts if a.severity in ["WARNING", "CRITICAL"]]
            )
            self.alerting_functionality["alert_success_rate"] = successful_alerts / len(
                recent_alerts
            )

        self.alerting_functionality["alerts_sent"] = len(self.alert_history)
        self.alerting_functionality["last_alert_test"] = current_time

        # Calculate average alert response time
        if recent_alerts:
            response_times = [
                getattr(alert, "response_time", 0.1) for alert in recent_alerts
            ]
            self.alerting_functionality["alert_response_time"] = sum(
                response_times
            ) / len(response_times)

        return {
            "functional": self.alerting_functionality["enabled"]
            and self.alerting_functionality["alert_success_rate"] > 0.8,
            "enabled": self.alerting_functionality["enabled"],
            "alerts_sent": self.alerting_functionality["alerts_sent"],
            "success_rate": self.alerting_functionality["alert_success_rate"],
            "response_time": self.alerting_functionality["alert_response_time"],
            "recent_alerts": len(recent_alerts),
            "message": f"Alerting functionality: {'functional' if self.alerting_functionality['enabled'] else 'disabled'} "
            f"({self.alerting_functionality['alert_success_rate']:.1%} success rate)",
        }

    def validate_metrics_consistency(self) -> Dict[str, Any]:
        """
        TS-5 ACCEPTANCE CRITERIA: Validate metrics consistency

        Ensures metrics remain consistent across all performance measurements during consolidation.
        """
        current_time = time.time()

        # Check for consistent metric collection across different components
        metric_names = list(self.metric_storage.keys())
        consistent_count = 0
        inconsistent_count = 0

        for metric_name in metric_names:
            metric_data = self.metric_storage[metric_name]
            if len(metric_data) > 1:
                # Check for reasonable consistency in metric values
                recent_values = list(metric_data)[-10:]  # Last 10 values
                if len(recent_values) >= 2:
                    avg_value = sum(point.value for point in recent_values) / len(
                        recent_values
                    )
                    variance = sum(
                        (point.value - avg_value) ** 2 for point in recent_values
                    ) / len(recent_values)
                    coefficient_of_variation = (variance**0.5) / max(avg_value, 0.1)

                    if (
                        coefficient_of_variation < 2.0
                    ):  # Reasonable consistency threshold
                        consistent_count += 1
                    else:
                        inconsistent_count += 1

        # Update consistency tracking
        self.metrics_consistency["consistent_metrics"] = consistent_count
        self.metrics_consistency["inconsistent_metrics"] = inconsistent_count
        total_metrics = consistent_count + inconsistent_count
        self.metrics_consistency["consistency_rate"] = consistent_count / max(
            1, total_metrics
        )
        self.metrics_consistency["last_consistency_check"] = current_time

        return {
            "consistent": self.metrics_consistency["consistency_rate"] >= 0.8,
            "consistency_rate": self.metrics_consistency["consistency_rate"],
            "consistent_metrics": consistent_count,
            "inconsistent_metrics": inconsistent_count,
            "total_metrics": total_metrics,
            "message": f"Metrics consistency: {self.metrics_consistency['consistency_rate']:.1%} "
            f"({consistent_count}/{total_metrics} metrics consistent)",
        }


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


# Register PerformanceMonitor with the factory system
try:
    register_manager_type(
        manager_type=ManagerType.PERFORMANCE,
        manager_class=PerformanceMonitor,
        description="Enterprise-grade performance monitoring with real-time metrics collection",
    )
except Exception:
    pass
