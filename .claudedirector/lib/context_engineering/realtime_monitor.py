"""
Real-Time Team Interaction Monitoring for Context Engineering Phase 3.2B

This module provides real-time monitoring capabilities for team interactions,
enabling proactive detection of coordination issues and bottlenecks.

Architecture:
- Event-driven processing for scalable real-time analysis
- Integration with TeamDynamicsEngine for contextual insights
- Configurable alert thresholds and notification channels
- Performance optimized for <5 minute detection latency

Author: Martin | Platform Architecture
Phase: Context Engineering 3.2B - Advanced Intelligence
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Callable, Union
from pathlib import Path
import threading
from queue import Queue, Empty


# Configure logging
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of team interaction events that can be monitored."""

    COMMUNICATION_DELAY = "communication_delay"
    DEPENDENCY_BLOCK = "dependency_block"
    WORKFLOW_BOTTLENECK = "workflow_bottleneck"
    STAKEHOLDER_CONFLICT = "stakeholder_conflict"
    PROCESS_DEVIATION = "process_deviation"
    RESOURCE_CONTENTION = "resource_contention"


class AlertSeverity(Enum):
    """Alert severity levels for team coordination issues."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TeamEvent:
    """Represents a team interaction event for real-time monitoring."""

    event_id: str
    event_type: EventType
    timestamp: datetime
    team_id: str
    participants: List[str]
    context: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "team_id": self.team_id,
            "participants": self.participants,
            "context": self.context,
            "metadata": self.metadata,
        }


@dataclass
class Alert:
    """Represents an alert generated from real-time team monitoring."""

    alert_id: str
    severity: AlertSeverity
    event_type: EventType
    team_id: str
    message: str
    timestamp: datetime
    source_events: List[str]
    recommended_actions: List[str]
    expires_at: Optional[datetime] = None
    acknowledged: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary representation."""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "event_type": self.event_type.value,
            "team_id": self.team_id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "source_events": self.source_events,
            "recommended_actions": self.recommended_actions,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "acknowledged": self.acknowledged,
        }


class EventProcessor:
    """Processes team events and identifies patterns requiring alerts."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.event_history: List[TeamEvent] = []
        self.pattern_thresholds = config.get("pattern_thresholds", {})
        self.analysis_window = timedelta(
            minutes=config.get("analysis_window_minutes", 30)
        )

    def process_event(self, event: TeamEvent) -> List[Alert]:
        """
        Process a team event and generate alerts if patterns are detected.

        Args:
            event: Team interaction event to process

        Returns:
            List of alerts generated from event analysis
        """
        # Store event in history
        self.event_history.append(event)
        self._cleanup_old_events()

        # Analyze patterns and generate alerts
        alerts = []

        # Check for communication delays
        if event.event_type == EventType.COMMUNICATION_DELAY:
            alert = self._check_communication_pattern(event)
            if alert:
                alerts.append(alert)

        # Check for dependency blocks
        elif event.event_type == EventType.DEPENDENCY_BLOCK:
            alert = self._check_dependency_pattern(event)
            if alert:
                alerts.append(alert)

        # Check for workflow bottlenecks
        elif event.event_type == EventType.WORKFLOW_BOTTLENECK:
            alert = self._check_workflow_pattern(event)
            if alert:
                alerts.append(alert)

        # Check for stakeholder conflicts
        elif event.event_type == EventType.STAKEHOLDER_CONFLICT:
            alert = self._check_stakeholder_pattern(event)
            if alert:
                alerts.append(alert)

        return alerts

    def _cleanup_old_events(self) -> None:
        """Remove events older than the analysis window."""
        cutoff = datetime.now() - self.analysis_window
        self.event_history = [
            event for event in self.event_history if event.timestamp > cutoff
        ]

    def _check_communication_pattern(self, event: TeamEvent) -> Optional[Alert]:
        """Check for communication delay patterns requiring alerts."""
        team_events = [
            e
            for e in self.event_history
            if e.team_id == event.team_id
            and e.event_type == EventType.COMMUNICATION_DELAY
        ]

        # Alert if multiple communication delays in short period
        if len(team_events) >= self.pattern_thresholds.get(
            "communication_threshold", 3
        ):
            return Alert(
                alert_id=f"comm_delay_{event.team_id}_{int(time.time())}",
                severity=AlertSeverity.HIGH,
                event_type=EventType.COMMUNICATION_DELAY,
                team_id=event.team_id,
                message=f"Multiple communication delays detected for team {event.team_id}",
                timestamp=datetime.now(),
                source_events=[e.event_id for e in team_events[-3:]],
                recommended_actions=[
                    "Review team communication channels",
                    "Check for stakeholder availability issues",
                    "Consider process adjustments",
                ],
            )
        return None

    def _check_dependency_pattern(self, event: TeamEvent) -> Optional[Alert]:
        """Check for dependency block patterns requiring alerts."""
        team_events = [
            e
            for e in self.event_history
            if e.team_id == event.team_id and e.event_type == EventType.DEPENDENCY_BLOCK
        ]

        # Alert if critical dependency blocks
        if len(team_events) >= self.pattern_thresholds.get("dependency_threshold", 2):
            return Alert(
                alert_id=f"dep_block_{event.team_id}_{int(time.time())}",
                severity=AlertSeverity.CRITICAL,
                event_type=EventType.DEPENDENCY_BLOCK,
                team_id=event.team_id,
                message=f"Critical dependency blocks detected for team {event.team_id}",
                timestamp=datetime.now(),
                source_events=[e.event_id for e in team_events[-2:]],
                recommended_actions=[
                    "Escalate dependency resolution",
                    "Identify alternative solutions",
                    "Engage dependency owners immediately",
                ],
            )
        return None

    def _check_workflow_pattern(self, event: TeamEvent) -> Optional[Alert]:
        """Check for workflow bottleneck patterns requiring alerts."""
        team_events = [
            e
            for e in self.event_history
            if e.team_id == event.team_id
            and e.event_type == EventType.WORKFLOW_BOTTLENECK
        ]

        # Alert if persistent workflow issues
        if len(team_events) >= self.pattern_thresholds.get("workflow_threshold", 2):
            return Alert(
                alert_id=f"workflow_block_{event.team_id}_{int(time.time())}",
                severity=AlertSeverity.HIGH,
                event_type=EventType.WORKFLOW_BOTTLENECK,
                team_id=event.team_id,
                message=f"Persistent workflow bottlenecks detected for team {event.team_id}",
                timestamp=datetime.now(),
                source_events=[e.event_id for e in team_events[-2:]],
                recommended_actions=[
                    "Review workflow process efficiency",
                    "Identify bottleneck root causes",
                    "Consider process automation opportunities",
                ],
            )
        return None

    def _check_stakeholder_pattern(self, event: TeamEvent) -> Optional[Alert]:
        """Check for stakeholder conflict patterns requiring alerts."""
        team_events = [
            e
            for e in self.event_history
            if e.team_id == event.team_id
            and e.event_type == EventType.STAKEHOLDER_CONFLICT
        ]

        # Alert on any stakeholder conflict (immediate attention needed)
        if team_events:
            return Alert(
                alert_id=f"stakeholder_conflict_{event.team_id}_{int(time.time())}",
                severity=AlertSeverity.CRITICAL,
                event_type=EventType.STAKEHOLDER_CONFLICT,
                team_id=event.team_id,
                message=f"Stakeholder conflict detected for team {event.team_id}",
                timestamp=datetime.now(),
                source_events=[event.event_id],
                recommended_actions=[
                    "Schedule immediate stakeholder alignment meeting",
                    "Engage leadership for conflict resolution",
                    "Document disagreement points for resolution",
                ],
            )
        return None


class AlertEngine:
    """Manages alert generation, routing, and notification delivery."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_handlers: List[Callable[[Alert], None]] = []
        self.notification_channels = config.get("notification_channels", [])

    def register_alert_handler(self, handler: Callable[[Alert], None]) -> None:
        """Register a handler for alert processing."""
        self.alert_handlers.append(handler)

    def process_alert(self, alert: Alert) -> None:
        """
        Process and route an alert through configured channels.

        Args:
            alert: Alert to process and notify
        """
        # Store active alert
        self.active_alerts[alert.alert_id] = alert

        # Route to all registered handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")

        # Send notifications
        self._send_notifications(alert)

        logger.info(f"Alert processed: {alert.alert_id} - {alert.message}")

    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an active alert.

        Args:
            alert_id: ID of alert to acknowledge

        Returns:
            True if alert was acknowledged, False if not found
        """
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            logger.info(f"Alert acknowledged: {alert_id}")
            return True
        return False

    def get_active_alerts(self, team_id: Optional[str] = None) -> List[Alert]:
        """
        Get currently active alerts, optionally filtered by team.

        Args:
            team_id: Optional team ID to filter alerts

        Returns:
            List of active alerts
        """
        alerts = list(self.active_alerts.values())
        if team_id:
            alerts = [alert for alert in alerts if alert.team_id == team_id]
        return alerts

    def _send_notifications(self, alert: Alert) -> None:
        """Send alert notifications through configured channels."""
        for channel in self.notification_channels:
            try:
                if channel == "console":
                    self._notify_console(alert)
                elif channel == "file":
                    self._notify_file(alert)
                # Additional notification channels can be added here
            except Exception as e:
                logger.error(f"Notification failed for channel {channel}: {e}")

    def _notify_console(self, alert: Alert) -> None:
        """Send alert notification to console."""
        print(f"🚨 TEAM ALERT [{alert.severity.value.upper()}]: {alert.message}")
        print(f"   Team: {alert.team_id}")
        print(f"   Time: {alert.timestamp}")
        print(f"   Actions: {', '.join(alert.recommended_actions)}")

    def _notify_file(self, alert: Alert) -> None:
        """Send alert notification to file."""
        alert_file = Path(self.config.get("alert_file", "alerts.log"))
        with open(alert_file, "a") as f:
            f.write(f"{json.dumps(alert.to_dict())}\n")


class TeamDataCollector:
    """Collects team interaction data from various sources."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_sources = config.get("data_sources", [])
        self.collection_interval = config.get("collection_interval", 60)  # seconds
        self.running = False
        self._collection_thread: Optional[threading.Thread] = None

    def start_collection(self) -> None:
        """Start background data collection."""
        if not self.running:
            self.running = True
            self._collection_thread = threading.Thread(
                target=self._collection_loop, daemon=True
            )
            self._collection_thread.start()
            logger.info("Team data collection started")

    def stop_collection(self) -> None:
        """Stop background data collection."""
        self.running = False
        if self._collection_thread:
            self._collection_thread.join(timeout=5)
        logger.info("Team data collection stopped")

    def _collection_loop(self) -> None:
        """Main collection loop running in background thread."""
        while self.running:
            try:
                # Simulate data collection from various sources
                # In production, this would integrate with actual data sources
                self._collect_from_sources()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Data collection error: {e}")
                time.sleep(self.collection_interval)

    def _collect_from_sources(self) -> List[TeamEvent]:
        """Collect team events from configured data sources."""
        events = []

        # Data source integration points for production deployment:
        # - Chat systems integration (Slack, Teams APIs)
        # - Project management integration (Jira, GitHub APIs)
        # - Communication platform integration
        # - Workflow system integration

        logger.debug(f"Collected {len(events)} events from data sources")
        return events


class RealTimeBottleneckDetector:
    """Detects team coordination bottlenecks in real-time."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.detection_algorithms = config.get(
            "detection_algorithms",
            [
                "communication_lag",
                "dependency_chain",
                "resource_contention",
                "process_deviation",
            ],
        )
        self.detection_thresholds = config.get("detection_thresholds", {})

    def analyze_bottleneck(self, events: List[TeamEvent]) -> List[Alert]:
        """
        Analyze events for bottleneck patterns and generate alerts.

        Args:
            events: List of team events to analyze

        Returns:
            List of alerts for detected bottlenecks
        """
        alerts = []

        for algorithm in self.detection_algorithms:
            if algorithm == "communication_lag":
                alerts.extend(self._detect_communication_lag(events))
            elif algorithm == "dependency_chain":
                alerts.extend(self._detect_dependency_chains(events))
            elif algorithm == "resource_contention":
                alerts.extend(self._detect_resource_contention(events))
            elif algorithm == "process_deviation":
                alerts.extend(self._detect_process_deviation(events))

        return alerts

    def _detect_communication_lag(self, events: List[TeamEvent]) -> List[Alert]:
        """Detect communication lag patterns."""
        comm_events = [
            e for e in events if e.event_type == EventType.COMMUNICATION_DELAY
        ]

        # Group by team and check for patterns
        team_groups = {}
        for event in comm_events:
            if event.team_id not in team_groups:
                team_groups[event.team_id] = []
            team_groups[event.team_id].append(event)

        alerts = []
        threshold = self.detection_thresholds.get("communication_lag_count", 3)

        for team_id, team_events in team_groups.items():
            if len(team_events) >= threshold:
                alerts.append(
                    Alert(
                        alert_id=f"comm_lag_{team_id}_{int(time.time())}",
                        severity=AlertSeverity.HIGH,
                        event_type=EventType.COMMUNICATION_DELAY,
                        team_id=team_id,
                        message=f"Communication lag pattern detected for team {team_id}",
                        timestamp=datetime.now(),
                        source_events=[e.event_id for e in team_events],
                        recommended_actions=[
                            "Review communication processes",
                            "Check stakeholder availability",
                            "Consider communication tool optimization",
                        ],
                    )
                )

        return alerts

    def _detect_dependency_chains(self, events: List[TeamEvent]) -> List[Alert]:
        """Detect dependency chain bottlenecks."""
        dep_events = [e for e in events if e.event_type == EventType.DEPENDENCY_BLOCK]

        alerts = []
        threshold = self.detection_thresholds.get("dependency_chain_length", 2)

        # Check for dependency chains affecting multiple teams
        if len(dep_events) >= threshold:
            affected_teams = list(set(e.team_id for e in dep_events))
            if len(affected_teams) > 1:
                alerts.append(
                    Alert(
                        alert_id=f"dep_chain_{int(time.time())}",
                        severity=AlertSeverity.CRITICAL,
                        event_type=EventType.DEPENDENCY_BLOCK,
                        team_id="multi_team",
                        message=f"Dependency chain affecting {len(affected_teams)} teams",
                        timestamp=datetime.now(),
                        source_events=[e.event_id for e in dep_events],
                        recommended_actions=[
                            "Escalate dependency resolution immediately",
                            "Identify critical path alternatives",
                            "Engage cross-team coordination",
                        ],
                    )
                )

        return alerts

    def _detect_resource_contention(self, events: List[TeamEvent]) -> List[Alert]:
        """Detect resource contention patterns."""
        resource_events = [
            e for e in events if e.event_type == EventType.RESOURCE_CONTENTION
        ]

        # Resource contention analysis implementation
        # Analyzes resource usage patterns and identifies conflicts
        alerts = []
        if len(resource_events) >= 2:  # Multiple resource conflicts
            alerts.append(
                Alert(
                    alert_id=f"resource_contention_{int(time.time())}",
                    severity=AlertSeverity.HIGH,
                    event_type=EventType.RESOURCE_CONTENTION,
                    team_id="multi_team",
                    message="Resource contention detected across teams",
                    timestamp=datetime.now(),
                    source_events=[e.event_id for e in resource_events],
                    recommended_actions=[
                        "Review resource allocation priorities",
                        "Coordinate resource scheduling",
                        "Consider resource capacity expansion",
                    ],
                )
            )
        return alerts

    def _detect_process_deviation(self, events: List[TeamEvent]) -> List[Alert]:
        """Detect process deviation patterns."""
        process_events = [
            e for e in events if e.event_type == EventType.PROCESS_DEVIATION
        ]

        # Process deviation analysis implementation
        # Analyzes adherence to established processes and identifies deviations
        alerts = []
        if len(process_events) >= 1:  # Any process deviation warrants attention
            alerts.append(
                Alert(
                    alert_id=f"process_deviation_{int(time.time())}",
                    severity=AlertSeverity.MEDIUM,
                    event_type=EventType.PROCESS_DEVIATION,
                    team_id=process_events[0].team_id,
                    message="Process deviation detected",
                    timestamp=datetime.now(),
                    source_events=[e.event_id for e in process_events[-1:]],
                    recommended_actions=[
                        "Review process adherence",
                        "Provide process training if needed",
                        "Evaluate if process updates are required",
                    ],
                )
            )
        return alerts


class RealTimeMonitor:
    """
    Main real-time monitoring system for team interactions.

    Coordinates event processing, alert generation, and notification delivery
    to provide proactive team coordination issue detection.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize real-time monitoring system.

        Args:
            config: Configuration dictionary with monitoring parameters
        """
        self.config = config
        self.event_processor = EventProcessor(config)
        self.bottleneck_detector = RealTimeBottleneckDetector(config)
        self.alert_engine = AlertEngine(config)
        self.data_collector = TeamDataCollector(config)

        self.event_queue: Queue = Queue()
        self.running = False
        self.monitoring_thread: Optional[threading.Thread] = None

        # Performance tracking
        self.start_time = datetime.now()
        self.events_processed = 0
        self.alerts_generated = 0

        logger.info("RealTimeMonitor initialized")

    def start_monitoring(self, teams: List[str]) -> None:
        """
        Begin real-time monitoring for specified teams.

        Args:
            teams: List of team IDs to monitor
        """
        if self.running:
            logger.warning("Monitoring already running")
            return

        self.running = True
        self.monitored_teams = set(teams)

        # Start components
        self.data_collector.start_collection()

        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()

        logger.info(f"Real-time monitoring started for teams: {teams}")

    def stop_monitoring(self) -> None:
        """Stop real-time monitoring."""
        if not self.running:
            return

        self.running = False
        self.data_collector.stop_collection()

        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

        logger.info("Real-time monitoring stopped")

    def process_team_event(self, event: TeamEvent) -> List[Alert]:
        """
        Process a team interaction event and generate alerts if needed.

        Args:
            event: Team event to process

        Returns:
            List of alerts generated from event processing
        """
        # Add event to processing queue
        self.event_queue.put(event)

        # Process immediately and return results
        alerts = []

        # Event pattern analysis
        pattern_alerts = self.event_processor.process_event(event)
        alerts.extend(pattern_alerts)

        # Bottleneck detection
        recent_events = self.event_processor.event_history[-10:]  # Last 10 events
        bottleneck_alerts = self.bottleneck_detector.analyze_bottleneck(recent_events)
        alerts.extend(bottleneck_alerts)

        # Process all generated alerts
        for alert in alerts:
            self.alert_engine.process_alert(alert)

        # Update performance metrics
        self.events_processed += 1
        self.alerts_generated += len(alerts)

        return alerts

    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        Get current monitoring status and performance metrics.

        Returns:
            Dictionary with monitoring status information
        """
        uptime = datetime.now() - self.start_time

        return {
            "running": self.running,
            "monitored_teams": list(getattr(self, "monitored_teams", [])),
            "uptime_seconds": uptime.total_seconds(),
            "events_processed": self.events_processed,
            "alerts_generated": self.alerts_generated,
            "active_alerts": len(self.alert_engine.active_alerts),
            "event_queue_size": self.event_queue.qsize(),
            "performance_metrics": {
                "events_per_minute": self.events_processed
                / max(uptime.total_seconds() / 60, 1),
                "alert_rate": self.alerts_generated / max(self.events_processed, 1),
            },
        }

    def get_team_alerts(self, team_id: str) -> List[Alert]:
        """
        Get active alerts for a specific team.

        Args:
            team_id: Team ID to get alerts for

        Returns:
            List of active alerts for the team
        """
        return self.alert_engine.get_active_alerts(team_id)

    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert.

        Args:
            alert_id: ID of alert to acknowledge

        Returns:
            True if alert was acknowledged successfully
        """
        return self.alert_engine.acknowledge_alert(alert_id)

    def _monitoring_loop(self) -> None:
        """Main monitoring loop running in background thread."""
        logger.info("Monitoring loop started")

        while self.running:
            try:
                # Process queued events
                self._process_event_queue()

                # Brief sleep to prevent excessive CPU usage
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(1)

        logger.info("Monitoring loop stopped")

    def _process_event_queue(self) -> None:
        """Process events from the queue."""
        try:
            while True:
                event = self.event_queue.get_nowait()

                # Additional processing for queued events if needed
                logger.debug(f"Processing queued event: {event.event_id}")

                self.event_queue.task_done()

        except Empty:
            # No more events in queue
            pass
