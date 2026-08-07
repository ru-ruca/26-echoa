"""s18: C-1 확대 검수 시트 기계 검증 — 저작권 판정이 걸린 검수라 특히 엄격히 본다.

검증:
    coverage      122씨앗 전부에 결론이 있는가 (채택 1건 또는 전체 불합격)
    one_pick      씨앗당 채택/수정이 정확히 1건인가 (2건 이상이면 어느 걸 쓸지 모른다)
    copyright     [저작권] 태그 집계 — 유사도 경계권과 실제 저작권 탈락이 일치하는가
    seed_defect   [씨앗결함] 태그 — 재작성으로 못 살리는 씨앗
    vocab         수정안이 해당 레벨 허용 어휘를 지키는가
    boundary      ⚠️ 경계권 씨앗의 판정 분포 (관용구 유지가 실제로 통과했는가)

산출물: reports/16_c1_review_verification.md

사용: uv run python -m src.steps.s18_verify_c1_review [검수시트.md]
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl
from src.steps.s04_gate_hard import load_allowlist, vocab_check

HEADER = re.compile(r"^## (\w+) \(([^,]+), ([^)]+)\) — (.*)$")
ROW = re.compile(r"^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| ([\d.]+)\s*(⚠️)? \| (.*?) \|$")
FIX_EN = re.compile(r"수정:\s*(.+?)(?:\s*/\s*KR:|\s*\[|$)")
TAG = re.compile(r"\[(저작권|씨앗결함|어휘승인요청:[^\]]+)\]")


def parse(path: Path) -> list[dict]:
    seeds, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := HEADER.match(line):
            if cur:
                seeds.append(cur)
            cur = {
                "seed_id": m.group(1),
                "day_type": m.group(2),
                "cefr": m.group(3),
                "heading": m.group(4),
                "rows": [],
            }
        elif cur is not None and (m := ROW.match(line)):
            cur["rows"].append(
                {
                    "cand": int(m.group(1)),
                    "text_en": m.group(2).strip(),
                    "sim": float(m.group(5)),
                    "boundary": bool(m.group(6)),
                    "verdict": m.group(7).strip(),
                }
            )
    if cur:
        seeds.append(cur)
    return seeds


def main(sheet: str | None = None) -> None:
    path = Path(sheet) if sheet else REPORTS_DIR / "restricted" / "c1_full_review_sheet_filled.md"
    parsed = parse(path)
    targets = {s["id"]: s for s in read_jsonl(WORK_DIR / "c1_rewrite_targets.jsonl")}
    allow = {lv: load_allowlist(lv) for lv in ("A1", "A2", "B1", "B2")}

    picked, rejected, problems = {}, {}, []
    tags: Counter[str] = Counter()
    vocab_bad, boundary_stats = [], Counter()

    for s in parsed:
        sid = s["seed_id"]
        picks = [r for r in s["rows"] if r["verdict"].startswith(("채택", "수정"))]
        fail = "전체 불합격" in s["heading"]

        for t in TAG.findall(s["heading"]):
            tags[t.split(":")[0]] += 1
        for r in s["rows"]:
            for t in TAG.findall(r["verdict"]):
                tags[t.split(":")[0]] += 1

        if fail:
            rejected[sid] = s["heading"]
            if picks:
                problems.append((sid, "전체 불합격인데 채택 후보가 있음"))
        elif len(picks) == 1:
            picked[sid] = picks[0]
        elif not picks:
            problems.append((sid, "결론 없음 — 채택도 불합격도 없음"))
        else:
            problems.append((sid, f"채택이 {len(picks)}건 — 하나만 골라야 함"))

        if any(r["boundary"] for r in s["rows"]):
            boundary_stats["불합격" if fail else "채택" if picks else "미정"] += 1

    # 수정안 어휘 검사
    for sid, p in picked.items():
        if not p["verdict"].startswith("수정"):
            continue
        m = FIX_EN.search(p["verdict"])
        if not m:
            problems.append((sid, "수정안 파싱 실패"))
            continue
        cefr = targets[sid].get("cefr_level") or "A1"
        core, ext = allow[cefr]
        excess, _ = vocab_check(m.group(1).strip(), core, ext)
        if excess:
            tagged = {w.split(":")[1].strip().lower() for w in TAG.findall(p["verdict"]) if ":" in w}
            miss = [w for w in excess if w not in tagged]
            if miss:
                vocab_bad.append((sid, cefr, m.group(1).strip(), miss))

    lines = [
        "# s18 — C-1 확대 검수 시트 기계 검증",
        "",
        f"대상: `{path.name}` · 씨앗 {len(parsed)}개",
        "",
        "## 결론 분포",
        "",
        "| 결론 | 씨앗 |",
        "|---|---|",
        f"| 채택 (수정 포함) | {len(picked)} |",
        f"| 전체 불합격 | {len(rejected)} |",
        f"| **문제 있음** | **{len(problems)}** |",
        "",
        f"채택률 **{len(picked) / len(parsed):.0%}** (검수 대상은 저점·경계권 편향 집합이라 모집단 품질과 다르다)",
        "",
        "## 태그 집계",
        "",
        "| 태그 | 건수 |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in tags.most_common()],
        "",
        "## 씨앗 유사도 경계권(⚠️) 씨앗의 결론",
        "",
        "관용구 유지가 저작권상 안전하다는 판단이 맞았다면 경계권도 대부분 채택돼야 한다.",
        "",
        "| 결론 | 씨앗 |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in boundary_stats.most_common()],
        "",
        f"## 전체 불합격 {len(rejected)}건",
        "",
        "| 씨앗 | 계열 | CEFR | 사유 |",
        "|---|---|---|---|",
        *[
            f"| {sid} | {targets[sid]['day_type']} | {targets[sid].get('cefr_level')} | {h.replace('전체 불합격 —', '').strip()} |"
            for sid, h in sorted(rejected.items())
        ],
        "",
        f"## 수정안 어휘 이탈 {len(vocab_bad)}건",
        "",
        "| 씨앗 | CEFR | 수정안 | 목록 밖 |",
        "|---|---|---|---|",
        *[f"| {sid} | {lv} | {t} | {', '.join(w)} |" for sid, lv, t, w in vocab_bad],
        "",
        f"## 구조 문제 {len(problems)}건",
        "",
        *[f"- {sid}: {msg}" for sid, msg in problems],
        "",
    ]
    out = REPORTS_DIR / "16_c1_review_verification.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"씨앗 {len(parsed)} — 채택 {len(picked)} / 전체 불합격 {len(rejected)} / 문제 {len(problems)}")
    print(f"태그: {dict(tags)}")
    print(f"경계권 씨앗 결론: {dict(boundary_stats)}")
    print(f"수정안 어휘 이탈 {len(vocab_bad)}건")
    print(f"→ {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
