# 19. 일상 소통 중심 재설계 — 말하기 내장 + 매일 회화

> **작성**: 2026-07-09
> **성격**: 재설계 SSOT(단일 근거처). 학습 근거는 [research/2026-07_speaking-redesign-research.md](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md), 기술 결정은 [ADR-008](../../../26-SenTalk-en-study-app/docs/adr/008_speaking-practice-stt.md), 결정 요약은 [Decision Log](../adr/000_decision-log.md) D-18~D-20.
> **선행 문서**: [15 학습 절차 명세](15_learning-flow-spec.md) · [16 종합 점검](../../../26-SenTalk-en-study-app/docs/project-review/16_project-audit-2026-04.md) · [learning-strategy-review §3.5](../../../26-SenTalk-en-study-app/docs/analysis/learning-strategy-review.md) · [phase4/d1 회화 설계](../../../26-SenTalk-en-study-app/docs/phase4/d1-conversation-design.md)

---

## 1. 왜 (Context)

앱 소유자이자 본인 학습자의 요청: "단어 암기를 잘 못하고, 초급에서 영어를 포기한 적이 있으며, 일상 소통이 목표"인 자신이 실제로 쓸 수 있도록 설계부터 재검토.

**핵심 발견**: 이 프로필은 이 앱의 **원래 페르소나와 동일**하다([archive/11 마스터 문서](../../../26-SenTalk-en-study-app/docs/archive/11_project_master_document.md): 창업 동기 = 해외 출장 회화 + 단어암기식 학습 실패). 문제는 **구현이 원래 비전(실용 회화)에서 읽기·듣기 이해 + SRS 암기 앱으로 이탈**한 것.

### 확인된 요구사항 (2026-07-08 문답)
| 항목 | 답변 |
|------|------|
| 소통 장면 | 여행·해외 방문 + 스몰토크 + 듣고 이해 + 폭넓게 일상 전반 |
| 하루 학습 시간 | 15~20분 |
| 말하기 연습 | 소리 내어 연습 의향 있음 (마이크·음성인식 OK) |
| 콘텐츠 방향 | 기존 커리큘럼 유지 + 매일 관련 회화 1~2문장 증강 (사용자 제안) |
| 첫 구현 | 쉐도잉 + 발음 UI 부활 |

---

## 2. 진단 — 3대 괴리

1. **산출(말하기) 부재**: 학습 행동이 타이핑·탭뿐. 말하기 훈련 경로 0(STT·녹음·쉐도잉 코드 전무). `components/pronunciation/` 5개 컴포넌트는 import 0건 죽은 코드. STT는 [NEXT-TASKS](../../../26-SenTalk-en-study-app/docs/NEXT-TASKS.md) P3 최하위. — 소통이 목표인데 발화가 없음.
2. **회화 노출 부족**: 7일 사이클 중 5일이 명언·동화·영화·속담, 일상 회화는 주 1일(목). M01 2일차부터 동화 과거시제 서사체("Once upon a time, a little Mouse lived...")로 포기 경험자의 좌절 지점이 초반 배치. 목표에 맞는 real 337문장·dialogues 539줄은 있으나 소수/미적재.
3. **커리큘럼 이정표 부재**: "4년 뒤 C1"만 있고 "언제부터 소통 가능한가"의 근접 목표 없음. 재도전 학습자에겐 원거리 목표가 무효([research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) M2).

**유지·활용할 자산**: FSRS 2버튼 복습(D-01), 4단계 아코디언(D-02), 게이미피케이션, real 337·dialogues 539, [d1 회화 설계](../../../26-SenTalk-en-study-app/docs/phase4/d1-conversation-design.md)(20상황 ~110문장, 미실행), 죽은 발음 컴포넌트 5종(데이터도 DB에 100% 존재), 콜로케이션 5,705, 예문 데이터.

---

## 3. 재설계 5축

> 원칙: D-01·D-02 뼈대 유지. 자산 폐기 0. 과잉 설계 금지. **"뜻 암기 활동 0"을 설계 원칙으로 승격**(근거: [research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) L3·L4 — 단어카드가 비효율이라서가 아니라 이 사용자의 실패 이력·심리에 안 맞아서).

### 축 1. 말하기 내장 (새 스텝 없이, 3단 사다리)
- **Step 1 Sentence** — Tier 0 쉐도잉: TTS 청취 직후 ① 스크립트 보며 따라 1~2회 → ② 뜻 확인 → ③ 스크립트 숨기고 2회. honor system, 판정 없음(정의적 여과 최소화). 4~6회 상한(plateau). 죽은 `PronunciationGuide` 부활, 긴 문장은 `ipaChunks` 청크별. 마이크 불필요.
- **Step 3 Practice** — speaking phase 추가(fill_blank→listening→speaking→summary). 한 자리를 사다리로 점진 업그레이드. 기존 "Skip listening" 패턴 복제로 폴백.
- **Tier 1 녹음-자가비교**: `useRecorder`(MediaRecorder), 내 목소리/원어민 A/B, 자기 판정. 저장·전송 없음.
- **Tier 2 STT 인식 확인**: 녹음→서버 전사→내용어 매칭 ≥60~70% 통과(3회 후 자동 통과). "AI가 알아들었나" 프레이밍. → [ADR-008](../../../26-SenTalk-en-study-app/docs/adr/008_speaking-practice-stt.md).
- **복습**: `selectQuizType` 문장 reps≥2를 fill_blank/listening/speaking 3분기로. 마이크 불가 시 listening 폴백.
- 근거: [research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) §1(쉐도잉), §2(발화 인출). 배치 경계 준수 — 발화는 학습 후 인출에만, 쉬운 것부터.

### 축 2. 매일 회화 증강 (기존 유지 + 관련 회화 1~2)
하루 = [기존 문장 1개(현행 유지)] + [회화 페어 1~2개]. **요일 구조·기존 콘텐츠 보존**, 회화 노출 주 1일 → 매일.
- 소싱 우선순위: ① `sentence_words` 조인으로 어휘 공유 기존 문장 매칭(제작 0) → ② dialogues 539줄 적재분(제작 0) → ③ 부족분만 AI 생성(미지 단어 ≤1) → ④ 보조로 Tatoeba/VOA(라이선스 검증분, [research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) §8).
- 배치: 같은 month/week/day 순차 삽입 → `/api/next-lesson`이 정렬 기반이라 **앱 코드 수정 0, 데이터 INSERT/UPDATE만**. 페어는 notes에 `paired:` 기록.
- **M01~M03 먼저**, 이후 월 단위 점진. 문장 증가 → FSRS 큐 증가(안정기 15~20장/일) → 4~6주 관찰 후 페어 수 조정.

### 축 3. 커리큘럼 이정표 ("4년 뒤 C1" → "6주 뒤 여행 생존")
- `web/src/lib/curriculum-stages.ts` 상수 1개로 스테이지 오버레이(month 1~48 골격 불변): S1(M01-02) 여행 생존 1 → S2(M03-04) 여행 생존 2 → S3(M05-08) 스몰토크 입문 → S4(M09-12) A2 진입 → S5/S6.
- 스테이지 정의는 생존영어 8상황([research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) C3). **"되묻기"가 d1에 없으면 최우선 추가**.
- 졸업 과제: 초기 쉐도잉 self-check → STT 도입 후 "통과". 홈 진행률 "M01 Week2" → "여행 생존 1 — 8/20문장".
- 근거: 근접 하위목표·자기효능감([research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) M2·M3), CEFR can-do(C1). **레벨 수 세분화가 아니라 과업 기반**(CEFR-J 인접 서브레벨 변별력 약함, C5).

### 축 4. 단어 암기 약점 대응 (뜻 암기 0)
- Words 카드를 단어 → 콜로케이션 구 헤드라인("wake up — The Lion woke up")으로. 기존 Phase 5 P1 콜로케이션 계획과 병합.
- word 복습을 영한 매칭 → 예문 빈칸 우선("I ___ up at 7 AM.", `vocabulary.examples`). 예문 없을 때만 매칭 폴백.
- 재등장 배지: 새 문장에 아는 단어 포함 시 "아는 단어 3개"(`sentence_words` 조인) — 다중 맥락 재노출 가시화.
- 근거: [research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) §3(Lexical), §2 P1·P2(production 인출).

### 축 5. 15~20분 세션 (3부 + 최소 코스)
- ① 복습 워밍업 4~5분(FSRS ~6장, 1~2장 speaking) → ② 신규 8~10분(기존+회화 페어, 쉐도잉 포함) → ③ 오늘의 소리내기 3~5분(오늘+어제+그제 연속 쉐도잉 — 초 단위 회상은 세션 내에서만, [research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) P11).
- **최소 코스**: "복습 5분" 또는 "신규 1문장"도 스트릭 인정 — 성인 탈락 1위가 시간 부족([research](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md) M6), all-or-nothing 이탈 방지(M9).
- 홈 "오늘의 플랜" 체크리스트(`DailyGoal` 확장).

---

## 4. 로드맵 (세션 단위, 각각 독립 배포 가능)

| 순서 | 증분 | 규모 |
|------|------|------|
| **완료** | Phase 0 백업 + 정리 (admin 2종·잔재·next-pwa 제거, DB 테이블 보류) | — |
| S1 | 쉐도잉 + 발음 UI 부활 (Tier 0, `PronunciationGuide` 연결, `LessonData.ipa` 타입 확장, `speakingPractice` 토글) | 코드 소 |
| C1 | 매일 회화 증강 M01~03 (dayType 정규화 + dialogues Y1 적재 + 페어 매칭/생성) | 데이터 중 |
| M1 | 스테이지 이정표 (`curriculum-stages.ts` + 홈 진행률) | 코드 소 |
| P1 | 녹음-자가비교 Tier 1 (`use-recorder`). **iOS 실기기 테스트 = getUserMedia는 https 필수 → Vercel 프리뷰/https 터널 선행** | 코드 중 |
| V1 | 단어 학습 개선 (예문 빈칸·콜로케이션 헤드라인·재등장 배지, Phase 5 P1 병합) | 코드 소 |
| T1 | 세션 구조 (오늘의 플랜 3부 + 최소 코스) | 코드 소 |
| 게이트 후 | P2 서버 STT Tier 2. **착수 게이트: P1 녹음 주 3회+ 실사용 2~4주 관찰** | 코드 중~대 |

**하지 말 것**: 발음 유사도 채점 알고리즘, Web Speech `SpeechRecognition`(iOS PWA 미동작), 마일스톤 DB 테이블, 48개월 일괄 증강, 요일별 해금 스케줄러, 적응형 커리큘럼 엔진, AI 프리토킹 봇(초보 부적합) — 전부 사용자 1명·15~20분 앱의 ROI 초과.

---

## 5. 핵심 파일 (구현 참조)
- `web/src/components/learn/step-by-step-flow.tsx` — 쉐도잉·speaking phase(PracticePhase 머신, `LessonData.ipa` 타입, Skip 패턴)
- `web/src/components/pronunciation/pronunciation-guide.tsx` — 부활 대상(props: sentence/ipa/stressWords/intonationPatternId/showCurve)
- `web/src/app/learn/[id]/page.tsx` — 이미 ipaChunks·intonation 조회 중, 타입 확장만
- `web/src/lib/review-utils.ts` — `QuizMode`/`selectQuizType` 확장
- `web/src/components/review/quiz-listening.tsx` — `checkAnswer` → `lib/text-match.ts` 추출 원본
- `web/src/app/api/next-lesson/route.ts` — month/week/day 정렬(증강이 코드 무수정 동작하는 근거)
- `docs/phase4/d1-conversation-design.md` — dayType 정규화 SQL·프롬프트 템플릿
- DB 필드: `sentence_ipa.intonationPatternId/ipaChunks`, `vocabulary.syllableBreakdown/primaryStressPosition/examples`, `sentence_words`

---

## 6. 검증 방법
- S1: iOS Safari(홈화면 PWA)·Android Chrome 실기기 쉐도잉 UI+억양 커브 렌더, `cd web && pnpm format && npx tsc --noEmit && pnpm test:unit:run`
- C1: 증강 후 `/api/next-lesson`이 "기존 문장 → 페어 회화" 순인지 M01 W1 실제 학습으로 확인, FSRS 큐 크기 관찰
- P1: iOS 실기기 녹음→재생(audio/mp4), 권한 거부 시 폴백
- P2: 착수 게이트 통과 확인 → `text-match.ts` unit + Playwright fake-device
- 공통: 학습 1문장 완주 회귀, `docs/qa-test-cases.csv` TC 추가

---

*출처: 전 항목 근거는 [research/2026-07_speaking-redesign-research.md](../../../26-SenTalk-en-study-app/docs/research/2026-07_speaking-redesign-research.md).*
