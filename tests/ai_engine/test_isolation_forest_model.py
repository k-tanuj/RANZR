# tests/ai_engine/test_isolation_forest_model.py
"""Tests for the Isolation Forest model wrapper."""

import numpy as np
import pytest
from ai_engine.isolation_forest_model import train_model, anomaly_score

def test_train_and_predict():
    # Create simple synthetic normal data (e.g., clustered around zero)
    np.random.seed(42)
    normal_data = np.random.normal(0, 0.1, (100, 5))
    
    # Train model (now returns a dictionary of ensemble models)
    models = train_model(normal_data)
    assert models is not None
    assert isinstance(models, dict)
    assert "iforest" in models
    assert "lof" in models

    # Predict anomaly score for a normal sample
    normal_sample = np.array([0, 0, 0, 0, 0])
    score_normal = anomaly_score(normal_sample)
    
    # Predict anomaly score for an anomalous sample (far from zero)
    anomalous_sample = np.array([10, -10, 5, 20, -5])
    score_anomalous = anomaly_score(anomalous_sample)
    
    # The anomaly score should be higher for the anomalous sample
    assert score_anomalous > score_normal
