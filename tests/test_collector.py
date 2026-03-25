"""Tests for the collector module.

Unit tests for system metrics collection functionality.
"""
from src.collector import Collector, DiskPartition

def test_collector_initialization():
    """Test that the Collector initializes with the correct interval."""
    interval = 2.0
    collector = Collector(interval)
    assert collector.interval == interval

def test_collector_collect_metrics():
    """Test that the Collector can collect CPU, memory, and disk metrics."""
    collector = Collector(1.0)
    
    cpu_usage = collector.get_cpu_usage()
    assert cpu_usage is not None
    assert isinstance(cpu_usage.cpus, list)
    
    memory_usage = collector.get_memory_usage()
    assert memory_usage is not None
    assert memory_usage.total > 0
    
    disk_usage = collector.get_disk_usage()
    assert disk_usage is not None
    assert isinstance(disk_usage, list)
    assert len(disk_usage) > 0 and isinstance(disk_usage[0], DiskPartition)