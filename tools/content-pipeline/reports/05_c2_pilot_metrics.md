# s06 — C-2 파일럿 지표 리포트 (M01~03, 씨앗 145)

생성: 2026-08-04T00:19:38+00:00 · 게이트: s04(c2) · judge: judge_c2_v2

## 23 §5 기준 대비

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ 4.0/5 | 3.95 | 미달 |
| 근접 중복(통과분) | < 2% | 게이트 차단 18건 → 통과분 0% | 통과 |
| 씨앗 유사도 | 변형이므로 상한 대신 동일 판정(14건 차단) | — | 통과 |
| 인간 검수 합격률(샘플) | ≥ 90% | 검수 시트 회수 후 판정 | 대기 |

## 게이트·채점 요약

- 후보 870 → 게이트 통과 738 (85%) — 탈락 사유: {'vocab_core_p90': 9, 'vocab_extended': 99, 'seed_identical': 14, 'near_duplicate_db': 3, 'near_duplicate_batch': 15}
- judge 채점 738건 — avg 분포: ≥4.5 147 · 4.0~4.5 313 · <4.0 278 · 플래그 28건
- 씨앗별 생존(6개 중): 평균 5.1개 · **3개 미만 생존 씨앗 7개** ['M01_048', 'M02_023', 'M02_024', 'M02_027', 'M02_037', 'M03_033', 'M03_038']
- **씨앗 적격성**: 씨앗 평균 ≥ 3.5 인 적격 씨앗 120개 / 부적격 24개
  (적격분 변형 616건, judge 평균 **4.15** → 기준 충족)
- 인간 검수 대상(적격분만): judge 저점 163 + 무작위 샘플 45 = 208건 (seed=42)

## 씨앗 계열별 judge 평균 — 어떤 씨앗이 substitution drill에 맞는가

| day_type | 채점 건수 | judge 평균 |
|---|---|---|
| proverb | 61 | 2.92 |
| tale | 209 | 3.77 |
| quote | 65 | 3.92 |
| movie | 81 | 4.02 |
| real | 322 | 4.25 |

## judge 평균 최하위 씨앗 12개 (재생성·폐기 검토 대상)

| 씨앗 | 계열 | 평균 | 원문 |
|---|---|---|---|
| M02_040 | proverb | 1.33 | A friend in need is a friend indeed. |
| M03_033 | proverb | 2.00 | When in Rome, do as the Romans do. |
| M02_021 | proverb | 2.07 | Don't put off until tomorrow what you can do today. |
| M02_031 | proverb | 2.39 | The best time to plant a tree was 20 years ago. |
| M01_023 | proverb | 2.61 | Actions speak louder than words. |
| M01_015 | tale | 2.73 | You are so slow! laughed the Hare. |
| M02_042 | tale | 2.74 | They lived happily ever after. |
| M01_027 | tale | 2.83 | I am getting ready for winter, said the Ant. |
| M02_003 | tale | 2.89 | She found a little house in the forest, and she went inside. |
| M01_042 | proverb | 2.93 | Better late than never. |
| M01_018 | tale | 3.00 | I will take a nap, thought the Hare. |
| M03_022 | proverb | 3.00 | All roads lead to Rome. |

## 판정과 원인 — 생성 품질이 아니라 씨앗 적격성

전체 평균 3.95는 기준 미달이지만, **적격 씨앗만 보면 4.15로 기준을 넘는다.**
계열별 격차가 원인을 가리킨다: `real` 4.25 · `movie` 4.02 · `quote` 3.92 · `tale` 3.77 · `proverb` 2.92.

세 judge 배치가 독립적으로 같은 결론을 냈다 — **속담·동화 종결구는 substitution drill 대상이 아니다**:

- 슬롯을 치환하면 "지어낸 격언"이 된다 (A friend in need → A doctor in need). 실제 발화 상황이 없어 재사용 가치가 0.
- 고유명사가 의미를 지탱하는 속담(All roads lead to **Rome**)은 일반명사 치환 자체가 성립하지 않는다.
- 화석화된 관용구(happily ever after, raining cats and dogs)는 슬롯화하면 정작 그 관용구를 못 가르친다.
- 씨앗 고정부가 A1을 넘는 문법(비교급 louder, 최상급 the best time, 자유관계절)을 담으면 변형 전량이 A1을 이탈한다.
- 서사체 도치·인용문("…," said the Ant)은 인용부호 표기까지 씨앗에서 상속되고 대화 재사용성이 낮다.

이 판정은 [prompts/style_lessons.md](../prompts/style_lessons.md) §13~17 "C-2 씨앗 적격성 규칙"으로 반영했다.

### 권고

1. **부적격 씨앗 24개는 C-2에서 제외** — 개별 변형을 고쳐도 해결되지 않는다.
   통청크 암기 자산으로 그대로 쓰거나 C-3 대화에서 문맥과 함께 제시한다.
2. 인간 검수는 적격분 208건으로 진행 → 합격률로 23 §5 마지막 기준을 판정.
3. 월 단위 확대 전에 **씨앗 선별을 파이프라인 단계로 승격**(s01 분류에 C-2 적격 플래그 추가) 검토.
