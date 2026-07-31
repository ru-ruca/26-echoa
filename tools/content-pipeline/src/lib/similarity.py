"""문장 유사도 — 씨앗 유사도 상한(저작권)과 근접 중복 검사가 공유한다.

저작권 유사성은 표현 전체가 문제이므로 기능어를 포함한 전체 토큰으로 본다.
두 지표를 함께 쓴다: 단어 집합 겹침(jaccard) + 문자열 순서 유사도(ratio).
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

_WORD = re.compile(r"[a-z']+")


def tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def jaccard(a: str, b: str) -> float:
    sa, sb = set(tokens(a)), set(tokens(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, " ".join(tokens(a)), " ".join(tokens(b))).ratio()


def similarity(a: str, b: str) -> dict[str, float]:
    return {"jaccard": round(jaccard(a, b), 3), "ratio": round(ratio(a, b), 3)}
