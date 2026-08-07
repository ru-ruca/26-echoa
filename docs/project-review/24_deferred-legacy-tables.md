# 미모델링 legacy 테이블 4개 — 존폐 판정 보류

> 작성일: 2026-08-07 (모노레포 스캐폴딩 중)
> 상태: **보류** — 판정 시점은 [22번 spec](22_learning-design-spec.md) 검토 때
> 관련: [ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md) · [23 §9](23_content-pipeline-spec.md)

## 무엇인가

legacy 라이브 DB에는 있는데 `web/src/db/schema.ts`에도 drizzle 스냅샷에도 **없는** 테이블 4개다.
그래서 legacy 앱 코드가 한 번도 읽은 적이 없다. 새 `packages/db` 스키마에서도 일단 **뺐다**.

| 테이블 | 행 수 | 성격 |
|---|---|---|
| `quizzes` | 934 | 월/주 단위 퀴즈 (fill_blank·multiple_choice) |
| `daily_expressions` | 105 | 일일 표현 |
| `question_patterns` | 91 | 질문 패턴 + 예문 |
| `grammar_patterns` | 48 | 월별 문법 패턴 + 예문 |

## 왜 지금 판정하지 않나 — 의존성

| 무엇과 얽히나 | 관계 | 결론 |
|---|---|---|
| 새 스키마 baseline | clean baseline이라 나중 추가는 **마이그레이션 1개**로 끝난다 (legacy는 drift 때문에 이게 안 됐다) | 선행 조건 **아님** |
| [22번 학습설계 spec](22_learning-design-spec.md) | `quizzes`는 복습 퀴즈 자산인데 22번이 복습을 **FSRS + 3타입(sentence/word/collocation) × 퀴즈 분기**로 재설계했다. 나머지 3개는 22 §7 학습모드 확장·§8 콘텐츠 백로그와 직결 | **여기서 판정해야 근거가 생긴다** |
| [23 §9 C-2 미결정](23_content-pipeline-spec.md) | `question_patterns`(91)는 C-2 패턴 문장(528건)과 **같은 문제 공간**이다 — "패턴 변형을 학습 흐름에서 어떻게 쓸까" | **묶어서 한 번에** 판정 |
| legacy 데이터 이관 | 이관 스크립트는 대상 테이블 목록이 확정돼야 짤 수 있다 | **이관 직전이 마감 시한** |

판정 근거가 "학습 흐름에서 실제로 쓰이느냐"인데, 그 답은 22번에서만 나온다.
버리지 않고 legacy Neon DB에 그대로 둔 채, 필요해지면 되살린다.

## 판정 순서

1. **22번 spec 검토·확정** — 4테이블 + C-2 소비 방식을 **묶어서** 판정
2. → legacy 데이터 이관 스크립트 작성 (판정 결과 반영)
3. → 필요한 것만 `packages/db`에 마이그레이션으로 추가

## 컬럼 정의 (legacy `docs/db-schema/01-TABLE-DEFINITIONS.md`에서 옮김)

판정할 때 legacy repo를 다시 열지 않아도 되도록 정의만 보존한다.

```sql
CREATE TABLE quizzes (
  id SERIAL PRIMARY KEY,
  month INTEGER NOT NULL,
  week INTEGER,
  quiz_type VARCHAR(50),              -- fill_blank, multiple_choice, etc.
  question_en TEXT NOT NULL,
  question_kr TEXT,
  options JSONB,                      -- 선택지 배열
  answer TEXT NOT NULL,
  explanation TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE daily_expressions (
  id SERIAL PRIMARY KEY,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  expression_en TEXT NOT NULL,
  expression_kr TEXT NOT NULL,
  context TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE question_patterns (
  id SERIAL PRIMARY KEY,
  pattern VARCHAR(500) NOT NULL,
  pattern_kr VARCHAR(500),
  cefr_level VARCHAR(10),
  examples JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE grammar_patterns (
  id SERIAL PRIMARY KEY,
  month INTEGER NOT NULL,
  pattern_name VARCHAR(200),
  description TEXT,
  examples JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 판정할 때 볼 것

- `quizzes` 934건: 22 §9 복습 화면이 정의한 3분기(fill_blank·listening·speaking)와
  `quiz_type`이 겹치는지. 겹치면 재활용, 아니면 폐기.
- `question_patterns` 91건 + C-2 528건: 둘 다 "패턴 + 변형"이다. 학습 흐름에서
  **복습 변형 문제**로 쓸지 **신규 문장**으로 쓸지가 정해지면 둘의 운명이 같이 정해진다.
- `daily_expressions` 105 · `grammar_patterns` 48: 22 §7 "학습 모드 확장"의 재료인지.
  legacy `expressions`(658건, 이미 모델링됨)와 중복되지 않는지 확인 필요.
