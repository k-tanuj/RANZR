import os
import sys
import numpy as np
from datetime import datetime

# Import RANZR modules
from detection.feature_extraction import extract_features
from detection.entropy_analysis import normalized_entropy
from detection.threat_score import compute_threat_score, severity_level
from detection.response import terminate_process_by_pid
from ai_engine.isolation_forest_model import train_model, anomaly_score
from reporting.explanation import generate_explanation
from reporting.voice_alert import generate_voice_alert
from reporting.pdf_report import generate_report
from blockchain.prepare_data import prepare_blockchain_payload
from config import settings

def main():
    print("Initializing RANZR AI-Powered Ransomware Detection Pipeline")
    
    # --- 1. Train AI Anomaly Detection Baseline ---
    print("\n[AI Engine] Training Isolation Forest Baseline...")
    # Generate synthetic normal baseline data (n_samples, n_features=5)
    np.random.seed(42)
    synthetic_normal_data = np.random.normal(0, 0.1, (1000, 5))
    train_model(synthetic_normal_data)
    print(" -> Model trained successfully.")

    # --- 2. Simulate System Monitoring Input ---
    print("\n[Monitoring] Simulating suspicious behavior input...")
    dummy_monitoring_data = {
        "file_mod_count": 850,       # High file modification rate
        "rename_count": 400,         # Suspicious renaming
        "cpu_usage": 95.0,           # High CPU spike
        "memory_usage": 50.0,
        "new_process_count": 5,
    }
    mock_suspicious_pid = 9999
    # We will use this script itself to simulate a file being encrypted
    mock_file_path = os.path.abspath(__file__)

    # --- 3. Feature Extraction & AI Scoring ---
    print("[AI Engine] Extracting features and predicting anomaly score...")
    features = extract_features(dummy_monitoring_data)
    score_anomaly = anomaly_score(features)
    print(f" -> Anomaly Score: {score_anomaly:.2f}")

    # --- 4. Entropy Analysis ---
    print(f"[Analysis] Calculating file entropy for: {mock_file_path}")
    score_entropy = normalized_entropy(mock_file_path)
    print(f" -> Normalized Entropy Score: {score_entropy:.2f}")

    # --- 5. Threat Score Calculation ---
    print("[Engine] Computing overall threat score...")
    scores = {
        "anomaly": score_anomaly,
        "entropy": score_entropy,
        # Normalize CPU usage (assumes 0-100 scale)
        "cpu": dummy_monitoring_data["cpu_usage"] / 100.0,
        # Proxy metrics for demonstration based on raw values
        "file_activity": min(dummy_monitoring_data["file_mod_count"] / 1000.0, 1.0),
        "process": min(dummy_monitoring_data["new_process_count"] / 10.0, 1.0),
    }
    threat_score = compute_threat_score(scores, settings.get("weights"))
    severity = severity_level(threat_score)
    print(f" -> Final Threat Score: {threat_score} ({severity})")

    # Final record to hold incident data
    incident_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "threat_score": threat_score,
        "severity": severity,
        "anomaly_score": score_anomaly,
        "entropy_score": score_entropy,
        "cpu_usage": dummy_monitoring_data["cpu_usage"],
        "file_mod_rate": dummy_monitoring_data["file_mod_count"],
        "action_taken": "None"
    }

    # --- 6. Automated Response Logic ---
    if severity in ["High Risk", "Critical"]:
        print(f"\n[Response] {severity} behavior detected! Initiating containment...")
        # attempt to kill the dummy process (will likely fail since it's dummy, but logic passes)
        action_msg = f"Attempted to terminate PID {mock_suspicious_pid}"
        terminate_process_by_pid(mock_suspicious_pid)
        incident_record["action_taken"] = action_msg
        
        # --- 7. Voice Alert (ElevenLabs) ---
        print("\n[Alert] Triggering voice warning...")
        try:
            generate_voice_alert(
                f"Critical ransomware behavior detected with threat score {threat_score}. Suspicious process containment initiated."
            )
        except Exception as e:
            print(f" -> Voice alert failed (Ensure valid ElevenLabs key in config): {e}")

        # --- 8. AI Threat Explanation (Ollama) ---
        print("\n[AI Engine] Generating reasoning via local LLM (Ollama)...")
        try:
            explanation = generate_explanation(incident_record)
            incident_record["explanation"] = explanation
            print(" -> Explanation:\n" + explanation)
        except Exception as e:
            print(f" -> Explanation generation failed (Is Ollama running with 'llama3'?): {e}")
            incident_record["explanation"] = "AI generation failed."
    else:
        print("\n[Status] System operating within safe parameters.")

    # --- 9. PDF Report Generation ---
    print("\n[Reporting] Generating incident PDF report...")
    pdf_path = os.path.join(os.path.dirname(__file__), "incident_report.pdf")
    pdf_hash = generate_report(incident_record, pdf_path)
    print(f" -> Report generated at: {pdf_path}")
    print(f" -> Document Hash (SHA-256): {pdf_hash}")

    # --- 10. Blockchain Data Prep for Algorand ---
    print("\n[Blockchain] Formatting data for Algorand TestNet logging...")
    payload = prepare_blockchain_payload(incident_record)
    print(f" -> Payload JSON: {payload['payload']}")
    print(f" -> Payload Hash for Smart Contract: {payload['hash']}")
    print("\nPipeline Execution Complete. Handing off hash to Nilesh for Blockchain deployment.")

if __name__ == "__main__":
    main()
