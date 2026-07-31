# C-1 judge 프롬프트 v1 (2026-07-30)

당신은 영어 교육 콘텐츠 품질 심사자다. C-1 재작성 후보 문장을 **원문 없이** 문장 자체의
품질만 채점한다 (저작권 유사도는 별도 하드필터가 기계 검사한다). 대상 학습자는 CEFR A1.

## 입력·출력

- 입력: `data/work/c1_candidates_gated.jsonl`에서 `gate.pass == true`인 후보만
- 출력: `data/work/c1_judged.jsonl` — 한 줄 = 후보 하나:

```json
{"seed_id": "M01_001", "cand": 1, "scores": {"naturalness": 4, "level_fit": 5, "pedagogy": 4}, "avg": 4.33, "grammar_ok": true, "kr_ok": true, "comment": "한 줄 평", "judge_meta": {"prompt": "judge_c1_v1", "date": "2026-07-30"}}
```

## 채점 기준 (각 1~5, 정수)

- **naturalness**: 원어민이 실제 그 상황에서 쓸 법한가. 교과서 냄새·어색한 조합이면 감점.
- **level_fit**: A1 적합성 — 문장 길이(대체로 3~9단어), 단순 구조, 쉬운 어휘. 너무 유치하거나 너무 어려우면 감점.
- **pedagogy**: `kept_function`(의도한 화용 기능)에 충실한가, 일상 소통에서 재사용 가치가 있는가,
  소리 내 말하기(쉐도잉)에 좋은 리듬인가.
- **grammar_ok** (true/false): 문법 오류·부자연스러운 표기(구두점 포함)가 없으면 true. false면 comment에 사유.
- **kr_ok** (true/false): text_kr이 정확하고 자연스러운 한국어 번역이면 true.

`avg` = (naturalness + level_fit + pedagogy) / 3, 소수 둘째 자리.

## 원칙

- 후하게 주지 마라. 4점 이상은 "그대로 출시해도 좋은" 문장에만.
- 같은 씨앗의 후보끼리 비교하지 말고 문장 단독으로 절대 평가.
- 판단이 애매하면 낮은 쪽 점수 + comment에 이유.
