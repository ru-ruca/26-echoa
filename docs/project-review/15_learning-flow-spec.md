# SenTalk 학습 절차 명세

> 작성일: 2026-04-12
> 상태: 구현 완료
> 관련 코드: `web/src/components/learn/step-by-step-flow.tsx`

---

## 1. 전체 학습 플로우

```
앱 진입 → Home → "오늘의 학습" 클릭 → Learn/[id] 페이지
                                        │
                                        ▼
                              ┌─────────────────┐
                              │  Step 1: Sentence │
                              │  (문장 학습)       │
                              └────────┬──────────┘
                                       │ Continue
                                       ▼
                              ┌─────────────────┐
                              │  Step 2: Words    │
                              │  (단어 학습)       │
                              └────────┬──────────┘
                                       │ Continue
                                       ▼
                              ┌─────────────────┐
                              │  Step 3: Practice │
                              │  (연습 2단계)      │
                              └────────┬──────────┘
                                       │ Continue
                                       ▼
                              ┌─────────────────┐
                              │  Step 4: Complete │
                              │  (평가 Again/Good)│
                              └────────┬──────────┘
                                       │ Rating 선택
                                       ▼
                              ┌─────────────────┐
                              │  Lesson Complete  │
                              │  +XP earned       │
                              └─────────────────┘
```

---

## 2. 컴포넌트 상태 관리 구조

```
StepByStepFlow (부모 — 모든 상태 소유)
│
├── activeStep: number (0-3, 현재 진행 스텝)
├── completedSteps: Set<number> (완료된 스텝 인덱스)
├── reviewingStep: number | null (리뷰 중인 스텝)
├── practiceState: PracticeState (Practice 내부 상태 — 부모에서 관리)
│   ├── phase: 'fill_blank' | 'listening' | 'summary'
│   ├── fillBlankCorrect: boolean | null
│   ├── listeningCorrect: boolean | null
│   └── listeningSkipped: boolean
├── practiceResult: PracticeResult | null (Practice 완료 결과)
├── isSubmitting: boolean
├── isCompleted: boolean
└── earnedXp: number

※ practiceState를 부모에서 관리하는 이유:
   리뷰 모드로 다른 스텝을 열면 Practice가 unmount →
   자식 useState가 초기화됨 → 상태 유실.
   부모에서 관리하면 unmount/remount 시에도 상태 보존.
```

---

## 3. 아코디언 동작 규칙

### 기본 원칙: **항상 1개만 열림** (배타적 아코디언)

```
규칙 1: 리뷰 중이 아닐 때 → active 스텝만 열림
규칙 2: 리뷰 중일 때 → 리뷰 스텝만 열림 (active 포함 모두 닫힘)
규칙 3: "Back to Current" → 리뷰 해제, active 스텝 다시 열림
규칙 4: locked 스텝은 클릭 불가
규칙 5: Practice 상태는 unmount 시에도 보존 (부모 상태)
```

### isExpanded 결정 로직

```typescript
const isExpanded =
  reviewingStep !== null
    ? reviewingStep === index    // 리뷰 중: 리뷰 스텝만
    : state === 'active';        // 평시: active 스텝만
```

### 3가지 카드 상태

| 상태 | 조건 | 외관 | 클릭 동작 |
|------|------|------|----------|
| **active** | `index === activeStep && !completed` | 펼쳐진 카드, primary 좌측 보더 | 콘텐츠 표시 |
| **completed** | `completedSteps.has(index)` | 접힌 카드, ✓ + 요약 텍스트 | 클릭 → 리뷰 모드 |
| **locked** | `index > activeStep && !completed` | 회색, 🔒 아이콘 | 클릭 불가 |

---

## 4. 상태 전이도 (전체)

```
초기 상태:
  [Sentence: ACTIVE] [Words: LOCKED] [Practice: LOCKED] [Complete: LOCKED]
  activeStep=0, completedSteps={}, reviewingStep=null

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: Sentence → Continue 클릭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  completedSteps += {0}
  activeStep = 1
  [Sentence: COMPLETED] [Words: ACTIVE] [Practice: LOCKED] [Complete: LOCKED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: Words → Continue 클릭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  completedSteps += {1}
  activeStep = 2
  practiceState.phase = 'fill_blank' (초기값)
  [Sentence: COMPLETED] [Words: COMPLETED] [Practice: ACTIVE] [Complete: LOCKED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: Practice 진행 중 Sentence 클릭 (리뷰)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  reviewingStep = 0
  → isExpanded: reviewingStep(0)만 열림
  → Practice(active)는 닫히지만 practiceState 보존 (부모 상태)
  [Sentence: REVIEW/열림] [Words: COMPLETED] [Practice: ACTIVE/닫힘] [Complete: LOCKED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: "Back to Current" 클릭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  reviewingStep = null
  → Practice가 다시 열림, 이전 phase 상태 그대로 복원
  [Sentence: COMPLETED] [Words: COMPLETED] [Practice: ACTIVE/열림] [Complete: LOCKED]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: Practice Summary → Continue 클릭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  completedSteps += {2}
  activeStep = 3
  practiceResult = { fillBlankCorrect, listeningCorrect, listeningSkipped }
  [Sentence: COMPLETED] [Words: COMPLETED] [Practice: COMPLETED] [Complete: ACTIVE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이벤트: Complete → Again 또는 Good 클릭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  POST /api/progress → FSRS 스케줄링 + XP + 스트릭
  completedSteps += {3}
  isCompleted = true
  → 🎉 Lesson Complete 화면 렌더링
```

---

## 5. Practice 내부 상태 전이도

```
Practice 스텝이 열릴 때 practiceState 기준 렌더링:

  ┌─────────────┐
  │ phase =     │
  │ 'fill_blank'│  ← 초기값
  └──────┬──────┘
         │ Check 답변 → fillBlankCorrect 설정
         │ "Next: Listening" 클릭
         ▼
  ┌─────────────┐
  │ phase =     │
  │ 'listening' │     진행도: 1/2 → 2/2
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Check    Skip listening
    │      listeningSkipped=true
    │      phase='summary' (자동)
    │         │
    ▼         │
  "See Results"
  phase='summary'
    │         │
    └────┬────┘
         ▼
  ┌─────────────┐
  │ phase =     │
  │ 'summary'   │
  │             │
  │ 결과 표시:   │
  │ Fill-blank: ✅/❌        │
  │ Listening:  ✅/❌/Skipped │
  └──────┬──────┘
         │ Continue 클릭
         │ → onComplete() 호출
         │ → 부모가 practiceResult 저장
         │ → activeStep = 3 (Complete)
         ▼
  Practice 완료 → Complete 스텝으로

※ 리뷰 시 Practice 열면:
  - savedResult 존재 → 저장된 결과 표시
  - savedResult 없음 → practiceState 기준 현재 phase 표시 (상태 보존)
```

### Practice 진행도 표시

| Phase | 표시 | 설명 |
|-------|------|------|
| fill_blank | "1/2" | 빈칸 채우기 |
| listening | "2/2" | 듣고 쓰기 |
| summary | 결과 | "X/Y Correct" |

### Summary 결과 표시 (Listening Skip 포함)

| Fill-blank | Listening | 표시 |
|-----------|-----------|------|
| ✅ Correct | ✅ Correct | "2/2 Correct" |
| ✅ Correct | ❌ Incorrect | "1/2 Correct" |
| ✅ Correct | Skipped | "1/1 Correct" + "Listening: Skipped" |
| ❌ Incorrect | Skipped | "0/1 Correct" + "Listening: Skipped" |

---

## 6. 각 스텝 와이어프레임

### Step 1: Sentence

```
┌─────────────────────────────────────┐
│  🎧 Sentence              [Review] │
│  Step 1 of 4                        │
│                                     │
│  "Listen, read, and understand"     │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  "Once upon a time, a       │    │
│  │   little Mouse lived        │    │
│  │   in a forest."             │    │
│  │       [🔊 Play]             │    │
│  │  IPA: /wʌns əˈpɑn.../      │    │
│  │  Stress: once, time, mouse  │    │
│  │  ─────────────────────      │    │
│  │  [Show Meaning]             │    │
│  └─────────────────────────────┘    │
│  [Continue ▶]                       │
└─────────────────────────────────────┘
```

### Step 2: Words

```
┌─────────────────────────────────────┐
│  📚 Words                  [Review] │
│  Step 2 of 4                        │
│  "Study the key vocabulary"         │
│                                     │
│  ┌─ Collocation Quiz ─── 1/3 ─┐    │
│  │  once a ___                 │    │
│  │  [입력]  [Check]            │    │
│  └─────────────────────────────┘    │
│                                     │
│  🔊 once /wʌns/ 한 번 ── adv A2    │ ← 클릭→사전
│     once a week  at once            │
│  🔊 upon /əˈpɑn/ ~에 ── prep B1    │
│  🔊 time /taɪm/ 시간 ── noun A1    │
│     free time  have time            │
│                                     │
│  [Continue ▶]                       │
└─────────────────────────────────────┘
```

### Step 3: Practice

```
Phase 1 (1/2):                    Phase 2 (2/2):
┌──────────────────────────┐     ┌──────────────────────────┐
│  ✏ Practice               │     │  ✏ Practice               │
│  Step 3 of 4              │     │  Step 3 of 4              │
│  Practice...      1/2     │     │  Now try...       2/2     │
│                            │     │                            │
│  ┌─ Fill in the Blank ─┐  │     │  ┌─ Listening Quiz ──┐    │
│  │ "옛날 옛적에..."     │  │     │  │ "Listen and type"  │    │
│  │ "Once ___ a time..." │  │     │  │     [🔊 Play]      │    │
│  │ [입력]  [Check]      │  │     │  │ [Hint]             │    │
│  └──────────────────────┘  │     │  │ [textarea]         │    │
│                            │     │  │ [Check]            │    │
│  → 답변 후:                │     │  └────────────────────┘    │
│  [Next: Listening ▶]       │     │                            │
└──────────────────────────┘     │  → 답변 후:                │
                                  │  [See Results ▶]            │
                                  │  (또는) Skip listening      │
                                  └──────────────────────────┘

Summary:
┌──────────────────────────┐
│  ✏ Practice               │
│  Practice Results         │
│  🎉 2/2 Correct!         │
│  +10 bonus XP             │
│  Fill-blank: ✅ Correct   │
│  Listening:  ✅ Correct   │
│  [Continue ▶]             │
└──────────────────────────┘
```

### Step 4: Complete

```
┌─────────────────────────────────────┐
│  ✔ Complete                         │
│  Step 4 of 4                        │
│  "How well do you know this?"      │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  "Once upon a time..."      │    │
│  │  "옛날 옛적에..."           │    │
│  └─────────────────────────────┘    │
│                                     │
│  Suggest "Good" (+5 bonus XP)       │
│                                     │
│  [Again < 10m]    [Good ~3d]        │
└─────────────────────────────────────┘
```

---

## 7. 과거 문제점 및 수정 이력

| 날짜 | 문제 | 원인 | 수정 |
|------|------|------|------|
| 2026-04-12 | Practice 중 다른 스텝 클릭 시 Practice 사라짐 | `isExpanded`가 active + reviewingStep 동시 허용 | 배타적 아코디언으로 변경 |
| 2026-04-12 | Practice와 Complete가 동시 열림 | 위와 동일 | 위와 동일 |
| 2026-04-12 | Practice 리뷰 후 돌아오면 상태 유실 | PracticeContent의 자체 useState가 unmount 시 초기화 | practiceState를 부모로 올림 |
| 2026-04-12 | Practice 진행도 구분 불가 | phase 표시 없음 | 1/2, 2/2 진행도 추가 |
| 2026-04-12 | Listening Skip 시 결과에 미표시 | Skip 시 결과 배열에서 제외 | "Skipped" 상태 표시 |
| 2026-04-12 | Practice/QuizFillBlank/QuizListening 스타일 불일치 | 각 컴포넌트가 다른 스타일 | CollocationQuiz 스타일로 통일 |

---

## 8. 공통 UI 규칙

### 버튼 스타일

| 용도 | 컴포넌트 | 스타일 |
|------|----------|--------|
| Continue/전환 | StepButton | `bg-primary w-full rounded-xl py-3 text-sm font-semibold text-white` |
| 퀴즈 Check | 각 퀴즈 내부 | `bg-primary rounded-lg px-6 py-2 text-sm font-medium text-white` |
| 평가 (Again/Good) | RatingButtons | `grid-cols-2 gap-3`, red/emerald `rounded-xl py-3 font-bold` |
| Skip 링크 | 텍스트 | `text-muted-foreground text-sm` |

### 퀴즈 컴포넌트 (CollocationQuiz, QuizFillBlank, QuizListening 공통)

| 요소 | 스타일 |
|------|--------|
| 컨테이너 | `bg-background rounded-xl p-4` |
| 입력 필드 | `border-border bg-card rounded-lg px-3 py-2 text-center text-sm` |
| Check 버튼 | `bg-primary rounded-lg px-6 py-2 text-sm` |
| 결과 표시 | `rounded-lg px-3 py-2` + emerald/red 배경 |

---

## 9. 데이터 흐름

```
Learn/[id] (Server Component)
  │
  │ getSentenceData(id) → 문장+IPA+단어+콜로케이션+인접ID
  │
  ▼
StepByStepFlow (Client Component)
  │
  ├── Step 1: Sentence → 표시만 (API 호출 없음)
  ├── Step 2: Words → 표시만 (API 호출 없음)
  ├── Step 3: Practice → practiceState (부모 관리, 로컬 상태)
  └── Step 4: Complete → POST /api/progress
                           │ (트랜잭션)
                           ├── FSRS 카드 스케줄링
                           ├── XP 부여 (rating + practiceBonus)
                           ├── 스트릭 업데이트
                           └── 응답: { xpEarned }
```

---

## 10. XP 보상 체계

| 행동 | XP |
|------|-----|
| 신규 문장 학습 완료 | 10 XP |
| 복습 Good | 5 XP |
| 복습 Again | 1 XP |
| Practice 정답 (각 퀴즈당) | 5 XP |
| 7일 연속 보너스 | 50 XP |

### 제안 평가 로직

```
Practice 결과 → 자동 제안:
  모두 정답 → "Good" 제안
  1개 이상 정답 → "Good" 제안
  모두 오답 → "Again" 제안
```
