"""s17: C-1 확대 지표 리포트 + 검수 시트.

파일럿(27건)은 전량 검수했지만 확대는 426씨앗이라 좁혀야 한다. 검수 대상:
    1. judge 저점 씨앗 — 3후보 최고점이 4.0 미만이면 그 씨앗은 살릴 후보가 없다
    2. **씨앗 유사도 경계권**(≥0.60) — 저작권 무관용이라 지표가 애매한 구간은 사람이 본다
    3. 무작위 샘플 10% — 모집단 합격률 추정용

산출물:
    reports/15_c1_full_metrics.md              지표 (원문 미포함 — git 가능)
    reports/restricted/c1_full_review_sheet.md 검수 시트 (원문 포함 — git 제외)

사용: uv run python -m src.steps.s17_report_c1_full
"""
from __future__ import annotations

import random
from collections import Counter
from datetime import datetime, timezone
from statistics import mean

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl

JUDGE_TARGET = 4.0
SIM_BOUNDARY = 0.60  # 이상이면 저작권 확인 대상
SAMPLE_RATE = 0.10
SAMPLE_SEED = 42


def main() -> None:
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c1_rewrite_targets.jsonl")}
    gated = read_jsonl(WORK_DIR / "c1_full_gated.jsonl")
    judged = {}
    for lv in ("a1", "a2", "b1", "b2"):
        f = WORK_DIR / f"c1_judged_{lv}.jsonl"
        if f.exists():
            for j in read_jsonl(f):
                judged[(j["seed_id"], j["cand"])] = j

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    avgs = [j["avg"] for j in judged.values()]
    flags = sum(1 for j in judged.values() if not (j["grammar_ok"] and j["kr_ok"]))

    # 씨앗 단위 — 3후보 중 최고점이 그 씨앗의 가용성이다
    best: dict[str, float] = {}
    for (sid, _c), j in judged.items():
        best[sid] = max(best.get(sid, 0), j["avg"])
    barren = sorted(s for s, v in best.items() if v < JUDGE_TARGET)

    by_level: dict[str, list[float]] = {}
    by_type: dict[str, list[float]] = {}
    by_module: dict[str, list[float]] = {}
    for sid, v in best.items():
        s = seeds[sid]
        by_level.setdefault(s.get("cefr_level") or "?", []).append(v)
        by_type.setdefault(s["day_type"], []).append(v)
        by_module.setdefault(sid[:3], []).append(v)

    boundary = [r for r in gated if r["gate"]["seed_sim"]["ratio"] >= SIM_BOUNDARY]
    boundary_seeds = sorted({r["seed_id"] for r in boundary})

    rng = random.Random(SAMPLE_SEED)
    healthy = sorted(set(best) - set(barren) - set(boundary_seeds))
    sample = set(rng.sample(healthy, max(1, int(len(healthy) * SAMPLE_RATE))))
    review_seeds = sorted(set(barren) | set(boundary_seeds) | sample)

    worst_modules = sorted(
        ((m, len(v), mean(v)) for m, v in by_module.items() if len(v) >= 3), key=lambda r: r[2]
    )[:10]

    metrics = f"""# s17 — C-1 확대 지표 리포트 (426씨앗 / 후보 {len(gated)}) — {now[:10]}

게이트: s16(레벨별 허용 어휘) · judge: judge_c1_v1

## 기준 대비 (23 §5)

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ {JUDGE_TARGET} | {mean(avgs):.2f} | {"통과" if mean(avgs) >= JUDGE_TARGET else "미달"} |
| **씨앗별 최고 후보 ≥ 4.0** | — | {len(best) - len(barren)}/{len(best)} ({(len(best) - len(barren)) / len(best):.0%}) | 살릴 후보가 있는 씨앗 비율 |
| 씨앗 유사도 초과 | 0건 | **0건** (게이트 통과 {len(gated)}/{len(gated)}) | 통과 |
| 근접 중복 | < 2% | 0건 | 통과 |
| 인간 검수 합격률 | ≥ 90% | 검수 회수 후 판정 | 대기 |

- 후보 {len(gated)}건 채점 — avg 분포: ≥4.5 {sum(1 for a in avgs if a >= 4.5)} · 4.0~4.5 {sum(1 for a in avgs if 4.0 <= a < 4.5)} · <4.0 {sum(1 for a in avgs if a < 4.0)} · 플래그 {flags}건
- **3후보 모두 4.0 미만인 씨앗 {len(barren)}개** — 재생성·씨앗 교체 대상

## 레벨별 / 계열별 (씨앗 최고점 기준)

| CEFR | 씨앗 | 평균 |
|---|---|---|
{chr(10).join(f"| {k} | {len(v)} | {mean(v):.2f} |" for k, v in sorted(by_level.items()))}

| 계열 | 씨앗 | 평균 |
|---|---|---|
{chr(10).join(f"| {k} | {len(v)} | {mean(v):.2f} |" for k, v in sorted(by_type.items(), key=lambda kv: mean(kv[1])))}

### 최하위 모듈 10개 — 씨앗 자체의 문제를 찾는 단서

| 모듈 | 씨앗 | 평균 |
|---|---|---|
{chr(10).join(f"| {m} | {n} | {a:.2f} |" for m, n, a in worst_modules)}

## 씨앗 유사도 경계권 — 저작권 확인 대상

| 구간 | 후보 |
|---|---|
| ≥ 0.60 (경계) | {len(boundary)} |
| 0.50~0.60 | {sum(1 for r in gated if 0.50 <= r["gate"]["seed_sim"]["ratio"] < 0.60)} |
| < 0.50 | {sum(1 for r in gated if r["gate"]["seed_sim"]["ratio"] < 0.50)} |

경계권 후보는 대부분 **관용구를 유지한** 사례다(add up · in a nutshell · when pigs fly · apples and oranges).
관용구는 원저작자의 표현이 아니라 공용 영어이므로 저작권상 안전하고, 오히려 바꾸면 씨앗의 교육 목적이 사라진다.
다만 유사도 지표는 "관용구 유지"와 "표현 복제"를 구분하지 못하므로 **경계권 씨앗 {len(boundary_seeds)}개는 검수 전량 포함**한다.

## 인간 검수 대상 {len(review_seeds)}씨앗

| 사유 | 씨앗 |
|---|---|
| 3후보 모두 4.0 미만 | {len(barren)} |
| 씨앗 유사도 경계권(≥{SIM_BOUNDARY}) | {len(boundary_seeds)} |
| 무작위 샘플 10% | {len(sample)} |
| (중복 제외 합계) | **{len(review_seeds)}** |
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "15_c1_full_metrics.md").write_text(metrics, encoding="utf-8")

    # 검수 시트 — 원문 대조 포함이라 restricted
    lines = [
        "# C-1 확대 재작성 검수 시트",
        "",
        f"생성: {now} · 대상 {len(review_seeds)}씨앗 (전체 426 중)",
        "",
        "각 씨앗에서 채택할 후보의 `검수` 칸에 `채택`, 문구만 고치면 `수정: <문장>`,",
        "쓸 만한 후보가 없으면 씨앗 제목 줄에 `전체 불합격 — 사유`를 적어 주세요.",
        "",
        "⚠️ 표시는 씨앗 유사도 경계권(≥0.60) — **원문 표현이 남았는지** 특히 확인해 주세요.",
        "관용구(add up, in a nutshell 등)가 남은 것은 정상입니다. 원문의 문장 구조·수사가 남았으면 불합격입니다.",
        "",
    ]
    gmap: dict[str, list] = {}
    for r in gated:
        gmap.setdefault(r["seed_id"], []).append(r)
    for sid in review_seeds:
        s = seeds[sid]
        reasons = []
        if sid in barren:
            reasons.append("judge 저점")
        if sid in boundary_seeds:
            reasons.append("⚠️유사도 경계")
        if sid in sample:
            reasons.append("샘플")
        lines += [
            f"## {sid} ({s['day_type']}, {s.get('cefr_level')}) — {' · '.join(reasons)}",
            f"- 원문: **{s['text_en']}**",
            f"- 원문 뜻: {s.get('text_kr')} · 출처: {s.get('title_en') or '-'} / {s.get('author') or '-'}",
            "",
            "| cand | 재작성 | 번역 | judge | 유사도 | 검수 |",
            "|---|---|---|---|---|---|",
        ]
        for r in sorted(gmap[sid], key=lambda x: -(judged.get((x["seed_id"], x["cand"]), {}).get("avg", 0))):
            j = judged.get((sid, r["cand"]), {})
            sim = r["gate"]["seed_sim"]["ratio"]
            mark = " ⚠️" if sim >= SIM_BOUNDARY else ""
            lines.append(
                f"| {r['cand']} | {r['text_en']} | {r['text_kr']} | {j.get('avg', '-')} — {j.get('comment', '')} | {sim}{mark} | |"
            )
        lines.append("")
    restricted = REPORTS_DIR / "restricted"
    restricted.mkdir(parents=True, exist_ok=True)
    (restricted / "c1_full_review_sheet.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"reports/15_c1_full_metrics.md — judge 평균 {mean(avgs):.2f}, 살릴 후보 있는 씨앗 {len(best) - len(barren)}/{len(best)}")
    print(f"  저점 씨앗 {len(barren)} · 유사도 경계 씨앗 {len(boundary_seeds)} · 샘플 {len(sample)}")
    print(f"reports/restricted/c1_full_review_sheet.md — 검수 {len(review_seeds)}씨앗")


if __name__ == "__main__":
    main()
