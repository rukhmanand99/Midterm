"""
Test module for the plugin manager functionality.

This module tests plugin discovery, loading, and error handling.
"""
import pathlib
from unittest.mock import patch
import pytest
from src.plugin_mananger import PluginManager, PluginLoadError

class TestCommand:
    """Test command for plugin system testing"""
    def execute(self, first_value: float, second_value: float) -> float:
        """Test command execution"""
        return first_value + second_value

    def get_description(self) -> str:
        """Get command description"""
        return "Test Command"

def test_plugin_manager_singleton():
    """Test plugin manager singleton pattern"""
    manager1 = PluginManager()
    manager2 = PluginManager()
    assert manager1 is manager2

def test_discover_plugins():
    """Test plugin discovery"""
    manager = PluginManager()
    manager.discover_plugins()
    assert len(manager._plugins) > 0  # pylint: disable=protected-access

def test_get_plugin():
    """Test getting a plugin"""
    manager = PluginManager()
    # Reset plugins to ensure clean state
    manager._plugins = {}  # pylint: disable=protected-access
    # Add a test plugin
    manager._plugins['test'] = lambda: None  # pylint: disable=protected-access
    plugin = manager.get_plugin('test')
    assert plugin is not None

def test_get_nonexistent_plugin():
    """Test getting a non-existent plugin"""
    manager = PluginManager()
    plugin = manager.get_plugin('nonexistent')
    assert plugin is None

def test_plugin_load_error():
    """Test error handling for invalid plugin files"""
    manager = PluginManager()
    mock_spec = type('MockSpec', (), {'loader': None})()
    with patch('importlib.util.spec_from_file_location', return_value=mock_spec):
        with pytest.raises(PluginLoadError):
            # pylint: disable=protected-access
            manager._load_plugin(str(pathlib.Path('nonexistent.py')))

def test_plugin_registration():
    """Test plugin registration"""
    manager = PluginManager()
    # pylint: disable=protected-access
    manager._plugins = {}  # Reset plugins
    manager._load_plugin = lambda x: None  # Mock _load_plugin
    manager.discover_plugins()
    assert isinstance(manager._plugins, dict)
