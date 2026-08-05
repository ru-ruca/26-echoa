"""s04b: C-3 대화 하드필터 — 대화 단위 검사 (23 §4).

c1/c2는 문장 단위라 s04가 담당하고, c3는 턴 배열이 검사 대상이라 분리했다.

검사:
    seed_missing      씨앗 문장이 B 발화로 그대로 있는가 (변형 금지)
    seed_turn_wrong   seed_turn 인덱스가 실제 위치와 맞는가
    turn_count        2~6턴 (23 §3 상한)
    speaker_alt       A/B 교대 위반 (같은 화자 연속)
    seed_not_b        씨앗이 B가 아닌 화자에 배치됨
    turn_too_long     한 턴이 12단어 초과 (A1 이탈)
    length_creep      뒤 턴이 앞 턴보다 크게 길어짐 (난이도 상승 신호)
    vocab_extended    허용 목록 밖 content lemma가 대화 전체에서 3개 이상
    near_duplicate_db 기존 커리큘럼 문장과 근접 중복인 턴
    empty_dialogue    생성 거부(turns=[]) — 탈락이 아니라 별도 집계

사용: uv run python -m src.steps.s04b_gate_c3 [입력.jsonl 출력.jsonl]
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl
from src.lib.similarity import jaccard, ratio, tokens
from src.lib.textproc import content_lemmas
from src.steps.s04_gate_hard import DUP_PREFILTER_JACCARD, load_allowlist

MIN_TURNS, MAX_TURNS = 2, 6
MAX_WORDS_PER_TURN = 12
LENGTH_CREEP_RATIO = 1.8  # 마지막 턴이 첫 턴의 이 배를 넘으면 난이도 상승 신호
VOCAB_EXCESS_MAX = 2  # 대화 전체 기준 (23 §3: 문장당이 아니라 대화당)
DUP_RATIO = 0.92


def check(dlg: dict, seed_text: str, db_index) -> dict:
    fails: list[str] = []
    turns = dlg.get("turns") or []

    if not turns:
        return {"pass": False, "fails": ["empty_dialogue"], "note": dlg.get("note", ""), "n_turns": 0}

    if not MIN_TURNS <= len(turns) <= MAX_TURNS:
        fails.append("turn_count")

    speakers = [t.get("speaker") for t in turns]
    if any(a == b for a, b in zip(speakers, speakers[1:])):
        fails.append("speaker_alt")

    # 씨앗 보존 — 토큰 정규화 후 완전 일치를 요구한다 (구두점·대소문자만 관용)
    norm_seed = " ".join(tokens(seed_text))
    matches = [i for i, t in enumerate(turns, 1) if " ".join(tokens(t.get("text_en", ""))) == norm_seed]
    if not matches:
        fails.append("seed_missing")
    else:
        if dlg.get("seed_turn") not in matches:
            fails.append("seed_turn_wrong")
        if all(turns[i - 1].get("speaker") != "B" for i in matches):
            fails.append("seed_not_b")

    lengths = [len(tokens(t.get("text_en", ""))) for t in turns]
    if any(n > MAX_WORDS_PER_TURN for n in lengths):
        fails.append("turn_too_long")
    if lengths and lengths[-1] > max(3, lengths[0]) * LENGTH_CREEP_RATIO:
        fails.append("length_creep")

    core, extended = load_allowlist()
    all_lemmas = [lm for t in turns for lm in content_lemmas(t.get("text_en", ""))]
    ext_excess = sorted({lm for lm in all_lemmas if lm not in extended})
    if len(ext_excess) > VOCAB_EXCESS_MAX:
        fails.append("vocab_extended")

    dup = {"turn": None, "id": None, "ratio": 0.0}
    for i, t in enumerate(turns, 1):
        text = t.get("text_en", "")
        if " ".join(tokens(text)) == norm_seed:
            continue  # 씨앗 턴은 원문과 같은 게 정상
        tok = set(tokens(text))
        for rid, rtext, rtok in db_index:
            if not tok or len(tok & rtok) / len(tok | rtok) < DUP_PREFILTER_JACCARD:
                continue
            r = ratio(text, rtext)
            if r > dup["ratio"]:
                dup = {"turn": i, "id": rid, "ratio": round(r, 3)}
    if dup["ratio"] >= DUP_RATIO:
        fails.append("near_duplicate_db")

    return {
        "pass": not fails,
        "fails": fails,
        "n_turns": len(turns),
        "turn_lengths": lengths,
        "vocab_excess": ext_excess,
        "max_db_sim": dup,
    }


def main(in_path: str | None = None, out_path: str | None = None) -> None:
    src = Path(in_path) if in_path else WORK_DIR / "c3_candidates.jsonl"
    dst = Path(out_path) if out_path else WORK_DIR / "c3_candidates_gated.jsonl"

    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c3_seeds.jsonl")}
    dialogues = read_jsonl(src)
    db_index = [
        (r["id"], r["text_en"], set(tokens(r["text_en"])))
        for r in read_jsonl(WORK_DIR / "sentences_all.jsonl")
    ]

    results = []
    for dlg in dialogues:
        seed = seeds[dlg["seed_id"]]
        results.append(dlg | {"group": seed["group"], "gate": check(dlg, seed["text_en"], db_index)})
    write_jsonl(dst, results)

    n_pass = sum(1 for r in results if r["gate"]["pass"])
    empty = sum(1 for r in results if "empty_dialogue" in r["gate"]["fails"])
    fail_counts = Counter(f for r in results for f in r["gate"]["fails"])
    by_group = Counter(r["group"] for r in results if r["gate"]["pass"])
    print(f"[c3] 대화 {len(results)} → 통과 {n_pass} ({n_pass / len(results):.0%}) · 생성거부 {empty}")
    print(f"탈락 사유: {dict(fail_counts) or '없음'}")
    print(f"그룹별 통과: {dict(by_group)}")


if __name__ == "__main__":
    main(
        sys.argv[1] if len(sys.argv) > 1 else None,
        sys.argv[2] if len(sys.argv) > 2 else None,
    )
