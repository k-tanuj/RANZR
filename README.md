# RANZR: AI-Powered Behavioral Ransomware Detection & Autonomous Response System

## Project Overview
RANZR is a real-time, behavior-based ransomware detection and autonomous containment system. Unlike traditional signature-based antivirus solutions, RANZR leverages AI anomaly detection, file entropy analysis, and a structured threat scoring engine to identify zero-day and polymorphic ransomware threats in real-time.

When suspicious activity is detected, RANZR initiates an autonomous response that includes:
- Automated process termination
- AI-generated root cause explanation (powered by Ollama)
- Real-time voice alerts (powered by ElevenLabs)
- Forensic PDF report generation
- Tamper-proof evidence logging formatted for the Algorand blockchain

## Roles
This repository implements **Tanuj's responsibilities** (AI & Intelligence Lead), which include:
- AI detection logic (Isolation Forest)
- File entropy analysis
- Threat scoring engine
- Automated response logic
- AI explanation system (Ollama)
- Voice alert integration (ElevenLabs)
- Forensic report generation (ReportLab)
- Blockchain-ready evidence formatting

## System Architecture
```
System Monitoring -> Feature Extraction -> AI Anomaly Detection -> Entropy Analysis 
-> Threat Score Engine -> Automatic Response -> Voice Alert (ElevenLabs) 
-> AI Threat Explanation (Ollama) -> Incident Report (PDF) 
-> Blockchain Logging (Algorand) -> Dashboard
```

## Setup & Installation
1. **Prerequisites:** Python 3.8+
2. **Install core dependencies:**
   ```bash
   pip install numpy scipy scikit-learn psutil reportlab pyyaml requests pytest
   ```
3. **External Services:**
   - **Ollama**: Must be installed locally and running with the `llama3` (or `mistral`) model pulled (`ollama run llama3`).
   - **ElevenLabs**: Update `config/settings.yaml` with your valid API key for voice alerts.

## Running the Pipeline
To execute the end-to-end AI detection and response pipeline simulation:
```bash
python main_ai_pipeline.py
```

## Running Tests
To run the unit test suite:
```bash
pytest tests/
```

## Project Structure
- `detection/`: Core feature extraction, entropy analysis, threat scoring, and response.
- `ai_engine/`: Isolation Forest model training and inference.
- `reporting/`: AI explanation (Ollama), voice alerts (ElevenLabs), and PDF report generation.
- `blockchain/`: Data formatting and hashing for Algorand smart contracts.
- `config/`: Centralized settings (thresholds, weights, API keys).
- `tests/`: Unit tests for all components.
