# reporting/explanation.py
"""AI threat explanation utilities using Ollama.

This module formats threat data and queries a local Ollama LLM (e.g., Llama 3 or Mistral)
to generate a human‑readable explanation of why the activity resembles ransomware.
"""

import json
import subprocess

def generate_explanation(threat_data: dict) -> str:
    """Generate an explanation string from *threat_data* using Ollama.

    The *threat_data* dictionary should contain keys such as:
        - ``threat_score``
        - ``anomaly_score``
        - ``entropy_score``
        - ``cpu_usage``
        - ``file_mod_rate``
        - ``action_taken``
    The function serialises the data to JSON and passes it to Ollama via the
    ``ollama run`` command. Adjust the model name as needed.
    """
    # Serialize the data for the prompt
    data_json = json.dumps(threat_data, indent=2)
    prompt = (
        "You are an elite Enterprise AI Security Analyst for the RANZR system. "
        "Given the following ransomware detection telemetry data, explain in clear, professional "
        "language why this activity was flagged as a ransomware attack.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Focus heavily on the exact metric values (e.g., Entropy, Anomaly Score, Mod Rate).\n"
        "2. Map the observed behaviors to the MITRE ATT&CK Framework. Specifically look for tags "
        "like T1486 (Data Encrypted for Impact), T1490 (Inhibit System Recovery), or T1036 (Masquerading).\n"
        "3. Provide a brief recommendation for the SOC team based on the 'action_taken'.\n\n"
        "TELEMETRY DATA:\n"
        f"{data_json}\n"
    )
    # Run Ollama locally via its REST API
    try:
        import requests
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        raise RuntimeError(f"Ollama execution failed: {str(e)}")
