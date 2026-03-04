# detection/feature_extraction.py
"""Feature extraction utilities for RANZR.

This module provides functions to normalize raw monitoring data and construct a feature vector
compatible with the Isolation Forest model.
"""

import numpy as np

def normalize_value(value, min_val, max_val):
    """Scale a numeric value to the range [0, 1]."""
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)

def extract_features(monitoring_data):
    """Convert raw monitoring data dict into a NumPy feature array.

    Expected keys in ``monitoring_data``:
        - ``file_mod_count`` (int)
        - ``rename_count`` (int)
        - ``cpu_usage`` (float, percent)
        - ``memory_usage`` (float, percent)
        - ``new_process_count`` (int)
    """
    # Define reasonable min/max ranges for normalization (these can be tuned later)
    ranges = {
        "file_mod_count": (0, 1000),
        "rename_count": (0, 500),
        "cpu_usage": (0, 100),
        "memory_usage": (0, 100),
        "new_process_count": (0, 200),
    }

    features = []
    for key in ["file_mod_count", "rename_count", "cpu_usage", "memory_usage", "new_process_count"]:
        val = monitoring_data.get(key, 0)
        min_val, max_val = ranges[key]
        features.append(normalize_value(val, min_val, max_val))

    return np.array(features, dtype=np.float32)
