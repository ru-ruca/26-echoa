# 앱 껍데기 재검토 — 스택 실측과 선택지 비교 (2026-08)

> 조사일: 2026-08-07
> 계기: 모노레포 스캐폴딩 착수 시점에 [ADR-009](../adr/009_stack-monorepo-decision.md)의 전제 두 개가 깨진 것을 확인
> 결론: [ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md) — 웹 먼저, 앱 껍데기는 유예
> 성격: **학습·기술 자료**. 결정문이 아니라 결정을 뒷받침한 사실과 비교표를 남긴다.

---

## 1. 왜 다시 봤나 — 깨진 전제 두 개

### 1-1. `create-t3-turbo`가 8개월 정체

ADR-009 §Decision-3은 "`create-t3-turbo` 기반"을 결정했다. 근거는 "Better Auth·Drizzle·tRPC·NativeWind를
이미 세팅"해 준다는 점이었다. 그런데 착수 시점에 확인하니 **main 브랜치 마지막 커밋이 2025-12-12**로
8개월째 멈춰 있었다.

| 항목 | t3-turbo main (2025-12-12) | 2026-08-07 latest |
|---|---|---|
| next | 15 | **16.3.0** (2026-08-03, LTS) |
| react | 19.1.4 | **19.2.8** |
| expo | ~54.0.20 (RN 0.81) | **57.0.11** (SDK 57, 2026-06-30, RN 0.86) |
| better-auth | 1.4.0-beta.9 | **1.6.26** |
| @trpc/server | 11.7.1 | **11.18.0** |
| turbo | 2.5.8 | **2.10.8** |
| nativewind | 5.0.0-preview.2 | 4.2.6 stable / 5.0.0-preview.4 |

legacy(`26-SenTalk`)가 이미 **Next 16.2.3 · React 19.2.3 · Tailwind 4.2.2**였다.
스타터를 그대로 clone하면 **legacy보다 뒤로 가는** 스캐폴딩이 된다.

참고로 Expo SDK 54는 **Legacy Architecture를 지원하는 마지막 버전**이고 SDK 55부터
`newArchEnabled` 옵션 자체가 사라졌다. 8개월 전 스타터에서 시작하면 이 전환도 떠안는다.

### 1-2. "개발자는 Dart 미경험" 전제가 깨졌다

ADR-009 §Context L14는 "개발자는 React/TypeScript 숙련, **Dart 미경험**"을 전제로 Flutter를 배제했다.
그런데 회사 프로젝트 `26-krste-baeknyeongaye/bg-user-flutter`가 Flutter다.

다만 실물을 열어 보니 **Flutter UI 앱이 아니라 WebView 래퍼**였다:

- `lib/` 아래 Dart 파일이 **3개**(`main.dart` · `mok_verify_page.dart` · `config/env.dart`)
- `webview_flutter` + `flutter_inappwebview` + 네이티브 브리지
  (`biometric_signature` · `local_auth` · `geolocator` · `image_picker` · FCM)
- `android/app/build.gradle.kts`에 release signing 설정 완료

즉 보유 경험은 "Flutter UI 개발"이 아니라 **"웹 앱을 네이티브로 감싸고 스토어에 올리는 절차"**다.
이건 Flutter를 다시 검토할 근거는 못 되지만, **래퍼 방식 자체의 실현 가능성**에 대한 근거는 된다.

---

## 2. Echoa가 실제로 네이티브를 요구하는 것

비교의 축을 잡기 위해 먼저 확인한 것. Echoa에서 웹으로 안 되는 것은 **3개뿐**이다.

| 요구 | 웹만으로 되나 | 근거 |
|---|---|---|
| **TTS** | ✗ | iOS Safari는 `speechSynthesis.getVoices()`가 빈 배열을 반환해 목소리를 고를 수 없고, 백그라운드 진입 시 재생이 멈춘다. Safari 18도 언어별 voice 목록이 불안정하다. |
| **녹음** | △ | MediaRecorder는 되지만 iOS는 오디오 세션 제어가 제한적 |
| **AdMob** | ✗ | 웹은 AdSense, 앱은 AdMob — 수익 모델([D-23](../adr/000_decision-log.md))이 앱 광고 전제 |

나머지(4단계 아코디언 학습 흐름·FSRS 복습 큐·진도 통계)는 전부 웹으로 된다.
그래서 **진짜 축은 "네이티브를 얼마나 하느냐"가 아니라 "UI를 몇 벌 쓰느냐"**다.

플러그인 실측 (2026-08-07):

| 기능 | Expo | Capacitor |
|---|---|---|
| TTS | `expo-speech` 57.0.1 (큐 지원) | `@capacitor-community/text-to-speech` 8.0.2 (`queueStrategy` flush/add) |
| 녹음 | `expo-audio` 57.0.3 | `@capacitor-community/voice-recorder` |
| 광고 | `react-native-google-mobile-ads` 16.4.0 | `@capacitor-community/admob` 8.0.0 |

`@capacitor/core`는 8.5.0이고 2026-08-05에 갱신됐다 — 활발하다.

---

## 3. 선택지 5개 비교

| 축 | A. Next.js + Expo 모노레포<br>(ADR-009 원안) | B. Next.js + Capacitor 래퍼 | C. Next.js + Flutter WebView 래퍼 | D. Expo universal 단독 | E. Next.js + Flutter 앱 |
|---|---|---|---|---|---|
| **UI 벌수** | **2벌** (웹 React + 앱 RN) | **1벌** | **1벌** | 1벌 | 2벌 |
| **비즈니스 로직** | 1벌 (TS 공유) | 1벌 | 1벌 | 1벌 | **2벌** (TS + Dart) |
| legacy TS 로직 재사용 | ✓ | ✓ | ✓ | ✓ | ✗ Dart 재작성 |
| **웹 SEO** | ✓ Next.js | ✓ Next.js | ✓ Next.js | △ SSG는 됨, SSR은 SDK 55+ alpha | ✓ |
| 앱 품질 | **최상** | WebView | WebView | ✓ | 최상 |
| TTS·녹음·광고 | ✓ expo-* | ✓ plugin | ✓ Dart 브리지 직접 | ✓ | ✓ |
| **Apple 4.2.2 위험** | 없음 | **있음** | **있음** | 없음 | 없음 |
| 보유 경험 | React/TS ✓ | React/TS ✓ | React/TS + 회사 패턴 ✓ | React/TS ✓ | Dart UI ✗ |
| 학습 비용 | 중 | **낮음** | 낮음 | 중 | **높음** |
| 배포 | EAS Build/Submit (Xcode·Android Studio 불필요, OTA 무료 1,000 MAU) | 웹 배포 즉시 + 앱 재빌드 | 동일 | EAS | Codemagic 등 |

### 각 안의 진짜 비용

- **A의 비용은 UI 2벌**이다. [22 §9](../project-review/22_learning-design-spec.md) 화면 명세
  (홈·학습 4단계 아코디언·복습 큐·진도통계)를 웹과 앱에서 각각 구현하게 된다. 1인에겐 이게 가장 크다.
- **B·C의 비용은 Apple 4.2.2**다. 단순 웹 래핑("web clipping")은 명시적으로 금지되고, 통과하더라도
  다음 업데이트 심사에서 거부될 수 있다. 다만 **실질적인 네이티브 기능**(TTS·녹음·푸시)이 붙으면
  통과 사례가 일반적이고, Echoa는 그 기능들이 **부가가 아니라 핵심 기능**이라 명분이 있다.
- **C는 회사에서 이미 성공시킨 패턴**이지만, 브리지를 Dart로 직접 써야 한다. B(Capacitor)는 같은 일을
  JS API 호출로 한다 — 유지할 언어가 하나 줄어든다.
- **D**는 코드가 진짜 1벌이지만 Expo Router의 웹 SSR이 SDK 55+ alpha다. Echoa는 콘텐츠+SEO 앱이라
  Next.js를 포기하기 어렵다.
- **E**는 로직까지 2벌이라 1인에겐 최악. **ADR-009의 결론이 전제가 바뀐 뒤에도 유효하다.**

### 결정을 미룰 수 있다는 발견

`packages/{core,db,api}`는 **A·B·C·D 어느 쪽을 골라도 동일하게 필요하고 동일하게 쓰인다.**
지금 만들 것의 대부분이 껍데기 결정과 무관하다.

그리고 ADR-009 §Decision-4가 이미 **"네이티브 착수 트리거 = TTS"**로 정해 뒀다.
지금 껍데기를 고르는 것은 그 트리거를 앞당겨 당기는 셈이다. 웹 학습 흐름을 만들어
TTS 제약이 실제로 어떻게 나타나는지 본 뒤 고르는 편이 정보가 많다.

---

## 4. 참고 자료

### Flutter vs React Native (2026)

- 크로스플랫폼 점유율은 Flutter 46% / React Native 35%. 둘이 합쳐 80% 이상.
- 채용 공고는 React Native가 많다(LinkedIn 기준 6,413 vs 1,068).
- 솔로 개발자 관점의 통상적 권고: **이미 JS를 알면 React Native, 아니면 Flutter**.
- Flutter Web은 여전히 SEO에 부적합하다 — canvas 렌더링이라 크롤러가 시맨틱 HTML을 못 본다.
  `HTML-in-Canvas`(Chrome 신규 API)가 표준화되면 달라질 수 있으나 아직이다.
  → **ADR-009의 웹 SEO 근거는 2026-08 현재도 유효**하다.

### 출처

- [create-t3-turbo](https://github.com/t3-oss/create-t3-turbo) — main 커밋 이력·`pnpm-workspace.yaml` catalog 실측
- [Next.js 16.3 (2026-08-03)](https://nextjs.org/blog/next-16-3) · [Next.js 16 (LTS)](https://nextjs.org/blog/next-16)
- [Expo SDK 57 (2026-06-30)](https://expo.dev/changelog/sdk-57) · [SDK 56 (2026-05-21)](https://expo.dev/changelog/sdk-56) · [SDK 55](https://expo.dev/changelog/sdk-55)
- [React Native 0.82 — A New Era](https://reactnative.dev/blog/2025/10/08/react-native-0.82)
- [Expo — The solo dev playbook: EAS Build, Update, Submit](https://expo.dev/blog/building-a-cross-platform-app-without-touching-xcode-or-android-studio)
- [Better Auth — Database schema](https://www.better-auth.com/docs/concepts/database) · [Naver provider](https://www.better-auth.com/docs/authentication/naver)
- [Neon — Serverless driver (HTTP vs WebSocket)](https://neon.com/docs/serverless/serverless-driver) · [Drizzle + Neon](https://neon.com/docs/guides/drizzle)
- [Expo — Tailwind CSS 가이드](https://docs.expo.dev/guides/tailwind/) (NativeWind·Uniwind 병기, 공식 기본값 없음)
- [NativeWind 5.0 release plan](https://github.com/nativewind/nativewind/discussions/1818)
- [Median — Will Apple approve my webview app?](https://median.co/blog/will-apple-approve-my-webview-app) · [Mobiloud — App Store Review Guidelines: webview wrapper](https://www.mobiloud.com/blog/app-store-review-guidelines-webview-wrapper)
- [The State of Speech Synthesis in Safari](https://weboutloud.io/bulletin/speech_synthesis_in_safari/) · [PWA iOS Limitations (2026)](https://www.magicbell.com/blog/pwa-ios-limitations-safari-support-complete-guide)
- [Flutter Web & Desktop 2026: Production Readiness](https://softaims.com/blog/flutter-web-desktop-production-ready-2026)

이전 조사: [2026-07 네이티브 스택 리서치](2026-07_native-stack-research.md) · [출시 타당성](2026-07_release-feasibility-research.md)
