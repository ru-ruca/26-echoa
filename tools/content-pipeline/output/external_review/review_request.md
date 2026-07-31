# C-1 재작성 확정본 — 외부 검토 요청 프롬프트

아래 프롬프트와 함께 `c1_for_review.jsonl`(31행)을 전달하면 된다.
회수한 결과는 `c1_external_verdict.jsonl`로 저장 → 파이프라인이 집계한다.

---

You are a native-English ESL content reviewer for a beginner (CEFR A1) English learning app for Korean adults. Review each sentence in the attached JSONL (fields: `id`, `type`, `text_en`, `text_kr`, `function`).

Evaluate every line on:
1. **Idiomaticity** — Is `text_en` something a native speaker would actually say in daily life? Flag unnatural collocations, textbook-only phrasing, or invented proverbs.
2. **A1 fit** — Short, simple structure; no comparatives/superlatives/relative clauses beyond A1; contractions preferred (I'm, don't, it's).
3. **Korean translation** — Is `text_kr` an accurate, natural Korean rendering (polite 해요체)?
4. **Pairs** — Four ids appear twice (`type: "adopted"` and `type: "alternative"`). For those, also decide which version is better for an A1 learner.

Output **JSONL only** (no prose), one line per input line:

```json
{"id": "M01_001", "type": "adopted", "verdict": "ok", "issue": null, "fixed_en": null, "fixed_kr": null, "pick": null}
```

- `verdict`: `"ok"` (usable as-is) or `"fix"` (needs change).
- `issue`: one short sentence when verdict is `"fix"`, else null.
- `fixed_en` / `fixed_kr`: your corrected version when verdict is `"fix"`, else null. Keep fixes within A1 vocabulary.
- `pick`: only on the four paired ids — `"adopted"` or `"alternative"` (put it on both lines of the pair, same value). Null elsewhere.

Be strict about idiomaticity — these sentences will be memorized and spoken aloud by learners, so "understandable but odd" counts as `"fix"`.
