# Cyber Module Status (Monitoring / Logging / Baseline)

## Done
- File system monitoring on `RANZR/test_folder/` (create/modify/rename/delete)
- Rename captured as `moved` event (src -> dest)
- Per-event logging: `logs/events.jsonl`
- Windowed feature snapshots (default 5s)
- Snapshot logging:
  - `logs/features.csv` (history)
  - `logs/features.jsonl` (history, optional)
  - `logs/system_metrics.json` (latest snapshot only)
- Baseline dataset generation:
  - `data/normal_behavior.csv`

## Outputs to share (AI-ready)
- `data/normal_behavior.csv`
- `logs/system_metrics.json`
- `logs/features.csv`
- `logs/events.jsonl`

## How to validate quickly
1) Run monitor:
   - `python -m monitoring.file_monitor`
2) Generate rename:
   - create `a.txt` then rename to `b.txt`
3) Confirm:
   - `events.jsonl` contains `"type": "moved"`
   - next snapshot window shows `rename_count > 0`

## Remaining (optional enhancements)
- CLI flags: `--baseline`, `--poll-seconds`, `--path`
- Debounce repeated `modified` events (reduce noise)
- Threshold tuning from baseline percentiles