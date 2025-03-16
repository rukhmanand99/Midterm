"""
Plugin manager for the Advanced Calculator.

This module implements a Singleton pattern for managing calculator plugins.
It handles plugin discovery, loading, and registration with the calculator.
"""
import os
import importlib.util
import logging
from typing import Dict, Optional, Type

from .calculator import Command

class PluginManagerError(Exception):
    """Base exception class for plugin manager errors"""

class PluginLoadError(PluginManagerError):
    """Exception raised when a plugin fails to load"""

class PluginDiscoveryError(PluginManagerError):
    """Exception raised when plugin discovery fails"""

class PluginManager:
    """Singleton class for managing calculator plugins"""
    _instance: Optional['PluginManager'] = None
    _plugins: Dict[str, Type[Command]] = {}

    def __new__(cls) -> 'PluginManager':
        """Create or return the singleton instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._plugins = {}  # Initialize in __new__
        return cls._instance

    def discover_plugins(self, plugin_dir: Optional[str] = None) -> None:
        """Discover and load plugins from the plugin directory"""
        if plugin_dir is None:
            plugin_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'plugins'
            )

        if not os.path.exists(plugin_dir):
            raise PluginDiscoveryError(f"Plugin directory not found: {plugin_dir}")

        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_path = os.path.join(plugin_dir, filename)
                try:
                    self._load_plugin(plugin_path)
                except Exception as e:
                    logging.error("Failed to load plugin %s: %s", filename, str(e))
                    raise PluginLoadError(f"Failed to load {filename}: {str(e)}") from e

    def _load_plugin(self, plugin_path: str) -> None:
        """Load a plugin module and register its commands"""
        module_name = os.path.splitext(os.path.basename(plugin_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Invalid plugin file: {plugin_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for item_name in dir(module):
            item = getattr(module, item_name)
            if (isinstance(item, type) and
                issubclass(item, Command) and
                item is not Command):
                self._plugins[item_name.lower()] = item
                logging.info("Loaded plugin command: %s", item_name)

    def get_plugin(self, name: str) -> Optional[Type[Command]]:
        """Get a plugin command by name"""
        return self._plugins.get(name.lower())
