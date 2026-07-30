"""spacy 기반 텍스트 처리 — 허용 어휘 검사의 공통 토대.

어휘 검사 대상은 content word(NOUN·VERB·ADJ·ADV)의 lemma만이다.
기능어(관사·전치사·대명사·조동사·접속사 등)·고유명사·감탄사·숫자·구두점은
어휘 학습 대상이 아니므로 자동 허용한다.
"""
from __future__ import annotations

from functools import lru_cache

CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV"}


@lru_cache(maxsize=1)
def nlp():
    import spacy

    return spacy.load("en_core_web_sm", disable=["parser", "ner"])


def content_lemmas(text: str) -> list[str]:
    """문장에서 검사 대상 content lemma(소문자)를 추출한다."""
    doc = nlp()(text)
    return [
        t.lemma_.lower()
        for t in doc
        if t.pos_ in CONTENT_POS and t.is_alpha
    ]


def normalize_word(word: str) -> str:
    """단어 사전 항목을 허용 목록 키로 정규화한다 (소문자 + lemma)."""
    word = word.strip().lower()
    doc = nlp()(word)
    # 다단어 항목("wake up")은 각 토큰 lemma를 공백 연결하지 않고 첫 content lemma 반환이
    # 아니라 — 사전 항목 자체가 키이므로 전체를 lemma 시퀀스로 정규화한다.
    lemmas = [t.lemma_.lower() for t in doc if t.is_alpha]
    return " ".join(lemmas) if lemmas else word
