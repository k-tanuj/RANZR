# detection/response.py
"""Automatic response utilities for RANZR.

Provides functions to terminate suspicious processes and log the action.
The module uses ``psutil`` to safely kill a process by PID or by name.
"""

import psutil
import logging
from datetime import datetime

# Configure a simple logger (could be enhanced later)
logging.basicConfig(
    filename="response.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def terminate_process_by_pid(pid: int) -> bool:
    """Terminate a process given its PID.

    Returns ``True`` if the process was terminated, ``False`` otherwise.
    """
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=5)
        logging.info(f"Terminated process PID {pid}")
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        logging.warning(f"Failed to terminate PID {pid}: {e}")
        return False

def terminate_process_by_name(name: str) -> int:
    """Terminate all processes matching *name*.

    Returns the number of processes successfully terminated.
    """
    terminated = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info["name"] and proc.info["name"].lower() == name.lower():
            if terminate_process_by_pid(proc.info["pid"]):
                terminated += 1
    logging.info(f"Terminated {terminated} processes with name '{name}'")
    return terminated

def log_action(action: str, details: str = ""):
    """Utility to log a custom action.

    ``action`` is a short description, ``details`` can contain extra info.
    """
    timestamp = datetime.utcnow().isoformat() + "Z"
    logging.info(f"{timestamp} - {action} - {details}")
