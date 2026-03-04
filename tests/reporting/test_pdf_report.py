# tests/reporting/test_pdf_report.py
"""Tests for the PDF incident report generation module."""

import os
import json
from reportlab.pdfgen import canvas
from reporting.pdf_report import generate_report, _hash_file

def test_generate_report_creates_file_and_valid_hash(tmp_path):
    # Dummy incident report data
    report_data = {
        "timestamp": "2026-03-02T12:00:00Z",
        "threat_score": 95.0,
        "anomaly_score": 0.98,
        "entropy_score": 0.90,
        "cpu_usage": 92.5,
        "file_mod_rate": 450,
        "action_taken": "Terminated PID 1234",
        "explanation": "High file activity and anomaly score indicating ransomware."
    }
    output_path = os.path.join(tmp_path, "incident_report.pdf")
    
    # Generate the report
    file_hash = generate_report(report_data, output_path)
    
    # Check that file exists
    assert os.path.exists(output_path)
    # Check that file size is greater than 0
    assert os.path.getsize(output_path) > 0
    # Check that the hash is valid (64 characters for SHA-256 hex digest)
    assert len(file_hash) == 64
    
    # Verify that the computed hash matches the returned hash
    computed_hash = _hash_file(output_path)
    assert file_hash == computed_hash
