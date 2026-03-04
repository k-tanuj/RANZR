# reporting/chatbot.py
"""Interactive Security Analyst Chatbot for RANZR.

Supports both "offline" (Local Ollama) and "online" (Cloud API like Groq/OpenAI) modes.
Allows the SOC team to interrogate the system about the latest ransomware incident.
"""

import sys
import json
import requests
import os

# Add parent directory to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def load_latest_incident_data():
    """Attempt to load the latest incident data (mocked for this demo)."""
    # In a full system, this would load the latest JSON payload or database entry.
    return {
        "status": "Ransomware Detected",
        "threat_score": 72.67,
        "anomalies": ["High CPU (95%)", "Rapid File Modifications", "High Entropy (0.89)"],
        "action_taken": "Suspicious process terminated."
    }

def chat_offline_ollama(messages):
    """Query the local Ollama LLM."""
    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": "llama3",
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"Offline LLM Error: Ensure Ollama is running. ({e})"

def chat_online_api(messages):
    """Query the online LLM API (Default configured for Groq's fast free tier)."""
    url = settings.get("online_llm_endpoint")
    api_key = settings.get("online_llm_api_key")
    model = settings.get("online_llm_model", "llama3-8b-8192")

    if not api_key or api_key == "YOUR_ONLINE_API_KEY_HERE":
        return "Online LLM Error: Please set your 'online_llm_api_key' in config/settings.yaml."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Online API Error: {e}"

def start_chatbot():
    print("=====================================================")
    print("🛡️ RANZR Chatbot Initialized")
    print("=====================================================")
    
    mode = settings.get("chatbot_mode", "offline").lower()
    print(f"[*] Mode: {mode.upper()}")
    
    incident = load_latest_incident_data()
    system_prompt = (
        "You are RANZR, an elite cybersecurity assistant. "
        "You are helping a SOC analyst investigate a recent ransomware incident. "
        f"Here is the context of the latest attack: {json.dumps(incident)}\n"
        "Keep your answers concise, professional, and actionable."
    )

    # Message history
    messages = [{"role": "system", "content": system_prompt}]

    print("[*] Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("Analyst > ")
            if user_input.lower() in ("exit", "quit"):
                print("Ending session. Stay secure.")
                break
            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})
            
            print("RANZR is thinking...\n")
            if mode == "online":
                reply = chat_online_api(messages)
            else:
                reply = chat_offline_ollama(messages)
                
            print(f"RANZR > {reply}\n")
            
            # Save the assistant reply to history
            messages.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\nEnding session. Stay secure.")
            break

if __name__ == "__main__":
    start_chatbot()
