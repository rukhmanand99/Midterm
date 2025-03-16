"""
Tests for the scientific calculator plugin.
"""
import math
import pytest
from plugins.statistics import PowerCommand, SquareRootCommand, LogarithmCommand

def test_power_command():
    """Test power operation"""
    cmd = PowerCommand()
    assert cmd.execute(2, 3) == 8
    assert cmd.execute(3, 2) == 9
    assert cmd.execute(2, 0) == 1
    assert cmd.get_description() == "Power"

def test_square_root_command():
    """Test square root operation"""
    cmd = SquareRootCommand()
    assert cmd.execute(4) == 2
    assert cmd.execute(9) == 3
    assert cmd.execute(0) == 0
    assert cmd.get_description() == "Square Root"

def test_square_root_negative():
    """Test square root of negative number"""
    cmd = SquareRootCommand()
    with pytest.raises(ValueError):
        cmd.execute(-1)

def test_logarithm_command():
    """Test natural logarithm operation"""
    cmd = LogarithmCommand()
    assert cmd.execute(math.e) == 1
    assert cmd.execute(1) == 0
    assert cmd.get_description() == "Natural Logarithm"

def test_logarithm_invalid():
    """Test logarithm of invalid numbers"""
    cmd = LogarithmCommand()
    with pytest.raises(ValueError):
        cmd.execute(0)
    with pytest.raises(ValueError):
        cmd.execute(-1)
