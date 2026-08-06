"""s12: C-3 검수 회수 — 판정을 반영해 확정본을 만든다.

판정 반영 (reports/c3_review_sheet_filled.md):
    합격    그대로 채택
    수정    지정된 턴의 영어/한국어를 교체
    불합격  대화 제외

수정안 형식 (자유 서술이라 아래 패턴을 인식한다):
    N턴 X "영어" / KR "한국어"      영어+한국어 교체
    N턴 한국어 "한국어"             한국어만 교체
    여러 턴은 ` + `로 이어짐

산출물:
    output/c3_final.jsonl        확정 대화
    output/c3_rows_final.jsonl   적재 행 (기존 conversation 스키마)

사용: uv run python -m src.steps.s12_c3_adopt
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl, write_jsonl
from src.steps.s09b_verify_c3_review import classify, parse
from src.steps.s11_c3_schema import DIALOGUE_NO_BASE, to_rows

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
REVIEW_DATE = "2026-08-05"

# N턴 [화자] "영어" / KR "한국어"  |  N턴 한국어 "한국어"
FIX_BOTH = re.compile(r"(\d+)턴\s*[AB]?\s*[\"“]([^\"”]+)[\"”]\s*/\s*KR\s*[\"“]([^\"”]+)[\"”]")
FIX_KR = re.compile(r"(\d+)턴\s*한국어\s*[\"“]([^\"”]+)[\"”]")


def apply_fixes(turns: list[dict], verdict: str) -> tuple[list[dict], int]:
    turns = [dict(t) for t in turns]
    applied = 0
    for m in FIX_BOTH.finditer(verdict):
        i = int(m.group(1)) - 1
        if 0 <= i < len(turns):
            turns[i]["text_en"], turns[i]["text_kr"] = m.group(2).strip(), m.group(3).strip()
            applied += 1
    for m in FIX_KR.finditer(verdict):
        i = int(m.group(1)) - 1
        if 0 <= i < len(turns):
            turns[i]["text_kr"] = m.group(2).strip()
            applied += 1
    return turns, applied


def main() -> None:
    reviews = {r["seed_id"]: r for r in parse(REPORTS_DIR / "c3_review_sheet_filled.md")}
    gated = read_jsonl(WORK_DIR / "c3_candidates_gated.jsonl")
    judged = {j["seed_id"]: j for j in read_jsonl(WORK_DIR / "c3_judged.jsonl")}
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c3_seeds.jsonl")}

    final, actions, unparsed = [], Counter(), []
    for dlg in gated:
        sid = dlg["seed_id"]
        rev = reviews.get(sid)
        kind = classify(rev["verdict_raw"]) if rev else "미판정"
        actions[kind] += 1
        if kind in ("불합격", "미판정"):
            continue

        turns, n_fix = dlg["turns"], 0
        if kind == "수정":
            turns, n_fix = apply_fixes(dlg["turns"], rev["verdict_raw"])
            if n_fix == 0:
                unparsed.append((sid, rev["verdict_raw"][:80]))

        final.append(
            {
                "seed_id": sid,
                "group": seeds[sid]["group"],
                "title": dlg["title"],
                "situation": dlg["situation"],
                "seed_turn": dlg["seed_turn"],
                "turns": turns,
                "content_origin": "ai_generated",
                "review": {
                    "verdict": kind,
                    "turns_fixed": n_fix,
                    "judge_avg": judged[sid]["avg"],
                    "reviewed_at": REVIEW_DATE,
                },
                "gen_meta": dlg["gen_meta"] | {"adopted_at": str(date.today())},
            }
        )

    n = write_jsonl(OUTPUT_DIR / "c3_final.jsonl", final)

    rows = []
    for i, dlg in enumerate(final):
        rows += to_rows(dlg, seeds[dlg["seed_id"]], DIALOGUE_NO_BASE + i)
    n_rows = write_jsonl(OUTPUT_DIR / "c3_rows_final.jsonl", rows)

    grp = Counter(f["group"] for f in final)
    print(f"output/c3_final.jsonl      대화 {n}개 — {dict(actions)}")
    print(f"  그룹별: {dict(grp)} · 턴 수정 {sum(f['review']['turns_fixed'] for f in final)}건")
    print(f"output/c3_rows_final.jsonl  적재 행 {n_rows}개 (기존 conversation 스키마)")
    if unparsed:
        print(f"⚠️  수정안 파싱 실패 {len(unparsed)}건:")
        for sid, v in unparsed:
            print(f"   {sid}: {v}")


if __name__ == "__main__":
    main()
