# Performance Monitoring API

**Real-time performance tracking and optimization metrics.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 📊 **Performance Monitoring API**

### **Performance Monitor**
```python
# .claudedirector/lib/claudedirector/monitoring/performance_monitor.py
class PerformanceMonitor:
    """Monitor system performance and resource usage"""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.thresholds = {
            'response_time': 2.0,  # seconds
            'mcp_timeout': 5.0,    # seconds
            'memory_usage': 0.8,   # 80% of available
        }

    def record_response_time(self, operation: str, duration: float):
        """Record response time for operation"""
        self.metrics[f"{operation}_response_time"].append({
            'duration': duration,
            'timestamp': time.time()
        })

        # Alert if threshold exceeded
        if duration > self.thresholds['response_time']:
            self._trigger_alert(f"Slow response: {operation} took {duration:.2f}s")

    def record_mcp_call(self, server: str, capability: str, duration: float, success: bool):
        """Record MCP server call metrics"""
        self.metrics[f"mcp_{server}_{capability}"].append({
            'duration': duration,
            'success': success,
            'timestamp': time.time()
        })

    def get_performance_summary(self) -> dict:
        """Get performance metrics summary"""
        summary = {}

        for metric_name, measurements in self.metrics.items():
            if not measurements:
                continue

            recent_measurements = [
                m for m in measurements
                if time.time() - m['timestamp'] < 3600  # Last hour
            ]

            if recent_measurements:
                durations = [m['duration'] for m in recent_measurements]
                summary[metric_name] = {
                    'count': len(recent_measurements),
                    'avg_duration': sum(durations) / len(durations),
                    'max_duration': max(durations),
                    'min_duration': min(durations)
                }

        return summary

    def check_health(self) -> Dict[str, bool]:
        """Check overall system health"""
        health_checks = {}

        # Check response times
        recent_responses = self._get_recent_metric('response_time')
        if recent_responses:
            avg_response = sum(recent_responses) / len(recent_responses)
            health_checks['response_time_healthy'] = avg_response < self.thresholds['response_time']

        # Check MCP server availability
        for server in ['sequential', 'context7', 'magic']:
            recent_calls = self._get_recent_metric(f'mcp_{server}')
            if recent_calls:
                success_rate = sum(1 for call in recent_calls if call.get('success', False)) / len(recent_calls)
                health_checks[f'{server}_healthy'] = success_rate > 0.8

        return health_checks
```
