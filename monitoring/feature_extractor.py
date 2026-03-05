from threading import Lock
import psutil


class FeatureExtractor:
    def __init__(self):
        self._lock = Lock()

        self.file_modifications = 0
        self.renames = 0
        self.creations = 0
        self.deletions = 0

        self.last_process_count = len(psutil.pids())
        self.cpu_usage = 0.0
        self.memory_usage = psutil.virtual_memory().percent
        self.process_spike = 0

        # warm-up for cpu_percent(None)
        psutil.cpu_percent(interval=None)

    def increment_modifications(self):
        with self._lock:
            self.file_modifications += 1

    def increment_renames(self):
        with self._lock:
            self.renames += 1

    def increment_creations(self):
        with self._lock:
            self.creations += 1

    def increment_deletions(self):
        with self._lock:
            self.deletions += 1

    def update_system_metrics(self):
        self.cpu_usage = psutil.cpu_percent(interval=None)
        self.memory_usage = psutil.virtual_memory().percent

        current_process_count = len(psutil.pids())
        self.process_spike = current_process_count - self.last_process_count
        self.last_process_count = current_process_count

    def generate_feature_snapshot(self):
        with self._lock:
            snapshot = {
                "file_modification_rate": self.file_modifications,
                "rename_count": self.renames,
                "file_creation_count": self.creations,
                "file_deletion_count": self.deletions,
                "cpu_usage_percent": self.cpu_usage,
                "memory_usage_percent": self.memory_usage,
                "process_spike": self.process_spike,
            }

            # window reset
            self.file_modifications = 0
            self.renames = 0
            self.creations = 0
            self.deletions = 0

        return snapshot