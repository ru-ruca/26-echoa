"""s06: 지표 리포트 + 인간 검수 시트 (Phase 1 = C-1 모드).

산출물:
    reports/04_c1_pilot_metrics.md        지표 리포트 (원문 미포함 — git 가능)
    reports/restricted/c1_review_sheet.md 인간 검수 시트 (씨앗 원문 포함 — git 제외)

C-1은 27개(전량 검수 가능) + 출시 전제 저작권 건이라 샘플이 아닌 전량 검수한다.
(무작위 5~10% 샘플은 C-2 대량 생성에서 적용 — 23 §4)

사용: uv run python -m src.steps.s06_report c1
"""
from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime, timezone
from statistics import mean

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl

JUDGE_TARGET = 4.0  # 23 §5


def main(mode: str = "c1") -> None:
    if mode != "c1":
        raise SystemExit(f"mode '{mode}'는 아직 미구현 — Phase 2에서 c2 추가")

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
