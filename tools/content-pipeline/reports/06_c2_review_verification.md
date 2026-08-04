# s09 — 검수 시트 기계 검증

대상: `c2_review_sheet_filled_v2.md` · 판정 208건

## 판정 분포

| 판정 | 건수 |
|---|---|
| 수정 | 78 |
| 합격 | 58 |
| 불합격 | 47 |
| 씨앗결함 | 22 |
| 수정(KR만) | 3 |

### 23 §5 합격률은 무작위 샘플로만 판정한다

저점군은 judge<4.0으로 **의도적으로 편향 추출**한 집합이라 그 합격률은 모집단 품질이 아니다.
모집단 추정치는 무작위 샘플뿐이다.

| 집합 | 합격 | 수정 | 불합격 | 합격률 | 합격+수정 |
|---|---|---|---|---|---|
| 무작위 샘플 (45건) | 40 | 4 | 0 | **89%** | 98% |
| judge 저점군 (163건) | 18 | 74 | 47 | **11%** | 56% |

## 패턴 고정부를 깨는 수정안

**0건** — 고정부를 바꾼 수정은 substitution drill이 아니다.
고정부 자체가 비관용이면 개별 변형이 아니라 **씨앗을 교체**해야 한다.

| 씨앗 | cand | 패턴 | 수정안 |
|---|---|---|---|

### 같은 씨앗에서 2건 이상 고정부가 깨진 경우 = 씨앗 결함

| 씨앗 | 건수 | 씨앗 원문 |
|---|---|---|

## 허용 어휘를 벗어난 수정안

**10건**

| 씨앗 | cand | 수정안 | 목록 밖 |
|---|---|---|---|
| M01_002 | 6 | Once upon a time, a little fish lived in a fishbowl. | fishbowl |
| M01_020 | 5 | My favorite color is blue. What's your favorite color? | color, color |
| M01_024 | 4 | Finish your homework first, then watch TV. | homework |
| M01_025 | 2 | In spring, the students worked hard every day. | spring |
| M01_028 | 3 | When winter came, my brother had no coat. | coat |
| M01_040 | 2 | Why is my glass empty? | glass |
| M02_004 | 3 | She went inside and saw a lot of people. | lot |
| M03_002 | 6 | Once upon a time, there was a king called James. | king |
| M03_005 | 4 | A doctor stopped her in the hallway. | hallway |
| M03_023 | 6 | You're my hero. | hero |

## 수정안 파싱 실패 0건


## 씨앗결함 판정 8개 씨앗 (v2)

검수자가 '고정부 자체가 문제'로 판정한 씨앗. 변형 수정으로 해결되지 않아 씨앗 교체·폐기 대상.

| 씨앗 | 표기 행 | 씨앗 원문 | 사유 | 대안 씨앗 |
|---|---|---|---|---|
| M01_003 | 6/6 | One day, the Mouse ran across a sleeping Lion. | 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) | One day, I ran into an old friend. |
| M01_005 | 1/1 | Please let me go! cried the Mouse. | 고정부에 인용부호가 없어 모든 변형이 같은 표기 오류를 물려받음 | "Please let me go!" cried the Mouse. |
| M01_012 | 2/2 | The early bird catches the worm. | 속담 고정부의 단순현재가 일회성 사건 슬롯과 항상 충돌 | 없음 (속담은 치환 드릴에 부적합) |
| M01_016 | 1/1 | Let's have a race! said the Tortoise. | 고정부에 인용부호가 없어 모든 변형이 같은 표기 오류를 물려받음 | "Let's have a race!" said the Tortoise. |
| M01_031 | 4/4 | I love my family very much. | 고정부 'very much'가 사물·장소 목적어와 결합하지 않아 사람 이외의 슬롯 값 전체가 번역투가 됨 | I really like my job. |
| M02_006 | 3/3 | This one is too cold. This one is just right! | 두 문장 모두 'This one'이라 대조가 성립하지 않는 지시 결함 | That one is too cold. This one is just right! |
| M03_011 | 3/3 | It's raining cats and dogs. | 관용구 'cats and dogs'를 슬롯으로 취급해 어떤 값을 넣어도 관용구가 깨지고 진행 고정부와 시제가 충돌 | 없음 (관용구는 치환 드릴에 부적합) |
| M03_045 | 2/2 | Nothing can stop us today! | [TIME] 슬롯이 관용구의 즉시성 때문에 today/now만 허용해 치환이 사실상 불가능 | Nothing can stop us today! |

부분 표기(일부 행에만 씨앗결함) **0건** — v2 규칙은 전 행 표기를 요구한다.

## 어휘 승인 요청 15건 (v2)

| 단어 | 요청 횟수 |
|---|---|
| fishbowl | 1 |
| better | 1 |
| blue | 1 |
| color | 1 |
| homework | 1 |
| spring | 1 |
| coat | 1 |
| glass | 1 |
| table | 1 |
| young | 1 |
| king | 1 |
| hallway | 1 |
| hero | 1 |
| water | 1 |
| tell | 1 |
