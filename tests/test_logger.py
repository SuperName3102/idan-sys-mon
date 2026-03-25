"""Tests for the logger module.

Unit tests for logging functionality.
"""
from src.logger import Logger
from src import collector


def test_logger_initialization():
    """Test that the Logger initializes with the correct log file path."""
    log_path = "test_log.log"
    logger = Logger(log_path)
    assert logger.log_path == log_path

def test_logger_log_metrics():
    """Test that the Logger can log metrics to the specified file."""
    log_path = "test_log.log"
    logger = Logger(log_path)
    
    # Create dummy metrics data
    cpu_usage = collector.CPU([10.0, 20.0])
    memory_usage = collector.Memory(8 * 1024 * 1024 * 1024, 4 * 1024 * 1024 * 1024, 50.0)  # total, used, percent
    disk_usage = [collector.DiskPartition("C:", 500 * 1024 * 1024 * 1024, 250 * 1024 * 1024 * 1024, 50.0)]  # partition, total, used, percent
    
    metrics = {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
        "network": None,
        "previous_network": None
    }
    
    logger.log(metrics, 2.1)
    
    # Check that the log file was created and contains the expected content
    with open(log_path, 'r') as log_file:
        content = log_file.read()
        assert "CPU Usage" in content
        assert "Memory Usage" in content
        assert "Disk Usage" in content