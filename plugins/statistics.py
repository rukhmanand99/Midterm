"""
Scientific calculator plugin providing advanced mathematical operations.
"""
import math
import logging

from src.calculator import Command

class PowerCommand(Command):
    """Command to calculate power of a number"""
    def execute(self, a: float, b: float) -> float:
        """Calculate base raised to exponent"""
        logging.info("Calculating %s raised to %s", a, b)
        return math.pow(float(a), float(b))

    def get_description(self) -> str:
        """Get command description"""
        return "Power"

class SquareRootCommand(Command):
    """Command to calculate square root"""
    def execute(self, a: float, b: float = 0) -> float:
        """Calculate square root of a number"""
        if float(a) < 0:
            logging.error("Square root of negative number attempted")
            raise ValueError("Cannot calculate square root of negative number")
        logging.info("Calculating square root of %s", a)
        return math.sqrt(float(a))

    def get_description(self) -> str:
        """Get command description"""
        return "Square Root"

class LogarithmCommand(Command):
    """Command to calculate logarithm"""
    def execute(self, a: float, b: float = math.e) -> float:
        """Calculate logarithm of a number with given base (default: e)"""
        if float(a) <= 0:
            logging.error("Logarithm of non-positive number attempted")
            raise ValueError("Cannot calculate logarithm of non-positive number")
        logging.info("Calculating logarithm of %s with base %s", a, b)
        return math.log(float(a), float(b))

    def get_description(self) -> str:
        """Get command description"""
        return "Natural Logarithm"
