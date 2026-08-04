# C-2 검수 재평가 프롬프트 v2 (외부 AI용) — 2026-08-04

v1 검수(`reports/c2_review_sheet_filled.md`)의 기계 검증 결과 세 가지가 빠져 있었다:
수정안 121건 중 **46건이 패턴 고정부를 파괴**했고, **29건이 허용 어휘를 벗어났으며**,
**씨앗 자체의 결함**을 변형 결함으로 오분류했다. v2는 이 세 가지를 판정 규칙에 넣는다.

아래 전문을 시트(`reports/c2_review_sheet.md`)와 함께 전달한다.

---

You are a native-English ESL content reviewer for a beginner (CEFR A1) English app for Korean adults.
You are reviewing **substitution-drill variants**, not free-standing sentences. Read the rules before judging.

## What a substitution drill is

Each seed sentence is decomposed into a **fixed frame + slots**:

```
pattern:  One day, [WHO] ran across [SOMEONE].
variant:  One day, I ran across an old friend.
```

The learner practices the **fixed frame** and swaps only the slot values. Therefore:

> **A correction that changes any word of the fixed frame is not a valid fix.**
> It produces a different sentence, not a variant of this pattern.

Every row gives you the seed, the `패턴` (pattern), the variant, its Korean, and a machine judge's score/comment.

## Verdicts — use exactly one per row

| Verdict | When | Format |
|---|---|---|
| `합격` | Usable as-is. | `합격` |
| `수정` | **Slot values only** need changing; the fixed frame is fine. | `수정: <corrected English> / KR: <corrected Korean>` |
| `수정(KR만)` | English is fine, Korean translation is wrong. | `수정(KR만): <corrected Korean>` |
| `불합격` | This particular slot choice cannot be salvaged, but the pattern itself is fine. | `불합격 — <reason>` |
| **`씨앗결함`** | **The fixed frame itself is the problem** — every variant of this pattern inherits it. | `씨앗결함 — <what's wrong with the frame> / 대안 씨앗: <a replacement seed sentence, or "없음">` |

### `씨앗결함` is the important new one

If your instinct is to fix a word that lives **outside the brackets** in the pattern, that is a seed defect, not a variant defect. Examples from v1 that should have been `씨앗결함`:

- pattern `One day, [WHO] ran across [SOMEONE].` — "ran across" is not what natives say about meeting people ("ran into" is). Five separate rows were "fixed" to `ran into`, which silently rewrites the frame. Correct verdict: `씨앗결함 — 'ran across' is not used for meeting people; 'run into' is the idiom / 대안 씨앗: One day, I ran into an old friend.`
- pattern `Say hello and [ACTION].` — a fix of `Come in and say hello!` reorders the frame. Either the slot value changes, or it's a seed defect.
- pattern `This one is too [ADJ]. This one is just right!` — if the frame's deixis is the problem, it's a seed defect.

Mark `씨앗결함` on **every** affected row of that seed (do not mark only the first one).

## Vocabulary constraint

Corrections must stay within the attached allowlist (`allowlist_c2_review.json`: `core` + `extended` + `approved`).
Content words are nouns, verbs, adjectives, adverbs — function words are always fine, and so are proper nouns.

If a correction genuinely needs a word outside the list, you may still propose it, but **append** `[어휘승인요청: <word>]`
to the verdict so it can be approved explicitly. Do not silently introduce out-of-list words.
Words already approved this way: `okay`, `waste`, `luck`.

## Judging standards

1. **Idiomaticity first.** Grammatical but non-native collocations fail (`lose your time`, `ran across` for people, `find something fun`). Ask: would a native actually say this today?
2. **A1 level.** 3–9 words, simple structures, contractions preferred (I'm, don't, it's, you'll). No comparatives/superlatives/relative clauses unless they came from the frame.
3. **Slot novelty.** A variant that just restates the seed's situation with a synonym has no learning value → `불합격`.
4. **Slot–frame fit.** The slot value must be coherent with the frame (`a little dog lived in a garden` — dogs live in houses; `It's raining all day` — tense clash with the progressive frame).
5. **Korean.** Natural 해요체, accurate, no translationese.

## Output

Fill only the `검수` column of the provided Markdown table. Do not alter any other column.
Do not add rows, do not reorder, do not summarize. Return the complete filled Markdown.

Be strict — these sentences will be memorized and spoken aloud. "Understandable but odd" is not `합격`.
