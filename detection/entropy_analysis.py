# detection/entropy_analysis.py
"""Entropy analysis utilities for RANZR.

Provides functions to compute Shannon entropy of a file's byte distribution.
The entropy is normalized to a 0-8 scale (max entropy for a byte is 8 bits).
"""

import math
import os

def shannon_entropy(file_path):
    """Calculate the Shannon entropy of the file at *file_path*.

    Returns a float between 0.0 and 8.0.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read file as bytes
    with open(file_path, "rb") as f:
        data = f.read()
    if not data:
        return 0.0

    # Frequency of each byte value (0-255)
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1
    total_bytes = len(data)

    entropy = 0.0
    for count in byte_counts:
        if count == 0:
            continue
        p = count / total_bytes
        entropy -= p * math.log2(p)
    # Max entropy for a byte is 8 bits; already in that range
    return entropy

def normalized_entropy(file_path, max_entropy=8.0):
    """Return entropy normalized to 0‑1 range.

    ``max_entropy`` defaults to 8.0 (the theoretical maximum for a byte).
    """
    return shannon_entropy(file_path) / max_entropy
