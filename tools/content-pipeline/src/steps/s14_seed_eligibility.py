"""s14: 씨앗 적격성 자동 분류 — 부적격 씨앗의 생성·채점 비용을 미리 없앤다.

파일럿에서 셋 다 같은 결론에 도달했다: **어떤 씨앗을 넣느냐가 결과를 지배한다.**
그런데 판별이 judge 사후에 이뤄져, C-2에서 부적격 씨앗 24개 × 6 = 144건을 생성·채점한 뒤 버렸다.
이 단계는 style_lessons §13~19를 **생성 전에** 적용한다.

판정 (c2_eligible / c3_eligible):
    narrative        서사체 도치·인용문("…," said X) → C-2·C-3 모두 부적격 (§17·§19)
    proverb_type     day_type='proverb' → C-2 부적격, C-3 적격 (§13·§18)
    fossilized       화석화 관용구(고유명사 의존 포함) → C-2 부적격 (§14·§15)
    over_a1          고정부가 A1 초과(비교급·최상급·자유관계절) → C-2 부적격 (§16)
    too_long         12단어 초과 → 양쪽 부적격 (턴·변형 상한)
    duplicate_seed   같은 문장이 다른 씨앗에 이미 있음 → 후순위 중복 제거

기계 판별은 보수적으로 — 애매하면 적격으로 두고 judge·검수에 맡긴다.
확실한 부적격만 걸러도 파일럿 실측 기준 생성량의 상당 부분을 아낀다.

사용: uv run python -m src.steps.s14_seed_eligibility [씨앗.jsonl]
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl, write_jsonl
from src.lib.similarity import tokens

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

_SAY_VERBS = "said|cried|laughed|thought|asked|replied|shouted|answered|whispered"
# 서사체 인용 꼬리표 — 두 어순 모두: "…," said the Ant. / "…!" she said.
NARRATIVE_TAG = re.compile(
    rf"\b((({_SAY_VERBS})\s+(the\s+)?\w+)|((he|she|they|\w+)\s+({_SAY_VERBS})))\s*[.!?]?\s*$",
    re.IGNORECASE,
)
# 우화 인물 표기 — 관사 + 대문자 보통명사(the Lion, a Mouse). 일상 발화에는 거의 없다.
FABLE_CHARACTER = re.compile(r"\b(the|a|an)\s+([A-Z]\w+)")
# 위 패턴의 오탐 방지 — 실제 고유명사 계열은 우화 인물이 아니다
PROPER_OK = {
    "English", "Korean", "Korea", "America", "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December", "Internet",
}
# 비축약형 — style_lessons §1 위반이 씨앗에서 상속된다
UNCONTRACTED = re.compile(
    r"\b(I am|you are|we are|they are|it is|he is|she is|do not|does not|did not|"
    r"will not|cannot|can not|is not|are not|let us)\b",
    re.IGNORECASE,
)
# 비교급·최상급·자유관계절 (§16)
OVER_A1 = [
    (re.compile(r"\b(more|most|less|least)\s+\w+", re.I), "비교급/최상급"),
    (re.compile(r"\bthe\s+(best|worst|biggest|largest|first)\b", re.I), "최상급"),
    (re.compile(r"\w+(er|est)\s+than\b", re.I), "비교급"),
    (re.compile(r"\bwhat\s+you\s+can\b", re.I), "자유관계절"),
]
# 고유명사 의존 관용구 (§14) — 문장 기능이 특정 고유명사에 걸려 있는 것
PROPER_DEPENDENT = re.compile(r"\b(Rome|Romans|Greek|Trojan)\b")
# 화석화 관용구 (§15)
FOSSILIZED = [
    "happily ever after",
    "cats and dogs",
    "once upon a time",
    "the early bird",
]
MAX_WORDS = 12


def classify(seed: dict, seen_texts: dict[str, str]) -> dict:
    text = seed["text_en"]
    norm = " ".join(tokens(text))
    reasons_c2, reasons_c3 = [], []

    if NARRATIVE_TAG.search(text.rstrip()):
        reasons_c2.append("narrative")
        reasons_c3.append("narrative")

    # 약어(TV·PC)는 전부 대문자라 우화 인물이 아니다
    if any(
        m.group(2) not in PROPER_OK and not m.group(2).isupper()
        for m in FABLE_CHARACTER.finditer(text)
    ):
        reasons_c2.append("fable_character")
        reasons_c3.append("fable_character")

    if UNCONTRACTED.search(text):
        reasons_c2.append("uncontracted")  # 씨앗 교정 대상 (§1)

    if seed.get("day_type") == "proverb":
        reasons_c2.append("proverb_type")  # C-3는 적격 (§18)

    if any(f in text.lower() for f in FOSSILIZED):
        reasons_c2.append("fossilized")
    if PROPER_DEPENDENT.search(text):
        reasons_c2.append("proper_dependent")

    for pat, label in OVER_A1:
        if pat.search(text):
            reasons_c2.append(f"over_a1:{label}")
            break

    if len(tokens(text)) > MAX_WORDS:
        reasons_c2.append("too_long")
        reasons_c3.append("too_long")

    dup_of = seen_texts.get(norm)
    if dup_of:
        reasons_c2.append(f"duplicate_of:{dup_of}")
        reasons_c3.append(f"duplicate_of:{dup_of}")
    else:
        seen_texts[norm] = seed["id"]

    return {
        "c2_eligible": not reasons_c2,
        "c3_eligible": not reasons_c3,
        "c2_reasons": reasons_c2,
        "c3_reasons": reasons_c3,
    }


def main(seed_file: str | None = None) -> None:
    src = Path(seed_file) if seed_file else WORK_DIR / "c2_seeds.jsonl"
    seeds = read_jsonl(src)

    seen: dict[str, str] = {}
    out = [s | {"eligibility": classify(s, seen)} for s in seeds]
    dst = WORK_DIR / f"{src.stem}_eligibility.jsonl"
    write_jsonl(dst, out)

    c2_ok = sum(1 for s in out if s["eligibility"]["c2_eligible"])
    c3_ok = sum(1 for s in out if s["eligibility"]["c3_eligible"])
    c2_reasons = Counter(r.split(":")[0] for s in out for r in s["eligibility"]["c2_reasons"])
    c3_reasons = Counter(r.split(":")[0] for s in out for r in s["eligibility"]["c3_reasons"])

    # 파일럿 실측과 대조 — 이 규칙이 실제로 부적격 씨앗을 잡았는가
    validation = ""
    final_file = OUTPUT_DIR / "c2_final.jsonl"
    if final_file.exists():
        # 올바른 기준: judge 점수가 아니라 **확정본에 기여했는가**.
        # judge는 M01_005(4.20)·M01_016(4.33)을 높게 줬지만 인간 검수가 씨앗결함으로 버렸다.
        final = read_jsonl(final_file)
        productive = {f["seed_id"] for f in final}
        all_ids = {s["id"] for s in out}
        barren = all_ids - productive  # 생성했으나 확정본에 한 건도 못 남긴 씨앗
        flagged = {s["id"] for s in out if not s["eligibility"]["c2_eligible"]}
        hit = flagged & barren
        cost = flagged & productive
        saved_variants = len(hit) * 6
        validation = f"""
## 규칙 검증 — 파일럿 실측 대조 (C-2)

기준은 judge 점수가 아니라 **확정본에 기여했는가**다. judge는 M01_005(4.20)·M01_016(4.33)을
높게 줬지만 인간 검수가 씨앗결함으로 버렸다 — judge 점수만으로 판정하면 규칙을 과소평가하게 된다.

| 항목 | 값 |
|---|---|
| 씨앗 전체 | {len(all_ids)} |
| 확정본에 **한 건도 못 남긴** 씨앗(무익) | {len(barren)} |
| 규칙이 부적격 판정 | {len(flagged)} |
| **무익 씨앗을 미리 잡음** | **{len(hit)} / {len(barren)} ({len(hit) / max(1, len(barren)):.0%})** |
| 생산적 씨앗을 잘못 차단 | {len(cost)} — {sorted(cost)} |

규칙을 생성 전에 적용했다면 **변형 약 {saved_variants}건**(무익 씨앗 {len(hit)}개 × 6)의
생성·채점 비용을 아꼈다. 잘못 차단하는 {len(cost)}개는 손실이지만, 대부분 인간 검수가
씨앗결함·부적격으로 판정했던 계열이라 실질 손실은 그보다 작다.

놓친 무익 씨앗 {len(barren - flagged)}개는 3인칭 과거 서사·의미 판단이 필요한 것들로,
기계로는 판별이 어렵다 — judge·검수가 사후에 거른다(2중 안전망).
"""

    report = f"""# s14 — 씨앗 적격성 자동 분류 (2026-08-06)

씨앗 {len(seeds)}개를 style_lessons §13~19 규칙으로 생성 **전에** 판별한다.
파일럿에서는 judge 사후에 걸러 C-2 부적격 씨앗 24개 × 6 = 144건을 만들고 버렸다.

## 판정 결과

| 트랙 | 적격 | 부적격 |
|---|---|---|
| C-2 (슬롯 치환) | {c2_ok} | {len(seeds) - c2_ok} |
| C-3 (대화) | {c3_ok} | {len(seeds) - c3_ok} |

### C-2 부적격 사유

| 사유 | 씨앗 |
|---|---|
{chr(10).join(f"| {k} | {v} |" for k, v in c2_reasons.most_common())}

### C-3 부적격 사유

| 사유 | 씨앗 |
|---|---|
{chr(10).join(f"| {k} | {v} |" for k, v in c3_reasons.most_common()) or "| (없음) | 0 |"}
{validation}
## 설계 원칙

**보수적으로 판별한다** — 애매하면 적격으로 두고 judge·검수에 맡긴다.
기계가 확실히 아는 것(서사체 꼬리표·고유명사 의존·화석화 관용구·길이·중복)만 거르고,
"이 문장이 실제 발화인가" 같은 판단은 사람과 judge의 몫으로 남긴다.
과잉 차단은 좋은 콘텐츠를 잃지만, 과소 차단은 생성·채점 비용만 쓰고 어차피 걸러진다.

## 운영

생성 배치를 만들 때 `eligibility.c2_eligible` / `c3_eligible`로 씨앗을 거른다.
부적격 씨앗은 통청크 암기 자산으로 유지하거나(§19) 해당 트랙만 건너뛴다(§18).
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "13_seed_eligibility.md").write_text(report, encoding="utf-8")

    print(f"{dst.name}  씨앗 {len(seeds)} — C-2 적격 {c2_ok} / C-3 적격 {c3_ok}")
    print(f"C-2 부적격 사유: {dict(c2_reasons)}")
    print("→ reports/13_seed_eligibility.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
