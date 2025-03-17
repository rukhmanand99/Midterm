# Advanced Python Calculator

A sophisticated calculator application demonstrating professional software development practices, including design patterns, logging, and plugin architecture.

## Features

- Interactive REPL (Read-Eval-Print Loop) interface
- Plugin system for extensible functionality
- Pandas-based calculation history management
- Comprehensive logging system
- Environment variable configuration
- Implementation of key design patterns

## Design Patterns

### Command Pattern
The calculator uses the Command pattern for operation handling (`src/calculator.py`). Each operation (add, subtract, etc.) is encapsulated as a command object, allowing for:
- Operation history tracking
- Undo/redo functionality
- Easy addition of new operations

### Factory Method Pattern
The plugin system (`src/plugin_manager.py`) uses the Factory pattern to:
- Dynamically load calculator extensions
- Create plugin instances without coupling to concrete classes
- Maintain extensibility without core code modification

### Facade Pattern
The REPL interface (`src/repl.py`) implements the Facade pattern to:
- Simplify complex operations for end users
- Provide a unified interface to subsystems
- Abstract implementation details

## Environment Variables

The application uses the following environment variables:
- `CALC_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `CALC_HISTORY_FILE`: Path to history storage file
- `CALC_PLUGIN_DIR`: Directory for plugin discovery

## Logging

Comprehensive logging is implemented with:
- Multiple severity levels (INFO, WARNING, ERROR)
- Rotating file handlers
- Configurable output formats
- Operation tracking and error reporting

## Exception Handling Examples

### LBYL (Look Before You Leap)
```python
# Example from src/calculator.py
def divide(self, a, b):
    if b == 0:  # Looking before leaping
        raise ValueError("Division by zero is not allowed")
    return a / b
```

### EAFP (Easier to Ask for Forgiveness than Permission)
```python
# Example from src/plugin_manager.py
def load_plugin(self, plugin_name):
    try:
        return importlib.import_module(f"plugins.{plugin_name}")
    except ImportError:
        raise PluginNotFoundError(f"Plugin {plugin_name} not found")
```

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure environment variables
4. Run the calculator:
   ```bash
   python main.py
   ```

## Testing

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Video Demo
video link : https://drive.google.com/file/d/1cD5qVlrIefliBugi91NcQ86sqeEscW5I/view?usp=sharing