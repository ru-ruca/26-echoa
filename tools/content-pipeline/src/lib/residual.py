"""공통 최장 어구를 뺀 잔여 유사도.

저작권 질문은 "공용 언어를 넘어 저자의 표현을 가져왔는가"다.
관용구 학습 씨앗은 관용구를 남기는 게 정상이라 토큰 겹침이 커지고, 유사도 지표가 이를
표현 복제와 구분하지 못한다. 공통 최장 어구(=대개 그 관용구)를 양쪽에서 제거하고
남은 부분의 유사도를 재면, "관용구 말고 또 무엇이 같은가"를 볼 수 있다.

**한계**: 이 지표는 공통 어구가 관용구인지 저자의 표현인지 판별하지 못한다.
실제 문장을 사람이 봐야 한다 — 잔여 유사도는 판단의 근거이지 판정이 아니다.
"""
from __future__ import annotations

from difflib import SequenceMatcher

from src.lib.similarity import ratio, tokens


def longest_common_phrase(a: str, b: str) -> str:
    ta, tb = tokens(a), tokens(b)
    m = SequenceMatcher(None, ta, tb).find_longest_match(0, len(ta), 0, len(tb))
    return " ".join(ta[m.a : m.a + m.size])


def residual_similarity(a: str, b: str) -> dict:
    """공통 최장 어구 제거 후 잔여 유사도."""
    phrase = longest_common_phrase(a, b)
    if not phrase:
        return {"phrase": "", "phrase_len": 0, "residual_ratio": round(ratio(a, b), 3)}
    ta, tb = tokens(a), tokens(b)
    pt = phrase.split()

    def strip(toks: list[str]) -> str:
        for i in range(len(toks) - len(pt) + 1):
            if toks[i : i + len(pt)] == pt:
                return " ".join(toks[:i] + toks[i + len(pt) :])
        return " ".join(toks)

    ra, rb = strip(ta), strip(tb)
    return {
        "phrase": phrase,
        "phrase_len": len(pt),
        "residual_ratio": round(ratio(ra, rb), 3) if (ra or rb) else 0.0,
    }
