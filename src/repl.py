"""
REPL (Read-Eval-Print Loop) interface for the Advanced Calculator.

This module provides a command-line interface using Python's cmd module.
It implements the Facade pattern to simplify interaction with the calculator.
"""
import cmd
import shlex
from datetime import datetime
from typing import List, Dict, Any

from src.plugin_mananger import PluginManager
from .calculator import Calculator

def parse_date(date_str: str) -> datetime:
    """Parse date string in various formats"""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")

def parse_history_args(args: List[str]) -> Dict[str, Any]:
    """Parse history command arguments"""
    result = {
        'start_date': None,
        'end_date': None,
        'operation': None,
        'limit': None
    }

    i = 0
    while i < len(args):
        if args[i] == '--from' and i + 1 < len(args):
            result['start_date'] = parse_date(args[i + 1])
            i += 2
        elif args[i] == '--to' and i + 1 < len(args):
            result['end_date'] = parse_date(args[i + 1])
            i += 2
        elif args[i] == '--operation' and i + 1 < len(args):
            result['operation'] = args[i + 1]
            i += 2
        elif args[i] == '--limit' and i + 1 < len(args):
            result['limit'] = int(args[i + 1])
            i += 2
        else:
            i += 1

    return result

class CalculatorREPL(cmd.Cmd):  # pylint: disable=too-many-public-methods
    """REPL interface for the calculator"""
    intro = (
        "Welcome to Advanced Calculator! Type help or ? to list commands.\n"
        "Available commands: add, subtract, multiply, divide, history, "
        "history_stats, clear_history, save_history, load_history, quit"
    )
    prompt = "calc> "

    def __init__(self):
        """Initialize REPL with calculator and plugin system"""
        super().__init__()
        self.calculator = Calculator()
        self.plugin_manager = PluginManager()
        self.plugin_manager.discover_plugins()

    def do_add(self, arg: str) -> None:
        """Add two numbers: add <number1> <number2>"""
        try:
            num1, num2 = map(float, shlex.split(arg))
            result = self.calculator.execute_command('add', num1, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Usage: add <number1> <number2>")

    def do_subtract(self, arg: str) -> None:
        """Subtract second number from first: subtract <number1> <number2>"""
        try:
            num1, num2 = map(float, shlex.split(arg))
            result = self.calculator.execute_command('subtract', num1, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Usage: subtract <number1> <number2>")

    def do_multiply(self, arg: str) -> None:
        """Multiply two numbers: multiply <number1> <number2>"""
        try:
            num1, num2 = map(float, shlex.split(arg))
            result = self.calculator.execute_command('multiply', num1, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Usage: multiply <number1> <number2>")

    def do_divide(self, arg: str) -> None:
        """Divide first number by second: divide <number1> <number2>"""
        try:
            num1, num2 = map(float, shlex.split(arg))
            result = self.calculator.execute_command('divide', num1, num2)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {str(e)}")
            print("Usage: divide <number1> <number2>")

    def do_history(self, arg: str) -> None:
        """View calculation history with optional filters.
        
        Usage: history [--from <date>] [--to <date>] [--operation <op>] [--limit <n>]
        """
        try:
            args = parse_history_args(shlex.split(arg))
            history = self.calculator.get_history(**args)

            if history.empty:
                print("No calculations found")
                return

            for _, row in history.iterrows():
                print(
                    f"{row['timestamp']} - {row['operation']}: "
                    f"{row['operands']} = {row['result']}"
                )

        except ValueError as e:
            print(f"Error: {str(e)}")
            print(
                "Usage: history [--from <date>] [--to <date>] "
                "[--operation <op>] [--limit <n>]"
            )

    def do_history_stats(self, _: str) -> None:
        """View statistics about calculation history"""
        stats = self.calculator.get_history_stats()
        if stats['total_calculations'] == 0:
            print("No calculations found")
            return

        print(f"Total calculations: {stats['total_calculations']}")
        print(f"Most used operation: {stats['most_used_operation']}")
        print(f"Average result: {stats['average_result']:.2f}")
        print("\nOperations breakdown:")
        for op, count in stats['operations_count'].items():
            print(f"  {op}: {count}")
        print(f"\nLast calculation: {stats['last_calculation']}")
        print(f"Unique operations used: {stats['unique_operations']}")

    def do_clear_history(self, _: str) -> None:
        """Clear all calculation history"""
        self.calculator.clear_history()
        print("History cleared")

    def do_save_history(self, arg: str) -> None:
        """Save history to file: save_history <filename>"""
        try:
            filename = shlex.split(arg)[0]
            self.calculator.save_history(filename)
            print(f"History saved to {filename}.csv")
        except (IndexError, FileNotFoundError) as e:
            print(f"Error: {str(e)}")
            print("Usage: save_history <filename>")

    def do_load_history(self, arg: str) -> None:
        """Load history from file: load_history <filename>"""
        try:
            filename = shlex.split(arg)[0]
            self.calculator.load_history(filename)
            print(f"History loaded from {filename}.csv")
        except (IndexError, FileNotFoundError) as e:
            print(f"Error: {str(e)}")
            print("Usage: load_history <filename>")

    def do_quit(self, _: str) -> bool:
        """Exit the calculator"""
        print("Goodbye!")
        return True

    def do_exit(self, _: str) -> bool:
        """Exit the calculator (alias for quit)"""
        return self.do_quit(_)

    def do_end(self, _: str) -> bool:
        """Exit the calculator (alias for quit)"""
        return self.do_quit(_)

    def do_EOF(self, _: str) -> bool:  # pylint: disable=invalid-name
        """Handle EOF (Ctrl+D/Ctrl+Z)"""
        print("\nGoodbye!")
        return True

    def default(self, line: str) -> None:
        """Handle unknown commands and plugin commands"""
        command = line.split()[0] if line else ""
        plugin = self.plugin_manager.get_plugin(command)
        if not plugin:
            print(f"Unknown command: {command}")
            print("Type 'help' for a list of commands")
            return

        try:
            args = shlex.split(line)[1:]
            if len(args) < 1:
                print(f"Error: {command} requires at least one argument")
                return

            cmd_instance = plugin()
            if len(args) == 1:
                result = cmd_instance.execute(float(args[0]), 0)
            else:
                result = cmd_instance.execute(float(args[0]), float(args[1]))
            print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {str(e)}")
            print(f"Usage: {command} <number> [<number2>]")

    def get_names(self) -> List[str]:
        """Get list of command names"""
        return [n[3:] for n in dir(self) if n.startswith('do_')]

    def help_add(self) -> None:
        """Help message for add command"""
        print("Add two numbers: add <number1> <number2>")

    def help_subtract(self) -> None:
        """Help message for subtract command"""
        print("Subtract second number from first: subtract <number1> <number2>")

    def help_multiply(self) -> None:
        """Help message for multiply command"""
        print("Multiply two numbers: multiply <number1> <number2>")

    def help_divide(self) -> None:
        """Help message for divide command"""
        print("Divide first number by second: divide <number1> <number2>")

    def help_history(self) -> None:
        """Help message for history command"""
        print("View calculation history with optional filters:")
        print("  --from <date>     - Show entries from this date")
        print("  --to <date>       - Show entries until this date")
        print("  --operation <op>  - Filter by operation type")
        print("  --limit <n>       - Show only last n entries")

    def help_history_stats(self) -> None:
        """Help message for history_stats command"""
        print("View statistics about calculation history")

    def help_clear_history(self) -> None:
        """Help message for clear_history command"""
        print("Clear all calculation history")

    def help_save_history(self) -> None:
        """Help message for save_history command"""
        print("Save history to file: save_history <filename>")

    def help_load_history(self) -> None:
        """Help message for load_history command"""
        print("Load history from file: load_history <filename>")

    def help_quit(self) -> None:
        """Help message for quit command"""
        print("Exit the calculator")

    def help_exit(self) -> None:
        """Help message for exit command"""
        print("Exit the calculator (alias for quit)")

    def help_end(self) -> None:
        """Help message for end command"""
        print("Exit the calculator (alias for quit)")

    def help_EOF(self) -> None:  # pylint: disable=invalid-name
        """Help message for EOF command"""
        print("Exit the calculator (Ctrl+D/Ctrl+Z)")

    def emptyline(self) -> bool:
        """Handle empty line input"""
        return False

    def postcmd(self, stop: bool, line: str) -> bool:
        """Post-command hook"""
        return stop

    def do_help(self, arg: str) -> None:
        """List available commands with "help" or detailed help with "help cmd"."""
        if arg:
            # Show help about specific command
            super().do_help(arg)
        else:
            # Show list of all commands
            print("Available commands:")
            print("  Basic operations:")
            print("    add <num1> <num2>      - Add two numbers")
            print("    subtract <num1> <num2>  - Subtract second number from first")
            print("    multiply <num1> <num2>  - Multiply two numbers")
            print("    divide <num1> <num2>    - Divide first number by second")
            print("\n  History management:")
            print("    history                - View calculation history")
            print("    history_stats          - View history statistics")
            print("    clear_history          - Clear history")
            print("    save_history <file>    - Save history to file")
            print("    load_history <file>    - Load history from file")
            print("\n  Other commands:")
            print("    help [command]         - Show this help or help for a command")
            print("    quit (or exit)         - Exit the calculator")
