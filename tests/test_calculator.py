"""
Test module for the calculator functionality.

This module tests core calculator operations, history management,
and error handling.
"""
import pytest
from src.calculator import (
    Calculator, Command, AddCommand, SubtractCommand,
    MultiplyCommand, DivideCommand
)

def test_calculator_singleton():
    """Test calculator singleton pattern"""
    calc1 = Calculator()
    calc2 = Calculator()
    assert calc1 is calc2
    # Access to protected members is necessary for testing singleton implementation
    assert calc1._commands is calc2._commands  # pylint: disable=protected-access

def test_add_command():
    """Test addition command"""
    cmd = AddCommand()
    assert cmd.execute(2, 3) == 5
    assert cmd.get_description() == "Addition"

def test_subtract_command():
    """Test subtraction command"""
    cmd = SubtractCommand()
    assert cmd.execute(5, 3) == 2
    assert cmd.get_description() == "Subtraction"

def test_multiply_command():
    """Test multiplication command"""
    cmd = MultiplyCommand()
    assert cmd.execute(4, 3) == 12
    assert cmd.get_description() == "Multiplication"

def test_divide_command():
    """Test division command"""
    cmd = DivideCommand()
    assert cmd.execute(6, 2) == 3
    assert cmd.get_description() == "Division"

def test_divide_by_zero():
    """Test division by zero error"""
    cmd = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        cmd.execute(1, 0)

def test_calculator_execute():
    """Test calculator command execution"""
    calc = Calculator()
    calc.clear_history()  # Start with clean history
    assert calc.execute_command('add', 2, 3) == 5
    assert calc.execute_command('subtract', 5, 3) == 2
    assert calc.execute_command('multiply', 4, 3) == 12
    assert calc.execute_command('divide', 6, 2) == 3

def test_calculator_invalid_command():
    """Test handling of invalid commands"""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.execute_command('invalid', 1, 2)

def test_calculator_history():
    """Test calculation history management"""
    calc = Calculator()
    calc.clear_history()  # Start with clean history
    calc.execute_command('add', 2, 3)
    history = calc.get_history()
    assert len(history) == 1
    assert history.iloc[0]['operation'] == 'add'
    # Using literal_eval for safe evaluation of string tuples
    from ast import literal_eval  # pylint: disable=import-outside-toplevel
    assert literal_eval(history.iloc[0]['operands']) == (2.0, 3.0)
    assert history.iloc[0]['result'] == 5

def test_calculator_clear_history():
    """Test clearing calculation history"""
    calc = Calculator()
    calc.execute_command('add', 2, 3)
    calc.clear_history()
    history = calc.get_history()
    assert len(history) == 0

def test_calculator_save_load_history(tmp_path):
    """Test saving and loading history"""
    calc = Calculator()
    calc.clear_history()  # Start with clean history
    calc.execute_command('add', 2, 3)
    filename = tmp_path / "test_history.csv"
    calc.save_history(str(filename))
    calc.clear_history()
    assert len(calc.get_history()) == 0
    calc.load_history(str(filename))
    history = calc.get_history()
    assert len(history) == 1
    assert history.iloc[0]['operation'] == 'add'

def test_calculator_load_nonexistent_history():
    """Test loading non-existent history file"""
    calc = Calculator()
    with pytest.raises(FileNotFoundError):
        calc.load_history("nonexistent.csv")

def test_register_command():
    """Test registering new commands"""
    calc = Calculator()
    # Reset calculator to initial state
    calc._commands = {  # pylint: disable=protected-access
        'add': AddCommand(),
        'subtract': SubtractCommand(),
        'multiply': MultiplyCommand(),
        'divide': DivideCommand()
    }

    class TestCommand(Command):
        """Test command implementation"""
        def execute(self, a: float, b: float) -> float:
            """Execute test command"""
            return a + b

        def get_description(self) -> str:
            """Get command description"""
            return "Test command"
    calc.register_command('test', TestCommand())
    commands = calc.get_available_commands()
    assert len(commands) == 5
    assert set(commands) == {'add', 'subtract', 'multiply', 'divide', 'test'}

def test_get_available_commands():
    """Test getting available commands"""
    calc = Calculator()
    # Reset calculator to initial state
    calc._commands = {  # pylint: disable=protected-access
        'add': AddCommand(),
        'subtract': SubtractCommand(),
        'multiply': MultiplyCommand(),
        'divide': DivideCommand()
    }
    commands = calc.get_available_commands()
    assert set(commands) == {'add', 'subtract', 'multiply', 'divide'}
