"""s10: C-2 검수 회수 — v2 판정을 반영해 확정본을 만든다.

판정 반영 (reports/c2_review_sheet_filled_v2.md):
    합격          그대로 채택
    수정          수정안(영문+한글) 적용
    수정(KR만)    한글만 교체
    불합격        제외
    씨앗결함      해당 씨앗의 **전 변형** 제외 (씨앗 자체 문제 — s11에서 씨앗 교체 후 재생성)

검수 시트에 없는 변형(적격 씨앗 · judge ≥ 4.0 · 샘플 미추출)은 샘플 검수 원칙(23 §4)에 따라 채택한다.
부적격 씨앗(씨앗 평균 < 3.5)의 변형은 전부 제외한다.

산출물:
    output/c2_final.jsonl          확정 변형 (content_origin=ai_generated)
    output/c2_seed_defects.json    씨앗결함 8개 + 대안 씨앗 (s11 입력)

사용: uv run python -m src.steps.s10_c2_adopt
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from statistics import mean

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl, write_jsonl
from src.steps.s06_report import SEED_ELIGIBLE_MIN
from src.steps.s09_verify_review import FIX_EN, SEED_ALT, classify, parse

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
REVIEW_SHEET = REPORTS_DIR / "c2_review_sheet_filled_v2.md"
REVIEW_DATE = "2026-08-04"

FIX_KR = __import__("re").compile(r"KR:\s*(.+?)(?:\s*\[어휘승인요청|$)")
FIX_KR_ONLY = __import__("re").compile(r"수정\(KR만\):\s*(.+?)(?:\s*\[어휘승인요청|$)")


def main() -> None:
    gated = read_jsonl(WORK_DIR / "c2_candidates_gated.jsonl")
    judged = {(j["seed_id"], j["cand"]): j for j in read_jsonl(WORK_DIR / "c2_judged.jsonl")}
    reviews = {(r["seed_id"], r["cand"]): r for r in parse(REVIEW_SHEET)}

    seed_avgs: dict[str, list[float]] = {}
    for (sid, _c), j in judged.items():
        seed_avgs.setdefault(sid, []).append(j["avg"])
    ineligible = {sid for sid, v in seed_avgs.items() if mean(v) < SEED_ELIGIBLE_MIN}

    # 씨앗결함 — 시트에 한 행이라도 표기됐으면 그 씨앗 전체가 결함
    defects: dict[str, dict] = {}
    for r in reviews.values():
        if classify(r["verdict_raw"]) != "씨앗결함":
            continue
        d = defects.setdefault(r["seed_id"], {"reason": "", "alt": ""})
        reason = r["verdict_raw"].removeprefix("씨앗결함").lstrip("— ").split(" / 대안 씨앗:")[0]
        d["reason"] = d["reason"] or reason.strip()
        if m := SEED_ALT.search(r["verdict_raw"]):
            alt = m.group(1).strip()
            d["alt"] = d["alt"] or ("" if alt.startswith("없음") else alt)

    final, actions = [], Counter()
    for row in gated:
        sid, cand = row["seed_id"], row["cand"]
        if not row["gate"]["pass"]:
            actions["게이트탈락"] += 1
            continue
        if sid in ineligible:
            actions["부적격씨앗"] += 1
            continue
        if sid in defects:
            actions["씨앗결함"] += 1
            continue

        rev = reviews.get((sid, cand))
        kind = classify(rev["verdict_raw"]) if rev else "미검수"
        text_en, text_kr = row["text_en"], row["text_kr"]

        if kind == "불합격":
            actions["불합격"] += 1
            continue
        if kind == "수정":
            if m := FIX_EN.search(rev["verdict_raw"]):
                text_en = m.group(1).strip()
            if m := FIX_KR.search(rev["verdict_raw"]):
                text_kr = m.group(1).strip()
        elif kind == "수정(KR만)":
            if m := FIX_KR_ONLY.search(rev["verdict_raw"]):
                text_kr = m.group(1).strip()
        actions[kind] += 1

        final.append(
            {
                "seed_id": sid,
                "cand": cand,
                "pattern": row["pattern"],
                "text_en": text_en,
                "text_kr": text_kr,
                "slots": row.get("slots"),
                "content_origin": "ai_generated",
                "review": {
                    "verdict": kind,
                    "modified": kind.startswith("수정"),
                    "judge_avg": judged.get((sid, cand), {}).get("avg"),
                    "reviewed_at": REVIEW_DATE,
                },
                "gen_meta": row["gen_meta"] | {"adopted_at": str(date.today())},
            }
        )

    # 수정 반영으로 문장이 서로 수렴할 수 있어 확정 직전에 다시 게이트를 태운다
    from src.steps.s04_gate_hard import main as gate_main

    tmp = WORK_DIR / "c2_final_precheck.jsonl"
    write_jsonl(tmp, final)
    gate_main("c2", str(tmp), str(WORK_DIR / "c2_final_regated.jsonl"))
    regated = {(r["seed_id"], r["cand"]): r["gate"] for r in read_jsonl(WORK_DIR / "c2_final_regated.jsonl")}
    dropped = [k for k, g in regated.items() if not g["pass"]]
    final = [f for f in final if regated[(f["seed_id"], f["cand"])]["pass"]]
    actions["재게이트탈락"] = len(dropped)

    n = write_jsonl(OUTPUT_DIR / "c2_final.jsonl", final)
    (OUTPUT_DIR / "c2_seed_defects.json").write_text(
        json.dumps(
            {
                "note": "C-2 씨앗결함 — 고정부 자체의 결함이라 변형 수정으로 해결되지 않는다. "
                "alt가 있으면 씨앗 교체 후 재생성, 없으면 C-2에서 폐기(통청크 자산으로 유지).",
                "reviewed_at": REVIEW_DATE,
                "seeds": defects,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    print(f"output/c2_final.jsonl  {n}건 — {dict(actions)}")
    replace = {k: v for k, v in defects.items() if v["alt"]}
    print(f"output/c2_seed_defects.json  씨앗결함 {len(defects)}개 (교체 {len(replace)} / 폐기 {len(defects) - len(replace)})")


if __name__ == "__main__":
    main()
