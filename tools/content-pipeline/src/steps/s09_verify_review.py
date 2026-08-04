"""s09: 검수 시트 회수 전 기계 검증 — 판정 커버리지와 수정안의 규칙 준수를 확인한다.

C-2 검수의 최대 위험: 검수자가 자연스러운 영어로 고치면서 **패턴 고정부를 깨는 것**.
고정부가 깨진 수정안은 substitution drill이 아니라 그냥 다른 문장이고,
고정부 자체가 문제라면 개별 변형이 아니라 **씨앗을 고쳐야** 한다.

검증 항목:
    coverage      208건 전부에 판정이 있는가
    pattern_broken 수정안이 패턴 고정부를 유지하는가
    vocab          수정안이 허용 어휘를 지키는가
    seed_level     같은 씨앗에서 같은 고정부 결함이 반복 지적됐는가 (씨앗 결함 신호)

사용: uv run python -m src.steps.s09_verify_review <검수시트.md>
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from src.lib.jsonl import REPORTS_DIR, WORK_DIR, read_jsonl
from src.steps.s04_gate_hard import contains_in_order, fixed_segments, load_allowlist, vocab_check

SEED_HEADER = re.compile(r"^## (\w+) \(")
PATTERN_LINE = re.compile(r"^- 패턴: `(.+)`")
ROW = re.compile(r"^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.*?) \|$")
FIX_EN = re.compile(r"수정:\s*(.+?)(?:\s*/\s*KR:|\s*\[어휘승인요청|$)")
SEED_ALT = re.compile(r"대안 씨앗:\s*(.+?)\s*$")
VOCAB_REQ = re.compile(r"\[어휘승인요청:\s*([^\]]+)\]")


def parse(path: Path) -> list[dict]:
    rows, seed_id, pattern = [], None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := SEED_HEADER.match(line):
            seed_id = m.group(1)
        elif m := PATTERN_LINE.match(line):
            pattern = m.group(1)
        elif (m := ROW.match(line)) and seed_id:
            rows.append(
                {
                    "seed_id": seed_id,
                    "cand": int(m.group(1)),
                    "pattern": pattern,
                    "text_en": m.group(2).strip(),
                    "verdict_raw": m.group(6).strip(),
                }
            )
    return rows


def classify(verdict: str) -> str:
    """v1(합격·수정·불합격)과 v2(씨앗결함·수정(KR만) 추가) 양쪽을 인식한다."""
    if not verdict:
        return "미판정"
    for prefix in ("씨앗결함", "수정(KR만)", "수정", "불합격", "합격"):
        if verdict.startswith(prefix):
            return prefix
    return "기타"


def sample_split(rows: list[dict]) -> tuple[Counter, Counter]:
    """무작위 샘플군과 judge 저점군의 판정 분포를 분리한다.

    23 §5의 합격률은 **무작위 샘플**로만 판정해야 한다 — 저점군은 의도적으로
    편향 추출된 집합이라 그 합격률은 모집단 품질이 아니다.
    """
    import random

    from src.steps.s06_report import JUDGE_TARGET, SAMPLE_RATE, SAMPLE_SEED, SEED_ELIGIBLE_MIN

    judged = {(j["seed_id"], j["cand"]): j for j in read_jsonl(WORK_DIR / "c2_judged.jsonl")}
    seed_avgs: dict[str, list[float]] = {}
    for (sid, _c), j in judged.items():
        seed_avgs.setdefault(sid, []).append(j["avg"])
    from statistics import mean as _mean

    ineligible = {sid for sid, v in seed_avgs.items() if _mean(v) < SEED_ELIGIBLE_MIN}
    eligible = {k: j for k, j in judged.items() if k[0] not in ineligible}
    low = {k for k, j in eligible.items() if j["avg"] < JUDGE_TARGET}
    rest = [k for k, j in eligible.items() if j["avg"] >= JUDGE_TARGET]
    sample = set(random.Random(SAMPLE_SEED).sample(rest, max(1, int(len(rest) * SAMPLE_RATE))))

    verdicts = {(r["seed_id"], r["cand"]): classify(r["verdict_raw"]) for r in rows}
    return (
        Counter(verdicts.get(k, "미수록") for k in sample),
        Counter(verdicts.get(k, "미수록") for k in low),
    )


def main(sheet: str) -> None:
    path = Path(sheet)
    rows = parse(path)
    core, extended = load_allowlist()
    seeds = {s["id"]: s for s in read_jsonl(WORK_DIR / "c2_seeds.jsonl")}

    dist = Counter(classify(r["verdict_raw"]) for r in rows)
    sample_dist, low_dist = sample_split(rows)

    # v2 산출물: 씨앗결함 판정과 어휘 승인 요청
    seed_defects: dict[str, dict] = {}
    for r in rows:
        if classify(r["verdict_raw"]) != "씨앗결함":
            continue
        d = seed_defects.setdefault(r["seed_id"], {"rows": 0, "reason": "", "alt": ""})
        d["rows"] += 1
        reason = r["verdict_raw"].removeprefix("씨앗결함").lstrip("— ").split(" / 대안 씨앗:")[0]
        d["reason"] = d["reason"] or reason.strip()
        if m := SEED_ALT.search(r["verdict_raw"]):
            d["alt"] = d["alt"] or m.group(1).strip()
    vocab_requests = Counter(
        w.strip() for r in rows for w in VOCAB_REQ.findall(r["verdict_raw"])
    )
    # 씨앗결함이 그 씨앗의 전 행에 표기됐는가 (프롬프트 v2 요구사항)
    rows_per_seed = Counter(r["seed_id"] for r in rows)
    partial_defects = [
        (sid, d["rows"], rows_per_seed[sid])
        for sid, d in seed_defects.items()
        if d["rows"] != rows_per_seed[sid]
    ]
    broken, vocab_bad, unparsed = [], [], []
    per_seed_fix = defaultdict(list)

    for r in rows:
        kind = classify(r["verdict_raw"])
        if kind != "수정":
            continue
        m = FIX_EN.search(r["verdict_raw"])
        if not m:
            unparsed.append(r)
            continue
        fixed = m.group(1).strip()
        segs = fixed_segments(r["pattern"] or "")
        if segs and not contains_in_order(fixed, segs):
            broken.append((r, fixed))
            per_seed_fix[r["seed_id"]].append(fixed)
        ext_excess, core_excess = vocab_check(fixed, core, extended)
        if ext_excess:
            vocab_bad.append((r, fixed, ext_excess))

    lines = [
        "# s09 — 검수 시트 기계 검증",
        "",
        f"대상: `{path.name}` · 판정 {len(rows)}건",
        "",
        "## 판정 분포",
        "",
        "| 판정 | 건수 |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in dist.most_common()],
        "",
        "### 23 §5 합격률은 무작위 샘플로만 판정한다",
        "",
        "저점군은 judge<4.0으로 **의도적으로 편향 추출**한 집합이라 그 합격률은 모집단 품질이 아니다.",
        "모집단 추정치는 무작위 샘플뿐이다.",
        "",
        "| 집합 | 합격 | 수정 | 불합격 | 합격률 | 합격+수정 |",
        "|---|---|---|---|---|---|",
        *[
            f"| {label} ({sum(d.values())}건) | {d['합격']} | {d['수정']} | {d['불합격']} | "
            f"**{d['합격'] / max(1, sum(d.values())):.0%}** | {(d['합격'] + d['수정']) / max(1, sum(d.values())):.0%} |"
            for label, d in (("무작위 샘플", sample_dist), ("judge 저점군", low_dist))
        ],
        "",
        "## 패턴 고정부를 깨는 수정안",
        "",
        f"**{len(broken)}건** — 고정부를 바꾼 수정은 substitution drill이 아니다.",
        "고정부 자체가 비관용이면 개별 변형이 아니라 **씨앗을 교체**해야 한다.",
        "",
        "| 씨앗 | cand | 패턴 | 수정안 |",
        "|---|---|---|---|",
        *[f"| {r['seed_id']} | {r['cand']} | `{r['pattern']}` | {f} |" for r, f in broken],
        "",
        "### 같은 씨앗에서 2건 이상 고정부가 깨진 경우 = 씨앗 결함",
        "",
        "| 씨앗 | 건수 | 씨앗 원문 |",
        "|---|---|---|",
        *[
            f"| {sid} | {len(v)} | {seeds[sid]['text_en']} |"
            for sid, v in sorted(per_seed_fix.items(), key=lambda kv: -len(kv[1]))
            if len(v) >= 2
        ],
        "",
        "## 허용 어휘를 벗어난 수정안",
        "",
        f"**{len(vocab_bad)}건**",
        "",
        "| 씨앗 | cand | 수정안 | 목록 밖 |",
        "|---|---|---|---|",
        *[f"| {r['seed_id']} | {r['cand']} | {f} | {', '.join(e)} |" for r, f, e in vocab_bad],
        "",
        f"## 수정안 파싱 실패 {len(unparsed)}건",
        "",
        *[f"- {r['seed_id']} c{r['cand']}: `{r['verdict_raw'][:80]}`" for r in unparsed],
        "",
        f"## 씨앗결함 판정 {len(seed_defects)}개 씨앗 (v2)",
        "",
        "검수자가 '고정부 자체가 문제'로 판정한 씨앗. 변형 수정으로 해결되지 않아 씨앗 교체·폐기 대상.",
        "",
        "| 씨앗 | 표기 행 | 씨앗 원문 | 사유 | 대안 씨앗 |",
        "|---|---|---|---|---|",
        *[
            f"| {sid} | {d['rows']}/{rows_per_seed[sid]} | {seeds[sid]['text_en']} | {d['reason']} | {d['alt'] or '—'} |"
            for sid, d in sorted(seed_defects.items())
        ],
        "",
        f"부분 표기(일부 행에만 씨앗결함) **{len(partial_defects)}건** — v2 규칙은 전 행 표기를 요구한다."
        + (f" {partial_defects}" if partial_defects else ""),
        "",
        f"## 어휘 승인 요청 {len(vocab_requests)}건 (v2)",
        "",
        "| 단어 | 요청 횟수 |",
        "|---|---|",
        *[f"| {w} | {n} |" for w, n in vocab_requests.most_common()],
        "",
    ]
    out = REPORTS_DIR / "06_c2_review_verification.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"판정 {len(rows)}건 — {dict(dist)}")
    print(f"패턴 고정부 파괴 수정안 {len(broken)}건 / 어휘 이탈 {len(vocab_bad)}건 / 파싱 실패 {len(unparsed)}건")
    print(f"씨앗 결함 신호(같은 씨앗 2건 이상): {sum(1 for v in per_seed_fix.values() if len(v) >= 2)}개 씨앗")
    print(f"→ {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(REPORTS_DIR / "c2_review_sheet_filled.md"))
