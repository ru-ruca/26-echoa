"""s08: 외부 AI 교차 검토(verdict) 병합 — C-1 최종본 확정.

적용 규칙 (output/external_review/c1_external_verdict.jsonl, 2026-07-31):
    pick == "alternative"  → 검수자 대안으로 교체 (fix보다 우선)
    verdict == "fix"       → 외부 수정문(fixed_en/kr) 적용
    그 외                  → 채택본 유지

산출물: output/c1_final.jsonl (27건 — echoa DB 적재 대기 최종본)

사용: uv run python -m src.steps.s08_external c1
"""
from __future__ import annotations

import sys
from pathlib import Path

from src.lib.jsonl import read_jsonl, write_jsonl

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"


def main(mode: str = "c1") -> None:
    if mode != "c1":
        raise SystemExit(f"mode '{mode}'는 아직 미구현")

    adopted = read_jsonl(OUTPUT_DIR / "c1_adopted.jsonl")
    alts = {a["seed_id"]: a for a in read_jsonl(OUTPUT_DIR / "c1_alternatives.jsonl")}
    verdicts = {
        v["id"]: v
        for v in read_jsonl(OUTPUT_DIR / "external_review" / "c1_external_verdict.jsonl")
        if v["type"] == "adopted"
    }
    # 쌍(pick) 일관성 검증 — adopted/alternative 두 줄의 pick이 다르면 사람이 봐야 한다
    alt_picks = {
        v["id"]: v["pick"]
        for v in read_jsonl(OUTPUT_DIR / "external_review" / "c1_external_verdict.jsonl")
        if v["type"] == "alternative"
    }
    for seed_id, pick in alt_picks.items():
        if verdicts[seed_id]["pick"] != pick:
            raise SystemExit(f"{seed_id}: pick 불일치 (adopted={verdicts[seed_id]['pick']}, alt={pick}) — 수동 확인 필요")

    final, applied = [], {"alternative": 0, "fixed": 0, "kept": 0}
    for row in adopted:
        v = verdicts[row["seed_id"]]
        out = dict(row)
        if v.get("pick") == "alternative":
            alt = alts[row["seed_id"]]
            out["text_en"], out["text_kr"] = alt["text_en"], alt["text_kr"]
            out["source_cand"] = "reviewer_alternative"
            action = "alternative"
        elif v["verdict"] == "fix":
            out["text_en"], out["text_kr"] = v["fixed_en"], v["fixed_kr"]
            action = "fixed"
        else:
            action = "kept"
        out["review"] = row["review"] | {
            "external": {"verdict": v["verdict"], "issue": v["issue"], "applied": action, "reviewed_at": "2026-07-31"}
        }
        applied[action] += 1
        final.append(out)

    n = write_jsonl(OUTPUT_DIR / "c1_final.jsonl", final)
    print(f"output/c1_final.jsonl  {n}건 — 유지 {applied['kept']} / 외부수정 {applied['fixed']} / 대안교체 {applied['alternative']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c1")
