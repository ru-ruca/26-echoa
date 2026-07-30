"""JSONL 입출력 공통 — 모든 단계 산출물은 JSONL로 주고받는다."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

WORK_DIR = Path(__file__).resolve().parents[2] / "data" / "work"
REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
