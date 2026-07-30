# ADR-009: 네이티브 스택 및 모노레포 결정 (RN/Expo + Next.js)

> Status: **Accepted** (2026-07-27)
> **Supersedes**: [ADR-001](../../../26-SenTalk-en-study-app/docs/adr/001_deployment-platform.md) (배포 플랫폼 + Flutter 전환) — P-01 결정 해소
> 근거 원자료: [docs/research/2026-07_native-stack-research.md](../research/2026-07_native-stack-research.md)
> 재구성 계획: [docs/project-review/21_rebuild-plan.md](../project-review/21_rebuild-plan.md)

## Context

ADR-001(2026-04)은 초기 MVP를 전제로 "WebView 래퍼 비권장, 스토어 출시는 Flutter 완전 재작성이 최적"이라 결론하고 결정을 보류(P-01)했다. 이후 출시 타당성 조사([ADR 20](../project-review/20_release-feasibility.md))와 사용자 결정으로 전제가 바뀌었다:

- MVP 단계를 넘어섰고, 학습자료·UI/UX까지 재설계하며 **새 프로젝트로 재구성**하기로 함.
- 목표는 개인 우선 → 공개 확장, 이후 네이티브(iOS·Android).
- 개발자는 React/TypeScript 숙련, Dart 미경험, 1인, AI 코딩 툴 적극 활용.

ADR-001이 검토하지 않은 두 축(RN/Expo 대안, 웹+앱 단일 코드베이스)을 2026-07 최신 정보로 재조사해 스택을 확정한다.

## Decision

1. **네이티브 스택 = React Native / Expo** (Flutter 배제)
2. **웹 = Next.js 유지** (Expo web / Flutter web 아님)
3. **구조 = pnpm + Turborepo 모노레포** — `create-t3-turbo` 기반, Next.js 웹 + Expo 앱, 공유 패키지(타입·zod·API 클라이언트·순수 로직). Solito 스킵.
4. **네이티브 착수 트리거 = TTS** — iOS 웹 Web Speech 한계가 실제 제약이 될 때. 그전엔 웹+PWA로 커버(한국 iOS PWA 정상 동작).

## 근거

### Flutter를 배제한 이유
- **웹 SEO 치명적**: HTML 렌더러 제거(3.29, 2025-02) 후 CanvasKit만 → 텍스트가 canvas에 픽셀로 그려져 크롤러가 빈 캔버스만 봄. 콘텐츠형 학습앱에 부적합. iOS는 WasmGC 미지원으로 느린 경로.
- **TS 자산 재사용 0**: Dart라 `ts-fsrs`·Drizzle·OpenAI TS 코드·타입을 전부 버려야 함. dart-fsrs(`fsrs` 2.0.1)는 13개월 정체.
- Dart 신규 학습 + AI 코딩 지원이 TS/React 대비 약하다는 통념(정량 근거는 미확인).
- 유일 우위(일부 네이티브 플러그인 성숙도)는 위 열세를 못 이김.

### RN/Expo를 선택한 이유
- TS·React 유지 → `ts-fsrs` 5.4.1(순수 JS, Hermes 그대로 동작)·Drizzle(expo-sqlite 공식 지원)·게이미피케이션·리뷰 로직·OpenAI 코드 재사용.
- 웹(Next.js)과 **언어·타입·비즈니스 로직 공유** 가능.
- State of RN 2025: New Architecture 80%, Expo Router 71% — 성숙·안정.
- 감수할 점: 온디바이스 STT 과도기(`@react-native-voice` 2026-01 아카이브 → 서버 STT로 우회), expo-speech 순차재생 안정화 필요.

### 웹을 Next.js로 유지하는 이유
- Expo web(SSR alpha, RSC→HTML 미지원)·Flutter web(canvas SEO)은 콘텐츠+SEO에서 Next.js 미달. Bluesky조차 RNW 웹에 커스텀 SSR을 따로 붙임.

### 모노레포인 이유
- 1인이 웹+앱 둘 다 낼 거면 정당. 단 **공유 경계는 좁게**(타입·zod·API·순수 로직만, UI는 웹/앱 2벌) — Tamagui 전면 도입 등 억지 공유는 과함. `create-t3-turbo`가 Better Auth·Drizzle·tRPC·NativeWind를 이미 세팅.

## 대안 비교

| 대안 | 결론 |
|---|---|
| Flutter 완전 재작성 (ADR-001 원안) | 배제 — 웹 SEO·TS 자산·학습곡선 |
| Expo universal 단일 코드베이스 | 부분 채택 안 함 — 웹 SEO·품질이 Next.js 미달(SSR alpha·RSC 미완) |
| Next.js 웹 + 손수 유지 2벌 네이티브(공유 없이) | 배제 — 1인에 drift·이중 QA 부담 |
| **Next.js 웹 + Expo 앱 모노레포(공유 스파인)** | **채택** |

## 결과 / 트레이드오프

- **얻는 것**: TS 단일 언어, 자산 재사용, 웹 SEO 유지, AI 코딩 생산성, 인증(Better Auth)·타입공유 재발명 회피.
- **감수**: UI는 웹/앱 2벌 작성, 모노레포 초기 설정(Metro·peerDependency 함정), 온디바이스 STT 과도기.
- **미룸**: 네이티브 앱은 TTS/스토어 노출이 실제 제약이 될 때 착수(웹 먼저).

## 참고 출처

- [네이티브 스택 리서치 아카이브](../research/2026-07_native-stack-research.md) — 전체 근거·출처 URL
- [출시 타당성 검토 (ADR 20)](../project-review/20_release-feasibility.md)
- [create-t3-turbo](https://github.com/t3-oss/create-t3-turbo) · [State of React Native 2025](https://results.stateofreactnative.com/en-US/) · [Expo monorepos](https://docs.expo.dev/guides/monorepos/)
