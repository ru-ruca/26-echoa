"""s04: 1단 하드필터 (23 §4) — Phase 1은 C-1 모드.

검사 (후보별, 통과/탈락):
    too_similar_to_seed   씨앗 유사도 상한 — 저작권. 표현 대체가 불충분하면 탈락
    near_duplicate_db     기존 커리큘럼 전체(3,622)와 근접 중복 (자기 씨앗 제외)
    near_duplicate_batch  같은 배치의 앞선 통과 후보와 근접 중복
    vocab_extended        extended 허용 목록 밖 content lemma ≥ 1
    vocab_core_p90        core 밖 content lemma > 2 (baseline p90 — s02 리포트)

임계값은 시작값이며, 산출 리포트의 분포를 보고 조정한다 (23 §9).

사용: uv run python -m src.steps.s04_gate_hard c1
"""
from __future__ import annotations

import json
import sys
from statistics import mean

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl
from src.lib.similarity import jaccard, ratio, similarity
from src.lib.textproc import content_lemmas

# 씨앗 유사도 상한 (C-1: 원문과 "달라야" 통과)
SEED_JACCARD_MAX = 0.55
SEED_RATIO_MAX = 0.65
# 근접 중복 (생성물 간·기존 DB와)
DUP_RATIO = 0.85
DUP_PREFILTER_JACCARD = 0.4  # 이 미만이면 ratio 계산 생략 (성능)
# 어휘
CORE_EXCESS_MAX = 2


def load_allowlist() -> tuple[set[str], set[str]]:
    data = json.loads((WORK_DIR / "allowlist_m01_03.json").read_text(encoding="utf-8"))
    core = set(data["core"])
    extended = core | set(data["extended_extra"])
    return core, extended


def check_c1(cand: dict, seed_text: str, db_rows: list[dict], passed_texts: list[str],
             core: set[str], extended: set[str]) -> dict:
    text = cand["text_en"]
    fails: list[str] = []

    seed_sim = similarity(text, seed_text)
    if seed_sim["jaccard"] >= SEED_JACCARD_MAX or seed_sim["ratio"] >= SEED_RATIO_MAX:
        fails.append("too_similar_to_seed")

    max_db = {"id": None, "ratio": 0.0}
    for row in db_rows:
        if jaccard(text, row["text_en"]) < DUP_PREFILTER_JACCARD:
            continue
        r = ratio(text, row["text_en"])
        if r > max_db["ratio"]:
            max_db = {"id": row["id"], "ratio": round(r, 3)}
    if max_db["ratio"] >= DUP_RATIO:
        fails.append("near_duplicate_db")

    for prev in passed_texts:
        if jaccard(text, prev) >= DUP_PREFILTER_JACCARD and ratio(text, prev) >= DUP_RATIO:
            fails.append("near_duplicate_batch")
            break

    lemmas = content_lemmas(text)
    ext_excess = [lm for lm in lemmas if lm not in extended]
    core_excess = [lm for lm in lemmas if lm not in core]
    if ext_excess:
        fails.append("vocab_extended")
    if len(core_excess) > CORE_EXCESS_MAX:
        fails.append("vocab_core_p90")

    return {
        "pass": not fails,
        "fails": fails,
        "seed_sim": seed_sim,
        "max_db_sim": max_db,
        "vocab": {"extended_excess": ext_excess, "core_excess": core_excess},
    }


def main(mode: str = "c1") -> None:
    if mode != "c1":
        raise SystemExit(f"mode '{mode}'는 아직 미구현 — Phase 2에서 c2 추가")

    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "seeds_m01_03.jsonl")}
    candidates = read_jsonl(WORK_DIR / "c1_candidates.jsonl")
    core, extended = load_allowlist()
    # 자기 씨앗은 seed_sim이 담당하므로 DB 중복 검사에서 제외
    db_all = read_jsonl(WORK_DIR / "sentences_all.jsonl")

    results = []
    passed_texts: list[str] = []
    for cand in candidates:
        seed = seeds[cand["seed_id"]]
        db_rows = [r for r in db_all if r["id"] != cand["seed_id"]]
        gate = check_c1(cand, seed["text_en"], db_rows, passed_texts, core, extended)
        if gate["pass"]:
            passed_texts.append(cand["text_en"])
        results.append(cand | {"gate": gate})

    write_jsonl(WORK_DIR / "c1_candidates_gated.jsonl", results)

    n_pass = sum(1 for r in results if r["gate"]["pass"])
    seed_ratios = [r["gate"]["seed_sim"]["ratio"] for r in results]
    seed_jacs = [r["gate"]["seed_sim"]["jaccard"] for r in results]
    fail_counts: dict[str, int] = {}
    for r in results:
        for f in r["gate"]["fails"]:
            fail_counts[f] = fail_counts.get(f, 0) + 1

    print(f"후보 {len(results)} → 통과 {n_pass} ({n_pass / len(results):.0%})")
    print(f"탈락 사유: {fail_counts or '없음'}")
    print(f"씨앗 유사도 분포 — ratio 평균 {mean(seed_ratios):.2f} 최대 {max(seed_ratios):.2f} / "
          f"jaccard 평균 {mean(seed_jacs):.2f} 최대 {max(seed_jacs):.2f}")
    print(f"임계값: seed jaccard<{SEED_JACCARD_MAX} & ratio<{SEED_RATIO_MAX}, "
          f"dup ratio<{DUP_RATIO}, core 초과≤{CORE_EXCESS_MAX}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c1")
