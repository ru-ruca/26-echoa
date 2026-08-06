"""s13: A1 허용 어휘 목록 보강 — 매 라운드 개별 승인의 병목을 없앤다.

문제: 게이트의 허용 목록이 `A1 사전(419) ∪ M01~03 실등장(122)`이라 좁다.
생성기가 tonight·weekend·taxi·neighbor·left·story 같은 **일상어에서 계속 막히고**,
그때마다 인간이 한 단어씩 승인해 왔다(C-1 3개 → C-2 14개 → C-3에서도 반복).

근거: **year1(M01~12) 904문장이 전부 `cefr_level='A1'`** 이다. 커리큘럼 설계자가
"A1 학습자에게 내보내도 된다"고 판정한 문장들이므로, **그 문장들이 쓰는 단어는 A1 적정**이다.
외부 워드리스트를 들여오지 않고 우리 자산만으로 검증 가능한 기준을 세운다.

    expanded = A1 사전 ∪ year1 커리큘럼 실등장 content lemma

산출물:
    output/allowlist_a1_expanded.json   (s04가 extended에 병합)
    reports/12_allowlist_expansion.md   확장 효과 실측 (C-2 탈락분 회수율)

사용: uv run python -m src.steps.s13_expand_allowlist
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl
from src.lib.textproc import content_lemmas

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"


def build_level_allowlists() -> dict:
    """CEFR 레벨별 허용 어휘 — 연차와 CEFR이 1:1이라(year1=A1 … year4=B2) 누적으로 쌓는다.

    A2 학습자는 A1에서 배운 것도 아니까 상위 레벨은 하위를 포함한다.
    C-1 재작성 대상이 A1~B2에 걸쳐 있어 레벨별 목록이 없으면 게이트가 정상 어휘를 대량 탈락시킨다.
    """
    sentences = read_jsonl(WORK_DIR / "sentences_by_level.jsonl")
    vocab = read_jsonl(WORK_DIR / "vocabulary.jsonl")

    by_level: dict[str, set[str]] = {}
    for s in sentences:
        by_level.setdefault(s["cefr_level"], set()).update(content_lemmas(s["text_en"]))
    dict_by_level: dict[str, set[str]] = {}
    for v in vocab:
        if v.get("word") and v.get("cefr_level"):
            dict_by_level.setdefault(v["cefr_level"], set()).add(v["word"].strip().lower())

    order = ["A1", "A2", "B1", "B2"]
    cumulative: set[str] = set()
    out = {}
    for lv in order:
        cumulative |= by_level.get(lv, set()) | dict_by_level.get(lv, set())
        out[lv] = sorted(cumulative)
    return out


def main() -> None:
    base = json.loads((WORK_DIR / "allowlist_m01_03.json").read_text(encoding="utf-8"))
    core = set(base["core"])
    pilot_extra = set(base["extended_extra"])
    approved = {
        w["lemma"]
        for w in json.loads((OUTPUT_DIR / "allowlist_human_approved.json").read_text(encoding="utf-8"))["words"]
    }
    before = core | pilot_extra | approved

    year1 = read_jsonl(WORK_DIR / "sentences_year1.jsonl")
    freq: Counter[str] = Counter()
    for s in year1:
        freq.update(content_lemmas(s["text_en"]))
    year1_lemmas = set(freq)
    new = sorted(year1_lemmas - before)

    payload = {
        "note": "A1 허용 어휘 확장 — year1(M01~12) 커리큘럼 실등장 content lemma. "
        "year1 904문장이 전부 cefr_level='A1'이라 그 어휘는 A1 적정으로 본다.",
        "basis": {
            "year1_sentences": len(year1),
            "all_a1_labeled": True,
            "source": "legacy sentences (month<=12), 2026-08-06 추출",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "added": len(new),
        "lemmas": new,
        "frequency": {w: freq[w] for w in new},
    }
    (OUTPUT_DIR / "allowlist_a1_expanded.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # 확장 효과 — 게이트 산출물이 아니라 후보 원본에서 직접 계산한다.
    # (게이트 파일을 읽으면 이미 확장이 반영된 상태라 순환 참조가 된다)
    after = before | year1_lemmas
    candidates = read_jsonl(WORK_DIR / "c2_candidates.jsonl")
    vocab_failed, recovered = [], []
    still_out: Counter[str] = Counter()
    for c in candidates:
        excess_before = [lm for lm in content_lemmas(c["text_en"]) if lm not in before]
        if not excess_before:
            continue
        vocab_failed.append(c)
        remaining = [lm for lm in excess_before if lm not in after]
        if remaining:
            still_out.update(remaining)
        else:
            recovered.append(c)

    report = f"""# s13 — A1 허용 어휘 목록 확장 (2026-08-06)

## 근거

year1(M01~12) 커리큘럼 **904문장이 전부 `cefr_level='A1'`** 이다.
커리큘럼 설계자가 A1 학습자에게 내보내도 된다고 판정한 문장들이므로, **그 문장들이 쓰는 단어는 A1 적정**이다.
외부 워드리스트를 들여오지 않고 우리 자산만으로 검증 가능한 기준이다.

## 확장 결과

| 집합 | 크기 |
|---|---|
| A1 사전(core) | {len(core)} |
| M01~03 실등장(파일럿 extended_extra) | {len(pilot_extra)} |
| 인간 승인 누적 | {len(approved)} |
| **확장 전 합계** | **{len(before)}** |
| **year1 실등장 신규 추가** | **+{len(new)}** |
| **확장 후 합계** | **{len(after)}** |

## 확장 효과 — C-2 어휘 탈락분 회수

| 지표 | 값 |
|---|---|
| C-2에서 `vocab_extended`로 탈락 | {len(vocab_failed)}건 |
| **확장 목록으로 회수 가능** | **{len(recovered)}건 ({len(recovered) / max(1, len(vocab_failed)):.0%})** |
| 여전히 목록 밖 | {len(vocab_failed) - len(recovered)}건 |

### 확장 후에도 목록 밖인 lemma (상위 20)

| lemma | 탈락 유발 |
|---|---|
{chr(10).join(f"| {w} | {n} |" for w, n in still_out.most_common(20))}

이들은 year1 커리큘럼이 쓰지 않는 단어다 — 생성기가 임의로 끌어온 것이므로 **탈락이 정상**이다.
확장 목록은 "커리큘럼이 실제로 A1에서 쓰는 어휘"라는 경계를 유지한다.

## 신규 추가 어휘 빈도 상위 30

| lemma | year1 등장 |
|---|---|
{chr(10).join(f"| {w} | {freq[w]} |" for w in sorted(new, key=lambda x: -freq[x])[:30])}

## 운영

- `s04_gate_hard.load_allowlist()`가 이 파일을 extended에 병합한다 (인간 승인 목록과 동일 방식).
- 월 단위 확대 시 해당 연차 문장으로 다시 돌리면 된다 (year2는 A2, year3~4는 B1·B2 — 레벨별로 분리 적용).

### 적용 범위 — 앞으로만, 소급 아님

확장 목록은 **이후 라운드(C-1 341 확대·월 단위 확대)에 적용**한다.
이미 확정된 [c2_final.jsonl](../output/c2_final.jsonl) 528건에는 소급하지 않는다 —
회수 가능한 {len(recovered)}건은 **인간 검수를 거치지 않은 후보**라, 검수 없이 합류시키면
"노출 전 전량 검수"(23 §4) 원칙이 깨진다. 필요하면 별도 라운드로 judge·검수를 태워 합류시킨다.
"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "12_allowlist_expansion.md").write_text(report, encoding="utf-8")

    levels = build_level_allowlists()
    (OUTPUT_DIR / "allowlist_by_level.json").write_text(
        json.dumps(
            {
                "note": "CEFR 레벨별 허용 어휘(누적). 연차와 CEFR이 1:1(year1=A1 … year4=B2)이라 "
                "해당 연차까지의 커리큘럼 실등장 어휘 + 사전 어휘를 쌓는다. "
                "상위 레벨은 하위를 포함한다(A2 학습자는 A1 어휘도 안다).",
                "generated_at": payload["generated_at"],
                "sizes": {k: len(v) for k, v in levels.items()},
                "lemmas": levels,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    print(f"output/allowlist_a1_expanded.json  신규 {len(new)}개 (합계 {len(before)} → {len(after)})")
    print(f"C-2 어휘 탈락 {len(vocab_failed)}건 중 {len(recovered)}건 회수 가능 ({len(recovered) / max(1, len(vocab_failed)):.0%})")
    print(f"output/allowlist_by_level.json  레벨별 누적: { {k: len(v) for k, v in levels.items()} }")
    print("→ reports/12_allowlist_expansion.md")


if __name__ == "__main__":
    main()
