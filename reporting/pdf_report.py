# reporting/pdf_report.py
"""PDF incident report generation for RANZR.

Uses ReportLab to create a professional PDF containing timestamp, threat scores,
AI explanation, key metrics, action taken, and a SHA‑256 hash of the report.
"""

import os
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def _hash_file(file_path: str) -> str:
    """Compute SHA‑256 hash of the given file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_report(report_data: dict, output_path: str) -> str:
    """Generate a PDF incident report.

    Parameters
    ----------
    report_data: dict
        Expected keys: ``timestamp``, ``threat_score``, ``anomaly_score``,
        ``entropy_score``, ``cpu_usage``, ``file_mod_rate``, ``action_taken``,
        ``explanation`` (string).
    output_path: str
        Destination file path for the PDF.

    Returns
    -------
    str
        The SHA‑256 hash of the generated PDF.
    """
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER
    margin = 50
    y = height - margin
    line_height = 14

    def draw_line(text):
        nonlocal y
        c.drawString(margin, y, text)
        y -= line_height

    draw_line(f"Incident Report – {report_data.get('timestamp', datetime.utcnow().isoformat())}")
    draw_line(" ")
    draw_line(f"Threat Score: {report_data.get('threat_score', 'N/A')}")
    draw_line(f"Anomaly Score: {report_data.get('anomaly_score', 'N/A')}")
    draw_line(f"Entropy Score: {report_data.get('entropy_score', 'N/A')}")
    draw_line(f"CPU Usage: {report_data.get('cpu_usage', 'N/A')}%")
    draw_line(f"File Modification Rate: {report_data.get('file_mod_rate', 'N/A')}")
    draw_line(f"Action Taken: {report_data.get('action_taken', 'N/A')}")
    draw_line(" ")
    draw_line("AI Explanation:")
    explanation = report_data.get('explanation', '')
    for line in explanation.splitlines():
        draw_line(line)
    c.showPage()
    c.save()
    # Compute hash
    return _hash_file(output_path)
