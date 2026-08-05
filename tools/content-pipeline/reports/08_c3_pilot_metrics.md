# s06 — C-3 파일럿 지표 리포트 (대화 50개)

생성: 2026-08-05T01:52:09+00:00 · 게이트: s04b(c3) · judge: judge_c3_v1

## 23 §5 기준 대비

| 지표 | 기준 | 실측 | 판정 |
|---|---|---|---|
| judge 평균 | ≥ 4.0/5 | 3.74 | 미달 |
| **C-3 마지막 턴 CEFR 유지** | 유지 | 50/50 (100%) | 통과 |
| 근접 중복 | < 2% | 게이트 통과분 0% | 통과 |
| 씨앗 보존(원문 그대로) | 필수 | 게이트 100% | 통과 |
| 인간 검수 합격률 | ≥ 90% | 검수 시트 회수 후 판정 | 대기 |

- 대화 50개 전량 게이트 통과 (턴 구조·씨앗 보존·난이도 상승·어휘)
- judge avg 분포: ≥4.5 5 · 4.0~4.5 21 · <4.0 24 · 플래그 6건
- **스키마 적재 검증 통과** — 기존 `day_type='conversation'` 스키마에 그대로 매핑 (23 §3 "새 스키마를 만들지 않는다"). [preview](../output/c3_rows_preview.jsonl)

## style_lessons §17 가설 판정 — C-2 부적격 씨앗을 C-3으로 이관할 수 있는가

§17은 "속담·서사체는 C-2에서 제외하되 C-3 대화에서 문맥과 함께 제시한다"고 적었다.
이 파일럿은 그 대조 실험이다: **A_daily**(일상 발화 씨앗) vs **B_c2_ineligible**(C-2 부적격 씨앗).

| 그룹 | 대화 | judge 평균 | **seed_fit 비율** | 마지막 턴 A1 |
|---|---|---|---|---|
| A_daily | 22 | 4.10 | **100%** | 100% |
| B_c2_ineligible | 28 | 3.46 | **57%** | 100% |

**판정: **계열에 따라 갈린다** — real·quote·movie·proverb는 C-3로 살아나고, tale는 문맥을 붙여도 살아나지 않는다**

A군 seed_fit 100% vs B군 57%. 다만 B군 전체 비율은 서로 다른 계열의 평균이라 오해를 부른다 — 쪼개면 이렇다:

| B군 계열 | 씨앗 | **seed_fit** | judge 평균 |
|---|---|---|---|
| real | 3 | **100%** | 3.75 |
| quote | 2 | **100%** | 4.25 |
| movie | 1 | **100%** | 4.00 |
| proverb | 12 | **75%** | 3.54 |
| tale | 10 | **10%** | 3.05 |

`seed_fit=false`인 씨앗 12개 — 문맥을 붙여도 학습자가 실제로 말할 상황이 안 그려진 것:

| 씨앗 | 그룹 | 계열 | avg | 씨앗 원문 |
|---|---|---|---|---|
| M01_005 | B_c2_ineligible | tale | 2.75 | "Please let me go!" cried the Mouse. |
| M01_015 | B_c2_ineligible | tale | 2.75 | You are so slow! laughed the Hare. |
| M02_003 | B_c2_ineligible | tale | 2.75 | She found a little house in the forest, and she went inside. |
| M02_031 | B_c2_ineligible | proverb | 2.75 | The best time to plant a tree was 20 years ago. |
| M02_042 | B_c2_ineligible | tale | 2.75 | They lived happily ever after. |
| M03_042 | B_c2_ineligible | proverb | 2.75 | Every journey teaches something new. |
| M01_018 | B_c2_ineligible | tale | 3.0 | I will take a nap, thought the Hare. |
| M02_005 | B_c2_ineligible | tale | 3.0 | This porridge is too hot! she said. |
| M01_016 | B_c2_ineligible | tale | 3.25 | "Let's have a race!" said the Tortoise. |
| M01_027 | B_c2_ineligible | tale | 3.25 | I am getting ready for winter, said the Ant. |
| M02_013 | B_c2_ineligible | tale | 3.25 | A beautiful princess was born in a kingdom. |
| M03_046 | B_c2_ineligible | proverb | 3.75 | All roads lead to Rome. |

## judge 평균 최하위 10개

| 씨앗 | 그룹 | avg | 코멘트 |
|---|---|---|---|
| M01_005 | B_c2_ineligible | 2.75 | 동화 인용문을 '무슨 책 읽어요?' 답으로 놓아 문답이 어긋나고 낭독 상황에서만 성립 · kr 'cried'를 '울었어요'로 오역 — 구조적 |
| M01_015 | B_c2_ineligible | 2.75 | 인용부호 누락에 비축약형 'You are' · 낭독 전용 대사라 학습자가 말할 상황이 안 그려짐 — 구조적 |
| M02_003 | B_c2_ineligible | 2.75 | 씨앗이 13단어 서사문이라 턴 길이 상한을 넘고 'does→found' 시제도 어긋남 — 구조적 |
| M02_031 | B_c2_ineligible | 2.75 | 구조적 — 속담 전반부만 씨앗이라 단독으로는 기능하지 않고 완성부를 A가 말함. 최상급·11단어로 A1 상한 초과(style_lessons §16). |
| M02_042 | B_c2_ineligible | 2.75 | 구조적 — 동화 결말문은 낭독 상황에서만 성립해 대화 발화로 전이 불가. 'I like happy books'도 비관용(happy endings). |
| M03_042 | B_c2_ineligible | 2.75 | 구조적 — 씨앗이 지어낸 격언(§4). 여행 소감을 묻는 자리에 격언으로 답하는 원어민 발화 상황이 없음. |
| M03_048 | B_c2_ineligible | 2.75 | 수정 가능 — 비축약 'I am'과 ', and' 접속이 문어체(§1). 'I'm tired. I want to go to bed.'로 바꾸면 해결. |
| M01_018 | B_c2_ineligible | 3.0 | 상황 자체가 '수업 중 낭독'이라 어떤 문장이든 끼워 맞춰지는 프레임 · 인용부호도 누락 — 구조적 |
| M02_005 | B_c2_ineligible | 3.0 | 인용부호 누락에 현재·과거 시제가 섞임 · porridge는 저빈도 어휘 — 구조적 |
| M01_016 | B_c2_ineligible | 3.25 | 도입부 인용을 그대로 옮긴 낭독체이고 'said the Tortoise' 꼬리가 재사용을 막음 — 구조적 |
