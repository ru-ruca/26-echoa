# Echoa 콘텐츠 확장(C-2 패턴 문장 · C-3 대화) 조사

- **조사일**: 2026-07-28
- **목적**: 기존 커리큘럼 문장 3,622개를 씨앗으로 AI 콘텐츠 확장. 두 방향 "어떻게 만들지" 설계.
  - **C-2 패턴 기반 문장 확장**: 씨앗 문장의 문법·표현 패턴을 유지하며 변형·맥락 문장 생성.
  - **C-3 대화 패턴 확장**: 단일 문장 → A-B 대화(답글·이어지는 턴)로 확장. 말하기 학습용.
- **출처 원칙**: 2024~2026 1차 자료(arxiv·ACL·공식 문서·법률 1차) 우선. 확인 못 한 건 "미확인" 명시.
- **검증 수준 표기**: [확인=본문 직접 fetch] / [스니펫=검색 요약만] / [미확인].

---

## 핵심 결론 먼저 (TL;DR)

1. **프롬프트만으로 CEFR 난이도를 못 잡는다.** 여러 1차 연구가 공통으로 지적. 실무 해법은 **"overgenerate + 자동 채점 재랭킹(rerank)"** — N개 뽑고 난이도 스코어러로 걸러 최선만 채택. C-2·C-3 둘 다의 중심 장치.
2. **C-2는 paraphrase가 아니라 substitution drill이다.** paraphrase=같은 뜻·다른 표현. C-2=같은 구조·**새 내용**(슬롯 치환). 씨앗에서 패턴(템플릿) 뽑고 슬롯을 CEFR 어휘로 채우는 방식이 맞다.
3. **C-3는 6턴 안팎·짧은 왕복이 학습에 적합.** 턴이 길어질수록 난이도가 목표에서 벗어나는 "alignment drift"가 실측됨. 짧게 끊고 역할·상황 고정.
4. **어휘 통제는 wordlist로 강제한다.** EVP/CEFR-J 등 레벨별 wordlist를 프롬프트에 넣고, 생성 후 wordlist 초과 토큰 비율(Token Miss Rate류)로 자동 필터.
5. **검수는 2단계.** 자동(문법·중복·환각·CEFR·wordlist) → LLM-as-judge(rubric+CoT+few-shot) → 인간 샘플 검수. Duolingo도 최종 인간 게이트 유지.
6. **저작권**: AI 순수 생성물은 미국 저작권 보호 대상 아님(= 남이 베껴도 못 막지만, 우리도 원문 베끼면 위험). 씨앗을 재작성할 때 **구조·표현이 원문과 실질적으로 유사하면 침해** — 단어만 바꾸는 건 안전판이 안 됨. C-2/C-3는 "뜻 보존 재작성"이 아니라 "패턴만 빌린 새 내용"이라 상대적으로 안전.

---

## Q1. LLM 언어학습 콘텐츠 생성 베스트 프랙티스 (2024~2026)

### 1-1. CEFR 난이도 제어 — 프롬프트만으로는 부족 [확인]

**From Tarzan to Tolkien (ACL Findings 2024)** — 난이도 제어의 가장 구체적 1차 근거.
- few-shot GPT-4: 가장 자세한 프롬프트로 control error **0.28±0.03**, 단 프롬프트 **2,206 토큰**(비쌈).
- finetuning: prompt 대비 ControlError **약 50% 감소**. RL(PPO): 추가 50% 감소.
- 결과 모델 **CaLM**(LLaMa2-7B finetune+PPO)이 GPT-4를 이김. CaLM+top-3 sampling control error **0.15±0.01** (GPT-4 baseline 0.57).
- 품질 점수는 방법 무관 **~9.5/10 유지** → 난이도 통제해도 품질 안 깎임.
- 함의: **자세한 few-shot로 어느 정도 되지만 토큰값 비싸고 완벽하지 않다.** 소규모 팀은 finetune 대신 "overgenerate + 자동 CEFR 스코어러 재랭킹"으로 근접 가능.
- URL: https://aclanthology.org/2024.findings-acl.926/ · https://arxiv.org/abs/2406.03030 · https://arxiv.org/html/2406.03030v1

**Alignment Drift in CEFR-prompted LLMs (ACL 2025 BEA workshop)** [스니펫]
- CEFR 프롬프트를 줘도 대화가 진행될수록 목표 레벨에서 **점점 벗어나는 "alignment drift"** 발생. → 긴 콘텐츠·긴 대화일수록 통제 어려움. 짧게 끊어야 한다는 근거.
- URL: https://aclanthology.org/2025.bea-1.6.pdf · https://arxiv.org/abs/2505.08351

**기타 CEFR 제어 연구** [스니펫]
- ReadCtrl(2024): readability-controlled instruction learning으로 개인화 생성.
- 다차원 프레임워크: controlled prompting + 자동 readability 예측 + CEFR 어휘 제약 + 구문 복잡도 분석을 결합해야 단일 지표 프롬프트보다 낫다.
- Ace-CEFR(2025): 대화체 텍스트의 언어 난이도 자동 평가용 데이터셋 — LLM 앱의 난이도 평가에 쓰는 벤치마크. URL: https://arxiv.org/abs/2506.14046
- reinforcement-tuned LLM으로 CEFR별 ESL 자료 자동 생성(Springer, 2025). URL: https://link.springer.com/article/10.1007/s44163-025-00762-3

> **미확인**: "숫자 레벨(0~4)이 CEFR 이름 명시보다 효과적"이라는 통설이 검색 요약에 등장하나, Tarzan 본문 확인 결과 **그 논문은 숫자-only vs 레벨명을 비교하지 않음**. 1차 출처를 특정하지 못함 → **미확인**으로 둠. 실무에선 "레벨명 + can-do 서술 + few-shot 예시"를 함께 주는 게 안전.

### 1-2. 어휘(미지 단어) 통제 — wordlist 강제가 정석 [확인/스니펫]

- **English Vocabulary Profile(EVP)**: Cambridge Learner Corpus 기반, 단어·구·관용구·콜로케이션의 CEFR 레벨을 제공하는 공개 레퍼런스. 슬롯 어휘 통제의 1차 소스. URL(연구): https://arxiv.org/abs/2506.02758
- **CEFR-J wordlist**(영어 대상, 오픈): 레벨별 영어 단어 목록. 프롬프트 제약 + 사후 필터에 바로 쓸 수 있음. URL: https://github.com/openlanguageprofiles/olp-en-cefrj
- 방법(연구 공통): ① 타깃 CEFR band에 맞는 **어휘 리스트를 프롬프트에 주입**(constrained prompting), ② 생성 후 **band 초과 단어 비율**을 재서 필터. (SRS-Stories 등 vocabulary-constrained 생성) URL: https://arxiv.org/abs/2512.18362 [스니펫]
- Echoa 함의: Echoa엔 이미 단어 3,910개 + 콜로케이션 5,705개 자산이 있음 → **자체 CEFR wordlist(허용 어휘)**를 만들어 프롬프트 제약 + 사후 필터로 재사용. "신규 어휘 폭증"을 막는 가장 확실한 레버.

### 1-3. 자연스러움 확보

- paraphrase 연구 공통: LLM에 **어휘·구문을 바꾸되 의미 보존**을 지시하면 다양성은 올라가나, "**natural and plausible**"(자연스럽고 그럴듯) 요건을 별도로 강제해야 함. (ParaFusion) URL: https://arxiv.org/html/2404.12010
- 자연스러움은 **생성 지시**보다 **사후 검수(LLM-judge naturalness 축)**로 잡는 게 현실적(Q4 참고).

---

## Q2. C-2 패턴 확장 방법론

### 2-1. 교육학 개념 — substitution drill / pattern practice [스니펫]

- **Substitution drill**(British Council 정의): 교사가 문장을 모델로 제시 → 학습자 반복 → 핵심 단어를 **치환**해 새 구조를 말하게 함. 예) "She is reading a **book**." → book을 newspaper/magazine으로 치환.
- 이론적 뿌리: **Audiolingual Method**의 pattern practice. 자동화(automaticity)·유창성 형성엔 효과적, 단 **기계적·창의성 제약**이 비판점.
- URL: https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/q-s/substitution-drill

> **핵심 구분**: C-2는 **paraphrase(같은 뜻·다른 표현)가 아니라 substitution drill(같은 구조·새 내용)**. 씨앗 "I'd like to book a table for two."의 패턴 `I'd like to [V] [obj] for [n].`을 뽑아 → "I'd like to reserve a room for three." 처럼 **슬롯을 갈아끼운다.** paraphrase로 접근하면 뜻이 같은 사족만 늘고, 저작권 유사도도 오히려 높아짐.

### 2-2. AI 적용 기법 — 템플릿 추출 → 슬롯 채우기 → 재랭킹

1. **패턴(템플릿) 추출**: 씨앗 문장에서 고정부(문법 골격·타깃 표현)와 가변 슬롯을 분리. LLM에 "이 문장의 문법 패턴을 유지하고 명사구/동사구 슬롯을 표시하라"고 지시.
2. **슬롯 채우기(constrained)**: 슬롯을 **허용 CEFR wordlist·주제 카테고리** 안에서만 채우게 함. 씨앗의 문법·타깃 표현은 건드리지 않음.
3. **다양성 강제(diversity forcing)**: 한 씨앗에서 여러 변형을 뽑을 때 **주제·주어·목적어를 서로 다르게** 지정. (한 주제를 12가지로 다르게 프롬프트하면 250억 토큰 코퍼스에서 중복 <1%라는 실측 있음 — 아래 과생성 함정 참고)
4. **재랭킹**: 생성 후 CEFR 스코어러 + 자연스러움 judge로 걸러 상위만 채택.

- 근거: ParaFusion(LLM로 어휘·구문 다양성을 키우되 의미 근접 유지) URL: https://arxiv.org/html/2404.12010 · Controlled Language Generation for Language Learning Items(2022, 학습 문항 통제 생성) URL: https://arxiv.org/abs/2211.15731 [PDF만, 본문 미확인]

### 2-3. 과생성의 함정 — 부자연·반복·model collapse [스니펫]

- **Model/mode collapse**: 생성물을 다시 학습·재생성에 넣으면 **다양성이 무너지고 반복·저빈도 표현 소실**. AI 생성물끼리만 순환시키면 tail이 사라짐.
- 완화책(2024 실측): ① **원본(사람) 데이터 5% 이상 섞기**, ② **diversity forcing**(같은 주제도 프롬프트를 다르게), ③ **dedup + 강한 품질 필터**, ④ 단일 모델 반복 출력 회피.
- URL: https://arxiv.org/abs/2404.05090 · https://aicompetence.org/avoiding-model-collapse-in-synthetic-data-training/
- Echoa 함의: C-2 변형을 **다시 씨앗으로 재확장하지 말 것**(1세대만). 씨앗은 항상 사람이 만든 원 커리큘럼 3,622개. 배치마다 near-duplicate 제거 필수.

---

## Q3. C-3 대화 생성 방법론

### 3-1. 단일 문장/상황 → A-B 대화 생성 기법 [확인/스니펫]

- **role-play 프롬프트**: LLM에 A·B 역할을 부여하고 **턴을 번갈아** 생성(autoregressive dyadic exchange). 사용자 프로필·상황을 프롬프트에 concat. (Synthetic Dialogue Generation) URL: https://www.emergentmind.com/topics/synthetic-dialogue-generation [스니펫]
- **CoT / taxonomy-driven 프롬프트**: 추론 흐름·주제 전개·언어 다양성을 강제. 무작정 뽑기보다 "상황→목표→턴 계획→대사"로 구조화.
- **turn-based(실시간 아님) 설계**: 끼어들기 없는 **왕복형**이 학습자에게 안전한 발화 공간을 준다. (LLM Agents for Education) URL: https://arxiv.org/abs/2503.11733 [스니펫]

### 3-2. 난이도·자연스러움 통제 — Beginner-Friendly LLMs 연구가 핵심 [확인]

**Toward Beginner-Friendly LLMs: Controlling Difficulty in Conversation (2025)** — C-3 난이도 설계의 가장 구체적 1차 근거.
- 네 방법 비교: ① prompting(단독 부족), ② detailed prompting(예시+wordlist), ③ **overgenerate(후보 병렬 생성 후 Token Miss Rate 최저 선택)**, ④ FUDGE(디코딩 시 난이도 편향 — 최고 성능이나 구현 복잡).
- 성능: FUDGE 토큰 이해율 **~88%** vs 기본 prompting 40.4%.
- **Token Miss Rate(TMR)**: 발화 중 사용자 레벨 초과 토큰 비율. lemmatization 후 레벨별 wordlist(JLPT 등)와 대조.
- 시스템 프롬프트 문구: "**keep the conversation going back and forth**"(자연스러운 왕복) + "**use these words and other words of similar or lower difficulty**"(허용 어휘 + 그 이하만).
- **alignment drift**: 통제 안 하면 턴이 진행될수록 목표 난이도에서 벗어남 → **턴 수를 짧게** 유지해야.
- 평가: 방법당 **6턴 대화 4개**로 사람 평가. FUDGE가 이해도 7.67/10·인지부하 최저 4.67/10·자연스러움 7.33/10. TMR과 이해도 상관 ρ=0.78.
- URL: https://arxiv.org/abs/2506.04072 · https://arxiv.org/html/2506.04072v1

> 실무 결론: 소규모 팀은 FUDGE(디코딩 개입) 대신 **overgenerate + TMR/CEFR 재랭킹**이 현실적. 두 논문(Tarzan·Beginner-Friendly)이 독립적으로 이 패턴을 지지.

### 3-3. 대화 길이·턴·역할 설계

- **턴 수**: 학습·평가용 연구는 **6턴 안팎**을 씀(Beginner-Friendly 6턴). 자연 대화 코퍼스 평균은 9~14턴이나, **말하기 연습·쉐도잉용은 짧게(2~6턴)**가 drift·인지부하 면에서 유리. [확인+스니펫]
- **역할**: A(상대)-B(학습자) 고정, 상황·목표 명시. turn-based 왕복.
- **쉐도잉·롤플레이 적합성**: 쉐도잉 앱들은 짧은 대화·자막·문장 replay·녹음을 결합(Shadow Flow, Speaking English By Shadowing). Echoa는 이미 dialogues 539줄 + 쉐도잉·순차재생 자산이 있어 C-3 산출물을 그대로 태울 수 있음.
- 참고 URL: https://arxiv.org/abs/2503.11733 · https://shadowflow.net/

### 3-4. Echoa 접목 포인트

- 씨앗 1문장 → 그 문장을 **B(학습자)의 한 턴**으로 두고 앞뒤에 A의 유도 발화 1~2개를 붙이는 방식이 자연스럽다("단일 문장을 대화의 축으로").
- 산출 형식은 기존 `{text, speaker?, focus?}[]`(shadowing-practice.tsx)와 dialogues 스키마에 맞춰 생성 → 적재 스크립트(34-sync-dialogues) 재사용.

---

## Q4. 품질 검증·검수 게이트

### 4-1. LLM-as-judge — rubric + CoT + few-shot [스니펫]

- 개방형 텍스트(문법·자연스러움·유용성) 평가에서 사실상 표준. 사람 평가 대체·보조.
- 효과 높이는 법: **CoT + few-shot 예시**, **평가 축을 rubric으로 분해**(예: style transfer → 강도·의미보존·자연스러움 3축), 각 점수의 의미를 예시로 고정.
- 한계: **같은 입력에 점수가 흔들림(불안정)** → 온도 낮추고 다중 판정·기준 고정 필요.
- URL(서베이): https://github.com/CSHaitao/Awesome-LLMs-as-Judges · https://aclanthology.org/2025.emnlp-main.796.pdf · https://aclanthology.org/2025.emnlp-main.138.pdf

### 4-2. 자동 필터 + 인간 검수(HITL) [스니펫]

- 파이프라인 정석: **자동 필터(중복·품질·환각) → HITL(사람이 초안 검토·수정)**. 사람이 "그럴듯하게 틀린" 케이스를 제일 잘 잡음.
- 중복·붕괴 방지: dedup, 다양성 강제, 실데이터 혼합(Q2 참고).
- URL: https://www.comet.com/site/blog/human-in-the-loop/ · https://rlhfbook.com/c/12-synthetic-data

### 4-3. Echoa 검수 게이트 설계(권고)

1. **자동 하드 필터**(탈락=버림): 문법 오류(파서/LLM), wordlist 초과율(TMR류) 임계 초과, near-duplicate(임베딩 유사도), 씨앗과 과유사(저작권), 길이·턴 규격 위반.
2. **LLM-as-judge 소프트 스코어**(rubric 1~5): 자연스러움 / CEFR 적합 / 패턴 유지(C-2) or 대화 응집·턴 자연성(C-3) / 교육 적절성. 임계 미만 재생성.
3. **인간 샘플 검수 게이트**: 배치의 5~10% 무작위 + judge 저점 전수. 한 명이라도 통과 못 하면 배치 반려. (Duolingo도 최종 인간 게이트 유지 — Q5)

---

## Q5. 유사 앱·서비스 사례 (2024~2026)

### 5-1. Duolingo — "Mad Lib" 템플릿 + 인간 게이트 [스니펫, 2곳 교차확인]

- **AI-first** 전략(2023 Duolingo Max, OpenAI 제휴). 콘텐츠 생성에 LLM 대거 도입.
- **2단계 인간 주도 파이프라인**:
  - Curriculum Design(전적으로 사람): Learning Designer가 테마·문법 초점·어휘 타깃·문항 유형 설계.
  - Prompt Preparation: **"Mad Lib" 스타일 프롬프트 템플릿** — 언어·CEFR·테마는 엔지니어링이 자동 주입, 문항 유형 등은 사람이 지정.
- **문항 유형별 프롬프트 템플릿 30+개**를 CMS에 통합. "고정 규칙 + 가변 파라미터" 조합.
- **품질 게이트**: Learning Designer가 **모든 생성물을 사용자 노출 전 검토**(문법·부자연·교육 부적합 잡음).
- 규모: 첫 100개 코스 12년 → 생성 AI·"shared content"로 **1년 안에 148개 신규 코스**. 콘텐츠 제작 속도 +40%(스니펫별 수치 차이 있음).
- URL: https://www.zenml.io/llmops-database/ai-powered-lesson-generation-system-for-language-learning · https://www.zenml.io/llmops-database/scaling-ai-powered-language-learning-through-personalization-assessment-and-content-generation · https://technologymagazine.com/ai-and-machine-learning/duolingos-ai-first-strategy-explained · https://investors.duolingo.com/news-releases/news-release-details/duolingo-launches-148-new-language-courses

> Echoa 직접 시사: **"사람이 설계 → 템플릿으로 대량 생성 → 사람이 최종 검수"** 3단계가 업계 검증된 골격. C-2/C-3도 이 골격을 그대로 따르면 됨.

### 5-2. Speak — 학습 루프, AI 대화 [스니펫]

- Speak Method 3단계: **Learn(원어민이 실제 쓰는 표현) → Practice(자동화될 때까지 반복) → Apply(AI 튜터와 실제 왕복 대화)**. 발음·표현 실시간 피드백, 레벨 매칭.
- 규모: 다운로드 1,500만+, 2024 말 valuation $1B, Wirecutter 2026 베스트 선정.
- URL: https://www.speak.com/ · https://apps.apple.com/us/app/speak-ai-language-learning/id6473027266
- 시사: "표현 학습 → 반복 → 대화 적용" 루프가 Echoa의 문장→쉐도잉→대화(C-3) 흐름과 정확히 겹침.

### 5-3. 말해보카 (국내) [스니펫]

- AI가 사용자 발화 실시간 피드백, 몰랐던 표현 자동으로 어휘에 추가. 20문제로 레벨 진단 후 맞춤 퀴즈.
- **예문 46,000개**를 카테고리(시험/비즈니스/일상)별 학습. 교과서~영화/미드/토크쇼 표현. 망각곡선 복습.
- AI가 문장 속 단어를 분석하는 영어사전 제공.
- URL: https://apps.apple.com/kr/app/id1460766549 · https://www.busan.com/view/busan/view.php?code=2022111412270281157
- 시사: 대량 예문 + 카테고리 + 복습 구조가 Echoa 자산과 유사. 규모감(수만 예문) 참고치.

> **미확인**: Duolingo·Speak·말해보카의 **정확한 생성 규모/모델/필터 수치**는 공식 상세 미공개. 위 수치는 보도·케이스스터디 스니펫 수준(1차 상세 스펙 아님).

---

## Q6. 저작권 / 유사도 (2026)

### 6-1. AI 생성물의 저작권 상태 [스니펫, 1차 근거]

- **순수 AI 생성물은 미국 저작권 보호 대상 아님**(인간 저작자 요건). 프롬프트를 아무리 정교하게 짜도 그것만으로는 저작자 안 됨. (US Copyright Office 2025-01-29 보고서)
- **Thaler v. Perlmutter**: D.C. Circuit이 2025-03 "저작권법은 인간 저작자 요구" 확인, 대법원 2026 상고 불수리.
- **AI-assisted**는 인간의 창작적 기여·표현 통제가 충분하면 보호 가능.
- URL: https://www.copyright.gov/ai/ · https://www.skadden.com/insights/publications/2025/02/copyright-office-publishes-report
- Echoa 함의: C-2/C-3 산출물은 **우리도 독점 저작권 주장 어려움**(남이 베껴도 막기 어려움). 무료+광고 모델엔 실질 문제 작음. 진짜 리스크는 아래 6-2.

### 6-2. 원문 재작성 시 유사도 리스크 [스니펫, 1차 근거]

- **단어만 동의어로 바꿔도 침해 면책 안 됨.** 핵심은 **substantial similarity(실질적 유사성)** — 원문의 "핵심(heart)" 표현·구조·흐름을 가져오면 paraphrase여도 침해(Harper & Row v. Nation).
- 정해진 "몇 % 바꾸면 안전" 임계 없음. "구조·flow·고유 표현을 너무 닮으면" 2차적저작물로 볼 수 있음.
- URL: https://www.gfrlaw.com/what-we-do/insights/copyright-infringement-similarity-expression-must-be-substantial · https://meta.wikimedia.org/wiki/Wikilegal/Close_Paraphrasing
- Echoa 함의(중요): **Echoa 씨앗 3,622개가 "외부 저작물에서 가져온 것"이면** C-2의 "패턴 유지 재작성"이 원저작물과 유사성을 남길 수 있음. 반대로 **패턴(문법 골격)만 빌리고 내용(어휘·상황)을 완전히 새로 채우면** 보호받는 건 아이디어/문법이라 안전. → **C-2는 paraphrase가 아니라 slot 치환으로 가야 저작권도 안전**(2-1 구분과 일치).

### 6-3. 실무 안전판 (권고)

- 씨앗 대비 **표층 유사도 자동 체크**(n-gram overlap·임베딩 유사도) → 임계 초과 산출물 폐기·재생성.
- 문법 패턴만 재사용, **어휘·주제·고유표현은 새로 채움**.
- 씨앗 출처가 상용 교재/코퍼스면 해당 산출물은 특히 유사도 게이트 강하게.

---

## Q7. C-2 설계 권고 (패턴 기반 문장 확장)

### 생성 방법
1. **씨앗 선정**: 원 커리큘럼 3,622개 중 M01~03 배치 문장(사람 제작 = 저작권/품질 기준선).
2. **패턴 추출**: LLM으로 각 씨앗의 `고정부(문법 골격 + 타깃 표현) + 가변 슬롯` 분해. 예) "Could you pass me the salt?" → `Could you [V] me the [n]?`
3. **슬롯 치환(constrained)**: 슬롯을 **Echoa 허용 CEFR wordlist + 주제 카테고리** 안에서 채움. 씨앗당 5~8 변형, 주어/목적어/상황을 서로 다르게(diversity forcing).
4. **재랭킹**: 후보를 자동 CEFR 스코어러 + naturalness judge로 상위 3~5만 채택.
5. **1세대 제한**: 변형을 다시 씨앗 삼아 재확장 금지(model collapse 방지).

### 프롬프트 전략
- 역할·목표 고정 + **레벨명 + can-do 서술 + few-shot 예시**(같은 패턴의 좋은 변형 2~3개) 제시.
- 허용 어휘 리스트 주입("아래 단어와 그 이하 난이도만 사용").
- "**패턴은 유지, 내용은 새로**"를 명시(= paraphrase 금지, substitution만).
- 구조화 출력(JSON): {pattern, slotFills, sentence, cefr, topic} — 사후 필터가 파싱하기 쉽게.

### 검수 기준 (게이트)
- 하드 필터(탈락): 문법 오류 / wordlist 초과율 임계 초과 / 씨앗과 n-gram·임베딩 유사도 초과(저작권) / 배치 내 near-duplicate / 패턴 이탈(고정부 훼손).
- 소프트 judge(1~5, 임계 미만 재생성): 자연스러움 · CEFR 적합 · 패턴 유지 · 교육 적절성.
- 인간 게이트: 배치 5~10% 무작위 + judge 저점 전수 검토.

### 파일럿 (M01~03)
- 규모: 씨앗 문장 × 변형 5~8 → 배치 산출. M01~03 3개월분만 먼저.
- 성공 기준(제안): 하드 필터 통과율, judge 평균 ≥ 4/5, 인간 검수 합격률 ≥ 90%, near-dup < 2%, 씨앗 유사도 초과 0건.
- 산출물은 기존 sentences 스키마(id `M{MM}_D{NN}_L{NN}`)에 맞춰 적재, 기존 학습 플로우(Sentence→Words→Practice)에서 검증.

---

## Q8. C-3 설계 권고 (대화 패턴 확장)

### 생성 방법
1. **씨앗 = 대화 축**: 씨앗 문장을 **B(학습자) 발화**로 두고, 앞에 A의 유도 발화 1개 + 뒤에 자연스러운 이어짐 1~2턴 부착.
2. **상황·역할 고정**: {상황, A역할, B역할, 목표}를 먼저 정하고 대사 생성(taxonomy/CoT).
3. **짧게**: 총 **2~6턴**(초급 4턴 안팎). alignment drift·인지부하 방지.
4. **overgenerate + 재랭킹**: 대화 후보 N개 → TMR/CEFR + 대화 응집·턴 자연성 judge로 최선 선택.

### 프롬프트 전략
- 시스템 지시: "keep the conversation going back and forth"(자연 왕복) + "허용 어휘 + 그 이하 난이도만".
- 역할·상황·턴 수 명시, few-shot으로 좋은 짧은 대화 1~2개 제시.
- 씨앗 문장을 **그대로 한 턴에 포함**(또는 최소 변형)해 학습 연결성 유지.
- 구조화 출력: `[{speaker, text, focus?}]` (기존 shadowing-practice·dialogues 스키마와 일치).

### 검수 기준 (게이트)
- 하드 필터: 턴 수·길이 규격 / 문법 / wordlist 초과율 / 화자 일관성(A·B 안 섞임) / near-duplicate / 씨앗 유사도(저작권).
- 소프트 judge(1~5): 대화 응집성 · 턴 자연성(주고받기) · CEFR 적합 · 쉐도잉/롤플레이 적합(발화 길이·리듬).
- 인간 게이트: 소리 내 읽어 어색한지 포함 5~10% 검수.

### 파일럿 (M01~03)
- 규모: M01~03 씨앗 중 대화 확장 적합 문장 선별 → 씨앗당 대화 1~2개(4턴 기준).
- 성공 기준(제안): drift 없음(마지막 턴도 CEFR 유지), judge 평균 ≥ 4/5, 인간 합격 ≥ 90%, TMR 임계 이하.
- 산출물은 `day_type='conversation'` sentences로 적재(id 문자열정렬 "일반→대화→복습"), `lib/dialogue.ts` window + speech-sequence 순차재생으로 바로 검증.

---

## 부록: 출처 전체 목록

**Q1 CEFR·난이도 제어**
- From Tarzan to Tolkien (ACL Findings 2024) [확인]: https://aclanthology.org/2024.findings-acl.926/ · https://arxiv.org/abs/2406.03030
- Alignment Drift in CEFR-prompted LLMs (BEA 2025) [스니펫]: https://aclanthology.org/2025.bea-1.6.pdf · https://arxiv.org/abs/2505.08351
- Ace-CEFR dataset (2025) [스니펫]: https://arxiv.org/abs/2506.14046
- CEFR-aligned ESL 자료 RL 생성 (Springer 2025) [스니펫]: https://link.springer.com/article/10.1007/s44163-025-00762-3

**Q1-2 어휘 통제**
- Exploiting EVP for L2 vocab assessment with LLMs (2025) [스니펫]: https://arxiv.org/abs/2506.02758
- CEFR-J wordlist (Open Language Profiles): https://github.com/openlanguageprofiles/olp-en-cefrj
- SRS-Stories vocabulary-constrained generation [스니펫]: https://arxiv.org/abs/2512.18362

**Q2 패턴 확장**
- Substitution drill (British Council): https://www.teachingenglish.org.uk/professional-development/teachers/knowing-subject/q-s/substitution-drill
- ParaFusion (2024) [스니펫]: https://arxiv.org/html/2404.12010
- Controlled Language Generation for Language Learning Items (2022) [PDF만]: https://arxiv.org/abs/2211.15731
- Model collapse (2024) [스니펫]: https://arxiv.org/abs/2404.05090 · https://aicompetence.org/avoiding-model-collapse-in-synthetic-data-training/

**Q3 대화 생성**
- Toward Beginner-Friendly LLMs: Controlling Difficulty in Conversation (2025) [확인]: https://arxiv.org/abs/2506.04072
- LLM Agents for Education (2025) [스니펫]: https://arxiv.org/abs/2503.11733
- Synthetic Dialogue Generation Techniques [스니펫]: https://www.emergentmind.com/topics/synthetic-dialogue-generation
- Shadow Flow (쉐도잉 앱): https://shadowflow.net/

**Q4 품질·검수**
- Awesome-LLMs-as-Judges (서베이): https://github.com/CSHaitao/Awesome-LLMs-as-Judges
- Reliable LLM-as-a-Judge framework (EMNLP 2025) [스니펫]: https://aclanthology.org/2025.emnlp-main.796.pdf
- Human-in-the-Loop workflows (Comet): https://www.comet.com/site/blog/human-in-the-loop/
- Synthetic Data & Distillation (RLHF Book): https://rlhfbook.com/c/12-synthetic-data

**Q5 유사 앱**
- Duolingo LLMOps case (ZenML) [스니펫]: https://www.zenml.io/llmops-database/ai-powered-lesson-generation-system-for-language-learning · https://www.zenml.io/llmops-database/scaling-ai-powered-language-learning-through-personalization-assessment-and-content-generation
- Duolingo AI-first (Technology Magazine): https://technologymagazine.com/ai-and-machine-learning/duolingos-ai-first-strategy-explained
- Duolingo 148 courses: https://investors.duolingo.com/news-releases/news-release-details/duolingo-launches-148-new-language-courses
- Speak: https://www.speak.com/
- 말해보카: https://apps.apple.com/kr/app/id1460766549 · https://www.busan.com/view/busan/view.php?code=2022111412270281157

**Q6 저작권**
- US Copyright Office AI: https://www.copyright.gov/ai/
- Skadden 요약(2025 보고서): https://www.skadden.com/insights/publications/2025/02/copyright-office-publishes-report
- Substantial similarity (Gordon Feinblatt): https://www.gfrlaw.com/what-we-do/insights/copyright-infringement-similarity-expression-must-be-substantial
- Close paraphrasing (Wikilegal): https://meta.wikimedia.org/wiki/Wikilegal/Close_Paraphrasing
