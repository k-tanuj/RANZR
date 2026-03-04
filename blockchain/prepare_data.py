# blockchain/prepare_data.py
"""Data preparation utilities for blockchain logging in RANZR.

This module formats incident information into a JSON payload suitable for
submission to an Algorand smart contract and provides a SHA‑256 hash of the
payload for tamper‑proof verification.
"""

import json
import hashlib
from typing import Dict, Any

def format_incident_data(incident: Dict[str, Any]) -> str:
    """Return a JSON string representation of *incident* with sorted keys.

    The JSON is compact (no whitespace) to ensure a deterministic hash.
    """
    return json.dumps(incident, separators=(',', ':'), sort_keys=True)

def compute_hash(data_str: str) -> str:
    """Compute the SHA‑256 hash of the given string and return the hex digest."""
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def prepare_blockchain_payload(incident: Dict[str, Any]) -> Dict[str, str]:
    """Prepare the payload for Algorand logging.

    Returns a dictionary with two keys:
        - ``payload``: the JSON string
        - ``hash``: SHA‑256 hash of the payload
    """
    payload = format_incident_data(incident)
    payload_hash = compute_hash(payload)
    return {"payload": payload, "hash": payload_hash}
