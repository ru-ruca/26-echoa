# s09 — 검수 시트 기계 검증

대상: `c2_review_sheet_filled.md` · 판정 208건

## 판정 분포

| 판정 | 건수 |
|---|---|
| 수정 | 121 |
| 합격 | 53 |
| 불합격 | 34 |

### 23 §5 합격률은 무작위 샘플로만 판정한다

저점군은 judge<4.0으로 **의도적으로 편향 추출**한 집합이라 그 합격률은 모집단 품질이 아니다.
모집단 추정치는 무작위 샘플뿐이다.

| 집합 | 합격 | 수정 | 불합격 | 합격률 | 합격+수정 |
|---|---|---|---|---|---|
| 무작위 샘플 (45건) | 37 | 8 | 0 | **82%** | 100% |
| judge 저점군 (163건) | 16 | 113 | 34 | **10%** | 79% |

## 패턴 고정부를 깨는 수정안

**46건** — 고정부를 바꾼 수정은 substitution drill이 아니다.
고정부 자체가 비관용이면 개별 변형이 아니라 **씨앗을 교체**해야 한다.

| 씨앗 | cand | 패턴 | 수정안 |
|---|---|---|---|
| M01_001 | 2 | `Say hello and [ACTION].` | Come in and say hello! |
| M01_003 | 1 | `One day, [WHO] ran across [SOMEONE].` | One day, I ran into an old friend. |
| M01_003 | 2 | `One day, [WHO] ran across [SOMEONE].` | One day, my mother ran into her old teacher. |
| M01_003 | 4 | `One day, [WHO] ran across [SOMEONE].` | One day, we ran into your parents. |
| M01_003 | 5 | `One day, [WHO] ran across [SOMEONE].` | One day, she ran into her aunt. |
| M01_003 | 6 | `One day, [WHO] ran across [SOMEONE].` | One day, my sister ran into her doctor. |
| M01_006 | 3 | `I will [ACTION] someday, I promise.` | I'll buy you a car someday, I promise. |
| M01_006 | 4 | `I will [ACTION] someday, I promise.` | I'll take you there someday, I promise. |
| M01_006 | 5 | `I will [ACTION] someday, I promise.` | I'll take you to my country someday, I promise. |
| M01_009 | 3 | `Nice to [VERB-PHRASE] too.` | Nice to meet your family. |
| M01_010 | 6 | `How are you [WHEN]?` | How was your trip? |
| M01_012 | 1 | `The [WHO] catches the [WHAT].` | The dog caught the ball. |
| M01_022 | 3 | `Let's go and [ACTION]!` | Let's go for a walk in the park! |
| M01_022 | 6 | `Let's go and [ACTION]!` | Let's take the train! |
| M01_025 | 3 | `In [WHEN], [WHO] worked hard every day.` | In the morning, my sister worked hard. |
| M01_025 | 5 | `In [WHEN], [WHO] worked hard every day.` | In the evening, my brother worked hard. |
| M01_031 | 1 | `I love my [THING] very much.` | I love my job. |
| M01_031 | 2 | `I love my [THING] very much.` | I love my new school. |
| M01_031 | 5 | `I love my [THING] very much.` | I love my morning coffee. |
| M01_031 | 6 | `I love my [THING] very much.` | I love my small town. |
| M01_034 | 2 | `What is [THING]?` | What's in the bag? |
| M01_034 | 3 | `What is [THING]?` | What do you do? |
| M01_035 | 3 | `What [THING] is it?` | What's the room number? |
| M01_037 | 2 | `When is your [EVENT]?` | When's your first day at school? |
| M01_037 | 4 | `When is your [EVENT]?` | When's your next vacation? |
| M01_046 | 2 | `Please [ACTION-A] and [ACTION-B].` | Let's stop and think. |
| M01_050 | 5 | `My [THING] is very [ADJECTIVE] today.` | My car is really dirty today. |
| M02_006 | 2 | `This one is too [ADJECTIVE]. This one is just right!` | That one is too big. This one is just right! |
| M02_006 | 3 | `This one is too [ADJECTIVE]. This one is just right!` | That one is too expensive. This one is just right! |
| M02_006 | 6 | `This one is too [ADJECTIVE]. This one is just right!` | That one is too short. This one is just right! |
| M02_015 | 2 | `[PERSON] will sleep for [DURATION]!` | My brother sleeps for ten hours! |
| M02_015 | 4 | `[PERSON] will sleep for [DURATION]!` | My grandfather sleeps for an hour. |
| M02_015 | 5 | `[PERSON] will sleep for [DURATION]!` | My sister wants to sleep five more minutes! |
| M02_015 | 6 | `[PERSON] will sleep for [DURATION]!` | My husband sleeps for two hours! |
| M02_016 | 2 | `One day, [PERSON] came to the [PLACE].` | One day, a little cat came into the garden. |
| M02_016 | 6 | `One day, [PERSON] came to the [PLACE].` | One day, a new family came to town. |
| M02_020 | 6 | `Don't worry. [SUBJECT] will be okay.` | Don't worry. The weather will be fine. |
| M02_025 | 2 | `I [VERB-PHRASE] quickly in the morning.` | I have a quick breakfast in the morning. |
| M02_025 | 6 | `I [VERB-PHRASE] quickly in the morning.` | I take a quick shower in the morning. |
| M03_005 | 3 | `[WHO] stopped her in the [PLACE].` | Her teacher stopped her at school. |
| M03_005 | 6 | `[WHO] stopped her in the [PLACE].` | A stranger stopped her on the street. |
| M03_008 | 5 | `I get on the bus at [PLACE].` | I get on the bus near my house. |
| M03_019 | 6 | `It's on the [PLACE].` | It's on Main Street. |
| M03_021 | 5 | `I'm [FEELING] when I [ACTION].` | I get thirsty when I run. |
| M03_029 | 3 | `When will you [ACTION]?` | When are you going to eat dinner? |
| M03_031 | 5 | `Please get out of the [PLACE].` | Please wait outside the room. |

### 같은 씨앗에서 2건 이상 고정부가 깨진 경우 = 씨앗 결함

| 씨앗 | 건수 | 씨앗 원문 |
|---|---|---|
| M01_003 | 5 | One day, the Mouse ran across a sleeping Lion. |
| M01_031 | 4 | I love my family very much. |
| M02_015 | 4 | The princess will sleep for 100 years! |
| M01_006 | 3 | I will help you someday, I promise. |
| M02_006 | 3 | This one is too cold. This one is just right! |
| M01_022 | 2 | Let's go and see the world! |
| M01_025 | 2 | In summer, the Ant worked hard every day. |
| M01_034 | 2 | What is this? |
| M01_037 | 2 | When is your birthday? |
| M02_016 | 2 | One day, a prince came to the castle. |
| M02_025 | 2 | I get dressed quickly in the morning. |
| M03_005 | 2 | A wolf stopped her in the forest. |

## 허용 어휘를 벗어난 수정안

**29건**

| 씨앗 | cand | 수정안 | 목록 밖 |
|---|---|---|---|
| M01_001 | 6 | Say hello and talk to your neighbors. | neighbor |
| M01_002 | 6 | Once upon a time, a little fish lived in a fishbowl. | fishbowl |
| M01_017 | 4 | My grandmother cooked and soon got tired. | cook |
| M01_017 | 5 | The boy studied and soon got tired. | study |
| M01_020 | 5 | My favorite color is blue. What's your favorite color? | color, color |
| M01_024 | 4 | Finish your homework first, then watch TV. | homework |
| M01_025 | 2 | In spring, the students worked hard every day. | spring |
| M01_028 | 3 | When winter came, my brother had no coat. | coat |
| M01_037 | 4 | When's your next vacation? | vacation |
| M01_040 | 2 | Why is my glass empty? | glass |
| M01_041 | 5 | Don't be nervous! I believe in you. | nervous |
| M01_043 | 6 | I live in the countryside. | countryside |
| M02_004 | 3 | She went inside and saw a lot of people. | lot |
| M02_014 | 5 | A boy put a note on the door. | note |
| M02_020 | 6 | Don't worry. The weather will be fine. | fine |
| M02_025 | 2 | I have a quick breakfast in the morning. | quick |
| M02_025 | 4 | I wash my face quickly in the morning. | wash |
| M02_025 | 6 | I take a quick shower in the morning. | quick |
| M02_038 | 4 | Let's clean up the yard. | yard |
| M02_047 | 3 | We can walk or take a taxi. | taxi |
| M03_002 | 6 | Once upon a time, there was a king called James. | king |
| M03_005 | 4 | A doctor stopped her in the hallway. | hallway |
| M03_012 | 4 | Take your time and enjoy the show. | enjoy |
| M03_018 | 4 | Go straight and cross the street. | cross |
| M03_023 | 6 | You're my hero. | hero |
| M03_027 | 3 | The cafe is between the bank and the park. | cafe |
| M03_031 | 5 | Please wait outside the room. | wait |
| M03_035 | 3 | Excuse me, can you give me directions? | direction |
| M03_041 | 5 | I'll email you again on Thursday. | email |

## 수정안 파싱 실패 4건

- M03_002 c1: `수정(KR만): 옛날에, 안나라는 소녀가 있었어요.`
- M03_002 c2: `수정(KR만): 옛날에, 톰이라는 소년이 있었어요.`
- M03_002 c3: `수정(KR만): 옛날에, 사라라는 여자가 있었어요.`
- M03_002 c4: `수정(KR만): 옛날에, 데이빗이라는 남자가 있었어요.`
