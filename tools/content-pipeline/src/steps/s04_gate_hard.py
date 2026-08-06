"""s04: 1단 하드필터 (23 §4) — c1(재작성)·c2(패턴 변형) 모드.

공통 검사: 근접 중복(기존 DB·배치 내), 어휘(extended 초과 0 / core 초과 ≤ p90).
모드별 검사:
    c1  too_similar_to_seed — 씨앗 유사도 **상한** (저작권: 표현 대체가 불충분하면 탈락)
    c2  pattern_broken      — 패턴 고정부가 씨앗·후보 모두에 순서대로 존재해야 함
        seed_identical      — 슬롯까지 씨앗과 사실상 같으면 변형이 아님
        (C-2는 구조 공유가 정상이라 중복 임계를 0.85→0.92로 상향)

임계값은 시작값이며 산출 분포를 보고 조정한다 (23 §9).

사용: uv run python -m src.steps.s04_gate_hard c1|c2 [입력.jsonl 출력.jsonl]
     기본 입출력 — c1: c1_candidates.jsonl → c1_candidates_gated.jsonl
                  c2: c2_candidates.jsonl → c2_candidates_gated.jsonl
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from statistics import mean

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl
from src.lib.similarity import ratio, similarity, tokens
from src.lib.textproc import content_lemmas

# 씨앗 유사도 상한 (c1: 원문과 "달라야" 통과)
SEED_JACCARD_MAX = 0.55
SEED_RATIO_MAX = 0.65
# 근접 중복
DUP_RATIO = {"c1": 0.85, "c2": 0.92}
SEED_IDENTICAL_RATIO = 0.92  # c2: 씨앗과 사실상 동일한 변형
DUP_PREFILTER_JACCARD = 0.4  # 이 미만이면 ratio 계산 생략 (성능)
# 어휘
CORE_EXCESS_MAX = 2


def load_allowlist() -> tuple[set[str], set[str]]:
    data = json.loads((WORK_DIR / "allowlist_m01_03.json").read_text(encoding="utf-8"))
    core = set(data["core"])
    extended = core | set(data["extended_extra"])
    out_dir = WORK_DIR.parents[1] / "output"
    # 인간 검수에서 승인된 어휘(누적) — 검수가 최종 게이트라는 원칙의 반영
    approved_file = out_dir / "allowlist_human_approved.json"
    if approved_file.exists():
        approved = json.loads(approved_file.read_text(encoding="utf-8"))
        extended |= {w["lemma"] for w in approved["words"]}
    # year1 커리큘럼 실등장 어휘 — 전 문장이 A1 라벨이라 A1 적정으로 본다 (s13)
    expanded_file = out_dir / "allowlist_a1_expanded.json"
    if expanded_file.exists():
        expanded = json.loads(expanded_file.read_text(encoding="utf-8"))
        extended |= set(expanded["lemmas"])
    return core, extended


def jaccard_sets(sa: set[str], sb: set[str]) -> float:
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def max_dup(text: str, tok: set[str], rows: list[tuple[str, str, set[str]]]) -> dict:
    """rows: (id, text, token_set). jaccard 프리필터 후 ratio 최대치."""
    best = {"id": None, "ratio": 0.0}
    for rid, rtext, rtok in rows:
        if jaccard_sets(tok, rtok) < DUP_PREFILTER_JACCARD:
            continue
        r = ratio(text, rtext)
        if r > best["ratio"]:
            best = {"id": rid, "ratio": round(r, 3)}
    return best


def vocab_check(text: str, core: set[str], extended: set[str]) -> tuple[list[str], list[str]]:
    lemmas = content_lemmas(text)
    return (
        [lm for lm in lemmas if lm not in extended],
        [lm for lm in lemmas if lm not in core],
    )


def normalize(text: str) -> str:
    return " ".join(tokens(text))


def fixed_segments(pattern: str) -> list[str]:
    """패턴에서 슬롯([VERB-PHRASE] 등)을 뺀 고정부 세그먼트(정규화)."""
    parts = re.split(r"\[[A-Z][A-Z0-9-]*\]", pattern)
    return [normalize(p) for p in parts if normalize(p)]


def contains_in_order(text: str, segments: list[str]) -> bool:
    t = normalize(text)
    pos = 0
    for seg in segments:
        i = t.find(seg, pos)
        if i < 0:
            return False
        pos = i + len(seg)
    return True


def check_common(cand: dict, db_rows, batch_rows, core, extended, dup_ratio: float) -> tuple[list[str], dict]:
    text = cand["text_en"]
    tok = set(tokens(text))
    fails: list[str] = []

    db_best = max_dup(text, tok, db_rows)
    if db_best["ratio"] >= dup_ratio:
        fails.append("near_duplicate_db")
    batch_best = max_dup(text, tok, batch_rows)
    if batch_best["ratio"] >= dup_ratio:
        fails.append("near_duplicate_batch")

    ext_excess, core_excess = vocab_check(text, core, extended)
    if ext_excess:
        fails.append("vocab_extended")
    if len(core_excess) > CORE_EXCESS_MAX:
        fails.append("vocab_core_p90")

    detail = {
        "max_db_sim": db_best,
        "vocab": {"extended_excess": ext_excess, "core_excess": core_excess},
    }
    return fails, detail


def main(mode: str = "c1", in_path: str | None = None, out_path: str | None = None) -> None:
    if mode not in ("c1", "c2"):
        raise SystemExit(f"mode '{mode}' 미지원 (c1|c2)")

    src = Path(in_path) if in_path else WORK_DIR / f"{mode}_candidates.jsonl"
    dst = Path(out_path) if out_path else WORK_DIR / f"{mode}_candidates_gated.jsonl"

    seeds_file = "c2_seeds.jsonl" if mode == "c2" else "seeds_m01_03.jsonl"
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / seeds_file)}
    candidates = read_jsonl(src)
    core, extended = load_allowlist()
    db_index = [
        (r["id"], r["text_en"], set(tokens(r["text_en"])))
        for r in read_jsonl(WORK_DIR / "sentences_all.jsonl")
    ]

    results = []
    batch_rows: list[tuple[str, str, set[str]]] = []
    for cand in candidates:
        seed = seeds[cand["seed_id"]]
        db_rows = [r for r in db_index if r[0] != cand["seed_id"]]
        fails, detail = check_common(cand, db_rows, batch_rows, core, extended, DUP_RATIO[mode])

        if mode == "c1":
            seed_sim = similarity(cand["text_en"], seed["text_en"])
            if seed_sim["jaccard"] >= SEED_JACCARD_MAX or seed_sim["ratio"] >= SEED_RATIO_MAX:
                fails.append("too_similar_to_seed")
            detail["seed_sim"] = seed_sim
        else:  # c2
            segs = fixed_segments(cand.get("pattern", ""))
            pattern_ok = bool(segs) and contains_in_order(cand["text_en"], segs) and contains_in_order(
                seed["text_en"], segs
            )
            if not pattern_ok:
                fails.append("pattern_broken")
            seed_r = ratio(cand["text_en"], seed["text_en"])
            if seed_r >= SEED_IDENTICAL_RATIO:
                fails.append("seed_identical")
            detail["pattern_ok"] = pattern_ok
            detail["seed_ratio"] = round(seed_r, 3)

        gate = {"pass": not fails, "fails": fails} | detail
        if gate["pass"]:
            cand_no = cand.get("cand", cand.get("source_cand", ""))
            batch_rows.append((f"{cand['seed_id']}#{cand_no}", cand["text_en"], set(tokens(cand["text_en"]))))
        results.append(cand | {"gate": gate})

    write_jsonl(dst, results)

    n_pass = sum(1 for r in results if r["gate"]["pass"])
    fail_counts: dict[str, int] = {}
    for r in results:
        for f in r["gate"]["fails"]:
            fail_counts[f] = fail_counts.get(f, 0) + 1
    print(f"[{mode}] 후보 {len(results)} → 통과 {n_pass} ({n_pass / len(results):.0%})")
    print(f"탈락 사유: {fail_counts or '없음'}")
    if mode == "c1":
        seed_ratios = [r["gate"]["seed_sim"]["ratio"] for r in results]
        print(f"씨앗 유사도 — ratio 평균 {mean(seed_ratios):.2f} 최대 {max(seed_ratios):.2f} (상한 {SEED_RATIO_MAX})")
    else:
        seed_ratios = [r["gate"]["seed_ratio"] for r in results]
        print(f"씨앗 ratio 분포 — 평균 {mean(seed_ratios):.2f} 최대 {max(seed_ratios):.2f} (동일 판정 ≥{SEED_IDENTICAL_RATIO})")


if __name__ == "__main__":
    main(
        sys.argv[1] if len(sys.argv) > 1 else "c1",
        sys.argv[2] if len(sys.argv) > 2 else None,
        sys.argv[3] if len(sys.argv) > 3 else None,
    )
