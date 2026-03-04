# tests/detection/test_threat_score.py
"""Tests for the threat score engine."""

import pytest
from detection.threat_score import compute_threat_score, severity_level

def test_compute_threat_score():
    scores = {
        "anomaly": 0.8,
        "entropy": 0.8, # Keep below 0.82 to avoid dynamic weight shift
        "cpu": 0.5,
        "file_activity": 0.6,
        "process": 0.2,
    }
    # Weighted sum: (0.8*0.35) + (0.8*0.25) + (0.5*0.15) + (0.6*0.15) + (0.2*0.10)
    # = 0.28 + 0.20 + 0.075 + 0.09 + 0.02 = 0.665
    # Score = 66.5
    score = compute_threat_score(scores)
    assert score == 66.50

def test_dynamic_threat_score():
    scores = {
        "anomaly": 0.8,
        "entropy": 0.9, # Triggers dynamic weighting shift
        "cpu": 0.5,
        "file_activity": 0.6,
        "process": 0.2,
    }
    score = compute_threat_score(scores)
    # We just ensure it calculates a valid float score > 66.50 since weights shifted to higher risk vectors
    assert isinstance(score, float)
    assert score > 66.50

def test_missing_keys_raises_value_error():
    scores = {"anomaly": 0.8}
    with pytest.raises(ValueError, match="Missing score components"):
        compute_threat_score(scores)

def test_severity_level():
    assert severity_level(30) == "Safe"
    assert severity_level(69) == "Suspicious"
    assert severity_level(80) == "High Risk"
    assert severity_level(95) == "Critical"
