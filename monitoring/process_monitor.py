import psutil
import time
from pathlib import Path

def get_process_count() -> int:
    return len(psutil.pids())

def get_cpu_usage(interval: float = 1.0) -> float:
    return psutil.cpu_percent(interval=interval)

def get_memory_usage() -> float:
    return psutil.virtual_memory().percent   

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from monitoring.feature_extractor import FeatureExtractor  # keep this if it's working

# Resolve path relative to the project (RANZR) folder, not current working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # ...\RANZR
MONITOR_PATH = PROJECT_ROOT / "test_folder"

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, extractor):
        self.extractor = extractor

    def on_modified(self, event):
        if not event.is_directory:
            self.extractor.increment_modifications()

    def on_moved(self, event):
        if not event.is_directory:
            self.extractor.increment_renames()

    def on_created(self, event):
        if not event.is_directory:
            self.extractor.increment_creations()

def start_monitoring():
    # Ensure folder exists
    MONITOR_PATH.mkdir(parents=True, exist_ok=True)

    extractor = FeatureExtractor()
    event_handler = FileMonitorHandler(extractor)

    observer = Observer()
    observer.schedule(event_handler, str(MONITOR_PATH), recursive=True)
    observer.start()

    try:
        while True:
            extractor.update_system_metrics()
            features = extractor.generate_feature_snapshot()
            print(features)
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_monitoring()