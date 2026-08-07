"""s19: C-1 확대 확정본 — 검수분과 미검수분을 합친다.

검수는 426씨앗 중 122개(저점·유사도 경계·샘플)만 봤다. 나머지 304개는 23 §4의
샘플 검수 원칙에 따라 채택하되, **어느 후보를 쓸지는 judge 최고점으로 정한다**.
미검수 씨앗은 전부 최고점이 4.0 이상이다(4.0 미만 씨앗은 전량 검수 대상이었다).

산출물:
    output/c1_full_final.jsonl        확정 (content_origin=ai_rewritten)
    output/c1_full_seed_defects.json  씨앗결함 — 재작성으로 못 살리는 씨앗

사용: uv run python -m src.steps.s19_c1_full_adopt
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl, write_jsonl
from src.steps.s18_verify_c1_review import FIX_EN, parse

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
FIX_KR = re.compile(r"KR:\s*(.+?)(?:\s*\[|$)")
JUDGE_TARGET = 4.0
REVIEW_DATE = "2026-08-07"


def main() -> None:
    targets = {s["id"]: s for s in read_jsonl(WORK_DIR / "c1_rewrite_targets.jsonl")}
    gated = read_jsonl(WORK_DIR / "c1_full_gated.jsonl")
    judged = {}
    for lv in ("a1", "a2", "b1", "b2"):
        f = WORK_DIR / f"c1_judged_{lv}.jsonl"
        if f.exists():
            for j in read_jsonl(f):
                judged[(j["seed_id"], j["cand"])] = j

    reviewed = {s["seed_id"]: s for s in parse(REPORTS_DIR / "restricted" / "c1_full_review_sheet_filled.md")}
    cand_map: dict[tuple[str, int], dict] = {(r["seed_id"], r["cand"]): r for r in gated}
    by_seed: dict[str, list[dict]] = {}
    for r in gated:
        by_seed.setdefault(r["seed_id"], []).append(r)

    final, defects, actions = [], {}, Counter()
    for sid, cands in by_seed.items():
        rev = reviewed.get(sid)

        if rev and "전체 불합격" in rev["heading"]:
            defects[sid] = {
                "day_type": targets[sid]["day_type"],
                "cefr": targets[sid].get("cefr_level"),
                "text_en": targets[sid]["text_en"],
                "reason": rev["heading"].split("전체 불합격 —")[-1].strip(),
            }
            actions["씨앗결함"] += 1
            continue

        if rev:
            picks = [r for r in rev["rows"] if r["verdict"].startswith(("채택", "수정"))]
            if not picks:
                actions["결론없음"] += 1
                continue
            p = picks[0]
            base = cand_map[(sid, p["cand"])]
            text_en, text_kr = base["text_en"], base["text_kr"]
            if p["verdict"].startswith("수정"):
                if m := FIX_EN.search(p["verdict"]):
                    text_en = m.group(1).strip()
                if m := FIX_KR.search(p["verdict"]):
                    text_kr = m.group(1).strip()
                actions["수정채택"] += 1
            else:
                actions["채택"] += 1
            source = "human_review"
        else:
            # 미검수 — judge 최고점 후보를 쓴다
            base = max(cands, key=lambda r: judged.get((sid, r["cand"]), {}).get("avg", 0))
            avg = judged.get((sid, base["cand"]), {}).get("avg", 0)
            if avg < JUDGE_TARGET:
                actions["미검수_저점제외"] += 1
                continue
            text_en, text_kr = base["text_en"], base["text_kr"]
            source = "judge_best"
            actions["미검수채택"] += 1

        final.append(
            {
                "seed_id": sid,
                "source_cand": base["cand"],
                "day_type": targets[sid]["day_type"],
                "cefr_level": targets[sid].get("cefr_level"),
                "month": targets[sid].get("month"),
                "text_en": text_en,
                "text_kr": text_kr,
                "kept_function": base.get("kept_function"),
                "content_origin": "ai_rewritten",
                "review": {
                    "source": source,
                    "modified": source == "human_review" and text_en != base["text_en"],
                    "judge_avg": judged.get((sid, base["cand"]), {}).get("avg"),
                    "seed_sim": base["gate"]["seed_sim"]["ratio"],
                    "reviewed_at": REVIEW_DATE,
                },
                "gen_meta": base["gen_meta"] | {"adopted_at": str(date.today())},
            }
        )

    final.sort(key=lambda r: r["seed_id"])
    n = write_jsonl(OUTPUT_DIR / "c1_full_final.jsonl", final)
    (OUTPUT_DIR / "c1_full_seed_defects.json").write_text(
        json.dumps(
            {
                "note": "재작성으로 살릴 수 없는 씨앗 — 교육 포인트가 문어체 커넥터라 A2 구어에 자리가 없다. "
                "씨앗 교체가 필요하다(style_lessons §24). 원문은 공개 경로에 넣지 않는다(ADR-010).",
                "reviewed_at": REVIEW_DATE,
                "seeds": defects,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    by_lv = Counter(f["cefr_level"] for f in final)
    by_src = Counter(f["review"]["source"] for f in final)
    print(f"output/c1_full_final.jsonl  {n}건 — {dict(actions)}")
    print(f"  CEFR: {dict(by_lv)} · 출처: {dict(by_src)}")
    print(f"output/c1_full_seed_defects.json  씨앗결함 {len(defects)}건")


if __name__ == "__main__":
    main()
