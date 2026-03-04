# config/__init__.py
"""Configuration utilities for RANZR."""

import os
import yaml

def load_config():
    """Load settings from settings.yaml."""
    config_path = os.path.join(os.path.dirname(__file__), "settings.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return {}

settings = load_config()
