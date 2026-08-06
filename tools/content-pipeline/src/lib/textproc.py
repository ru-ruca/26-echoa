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


def lemma_candidates(text: str) -> list[set[str]]:
    """content word마다 가능한 lemma 후보 집합을 낸다.

    spacy 규칙 lemmatizer가 중복자음을 잘못 처리한다 — `hoping` → `hop`(정답 `hope`).
    허용 어휘 검사에서 이런 오류로 정상 문장이 탈락하는 것을 막기 위해,
    lemma 하나가 아니라 후보 집합을 만들어 **하나라도 목록에 있으면 통과**시킨다.

    후보를 넓히는 것은 안전하다 — 목록에 없는 진짜 낯선 단어는 어떤 후보로도 통과하지 못한다.
    """
    out = []
    for t in nlp()(text):
        if t.pos_ not in CONTENT_POS or not t.is_alpha:
            continue
        lemma, surface = t.lemma_.lower(), t.text.lower()
        cands = {lemma, surface}
        # hop + e = hope (drop-e 굴절을 되돌린다)
        if surface.endswith(("ing", "ed")) and not lemma.endswith("e"):
            cands.add(lemma + "e")
        # 규칙 lemmatizer가 놓친 -s/-es 복수·3인칭
        if surface.endswith("s") and len(surface) > 3:
            cands.add(surface[:-1])
            if surface.endswith("es"):
                cands.add(surface[:-2])
        out.append(cands)
    return out


def normalize_word(word: str) -> str:
    """단어 사전 항목을 허용 목록 키로 정규화한다 (소문자 + lemma)."""
    word = word.strip().lower()
    doc = nlp()(word)
    # 다단어 항목("wake up")은 각 토큰 lemma를 공백 연결하지 않고 첫 content lemma 반환이
    # 아니라 — 사전 항목 자체가 키이므로 전체를 lemma 시퀀스로 정규화한다.
    lemmas = [t.lemma_.lower() for t in doc if t.is_alpha]
    return " ".join(lemmas) if lemmas else word
