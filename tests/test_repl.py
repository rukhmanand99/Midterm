"""test repl"""

import unittest
from unittest.mock import patch
from io import StringIO

# Import the CalculatorREPL class here
from src.repl import CalculatorREPL  # Adjust this import based on your file structure

class TestCalculatorREPL(unittest.TestCase):
    """Test cases for the CalculatorREPL class."""

    def setUp(self):
        """Setup for the test cases"""
        self.repl = CalculatorREPL()

    @patch('sys.stdout', new_callable=StringIO)
    def test_add(self, mock_stdout):
        """Test the add command"""
        self.repl.onecmd('add 3 5')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Result: 8.0")
        self.repl.onecmd('add 3 abc')  # Invalid input
        output = mock_stdout.getvalue().strip()
        self.assertIn("Error:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_divide_by_zero(self, mock_stdout):
        """Test division by zero"""
        self.repl.onecmd('divide 3 0')
        output = mock_stdout.getvalue().strip()
        self.assertIn("Error: Cannot divide by zero", output)  # Adjusted error message

    @patch('sys.stdout', new_callable=StringIO)
    def test_history(self, mock_stdout):
        """Test the history command"""
        self.repl.onecmd('history --limit 5')
        output = mock_stdout.getvalue().strip()
        self.assertIn("No calculations found", output)  # Assuming no history yet

    @patch('sys.stdout', new_callable=StringIO)
    def test_history_with_filters(self, mock_stdout):
        """Test history with filters"""
        self.repl.onecmd('history --from 2025-03-01 --operation add --limit 2')
        output = mock_stdout.getvalue().strip()
        self.assertIn("No calculations found", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_history_stats(self, mock_stdout):
        """Test the history stats command"""
        self.repl.onecmd('history_stats')
        output = mock_stdout.getvalue().strip()
        self.assertIn("No calculations found", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_clear_history(self, mock_stdout):
        """Test clearing history"""
        self.repl.onecmd('clear_history')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "History cleared")

    @patch('sys.stdout', new_callable=StringIO)
    def test_save_history(self, mock_stdout):
        """Test saving history to a file"""
        self.repl.onecmd('save_history test.csv')
        output = mock_stdout.getvalue().strip()
        self.assertIn("History saved to test.csv", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_load_history(self, mock_stdout):
        """Test loading history from a file"""
        self.repl.onecmd('load_history test.csv')
        output = mock_stdout.getvalue().strip()
        self.assertIn("History loaded from test.csv", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_quit(self, mock_stdout):
        """Test the quit command"""
        self.assertTrue(self.repl.do_quit(''))
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Goodbye!")

    @patch('sys.stdout', new_callable=StringIO)
    def test_help(self, mock_stdout):
        """Test the help command"""
        self.repl.onecmd('help')
        output = mock_stdout.getvalue().strip()
        self.assertIn("Available commands:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_plugin_command(self, mock_stdout):
        """Test plugin command handling"""
        self.repl.onecmd('unknown_plugin_command')
        output = mock_stdout.getvalue().strip()
        self.assertIn("Unknown command:", output)

    def test_emptyline(self):
        """Test empty line input"""
        self.assertFalse(self.repl.emptyline())

    @patch('sys.stdout', new_callable=StringIO)
    def test_eof(self, mock_stdout):
        """Test EOF handling"""
        self.repl.do_EOF('')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Goodbye!")


if __name__ == '__main__':
    unittest.main()
