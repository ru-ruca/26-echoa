"""s02: 허용 어휘 목록 구성 + 기존 문장의 초과율 baseline 실측.

first_month가 month 누적이 아니라(1/7/13/25만 존재) CEFR 기반으로 대체한다:
    core     = CEFR A1 vocabulary (+기능어는 POS로 자동 허용이라 목록 불필요)
    extended = core ∪ M01~03 문장 실등장 content lemma

baseline(core 기준 초과율)은 "기존 커리큘럼 문장도 core 밖 단어를 얼마나 쓰는가"의
실측치로, 생성물 하드필터 임계값의 근거가 된다 (23 §9 미결정 항목의 실측 단계).

산출물:
    data/work/allowlist_m01_03.json
    reports/02_allowlist_baseline.md
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from statistics import mean, quantiles

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl
from src.lib.textproc import content_lemmas, normalize_word

PILOT_CEFR = "A1"


def build_core(vocab: list[dict]) -> set[str]:
    core: set[str] = set()
    for v in vocab:
        if v.get("cefr_level") != PILOT_CEFR or not v.get("word"):
            continue
        word = v["word"].strip().lower()
        core.add(word)
        norm = normalize_word(word)
        core.add(norm)
        # 다단어 항목("get up" 등)은 개별 토큰 lemma도 허용해야 문장 검사와 맞물린다
        core.update(norm.split())
    core.discard("")
    return core


def main() -> None:
    vocab = read_jsonl(WORK_DIR / "vocabulary.jsonl")
    seeds = read_jsonl(WORK_DIR / "seeds_m01_03.jsonl")

    core = build_core(vocab)

    # 기존 문장 실측 — review(재사용)를 뺀 205문장이 학습 노출 원본이지만,
    # 실등장 어휘 수집은 전체 229로 해도 집합 연산이라 결과가 같다.
    per_sentence: list[dict] = []
    seen_lemmas: set[str] = set()
    excess_counter: Counter[str] = Counter()

    for s in seeds:
        lemmas = content_lemmas(s["text_en"])
        seen_lemmas.update(lemmas)
        if s["seed_class"] == "excluded_review":
            continue
        excess = [lm for lm in lemmas if lm not in core]
        excess_counter.update(excess)
        per_sentence.append(
            {
                "id": s["id"],
                "seed_class": s["seed_class"],
                "n_content": len(lemmas),
                "n_excess": len(excess),
                "excess_ratio": len(excess) / len(lemmas) if lemmas else 0.0,
                "excess_words": excess,
            }
        )

    extended_extra = sorted(seen_lemmas - core)
    ratios = [p["excess_ratio"] for p in per_sentence]
    counts = [p["n_excess"] for p in per_sentence]
    p90_ratio = quantiles(ratios, n=10)[-1]
    p90_count = quantiles(counts, n=10)[-1]

    allowlist = {
        "meta": {
            "pilot_months": 3,
            "cefr": PILOT_CEFR,
            "core_size": len(core),
            "extended_extra_size": len(extended_extra),
            "baseline_sentences": len(per_sentence),
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "core": sorted(core),
        "extended_extra": extended_extra,
    }
    out = WORK_DIR / "allowlist_m01_03.json"
    out.write_text(json.dumps(allowlist, ensure_ascii=False, indent=1), encoding="utf-8")

    zero = sum(1 for c in counts if c == 0)
    report = f"""# s02 — 허용 어휘 구성·baseline 초과율 리포트 (M01~03)

생성: {allowlist["meta"]["generated_at"]}

## 허용 어휘

| 집합 | 크기 | 구성 |
|---|---|---|
| core | {len(core)} | CEFR {PILOT_CEFR} vocabulary (word+lemma 정규화, 다단어는 토큰 분해 포함) |
| extended 추가분 | {len(extended_extra)} | M01~03 실등장 content lemma 중 core 밖 |

기능어(관사·전치사·대명사·조동사·접속사·고유명사·감탄사·수사)는 POS 기반 자동 허용 — 검사 대상은 NOUN·VERB·ADJ·ADV lemma만.

## 기존 문장 baseline (core 기준 초과율, review 제외 {len(per_sentence)}문장)

| 지표 | 값 |
|---|---|
| 초과 0개 문장 | {zero} ({zero / len(per_sentence):.0%}) |
| 문장당 초과 개수 평균 / p90 / 최대 | {mean(counts):.2f} / {p90_count:.0f} / {max(counts)} |
| 문장당 초과 비율 평균 / p90 / 최대 | {mean(ratios):.1%} / {p90_ratio:.1%} / {max(ratios):.1%} |

### 초과 빈도 상위 20 lemma

| lemma | 빈도 |
|---|---|
{chr(10).join(f"| {w} | {c} |" for w, c in excess_counter.most_common(20))}

### 초과가 많은 문장 상위 10

| id | class | 초과/전체 | 초과 단어 |
|---|---|---|---|
{chr(10).join(f"| {p['id']} | {p['seed_class']} | {p['n_excess']}/{p['n_content']} | {', '.join(p['excess_words'])} |" for p in sorted(per_sentence, key=lambda x: -x["n_excess"])[:10])}

## 하드필터 임계값 제안 (파일럿 s04에 적용, 실행 결과 보고 조정)

1. **extended 기준**: 생성물의 content lemma는 extended 안에 있어야 한다 — 초과 0 목표.
2. **core 기준 참고치**: 초과 content lemma 문장당 ≤ {max(1, round(p90_count))}개 (기존 p90 수준).
   extended를 통과했더라도 core 밖 단어가 이보다 많으면 A1 이탈로 보고 탈락.
3. judge 재랭킹에서 core 밖 단어 수를 감점 요소로 반영.
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "02_allowlist_baseline.md").write_text(report, encoding="utf-8")

    print(f"allowlist_m01_03.json  core={len(core)} extended_extra={len(extended_extra)}")
    print(f"reports/02_allowlist_baseline.md  baseline {len(per_sentence)}문장")
    print(f"  초과 0개 문장 {zero}/{len(per_sentence)}, 평균 초과 {mean(counts):.2f}개, p90 {p90_count:.0f}개")


if __name__ == "__main__":
    main()
