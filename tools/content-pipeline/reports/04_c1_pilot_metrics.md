# s06 — C-1 파일럿 지표 리포트 (M01~03분 27개)

생성: 2026-07-31T01:37:14+00:00 · 게이트: s04(c1) · judge: judge_c1_v1

## 23 §5 기준 대비

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ 4.0/5 | 4.03 | 통과 |
| 씨앗 유사도 초과(통과분) | 0건 | 0건 (게이트에서 1건 차단) | 통과 |
| 근접 중복(통과분) | < 2% | 0건 차단, 통과분 0% | 통과 |
| 인간 검수 합격률 | ≥ 90% | **100% (27/27 채택, 그중 수정 동반 11)** | **통과** |

## 인간 검수 회수 (2026-07-31 — 시트: reports/restricted/c1_review_sheet_filled.md)

- 채택 27/27 (원문 그대로 16 + 수정 11) → 수정 반영 확정본 [output/c1_adopted.jsonl](../output/c1_adopted.jsonl), 게이트 재검증 27/27 통과.
- 수정 사유: 축약형 미적용 4 · 콜로케이션 오류 4 · 문어체 1 · 비관용 조합 1 · `my friend` 호칭 1 → [prompts/style_lessons.md](../prompts/style_lessons.md)로 규칙화.
- 검수자 승인 어휘 2건(okay·waste) → [output/allowlist_human_approved.json](../output/allowlist_human_approved.json) 신설, s04가 병합.
- 검수자 대안 제안 4건(M01_031·M02_012·M02_022·M03_034) 게이트 4/4 통과 → 외부 검토에서 채택본과 비교 판정 예정.
- judge 1위와 인간 채택 불일치 4건 — 관용성 가중 부족. judge v2 개선 사항으로 style_lessons에 기록.

## 게이트·채점 요약

- 후보 81 → 게이트 통과 75 (93%) — 탈락 사유: {'vocab_extended': 4, 'too_similar_to_seed': 1, 'vocab_core_p90': 1}
- 씨앗 유사도(전체 81) ratio 평균 0.34 / 최대 0.67 (상한 0.65)
- judge avg 분포: ≥4.5 14 · 4.0~4.5 37 · <4.0 24
- grammar/kr 플래그: 1건

## 관찰 (다음 라운드 반영)

- spacy sm 모델이 비교급(higher·nicer)을 원급 lemma로 풀지 못해 어휘 필터가 보수적으로 탈락시킴 —
  C-2 전에 비교급 접미사 처리 추가 검토.
- judge가 잡은 감점 유형: 비관용 콜로케이션(lose time), 격언풍 조어(재사용성 낮음), A1 초과 문법(비교급 등).
  → c1_rewrite 프롬프트 v2에 "관용적 콜로케이션·대화 재사용성" 강조 반영 검토.
- 씨앗 유사도 상한(jaccard 0.55 / ratio 0.65)은 구조 복제 1건을 정확히 차단 — 유지.
