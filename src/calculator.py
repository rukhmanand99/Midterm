"""
Core calculator module implementing basic arithmetic operations.

This module provides the base Command class and concrete command implementations
for basic arithmetic operations. It also manages calculation history using pandas.
"""
import warnings
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd # type: ignore
# Suppress FutureWarning temporarily
warnings.simplefilter(action='ignore', category=FutureWarning)

class Command(ABC):
    """Abstract base class for calculator commands"""
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the command with given operands"""

    @abstractmethod
    def get_description(self) -> str:
        """Get command description"""

class AddCommand(Command):
    """Command to add two numbers"""
    def execute(self, a: float, b: float) -> float:
        """Add two numbers"""
        logging.info("Adding %s and %s", a, b)
        return float(a) + float(b)

    def get_description(self) -> str:
        """Get command description"""
        return "Addition"

class SubtractCommand(Command):
    """Command to subtract two numbers"""
    def execute(self, a: float, b: float) -> float:
        """Subtract second number from first"""
        logging.info("Subtracting %s from %s", b, a)
        return float(a) - float(b)

    def get_description(self) -> str:
        """Get command description"""
        return "Subtraction"

class MultiplyCommand(Command):
    """Command to multiply two numbers"""
    def execute(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        logging.info("Multiplying %s and %s", a, b)
        return float(a) * float(b)

    def get_description(self) -> str:
        """Get command description"""
        return "Multiplication"

class DivideCommand(Command):
    """Command to divide two numbers"""
    def execute(self, a: float, b: float) -> float:
        """Divide first number by second"""
        if float(b) == 0:
            logging.error("Division by zero attempted")
            raise ZeroDivisionError("Cannot divide by zero")
        logging.info("Dividing %s by %s", a, b)
        return float(a) / float(b)

    def get_description(self) -> str:
        """Get command description"""
        return "Division"

class Calculator:
    """Calculator class implementing command pattern and history management"""
    _instance = None

    def __new__(cls) -> 'Calculator':
        """Create or return singleton instance"""
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._commands = {
                'add': AddCommand(),
                'subtract': SubtractCommand(),
                'multiply': MultiplyCommand(),
                'divide': DivideCommand()
            }
            instance._history = pd.DataFrame(
                columns=['timestamp', 'operation', 'operands', 'result']
            )
            cls._instance = instance
        return cls._instance

    def execute_command(self, command_name: str, a: float, b: float) -> float:
        """Execute a command by name with given operands"""
        command = self._commands.get(command_name.lower())
        if not command:
            raise ValueError(f"Unknown command: {command_name}")

        result = command.execute(float(a), float(b))
        self._add_to_history(command_name, (float(a), float(b)), result)
        return result

    def _add_to_history(self, operation: str, operands: Tuple[float, float], result: float) -> None:
        """Add calculation to history"""
        new_record = pd.DataFrame({
            'timestamp': [datetime.now()],
            'operation': [operation],
            'operands': [str(operands)],
            'result': [result]
        })
        self._history = pd.concat([self._history, new_record], ignore_index=True)

    def get_history(self, start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   operation: Optional[str] = None,
                   limit: Optional[int] = None) -> pd.DataFrame:
        """Get calculation history with optional filters"""
        history = self._history.copy()

        if start_date:
            history = history[history['timestamp'] >= start_date]
        if end_date:
            history = history[history['timestamp'] <= end_date]
        if operation:
            history = history[history['operation'] == operation.lower()]
        if limit:
            history = history.tail(limit)

        return history

    def get_history_stats(self) -> Dict[str, Any]:
        """Get statistics about calculation history"""
        if self._history.empty:
            return {
                'total_calculations': 0,
                'most_used_operation': None,
                'average_result': 0,
                'operations_count': {},
                'last_calculation': None,
                'unique_operations': 0
            }

        operations_count = self._history['operation'].value_counts().to_dict()
        most_used = max(operations_count.items(), key=lambda x: x[1])[0]

        return {
            'total_calculations': len(self._history),
            'most_used_operation': most_used,
            'average_result': self._history['result'].mean(),
            'operations_count': operations_count,
            'last_calculation': self._history.iloc[-1]['timestamp'],
            'unique_operations': len(operations_count)
        }

    def clear_history(self) -> None:
        """Clear calculation history"""
        self._history = pd.DataFrame(columns=['timestamp', 'operation', 'operands', 'result'])

    def save_history(self, filename: str) -> None:
        """Save history to CSV file"""
        if not filename.endswith('.csv'):
            filename += '.csv'
        self._history.to_csv(filename, index=False)

    def load_history(self, filename: str) -> None:
        """Load history from CSV file"""
        if not filename.endswith('.csv'):
            filename += '.csv'
        self._history = pd.read_csv(filename, parse_dates=['timestamp'])

    def register_command(self, name: str, command: Command) -> None:
        """Register a new command"""
        self._commands[name.lower()] = command

    def get_available_commands(self) -> List[str]:
        """Get list of available command names"""
        return sorted(list(self._commands.keys()))
