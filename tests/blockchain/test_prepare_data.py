# tests/blockchain/test_prepare_data.py
"""Tests for the blockchain data preparation module."""

import json
from blockchain.prepare_data import format_incident_data, compute_hash, prepare_blockchain_payload

def test_format_incident_data():
    incident = {"b": 2, "a": 1, "c": [3, 4], "d": {"e": 5}}
    formatted = format_incident_data(incident)
    # Ensure keys are sorted and there's no extra whitespace
    assert formatted == '{"a":1,"b":2,"c":[3,4],"d":{"e":5}}'

def test_prepare_blockchain_payload():
    incident = {
        "timestamp": "2026-03-02T12:00:00Z",
        "threat_score": 95.0,
        "action_taken": "Terminated PID 1234"
    }
    result = prepare_blockchain_payload(incident)
    assert "payload" in result
    assert "hash" in result
    
    # Verify the payload is formatted correctly
    expected_payload = format_incident_data(incident)
    assert result["payload"] == expected_payload
    
    # Verify the hash matches the payload
    expected_hash = compute_hash(expected_payload)
    assert result["hash"] == expected_hash
    assert len(result["hash"]) == 64
