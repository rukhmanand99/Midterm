"""
Main entry point for the Advanced Calculator application.

This module initializes logging, loads environment variables,
and starts the calculator REPL interface.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

from src.repl import CalculatorREPL
from src.plugin_manager import PluginManager

def setup_logging() -> None:
    """Configure logging with file and console handlers"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'calculator.log')

    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5
    )
    console_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[file_handler, console_handler]
    )

def main() -> None:
    """Main entry point for the calculator application"""
    try:
        # Setup logging
        setup_logging()
        logging.info("Starting Advanced Calculator")

        # Load environment variables
        load_dotenv()
        logging.info("Environment variables loaded")

        # Initialize plugin system
        plugin_manager = PluginManager()
        plugin_manager.discover_plugins()
        logging.info("Plugin system initialized")

        # Start REPL interface
        repl = CalculatorREPL()
        repl.cmdloop()

    except FileNotFoundError as e:
        logging.error("File not found: %s", str(e))
        sys.exit(1)
    except PermissionError as e:
        logging.error("Permission denied: %s", str(e))
        sys.exit(1)
    except ImportError as e:
        logging.error("Failed to import module: %s", str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Calculator terminated by user")
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        logging.critical("Unexpected error: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
