# SenTalk 네이티브 스택 리서치 아카이브 (Flutter vs RN/Expo, 웹+앱 구조)

> 이 문서는 2026-07-27 "네이티브 재구성 스택 결정"을 위한 웹 조사 **원자료 아카이브**다.
> 결정·권고는 [`docs/adr/009_stack-monorepo-decision.md`](../adr/009_stack-monorepo-decision.md)와 [`docs/project-review/21_rebuild-plan.md`](../project-review/21_rebuild-plan.md) 참고 — 이 문서는 그 근거다.
> **조사 방식**: 조사 에이전트 다수 병렬(S1 핵심기능 생태계, S2 트렌드·유지보수·AI, S3 웹+앱 단일코드베이스 — S3는 하위 4갈래로 세분). 2025~2026 최신·1차 출처 우선.
> **신뢰도 표기**: 각 조사자가 표기한 [1차]/[2차], (fetch)/(스니펫), "미확인"을 보존. 미확인은 사실로 취급하지 말 것.
> **조사일**: 2026-07-27. 버전·정책은 변동되므로 착수 직전 원문 재확인.

---

## 1. 핵심 기능 생태계 (SenTalk 기능별 Flutter vs RN/Expo)

기준 기능: FSRS 간격반복, TTS(속도·순차재생), 마이크 녹음+재생, STT, 로컬 DB/오프라인, 로컬 알림. 개발자 = React/TS 숙련, Dart 미경험.

| 기능 | Flutter | RN/Expo | 우열 |
|---|---|---|---|
| **FSRS** | `fsrs`(dart-fsrs) 2.0.1, **13개월 정체**, 22 likes, unverified 업로더 | **`ts-fsrs` 5.4.1**(2026-05, 726★, 의존성 0, 순수 JS→Hermes 그대로 동작). **웹앱이 이미 쓰는 lib라 재작성 0** | **RN 압도** |
| **TTS** | `flutter_tts` 4.2.5, `awaitSpeakCompletion`으로 순차재생 안정 + iOS 오디오세션 제어 | `expo-speech`, onDone 체이닝 가능하나 웹/iOS/Android onDone·pause 버그 이력 | Flutter 근소 우위 |
| **녹음+재생+파형** | 코어 `record`(dBFS) 충분 + **파형 UI `audio_waveforms` 단일 성숙** | `expo-audio`(metering+PCM) 코어 충분, 파형 위젯은 Expo Go 불가·dev build 필요 | Flutter 근소 우위 |
| **STT(온디바이스)** | `speech_to_text` 단일 성숙 | **`@react-native-voice/voice` 2026-01 아카이브** → 후속 `expo-speech-recognition`(Android13+/iOS17+) 과도기 | Flutter 우위 |
| **STT(서버, OpenAI)** | HTTP 전송 | HTTP 전송 | 동일 |
| **로컬 DB/오프라인** | `drift`(완성도 최상, Dart 학습 필요), `isar`(정체) | **`expo-sqlite`+Drizzle 공식 지원 → 기존 Drizzle 스키마 재사용**(단 Drizzle×expo RC, pg→sqlite 방언 일부 이식) | RN 우위(자산 재사용) |
| **로컬 알림** | `flutter_local_notifications` | `expo-notifications` | 동일 |

**S1 총평**: 네이티브 플러그인 성숙도 **자체**는 Flutter가 근소 우위(TTS 순차재생·파형·온디바이스 STT). 그러나 React/TS 숙련·Dart 미경험 1인 개발자에겐 **RN/Expo가 총 마찰 최소** — ts-fsrs·Drizzle·OpenAI/TS 코드와 언어를 통째로 재사용. 감수할 곳: expo-speech 순차재생 안정화, 온디바이스 STT 과도기(또는 서버 STT), 일부 dev build 필요.

---

## 2. 트렌드 · 유지보수 · AI 코딩 지원

> **한계 명시**: 이 축의 "AI 코딩 어시스턴트 지원 품질" 직접 조사는 이번에 완결하지 못했다(조사 에이전트가 실행 대신 계획만 반환). 채택률·유지보수는 다른 조사(§3 하위)에서 확보한 State of RN 2025 등으로 보강. **AI 지원 품질은 아래를 "통념 수준"으로만 취급하고, 결정의 유일 근거로 쓰지 말 것.**

**채택률·트렌드(확보분)**
- State of React Native 2025 설문(2025-12-09~2026-01-08, 3,501명): RN 45% / **Expo 41%**(거의 동률), **Expo Router 71%**, **New Architecture 80% 채택**, Reanimated 93%, NativeWind 42%. [results.stateofreactnative.com](https://results.stateofreactnative.com/en-US/) — 1차 설문.
- New Architecture는 RN 0.82(2025-10)부터 유일·비활성화 불가, legacy는 2025-06 동결. Expo가 공식 권장 시작점("bare vs Expo 논쟁 종료"). [docs.expo.dev/guides/new-architecture](https://docs.expo.dev/guides/new-architecture/) — 1차.
- Flutter 최신 stable 3.44(2026-05~07). 2026 로드맵의 유일한 웹 공약은 "WebAssembly를 기본으로". [blog.flutter.dev 2026 로드맵](https://blog.flutter.dev/flutter-darts-2026-roadmap-89378f17ebbd) — 1차, 2026-02.

**유지보수 방향(확보분)**
- RNW(react-native-web)는 "maintenance-only phase, 주요 신기능 없음"이며 Meta 방향은 **React Strict DOM**으로 이동 중(RN 호환은 WIP). [swmansion.com 2026 예측](https://swmansion.com/blog/react-native-in-2026-trends-our-predictions-463a837420c7) — 2차(RN 코어 기여사, 신뢰 높음), 2026-01.

**AI 코딩 지원(미확보 — 통념)**
- TS/React가 학습 데이터가 훨씬 많아 LLM 코딩 지원이 강하다는 것은 널리 통용되는 통념이나, 이번 조사에서 **Flutter/Dart 대비 정량 비교나 2025~2026 개발자 후기를 직접 확보하지 못함(미확인)**. SenTalk 결정에서 이 항목은 방향성 참고로만 사용.

**Stack Overflow 2025 사용률**: RN 14.51% vs Flutter 13.55%라는 2차 인용이 있으나 원본(survey.stackoverflow.co) 직접 확인 실패 — 미확인.

---

## 3. 웹 + 앱 구조 (단일 코드베이스 vs 분리)

### 3.1 Expo + react-native-web (웹+iOS+Android 단일)
- Static rendering(SSG, 빌드타임 HTML)은 프로덕션 가능·SEO 크롤 가능, 그러나 **SSR은 alpha(SDK 55+), RSC는 preview(SDK 56)이고 "RSC→HTML 렌더링은 아직 미지원"**. [docs.expo.dev/router/server-rendering](https://docs.expo.dev/router/server-rendering), [docs.expo.dev/guides/server-components](https://docs.expo.dev/guides/server-components/) — 1차, 2026-06.
- SDK 56(2026 중반) 스트리밍 SSR + `generateMetadata`(라우트별 SEO) 추가, Expo Router를 React Navigation에서 분리. [dev.to/expo](https://dev.to/expo/expo-router-v56-ships-ssr-and-breaks-free-from-react-navigation-4pfb) — Expo 작성, 2026-06.
- RNW는 React DOM 대비 ~30~40KB gzipped 추가(단일 출처, 정밀 수치는 미확인). 기본 클라이언트 렌더 → 동적 페이지 SEO는 SSR 레이어 필요. `View`→`div`·`Text`→`span`이라 **시맨틱 HTML/접근성은 별도 노력**.
- **프로덕션 증거**: Bluesky(bsky.app)가 최대 RNW 웹 사례. 단 Expo Router 웹 SSR을 안 쓰고 **자체 Go 웹서비스(bskyweb) + OG 카드 서버**를 따로 구축 — SEO가 필요한 콘텐츠 앱엔 시사적. [github.com/bluesky-social/social-app](https://github.com/bluesky-social/social-app) — 1차.
- 실무 컨센서스: "모바일이 주고 웹이 보조면 RNW+Expo, **웹 우선이면 Next.js + 별도 RN 앱**". [reactnativerelay.com](https://reactnativerelay.com/article/react-native-web-expo-cross-platform-2026) — 2차, 2026-06.
- **`expo-speech`는 진짜 유니버설**: Android/iOS/Web 동일 API(웹은 Web Speech 백엔드), speak/stop/pause/resume/getAvailableVoicesAsync 웹 동작. 단 pause/resume은 Android 미지원, 음성 객체 필드가 플랫폼별 상이. [docs.expo.dev/versions/latest/sdk/speech](https://docs.expo.dev/versions/latest/sdk/speech/) — 1차.

### 3.2 Flutter Web
- **HTML 렌더러 제거됨**(3.24 deprecated → **3.29 제거, 2025-02**). CanvasKit이 유일 렌더러 → "가벼운 DOM 옵션"이 더는 없음. [docs.flutter.dev 3.29 릴리스노트](https://docs.flutter.dev/release/release-notes/release-notes-3.29.0) — 1차.
- **WASM(Skwasm)은 아직 opt-in**(`--wasm`), ~1.1MB. **WasmGC는 Chromium 119+만, iOS 전 브라우저(WebKit)는 미지원** → iOS는 조용히 JS/CanvasKit 경로. [docs.flutter.dev/platform-integration/web/wasm](https://docs.flutter.dev/platform-integration/web/wasm) — 1차, 2026-07.
- **SEO 치명적**: CanvasKit은 텍스트를 canvas에 픽셀로 그림 → **크롤러는 빈 canvas만 봄**(읽을 텍스트·링크·인덱스 콘텐츠 0). 네이티브 SSR·메타태그·사이트맵 없음, SEO 기능요청(#171598)은 2025-07 장기 이슈 중복으로 종료. [github.com/flutter/flutter#171598](https://github.com/flutter/flutter/issues/171598) — 1차.
- CanvasKit ~1.5~2MB(첫 페인트 전 고정 비용). 텍스트 선택·복사는 웹에서 2026 현재도 버그 상존(#184232 2026-03-27 등). 접근성은 별도 semantics 트리 opt-in. [docs.flutter.dev/ui/accessibility/web-accessibility](https://docs.flutter.dev/ui/accessibility/web-accessibility) — 1차, 2026-05.
- `flutter_tts` 4.2.5는 Web+Android+iOS 지원(웹은 Web Speech). [pub.dev/packages/flutter_tts](https://pub.dev/packages/flutter_tts) — 1차.
- 실무 verdict: Flutter Web은 **로그인 뒤 앱형 화면(대시보드·툴)엔 프로덕션 가능, SEO 의존 공개 사이트엔 부적합**. 명명된 Flutter 프로덕션(Google Pay India, Nubank 등)은 대부분 모바일/임베디드. [softaims.com](https://softaims.com/blog/flutter-web-desktop-production-ready-2026) — 2차.

### 3.3 모노레포 (Next.js 웹 + Expo 앱)
- Expo 공식 모노레포 문서 최신(2026-06-30), Metro 모노레포 해석 내장. Vercel 공식 Turborepo+RN 템플릿 존재. [docs.expo.dev/guides/monorepos](https://docs.expo.dev/guides/monorepos/) — 1차.
- **`create-t3-turbo`**(5,600★+) — Next.js+Expo 모노레포 최다 스타 스타터. 2025~2026 스택: Next.js 15·React 19·Expo SDK 54·tRPC v11·**Better Auth(NextAuth 대체)·Drizzle(Prisma 대체)**·Tailwind v4+NativeWind v5. [github.com/t3-oss/create-t3-turbo](https://github.com/t3-oss/create-t3-turbo) — 1차.
- **공유 경계**: 60~80% 공유 가능(비즈니스 로직·순수 함수·훅·API 호출·상태·**Zod 스키마·TS 타입·tRPC 라우터+클라이언트**). **UI는 공유 불가**(DOM+CSS vs RN 프리미티브+StyleSheet) — Tamagui/RNW 도입 없이는 "UI 2벌". [techoral.com](https://techoral.com/react/react-native-sharing.html) — 2차.
- **Solito는 스킵 권장**: 마지막 커밋 2026-01, 릴리스 ~2~3/년, 1인 메인테이너(느려지는 중). Expo Router가 웹까지 커버해 대부분 프로젝트가 Solito 생략. [github.com/nandorojo/solito](https://github.com/nandorojo/solito)(GitHub API) — 1차.
- **1인 개발자 판단**: 웹+앱 둘 다 낼 거면 모노레포 정당(단 native 앱이 실제로 나올 때만 이득). 이미 Next.js에 투자했고 native를 추가하려는 SenTalk이 정확히 이 케이스. 함정(Metro watchFolders, 중복 React "Invalid hook call" → react를 peerDependency로, pnpm hoisting)은 대부분 SDK 55 자동 지원으로 완화.

### 3.4 PWA vs Native (한국 시장)
- **한국(비EU)은 iOS PWA 정상**: iOS 16.4+(2023-03)부터 홈스크린 설치 PWA는 Web Push 가능(2026 초 iPhone 95%+ iOS 16+). EU DMA의 "iOS PWA 파손" 담론은 EU 한정이라 한국엔 무관. [magicbell 2026](https://www.magicbell.com/blog/pwa-ios-limitations-safari-support-complete-guide) — 2차.
- 단 iOS PWA 제약: 설치 프롬프트 없음(수동 안내), ~50MB 캐시 캡·7일 미사용 시 저장소 eviction, 백그라운드 실행 불가.
- **TTS가 결정적 약점**: iOS 웹 Web Speech는 `getVoices()` 빈 배열(음성 선택 불가), speak()는 사용자 제스처 필요(자동 재생 불가), 백그라운드/잠금 시 중단. 네이티브 TTS(expo-speech/flutter_tts)가 음성 제어·오프라인·백그라운드 오디오 해결. 단 네이티브도 iOS는 고품질 "super-compact" 음성을 명시 지정하고 언어를 pin해야 함. [weboutloud](https://weboutloud.io/bulletin/speech_synthesis_in_safari/) — 2차.
- 스토어: Play는 TWA로 저렴 진입, **Apple은 Capacitor 래퍼 필요 + 4.2.2 리젝 리스크**(네이티브 기능 실제 추가 필요).
- 대형 언어앱 선례: **Duolingo = Swift/네이티브 Android + Kotlin Multiplatform(로직 공유, UI는 네이티브)**, Babbel = 웹 ReactJS + 모바일 네이티브(일부 RN). 순수 크로스플랫폼 UI가 아님. [duolingoguides](https://duolingoguides.com/does-duolingo-use-react-native/), [developer.android.com/stories Duolingo](https://developer.android.com/stories/apps/duolingo-excellence) — 2차.

### 3.5 하이브리드 vs 단일 코드베이스 (1인)
- **2벌 프론트(Next.js 웹 + 별도 네이티브) 하이브리드를 손으로 유지하는 것이 1인에겐 가장 비현실적**이라는 게 2025~2026 실무 컨센서스 — 중복이 구조적 drift·이중 QA·이중 버그세를 낳음("full-stack fatigue"). [pavan-kumar 분석](https://pavan-kumar-appannagari.github.io/posts/feature-parity-architectural-not-testing/) — 2차.
- 그러나 콘텐츠 앱은 SEO 때문에 Next.js 웹이 유리 → **절충: Next.js 웹 유지 + Expo 네이티브, 둘 다 TS + 공유 타입 스파인(zod/tRPC)**. Flutter는 TS 타입 공유 0이라 이 절충의 최악 궁합.
- 저비용 임시 다리: **Capacitor로 기존 PWA를 스토어 셸로 래핑**("몇 분") — camera/push/geolocation 획득, 진짜 네이티브는 TTS/UX가 실제 제약될 때. iOS push/background는 여전히 부분적. [without.systems](https://without.systems/progressive-web-to-native-mobile-with-capacitor) — 2차.
- 웹 먼저 근거: 웹은 ~2~4개월(네이티브 5~10개월), 즉시 배포(스토어 심사 없음), "web 시작 후 native 업그레이드가 native 먼저보다 훨씬 저렴". [brainhub](https://brainhub.eu/library/app-vs-website-which-to-develop-first) — 2차.

---

## 4. 종합 판단 (SenTalk 관점)

1. **스택 = RN/Expo**: Flutter의 유일 우위(일부 네이티브 플러그인)는 (a)웹 SEO 치명적 (b)TS 백엔드 타입 공유 0 (c)ts-fsrs·Drizzle 재사용 불가 (d)Dart 학습 (e)AI 코딩 지원 통념상 약세를 못 이김. SenTalk은 콘텐츠+TS 자산이 핵심이라 RN/Expo가 정합.
2. **웹 = Next.js 유지**: Expo web(SSR alpha·RSC 미완)·Flutter web(canvas SEO 치명적) 둘 다 콘텐츠+SEO엔 Next.js 미달.
3. **구조 = 모노레포**: create-t3-turbo 기반, 공유 경계 좁게(타입·zod·API·순수 로직), UI 2벌. Solito 스킵.
4. **네이티브 전환 트리거 = TTS**: iOS 웹 Web Speech 한계가 실제 제약이 될 때 Expo 앱. 그전엔 웹+PWA(한국 iOS 정상)로 커버.

---

## 5. 미확인 항목

- **AI 코딩 어시스턴트의 Flutter/Dart vs RN/TS 지원 품질 정량 비교·2025~2026 후기** — 직접 확보 못함(통념 수준만).
- Stack Overflow 2025 RN vs Flutter 사용률 원본 수치(2차 인용만).
- RNW의 React DOM 대비 정확한 번들 증가량(단일 출처 ~30~40KB).
- Expo brownfield→단일 앱 통합 사례의 기간·재사용률(Expo 벤더 블로그, fetch 실패).
- Drizzle×expo-sqlite의 프로덕션 안정성(RC 단계).
- 한국 개발자 커뮤니티/채용 시장의 Flutter vs RN 선호 최신 수치(부분만).
