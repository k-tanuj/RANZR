# detection/threat_score.py
"""Threat score calculation utilities for RANZR.

Combines anomaly score, entropy score, CPU usage, file activity rate, and process spike
into a weighted threat score (0‑100).
"""

from typing import Dict

# Default weights (can be overridden via config)
DEFAULT_WEIGHTS = {
    "anomaly": 0.35,
    "entropy": 0.25,
    "cpu": 0.15,
    "file_activity": 0.15,
    "process": 0.10,
}

def compute_threat_score(scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
    """Calculate the overall threat score using dynamic weighting.

    Parameters
    ----------
    scores: dict
        Mapping with keys ``anomaly``, ``entropy``, ``cpu``, ``file_activity``, ``process``.
        Each value should be in the 0‑1 range (probability or normalized metric).
    weights: dict, optional
        Custom weighting factors that sum to 1.0. If omitted, ``DEFAULT_WEIGHTS`` are used.

    Returns
    -------
    float
        Threat score scaled to 0‑100.
    """
    if weights is None:
        w = DEFAULT_WEIGHTS.copy()
    else:
        w = weights.copy()
        
    required = set(DEFAULT_WEIGHTS.keys())
    missing = required - scores.keys()
    if missing:
        raise ValueError(f"Missing score components: {missing}")
        
    # --- Dynamic Weighting Logic ---
    # Ransomware drastically spikes file entropy and file activity. 
    # If entropy suggests high likeliness of encryption, adjust weights dynamically.
    if scores.get("entropy", 0.0) >= 0.82:
        # Increase the significance of entropy and file activity 
        w["entropy"] = min(w["entropy"] + 0.15, 0.45)
        w["file_activity"] = min(w["file_activity"] + 0.10, 0.35)
        
        # Normalize weights so they sum to 1.0 again
        total_weight = sum(w.values())
        for k in w:
            w[k] /= total_weight
            
    # Weighted sum
    weighted_sum = sum(scores[key] * w.get(key, 0) for key in required)
    # Scale to 0‑100
    return round(weighted_sum * 100, 2)

def severity_level(threat_score: float) -> str:
    """Return textual severity based on the threat score.

    - 0‑40   : "Safe"
    - 40‑70  : "Suspicious"
    - 70‑85  : "High Risk"
    - 85‑100 : "Critical"
    """
    if threat_score < 40:
        return "Safe"
    if threat_score < 70:
        return "Suspicious"
    if threat_score < 85:
        return "High Risk"
    return "Critical"
