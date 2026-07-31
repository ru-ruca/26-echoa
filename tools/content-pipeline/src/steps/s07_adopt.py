"""s07: 인간 검수 회수 — 채택 결정을 후보 데이터와 병합해 확정본을 만든다.

결정 출처: reports/restricted/c1_review_sheet_filled.md (2026-07-31 검수).
결정 테이블을 이 파일에 명시해 감사·재현 가능하게 남긴다 (시트 파싱은 취약해 하지 않음).

산출물 (output/ — 재작성본은 원문 미포함이라 git 추적):
    output/c1_adopted.jsonl        채택 27 (수정 11 반영, content_origin=ai_rewritten)
    output/c1_alternatives.jsonl   검수자 대안 제안 4 (게이트 재검증 대상)

사용: uv run python -m src.steps.s07_adopt c1
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from src.lib.jsonl import WORK_DIR, read_jsonl, write_jsonl

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"

REVIEW_DATE = "2026-07-31"

# seed_id -> (채택 cand, 수정 text_en 또는 None, 수정 text_kr 또는 None, 수정 사유 또는 None)
ADOPTIONS: dict[str, tuple[int, str | None, str | None, str | None]] = {
    "M01_001": (1, None, None, None),
    "M01_011": (1, None, None, None),
    "M01_013": (1, None, None, None),
    "M01_022": (3, None, None, None),
    "M01_024": (1, None, None, None),
    "M01_031": (3, None, None, None),
    "M01_033": (3, None, None, None),
    "M01_040": (1, None, None, None),
    "M01_041": (2, None, None, None),
    "M02_001": (3, "Wake up! It's a great day!", "일어나세요! 멋진 하루예요!",
                "'A great day is here'는 비관용 — 뒷문장 교체"),
    "M02_010": (1, None, None, None),
    "M02_012": (2, None, None, None),
    "M02_020": (1, "Don't worry. Everything will be okay.", "걱정 마세요. 다 괜찮을 거예요.",
                "'All will be well'은 문어·고어체"),
    "M02_022": (3, None, None, None),
    "M02_030": (3, "You never know what will happen tomorrow.", "내일 무슨 일이 있을지는 아무도 몰라요.",
                "'know about tomorrow'는 비관용 — 'You never know'가 표준"),
    "M02_032": (1, "Don't waste your time. It never comes back.", "시간을 낭비하지 마세요. 절대 돌아오지 않아요.",
                "콜로케이션 오류 lose→waste"),
    "M02_039": (1, "I'm always here for you.", None, "축약형 적용"),
    "M02_045": (1, "Don't forget me!", "저를 잊지 마세요!", "'my friend' 호칭 삭제(비원어민 신호)"),
    "M03_001": (3, "Start now, and learn along the way.", "지금 시작하고, 가면서 배워요.",
                "on the way→along the way, Begin→Start(구어 빈도)"),
    "M03_010": (2, "Let's do something fun outside!", "밖에서 재미있는 걸 해 봐요!",
                "find→do something fun(관용성)"),
    "M03_012": (1, None, None, None),
    "M03_021": (2, "I'm happy when I get home.", "집에 돌아오면 행복해요.",
                "come home→get home(귀가 문맥 최빈) + 축약형"),
    "M03_023": (3, "You're my home.", "당신이 저의 집이에요.", "축약형 적용"),
    "M03_032": (1, None, None, None),
    "M03_034": (1, None, None, None),
    "M03_041": (2, "I'll visit you again on Friday.", None, "축약형 적용"),
    "M03_045": (1, None, None, None),
}

# 검수자 대안 제안 — 후보보다 낫다고 판단, 게이트 미검증 상태
ALTERNATIVES: list[dict] = [
    {"seed_id": "M01_031", "text_en": "My family is everything to me.",
     "text_kr": "가족은 저에게 전부예요.", "note": "가족의 소중함을 직접 표현, 감정 밀도 높음"},
    {"seed_id": "M02_012", "text_en": "Just be yourself.",
     "text_kr": "있는 그대로의 당신이면 돼요.", "note": "3단어 고빈도 관용구"},
    {"seed_id": "M02_022", "text_en": "I want to look nice today.",
     "text_kr": "오늘은 멋져 보이고 싶어요.", "note": "'look nice'는 옷차림 대화 최빈 표현"},
    {"seed_id": "M03_034", "text_en": "Something good is coming.",
     "text_kr": "좋은 일이 다가오고 있어요.", "note": "'on the way'보다 쉬운 어휘, 구어 빈도 동등"},
]


def main(mode: str = "c1") -> None:
    if mode != "c1":
        raise SystemExit(f"mode '{mode}'는 아직 미구현")

    candidates = {(c["seed_id"], c["cand"]): c for c in read_jsonl(WORK_DIR / "c1_candidates.jsonl")}
    judged = {(j["seed_id"], j["cand"]): j for j in read_jsonl(WORK_DIR / "c1_judged.jsonl")}

    adopted = []
    for seed_id, (cand, mod_en, mod_kr, reason) in sorted(ADOPTIONS.items()):
        base = candidates[(seed_id, cand)]
        j = judged.get((seed_id, cand), {})
        adopted.append(
            {
                "seed_id": seed_id,
                "source_cand": cand,
                "text_en": mod_en or base["text_en"],
                "text_kr": mod_kr or base["text_kr"],
                "kept_function": base["kept_function"],
                "content_origin": "ai_rewritten",
                "review": {
                    "result": "adopted",
                    "modified": bool(mod_en),
                    "reason": reason,
                    "judge_avg": j.get("avg"),
                    "reviewed_at": REVIEW_DATE,
                },
                "gen_meta": base["gen_meta"] | {"adopted_at": str(date.today())},
            }
        )

    alts = [
        a | {"content_origin": "ai_rewritten", "review": {"result": "reviewer_alternative", "reviewed_at": REVIEW_DATE}}
        for a in ALTERNATIVES
    ]

    n1 = write_jsonl(OUTPUT_DIR / "c1_adopted.jsonl", adopted)
    n2 = write_jsonl(OUTPUT_DIR / "c1_alternatives.jsonl", alts)
    n_mod = sum(1 for a in adopted if a["review"]["modified"])
    print(f"output/c1_adopted.jsonl       {n1}건 (수정 반영 {n_mod})")
    print(f"output/c1_alternatives.jsonl  {n2}건 (게이트 재검증 대상)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c1")
