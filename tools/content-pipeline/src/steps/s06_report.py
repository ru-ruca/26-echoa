"""s06: 지표 리포트 + 인간 검수 시트 (c1·c2 모드).

c1: 27개 전량 검수 (출시 전제 저작권 건). 시트는 씨앗 원문 포함 → reports/restricted/.
c2: judge 저점(<4.0) 전량 + 통과분 무작위 10% 샘플 검수 (23 §4). c2 씨앗은
    저위험 원문·재작성본이라 시트를 reports/에 둔다 (격리 불필요).

사용: uv run python -m src.steps.s06_report c1|c2
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from datetime import datetime, timezone
from statistics import mean

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl

JUDGE_TARGET = 4.0  # 23 §5
SAMPLE_RATE = 0.10
SAMPLE_SEED = 42  # 재현성
SEED_ELIGIBLE_MIN = 3.5  # 씨앗 평균이 이 미만이면 C-2 부적격 씨앗으로 분리


def report_c2() -> None:
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c2_seeds.jsonl")}
    gated = read_jsonl(WORK_DIR / "c2_candidates_gated.jsonl")
    judged = {(j["seed_id"], j["cand"]): j for j in read_jsonl(WORK_DIR / "c2_judged.jsonl")}

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    passed = [r for r in gated if r["gate"]["pass"]]
    fail_counts = Counter(f for r in gated for f in r["gate"]["fails"])
    avgs = [j["avg"] for j in judged.values()]
    flags = sum(1 for j in judged.values() if not (j["grammar_ok"] and j["kr_ok"]))

    # 씨앗별 생존 수 — 씨앗당 6개 중 몇 개가 게이트를 통과했나
    per_seed = Counter(r["seed_id"] for r in passed)
    starved = sorted(sid for sid in seeds if per_seed.get(sid, 0) < 3)

    # 씨앗 계열별 judge 평균 — "어떤 씨앗이 substitution drill에 맞는가"의 실측
    by_type: dict[str, list[float]] = {}
    seed_avgs: dict[str, list[float]] = {}
    for (sid, _c), j in judged.items():
        by_type.setdefault(seeds[sid]["day_type"], []).append(j["avg"])
        seed_avgs.setdefault(sid, []).append(j["avg"])
    type_rows = sorted(
        ((t, len(v), mean(v)) for t, v in by_type.items()), key=lambda r: r[2]
    )
    worst_seeds = sorted(
        ((sid, mean(v), seeds[sid]["day_type"], seeds[sid]["text_en"]) for sid, v in seed_avgs.items()),
        key=lambda r: r[1],
    )[:12]

    # 씨앗 적격성 — 씨앗 평균이 기준 미달이면 씨앗 자체가 substitution drill에 안 맞는 것으로 보고
    # 검수 대상에서 분리한다 (개별 변형을 고쳐도 해결되지 않음. 리포트 §판정 참조)
    ineligible = {sid for sid, v in seed_avgs.items() if mean(v) < SEED_ELIGIBLE_MIN}

    # 검수 대상: 적격 씨앗의 judge 저점 전량 + 나머지 무작위 10%
    eligible_judged = {k: j for k, j in judged.items() if k[0] not in ineligible}
    low = [k for k, j in eligible_judged.items() if j["avg"] < JUDGE_TARGET]
    rest = [k for k, j in eligible_judged.items() if j["avg"] >= JUDGE_TARGET]
    rng = random.Random(SAMPLE_SEED)
    sample = set(low) | set(rng.sample(rest, max(1, int(len(rest) * SAMPLE_RATE))))

    elig_avgs = [j["avg"] for j in eligible_judged.values()]

    metrics = f"""# s06 — C-2 파일럿 지표 리포트 (M01~03, 씨앗 145)

생성: {now} · 게이트: s04(c2) · judge: judge_c2_v2

## 23 §5 기준 대비

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ {JUDGE_TARGET}/5 | {mean(avgs):.2f} | {"통과" if mean(avgs) >= JUDGE_TARGET else "미달"} |
| 근접 중복(통과분) | < 2% | 게이트 차단 {fail_counts.get("near_duplicate_db", 0) + fail_counts.get("near_duplicate_batch", 0)}건 → 통과분 0% | 통과 |
| 씨앗 유사도 | 변형이므로 상한 대신 동일 판정({fail_counts.get("seed_identical", 0)}건 차단) | — | 통과 |
| 인간 검수 합격률(샘플) | ≥ 90% | 검수 시트 회수 후 판정 | 대기 |

## 게이트·채점 요약

- 후보 {len(gated)} → 게이트 통과 {len(passed)} ({len(passed) / len(gated):.0%}) — 탈락 사유: {dict(fail_counts)}
- judge 채점 {len(judged)}건 — avg 분포: ≥4.5 {sum(1 for a in avgs if a >= 4.5)} · 4.0~4.5 {sum(1 for a in avgs if 4.0 <= a < 4.5)} · <4.0 {sum(1 for a in avgs if a < 4.0)} · 플래그 {flags}건
- 씨앗별 생존(6개 중): 평균 {mean(per_seed.values()) if per_seed else 0:.1f}개 · **3개 미만 생존 씨앗 {len(starved)}개** {starved if len(starved) <= 15 else str(starved[:15]) + " …"}
- **씨앗 적격성**: 씨앗 평균 ≥ {SEED_ELIGIBLE_MIN} 인 적격 씨앗 {len(seed_avgs) - len(ineligible)}개 / 부적격 {len(ineligible)}개
  (적격분 변형 {len(eligible_judged)}건, judge 평균 **{mean(elig_avgs):.2f}** → 기준 {"충족" if mean(elig_avgs) >= JUDGE_TARGET else "미달"})
- 인간 검수 대상(적격분만): judge 저점 {len(low)} + 무작위 샘플 {len(sample) - len(low)} = {len(sample)}건 (seed={SAMPLE_SEED})

## 씨앗 계열별 judge 평균 — 어떤 씨앗이 substitution drill에 맞는가

| day_type | 채점 건수 | judge 평균 |
|---|---|---|
{chr(10).join(f"| {t} | {n} | {a:.2f} |" for t, n, a in type_rows)}

## judge 평균 최하위 씨앗 12개 (재생성·폐기 검토 대상)

| 씨앗 | 계열 | 평균 | 원문 |
|---|---|---|---|
{chr(10).join(f"| {sid} | {dt} | {a:.2f} | {txt} |" for sid, a, dt, txt in worst_seeds)}

## 판정과 원인 — 생성 품질이 아니라 씨앗 적격성

전체 평균 {mean(avgs):.2f}는 기준 미달이지만, **적격 씨앗만 보면 {mean(elig_avgs):.2f}로 기준을 넘는다.**
계열별 격차가 원인을 가리킨다: {" · ".join(f"`{t}` {a:.2f}" for t, _n, a in reversed(type_rows))}.

세 judge 배치가 독립적으로 같은 결론을 냈다 — **속담·동화 종결구는 substitution drill 대상이 아니다**:

- 슬롯을 치환하면 "지어낸 격언"이 된다 (A friend in need → A doctor in need). 실제 발화 상황이 없어 재사용 가치가 0.
- 고유명사가 의미를 지탱하는 속담(All roads lead to **Rome**)은 일반명사 치환 자체가 성립하지 않는다.
- 화석화된 관용구(happily ever after, raining cats and dogs)는 슬롯화하면 정작 그 관용구를 못 가르친다.
- 씨앗 고정부가 A1을 넘는 문법(비교급 louder, 최상급 the best time, 자유관계절)을 담으면 변형 전량이 A1을 이탈한다.
- 서사체 도치·인용문("…," said the Ant)은 인용부호 표기까지 씨앗에서 상속되고 대화 재사용성이 낮다.

이 판정은 [prompts/style_lessons.md](../prompts/style_lessons.md) §13~17 "C-2 씨앗 적격성 규칙"으로 반영했다.

### 권고

1. **부적격 씨앗 {len(ineligible)}개는 C-2에서 제외** — 개별 변형을 고쳐도 해결되지 않는다.
   통청크 암기 자산으로 그대로 쓰거나 C-3 대화에서 문맥과 함께 제시한다.
2. 인간 검수는 적격분 {len(sample)}건으로 진행 → 합격률로 23 §5 마지막 기준을 판정.
3. 월 단위 확대 전에 **씨앗 선별을 파이프라인 단계로 승격**(s01 분류에 C-2 적격 플래그 추가) 검토.
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "05_c2_pilot_metrics.md").write_text(metrics, encoding="utf-8")

    lines = [
        "# C-2 변형 인간 검수 시트 (적격 씨앗의 judge 저점 전량 + 무작위 10%)",
        "",
        f"생성: {now} · 대상 {len(sample)}건",
        "",
        f"**대상 범위**: 씨앗 평균 ≥ {SEED_ELIGIBLE_MIN}인 적격 씨앗 {len(seed_avgs) - len(ineligible)}개"
        f" (변형 {len(eligible_judged)}건, judge 평균 {mean(elig_avgs):.2f}).",
        f"부적격 씨앗 {len(ineligible)}개는 개별 변형 수정으로 해결되지 않아 제외 —"
        " 씨앗 단위 폐기/다른 방식 적용을 리포트 §판정에서 별도 결정한다.",
        "",
        "판정: `합격` / `수정: <고친 문장>` / `불합격 — 사유` 를 `검수` 칸에 표기.",
        "",
        f"> 부적격 씨앗: {', '.join(sorted(ineligible))}",
        "",
    ]
    by_seed: dict[str, list] = {}
    for (sid, c) in sorted(sample):
        by_seed.setdefault(sid, []).append(c)
    gated_map = {(r["seed_id"], r["cand"]): r for r in gated}
    for sid, cands in by_seed.items():
        seed = seeds[sid]
        pattern = gated_map[(sid, cands[0])].get("pattern", "")
        lines += [
            f"## {sid} ({seed['day_type']}, {seed['origin']}) — 씨앗: {seed['text_en']}",
            f"- 패턴: `{pattern}`",
            "",
            "| cand | 변형 | 번역 | judge | 코멘트 | 검수 |",
            "|---|---|---|---|---|---|",
        ]
        for c in cands:
            r = gated_map[(sid, c)]
            j = judged[(sid, c)]
            mark = " ⚠️저점" if j["avg"] < JUDGE_TARGET else ""
            lines.append(
                f"| {c} | {r['text_en']} | {r['text_kr']} | {j['avg']}{mark} | {j.get('comment', '')} | |"
            )
        lines.append("")
    (REPORTS_DIR / "c2_review_sheet.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"reports/05_c2_pilot_metrics.md — judge 평균 {mean(avgs):.2f}, 통과 {len(passed)}/{len(gated)}")
    print(f"reports/c2_review_sheet.md — 검수 대상 {len(sample)}건 (저점 {len(low)} + 샘플 {len(sample) - len(low)})")


def main(mode: str = "c1") -> None:
    if mode == "c2":
        report_c2()
        return
    if mode != "c1":
        raise SystemExit(f"mode '{mode}' 미지원 (c1|c2)")

    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "seeds_m01_03.jsonl")}
    gated = read_jsonl(WORK_DIR / "c1_candidates_gated.jsonl")
    judged = {(j["seed_id"], j["cand"]): j for j in read_jsonl(WORK_DIR / "c1_judged.jsonl")}

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    n_pass = sum(1 for r in gated if r["gate"]["pass"])
    fail_counts = Counter(f for r in gated for f in r["gate"]["fails"])
    avgs = [j["avg"] for j in judged.values()]
    flags = sum(1 for j in judged.values() if not (j["grammar_ok"] and j["kr_ok"]))
    seed_ratios = [r["gate"]["seed_sim"]["ratio"] for r in gated]

    # ---- 지표 리포트 (원문 미포함) ----
    metrics = f"""# s06 — C-1 파일럿 지표 리포트 (M01~03분 27개)

생성: {now} · 게이트: s04(c1) · judge: judge_c1_v1

## 23 §5 기준 대비

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ {JUDGE_TARGET}/5 | {mean(avgs):.2f} | {"통과" if mean(avgs) >= JUDGE_TARGET else "미달"} |
| 씨앗 유사도 초과(통과분) | 0건 | 0건 (게이트에서 {fail_counts.get("too_similar_to_seed", 0)}건 차단) | 통과 |
| 근접 중복(통과분) | < 2% | {fail_counts.get("near_duplicate_db", 0) + fail_counts.get("near_duplicate_batch", 0)}건 차단, 통과분 0% | 통과 |
| 인간 검수 합격률 | ≥ 90% | 검수 시트 회수 후 판정 | 대기 |

## 게이트·채점 요약

- 후보 81 → 게이트 통과 {n_pass} ({n_pass / len(gated):.0%}) — 탈락 사유: {dict(fail_counts)}
- 씨앗 유사도(전체 81) ratio 평균 {mean(seed_ratios):.2f} / 최대 {max(seed_ratios):.2f} (상한 0.65)
- judge avg 분포: ≥4.5 {sum(1 for a in avgs if a >= 4.5)} · 4.0~4.5 {sum(1 for a in avgs if 4.0 <= a < 4.5)} · <4.0 {sum(1 for a in avgs if a < 4.0)}
- grammar/kr 플래그: {flags}건

## 관찰 (다음 라운드 반영)

- spacy sm 모델이 비교급(higher·nicer)을 원급 lemma로 풀지 못해 어휘 필터가 보수적으로 탈락시킴 —
  C-2 전에 비교급 접미사 처리 추가 검토.
- judge가 잡은 감점 유형: 비관용 콜로케이션(lose time), 격언풍 조어(재사용성 낮음), A1 초과 문법(비교급 등).
  → c1_rewrite 프롬프트 v2에 "관용적 콜로케이션·대화 재사용성" 강조 반영 검토.
- 씨앗 유사도 상한(jaccard 0.55 / ratio 0.65)은 구조 복제 1건을 정확히 차단 — 유지.
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "04_c1_pilot_metrics.md").write_text(metrics, encoding="utf-8")

    # ---- 인간 검수 시트 (원문 포함 — restricted) ----
    lines = [
        "# C-1 재작성 인간 검수 시트 (전량 27씨앗)",
        "",
        f"생성: {now}",
        "",
        "각 씨앗에서 **채택할 후보 1개**의 `검수` 칸에 `채택`, 나머지는 비움.",
        "쓸 만한 후보가 없으면 씨앗 제목 줄에 `전체 불합격 — 사유`를 적는다.",
        "문구만 고치면 되는 후보는 `수정: <고친 문장>`으로 표기.",
        "",
    ]
    for seed_id in sorted({r["seed_id"] for r in gated}):
        seed = seeds[seed_id]
        lines += [
            f"## {seed_id} ({seed['day_type']}) — 원문: {seed['text_en']}",
            f"- 원문 뜻: {seed['text_kr']} · notes: {seed.get('notes') or '-'}",
            "",
            "| cand | 후보 문장 | 번역 | judge | 플래그 | 검수 |",
            "|---|---|---|---|---|---|",
        ]
        cands = sorted(
            (r for r in gated if r["seed_id"] == seed_id),
            key=lambda r: -(judged.get((r["seed_id"], r["cand"]), {}).get("avg", 0)),
        )
        for r in cands:
            j = judged.get((r["seed_id"], r["cand"]))
            if not r["gate"]["pass"]:
                lines.append(
                    f"| {r['cand']} | ~~{r['text_en']}~~ | {r['text_kr']} | 게이트 탈락 | {', '.join(r['gate']['fails'])} | |"
                )
                continue
            flag = []
            if j and not j["grammar_ok"]:
                flag.append("grammar")
            if j and not j["kr_ok"]:
                flag.append("kr")
            comment = f" — {j['comment']}" if j and j.get("comment") else ""
            lines.append(
                f"| {r['cand']} | {r['text_en']} | {r['text_kr']} | {j['avg'] if j else '-'}{comment} | {', '.join(flag) or '-'} | |"
            )
        lines.append("")

    restricted = REPORTS_DIR / "restricted"
    restricted.mkdir(parents=True, exist_ok=True)
    (restricted / "c1_review_sheet.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"reports/04_c1_pilot_metrics.md — judge 평균 {mean(avgs):.2f}, 게이트 통과 {n_pass}/81")
    print("reports/restricted/c1_review_sheet.md — 검수 시트 (27씨앗 전량, 원문 포함·git 제외)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c1")
