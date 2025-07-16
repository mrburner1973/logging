#!/usr/bin/env python3
"""
Logging System with TimeRotatedFileHandler in a single file.

This script provides a complete logging solution with automatic log rotation
based on time. It can be used as a standalone module or executed directly.

Features:
- Automatic log rotation (daily, hourly, weekly, etc.)
- Configurable backup count
- Console and file output
- Multiple log levels
- UTF-8 encoding
- Automatic directory creation

License: MIT License
Copyright (c) 2025 Marc Peters
"""

import logging
import os
import argparse
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


def print_help():
    """Print comprehensive help documentation for the logging system."""
    help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ROTATING LOG SYSTEM - DOCUMENTATION                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

OVERVIEW:
    This script provides a complete logging solution with automatic log rotation
    based on time. It can be used as a standalone module or executed directly.

FEATURES:
    • Automatic log rotation (daily, hourly, weekly, etc.)
    • Configurable backup count
    • Console and file output
    • Multiple log levels
    • UTF-8 encoding
    • Automatic directory creation

COMMAND LINE USAGE:
    python logging_with_rotation.py [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    --demo             Run demonstration with sample log messages
    --test-rotation    Test log rotation functionality
    --show-examples    Show usage examples

LOG LEVELS:
    DEBUG    (10)  - Detailed information for debugging
    INFO     (20)  - General information messages
    WARNING  (30)  - Warning messages
    ERROR    (40)  - Error messages
    CRITICAL (50)  - Critical error messages

ROTATION TIMING OPTIONS:
    'S'        - Seconds
    'M'        - Minutes  
    'H'        - Hours
    'D'        - Days
    'midnight' - Daily at midnight (default)
    'W0'-'W6'  - Weekly (0=Monday, 1=Tuesday, ..., 6=Sunday)

PROGRAMMATIC USAGE:

    Basic Usage:
    ────────────
    from logging_with_rotation import create_rotating_logger
    
    # Create a basic logger
    logger = create_rotating_logger()
    logger.info("This is a test message")

    Advanced Usage:
    ───────────────
    # Custom configuration
    logger = create_rotating_logger(
        name="my_app",
        log_file="app.log",
        log_dir="my_logs",
        level=logging.DEBUG,
        when="H",           # Rotate hourly
        interval=2,         # Every 2 hours
        backup_count=24,    # Keep 24 files (48 hours)
        console_output=True
    )

    Multiple Loggers:
    ─────────────────
    # Create different loggers for different components
    db_logger = create_rotating_logger("database", "db.log", when="midnight")
    api_logger = create_rotating_logger("api", "api.log", when="H", interval=6)
    
    db_logger.info("Database connection established")
    api_logger.warning("API rate limit approaching")

EXAMPLES:

    1. Daily Rotation at Midnight:
       logger = create_rotating_logger(when="midnight", backup_count=30)

    2. Hourly Rotation:
       logger = create_rotating_logger(when="H", backup_count=24)

    3. Weekly Rotation (Sunday):
       logger = create_rotating_logger(when="W6", backup_count=4)

    4. Debug Logging with Custom Format:
       custom_fmt = "%(asctime)s [%(levelname)s] %(message)s"
       logger = create_rotating_logger(
           level=logging.DEBUG,
           custom_format=custom_fmt
       )

FILE NAMING:
    Rotated files are automatically named with timestamps:
    application.log.2025-07-15_23-59-59
    application.log.2025-07-14_23-59-59

DIRECTORY STRUCTURE:
    logs/
    ├── application.log              (current log file)
    ├── application.log.2025-07-15_23-59-59
    ├── application.log.2025-07-14_23-59-59
    └── ...

API REFERENCE:
    create_rotating_logger(name, log_file, log_dir, level, when, interval, 
                          backup_count, console_output, custom_format)
    get_existing_logger(name)

For more information, run with --show-examples or --demo
"""
    print(help_text)


def show_examples():
    """Show detailed usage examples."""
    examples = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              USAGE EXAMPLES                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

EXAMPLE 1: Basic Web Application Logging
────────────────────────────────────────────
from logging_with_rotation import create_rotating_logger

# Create logger for web application
app_logger = create_rotating_logger(
    name="webapp",
    log_file="webapp.log",
    log_dir="logs/webapp",
    level=logging.INFO,
    when="midnight",
    backup_count=7  # Keep 1 week of logs
)

app_logger.info("Application started")
app_logger.warning("High memory usage detected")
app_logger.error("Database connection failed")

EXAMPLE 2: Database Operations with Hourly Rotation
───────────────────────────────────────────────────
# High-frequency database operations
db_logger = create_rotating_logger(
    name="database",
    log_file="database.log",
    log_dir="logs/db",
    level=logging.DEBUG,
    when="H",           # Rotate every hour
    interval=1,
    backup_count=48     # Keep 48 hours of logs
)

db_logger.debug("Executing query: SELECT * FROM users")
db_logger.info("Query completed in 0.05 seconds")

EXAMPLE 3: API Server with Custom Format
────────────────────────────────────────────
# API requests with custom log format
custom_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

api_logger = create_rotating_logger(
    name="api_server",
    log_file="api.log",
    log_dir="logs/api",
    when="midnight",
    custom_format=custom_format,
    console_output=False  # File only
)

api_logger.info("GET /api/users - 200 OK")
api_logger.warning("POST /api/login - Rate limit exceeded")

EXAMPLE 4: Multi-Component System
─────────────────────────────────────
# Different components with different rotation schedules
auth_logger = create_rotating_logger("auth", "auth.log", when="midnight")
cache_logger = create_rotating_logger("cache", "cache.log", when="H", interval=6)
email_logger = create_rotating_logger("email", "email.log", when="D")

auth_logger.info("User authenticated: user123")
cache_logger.debug("Cache hit for key: user_profile_456")
email_logger.info("Email sent to user@example.com")

EXAMPLE 5: Error Tracking with High Retention
──────────────────────────────────────────────
# Keep error logs for longer periods
error_logger = create_rotating_logger(
    name="errors",
    log_file="errors.log",
    log_dir="logs/errors",
    level=logging.ERROR,  # Only errors and critical
    when="midnight",
    backup_count=90,      # Keep 3 months of error logs
    console_output=True
)

try:
    # Some risky operation
    result = risky_operation()
except Exception as e:
    error_logger.error(f"Operation failed: {str(e)}")

EXAMPLE 6: Development vs Production Configuration
──────────────────────────────────────────────────
import os

# Different settings based on environment
if os.getenv('ENV') == 'production':
    logger = create_rotating_logger(
        level=logging.WARNING,  # Less verbose in production
        when="midnight",
        backup_count=30,
        console_output=False
    )
else:
    logger = create_rotating_logger(
        level=logging.DEBUG,    # Verbose in development
        when="H",
        backup_count=24,
        console_output=True
    )

EXAMPLE 7: Multiple Log Files for Different Purposes
─────────────────────────────────────────────────────
# Separate loggers for different concerns
access_logger = create_rotating_logger("access", "access.log", level=logging.INFO)
error_logger = create_rotating_logger("errors", "errors.log", level=logging.ERROR)
debug_logger = create_rotating_logger("debug", "debug.log", level=logging.DEBUG)

# Log to appropriate logger based on context
access_logger.info("User logged in")
debug_logger.debug("Processing user preferences")
error_logger.error("Failed to save user data")
"""
    print(examples)


def run_demo():
    """Run a demonstration of the logging system."""
    print("\n" + "="*80)
    print("ROTATING LOGGER DEMONSTRATION")
    print("="*80)
    
    # Create demo logger
    demo_logger = create_rotating_logger(
        name="demo",
        log_file="demo.log",
        log_dir="demo_logs",
        level=logging.DEBUG,
        when="S",  # Rotate every second for demo
        interval=10,  # Every 10 seconds
        backup_count=5
    )
    
    print("\nDemo logger created with the following configuration:")
    print("- Name: demo")
    print("- Log file: demo_logs/demo.log")
    print("- Rotation: Every 10 seconds")
    print("- Backup count: 5 files")
    print("- Level: DEBUG")
    
    print("\nGenerating sample log messages...")
    
    # Generate sample messages
    demo_logger.debug("This is a DEBUG message - detailed information")
    demo_logger.info("This is an INFO message - general information")
    demo_logger.warning("This is a WARNING message - something unexpected")
    demo_logger.error("This is an ERROR message - something went wrong")
    demo_logger.critical("This is a CRITICAL message - serious problem")
    
    print("\nSample messages logged successfully!")
    print("Check the 'demo_logs' directory for log files.")
    print("Run the script again in 10+ seconds to see rotation in action.")


def test_rotation():
    """Test the log rotation functionality."""
    print("\n" + "="*80)
    print("LOG ROTATION TEST")
    print("="*80)
    
    import time
    
    # Create test logger with very short rotation interval
    test_logger = create_rotating_logger(
        name="rotation_test",
        log_file="rotation_test.log", 
        log_dir="test_logs",
        when="S",  # Rotate every second
        interval=3,  # Every 3 seconds
        backup_count=3
    )
    
    print("Creating test logger with 3-second rotation...")
    print("Generating messages over 15 seconds to demonstrate rotation...")
    
    for i in range(15):
        test_logger.info(f"Test message {i+1} - timestamp: {datetime.now()}")
        print(f"Message {i+1} logged")
        time.sleep(1)
    
    print("\nRotation test completed!")
    print("Check the 'test_logs' directory to see rotated files.")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Rotating Log System - A comprehensive logging solution with time-based rotation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python logging_with_rotation.py --help           Show full documentation
  python logging_with_rotation.py --demo           Run demonstration
  python logging_with_rotation.py --show-examples  Show usage examples
  python logging_with_rotation.py --test-rotation  Test rotation functionality

For complete documentation, use --help
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run demonstration with sample log messages')
    parser.add_argument('--show-examples', action='store_true',
                       help='Show detailed usage examples')
    parser.add_argument('--test-rotation', action='store_true',
                       help='Test log rotation functionality')
    
    return parser.parse_args()


def main():
    """Main function for command line execution."""
    args = parse_arguments()
    
    if args.demo:
        run_demo()
    elif args.show_examples:
        show_examples()
    elif args.test_rotation:
        test_rotation()
    else:
        print_help()


def create_rotating_logger(
    name: str = "rotating_logger",
    log_file: str = "application.log",
    log_dir: str = "logs",
    level: int = logging.INFO,
    when: str = "midnight",
    interval: int = 1,
    backup_count: int = 7,
    console_output: bool = True,
    custom_format: str = None
) -> logging.Logger:
    """
    Creates a logger with TimeRotatedFileHandler.
    
    Args:
        name (str): Name of the logger
        log_file (str): Name of the log file
        log_dir (str): Directory for log files
        level (int): Logging level (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50)
        when (str): Rotation timing:
                   'S' - Seconds
                   'M' - Minutes  
                   'H' - Hours
                   'D' - Days
                   'midnight' - Daily at midnight
                   'W0'-'W6' - Weekly (0=Monday, 6=Sunday)
        interval (int): Interval for rotation
        backup_count (int): Number of backup files to keep
        console_output (bool): Whether to also log to console
        custom_format (str): Custom format for log messages
    
    Returns:
        logging.Logger: Configured logger
    """
    
    # Create or get existing logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers on multiple calls
    if logger.handlers:
        logger.handlers.clear()
    
    # Create log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        print(f"Log directory created: {log_dir}")
    
    # Full path to log file
    log_path = os.path.join(log_dir, log_file)
    
    # Define format
    if custom_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    else:
        log_format = custom_format
    
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Create and configure TimeRotatedFileHandler
    file_handler = TimedRotatingFileHandler(
        filename=log_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Set suffix for rotated files (timestamp)
    file_handler.suffix = "%Y-%m-%d_%H-%M-%S"
    
    # Add file handler to logger
    logger.addHandler(file_handler)
    
    # Optional: Console handler for console output
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_existing_logger(name: str) -> logging.Logger:
    """
    Gets an already configured logger.
    
    Args:
        name (str): Name of the logger
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


if __name__ == "__main__":
    main()
