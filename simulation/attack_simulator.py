"""
RANZR Attack Simulator - Safe Ransomware Behavior Emulator

This script simulates ransomware-like behavior WITHOUT using actual malware:
- Rapid file modifications (simulates encryption)
- Mass file renaming (adds .locked extension)
- CPU spike generation
- High file creation/deletion activity

Usage:
    python -m simulation.attack_simulator [--intensity low|medium|high]
    
Press Ctrl+C to stop the simulation.
"""

import os
import time
import random
import threading
import argparse
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_FOLDER = PROJECT_ROOT / "test_folder"


class RansomwareSimulator:
    """Simulates ransomware behavior for testing detection systems."""
    
    def __init__(self, intensity="medium"):
        self.intensity = intensity
        self.running = True
        
        # Intensity configurations
        self.configs = {
            "low": {
                "file_count": 5,
                "modify_delay": 1.0,
                "rename_delay": 3.0,
                "cpu_iterations": 500000
            },
            "medium": {
                "file_count": 15,
                "modify_delay": 0.3,
                "rename_delay": 1.5,
                "cpu_iterations": 1000000
            },
            "high": {
                "file_count": 30,
                "modify_delay": 0.1,
                "rename_delay": 0.5,
                "cpu_iterations": 2000000
            }
        }
        
        self.config = self.configs.get(intensity, self.configs["medium"])
        
    def setup_environment(self):
        """Create target folder and initial test files."""
        TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
        
        print(f"[+] Setting up simulation environment in: {TARGET_FOLDER}")
        print(f"[+] Attack intensity: {self.intensity.upper()}")
        print(f"[+] Creating {self.config['file_count']} initial files...")
        
        for i in range(self.config['file_count']):
            file_path = TARGET_FOLDER / f"document_{i:03d}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                # Write some random content
                f.write(f"Document {i}\n")
                f.write("=" * 50 + "\n")
                f.write("Important business data\n" * 5)
                f.write(f"Created at: {time.ctime()}\n")
        
        print(f"[✓] Environment ready!\n")
    
    def modify_files_continuously(self):
        """
        Rapidly modify files to simulate encryption behavior.
        Ransomware typically encrypts files, which shows up as modifications.
        """
        print("[Thread] File modification attack started...")
        
        while self.running:
            try:
                files = list(TARGET_FOLDER.glob("*.txt"))
                if not files:
                    time.sleep(0.5)
                    continue
                
                # Modify random files
                for _ in range(min(3, len(files))):
                    file_path = random.choice(files)
                    try:
                        with open(file_path, "a", encoding="utf-8") as f:
                            # Simulate encryption by appending random data
                            f.write(f"[ENCRYPTED_{random.randint(10000, 99999)}]\n")
                    except (PermissionError, FileNotFoundError):
                        pass
                
                time.sleep(self.config['modify_delay'])
            except Exception as e:
                print(f"[!] Modify thread error: {e}")
                time.sleep(1)
    
    def rename_files_continuously(self):
        """
        Rename files by adding .locked extension.
        Typical ransomware behavior to mark encrypted files.
        """
        print("[Thread] File rename attack started...")
        
        while self.running:
            try:
                files = list(TARGET_FOLDER.glob("*.txt"))
                
                for file_path in files:
                    if not self.running:
                        break
                    
                    try:
                        # Add .locked extension
                        new_path = file_path.with_suffix(file_path.suffix + ".locked")
                        
                        # Only rename if target doesn't exist
                        if not new_path.exists():
                            file_path.rename(new_path)
                        
                        # Rename back after a moment (to keep simulation running)
                        time.sleep(0.2)
                        if new_path.exists() and not file_path.exists():
                            new_path.rename(file_path)
                    except (PermissionError, FileNotFoundError, FileExistsError):
                        pass
                
                time.sleep(self.config['rename_delay'])
            except Exception as e:
                # Suppress rename errors (expected in concurrent simulation)
                time.sleep(1)
    
    def create_cpu_spike(self):
        """
        Generate CPU spike to simulate ransomware encryption overhead.
        Real ransomware causes high CPU usage during encryption.
        """
        print("[Thread] CPU spike generator started...")
        
        while self.running:
            try:
                # Perform intensive computation
                _ = [x ** 2 for x in range(self.config['cpu_iterations'])]
                time.sleep(0.1)  # Brief pause
            except Exception as e:
                print(f"[!] CPU thread error: {e}")
                time.sleep(1)
    
    def create_delete_cycle(self):
        """
        Simulate file creation and deletion patterns.
        Some ransomware variants create temp files during encryption.
        """
        print("[Thread] File creation/deletion cycle started...")
        
        while self.running:
            try:
                # Create temporary files
                for i in range(3):
                    temp_file = TARGET_FOLDER / f"~tmp_{random.randint(1000, 9999)}.tmp"
                    temp_file.write_text(f"Temp data {i}")
                
                time.sleep(0.5)
                
                # Delete temp files
                for temp_file in TARGET_FOLDER.glob("~tmp_*.tmp"):
                    try:
                        temp_file.unlink()
                    except FileNotFoundError:
                        pass
                
                time.sleep(2)
            except Exception as e:
                print(f"[!] Create/Delete thread error: {e}")
                time.sleep(1)
    
    def run(self):
        """Start the ransomware simulation with all attack vectors."""
        self.setup_environment()
        
        print("=" * 60)
        print("🚨 RANSOMWARE SIMULATION ACTIVE 🚨")
        print("=" * 60)
        print("\n[*] Attack vectors deployed:")
        print("    • Rapid file modifications")
        print("    • Mass file renaming (.locked)")
        print("    • CPU spike generation")
        print("    • File creation/deletion cycles")
        print("\n[*] Your monitoring system should now detect:")
        print("    • High file_modification_rate")
        print("    • Elevated rename_count")
        print("    • CPU usage spike (>80%)")
        print("    • Process anomalies")
        print("\n[!] Press Ctrl+C to stop simulation\n")
        print("=" * 60 + "\n")
        
        # Start attack threads
        threads = [
            threading.Thread(target=self.modify_files_continuously, daemon=True),
            threading.Thread(target=self.rename_files_continuously, daemon=True),
            threading.Thread(target=self.create_cpu_spike, daemon=True),
            threading.Thread(target=self.create_delete_cycle, daemon=True),
        ]
        
        for thread in threads:
            thread.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[!] Stopping simulation...")
            self.running = False
            time.sleep(2)
            print("[✓] Simulation stopped safely")
            print(f"[*] Test files remain in: {TARGET_FOLDER}")


def main():
    parser = argparse.ArgumentParser(
        description="RANZR Attack Simulator - Safe ransomware behavior emulator"
    )
    parser.add_argument(
        "--intensity",
        choices=["low", "medium", "high"],
        default="medium",
        help="Attack intensity level (default: medium)"
    )
    
    args = parser.parse_args()
    
    simulator = RansomwareSimulator(intensity=args.intensity)
    simulator.run()


if __name__ == "__main__":
    main()
