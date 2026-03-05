from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from monitoring.feature_extractor import FeatureExtractor
from monitoring.metrics_logger import append_csv, append_jsonl, write_latest_json

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # ...\RANZR
MONITOR_PATH = PROJECT_ROOT / "test_folder"

LOG_DIR = PROJECT_ROOT / "logs"
JSONL_PATH = LOG_DIR / "features.jsonl"
CSV_PATH = LOG_DIR / "features.csv"
EVENTS_JSONL_PATH = LOG_DIR / "events.jsonl"
SYSTEM_METRICS_JSON_PATH = LOG_DIR / "system_metrics.json"  # stable "latest snapshot"

DATA_DIR = PROJECT_ROOT / "data"
BASELINE_CSV_PATH = DATA_DIR / "normal_behavior.csv"

CSV_FIELDNAMES = [
    "ts",
    "ts_iso_utc",
    "window_seconds",
    "file_modification_rate",
    "rename_count",
    "file_creation_count",
    "file_deletion_count",
    "cpu_usage_percent",
    "memory_usage_percent",
    "process_spike",
]

BASELINE_FIELDNAMES = [
    "file_modification_rate",
    "rename_count",
    "cpu_usage_percent",
    "memory_usage_percent",
    "process_spike",
]

# Demo thresholds (tune later)
SUSPICIOUS_FILE_MOD_RATE = 30
SUSPICIOUS_CPU_PERCENT = 80.0


def _log_event(event_type: str, src: str | None = None, dest: str | None = None) -> None:
    entry = {
        "ts": time.time(),
        "ts_iso_utc": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "src": src,
        "dest": dest,
    }
    print("EVENT:", entry)
    append_jsonl(EVENTS_JSONL_PATH, entry)


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, extractor: FeatureExtractor):
        self.extractor = extractor

    def on_modified(self, event):
        if not event.is_directory:
            _log_event("modified", src=getattr(event, "src_path", None))
            self.extractor.increment_modifications()

    def on_moved(self, event):
        if not event.is_directory:
            _log_event(
                "moved",
                src=getattr(event, "src_path", None),
                dest=getattr(event, "dest_path", None),
            )
            self.extractor.increment_renames()

    def on_created(self, event):
        if not event.is_directory:
            _log_event("created", src=getattr(event, "src_path", None))
            self.extractor.increment_creations()

    def on_deleted(self, event):
        if not event.is_directory:
            _log_event("deleted", src=getattr(event, "src_path", None))
            self.extractor.increment_deletions()


def start_monitoring(
    poll_seconds: int = 5,
    log_jsonl: bool = True,
    log_csv: bool = True,
    collect_baseline: bool = False,
) -> None:
    MONITOR_PATH.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    extractor = FeatureExtractor()
    handler = FileMonitorHandler(extractor)

    observer = Observer()
    observer.schedule(handler, str(MONITOR_PATH), recursive=True)

    extractor.update_system_metrics()
    time.sleep(0.2)

    observer.start()
    try:
        while True:
            extractor.update_system_metrics()
            snapshot = extractor.generate_feature_snapshot()

            row = {
                "ts": time.time(),
                "ts_iso_utc": datetime.now(timezone.utc).isoformat(),
                "window_seconds": poll_seconds,
                **snapshot,
            }

            # Stable JSON for other modules (AI/Dashboard) to read
            write_latest_json(SYSTEM_METRICS_JSON_PATH, row)

            # Console
            print("SNAPSHOT:", row)

            # Demo threshold alerts (pre-AI)
            if (
                row.get("file_modification_rate", 0) > SUSPICIOUS_FILE_MOD_RATE
                and row.get("cpu_usage_percent", 0.0) > SUSPICIOUS_CPU_PERCENT
            ):
                print("SUSPICIOUS: threshold triggered")

            # Logs
            if log_jsonl:
                append_jsonl(JSONL_PATH, row)
            if log_csv:
                append_csv(CSV_PATH, CSV_FIELDNAMES, row)

            # Baseline dataset (normal behavior)
            if collect_baseline:
                append_csv(BASELINE_CSV_PATH, BASELINE_FIELDNAMES, row)

            time.sleep(poll_seconds)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    # set collect_baseline=True when you want 15–30 min normal usage dataset
    start_monitoring(collect_baseline=True)