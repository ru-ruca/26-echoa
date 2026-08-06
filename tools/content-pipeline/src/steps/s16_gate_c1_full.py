"""s16: C-1 확대 게이트 — 레벨별 허용 어휘로 검사한다.

파일럿 s04(c1)는 A1 고정이었다. 확대 대상은 A1~B2에 걸쳐 있어 씨앗의 CEFR에 맞는
허용 목록을 써야 한다 — 안 그러면 B2 문장이 A1 목록에 걸려 대량 탈락한다.

검사 항목은 s04(c1)와 같다: 씨앗 유사도 상한(저작권)·근접 중복·어휘.

사용: uv run python -m src.steps.s16_gate_c1_full <후보.jsonl> <출력.jsonl>
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from statistics import mean

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl
from src.lib.similarity import ratio, similarity, tokens
from src.steps.s04_gate_hard import (
    CORE_EXCESS_MAX,
    DUP_PREFILTER_JACCARD,
    DUP_RATIO,
    SEED_JACCARD_MAX,
    SEED_RATIO_MAX,
    jaccard_sets,
    load_allowlist,
    vocab_check,
)


def main(in_path: str, out_path: str) -> None:
    candidates = read_jsonl(Path(in_path))
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c1_rewrite_targets.jsonl")}
    db_index = [
        (r["id"], r["text_en"], set(tokens(r["text_en"])))
        for r in read_jsonl(WORK_DIR / "sentences_all.jsonl")
    ]
    allowlists = {lv: load_allowlist(lv) for lv in ("A1", "A2", "B1", "B2")}

    results, batch_rows = [], []
    for cand in candidates:
        seed = seeds[cand["seed_id"]]
        core, extended = allowlists.get(seed.get("cefr_level") or "A1", allowlists["A1"])
        text, tok = cand["text_en"], set(tokens(cand["text_en"]))
        fails = []

        seed_sim = similarity(text, seed["text_en"])
        if seed_sim["jaccard"] >= SEED_JACCARD_MAX or seed_sim["ratio"] >= SEED_RATIO_MAX:
            fails.append("too_similar_to_seed")

        best = {"id": None, "ratio": 0.0}
        for rid, rtext, rtok in db_index:
            if rid == cand["seed_id"] or jaccard_sets(tok, rtok) < DUP_PREFILTER_JACCARD:
                continue
            r = ratio(text, rtext)
            if r > best["ratio"]:
                best = {"id": rid, "ratio": round(r, 3)}
        if best["ratio"] >= DUP_RATIO["c1"]:
            fails.append("near_duplicate_db")

        for prev_text, prev_tok in batch_rows:
            if jaccard_sets(tok, prev_tok) >= DUP_PREFILTER_JACCARD and ratio(text, prev_text) >= DUP_RATIO["c1"]:
                fails.append("near_duplicate_batch")
                break

        ext_excess, core_excess = vocab_check(text, core, extended)
        if ext_excess:
            fails.append("vocab_level")
        if len(core_excess) > CORE_EXCESS_MAX:
            fails.append("vocab_core")

        gate = {
            "pass": not fails,
            "fails": fails,
            "cefr": seed.get("cefr_level"),
            "seed_sim": seed_sim,
            "max_db_sim": best,
            "vocab": {"level_excess": ext_excess},
        }
        if gate["pass"]:
            batch_rows.append((text, tok))
        results.append(cand | {"gate": gate})

    write_jsonl(Path(out_path), results)
    n_pass = sum(1 for r in results if r["gate"]["pass"])
    fail_counts = Counter(f for r in results for f in r["gate"]["fails"])
    by_cefr = Counter(r["gate"]["cefr"] for r in results if r["gate"]["pass"])
    ratios = [r["gate"]["seed_sim"]["ratio"] for r in results]
    print(f"[c1-full] 후보 {len(results)} → 통과 {n_pass} ({n_pass / len(results):.0%})")
    print(f"탈락 사유: {dict(fail_counts) or '없음'}")
    print(f"CEFR별 통과: {dict(by_cefr)}")
    print(f"씨앗 유사도 — ratio 평균 {mean(ratios):.2f} 최대 {max(ratios):.2f} (상한 {SEED_RATIO_MAX})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
