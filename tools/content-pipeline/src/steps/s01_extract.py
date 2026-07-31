"""s01: legacy DB에서 파일럿(M01~03) 씨앗·어휘·출처를 추출한다.

산출물 (data/work/):
    seeds_m01_03.jsonl     문장 229개 + seed_class 분류
    vocabulary.jsonl       단어 사전 전체 (month 확대 대비)
    sources.jsonl          출처 전체 (copyright 필드 포함 — C-1 선별용)
    sentence_words.jsonl   M01~03 문장-단어 연결

주의: 라이브 sentences 스키마는 코드 선언과 drift가 있다
(expression_ids·updated_at 없음, source_id는 text) — 라이브 컬럼만 조회한다.
"""
from __future__ import annotations

from collections import Counter

from psycopg2.extras import RealDictCursor

from src.db import connect_readonly
from src.lib.jsonl import WORK_DIR, write_jsonl

PILOT_MONTHS = 3

# ADR-010 처리 기준: quote·movie = 재작성, real·tale·proverb = 저위험 유지.
# review는 original_id로 기존 문장 재사용이라 씨앗에서 제외,
# conversation은 기존 대화 자산(C-3 스키마 검증 참조용)으로 분리.
C1_TYPES = {"quote", "movie"}


def classify(row: dict) -> str:
    day_type = row["day_type"]
    if day_type == "review":
        return "excluded_review"
    if day_type == "conversation":
        return "c3_reference"
    if day_type in C1_TYPES:
        return "c1_rewrite"
    return "c2_seed"


def main() -> None:
    conn = connect_readonly()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT id, month, week, day, day_type, text_en, text_kr, cefr_level,
               source_id, original_id, notes,
               dialogue_id, speaker, dialogue_title, dialogue_situation
        FROM sentences
        WHERE month <= %s
        ORDER BY month, week, day, id
        """,
        (PILOT_MONTHS,),
    )
    seeds = [dict(r) | {"seed_class": classify(r)} for r in cur.fetchall()]

    cur.execute(
        """
        SELECT id, word, pos, cefr_level, meaning_kr, first_month
        FROM vocabulary ORDER BY id
        """
    )
    vocab = [dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT id, type, title_en, title_kr, author, year, url, copyright, description
        FROM sources ORDER BY id
        """
    )
    sources = [dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT sw.sentence_id, sw.word_id, sw.word_text
        FROM sentence_words sw
        JOIN sentences s ON s.id = sw.sentence_id
        WHERE s.month <= %s
        ORDER BY sw.sentence_id, sw.word_id
        """,
        (PILOT_MONTHS,),
    )
    sentence_words = [dict(r) for r in cur.fetchall()]

    # 근접 중복 검사(s04)용 — 생성물이 기존 커리큘럼 전체와 겹치지 않아야 한다
    cur.execute("SELECT id, text_en FROM sentences ORDER BY id")
    all_sentences = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    n_seeds = write_jsonl(WORK_DIR / "seeds_m01_03.jsonl", seeds)
    n_vocab = write_jsonl(WORK_DIR / "vocabulary.jsonl", vocab)
    n_sources = write_jsonl(WORK_DIR / "sources.jsonl", sources)
    n_sw = write_jsonl(WORK_DIR / "sentence_words.jsonl", sentence_words)
    n_all = write_jsonl(WORK_DIR / "sentences_all.jsonl", all_sentences)

    dist = Counter(s["seed_class"] for s in seeds)
    print(f"seeds_m01_03.jsonl    {n_seeds}행  {dict(dist)}")
    print(f"vocabulary.jsonl      {n_vocab}행")
    print(f"sources.jsonl         {n_sources}행")
    print(f"sentence_words.jsonl  {n_sw}행")
    print(f"sentences_all.jsonl   {n_all}행")

    expected = {"c1_rewrite": 27, "c2_seed": 118, "c3_reference": 60, "excluded_review": 24}
    if dict(dist) != expected:
        print(f"⚠️  분류 분포가 사전 실측과 다름 — 예상 {expected}")


if __name__ == "__main__":
    main()
