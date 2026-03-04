# tests/detection/test_entropy_analysis.py
"""Tests for the entropy analysis module."""

import os
import numpy as np
import pytest
from detection.entropy_analysis import shannon_entropy, normalized_entropy

def test_shannon_entropy_range(tmp_path):
    # Create a temporary file with uniform byte distribution (high entropy)
    file_path = os.path.join(tmp_path, "data.bin")
    with open(file_path, "wb") as f:
        f.write(bytes([i % 256 for i in range(1024)]))
    entropy = shannon_entropy(file_path)
    assert 0 <= entropy <= 8
    norm = normalized_entropy(file_path)
    assert 0 <= norm <= 1
