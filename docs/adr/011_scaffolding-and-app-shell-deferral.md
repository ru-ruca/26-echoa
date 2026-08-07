# ADR-011: 스캐폴딩 실행 방식과 앱 껍데기 유예

> Status: **Accepted** (2026-08-07)
> **Amends**: [ADR-009](009_stack-monorepo-decision.md) — §Decision-1 유예 · §Decision-3 변경 · §2·§4 유지
> 근거 원자료: [2026-08 앱 껍데기 재검토](../research/2026-08_app-shell-reassessment.md)
> 재구성 계획: [21 §2·§4·§8](../project-review/21_rebuild-plan.md)

## Context

ADR-009(2026-07-27)는 **RN/Expo + Next.js 모노레포**를 `create-t3-turbo` 기반으로 만들기로 했다.
스캐폴딩에 착수하며 확인하니 그 결정의 전제 두 개가 깨져 있었다.

1. **`create-t3-turbo`가 8개월 정체** — main 마지막 커밋 2025-12-12. Next 15 · Expo SDK 54(RN 0.81) ·
   React 19.1 · better-auth 1.4-beta에 고정돼 있다. legacy(`26-SenTalk`)가 이미 Next 16.2.3 ·
   React 19.2.3이라, 스타터를 그대로 쓰면 **뒤로 가는** 스캐폴딩이 된다.
   ADR-009이 이 스타터를 고른 이유("인증·타입공유 재발명 회피")는 배선 패턴이지 버전이 아니었다.

2. **"개발자는 Dart 미경험"이 더 이상 사실이 아니다** — 회사 프로젝트 `bg-user-flutter`가 Flutter다.
   단 실물은 Flutter UI 앱이 아니라 **WebView 래퍼**(Dart 3파일 + 네이티브 브리지, release signing 완료)다.
   보유 경험은 "Flutter UI"가 아니라 **"웹 앱을 네이티브로 감싸 스토어에 올리는 절차"**다.

두 번째 전제가 깨지면서 선택지가 넓어졌다. 전면 재검토했다 —
Expo 모노레포 / Capacitor 래퍼 / Flutter WebView 래퍼 / Expo universal / Flutter 앱 5개.
비교표와 근거는 [research 문서](../research/2026-08_app-shell-reassessment.md) §3에 있다.

핵심 발견 두 가지:

- **Echoa가 웹으로 못 하는 것은 3개뿐**이다 — TTS(iOS Safari는 `getVoices()`가 빈 배열, 백그라운드 중단) ·
  녹음 · AdMob. 그래서 진짜 축은 "네이티브를 얼마나 하느냐"가 아니라 **"UI를 몇 벌 쓰느냐"**다.
- **`packages/{core,db,api}`는 어느 껍데기를 골라도 동일하다.** 지금 만들 것의 대부분이
  껍데기 결정과 무관하다 — 결정을 미뤄도 버리는 작업이 없다.

## Decision

### 1. 스타터를 clone하지 않고 최신 버전으로 손수 구성한다 (ADR-009 §3 변경)

`create-t3-turbo`는 **배선 참조**로만 쓴다 — `tooling/*` 분리, pnpm catalog로 버전 단일화,
tRPC↔Next 연결, Better Auth 스키마 형태. 채택 버전은 착수 시점 최신으로 고정한다:

Next 16.3.0 · React 19.2 · TypeScript 5.9 · Tailwind 4 · tRPC 11.18 · Drizzle 0.45.2 ·
Better Auth 1.6.26 · Turborepo 2.10.8 · ESLint 10 · Vitest 4.

> Drizzle 1.0은 rc 단계라 **0.45.2 유지**(legacy와 동일). 1.0 승격 시 별도 판단한다.

### 2. 앱 껍데기를 유예한다 (ADR-009 §1 유예 — 배제 아님)

이번 스캐폴딩은 `apps/web` + `packages/{core,db,api}`만 만든다.
**`apps/native`도 `packages/ui`도 만들지 않는다** — 빈 Expo 셸은 turbo 그래프·CI·의존성만 늘리고
아무것도 검증하지 않는다. UI 소비처가 하나뿐인데 UI 패키지를 미리 가르지도 않는다.

이건 ADR-009 §Decision-4("네이티브 착수 트리거 = TTS")를 **앞당기지 않고 그대로 따르는** 선택이다.

### 3. 트리거 도달 시 껍데기를 재평가한다 (ADR-009 §4 강화)

웹 학습 흐름이 완성돼 TTS 제약이 실제로 드러나면, 그 시점에 다시 고른다.
현재 기본 후보는 **Capacitor**다 — UI 1벌로 가면서 TTS·녹음·AdMob만 네이티브 플러그인으로 붙인다.
감수할 것은 Apple 4.2.2(단순 웹 래핑 금지) 심사 위험인데, Echoa는 TTS·녹음이 부가가 아니라
**핵심 기능**이라 명분이 있다. 이 판단이 틀리면 `apps/native`(Expo)로 전환한다 —
`packages/{core,db,api}`가 그대로 넘어가므로 버려지는 작업은 UI 한 벌뿐이다.

### 4. Flutter는 계속 배제한다 (ADR-009 §근거 유지)

전제가 바뀌었어도 결론은 같다.

- **Flutter 앱 + Next.js 웹**: 로직까지 2벌(TS + Dart). `ts-fsrs`·Drizzle·게이미피케이션을 전부
  다시 써야 한다. 1인에게 가장 비싼 안이다.
- **Flutter Web**: 2026-08 현재도 canvas 렌더링이라 크롤러가 시맨틱 HTML을 못 본다.
  ADR-009의 웹 SEO 근거는 그대로 유효하다.
- **Flutter WebView 래퍼**(회사 방식): 실현 가능하지만 브리지를 Dart로 직접 써야 한다.
  Capacitor는 같은 일을 JS API 호출로 한다 — 유지할 언어가 하나 줄어든다.

### 5. `packages/api`는 tRPC v11로 확정 (21 §2 미확정 해소)

21 §2가 "tRPC 라우터 **또는** API 클라이언트"로 열어 뒀던 것을 닫는다.
근거: Next 16 App Router 정식 지원, 입력 스키마가 라우터에 붙어 있어 **DB 없이도 계약을
자동 검증**할 수 있다(1인 개발에서 검증 자동화가 쉬운 쪽). 껍데기가 무엇이 되든
타입이 그대로 이어진다.

### 6. `packages/db` 스키마는 복사가 아니라 재선언

legacy `schema.ts`는 drizzle 스냅샷이 라이브 DB와 어긋나 `db:push`가 금지된 상태였고
(`schema.ts:52-55`), `references()` 호출이 **0건**이라 참조 무결성을 DB가 보장하지 않았으며,
`users` 테이블 자체가 없었다. 부채를 그대로 들고 가지 않는다 — 깨끗한 baseline으로 다시 선언한다.
[ADR-010](010_content-copyright-and-data-model.md)의 원문 격리는 **배럴 분리로 코드에서 강제**한다
(`schema/public.ts`에 `content_originals`를 넣지 않아, 공개 진입점으로는 타입 수준에서 닿을 수 없다).

## 결과 / 트레이드오프

- **얻는 것**: 8개월 부채 없이 시작. legacy와 버전 일치. UI를 몇 벌 쓸지 결정을 정보가 많은
  시점으로 미룸. 껍데기와 무관한 자산(core·db·api)을 먼저 확보.
- **감수**: 스타터의 검증된 Metro monorepo·Expo↔tRPC 배선을 나중에 직접 맞춰야 한다
  (Expo로 갈 경우). Capacitor로 가면 Apple 4.2.2 심사 위험을 진다.
- **되돌리기**: 껍데기 결정은 어느 쪽으로든 되돌릴 수 있다. `packages/*`가 공통이라
  전환 비용은 UI 한 벌이다.
- **21 §8 단계 1 검증 기준 조정**: "웹/앱 동시 기동" → **"웹 기동 + `packages/core` 타입 공유 +
  seed 적재 경로 증명"**. 앱을 안 만들었으므로.

## 참고 출처

- [2026-08 앱 껍데기 재검토](../research/2026-08_app-shell-reassessment.md) — 실측표·비교표·출처 URL 전체
- [ADR-009 네이티브 스택 및 모노레포 결정](009_stack-monorepo-decision.md)
- [ADR-010 콘텐츠 저작권 및 원문 격리](010_content-copyright-and-data-model.md)
