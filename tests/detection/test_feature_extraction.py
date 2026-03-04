# tests/detection/test_feature_extraction.py
"""Tests for the feature extraction module."""

import numpy as np
from detection.feature_extraction import extract_features

def test_extract_features_returns_correct_shape():
    # Provide dummy monitoring data with typical keys
    data = {
        "file_mod_count": 10,
        "rename_count": 2,
        "cpu_usage": 30.5,
        "memory_usage": 45.0,
        "new_process_count": 1,
    }
    features = extract_features(data)
    assert isinstance(features, np.ndarray)
    assert features.shape == (5,)
    # All values should be normalized between 0 and 1
    assert np.all(features >= 0) and np.all(features <= 1)
