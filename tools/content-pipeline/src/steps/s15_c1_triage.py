"""s15: C-1 확대 대상 선별 — 재작성이 실제로 필요한 씨앗만 남긴다.

ADR-010 처리 기준표는 계열별로 다르다:
    movie·drama·comedy·interview  높음      → AI 재작성 교체
    news·ted·academic             중간~높음 → 재작성 또는 자체작성
    quote                         낮음~중간 → **만료·저작물성 약한 것 선별, 나머지 재생성**

"선별"을 건너뛰고 전량 재작성하면 퍼블릭 도메인·자체작성 문장까지 불필요하게 바꾸게 된다.
sources.copyright 필드로 1차 선별하고, 표기가 없거나 모호한 것만 재작성 대상으로 남긴다.

산출물:
    data/work/c1_rewrite_targets.jsonl  재작성 대상 (CEFR별 분리 가능)
    reports/14_c1_triage.md             선별 결과·근거

사용: uv run python -m src.steps.s15_c1_triage
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl, write_jsonl

# ⚠️ copyright 필드는 신뢰할 수 없다 (2026-08-06 실측).
# `Public`으로 표기된 quote 중 Steve Jobs(2005)·Malala Yousafzai(2013)가 있었다 —
# 생존 인물·최근 발언인데 퍼블릭 도메인으로 라벨돼 있다. 필드만 믿으면 저작권물을 그대로 내보낸다.
# 따라서 quote는 **저자 귀속**으로 판정한다. 필드는 참고만 한다.
SELF_AUTHORED = re.compile(r"^original$|self[-_ ]?authored", re.I)
# 특정인에게 귀속되지 않는 표기 — ADR-010 "짧은 문구·명언은 저작물성이 약해 상대적으로 안전"
ANONYMOUS = re.compile(
    r"^(unknown|traditional|common saying|english saying|english proverb|proverb|anonymous|-|)$",
    re.I,
)
# 계열별 위험도 (ADR-010 처리 기준표)
HIGH = {"movie", "drama", "comedy", "interview"}
MID = {"news", "ted", "academic"}


def triage(seed: dict) -> dict:
    cr = (seed.get("copyright") or "").strip()
    author = (seed.get("author") or "").strip()
    dt = seed["day_type"]

    if SELF_AUTHORED.search(cr):
        # 자체 작성물은 계열과 무관하게 안전 (ADR-010 §1)
        return {"action": "keep", "reason": f"copyright='{cr}' — 자체 작성"}

    if dt in HIGH:
        return {"action": "rewrite", "reason": "ADR-010 고위험 계열 — 재작성 교체"}
    if dt in MID:
        return {"action": "rewrite", "reason": f"ADR-010 중간~고위험 계열 (copyright='{cr or '표기없음'}')"}

    # quote — 저자 귀속으로 판정 (copyright 필드는 신뢰 불가)
    if ANONYMOUS.match(author):
        return {"action": "keep", "reason": f"저자 미귀속('{author or '표기없음'}') — 저작물성 약함"}
    return {
        "action": "review",
        "reason": f"quote, 저자 '{author}' — 사후 70년 경과 여부 확인 필요 (copyright='{cr}'는 신뢰 불가)",
    }


def main() -> None:
    seeds = read_jsonl(WORK_DIR / "c1_full_seeds.jsonl")
    done = {s["seed_id"] for s in read_jsonl(WORK_DIR.parents[1] / "output" / "c1_final.jsonl")}

    out = []
    for s in seeds:
        t = triage(s)
        if s["id"] in done:
            t = {"action": "done", "reason": "파일럿에서 처리 완료"}
        out.append(s | {"triage": t})

    # 사용자 결정 2026-08-06: `review`(실명 저자 quote)도 재작성한다.
    # 사망연도 확인 비용보다 재작성이 확실하고, 광고 모델이라 인용 항변이 불리하다(ADR-010).
    targets = [s for s in out if s["triage"]["action"] in ("rewrite", "review")]
    write_jsonl(WORK_DIR / "c1_rewrite_targets.jsonl", targets)
    write_jsonl(WORK_DIR / "c1_triaged.jsonl", out)

    actions = Counter(s["triage"]["action"] for s in out)
    by_type = Counter((s["day_type"], s["triage"]["action"]) for s in out)
    by_cefr = Counter(s.get("cefr_level") for s in targets)
    keep_reasons = Counter(s["triage"]["reason"] for s in out if s["triage"]["action"] == "keep")

    report = f"""# s15 — C-1 확대 대상 선별 (2026-08-06)

생성: {datetime.now(timezone.utc).isoformat(timespec='seconds')}

ADR-010 처리 기준표는 계열별로 다르고, quote는 **"만료·저작물성 약한 것 선별, 나머지 재생성"** 이다.
선별을 건너뛰고 전량 재작성하면 자체 작성 문장까지 불필요하게 바꾸게 된다.

## ⚠️ `sources.copyright` 필드는 신뢰할 수 없다 (실측)

`copyright='Public'`으로 표기된 quote 중에 이런 것들이 있었다:

| id | 문장 | 저자 | 연도 |
|---|---|---|---|
| M13_001 | The only way to do great work is to love what… | **Steve Jobs** | 2005 |
| M13_017 | What I can point out is the importance of edu… | **Malala Yousafzai** | 2013 |

둘 다 퍼블릭 도메인이 **아니다**. 생존 인물이거나 사후 70년이 한참 남았다.
필드만 믿고 `keep` 하면 저작권물을 그대로 공개하게 된다 — ADR-010이 경고한
"사후 70년 미경과 인물의 명언은 주의"에 정면으로 걸린다.

**따라서 quote는 `copyright` 필드가 아니라 저자 귀속으로 판정한다.**
저자가 Unknown·Traditional·Common Saying 등 특정인에게 귀속되지 않으면 저작물성이 약해 유지(ADR-010),
실명 저자면 사후 70년 경과 여부를 **사람이 확인**해야 한다(`review`).

## 선별 결과 — 위험 계열 {len(seeds)}건

| 처리 | 건수 | 의미 |
|---|---|---|
{chr(10).join(f"| {k} | {v} | {'재작성 대상' if k == 'rewrite' else '유지(안전 표기)' if k == 'keep' else '파일럿 처리 완료' if k == 'done' else '사람 판단 필요'} |" for k, v in actions.most_common())}

**재작성 대상 {len(targets)}건** — 전량 재작성했을 때보다 **{len(seeds) - len(targets)}건 절감**.

### 계열별

| 계열 | rewrite | keep | review | done |
|---|---|---|---|---|
{chr(10).join(f"| {dt} | {by_type.get((dt, 'rewrite'), 0)} | {by_type.get((dt, 'keep'), 0)} | {by_type.get((dt, 'review'), 0)} | {by_type.get((dt, 'done'), 0)} |" for dt in sorted({s['day_type'] for s in out}))}

### 유지 사유 (상위)

| 사유 | 건수 |
|---|---|
{chr(10).join(f"| {r} | {n} |" for r, n in keep_reasons.most_common(10))}

## 재작성 대상의 CEFR 분포 — 레벨별 처리가 필요하다

| CEFR | 건수 |
|---|---|
{chr(10).join(f"| {k} | {v} |" for k, v in sorted(by_cefr.items(), key=lambda kv: str(kv[0])))}

파일럿은 A1(year1)만 다뤘고 허용 어휘 목록도 A1 기준이다.
**A2·B1·B2는 해당 연차 커리큘럼으로 [s13](12_allowlist_expansion.md)을 다시 돌려 레벨별 목록을 만든 뒤** 진행해야 한다.
그렇지 않으면 게이트가 정상 어휘를 대량 탈락시킨다.

## 결정 — `review` 77건도 재작성 (2026-08-06)

실명 저자 quote는 사후 70년 경과를 확인해야 keep 가능하지만, **전량 재작성**을 선택했다.
근거: 사망연도 확인 비용보다 재작성이 확실하고, 광고 모델이라 인용(제28조)·공정이용 항변이
모두 불리하다(ADR-010). 따라서 재작성 대상 = `rewrite` + `review` = **{len(targets)}건**.

## 다음

1. A1 대상분({by_cefr.get('A1', 0)}건) 먼저 재작성해 파이프라인 검증 — A2~B2는 처음 도는 레벨이다.
2. 검증 후 A2·B1·B2로 확대 (레벨별 허용 목록은 [s13](12_allowlist_expansion.md)에서 구축 완료).
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "14_c1_triage.md").write_text(report, encoding="utf-8")

    print(f"위험 계열 {len(seeds)}건 → {dict(actions)}")
    print(f"재작성 대상 {len(targets)}건 (CEFR: {dict(by_cefr)})")
    print("→ reports/14_c1_triage.md")


if __name__ == "__main__":
    main()
