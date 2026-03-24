# Idan System Monitor

A real-time system monitoring tool for Windows that tracks CPU, memory, disk, and network usage with configurable warning thresholds and comprehensive logging.

## Features

- **Real-time Metrics Display**: Live monitoring of system resources with automatic updates
- **Color-coded Warnings**: Visual indicators (green/yellow/red) for resource usage levels
- **Desktop Notifications**: Alerts when resource usage exceeds configured thresholds
- **JSON Logging**: Detailed performance history saved to log files
- **Configurable Thresholds**: Set custom warning levels for each metric
- **Per-core CPU Tracking**: Individual monitoring of each CPU core
- **Network Rate Tracking**: Upload/download speed calculations
- **Multi-partition Support**: Monitor all disk partitions simultaneously

## Requirements

- Python 3.10 or higher
- Windows operating system
- Python uv package manager

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd idan-sys-mon
```

2. Install dependencies:

```bash
uv sync
```

## Usage

### Basic Usage

Run the monitor with default settings:

```bash
uv run src/main.py
```

### Configuration Options

Customize the monitor using command-line arguments:

```bash
uv run src/main.py --interval 2 --cpu-warn 90 --mem-warn 90 --disk-warn 95 --net-warn 1000000 --log "C:\path\to\log.txt"
```

#### Available Arguments

| Argument      | Default   | Description                              |
| ------------- | --------- | ---------------------------------------- |
| `--interval`  | 2         | CPU sampling interval in seconds         |
| `--cpu-warn`  | 90        | CPU usage warning threshold (%)          |
| `--mem-warn`  | 90        | Memory usage warning threshold (%)       |
| `--disk-warn` | 95        | Disk usage warning threshold (%)         |
| `--net-warn`  | 1000000   | Network warning threshold (bytes/second) |
| `--log`       | `log.txt` | Path to log file                         |

### Example: Custom Configuration

Monitor with stricter thresholds and custom log location:

```bash
uv run src/main.py --interval 1 --cpu-warn 80 --mem-warn 85 --disk-warn 90 --log "C:\monitoring\system_metrics.txt"
```

## Output Format

### Display

The monitor shows four real-time tables:

- **CPU Usage**: Per-core usage and total average
- **Memory Usage**: Used/total memory and percentage
- **Disk Usage**: Percentage utilization per partition
- **Network Usage**: Upload and download speeds

### Log File Format

Metrics are logged in JSON format with timestamps:

```json
{
  "2024-03-24 14:30:45.123456": {
    "CPU Usage": {
      "1": "45.2%",
      "2": "38.9%",
      "Total": "42.0%"
    },
    "Memory Usage": {
      "Used": "8.5 GB",
      "Total": "16.0 GB",
      "Percent": "53.1%"
    },
    "Disk Usage": {
      "C:": "65.4%",
      "D:": "42.1%"
    },
    "Network Usage": {
      "Upload": "0.5 MB/s",
      "Download": "2.3 MB/s"
    }
  }
}
```

## Project Structure

```
idan-sys-mon/
├── src/
│   ├── collector.py      # System metrics collection
│   ├── display.py        # Real-time display rendering
│   ├── logger.py         # JSON logging functionality
│   ├── main.py          # Main application and CLI
│   └── report.py        # Report generation (future)
├── tests/
│   ├── test_collector.py
│   ├── test_logger.py
│   └── test_report.py
├── docs/
│   └── design.md        # Architecture documentation
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Module Documentation

### Collector (`src/collector.py`)

Handles system metrics collection using psutil. Provides classes for CPU, Memory, Disk, and Network data structures.

### Display (`src/display.py`)

Manages real-time visualization using the Rich library. Formats tables and sends desktop notifications based on thresholds.

### Logger (`src/logger.py`)

Records system metrics to JSON log files. Calculates network rates and formats byte values for readability.

### Main (`src/main.py`)

Application entry point. Manages the monitoring loop, configuration, and integration of all components.

## Keyboard Controls

- **Ctrl+C**: Stop monitoring and exit the application

## Troubleshooting

### Logger Disabled Message

If you see "Log file path invalid, logger disabled", ensure:

- The directory path exists
- You have write permissions to the directory
- The path is correctly formatted

### Missing Desktop Notifications

Desktop notifications require the Plyer library, which is listed in `pyproject.toml`. Ensure dependencies are installed:

```bash
uv sync
```

### High CPU/Memory Usage

Decrease the `--interval` value (minimum 1 second) or run with default settings (2 seconds).

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please ensure all tests pass and add documentation for new features.

## Development

Run tests:

```bash
uv run pytest tests/
```

## Future Enhancements

- Report generation from log files
- Historical data visualization
- Web-based dashboard
- Linux/macOS support
- Custom alert commands
