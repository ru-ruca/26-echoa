# C-2 변형 인간 검수 시트 (적격 씨앗의 judge 저점 전량 + 무작위 10%)

생성: 2026-08-04T00:19:38+00:00 · 대상 208건

**대상 범위**: 씨앗 평균 ≥ 3.5인 적격 씨앗 120개 (변형 616건, judge 평균 4.15).
부적격 씨앗 24개는 개별 변형 수정으로 해결되지 않아 제외 — 씨앗 단위 폐기/다른 방식 적용을 리포트 §판정에서 별도 결정한다.

판정: `합격` / `수정: <고친 문장>` / `불합격 — 사유` 를 `검수` 칸에 표기.

> 부적격 씨앗: M01_007, M01_015, M01_018, M01_023, M01_027, M01_030, M01_032, M01_033, M01_042, M02_003, M02_005, M02_013, M02_021, M02_030, M02_031, M02_036, M02_040, M02_042, M03_001, M03_022, M03_033, M03_042, M03_046, M03_048

## M01_001 (quote, c1_rewritten) — 씨앗: Say hello and make a new friend.
- 패턴: `Say hello and [ACTION].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Say hello and start your day. | 인사를 건네고 하루를 시작하세요. | 3.0 ⚠️저점 | 'start your day'와 붙으면 표어·광고 카피체가 되어 실제 발화 상황이 안 그려진다 — 구조적. | 불합격 — 'start your day'가 표어체로 흘러 실제 발화 상황이 없음 |
| 2 | Say hello and come in. | 인사하고 들어오세요. | 3.67 ⚠️저점 | 행동 순서가 뒤집혀 어색하다(come in and say hello가 관용) — 어순 교체로 수정 가능. | 불합격 — 'come in'은 인사보다 앞서는 동작이라 프레임 어순과 충돌 |
| 6 | Say hello and talk to people. | 인사하고 사람들과 이야기해 보세요. | 3.67 ⚠️저점 | 'talk to people'이 막연해 자기계발 조언체로 흐른다 — 대상 구체화로 수정 가능. | 수정: Say hello and talk to the new student. / KR: 인사하고 새로 온 학생과 이야기해 보세요. |

## M01_002 (tale, curriculum) — 씨앗: Once upon a time, a little Mouse lived in a forest.
- 패턴: `Once upon a time, a little [WHO] lived in a [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Once upon a time, a little girl lived in a small town. | 옛날 옛적에, 어린 소녀가 작은 마을에 살았어요. | 3.67 ⚠️저점 | 동화 정형구로 자연스럽지만 씨앗의 도입부 상황을 그대로 반복한다 — 구조적. | 합격 |
| 2 | Once upon a time, a little boy lived in a big city. | 옛날 옛적에, 어린 소년이 큰 도시에 살았어요. | 3.67 ⚠️저점 | boy/big city도 무난하나 치환이 같은 동화 오프닝 반복에 머문다 — 구조적. | 합격 |
| 3 | Once upon a time, a little dog lived in a garden. | 옛날 옛적에, 작은 강아지가 정원에 살았어요. | 3.33 ⚠️저점 | 개가 정원에 '산다'는 설정이 어색하다(집·마당) — PLACE 값 교체로 수정 가능. | 수정: Once upon a time, a little dog lived in a small house. / KR: 옛날 옛적에, 작은 강아지가 작은 집에 살았어요. |
| 4 | Once upon a time, a little cat lived in a warm house. | 옛날 옛적에, 작은 고양이가 따뜻한 집에 살았어요. | 3.67 ⚠️저점 | cat/warm house는 동화 이미지로 자연 — 치환 novelty가 낮은 건 구조적. | 합격 |
| 5 | Once upon a time, a little bird lived in a tall tree. | 옛날 옛적에, 작은 새가 큰 나무에 살았어요. | 3.67 ⚠️저점 | bird/tall tree가 이 패턴에서 가장 관용적 — 상황 반복은 구조적. | 합격 |
| 6 | Once upon a time, a little fish lived in a bowl. | 옛날 옛적에, 작은 물고기가 어항에 살았어요. | 3.33 ⚠️저점 | 'lived in a bowl'은 어항을 뜻하기에 표현이 모자라다(a fishbowl) — 수정 가능. | 수정: Once upon a time, a little fish lived in a fishbowl. / KR: 옛날 옛적에, 작은 물고기가 어항에 살았어요. [어휘승인요청: fishbowl] |

## M01_003 (tale, curriculum) — 씨앗: One day, the Mouse ran across a sleeping Lion.
- 패턴: `One day, [WHO] ran across [SOMEONE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | One day, I ran across an old friend. | 어느 날, 저는 오랜 친구와 우연히 마주쳤어요. | 3.67 ⚠️저점 | 사람과의 우연한 만남은 'ran into'가 관용이라 조합이 어긋난다 — 동사 교체로 수정 가능. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |
| 2 | One day, my mother ran across her old teacher. | 어느 날, 엄마가 옛 선생님과 우연히 마주쳤어요. | 3.33 ⚠️저점 | 고정부 'ran across + 사람'이 비관용(ran into) — 동사 교체로 수정 가능. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |
| 3 | One day, my father ran across his students. | 어느 날, 아빠가 제자들과 우연히 마주쳤어요. | 3.0 ⚠️저점 | 복수의 제자를 한꺼번에 우연히 마주치는 상황이 안 그려지고 동사도 비관용 — 구조적. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |
| 4 | One day, we ran across your parents. | 어느 날, 우리는 당신 부모님과 우연히 마주쳤어요. | 3.67 ⚠️저점 | ran into가 관용 — 동사 교체로 수정 가능, 나머지는 A1에 맞다. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |
| 5 | One day, she ran across her aunt. | 어느 날, 그녀는 이모와 우연히 마주쳤어요. | 3.67 ⚠️저점 | ran into가 관용 — 동사 교체로 수정 가능. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |
| 6 | One day, my sister ran across her doctor. | 어느 날, 언니가 의사 선생님과 우연히 마주쳤어요. | 3.67 ⚠️저점 | 의사를 길에서 마주치는 상황은 가능하나 ran across가 비관용 — 동사 교체로 수정 가능. | 씨앗결함 — 고정부 'ran across'는 사람을 우연히 만나는 뜻으로 쓰지 않음(관용은 run into) / 대안 씨앗: One day, I ran into an old friend. |

## M01_004 (tale, curriculum) — 씨앗: The Lion woke up and caught the Mouse.
- 패턴: `[WHO] woke up and [ACTION].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | My father woke up and made coffee. | 아빠가 일어나서 커피를 내렸어요. | 4.67 | 기상 후 일과 서술로 완전히 관용적이고 A1 길이 — 결함 없음. | 합격 |

## M01_005 (tale, curriculum) — 씨앗: Please let me go! cried the Mouse.
- 패턴: `Please let me [ACTION]! cried the [WHO].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Please let me answer! cried the student. | 제가 대답하게 해 주세요! 학생이 외쳤어요. | 3.67 ⚠️저점 | 수업 중 'Please let me answer!'를 외치는 상황은 다소 억지다 — 값 교체로 수정 가능. | 씨앗결함 — 고정부에 인용부호가 없어 모든 변형이 같은 표기 오류를 물려받음 / 대안 씨앗: "Please let me go!" cried the Mouse. |

## M01_006 (tale, curriculum) — 씨앗: I will help you someday, I promise.
- 패턴: `I will [ACTION] someday, I promise.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | I will buy you a car someday, I promise. | 언젠가 차 사 줄게요, 약속해요. | 4.0 | 자녀가 부모에게 하는 약속으로 상황이 그려진다 — 축약형만 수정 가능. | 합격 |
| 4 | I will take you there someday, I promise. | 언젠가 거기 데려가 줄게요, 약속해요. | 4.0 | 'take you there'가 관용적이고 슬롯 충돌이 없다 — 축약형만 수정 가능. | 합격 |
| 5 | I will show you my country someday, I promise. | 언젠가 제 나라를 보여 줄게요, 약속해요. | 3.33 ⚠️저점 | 'show you my country'는 비관용(take you to my country / show you around) — 동사구 교체로 수정 가능. | 수정: I will take you to my country someday, I promise. / KR: 언젠가 제 나라에 데려갈게요, 약속해요. |

## M01_008 (real, curriculum) — 씨앗: Hi! Nice to meet you.
- 패턴: `Hi! [GREETING-PHRASE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Hi! Good to see you. | 안녕! 만나서 반가워요. | 4.67 | 가장 흔한 인사 결합이고 재사용 범위가 넓다 — 결함 없음. | 합격 |
| 2 | Hi! Thanks for coming. | 안녕! 와 줘서 고마워요. | 4.67 | 손님을 맞는 실제 발화로 관용적 — 결함 없음. | 합격 |
| 3 | Hi! Welcome to my home. | 안녕! 우리 집에 온 걸 환영해요. | 3.67 ⚠️저점 | 'Welcome to my home'은 대본체다(구어는 Come on in / Welcome!) — 문구 교체로 수정 가능. | 수정: Hi! Come on in. / KR: 안녕! 어서 들어와요. |

## M01_009 (real, curriculum) — 씨앗: Nice to meet you too.
- 패턴: `Nice to [VERB-PHRASE] too.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | Nice to meet your family too. | 가족분들도 만나서 반가워요. | 3.67 ⚠️저점 | 'too'가 호응할 상대 발화가 없어 어색하다 — too 삭제로 수정 가능. | 불합격 — 'too'가 호응할 앞선 발화가 없어 이 슬롯 값으로는 성립하지 않음 |
| 6 | Nice to play with you too. | 저도 함께 놀아서 좋았어요. | 3.67 ⚠️저점 | 성인 발화로는 어색하고 아동 상황에 한정된다 — 값 교체로 수정 가능. | 수정: Nice to talk to you too. / KR: 저도 이야기 나눠서 좋았어요. |

## M01_010 (real, curriculum) — 씨앗: How are you today?
- 패턴: `How are you [WHEN]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | How are you after your trip? | 여행 다녀와서 어떠세요? | 3.67 ⚠️저점 | 여행 뒤에는 'How was your trip?'을 쓰는 게 관용이다 — 문구 교체로 수정 가능. | 수정: How are you these days? / KR: 요즘 어떻게 지내요? |

## M01_012 (proverb, curriculum) — 씨앗: The early bird catches the worm.
- 패턴: `The [WHO] catches the [WHAT].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | The dog catches the ball. | 개가 공을 잡아요. | 3.67 ⚠️저점 | 일회성 동작에 단순현재라 시제가 어긋난다(is catching/caught) — 시제 교체로 수정 가능. | 씨앗결함 — 속담 고정부의 단순현재가 일회성 사건 슬롯과 항상 충돌 / 대안 씨앗: 없음 (속담은 치환 드릴에 부적합) |
| 6 | The boy catches the big fish. | 소년이 큰 물고기를 잡아요. | 3.0 ⚠️저점 | 낚시는 일회성 사건이라 단순현재와 충돌한다(caught) — 시제·상황 불일치로 구조적. | 씨앗결함 — 속담 고정부의 단순현재가 일회성 사건 슬롯과 항상 충돌 / 대안 씨앗: 없음 (속담은 치환 드릴에 부적합) |

## M01_013 (quote, c1_rewritten) — 씨앗: Keep going, and you'll win.
- 패턴: `Keep [DOING], and you'll [RESULT].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Keep trying, and you'll learn. | 계속 해 보면 배우게 될 거예요. | 3.67 ⚠️저점 | 'you'll learn'이 막연해 격려 문구로는 약하다(you'll get it) — 결과부 교체로 수정 가능. | 수정: Keep trying, and you'll get it. / KR: 계속 해 보면 결국 해낼 거예요. |
| 3 | Keep practicing, and you'll play well. | 계속 연습하면 잘하게 될 거예요. | 3.67 ⚠️저점 | 'you'll play well'보다 'you'll get better'가 관용이다 — 결과부 교체로 수정 가능. | 수정: Keep practicing, and you'll get better. / KR: 계속 연습하면 더 잘하게 될 거예요. [어휘승인요청: better] |
| 5 | Keep asking, and you'll understand. | 계속 물어보면 이해하게 될 거예요. | 3.67 ⚠️저점 | 결과부가 막연해 표어체로 읽힌다 — 목적어 추가로 수정 가능. | 수정: Keep asking, and you'll find the answer. / KR: 계속 물어보면 답을 찾게 될 거예요. |

## M01_016 (tale, curriculum) — 씨앗: Let's have a race! said the Tortoise.
- 패턴: `Let's [ACTIVITY]! said [WHO].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Let's make a cake! said the little girl. | 케이크 만들자! 어린 소녀가 말했어요. | 4.33 | 아이 발화로 자연스럽다 — 인용부호 표기만 수정 가능. | 씨앗결함 — 고정부에 인용부호가 없어 모든 변형이 같은 표기 오류를 물려받음 / 대안 씨앗: "Let's have a race!" said the Tortoise. |

## M01_017 (tale, curriculum) — 씨앗: The Hare ran fast and soon got tired.
- 패턴: `[WHO] [ACTION] and soon got tired.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | The dog ran around the garden and soon got tired. | 개가 정원을 뛰어다니다 금방 지쳤어요. | 3.67 ⚠️저점 | 조합은 자연스러우나 10단어로 A1 상한을 넘는다 — 축약으로 수정 가능. | 수정: The dog played outside and soon got tired. / KR: 개가 밖에서 놀다가 금방 지쳤어요. |
| 4 | My grandmother worked in the kitchen and soon got tired. | 할머니가 부엌에서 일하시다 금방 지치셨어요. | 3.67 ⚠️저점 | 내용은 자연스러우나 길이가 A1을 넘는다 — 짧게 줄여 수정 가능. | 수정: My grandmother made a cake and soon got tired. / KR: 할머니가 케이크를 만들다 금방 지치셨어요. |
| 5 | The boy read a long book and soon got tired. | 소년이 긴 책을 읽다가 금방 지쳤어요. | 3.33 ⚠️저점 | '긴 책을 읽어서 지쳤다'는 인과가 약하고 길이도 초과한다 — 값 교체로 수정 가능. | 수정: The boy walked to school and soon got tired. / KR: 소년이 학교까지 걸어가다 금방 지쳤어요. |

## M01_019 (tale, curriculum) — 씨앗: The Tortoise never gave up and kept going.
- 패턴: `[WHO] never gave up and kept [DOING].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | My grandfather never gave up and kept working. | 할아버지는 절대 포기하지 않고 계속 일했어요. | 4.33 | 과거 서술로 자연스럽고 두 동사구가 잘 이어진다 — 결함 없음. | 합격 |

## M01_020 (real, curriculum) — 씨앗: My name is Sage. What's your name?
- 패턴: `My [THING] is [VALUE]. What's your [THING]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | My favorite day is Sunday. What's your favorite day? | 제가 좋아하는 요일은 일요일이에요. 좋아하는 요일이 뭐예요? | 4.33 | 되묻기까지 붙은 대화 시작 문형으로 자연스럽다 — 결함 없음. | 합격 |
| 5 | My favorite month is May. What's your favorite month? | 제가 좋아하는 달은 5월이에요. 좋아하는 달은 뭐예요? | 3.67 ⚠️저점 | 'favorite month'는 실제로 잘 묻지 않는 질문이다 — THING 값 교체로 수정 가능. | 수정: My favorite color is blue. What's your favorite color? / KR: 제가 좋아하는 색은 파란색이에요. 좋아하는 색은 뭐예요? [어휘승인요청: blue] [어휘승인요청: color] |

## M01_021 (real, curriculum) — 씨앗: I'm from Korea. Where are you from?
- 패턴: `I'm from [PLACE]. Where are you from?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | I'm from London. Where are you from? | 저는 런던에서 왔어요. 어디서 오셨어요? | 4.33 | 국가·도시명 교체 반복이라 세트 내 novelty가 없다 — 구조적. | 합격 |

## M01_022 (movie, c1_rewritten) — 씨앗: Let's go and see the world!
- 패턴: `Let's go and [ACTION]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | Let's go and walk in the park! | 공원에 걸으러 가요! | 3.67 ⚠️저점 | 'go for a walk in the park'가 관용이라 조합이 겉돈다 — 동사구 교체로 수정 가능. | 불합격 — 'walk'은 'go for a walk'가 관용이라 'go and' 고정부에 들어갈 수 없음 |
| 4 | Let's go and meet your friends! | 친구들 만나러 가요! | 3.67 ⚠️저점 | 'meet your friends'는 약속이 잡힌 뜻이라 즉흥 제안과 어긋난다 — 값 교체로 수정 가능. | 수정: Let's go and see your friends! / KR: 친구들 보러 가요! |
| 6 | Let's go and take the train! | 기차 타러 가요! | 3.67 ⚠️저점 | 'go and take the train'은 비관용이다(catch the train / take the train) — 동사 교체로 수정 가능. | 수정: Let's go and catch the train! / KR: 기차 타러 가요! |

## M01_024 (quote, c1_rewritten) — 씨앗: Finish your work first, then have fun.
- 패턴: `Finish your [TASK] first, then [ACTIVITY].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Finish your letter first, then go to the post office. | 편지 먼저 다 쓰고, 그다음에 우체국에 가세요. | 3.33 ⚠️저점 | 편지를 쓰고 우체국에 가는 설정이 요즘 생활과 멀다 — TASK 값 교체로 수정 가능. | 수정: Finish your homework first, then watch TV. / KR: 숙제 먼저 끝내고, 그다음에 TV 보세요. [어휘승인요청: homework] |

## M01_025 (tale, curriculum) — 씨앗: In summer, the Ant worked hard every day.
- 패턴: `In [WHEN], [WHO] worked hard every day.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | In March, the students worked hard every day. | 3월에, 학생들은 매일 열심히 공부했어요. | 3.67 ⚠️저점 | 특정 월과 '매일'의 습관 서술이 겹쳐 어색하다 — WHEN 값 교체로 수정 가능. | 수정: In spring, the students worked hard every day. / KR: 봄에, 학생들은 매일 열심히 공부했어요. [어휘승인요청: spring] |
| 3 | In the morning, my sister worked hard every day. | 아침에, 언니는 매일 열심히 일했어요. | 3.33 ⚠️저점 | '아침에'와 '매일'이 겹쳐 의미가 중복된다 — WHEN 값 교체로 수정 가능. | 불합격 — 'in the morning'은 '매일' 고정부와 의미가 겹쳐 프레임과 충돌 |
| 4 | In June, the doctor worked hard every day. | 6월에, 그 의사는 매일 열심히 일했어요. | 3.67 ⚠️저점 | 'In June'처럼 좁은 시점은 매일 습관과 충돌한다 — 값 교체로 수정 가능. | 수정: In winter, the doctor worked hard every day. / KR: 겨울에, 그 의사는 매일 열심히 일했어요. |
| 5 | In the evening, my brother worked hard every day. | 저녁에, 형은 매일 열심히 일했어요. | 3.33 ⚠️저점 | 시간대 슬롯과 '매일'이 어긋난다 — 값 교체로 수정 가능. | 불합격 — 'in the evening'도 '매일' 고정부와 겹쳐 이 슬롯 유형이 프레임에 맞지 않음 |

## M01_026 (tale, curriculum) — 씨앗: The Grasshopper just played all day.
- 패턴: `[WHO] just [ACTION-PAST] all day.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | The children just ran around all day. | 아이들은 하루 종일 뛰어다니기만 했어요. | 4.33 | 아이들 하루를 서술하는 자연스러운 문장이다 — 결함 없음. | 합격 |

## M01_028 (tale, curriculum) — 씨앗: When winter came, the Grasshopper had no food.
- 패턴: `When [EVENT] came, [WHO] had no [THING].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | When summer came, the town had no rain. | 여름이 왔을 때, 그 마을에는 비가 오지 않았어요. | 3.0 ⚠️저점 | 'the town had no rain'은 비관용이다(there was no rain) — 주어·구문 교체로 수정 가능하나 슬롯 충돌은 구조적. | 불합격 — 'the town had no rain'은 비관용이고 THING 슬롯이 사람 소유물이어야 성립 |
| 3 | When morning came, my brother had no time. | 아침이 왔을 때, 형은 시간이 없었어요. | 3.67 ⚠️저점 | 'morning came'과 '시간이 없었다'의 연결이 느슨하다 — 값 교체로 수정 가능. | 수정: When winter came, my brother had no coat. / KR: 겨울이 왔을 때, 형은 코트가 없었어요. [어휘승인요청: coat] |
| 4 | When lunch time came, the store had no bread. | 점심시간이 됐을 때, 가게에는 빵이 없었어요. | 3.33 ⚠️저점 | 가게에 빵이 없다는 서술은 성립하나 사람 슬롯이 아니어서 고정부와 살짝 어긋난다 — 수정 가능. | 수정: When lunch time came, the children had no food. / KR: 점심시간이 됐을 때, 아이들은 먹을 것이 없었어요. |

## M01_029 (real, curriculum) — 씨앗: This is my family.
- 패턴: `This is my [THING].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | This is my room. | 여기가 제 방이에요. | 4.67 | 집을 소개하는 실제 발화로 고빈도다 — 결함 없음. | 합격 |
| 3 | This is my phone. | 이건 제 휴대폰이에요. | 4.0 | 자연스럽지만 앞 후보들과 같은 사물 소개 반복이다 — 구조적(중복). | 합격 |

## M01_031 (movie, c1_rewritten) — 씨앗: I love my family very much.
- 패턴: `I love my [THING] very much.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | I love my job very much. | 저는 제 일을 정말 좋아해요. | 3.67 ⚠️저점 | 사물 목적어에 'very much'가 붙으면 딱딱한 번역투다 — very much 삭제로 수정 가능. | 씨앗결함 — 고정부 'very much'가 사물·장소 목적어와 결합하지 않아 사람 이외의 슬롯 값 전체가 번역투가 됨 / 대안 씨앗: I really like my job. |
| 2 | I love my new school very much. | 저는 새 학교를 정말 좋아해요. | 3.67 ⚠️저점 | 고정부 'very much'가 사물과 어울리지 않는다 — 삭제로 수정 가능. | 씨앗결함 — 고정부 'very much'가 사물·장소 목적어와 결합하지 않아 사람 이외의 슬롯 값 전체가 번역투가 됨 / 대안 씨앗: I really like my job. |
| 5 | I love my morning coffee very much. | 저는 아침 커피를 정말 좋아해요. | 3.0 ⚠️저점 | 'love my morning coffee very much'는 원어민이 쓰지 않는 조합이다 — very much 삭제로 수정 가능하나 슬롯 충돌은 구조적. | 씨앗결함 — 고정부 'very much'가 사물·장소 목적어와 결합하지 않아 사람 이외의 슬롯 값 전체가 번역투가 됨 / 대안 씨앗: I really like my job. |
| 6 | I love my small town very much. | 저는 우리 작은 마을을 정말 좋아해요. | 3.67 ⚠️저점 | 장소 목적어에 very much가 겹쳐 문어체가 된다 — 삭제로 수정 가능. | 씨앗결함 — 고정부 'very much'가 사물·장소 목적어와 결합하지 않아 사람 이외의 슬롯 값 전체가 번역투가 됨 / 대안 씨앗: I really like my job. |

## M01_034 (real, curriculum) — 씨앗: What is this?
- 패턴: `What is [THING]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | What is in the bag? | 가방 안에 뭐가 있어요? | 3.33 ⚠️저점 | 구어는 'What's in the bag?'이라 비축약형이 어색하다 — 축약으로 수정 가능. | 불합격 — 'in the bag'은 축약형 'What's ~?'를 요구해 비축약 고정부와 충돌 |
| 3 | What is your job? | 직업이 뭐예요? | 3.33 ⚠️저점 | 직업은 'What do you do?'로 묻는 게 관용이다 — 문형 교체로 수정 가능. | 불합격 — 직업은 'What do you do?'로 묻는 게 관용이라 이 프레임으로 표현할 수 없음 |

## M01_035 (real, curriculum) — 씨앗: What time is it?
- 패턴: `What [THING] is it?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | What number is it? | 몇 번이에요? | 3.67 ⚠️저점 | 무엇의 번호인지 불분명해 단독으로는 어색하다 — 명사 구체화로 수정 가능. | 불합격 — 무엇의 번호인지 지정할 수 없어 이 슬롯 값으로는 단독 발화가 성립하지 않음 |
| 5 | What word is it? | 무슨 단어예요? | 3.0 ⚠️저점 | 'What word is it?'은 비관용이다(What's the word?) — 구문 교체로 수정 가능하나 슬롯 충돌은 구조적. | 불합격 — 'What word is it?'은 비관용이고 THING 슬롯이 time/day 계열만 허용 |

## M01_036 (real, curriculum) — 씨앗: Where is the bathroom?
- 패턴: `Where is the [PLACE]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Where is the school? | 학교가 어디예요? | 3.67 ⚠️저점 | 문장은 자연스러우나 길 묻는 대상으로는 쓰임이 좁다 — 값 교체로 수정 가능. | 합격 |

## M01_037 (real, curriculum) — 씨앗: When is your birthday?
- 패턴: `When is your [EVENT]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | When is your first day at school? | 학교 첫날이 언제예요? | 4.0 | 개학 일정 묻기로 자연스럽다 — 축약형만 수정 가능. | 합격 |
| 4 | When is your next visit? | 다음 방문이 언제예요? | 3.33 ⚠️저점 | 'your next visit'은 사무적이라 A1 회화 상황과 거리가 있다 — 값 교체로 수정 가능. | 수정: When is your next trip? / KR: 다음 여행이 언제예요? |

## M01_038 (real, curriculum) — 씨앗: How are you doing?
- 패턴: `How are [PERSON] doing?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | How are the people at work doing? | 직장 사람들은 어떻게 지내요? | 2.67 ⚠️저점 | 'the people at work'를 안부 대상으로 쓰지 않는다(How are things at work?) — 구문 교체로 수정 가능하나 슬롯 충돌은 구조적. | 불합격 — 'the people at work'는 안부 대상으로 쓰지 않고 PERSON 슬롯이 개인만 허용 |

## M01_039 (real, curriculum) — 씨앗: Can you help me?
- 패턴: `Can you [VERB-PHRASE]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Can you open the window? | 창문 좀 열어 줄래요? | 4.67 | 부탁 표현으로 고빈도이고 짧다 — 결함 없음. | 합격 |
| 2 | Can you call me tomorrow? | 내일 저한테 전화해 줄래요? | 4.33 | 실제로 자주 쓰는 부탁이다 — 결함 없음. | 합격 |
| 3 | Can you speak English? | 영어 할 줄 알아요? | 4.33 | 능력을 묻는 용법까지 보여 준다(정중형은 Do you speak English?) — 결함 없음. | 합격 |
| 6 | Can you show me the way? | 길 좀 알려 줄래요? | 4.33 | 길 묻기 부탁으로 관용적이다 — 결함 없음. | 합격 |

## M01_040 (movie, c1_rewritten) — 씨앗: Why is my coffee cold?
- 패턴: `Why is my [THING] [ADJECTIVE]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | Why is my bag empty? | 왜 제 가방이 비어 있는 거죠? | 3.67 ⚠️저점 | 가방이 비었다는 상황이 잘 안 그려진다 — ADJECTIVE 값 교체로 수정 가능. | 수정: Why is my glass empty? / KR: 왜 제 잔이 비어 있는 거죠? [어휘승인요청: glass] |
| 6 | Why is my rice hard? | 왜 제 밥이 딱딱한 거죠? | 3.67 ⚠️저점 | 밥이 'hard'는 설익음을 뜻하기에 표현이 정확하지 않다 — 형용사 교체로 수정 가능. | 수정: Why is my bread hard? / KR: 왜 제 빵이 딱딱한 거죠? |

## M01_041 (movie, c1_rewritten) — 씨앗: Good luck! I believe in you.
- 패턴: `[CHEER-PHRASE]! I believe in you.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | You're ready! I believe in you. | 준비됐어요! 저는 당신을 믿어요. | 4.33 | 응원 상황에 맞고 축약형도 지켰다 — 결함 없음. | 합격 |
| 5 | It's okay! I believe in you. | 괜찮아요! 저는 당신을 믿어요. | 3.67 ⚠️저점 | 'It's okay'는 위로라 응원 자리와 기능이 어긋난다 — 문구 교체로 수정 가능. | 수정: You can do it! I believe in you. / KR: 할 수 있어요! 저는 당신을 믿어요. |

## M01_043 (real, curriculum) — 씨앗: I live in Seoul.
- 패턴: `I live in [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | I live in a big city. | 저는 큰 도시에 살아요. | 4.67 | 고빈도 답변으로 자연스럽다 — 결함 없음. | 합격 |
| 6 | I live in the country. | 저는 시골에 살아요. | 3.67 ⚠️저점 | 'the country'가 나라·시골 두 뜻으로 읽혀 A1에게 모호하다 — countryside로 수정 가능. | 수정: I live in a small town. / KR: 저는 작은 마을에 살아요. |

## M01_046 (real, curriculum) — 씨앗: Please sit down and relax.
- 패턴: `Please [ACTION-A] and [ACTION-B].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Please come in and have some tea. | 들어와서 차 한잔하세요. | 4.67 | 손님 맞이 발화로 두 동작이 관용적으로 이어진다 — 결함 없음. | 합격 |
| 2 | Please stop and think. | 잠깐 멈추고 생각해 보세요. | 3.67 ⚠️저점 | 'stop and think'는 굳은 조합이나 Please가 붙으면 설교체가 된다 — 문구 교체로 수정 가능. | 불합격 — 'stop and think'에 Please가 붙으면 설교체가 되어 이 슬롯 조합이 부적합 |
| 3 | Please go home and sleep. | 집에 가서 주무세요. | 3.67 ⚠️저점 | 관용형은 'go home and get some sleep'이다 — 동사구 교체로 수정 가능. | 수정: Please go home and get some sleep. / KR: 집에 가서 좀 주무세요. |
| 5 | Please slow down and eat. | 천천히 드세요. | 3.0 ⚠️저점 | 'slow down and eat'은 원어민이 쓰지 않는 결합이다(Eat slowly). KR도 두 동작을 살리지 못했다 — 구조적. | 불합격 — 'slow down and eat'은 비관용이고 두 동작 슬롯으로 분리되지 않음 |
| 6 | Please turn off the TV and sleep. | TV 끄고 주무세요. | 3.67 ⚠️저점 | 관용형은 'and go to sleep'이다 — 동사구 교체로 수정 가능. | 수정: Please turn off the TV and go to sleep. / KR: TV 끄고 주무세요. |

## M01_047 (real, curriculum) — 씨앗: Stand up when the teacher comes in.
- 패턴: `[COMMAND] when [PERSON] comes in.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Say hello when the new student comes in. | 새로 온 학생이 들어오면 인사하세요. | 4.33 | 교실 지시로 자연스럽고 두 절이 잘 붙는다 — 결함 없음. | 합격 |

## M01_050 (real, curriculum) — 씨앗: My computer is very slow today.
- 패턴: `My [THING] is very [ADJECTIVE] today.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 5 | My car is very dirty today. | 오늘 제 차가 아주 지저분해요. | 3.67 ⚠️저점 | 차가 더러운 건 하루치 상태가 아니라 today와 겉돈다. 수정 가능(today 빼거나 really). | 수정: My room is very cold today. / KR: 오늘 제 방이 아주 추워요. |

## M02_004 (tale, curriculum) — 씨앗: She went inside and saw three bowls of porridge.
- 패턴: `She went inside and saw [THING].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | She went inside and saw many people. | 그녀는 안으로 들어가서 많은 사람들을 봤어요. | 3.67 ⚠️저점 | 긍정문에서는 a lot of people이 원어민 기본. 수정 가능(many 교체). | 수정: She went inside and saw a lot of people. / KR: 그녀는 안으로 들어가서 사람이 많은 걸 봤어요. |
| 5 | She went inside and saw an open window. | 그녀는 안으로 들어가서 열린 창문을 봤어요. | 4.33 | an open window, 자연스러운 관찰. 결함 없음. | 합격 |

## M02_006 (tale, curriculum) — 씨앗: This one is too cold. This one is just right!
- 패턴: `This one is too [ADJECTIVE]. This one is just right!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | This one is too big. This one is just right! | 이건 너무 커. 이건 딱 좋아! | 3.67 ⚠️저점 | 두 문장 모두 This one이라 가리키는 대상이 겹친다(앞은 That one). 구조적. | 씨앗결함 — 두 문장 모두 'This one'이라 대조가 성립하지 않는 지시 결함 / 대안 씨앗: That one is too cold. This one is just right! |
| 3 | This one is too expensive. This one is just right! | 이건 너무 비싸. 이건 딱 좋아! | 3.67 ⚠️저점 | 같은 지시 충돌. 가격 비교 상황 자체는 유용하다. 구조적. | 씨앗결함 — 두 문장 모두 'This one'이라 대조가 성립하지 않는 지시 결함 / 대안 씨앗: That one is too cold. This one is just right! |
| 6 | This one is too short. This one is just right! | 이건 너무 짧아. 이건 딱 좋아! | 3.67 ⚠️저점 | 같은 지시 충돌. 구조적. | 씨앗결함 — 두 문장 모두 'This one'이라 대조가 성립하지 않는 지시 결함 / 대안 씨앗: That one is too cold. This one is just right! |

## M02_007 (real, curriculum) — 씨앗: I wake up at 7 o'clock every morning.
- 패턴: `I [VERB-PHRASE] at [TIME] every morning.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | I eat breakfast at 8 o'clock every morning. | 저는 매일 아침 8시에 아침을 먹어요. | 4.67 | 아침 일과 설명에 그대로 쓴다. 결함 없음. | 합격 |

## M02_010 (movie, c1_rewritten) — 씨앗: Don't stop now. You can do it!
- 패턴: `Don't stop now. You can [VERB-PHRASE]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Don't stop now. You can learn it! | 지금 멈추지 마세요. 익힐 수 있어요! | 3.67 ⚠️저점 | You can learn it은 응원 자리에 잘 안 쓴다. 수정 가능(do it). | 수정: Don't stop now. You can finish it! / KR: 지금 멈추지 마세요. 끝까지 할 수 있어요! |
| 6 | Don't stop now. You can eat later! | 지금 멈추지 마세요. 밥은 이따 먹으면 돼요! | 3.67 ⚠️저점 | 응원 고정부에 '밥은 이따'가 와서 기능이 어긋난다. 구조적. | 불합격 — 'eat later'는 응원 고정부와 기능이 어긋남 |

## M02_011 (proverb, curriculum) — 씨앗: Time flies when you're having fun.
- 패턴: `Time flies when you're [ACTIVITY-ING].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Time flies when you're swimming. | 수영하다 보면 시간이 빨리 가요. | 3.67 ⚠️저점 | 수영 중에 시간 얘기를 하는 상황이 드물다. 수정 가능(슬롯 교체). | 수정: Time flies when you're reading. / KR: 책을 읽다 보면 시간이 빨리 가요. |

## M02_012 (quote, c1_rewritten) — 씨앗: Just be yourself.
- 패턴: `Just be [STATE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Just be happy. | 그냥 즐겁게 지내요. | 3.67 ⚠️저점 | Just be happy는 훈계조라 실제 발화 상황이 좁다. 구조적. | 불합격 — 'Just be happy'는 훈계로 들려 실제 발화 자리가 성립하지 않음 |

## M02_014 (tale, curriculum) — 씨앗: A bad fairy put a curse on the princess.
- 패턴: `A [PERSON] put a [THING] on the [TARGET].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 5 | A boy put a letter on the door. | 한 남자아이가 문에 편지를 붙여 놨어요. | 3.0 ⚠️저점 | 문에 편지를 put on 하지 않는다(tape to/leave at). KR '붙여 놨어요'도 원문과 어긋난다. 수정 가능. | 수정: A boy put a letter on the table. / KR: 한 남자아이가 탁자에 편지를 놓았어요. [어휘승인요청: table] |

## M02_015 (tale, curriculum) — 씨앗: The princess will sleep for 100 years!
- 패턴: `[PERSON] will sleep for [DURATION]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | My brother will sleep for ten hours! | 우리 형은 열 시간 동안 잘 거예요! | 3.67 ⚠️저점 | 습관이면 sleeps가 맞다. 수정 가능(will→현재형). | 합격 |
| 4 | My grandfather will sleep for one hour! | 할아버지는 한 시간 동안 주무실 거예요! | 3.0 ⚠️저점 | for an hour가 맞고 한 시간에 감탄부호도 안 어울린다. 수정 가능. | 수정: My grandfather will sleep for an hour! / KR: 할아버지는 한 시간 동안 주무실 거예요! |
| 5 | My sister will sleep for five more minutes! | 언니는 딱 5분만 더 잘 거래요! | 3.33 ⚠️저점 | five more minutes는 관용이나 will과 붙으면 어색. 수정 가능. | 불합격 — 'five more minutes'는 즉시성 표현이라 will 고정부와 결합하지 않음 |
| 6 | My husband will sleep for two hours! | 남편은 두 시간 동안 잘 거예요! | 3.67 ⚠️저점 | 습관이면 sleeps. 수정 가능. | 합격 |

## M02_016 (tale, curriculum) — 씨앗: One day, a prince came to the castle.
- 패턴: `One day, [PERSON] came to the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | One day, a little cat came to the garden. | 어느 날, 작은 고양이가 정원에 왔어요. | 3.67 ⚠️저점 | 고양이는 came into/showed up in이 자연스럽다. 수정 가능. | 수정: One day, a little cat came to the house. / KR: 어느 날, 작은 고양이가 집에 왔어요. |
| 5 | One day, a letter came to the house. | 어느 날, 편지 한 통이 집에 왔어요. | 3.0 ⚠️저점 | [PERSON] 슬롯에 편지가 들어가 슬롯 유형이 깨졌다. 구조적. | 불합격 — [PERSON] 슬롯에 사물(letter)이 들어가 슬롯 유형이 깨짐 |
| 6 | One day, a new family came to the town. | 어느 날, 새 가족이 마을에 이사 왔어요. | 3.67 ⚠️저점 | came to town이 관용, the가 붙으면 어색. 수정 가능(the 삭제). | 불합격 — 'came to town'이 관용이라 'the [PLACE]' 고정부와 결합하지 않음 |

## M02_017 (tale, curriculum) — 씨앗: He kissed the princess and she woke up.
- 패턴: `He [ACTION] and she woke up.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | He played music and she woke up. | 그가 음악을 틀자 그녀가 깼어요. | 3.67 ⚠️저점 | put on music이 원어민 기본. 수정 가능. | 수정: He put on music and she woke up. / KR: 그가 음악을 틀자 그녀가 깼어요. |

## M02_018 (real, curriculum) — 씨앗: I turn on the TV after dinner.
- 패턴: `I [ACTIVITY] after dinner.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | I drink tea after dinner. | 저녁 먹고 차를 마셔요. | 4.33 | have tea가 조금 더 흔하다. 수정 가능. | 수정: I have tea after dinner. / KR: 저녁 먹고 차를 마셔요. |
| 5 | I eat some fruit after dinner. | 저녁 먹고 과일을 먹어요. | 4.33 | have some fruit이 더 흔하다. 수정 가능. | 수정: I have some fruit after dinner. / KR: 저녁 먹고 과일을 먹어요. |

## M02_020 (movie, c1_rewritten) — 씨앗: Don't worry. Everything will be okay.
- 패턴: `Don't worry. [SUBJECT] will be okay.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Don't worry. The weather will be okay. | 걱정 마세요. 날씨는 괜찮을 거예요. | 3.67 ⚠️저점 | 날씨에는 be fine이 짝이고 okay는 어색. 수정 가능. | 수정: Don't worry. Your father will be okay. / KR: 걱정 마세요. 아버지는 괜찮을 거예요. |

## M02_022 (quote, c1_rewritten) — 씨앗: I want to look nice today.
- 패턴: `I want to [VERB-PHRASE] today.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | I want to walk to work today. | 오늘은 걸어서 출근하고 싶어요. | 4.33 | walk to work, 자연스럽다. 결함 없음. | 합격 |
| 6 | I want to drink less coffee today. | 오늘은 커피를 줄이고 싶어요. | 3.67 ⚠️저점 | drink less coffee는 기간 목표라 today와 부딪힌다. 수정 가능. | 수정: I want to eat more fruit today. / KR: 오늘은 과일을 더 많이 먹고 싶어요. |

## M02_024 (real, curriculum) — 씨앗: I take off my shoes at the door.
- 패턴: `I take off my [THING] at the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | I take off my raincoat at the station. | 역에서 우비를 벗어요. | 3.67 ⚠️저점 | 역에서 우비를 벗는 습관은 상황이 너무 좁다. 수정 가능(장소 교체). | 수정: I take off my raincoat at the door. / KR: 문 앞에서 우비를 벗어요. |

## M02_025 (real, curriculum) — 씨앗: I get dressed quickly in the morning.
- 패턴: `I [VERB-PHRASE] quickly in the morning.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | I wake up quickly in the morning. | 저는 아침에 빨리 일어나요. | 3.33 ⚠️저점 | wake up은 의지로 빨리 하는 동작이 아니라 quickly와 안 붙는다. 수정 가능(get up). | 수정: I get up quickly in the morning. / KR: 저는 아침에 빨리 일어나요. |
| 2 | I eat breakfast quickly in the morning. | 저는 아침에 빨리 아침 식사를 해요. | 3.67 ⚠️저점 | 원어민은 eat fast나 have a quick breakfast. 수정 가능. | 불합격 — 'eat breakfast quickly'는 'have a quick breakfast'가 관용이라 이 프레임에서 부자연스러움 |
| 3 | I brush my teeth quickly in the morning. | 저는 아침에 빨리 이를 닦아요. | 3.67 ⚠️저점 | 가능하지만 부사 위치가 뻣뻣하다. 수정 가능. | 합격 |
| 4 | I clean my room quickly in the morning. | 저는 아침에 빨리 방을 청소해요. | 3.67 ⚠️저점 | 아침에 방 청소를 서둘러 한다는 설정이 좁다. 수정 가능. | 수정: I put on my shoes quickly in the morning. / KR: 저는 아침에 빨리 신발을 신어요. |
| 5 | I make my bed quickly in the morning. | 저는 아침에 빨리 침대를 정리해요. | 3.67 ⚠️저점 | 무난하나 quickly가 겉돈다. 수정 가능. | 합격 |
| 6 | I take a shower quickly in the morning. | 저는 아침에 빨리 샤워해요. | 3.33 ⚠️저점 | take a quick shower가 원어민 기본. 수정 가능. | 불합격 — 'take a quick shower'가 관용이라 부사를 뒤에 붙이는 고정부와 충돌 |

## M02_026 (real, curriculum) — 씨앗: What's the weather like today?
- 패턴: `What's the [NOUN] like [TIME]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | What's the hotel like this week? | 이번 주 호텔이 어때요? | 3.67 ⚠️저점 | 호텔 평가는 시간 슬롯과 안 붙는다. 수정 가능(시간 제거). | 불합격 — 호텔 평가는 시간에 따라 변하지 않아 [TIME] 슬롯 프레임과 결합하지 않음 |
| 6 | What's the school like on Monday? | 월요일에 학교는 어때요? | 3.0 ⚠️저점 | 성격을 묻는 틀에 요일이 들어가 충돌한다. 구조적. | 불합격 — 성격을 묻는 틀에 요일이 들어가 충돌 |

## M02_028 (real, curriculum) — 씨앗: It's raining outside.
- 패턴: `It's [STATE] outside.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | It's getting sunny outside. | 밖이 화창해지고 있어요. | 3.67 ⚠️저점 | getting sunny는 잘 안 쓴다(clearing up). 수정 가능. | 수정: It's getting cold outside. / KR: 밖이 추워지고 있어요. |

## M02_029 (real, curriculum) — 씨앗: Hurry up! We're late!
- 패턴: `[EXCLAMATION]! We're late!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Hurry now! We're late! | 지금 서둘러요! 늦었어요! | 3.0 ⚠️저점 | Hurry now가 아니라 Hurry up이다. 수정 가능. | 수정: Let's go! We're late! / KR: 빨리 가요! 늦었어요! |

## M02_032 (quote, c1_rewritten) — 씨앗: Don't waste your time. You can't get it back.
- 패턴: `Don't waste your time. You can't [VERB-PHRASE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | Don't waste your time. You can't turn it around. | 시간을 낭비하지 마세요. 다시 되돌릴 수 없어요. | 3.33 ⚠️저점 | turn it around는 보통 긍정 전환에 써서 can't와 어색. 수정 가능. | 불합격 — 'turn it around'는 부정문·시간 목적어와 결합하지 않음 |
| 3 | Don't waste your time. You can't stop it. | 시간을 낭비하지 마세요. 멈출 수 없어요. | 3.67 ⚠️저점 | it이 가리킬 것이 앞에 없다. 수정 가능. | 합격 |
| 4 | Don't waste your time. You can't buy more. | 시간을 낭비하지 마세요. 더 살 수 없어요. | 3.33 ⚠️저점 | buy more의 목적어가 비어 뜻이 안 선다. KR '더 살 수 없어요'도 살다/사다 중의성. 수정 가능. | 수정: Don't waste your time. You can't buy more time. / KR: 시간을 낭비하지 마세요. 시간은 더 살 수 없어요. |
| 5 | Don't waste your time. You can't do it again. | 시간을 낭비하지 마세요. 다시 할 수 없어요. | 3.67 ⚠️저점 | 무난하나 it 지시가 비어 있다. 수정 가능. | 합격 |

## M02_033 (real, curriculum) — 씨앗: What time do you usually wake up?
- 패턴: `What time do you usually [VERB-PHRASE]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | What time do you usually look at your phone? | 보통 몇 시에 휴대폰을 봐요? | 3.0 ⚠️저점 | 폰 보는 시각을 물어보는 상황이 없다. 구조적. | 불합격 — 휴대폰 보는 시각을 묻는 발화 상황이 없어 슬롯 값이 성립하지 않음 |

## M02_034 (real, curriculum) — 씨앗: I usually go to bed at 11 PM.
- 패턴: `I usually [VERB-PHRASE] at [TIME].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | I usually look at my phone at noon. | 보통 정오에 휴대폰을 봐요. | 3.0 ⚠️저점 | 정오에 폰 보기를 습관으로 말하지 않는다. 구조적. | 불합격 — 정오에 휴대폰 보기를 습관으로 서술하는 상황이 성립하지 않음 |

## M02_035 (real, curriculum) — 씨앗: I have breakfast at 8 o'clock.
- 패턴: `I have [MEAL] at [TIME].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | I have coffee at 9 o'clock. | 9시에 커피를 마셔요. | 4.33 | have coffee도 관용이나 [MEAL] 슬롯을 살짝 벗어난다. | 합격 |
| 6 | I have cake at 3 o'clock. | 3시에 케이크를 먹어요. | 3.67 ⚠️저점 | cake는 MEAL이 아니라 슬롯 유형이 어긋난다. 수정 가능. | 수정: I have lunch at 12 o'clock. / KR: 12시에 점심을 먹어요. |

## M02_038 (real, curriculum) — 씨앗: Let's clean up the room.
- 패턴: `Let's clean up the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Let's clean up the garden. | 같이 정원을 청소해요. | 3.67 ⚠️저점 | 정원은 tidy up이나 clean up the yard가 자연스럽다. 수정 가능. | 수정: Let's clean up the kitchen. / KR: 같이 부엌을 치워요. |

## M02_041 (tale, curriculum) — 씨앗: The three bears came home.
- 패턴: `[WHO] came home.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | The students came home. | 학생들이 집에 왔어요. | 3.67 ⚠️저점 | 학생들이 '집에 왔다'는 주체가 흐리다. 수정 가능. | 수정: The children came home. / KR: 아이들이 집에 왔어요. |

## M02_043 (real, curriculum) — 씨앗: Don't forget your umbrella!
- 패턴: `Don't forget your [OBJECT]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Don't forget your raincoat! | 우비를 잊지 마세요! | 4.33 | 비 오는 날 발화로 맞는다. | 합격 |

## M02_045 (movie, c1_rewritten) — 씨앗: Don't forget me!
- 패턴: `Don't forget [PERSON]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | Don't forget him! | 그를 잊지 마세요! | 3.67 ⚠️저점 | him이 누군지 문맥 없이는 안 선다. 수정 가능. | 합격 |
| 3 | Don't forget her! | 그녀를 잊지 마세요! | 3.67 ⚠️저점 | her도 같은 지시 문제. 수정 가능. | 합격 |
| 4 | Don't forget your family! | 가족을 잊지 마세요! | 3.67 ⚠️저점 | 가족을 잊지 말라는 건 훈계조라 발화 자리가 좁다. 수정 가능. | 불합격 — 훈계조가 되어 작별 인사 기능과 어긋남 |
| 5 | Don't forget your sister! | 여동생을 잊지 마세요! | 3.67 ⚠️저점 | 데리러 가라는 뜻인지 뜻이 갈린다. 수정 가능. | 불합격 — 'your sister'는 데리러 가라는 뜻으로도 읽혀 이 프레임에서 뜻이 갈림 |
| 6 | Don't forget your teacher! | 선생님을 잊지 마세요! | 3.0 ⚠️저점 | 선생님을 잊지 말라고 하는 상황이 안 그려진다. 구조적. | 불합격 — 선생님을 잊지 말라고 말하는 발화 상황이 성립하지 않음 |

## M02_046 (real, curriculum) — 씨앗: Good morning! How are you doing today?
- 패턴: `[GREETING]! How are you doing [TIME]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Good afternoon! How are you doing this week? | 좋은 오후예요! 이번 주 어떻게 지내요? | 3.33 ⚠️저점 | Good afternoon과 this week가 안 붙고, KR '좋은 오후예요'는 쓰지 않는 번역투. 수정 가능. | 수정: Good afternoon! How are you doing today? / KR: 안녕하세요! 오늘 어떻게 지내요? |
| 3 | Hi! How are you doing these days? | 안녕하세요! 요즘 어떻게 지내요? | 4.67 | Hi + these days, 그대로 쓴다. 결함 없음. | 합격 |
| 6 | Hi! How are you doing right now? | 안녕하세요! 지금 어떻게 지내요? | 3.0 ⚠️저점 | 인사 뒤에 right now는 붙지 않는다. 구조적. | 불합격 — 인사 뒤에 'right now'가 결합하지 않음 |

## M02_047 (real, curriculum) — 씨앗: We can walk or take the bus.
- 패턴: `We can [OPTION-A] or [OPTION-B].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | We can swim or run. | 우리는 수영하거나 뛸 수 있어요. | 3.67 ⚠️저점 | 수영과 달리기를 놓고 고르는 상황이 막연하다. 수정 가능. | 수정: We can walk or take the train. / KR: 우리는 걷거나 기차를 탈 수 있어요. |
| 5 | We can fly or swim. | 우리는 비행기를 타거나 수영할 수 있어요. | 3.0 ⚠️저점 | fly가 비행기인지 사람이 나는 건지 갈린다. 구조적. | 불합격 — 'fly'가 비행기 탑승인지 나는 것인지 갈려 슬롯 값이 성립하지 않음 |

## M03_002 (tale, curriculum) — 씨앗: Once upon a time, there was a girl called Little Red Riding Hood.
- 패턴: `Once upon a time, there was a [WHO] called [NAME].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Once upon a time, there was a girl called Anna. | 옛날에, 안나라고 불리는 소녀가 있었어요. | 3.67 ⚠️저점 | 동화 정형구로 자연스럽고 girl/Anna 조합도 무난 — 이름만 바뀌어 치환 novelty가 없는 건 구조적. KR '불리는'은 다소 딱딱(수정 가능). | 불합격 — 씨앗과 WHO 값이 같고 이름만 바뀌어 치환 학습 가치가 없음 |
| 2 | Once upon a time, there was a boy called Tom. | 옛날에, 톰이라고 불리는 소년이 있었어요. | 3.67 ⚠️저점 | boy/Tom도 동화 도입부로 무난 — 치환이 이름 교체에 머무는 건 구조적. | 수정(KR만): 옛날에, 톰이라는 소년이 있었어요. |
| 3 | Once upon a time, there was a woman called Sarah. | 옛날에, 사라라고 불리는 여자가 있었어요. | 3.67 ⚠️저점 | woman/Sarah 조합 자연 — 씨앗 상황을 그대로 반복(구조적). | 수정(KR만): 옛날에, 사라라는 여자가 있었어요. |
| 4 | Once upon a time, there was a man called David. | 옛날에, 데이빗이라고 불리는 남자가 있었어요. | 3.67 ⚠️저점 | man/David 조합 자연 — 치환 novelty 낮음(구조적). | 수정(KR만): 옛날에, 데이빗이라는 남자가 있었어요. |
| 5 | Once upon a time, there was a student called Mia. | 옛날에, 미아라고 불리는 학생이 있었어요. | 3.33 ⚠️저점 | 'a student called Mia'는 옛날 이야기 도입부와 레지스터가 충돌 — WHO 값 교체로 수정 가능. | 수정: Once upon a time, there was a young woman called Mia. / KR: 옛날에, 미아라는 젊은 여자가 있었어요. [어휘승인요청: young] |
| 6 | Once upon a time, there was a teacher called James. | 옛날에, 제임스라고 불리는 선생님이 있었어요. | 3.33 ⚠️저점 | 'a teacher called James'도 동화 오프닝에 안 맞는 현대 직업명 — 값 교체로 수정 가능. | 수정: Once upon a time, there was a king called James. / KR: 옛날에, 제임스라는 왕이 있었어요. [어휘승인요청: king] |

## M03_004 (tale, curriculum) — 씨앗: "Don't talk to strangers on the way!"
- 패턴: `"Don't [VERB-PHRASE] on the way!"`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | "Don't stop for strangers on the way!" | "가는 길에 낯선 사람이랑 멈추지 마!" | 3.67 ⚠️저점 | 'stop for strangers'는 비관용 조합(원어민은 stop and talk to) — 동사구 교체로 수정 가능. KR '낯선 사람이랑 멈추지 마'는 오역. | 수정: "Don't stop and talk to strangers on the way!" / KR: "가는 길에 멈춰서 낯선 사람과 이야기하지 마!" |
| 2 | "Don't play on the way!" | "가는 길에 놀지 마!" | 3.67 ⚠️저점 | 'Don't play on the way'는 원어민이 잘 안 쓰는 조합(play around/dawdle이 관용) — 수정 가능. | 수정: "Don't stop to play on the way!" / KR: "가는 길에 놀려고 멈추지 마!" |
| 3 | "Don't run on the way!" | "가는 길에 뛰지 마!" | 3.67 ⚠️저점 | 'run on the way'도 비관용 — 부사구 없이 'Don't run!'이 자연, 수정 가능. | 불합격 — 'run on the way'는 비관용이고 경로 부사구를 살릴 슬롯 값이 없음 |
| 5 | "Don't forget your bag on the way!" | "가는 길에 가방 잊지 마!" | 3.0 ⚠️저점 | 'forget your bag on the way'는 고정부와 충돌(잊는 건 장소지 경로가 아님) — 구조적. | 불합격 — 물건을 잊는 행위는 경로 부사구와 결합하지 않음 |
| 6 | "Don't lose your money on the way!" | "가는 길에 돈 잃어버리지 마!" | 3.67 ⚠️저점 | 'lose your money on the way'는 이해는 되나 관용도가 낮음 — 수정 가능. | 합격 |

## M03_005 (tale, curriculum) — 씨앗: A wolf stopped her in the forest.
- 패턴: `[WHO] stopped her in the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | Her teacher stopped her in the school. | 선생님이 학교에서 그녀를 멈추게 했어요. | 3.0 ⚠️저점 | 'in the school'은 관사·전치사가 어긋난 비관용(at school) — 수정 가능, KR 오역도 동일. | 수정: Her teacher stopped her in the store. / KR: 선생님이 가게에서 그녀를 불러 세웠어요. |
| 4 | A doctor stopped her in the hospital. | 의사가 병원에서 그녀를 멈추게 했어요. | 3.67 ⚠️저점 | 'in the hospital'은 입원 뜻으로 읽혀 어색(in the hallway 등) — 수정 가능, KR 오역 동일. | 수정: A doctor stopped her in the hallway. / KR: 의사가 복도에서 그녀를 불러 세웠어요. [어휘승인요청: hallway] |
| 6 | A stranger stopped her in the city. | 낯선 사람이 도시에서 그녀를 멈추게 했어요. | 3.67 ⚠️저점 | 'in the city'는 장소로 막연(on the street가 자연) — 수정 가능, KR 오역 동일. | 수정: A stranger stopped her in the park. / KR: 낯선 사람이 공원에서 그녀를 불러 세웠어요. |

## M03_006 (tale, curriculum) — 씨앗: "Where are you going?" asked the wolf.
- 패턴: `"Where are you going?" asked [WHO].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | "Where are you going?" asked my mother. | "어디 가니?" 엄마가 물었어요. | 3.67 ⚠️저점 | 인용문은 자연하나 슬롯이 화자만 바뀌어 씨앗 상황 반복 — 구조적. | 합격 |
| 2 | "Where are you going?" asked the teacher. | "어디 가니?" 선생님이 물었어요. | 3.67 ⚠️저점 | 자연스럽지만 화자 교체뿐이라 패턴 학습 가치가 낮음 — 구조적. | 합격 |
| 4 | "Where are you going?" asked my sister. | "어디 가니?" 언니가 물었어요. | 3.67 ⚠️저점 | 자연하나 치환 novelty 없음 — 구조적. | 합격 |
| 5 | "Where are you going?" asked the doctor. | "어디 가니?" 의사 선생님이 물었어요. | 3.33 ⚠️저점 | 의사가 이 질문을 하는 상황이 잘 안 그려지고 화자 교체뿐 — 구조적. | 불합격 — 의사가 이 질문을 하는 서사 상황이 성립하지 않음 |

## M03_007 (real, curriculum) — 씨앗: How do I get to the station?
- 패턴: `How do I get to the [PLACE]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | How do I get to the park? | 공원에 어떻게 가요? | 4.67 | 고빈도 관용문 — 결함 없음. | 합격 |
| 5 | How do I get to the school? | 학교에 어떻게 가요? | 4.33 | 'the school'은 특정 학교를 전제 — 문맥이 있으면 자연, 결함 없음 수준. | 합격 |

## M03_008 (real, curriculum) — 씨앗: I get on the bus at this stop.
- 패턴: `I get on the bus at [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 5 | I get on the bus at the corner near my house. | 우리 집 근처 모퉁이에서 버스를 타요. | 3.33 ⚠️저점 | 의미는 자연하나 11단어로 A1 길이 초과 — 수식구 삭제로 수정 가능. | 수정: I get on the bus at the corner. / KR: 모퉁이에서 버스를 타요. |
| 6 | I get on the bus at the hotel. | 호텔에서 버스를 타요. | 4.33 | 호텔 픽업 상황으로 자연 — 결함 없음. | 합격 |

## M03_010 (movie, c1_rewritten) — 씨앗: Let's do something fun outside!
- 패턴: `Let's do something [ADJ] outside!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | Let's do something different outside! | 같이 밖에서 다른 걸 해 봐요! | 3.67 ⚠️저점 | 'do something different'는 관용이나 outside와 붙으면 어색 — 형용사 교체로 수정 가능. | 불합격 — 'do something different'는 outside와 결합이 어색해 이 슬롯 값이 부적합 |
| 3 | Let's do something nice outside! | 같이 밖에서 좋은 걸 해 봐요! | 3.67 ⚠️저점 | 'do something nice outside'는 뜻이 막연해 발화 상황이 흐림 — 수정 가능. | 불합격 — 'do something nice outside'는 뜻이 막연해 발화 상황이 서지 않음 |
| 4 | Let's do something great outside! | 같이 밖에서 멋진 걸 해 봐요! | 3.0 ⚠️저점 | 'do something great'는 원어민이 쓰지 않는 조합 — 슬롯이 fun/cool 계열만 허용하는 구조적 한계. | 불합격 — 'do something great'는 비관용이고 ADJ 슬롯이 fun/cool 계열만 허용 |

## M03_011 (proverb, curriculum) — 씨앗: It's raining cats and dogs.
- 패턴: `It's raining [INTENSITY].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | It's raining all day. | 하루 종일 비가 와요. | 3.0 ⚠️저점 | 현재진행 + all day는 시제 충돌(It's been raining all day)이고 INTENSITY 슬롯에 기간이 들어감 — 구조적. | 씨앗결함 — 관용구 'cats and dogs'를 슬롯으로 취급해 어떤 값을 넣어도 관용구가 깨지고 진행 고정부와 시제가 충돌 / 대안 씨앗: 없음 (관용구는 치환 드릴에 부적합) |
| 5 | It's raining all night. | 밤새 비가 와요. | 3.0 ⚠️저점 | all night도 같은 시제 충돌·슬롯 불일치 — 구조적. | 씨앗결함 — 관용구 'cats and dogs'를 슬롯으로 취급해 어떤 값을 넣어도 관용구가 깨지고 진행 고정부와 시제가 충돌 / 대안 씨앗: 없음 (관용구는 치환 드릴에 부적합) |
| 6 | It's raining all week. | 일주일 내내 비가 와요. | 3.0 ⚠️저점 | all week는 시제 충돌이 더 뚜렷(It's been raining all week) — 구조적. | 씨앗결함 — 관용구 'cats and dogs'를 슬롯으로 취급해 어떤 값을 넣어도 관용구가 깨지고 진행 고정부와 시제가 충돌 / 대안 씨앗: 없음 (관용구는 치환 드릴에 부적합) |

## M03_012 (quote, c1_rewritten) — 씨앗: Take your time and look around.
- 패턴: `Take your time and [VERB-PHRASE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Take your time and watch the show. | 서두르지 말고 천천히 쇼를 보세요. | 3.67 ⚠️저점 | 서두르지 말라는 말 뒤에 오락 행위는 화용 충돌 — 수정 가능. KR '천천히 쇼를 보세요'도 오역. | 수정: Take your time and read the letter. / KR: 서두르지 말고 천천히 편지를 읽어 보세요. |
| 6 | Take your time and learn something new. | 서두르지 말고 천천히 새로운 걸 배워 보세요. | 3.67 ⚠️저점 | 'learn something new'는 서두름과 대비되는 행위가 아니라 결합이 느슨 — 수정 가능. | 수정: Take your time and do it well. / KR: 서두르지 말고 천천히 제대로 하세요. |

## M03_013 (tale, curriculum) — 씨앗: Hansel and Gretel lived with their father.
- 패턴: `[NAME] and [NAME2] lived with their [PERSON].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | Jack and Amy lived with their parents. | 잭과 에이미는 부모님과 함께 살았어요. | 4.0 | parents는 가장 평범해 동화 도입 훅으로는 약함 — 값 교체로 수정 가능. | 수정: Jack and Amy lived with their grandmother. / KR: 잭과 에이미는 할머니와 함께 살았어요. |

## M03_014 (tale, curriculum) — 씨앗: They got lost in the deep forest.
- 패턴: `[WHO] got lost in the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | The students got lost in the big station. | 학생들은 큰 역에서 길을 잃었어요. | 3.67 ⚠️저점 | 'the big station'은 원어민이 잘 안 쓰는 수식 — 'the station'으로 수정 가능. | 수정: The students got lost in the station. / KR: 학생들은 역에서 길을 잃었어요. |

## M03_015 (tale, curriculum) — 씨앗: They found a house made of candy!
- 패턴: `They found a [THING] made of [MATERIAL]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | They found a cake made of rice! | 그들은 쌀로 만든 케이크를 발견했어요! | 3.0 ⚠️저점 | 'a cake made of rice'는 비관용(made from/with, 또는 rice cake) — 재료 슬롯이 음식과 충돌하는 구조적 문제. | 불합격 — 'a cake made of rice'는 비관용(rice cake)이고 재료 슬롯이 고정부와 충돌 |
| 3 | They found a bowl made of chocolate! | 그들은 초콜릿으로 만든 그릇을 발견했어요! | 4.33 | 'a bowl made of chocolate' 자연 — 결함 없음. | 합격 |
| 6 | They found a salad made of fruit! | 그들은 과일로 만든 샐러드를 발견했어요! | 3.0 ⚠️저점 | 'a salad made of fruit'는 fruit salad라는 굳은 표현과 충돌 — 구조적. | 불합격 — 'a salad made of fruit'는 fruit salad라는 굳은 표현과 충돌 |

## M03_016 (tale, curriculum) — 씨앗: "Come in, children!" said the old woman.
- 패턴: `"Come in, [PERSON]!" said the [SPEAKER].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | "Come in, boys!" said the doctor. | "들어오렴, 얘들아!" 의사가 말했어요. | 3.67 ⚠️저점 | 의사가 'boys'라고 부르는 조합이 어색 — 호칭 교체로 수정 가능. | 수정: "Come in, boys!" said the teacher. / KR: "들어오렴, 얘들아!" 선생님이 말했어요. |
| 3 | "Come in, students!" said the man. | "들어와요, 학생들!" 남자가 말했어요. | 3.0 ⚠️저점 | 'Come in, students!'는 원어민이 쓰지 않는 호칭 — 호칭 슬롯이 everyone/class 계열만 허용하는 구조적 문제. | 불합격 — 'Come in, students!'는 호칭으로 쓰지 않고 슬롯이 everyone/class 계열만 허용 |
| 5 | "Come in, baby!" said the mother. | "들어오렴, 아가야!" 엄마가 말했어요. | 3.0 ⚠️저점 | 아기에게 'Come in'은 상황 자체가 성립하지 않음 — 구조적. | 불합격 — 아기에게 'Come in'을 말하는 상황 자체가 성립하지 않음 |
| 6 | "Come in, girls!" said the uncle. | "들어오렴, 얘들아!" 삼촌이 말했어요. | 3.67 ⚠️저점 | 'Come in, girls!'는 성립하나 삼촌 화자 조합이 약하고 KR이 girls를 '얘들아'로 뭉갬 — 수정 가능. | 수정: "Come in, girls!" said the mother. / KR: "들어오렴, 얘들아!" 엄마가 말했어요. |

## M03_017 (tale, curriculum) — 씨앗: The children were brave and escaped.
- 패턴: `The children were [ADJ] and [ACTION-PAST].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | The children were tired and slept. | 아이들은 피곤해서 잤어요. | 3.67 ⚠️저점 | 'were tired and slept'는 연결이 뚝 끊김(went to bed가 관용) — 동사 교체로 수정 가능. | 수정: The children were tired and went to bed. / KR: 아이들은 피곤해서 잠자리에 들었어요. |

## M03_018 (real, curriculum) — 씨앗: Go straight and turn left.
- 패턴: `Go straight and [NEXT-STEP].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | Go straight and walk to the station. | 직진해서 역까지 걸어가세요. | 3.67 ⚠️저점 | 'Go straight and walk to'는 의미가 겹쳐 군더더기 — 동사구 교체로 수정 가능. | 수정: Go straight and turn right. / KR: 직진해서 오른쪽으로 도세요. |

## M03_019 (real, curriculum) — 씨앗: It's on the right side.
- 패턴: `It's on the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | It's on the street. | 길가에 있어요. | 3.67 ⚠️저점 | 'It's on the street'는 위치 답으로 막연하고 노숙 뉘앙스도 있음 — 거리명 추가로 수정 가능. | 수정: It's on the corner. / KR: 모퉁이에 있어요. |

## M03_020 (real, curriculum) — 씨앗: I'm looking for the post office.
- 패턴: `I'm looking for the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | I'm looking for the bank. | 은행을 찾고 있어요. | 4.67 | 길 찾기 고빈도 문장, 축약형도 지킴 — 결함 없음. | 합격 |

## M03_021 (movie, c1_rewritten) — 씨앗: I'm happy when I get home.
- 패턴: `I'm [FEELING] when I [ACTION].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 5 | I'm thirsty when I run. | 달리면 목이 말라요. | 3.67 ⚠️저점 | 상태 변화라 'I get thirsty when I run'이 관용 — be→get 교체로 수정 가능. | 수정: I'm tired when I work late. / KR: 늦게까지 일하면 피곤해요. |

## M03_023 (quote, c1_rewritten) — 씨앗: You're my home.
- 패턴: `You're my [NOUN].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | You're my family. | 당신은 저의 가족이에요. | 4.33 | 'You're my family'는 감정 표현으로 자연 — 결함 없음. | 합격 |
| 5 | You're my brother. | 당신은 저의 형제예요. | 4.0 | 비유로는 자연하나 사실 서술이면 굳이 말할 상황이 없음 — 값 교체로 수정 가능. | 합격 |
| 6 | You're my teacher. | 당신은 저의 선생님이에요. | 3.67 ⚠️저점 | 'You're my teacher'는 뻔한 사실 진술이라 발화 동기가 약함 — 수정 가능. | 수정: You're my hero. / KR: 당신은 저의 영웅이에요. [어휘승인요청: hero] |

## M03_025 (real, curriculum) — 씨앗: It's next to the bank.
- 패턴: `It's next to the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | It's next to the school. | 학교 옆에 있어요. | 4.67 | 위치 안내 고빈도 문장 — 결함 없음. | 합격 |

## M03_027 (real, curriculum) — 씨앗: The restaurant is between the bank and the school.
- 패턴: `The [PLACE] is between the [PLACE-A] and the [PLACE-B].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | The hotel is between the station and the park. | 호텔은 역과 공원 사이에 있어요. | 4.33 | 자연 — 9단어로 A1 길이 상한 경계, 고정부가 긴 탓이라 구조적. | 합격 |
| 3 | The coffee shop is between the bank and the post office. | 커피숍은 은행과 우체국 사이에 있어요. | 4.0 | 영어는 자연하나 11단어로 A1 길이 초과 — 장소 값 축약으로 수정 가능. | 수정: The store is between the bank and the park. / KR: 가게는 은행과 공원 사이에 있어요. |

## M03_028 (real, curriculum) — 씨앗: I'll come back tomorrow.
- 패턴: `I'll come back [TIME].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 6 | I'll come back later today. | 이따가 다시 올게요. | 4.33 | 'later today' 자연 — 결함 없음. | 합격 |

## M03_029 (real, curriculum) — 씨앗: When will you go back home?
- 패턴: `When will you [ACTION]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | When will you visit us? | 언제 우리를 보러 올 거예요? | 4.67 | 'visit us' 조합 자연 — 결함 없음. | 합격 |
| 3 | When will you eat dinner? | 언제 저녁 먹을 거예요? | 3.67 ⚠️저점 | 가까운 개인 일정엔 will보다 be going to가 관용 — 시제 교체로 수정 가능. | 수정: When will you call me? / KR: 언제 전화할 거예요? |

## M03_031 (real, curriculum) — 씨앗: Please get out of the car.
- 패턴: `Please get out of the [PLACE].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Please get out of the house. | 집에서 나가 주세요. | 3.67 ⚠️저점 | 'get out of the house'는 쫓아내는 뉘앙스라 please와 충돌 — 'leave'로 수정 가능. | 수정: Please get out of the water. / KR: 물에서 나오세요. [어휘승인요청: water] |
| 5 | Please get out of the room. | 방에서 나가 주세요. | 3.67 ⚠️저점 | 방에서 나가라는 직접 명령은 무례하게 들림 — 완곡 표현으로 수정 가능. | 불합격 — 방에서 나가라는 직접 명령은 무례해 이 슬롯 값으로 부적합 |

## M03_034 (quote, c1_rewritten) — 씨앗: Something good is coming.
- 패턴: `Something [ADJ] is coming.`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 1 | Something new is coming. | 새로운 것이 오고 있어요. | 3.67 ⚠️저점 | 'Something new is coming'은 광고 티저 문구에 가까워 대화 상황이 약함 — 수정 가능. | 합격 |
| 3 | Something fun is coming. | 재미있는 일이 다가오고 있어요. | 3.67 ⚠️저점 | 'Something fun is coming up'이 관용 — up 추가로 수정 가능. | 불합격 — 'fun'은 'coming up'과만 결합해 이 고정부에서 성립하지 않음 |
| 5 | Something cold is coming. | 추위가 다가오고 있어요. | 3.0 ⚠️저점 | 'Something cold is coming'은 원어민이 쓰지 않는 조합(a cold front) — 구조적. | 불합격 — 'Something cold is coming'은 비관용(a cold front) |
| 6 | Something amazing is coming. | 놀라운 일이 다가오고 있어요. | 3.67 ⚠️저점 | 'amazing'은 광고 카피체로 기울어 발화 상황이 흐림 — 수정 가능. | 수정: Something big is coming. / KR: 큰 일이 다가오고 있어요. |

## M03_035 (real, curriculum) — 씨앗: Excuse me, can you help me?
- 패턴: `Excuse me, can you [REQUEST]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | Excuse me, can you show me the way? | 실례합니다, 길 좀 알려 주시겠어요? | 3.67 ⚠️저점 | 'show me the way'는 노래·문어 느낌, 길 안내는 'give me directions'가 관용 — 수정 가능. | 수정: Excuse me, can you tell me the time? / KR: 실례합니다, 몇 시인지 알려 주시겠어요? [어휘승인요청: tell] |

## M03_036 (real, curriculum) — 씨앗: I'm lost. Where am I?
- 패턴: `I'm lost. [QUESTION]?`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | I'm lost. Where is the hotel? | 길을 잃었어요. 호텔이 어디예요? | 4.67 | 길 잃음 상황에서 그대로 쓰는 문장 — 결함 없음. | 합격 |
| 6 | I'm lost. How far is the airport? | 길을 잃었어요. 공항까지 얼마나 멀어요? | 4.33 | 자연하고 두 문장 연결도 매끄러움 — 결함 없음. | 합격 |

## M03_041 (movie, c1_rewritten) — 씨앗: I'll visit you again on Friday.
- 패턴: `I'll [ACTION] you again on [DAY].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 3 | I'll meet you again on Sunday. | 일요일에 다시 만날게요. | 3.67 ⚠️저점 | 이미 아는 사이엔 meet again이 어색(see가 관용) — 동사 교체로 수정 가능. | 수정: I'll see you again on Sunday. / KR: 일요일에 다시 만나요. |
| 4 | I'll help you again on Wednesday. | 수요일에 다시 도와줄게요. | 3.67 ⚠️저점 | 도움을 요일로 예약하는 상황이 잘 안 그려짐 — 수정 가능. | 수정: I'll call you again on Wednesday. / KR: 수요일에 다시 전화할게요. |
| 5 | I'll teach you again on Thursday. | 목요일에 다시 가르쳐 줄게요. | 3.67 ⚠️저점 | teach again은 수업 문맥이 전제돼야 성립 — 수정 가능. | 불합격 — 'teach you again'은 수업 문맥이 전제돼야 성립해 단독 작별 발화로 부적합 |
| 6 | I'll ask you again on Tuesday. | 화요일에 다시 물어볼게요. | 3.0 ⚠️저점 | 'I'll ask you again on Tuesday'는 압박하는 뉘앙스라 학습 문장으로 부적합 — 구조적. | 불합격 — 'ask you again'이 압박 뉘앙스라 작별 약속 기능과 충돌 |

## M03_044 (tale, curriculum) — 씨앗: They found their way back home.
- 패턴: `They found their way back [DESTINATION].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 4 | They found their way back to the beach. | 그들은 해변으로 돌아가는 길을 찾았어요. | 4.0 | 자연 — 고정부가 길어 A1 상한 경계(구조적). | 합격 |

## M03_045 (movie, c1_rewritten) — 씨앗: Nothing can stop us today!
- 패턴: `Nothing can stop [PERSON] [TIME]!`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 2 | Nothing can stop you tomorrow! | 내일 아무것도 당신을 막을 수 없어요! | 3.0 ⚠️저점 | 관용구가 요구하는 now/today와 tomorrow가 충돌 — 시간 슬롯 자체가 구조적 문제. | 씨앗결함 — [TIME] 슬롯이 관용구의 즉시성 때문에 today/now만 허용해 치환이 사실상 불가능 / 대안 씨앗: Nothing can stop us today! |
| 4 | Nothing can stop her this week! | 이번 주에는 아무것도 그녀를 막을 수 없어요! | 3.0 ⚠️저점 | 'this week'는 관용구의 즉시성과 충돌 — 구조적. | 씨앗결함 — [TIME] 슬롯이 관용구의 즉시성 때문에 today/now만 허용해 치환이 사실상 불가능 / 대안 씨앗: Nothing can stop us today! |

## M03_047 (real, curriculum) — 씨앗: See you later! Have a great day.
- 패턴: `See you [TIME]! Have a great [OCCASION].`

| cand | 변형 | 번역 | judge | 코멘트 | 검수 |
|---|---|---|---|---|---|
| 5 | See you at lunch! Have a great morning. | 점심때 봐요! 좋은 아침 보내세요. | 3.67 ⚠️저점 | 'Have a great morning'은 원어민이 잘 쓰지 않음 — day로 교체하면 수정 가능. | 수정: See you at lunch! Have a great day. / KR: 점심때 봐요! 좋은 하루 보내세요. |
