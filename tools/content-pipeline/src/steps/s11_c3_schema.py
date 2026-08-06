"""s11: C-3 대화를 기존 conversation 스키마로 변환·검증 (23 §3 "새 스키마를 만들지 않는다").

기존 라이브 스키마(sentences 테이블, day_type='conversation')의 대화 표현:
    id                M01_D01_L01   — M{month}_D{dialogue}_L{line}
    dialogue_id       DLG_M01_001
    speaker           Alex / Sam    — 실제 이름 (A/B가 아님)
    dialogue_title    First Meeting
    dialogue_situation
    text_en / text_kr / month / week / day / cefr_level

변환 규칙:
    - 씨앗 id(M01_008)의 month를 상속하고, 대화 번호는 파일럿 구간(101~)으로 신규 발번해
      기존 DLG_M01_001~002와 충돌하지 않게 한다.
    - speaker A/B는 대화별로 이름 쌍을 배정한다 (기존 자산이 실제 이름을 쓰므로).
    - week/day는 씨앗 것을 상속한다 (같은 주차 학습 자료로 붙는다).

검증:
    id_collision      기존 sentences.id와 충돌
    dialogue_collision 기존 dialogue_id와 충돌
    field_missing     스키마 필수 필드 누락
    field_overflow    스키마에 없는 필드 사용

산출물: output/c3_rows_preview.jsonl (적재 대상 행 — 실제 INSERT는 하지 않는다)

사용: uv run python -m src.steps.s11_c3_schema [입력.jsonl]
"""
from __future__ import annotations

import sys
from pathlib import Path

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

# 라이브 sentences 스키마의 대화 관련 컬럼 (survey 2026-07-30 기준)
SCHEMA_FIELDS = {
    "id", "month", "week", "day", "day_type", "text_en", "text_kr", "cefr_level",
    "source_id", "is_new", "original_id", "notes", "stress_pattern", "audio_url",
    "chunk_breaks", "speaking_duration_sec", "intonation_pattern_id",
    "dialogue_id", "speaker", "dialogue_title", "dialogue_situation", "created_at",
}
REQUIRED = {"id", "month", "week", "day", "day_type", "text_en", "text_kr",
            "dialogue_id", "speaker", "dialogue_title"}

# 파일럿 대화 번호 시작점 — 기존 DLG_M01_001·002와 충돌 회피
DIALOGUE_NO_BASE = 101
NAME_PAIRS = [("Mina", "Jun"), ("Sora", "Tae"), ("Yuna", "Ben"), ("Hana", "Leo"), ("Nara", "Kai")]


def to_rows(dlg: dict, seed: dict, dialogue_no: int) -> list[dict]:
    month = int(seed["id"][1:3])
    a_name, b_name = NAME_PAIRS[dialogue_no % len(NAME_PAIRS)]
    dialogue_id = f"DLG_M{month:02d}_{dialogue_no:03d}"
    rows = []
    for i, t in enumerate(dlg["turns"], 1):
        rows.append(
            {
                "id": f"M{month:02d}_D{dialogue_no:03d}_L{i:02d}",
                "month": month,
                "week": seed.get("week"),
                "day": seed.get("day"),
                "day_type": "conversation",
                "text_en": t["text_en"],
                "text_kr": t["text_kr"],
                "cefr_level": "A1",
                "dialogue_id": dialogue_id,
                "speaker": a_name if t["speaker"] == "A" else b_name,
                "dialogue_title": dlg["title"],
                "dialogue_situation": dlg["situation"],
                "notes": f"C-3 생성 (씨앗 {seed['id']}, {seed['group']})",
                "is_new": True,
            }
        )
    return rows


def main(in_path: str | None = None) -> None:
    src = Path(in_path) if in_path else WORK_DIR / "c3_candidates_gated.jsonl"
    # 게이트 산출물(gate 필드 있음)과 확정본(없음) 양쪽을 받는다
    dialogues = [d for d in read_jsonl(src) if d.get("gate", {}).get("pass", True)]
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c3_seeds.jsonl")}
    live = read_jsonl(WORK_DIR / "sentences_all.jsonl")
    live_ids = {r["id"] for r in live}

    all_rows, problems = [], []
    for n, dlg in enumerate(dialogues):
        seed = seeds[dlg["seed_id"]]
        rows = to_rows(dlg, seed, DIALOGUE_NO_BASE + n)
        for r in rows:
            if r["id"] in live_ids:
                problems.append(("id_collision", r["id"]))
            missing = REQUIRED - {k for k, v in r.items() if v is not None}
            if missing:
                problems.append(("field_missing", f"{r['id']}: {sorted(missing)}"))
            extra = set(r) - SCHEMA_FIELDS
            if extra:
                problems.append(("field_overflow", f"{r['id']}: {sorted(extra)}"))
        all_rows += rows

    live_dialogue_ids = {r.get("dialogue_id") for r in live if r.get("dialogue_id")}
    new_dialogue_ids = {r["dialogue_id"] for r in all_rows}
    for did in new_dialogue_ids & live_dialogue_ids:
        problems.append(("dialogue_collision", did))

    n = write_jsonl(OUTPUT_DIR / "c3_rows_preview.jsonl", all_rows)
    print(f"대화 {len(dialogues)}개 → 적재 행 {n}개 (대화 id {len(new_dialogue_ids)}개)")
    if problems:
        from collections import Counter

        print(f"⚠️  스키마 문제 {len(problems)}건: {dict(Counter(p[0] for p in problems))}")
        for p in problems[:10]:
            print(f"   {p[0]}: {p[1]}")
    else:
        print("스키마 검증 통과 — id·dialogue_id 충돌 없음, 필수 필드 충족, 스키마 외 필드 없음")
    print("※ 실제 INSERT는 하지 않는다. output/c3_rows_preview.jsonl 확인 후 적재 단계에서 사용.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
