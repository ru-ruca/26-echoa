"""s09b: C-3 검수 시트 기계 검증 — 대화 단위 판정을 집계한다.

C-2 시트는 표 행마다 판정이 붙지만(s09), C-3는 대화 하나에 `- 검수:` 한 줄이라 파서가 다르다.

검증·집계:
    coverage        50개 대화 전부에 판정이 있는가
    verdict_dist    합격 / 수정 / 불합격 분포와 합격률
    group_split     A_daily vs B_c2_ineligible 판정 차이 (§18~19 규칙 검증)
    type_split      B군 계열별 불합격률 — tale이 실제로 못 살아나는가
    seed_touching   수정안이 씨앗 문장을 건드리는가 (C-2 확정본까지 영향)
    judge_agreement judge seed_fit=false와 인간 불합격이 일치하는가

산출물: reports/09_c3_review_verification.md

사용: uv run python -m src.steps.s09b_verify_c3_review [검수시트.md]
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl

HEADER = re.compile(r"^## (\w+) \(([^,]+), ([^)]+)\) — judge")
VERDICT = re.compile(r"^- 검수:\s*(.*)$")
TURN_REF = re.compile(r"(\d+)턴")


def parse(path: Path) -> list[dict]:
    rows, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := HEADER.match(line):
            if cur:
                rows.append(cur)
            cur = {"seed_id": m.group(1), "group": m.group(2), "day_type": m.group(3), "verdict_raw": ""}
        elif cur is not None and (m := VERDICT.match(line)):
            cur["verdict_raw"] = m.group(1).strip()
    if cur:
        rows.append(cur)
    return rows


def classify(v: str) -> str:
    if not v:
        return "미판정"
    for p in ("합격", "수정", "불합격"):
        if v.startswith(p):
            return p
    return "기타"


def main(sheet: str | None = None) -> None:
    path = Path(sheet) if sheet else REPORTS_DIR / "c3_review_sheet_filled.md"
    rows = parse(path)
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c3_seeds.jsonl")}
    gated = {d["seed_id"]: d for d in read_jsonl(WORK_DIR / "c3_candidates_gated.jsonl")}
    judged = {j["seed_id"]: j for j in read_jsonl(WORK_DIR / "c3_judged.jsonl")}

    dist = Counter(classify(r["verdict_raw"]) for r in rows)
    by_group: dict[str, Counter] = {}
    for r in rows:
        by_group.setdefault(r["group"], Counter())[classify(r["verdict_raw"])] += 1
    b_by_type: dict[str, Counter] = {}
    for r in rows:
        if r["group"] == "B_c2_ineligible":
            b_by_type.setdefault(r["day_type"], Counter())[classify(r["verdict_raw"])] += 1

    # 수정안이 씨앗 턴을 건드리는가 — 씨앗 원문 불변 규칙 위반이자 C-2 확정본까지 영향
    seed_touching = []
    for r in rows:
        if classify(r["verdict_raw"]) != "수정":
            continue
        seed_turn = gated[r["seed_id"]]["seed_turn"]
        if str(seed_turn) in TURN_REF.findall(r["verdict_raw"]):
            seed_touching.append(r)

    # judge seed_fit=false와 인간 불합격의 일치도
    jf = {sid for sid, j in judged.items() if not j["seed_fit"]}
    hr = {r["seed_id"] for r in rows if classify(r["verdict_raw"]) == "불합격"}
    agree, only_j, only_h = jf & hr, jf - hr, hr - jf

    def rate(c: Counter) -> str:
        n = sum(c.values())
        return f"{c['합격'] / n:.0%} / {(c['합격'] + c['수정']) / n:.0%}" if n else "—"

    lines = [
        "# s09b — C-3 검수 시트 기계 검증",
        "",
        f"대상: `{path.name}` · 대화 {len(rows)}개 (미판정 {dist['미판정']}건)",
        "",
        "## 판정 분포",
        "",
        "| 판정 | 건수 |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in dist.most_common()],
        "",
        f"합격률 **{dist['합격'] / len(rows):.0%}** · 합격+수정 **{(dist['합격'] + dist['수정']) / len(rows):.0%}**",
        "",
        "## 그룹별 — style_lessons §18~19 규칙 검증",
        "",
        "| 그룹 | 대화 | 합격 | 수정 | 불합격 | 합격률 / 합격+수정 |",
        "|---|---|---|---|---|---|",
        *[
            f"| {g} | {sum(c.values())} | {c['합격']} | {c['수정']} | {c['불합격']} | **{rate(c)}** |"
            for g, c in sorted(by_group.items())
        ],
        "",
        "### B군(C-2 부적격) 계열별",
        "",
        "| 계열 | 대화 | 합격 | 수정 | 불합격 | 불합격률 |",
        "|---|---|---|---|---|---|",
        *[
            f"| {dt} | {sum(c.values())} | {c['합격']} | {c['수정']} | {c['불합격']} | **{c['불합격'] / sum(c.values()):.0%}** |"
            for dt, c in sorted(b_by_type.items(), key=lambda kv: kv[1]["불합격"] / sum(kv[1].values()))
        ],
        "",
        "## judge `seed_fit=false` vs 인간 `불합격` 일치도",
        "",
        f"- 양쪽 모두 지목: **{len(agree)}건** {sorted(agree)}",
        f"- judge만 지목: {len(only_j)}건 {sorted(only_j)}",
        f"- 인간만 지목: {len(only_h)}건 {sorted(only_h)}",
        "",
        f"judge seed_fit이 인간 불합격을 예측한 정확도: **{len(agree) / max(1, len(hr)):.0%}**"
        " (인간 불합격 중 judge가 미리 잡은 비율)",
        "",
        f"## 씨앗 턴을 건드리는 수정안 {len(seed_touching)}건",
        "",
        "씨앗 문장은 원문 그대로여야 한다(게이트 규칙). 씨앗을 고치는 수정은 **C-2 확정본까지 영향**을 준다.",
        "",
        "| 씨앗 | 계열 | 수정안 |",
        "|---|---|---|",
        *[f"| {r['seed_id']} | {r['day_type']} | {r['verdict_raw'][:150]} |" for r in seed_touching],
        "",
    ]
    out = REPORTS_DIR / "09_c3_review_verification.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"대화 {len(rows)}개 — {dict(dist)}")
    print(f"합격률 {dist['합격'] / len(rows):.0%} · 합격+수정 {(dist['합격'] + dist['수정']) / len(rows):.0%}")
    for g, c in sorted(by_group.items()):
        print(f"  {g}: 합격률 {rate(c)} (불합격 {c['불합격']})")
    print(f"judge seed_fit ↔ 인간 불합격 일치 {len(agree)}건 / 씨앗 턴 수정 {len(seed_touching)}건")
    print(f"→ {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
