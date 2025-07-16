# Rotating Log System

A comprehensive Python logging solution with automatic time-based log rotation, designed for production applications and development environments.

## 🚀 Features

- **Automatic Log Rotation**: Time-based rotation (daily, hourly, weekly, etc.)
- **Configurable Backup Count**: Control how many rotated files to keep
- **Dual Output**: Console and file logging with independent configuration
- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **UTF-8 Encoding**: Full Unicode support for international applications
- **Automatic Directory Creation**: Creates log directories as needed
- **Thread-Safe**: Safe for use in multi-threaded applications
- **Zero Dependencies**: Uses only Python standard library

## 📋 Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 🛠️ Installation

Simply download the `logging_with_rotation.py` file and import it into your project:

```python
from logging_with_rotation import create_rotating_logger
```

## 🎯 Quick Start

### Basic Usage

```python
from logging_with_rotation import create_rotating_logger

# Create a basic logger with daily rotation
logger = create_rotating_logger()
logger.info("Application started")
logger.warning("This is a warning message")
logger.error("Something went wrong")
```

### Advanced Configuration

```python
import logging
from logging_with_rotation import create_rotating_logger

# Custom logger configuration
logger = create_rotating_logger(
    name="my_app",
    log_file="application.log",
    log_dir="logs/app",
    level=logging.DEBUG,
    when="H",           # Rotate every hour
    interval=2,         # Every 2 hours
    backup_count=24,    # Keep 24 files (48 hours)
    console_output=True
)
```

## 📖 Command Line Usage

The script can be run directly from the command line:

```bash
# Show comprehensive help
python logging_with_rotation.py

# Run demonstration
python logging_with_rotation.py --demo

# Show usage examples
python logging_with_rotation.py --show-examples

# Test rotation functionality
python logging_with_rotation.py --test-rotation
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | "rotating_logger" | Name of the logger |
| `log_file` | str | "application.log" | Name of the log file |
| `log_dir` | str | "logs" | Directory for log files |
| `level` | int | `logging.INFO` | Logging level |
| `when` | str | "midnight" | Rotation timing |
| `interval` | int | 1 | Interval for rotation |
| `backup_count` | int | 7 | Number of backup files to keep |
| `console_output` | bool | True | Whether to log to console |
| `custom_format` | str | None | Custom format for log messages |

### Rotation Timing Options

| Value | Description | Example |
|-------|-------------|---------|
| `'S'` | Seconds | Every N seconds |
| `'M'` | Minutes | Every N minutes |
| `'H'` | Hours | Every N hours |
| `'D'` | Days | Every N days |
| `'midnight'` | Daily at midnight | Every day at 00:00 |
| `'W0'` to `'W6'` | Weekly | W0=Monday, W1=Tuesday, etc. |

## 📁 File Structure

When using the default configuration, your log directory will look like this:

```
logs/
├── application.log                    # Current log file
├── application.log.2025-07-15_23-59-59  # Yesterday's log
├── application.log.2025-07-14_23-59-59  # Day before
└── ...                               # Older rotated logs
```

## 🏗️ Use Cases & Examples

### 1. Web Application Logging

```python
# Main application logger
app_logger = create_rotating_logger(
    name="webapp",
    log_file="webapp.log",
    when="midnight",
    backup_count=30  # Keep 30 days
)

# Access log with hourly rotation
access_logger = create_rotating_logger(
    name="access",
    log_file="access.log",
    when="H",
    backup_count=24  # Keep 24 hours
)
```

### 2. Database Operations

```python
# High-frequency database operations
db_logger = create_rotating_logger(
    name="database",
    log_file="database.log",
    level=logging.DEBUG,
    when="H",
    interval=6,      # Every 6 hours
    backup_count=28  # Keep 1 week
)
```

### 3. Error Tracking

```python
# Separate error logger with longer retention
error_logger = create_rotating_logger(
    name="errors",
    log_file="errors.log",
    level=logging.ERROR,
    when="midnight",
    backup_count=90,      # Keep 3 months
    console_output=True   # Also show in console
)
```

### 4. Development vs Production

```python
import os

env = os.getenv('ENVIRONMENT', 'development')

if env == 'production':
    logger = create_rotating_logger(
        level=logging.WARNING,
        console_output=False,
        backup_count=30
    )
else:
    logger = create_rotating_logger(
        level=logging.DEBUG,
        console_output=True,
        backup_count=7
    )
```

## 🔧 API Reference

### `create_rotating_logger()`

Creates a logger with TimeRotatedFileHandler.

**Parameters:**
- `name` (str): Name of the logger
- `log_file` (str): Name of the log file
- `log_dir` (str): Directory for log files
- `level` (int): Logging level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL)
- `when` (str): Rotation timing ('S', 'M', 'H', 'D', 'midnight', 'W0'-'W6')
- `interval` (int): Interval for rotation
- `backup_count` (int): Number of backup files to keep
- `console_output` (bool): Whether to also log to console
- `custom_format` (str): Custom format for log messages

**Returns:**
- `logging.Logger`: Configured logger instance

### `get_existing_logger()`

Gets an already configured logger.

**Parameters:**
- `name` (str): Name of the logger

**Returns:**
- `logging.Logger`: Logger instance

## 🎛️ Log Levels

| Level | Numeric Value | Usage |
|-------|---------------|-------|
| DEBUG | 10 | Detailed information for debugging |
| INFO | 20 | General information messages |
| WARNING | 30 | Warning messages |
| ERROR | 40 | Error messages |
| CRITICAL | 50 | Critical error messages |

## 🔒 Thread Safety

This logging system is thread-safe and can be used in multi-threaded applications without additional synchronization.

## 📝 Log Format

Default format includes:
- Timestamp (YYYY-MM-DD HH:MM:SS)
- Logger name
- Log level
- Function name and line number
- Log message

Example:
```
2025-07-16 14:30:45 - webapp - INFO - main:25 - Application started successfully
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the script has write permissions to the log directory
2. **Disk Space**: Monitor disk usage when using high backup counts
3. **File Locks**: On Windows, ensure no other processes are accessing log files

### Debug Tips

1. Enable DEBUG level logging to see detailed information
2. Use console output during development
3. Check file permissions and disk space
4. Verify log directory creation

## 📄 License

This project is in the public domain. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Suggestions and improvements are welcome! The script is designed to be self-contained and dependency-free.

## 📞 Support

For questions or issues:
1. Run `python logging_with_rotation.py --help` for comprehensive documentation
2. Check the examples with `python logging_with_rotation.py --show-examples`
3. Test functionality with `python logging_with_rotation.py --demo`

---

**Made with ❤️ for Python developers who need reliable logging solutions.**
