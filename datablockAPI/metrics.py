"""
datablockAPI - Metrics Collection
Basic metrics collection for monitoring API usage.
"""

from typing import Dict, Any
from collections import defaultdict
import time
from .logging_config import logger


class MetricsCollector:
    """Simple metrics collector for API operations."""

    def __init__(self):
        self.metrics = defaultdict(int)
        self.timers = {}
        self.start_time = time.time()

    def increment(self, metric: str, value: int = 1):
        """Increment a counter metric."""
        self.metrics[metric] += value

    def start_timer(self, operation: str):
        """Start timing an operation."""
        self.timers[operation] = time.time()

    def end_timer(self, operation: str):
        """End timing an operation and record duration."""
        if operation in self.timers:
            duration = time.time() - self.timers[operation]
            self.metrics[f"{operation}_duration"] = duration
            self.metrics[f"{operation}_count"] += 1
            del self.timers[operation]

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        metrics = dict(self.metrics)
        metrics["uptime_seconds"] = time.time() - self.start_time
        return metrics

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.timers.clear()
        self.start_time = time.time()


# Global metrics collector
metrics = MetricsCollector()


def record_api_call(endpoint: str, success: bool = True):
    """Record an API call for metrics."""
    metrics.increment("api_calls_total")
    if success:
        metrics.increment("api_calls_success")
    else:
        metrics.increment("api_calls_failed")

    metrics.increment(f"api_calls_{endpoint}")


def record_database_operation(operation: str, success: bool = True):
    """Record a database operation for metrics."""
    metrics.increment("db_operations_total")
    if success:
        metrics.increment("db_operations_success")
    else:
        metrics.increment("db_operations_failed")

    metrics.increment(f"db_operations_{operation}")
<parameter name="filePath">c:\Users\jun\dataground\datablockAPI\metrics.py