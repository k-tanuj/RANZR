# Cyber Module (Monitoring + Baseline Data)

This folder documents the **cyber monitoring** part that was implemented:
- File system behavior monitoring (create/modify/rename/delete) on a target folder
- System metrics sampling (CPU, memory, process count changes)
- Stable logs for AI-ready consumption
- Baseline dataset generation for normal behavior

---

## What was built (Cyber scope)

### 1) File activity monitoring (Watchdog)
Tracks file events inside:
- `RANZR/test_folder/`

Event types:
- `created`  → file created
- `modified` → file content changed
- `moved`    → **rename** (Windows reports rename as moved: src → dest)
- `deleted`  → file deleted

Per-event logs:
- `logs/events.jsonl`

### 2) Feature snapshots (windowed metrics)
Every `window_seconds` (default 5 seconds) a snapshot is produced and counters reset.

Snapshot fields:
- `file_modification_rate`
- `rename_count`
- `file_creation_count`
- `file_deletion_count`
- `cpu_usage_percent`
- `memory_usage_percent`
- `process_spike`

Snapshot logs:
- `logs/features.csv` (history)
- `logs/features.jsonl` (history, if enabled)
- `logs/system_metrics.json` (**latest snapshot only**, overwritten each window)

### 3) Baseline dataset for AI training
While monitoring is running with baseline enabled, it writes:
- `data/normal_behavior.csv`

Columns (training-ready):
- `file_modification_rate`
- `rename_count`
- `cpu_usage_percent`
- `memory_usage_percent`
- `process_spike`

---

## Install (Windows / venv recommended)

From project root `D:\RANZR-main\RANZR`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\cyber\requirements.txt
```

---

## Run monitoring

From project root:

```powershell
cd D:\RANZR-main\RANZR
python -m monitoring.file_monitor
```

Stop:
- Press `Ctrl + C` in the running terminal.

---

## Rename test (should increment rename_count)
While monitor is running, in another terminal:

```powershell
cd D:\RANZR-main\RANZR
"hi" | Out-File .\test_folder\a.txt -Force
Remove-Item .\test_folder\b.txt -ErrorAction SilentlyContinue
Rename-Item .\test_folder\a.txt -NewName b.txt
```

Expected:
- `logs/events.jsonl` includes a line:
  - `"type": "moved", "src": "...a.txt", "dest": "...b.txt"`
- next window in `logs/features.csv` shows:
  - `rename_count > 0`

---

## Baseline collection (normal behavior)
Enable baseline mode in `monitoring/file_monitor.py` (collect_baseline=True) and run for 15–30 minutes.

Verify baseline file is growing:
```powershell
cd D:\RANZR-main\RANZR
Get-Content .\data\normal_behavior.csv -Tail 10
```

Recommended baseline size with `window_seconds=5`:
- 15 minutes ≈ 180 rows
- 30 minutes ≈ 360 rows

---

## Outputs (Cyber deliverables)
- `data/normal_behavior.csv` (baseline dataset)
- `logs/features.csv` (feature history)
- `logs/events.jsonl` (per-event trace)
- `logs/system_metrics.json` (stable latest snapshot feed)

---