# ai_engine/isolation_forest_model.py
"""Isolation Forest model utilities for RANZR.

This module provides functions to train a baseline Isolation Forest model on synthetic
normal data and to compute an anomaly score for live monitoring data.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

# Default model parameters (can be overridden via config)
DEFAULT_PARAMS_IF = {
    "n_estimators": 100,
    "max_samples": "auto",
    "contamination": "auto",
    "random_state": 42,
}

DEFAULT_PARAMS_LOF = {
    "n_neighbors": 20,
    "novelty": True, # Required to predict on new samples
    "contamination": "auto",
}

_models = {}

def train_model(training_data: np.ndarray, params: dict = None) -> dict:
    """Train an Ensemble model (Isolation Forest + LOF) on *training_data*.

    Parameters
    ----------
    training_data: np.ndarray
        2‑D array where each row is a feature vector representing normal behavior.
    params: dict, optional
        Model hyper‑parameters to override defaults. Currently unused for LOF.
    """
    global _models
    
    # Preprocessing scaler for better LOF performance
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(training_data)
    
    # Train Isolation Forest
    if_params = params if params else DEFAULT_PARAMS_IF
    iforest = IsolationForest(**if_params)
    iforest.fit(scaled_data)
    
    # Train Local Outlier Factor
    lof = LocalOutlierFactor(**DEFAULT_PARAMS_LOF)
    lof.fit(scaled_data)
    
    _models = {
        "scaler": scaler,
        "iforest": iforest,
        "lof": lof
    }
    return _models

def anomaly_score(sample: np.ndarray) -> float:
    """Return an ensemble anomaly score (0‑1) for a single *sample*.

    Combines weighted probabilities from Isolation Forest and Local Outlier Factor.
    """
    if not _models:
        raise RuntimeError("Ensemble models have not been trained.")
        
    scaler = _models["scaler"]
    iforest = _models["iforest"]
    lof = _models["lof"]
    
    sample_reshaped = sample.reshape(1, -1)
    scaled_sample = scaler.transform(sample_reshaped)
    
    # Isolation Forest: ``decision_function`` returns higher values for normal samples
    raw_if = iforest.decision_function(scaled_sample)[0]
    prob_if = 1 / (1 + np.exp(raw_if)) # Sigmoid to convert to anomaly probability
    
    # LOF: ``decision_function`` returns higher values for normal samples too
    raw_lof = lof.decision_function(scaled_sample)[0]
    prob_lof = 1 / (1 + np.exp(raw_lof))
    
    # Ensemble average (weights can be adjusted depending on historical precision)
    ensemble_prob = (prob_if * 0.6) + (prob_lof * 0.4)
    
    return float(ensemble_prob)
