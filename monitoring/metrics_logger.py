from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Iterable


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_latest_json(path: Path, row: dict) -> None:
    """
    Writes a single JSON object (overwrites file). Useful as a stable, always-up-to-date
    file for dashboards/other modules to read.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _ensure_csv_schema(path: Path, fieldnames: list[str]) -> None:
    if not path.exists() or path.stat().st_size == 0:
        return

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        existing_header = next(reader, [])

    if existing_header and existing_header != fieldnames:
        rotated = path.with_name(f"{path.stem}.old_{int(time.time())}{path.suffix}")
        path.rename(rotated)


def append_csv(path: Path, fieldnames: list[str], row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _ensure_csv_schema(path, fieldnames)

    write_header = (not path.exists()) or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)