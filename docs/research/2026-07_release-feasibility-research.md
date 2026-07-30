# SenTalk 앱 출시 타당성 리서치 아카이브

> 이 문서는 2026-07-22 앱 출시 타당성 조사의 **원자료(raw findings) 전체**를 보존하는 아카이브다.
> 종합 판단·비교표·권고안·결정 필요 사항은 SSOT 문서 [`docs/project-review/20_release-feasibility.md`](../project-review/20_release-feasibility.md)를 참고 — 이 문서는 그 근거 자료이며, 이 조사가 1회성으로 끝나지 않고 다른 세션에서도 그대로 재사용·재검증할 수 있도록 세부 사실·수치·출처 URL을 생략 없이 남기는 것이 목적이다.
>
> **조사 방식**: WebSearch/WebFetch 기반 에이전트 13개 실행 (R1 출시 경로 옵션 — 하위 5개 병렬 조사, R2 스토어 등록 실무, R3 서버·인프라·성능, R4 보안·개인정보·법규, R5 수익성·시장 벤치마킹 — 하위 5개 병렬 조사). 2025~2026 최신 정보·1차 출처(공식 문서·정책 페이지) 우선.
> **신뢰도 표기**: 각 조사자가 원문에 표기한 [1차]/[2차], (fetch = 원문 직접 확인) / (스니펫 = 검색 요약만 확인)를 그대로 보존했다. "미확인"으로 명시된 항목은 사실로 취급하지 말 것.
> **조사일**: 2026-07-22. 이후 정책·가격·버전은 변동될 수 있으므로, 실제 의사결정 직전에는 원문 URL을 재확인할 것.

---

## 목차

1. [출시 경로 옵션](#1-출시-경로-옵션)
   1.1 [순수 웹 PWA 배포 (스토어 없이)](#11-순수-웹-pwa-배포-스토어-없이)
   1.2 [PWA → TWA → Google Play](#12-pwa--twa--google-play)
   1.3 [iOS App Store (PWA/웹뷰 경로)](#13-ios-app-store-pwa웹뷰-경로)
   1.4 [Capacitor](#14-capacitor)
   1.5 [React Native/Expo vs Flutter 재작성](#15-react-nativeexpo-vs-flutter-재작성)
2. [스토어 등록 실무 (Google Play · Apple)](#2-스토어-등록-실무-google-play--apple)
3. [서버·인프라·성능](#3-서버인프라성능)
4. [보안·개인정보·법규](#4-보안개인정보법규)
5. [수익성·시장 벤치마킹](#5-수익성시장-벤치마킹)
   5.1 [광고 수익 (AdMob 한국 eCPM)](#51-광고-수익-admob-한국-ecpm)
   5.2 [1인/인디 개발자 수익 사례](#52-1인인디-개발자-수익-사례)
   5.3 [구독 벤치마크 · 결제 인프라 · 스토어 수수료 정책](#53-구독-벤치마크--결제-인프라--스토어-수수료-정책)
   5.4 [한국 영어 학습 앱 벤치마킹](#54-한국-영어-학습-앱-벤치마킹)
   5.5 [시장 트렌드 · 비수익 가치](#55-시장-트렌드--비수익-가치)
6. [미확인 항목 종합](#6-미확인-항목-종합)

---

## 1. 출시 경로 옵션

### 1.1 순수 웹 PWA 배포 (스토어 없이)

**iOS Safari PWA 기능 상태 (2026-07 기준)**

- 안정판 iOS 26/Safari 26.x (iOS 26 = 2025-09-15 출시). WWDC26(2026-06)에서 Safari 27 beta 발표(가을 정식 출시 예상). [webkit.org/blog/17333](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/), [webkit.org/blog/17967](https://webkit.org/blog/17967/news-from-wwdc26-webkit-in-safari-27-beta/) — 1차, 직접 fetch.
- **Web Push**: iOS/iPadOS 16.4(2023-02)부터 지원하되 **홈스크린에 추가된 웹앱만** 가능. 2026년 현재도 이 요건은 유지(Safari 26.0·27 beta 노트에 변경 없음 확인). [webkit.org/blog/13878](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) — 1차, 직접 fetch.
- **iOS 26이 전환점**: "홈스크린에 추가한 모든 웹사이트가 기본으로 웹앱(standalone)으로 열림" — "there are now zero requirements for 'installability' in Safari". manifest·meta 태그 없어도 됨. [webkit.org/blog/17333](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) — 1차, 직접 fetch.
- **Storage eviction(7일 캡)**: 원문은 [webkit.org/blog/10218](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/)(2020-03-24) — "Safari 사용 7일" 미상호작용 시 IndexedDB·LocalStorage 등 삭제. **단 홈스크린 웹앱은 예외**: "Web applications added to the home screen are not part of Safari and thus have their own counter of days of use" + "We do not expect... to have its website data deleted." 이 정책을 뒤집는 후속 발표 없음(18.4·26.0·27 노트 확인). 쿼터는 브라우저 앱 전체 디스크 최대 ~60%, `navigator.storage.persist()` 병행 권장. — 1차, 직접 fetch.
- **백그라운드 동작 불가**: Background Sync API를 Safari(데스크톱·iOS 전부, 26.5까지)·Firefox 미지원, Chrome/Edge만 지원(글로벌 77.48%). [caniuse.com/background-sync](https://caniuse.com/background-sync) — 1차, 직접 fetch.
- **`beforeinstallprompt` 미지원**(iOS·Firefox) — 설치 유도 UX는 "공유 시트 → 홈 화면에 추가" 수동 안내만 가능. [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event) — 1차, 직접 fetch.
- **서드파티 브라우저에서도 홈스크린 추가 가능(iOS 16.4+)** — 어느 브라우저로 추가했든 실행은 WebKit 기반 웹앱 컨테이너. web.dev의 "iOS는 Safari만 설치 가능" 서술은 WebKit 1차 문서와 상충 — WebKit 쪽이 정확. [webkit.org/blog/13878](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) — 1차, 직접 fetch.
- **EU/DMA**: Apple이 iOS 17.4에서 EU 내 홈스크린 웹앱 제거를 시도했다가 2024-03-01 철회. "we will continue to offer... Home Screen web apps continue to be built directly on WebKit." 대체 엔진(비-WebKit)은 EU·일본에서 entitlement 신청 가능하나 홈스크린 웹앱은 전 세계 어디서든 WebKit 전용 유지. [developer.apple.com/support/dma-and-apps-in-the-eu](https://developer.apple.com/support/dma-and-apps-in-the-eu/) — 1차, 직접 fetch.
- **Android/Chrome PWA 설치 기준(현행)**: HTTPS + manifest(name/short_name, 192·512px 아이콘, start_url, display) + engagement 휴리스틱(상호작용 1회+30초 체류). **서비스워커·오프라인은 요구 목록에 없음.** [web.dev/articles/install-criteria](https://web.dev/articles/install-criteria) — 1차, 직접 fetch. Richer install UI(screenshots 필드)로 "일부 PWA 설치율 2배" — [developer.chrome.com/blog/richer-pwa-installation](https://developer.chrome.com/blog/richer-pwa-installation) — 1차(벤더 공식).

**Web Speech `speechSynthesis` 지원 현황**

- 글로벌 지원 95.03%(caniuse, 2026-06 데이터). Chrome/Edge/Firefox/Safari 데스크톱·iOS 전부 지원. [caniuse.com/speech-synthesis](https://caniuse.com/speech-synthesis) — 1차, 직접 fetch.
- **Chrome 71부터 사용자 활성화(제스처) 없는 `speak()` 제거** — 자동재생 정책 위반 남용 방지 목적. 첫 재생은 반드시 사용자 제스처 이후. [chromestatus.com/feature/5687444770914304](https://chromestatus.com/feature/5687444770914304) — 1차, 직접 fetch.
- iOS 실무 이슈(2차): `getVoices()` 빈 배열/음성 목록 누락 보고(iOS 16, Safari 18), 발화 중 백그라운드 전환·화면 잠금 시 중단되고 재시작 전까지 복구 안 되는 문제. [weboutloud.io](https://weboutloud.io/bulletin/speech_synthesis_in_safari/) — 2차.
- 미확인: iOS Safari `speak()`의 사용자 제스처 요구가 Chrome처럼 공식 문서화됐는지 — 확인 못함.

**수수료 비교 (스토어 vs 웹 결제)**

- Apple 표준 30%, Small Business Program 15%(전년 $1M 이하). [apple.com/newsroom/2020-11-18](https://www.apple.com/newsroom/2020/11/apple-announces-app-store-small-business-program/) — 1차.
- Google Play 기본 $1M까지 15%, 2026-06-30부터 EEA·UK·US 자동갱신구독 "10%+5% 빌링수수료"로 개편. [support.google.com/googleplay/answer/112622](https://support.google.com/googleplay/android-developer/answer/112622) — 1차, 직접 fetch(2026년 개편 반영 최신본).
- Stripe 표준(미국) 2.9%+30¢, 국제카드 +1.5%, 환전 +1%. [stripe.com/pricing](https://stripe.com/pricing) — 1차.
- **결론**: 동일 매출 기준 결제 수수료는 웹 ~3~4% vs 스토어 15~30%. 대신 스토어 발견성·자동 설치 프롬프트 포기, iOS 설치 전환율의 공신력 있는 수치는 미확인(마케팅 블로그 추정치뿐 — 신뢰 낮음).

---

### 1.2 PWA → TWA → Google Play

**도구 유지보수 상태**

- **Bubblewrap**: `archived:false`, 마지막 push 2026-06-22, 최신 릴리스 v1.24.1(2025-09-29 이후 신규 릴리스 없음) — "유지 모드"로 판단. [github.com/GoogleChromeLabs/bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) (GitHub API 직접 fetch로 확인). chromeos.dev 공식 가이드가 여전히 Bubblewrap을 표준 경로로 안내. [chromeos.dev/en/publish/pwa-in-play](https://chromeos.dev/en/publish/pwa-in-play) — 1차.
- **PWABuilder**: 메인 저장소 활발(2026-07-22 당일 push 있음). Android 패키징 전용 저장소(`pwabuilder-google-play`)는 2025-10-06 아카이브됐으나 "중단이 아니라 메인 모노레포로 통합"이라는 공지 확인. 내부적으로 **Bubblewrap을 그대로 사용**("We utilize Google's Bubblewrap to generate and sign..."). [github.com/pwa-builder/PWABuilder](https://github.com/pwa-builder/PWABuilder) — 1차, 직접 fetch.

**Digital Asset Links (DAL) 요건**

- `/.well-known/assetlinks.json`을 도메인 루트에 둬야 함(다른 경로 무효). [developers.google.com/digital-asset-links](https://developers.google.com/digital-asset-links/v1/getting-started) — 1차, 직접 fetch(스펙 문서 최종 업데이트 2025-08-28로 현행 확인).
- Chrome 86+부터 DAL 검증 실패·오프라인 시 HTTP 200 미반환·404/5xx 응답은 **앱 크래시로 처리**. [web.dev/articles/using-a-pwa-in-your-android-app](https://web.dev/articles/using-a-pwa-in-your-android-app) — 1차, 직접 fetch.

**Play 정책 — "Lighthouse 80점" 요건은 현재 없음**

- 현행 공식 가이드 2곳(web.dev, chromeos.dev) 모두 Lighthouse 점수 요건 언급 없음. 현행 기준은 "PWA installability criteria 충족"뿐. Lighthouse 12.0(2024-04-22)에서 PWA 카테고리 자체가 도구에서 제거됨. [github.com/GoogleChrome/lighthouse/issues/15535](https://github.com/GoogleChrome/lighthouse/issues/15535) — 1차(저장소), 스니펫.
- **Spam 정책 webview 조항 원문**: "We don't allow apps whose primary purpose is to drive affiliate traffic to a website **or provide a webview of a website without permission from the website owner**." [support.google.com/googleplay/answer/9899034](https://support.google.com/googleplay/android-developer/answer/9899034) — 1차, 직접 fetch.
- **Minimum Functionality 원문**: "Apps should provide a stable, responsive, and engaging user experience" — 위반 예시는 정적 텍스트/PDF 뷰어, 콘텐츠 매우 빈약한 앱. [support.google.com/googleplay/answer/9898783](https://support.google.com/googleplay/android-developer/answer/9898783) — 1차, 직접 fetch.
- **해석**: TWA라는 기술 자체를 금지하는 조항은 없음. 걸리는 건 (a) 남의 사이트 무단 래핑/제휴 트래픽 목적, (b) 자기 사이트라도 콘텐츠 빈약. **자기 소유 도메인 + 실질 기능이 있으면 정책상 허용.**

**개인 개발자 계정 등록 (2026-07 현행)**

- 등록비 $25 1회. 본인 명의 신분증+신용카드 필요, 개인은 D-U-N-S 불필요. [support.google.com/googleplay/answer/6112435](https://support.google.com/googleplay/android-developer/answer/6112435) — 1차, 직접 fetch.
- **신규 개인 계정(2023-11-13 이후 생성) 비공개 테스트 요건**: 테스터 **12명이 14일 연속 opt-in**해야 프로덕션 신청 가능(2024-12-11에 20명→12명으로 완화, 이게 2026-07 현재도 현행). [support.google.com/googleplay/answer/14151465](https://support.google.com/googleplay/android-developer/answer/14151465) — 1차, 직접 fetch.

**승인·리젝 실사례**

- **승인 사례(2025-01-30)**: Next.js 웹앱을 PWABuilder로 TWA 패키징 → Google Play 게시 성공(`com.toffeemoney.twa`). 12명/14일 비공개 테스트 실제로 거침. [dev.to/amzamani](https://dev.to/amzamani/how-to-publish-a-nextjs-web-app-to-the-play-store-a-step-by-step-guide-347e) — 2차, 직접 fetch.
- 리젝 유형(2026-02-24 상업 블로그): webview형 앱 리젝 1순위 = Webviews/Affiliate Spam(무단 래핑), 2순위 = Minimum Functionality. 통과 요령 = 네이티브 기능 2~3개(푸시·오프라인 폴백 등) 추가 + AAB + target API 35. [code2native.com](https://code2native.com/blog/webview-app-google-play-approval-2026) — 2차, 직접 fetch.
- 미확인: "DAL 정상인 자기 소유 TWA"가 그 이유만으로 리젝된 2024~2026 사례 — 발견 못함(리젝 사례는 전부 "타인 사이트 래핑/콘텐츠 빈약"으로 수렴).

---

### 1.3 iOS App Store (PWA/웹뷰 경로)

**App Review Guidelines 현행 원문**

- **4.2 (Minimum Functionality)**: "Your app should include features, content, and UI that elevate it beyond a repackaged website. If your app is not particularly useful, unique, or 'app-like,' it doesn't belong on the App Store." [developer.apple.com/app-store/review/guidelines](https://developer.apple.com/app-store/review/guidelines/) — 1차, 직접 fetch.
- **4.2.2**: "apps shouldn't primarily be marketing materials, advertisements, web clippings, content aggregators, or a collection of links." — 1차, 직접 fetch.
- **4.2.4·4.2.5는 2024-01-25 개정에서 삭제됨(Intentionally omitted)**. 4.2.6은 "커머셜 템플릿/앱 생성 서비스로 만든 앱은 콘텐츠 소유자 본인이 직접 제출하지 않으면 리젝" — PWABuilder류 도구도 본인 제출이면 이 조항 자체는 회피 가능하다는 해석 근거. — 1차, 직접 fetch.
- **4.7 (HTML5/JS 미니앱)**: "Apps may offer certain software that is not embedded in the binary, specifically HTML5 and JavaScript mini apps and mini games, streaming games, chatbots, and plug-ins..." + 4.7.2(사전 허가 없이 네이티브 API 노출 금지)·4.7.5(연령 확인 의무). — **4.7은 "앱 안에서 배포하는 미니앱"용 조항이지, 앱 자체가 웹뷰 래퍼인 경우를 허용하는 면죄부가 아님.** — 1차, 직접 fetch.
- **2.5.6 (WebKit 의무)**: "Apps that browse the web must use the appropriate WebKit framework and WebKit JavaScript. You may apply for an entitlement to use an alternative web browser engine... for the EU and Japan." 대체 엔진 entitlement는 **EU·일본**만(한국 미포함, 일본 추가 시점 미확인). — 1차, 직접 fetch.
- **가이드라인 변경 이력**(재검증용, 전부 [developer.apple.com/news](https://developer.apple.com/news/) 1차): 2024-01-25 4.7 신설급 개편 + 2.5.6 EU 대체 엔진 링크 추가 + 4.2.4·4.2.5 삭제([id=7j1f99yf](https://developer.apple.com/news/?id=7j1f99yf)) · 2025-11-13 4.7 강화(HTML5/JS 미니앱 scope 명확화, 웹앱 관련 2025~2026 중 가장 실질적, [id=ey6d8onl](https://developer.apple.com/news/?id=ey6d8onl)) · 2026-02-06 1.2 익명 채팅 UGC(웹앱 무관, [id=d75yllv4](https://developer.apple.com/news/?id=d75yllv4)) · 2026-06-08 AI·안전 중심(웹앱/미니앱/브라우저 엔진 변경 없음, [id=a233fmpw](https://developer.apple.com/news/?id=a233fmpw)). 가이드라인 페이지 자체엔 최종 개정일 표기 없음.

**PWABuilder iOS 패키징 — 실험적, 승인 비보장**

- 공식 문서: "Packaging PWAs for iOS is **Experimental**. ...acceptance into Apple's App Store depends only on UI/UX of your PWA and usage of native capabilities." [docs.pwabuilder.com](https://docs.pwabuilder.com/#/builder/app-store) — 1차, 직접 fetch.
- 공식 블로그: "PWABuilder doesn't guarantee that your app will be accepted into Apple's App Store." 산출물은 "native Swift app with a WebKit web view(WKWebView)". [blog.pwabuilder.com](https://blog.pwabuilder.com/posts/publish-your-pwa-to-the-ios-app-store/) — 1차.
- **iOS 패키징 저장소는 2025-09-11 아카이브(read-only)** — 플랫폼별 코드는 유지보수 축소 상태. [github.com/pwa-builder/pwabuilder-ios](https://github.com/pwa-builder/pwabuilder-ios) — 1차, 직접 fetch.
- 2024~2026년 "PWABuilder 산출물이 실제로 승인됐다"는 구체적 공개 후기는 확보 못함(미확인). 반대로 2024-08 Discourse 사례는 패키징 단계 자체에서 오류(415/500)로 실패.

**웹뷰 래퍼 심사 경향 (2024~2026)**

- **2025-11 Apple 개발자 포럼 실사례**: 메인은 네이티브이고 2~3개 화면만 웹뷰인 하이브리드 앱조차 **4.2로 10회 연속 리젝**. 심사팀은 조문 복붙만 반복, 공식 조언은 "Meet with Apple 1:1 상담". [developer.apple.com/forums/thread/806726](https://developer.apple.com/forums/thread/806726) — 1차, 직접 fetch.
- "웹뷰 = 무조건 리젝"은 과장이나 방향은 맞음 — 통과하는 앱은 푸시 알림·네이티브 내비게이션·딥링크 등을 실제로 추가한 경우. 4.2 리젝 해결을 파는 전문 업체(code2native, Webvify 등)가 2025~2026에도 영업 중 — "고칠 수 있다"는 시장이 형성돼 있다는 방증.

**EU DMA와 한국에의 함의**

- 2024-02 Apple이 EU에서 홈스크린 웹앱 제거 시도 → 2024-03-01 철회, "will continue to offer... in the EU". 비-WebKit 엔진 출시 브라우저는 2025-07 기준 0개(Open Web Advocacy). [developer.apple.com/support/dma-and-apps-in-the-eu](https://developer.apple.com/support/dma-and-apps-in-the-eu/) — 1차, 직접 fetch.
- **한국 영향은 사실상 없음(긍정적 의미로)**: 2024-02 제거 시도는 EU 한정, 한국은 애초에 영향권 밖. 오히려 iOS 26부터 홈스크린 웹앱 대우가 전 세계적으로 좋아짐(§1.1 참고) — 지역 제한 없이 적용.

**Apple Developer Program 등록**

- 연회비 $99("or in local currency"), 한국은 실무상 연 129,000원으로 통용(2차, 스니펫 — 1차 원화 표기는 결제 화면에서만 노출돼 미확인). 개인은 D-U-N-S 불필요, 본인 명의 신용카드 필요. [developer.apple.com/support/enrollment](https://developer.apple.com/support/enrollment/) — 1차, 직접 fetch.

**종합 판단**: PWA를 그대로 웹뷰 래핑해 제출하는 경로는 4.2/4.2.2에 정면으로 걸림 — PWABuilder조차 공식적으로 Experimental+승인 비보장+iOS 저장소 아카이브 상태. 무조건 불가능은 아니나(네이티브 기능을 실제로 얹으면 통과 사례 존재) 리젝-재제출 반복(회당 수일~수주)을 각오해야 함. **한국 사용자 대상이면 앱스토어 없이도 iOS 홈스크린 웹앱(A2HS)이 정상 동작**하고 iOS 26부터 오히려 대우가 좋아졌으므로, $99/년+심사 리스크 대신 "A2HS 안내 강화"가 저비용 대안이 될 수 있음.

---

### 1.4 Capacitor

**버전·유지보수 상태**

- 최신 메이저 Capacitor 8(2025-12-08 출시), 최신 패치 8.4.2(2026-07-14). [ionic.io/blog/announcing-capacitor-8](https://ionic.io/blog/announcing-capacitor-8) — 1차, 직접 fetch.
- 지원 정책: v8 Active, v7은 2026-06-08 일반 유지보수 종료·2026-12-08 연장지원 종료. 지금 시작하면 v8이 유일 선택. [capacitorjs.com/docs/main/reference/support-policy](https://capacitorjs.com/docs/main/reference/support-policy) — 1차, 직접 fetch.
- Ionic(OutSystems 소속)이 계속 유지보수, 매년 새 Android target SDK 대응 메이저 출시.
- Capacitor 8 핵심 변화: iOS 신규 프로젝트 기본 의존성 관리자가 CocoaPods→Swift Package Manager로 교체, Android edge-to-edge 지원.

**Next.js와의 궁합**

- Capacitor는 "컴파일된 정적 웹 자산 디렉토리"를 번들함(`webDir`). [capacitorjs.com/docs/config](https://capacitorjs.com/docs/config) — 1차, 직접 fetch.
- `server.url`로 원격 URL을 가리키는 방식은 존재하나 **공식 문서가 프로덕션 사용을 명시적으로 금지**: "This is not intended for use in production." — 1차, 직접 fetch. (4.2 리젝 리스크와 이중고이므로 배제 권장.)
- **static export(`output: 'export'`)가 사실상 필수.** 2026-06-23 갱신 튜토리얼(Capacitor 8+Next.js 15+): `output:'export'` + `images:{unoptimized:true}` + `webDir:'out'`, API 라우트나 서버 데이터 페칭은 외부 API로 리팩토링 필요. [capgo.app](https://capgo.app/blog/building-a-native-mobile-app-with-nextjs-and-capacitor/) — 2차, 직접 fetch.
- static export에서 안 되는 것(Next.js 공식): Request 의존 Route Handlers, Cookies, Rewrites/Redirects/Headers, Middleware, ISR, 기본 로더 이미지 최적화, Draft Mode, Server Actions, `generateStaticParams()` 없는 동적 라우트. [nextjs.org/docs/app/guides/static-exports](https://nextjs.org/docs/app/guides/static-exports) — 1차, 직접 fetch.
- 표준 패턴: API 라우트는 원격 서버(Vercel 등)에 그대로 두고, 앱(정적 번들)은 절대 URL로 fetch. SenTalk 기준 `learn/[id]`는 `generateStaticParams()` 필요, API 10개는 `NEXT_PUBLIC_API_URL` 절대경로 전환 필요.
- Capacitor 공식 Next.js 전용 가이드는 없음(`capacitorjs.com/solution/nextjs` 404 확인).

**Web Speech API가 Capacitor WebView에서 동작하는가 — 동작 안 한다고 봐야 함**

- **Android System WebView**: Chromium 트래커에 "Web Speech API 미구현" 이슈가 장기 미해결(로그인 장벽으로 원문 확인 실패, 스니펫). Capacitor 공식 문서도 웹 구현의 전제(`SpeechSynthesis API` 지원 필요, 없으면 에러)를 명시하며 **"For more text-to-speech capabilities, please see the Capacitor Community Text-to-Speech plugin"**로 네이티브 플러그인을 권장. [capacitorjs.com/docs/apis/screen-reader](https://capacitorjs.com/docs/apis/screen-reader) — 1차, 직접 fetch.
- **iOS WKWebView STT**: `webkitSpeechRecognition` 객체는 노출되지만 **기본 비활성**. WebKit Bugzilla #239816(2022-04, RESOLVED WORKSFORME) — Safari에서만 켜져 있고 다른 WKWebView 임베더는 비활성, 호스트 앱이 `NSSpeechRecognitionUsageDescription` 선언 시 동작 가능성 언급. [bugs.webkit.org/show_bug.cgi?id=239816](https://bugs.webkit.org/show_bug.cgi?id=239816) — 1차, 직접 fetch.
- iOS WKWebView TTS(speechSynthesis) 동작 여부는 **미확인**(안전한 설계는 플랫폼 분기 없이 네이티브 플러그인으로 통일).
- **결론: TTS·STT 모두 네이티브 플러그인 어댑터 계층이 필요.**

**네이티브 TTS/STT 플러그인 현황**

- `@capacitor-community/text-to-speech` v8.0.2(2026-06-15), Capacitor 8 정식 대응, 주간 다운로드 26,041회 — 활발히 유지보수. `speak({lang, rate, pitch, volume, voice, category, queueStrategy})` 등 SenTalk 요구(속도 설정) 커버. [github.com/capacitor-community/text-to-speech](https://github.com/capacitor-community/text-to-speech) — 1차, 직접 fetch.
- `@capacitor-community/speech-recognition` v7.0.1(2025-06-09), peer `>=7.0.0`(Cap 8 설치는 가능하나 정식 v8 대응 릴리스는 아직 없음), 주간 다운로드 56,812회. 대안: Capawesome의 speech-recognition/speech-synthesis 플러그인 — Cap 8.x 호환표 명시, silence detection·on-device 모델 지원. [capawesome.io/plugins/speech-recognition](https://capawesome.io/plugins/speech-recognition/) — 1차(벤더), 직접 fetch.

**Apple 4.2 리스크 (Capacitor 맥락)**

- Capacitor 공식은 "Capacitor apps are normal native apps"라고만 하고 4.2 대응 전용 가이드는 없음.
- 2020년 Ionic 포럼 실사례: 클럽 멤버십 앱이 외부 링크 위주라 4.2로 2회 리젝 → 링크 제거+콘텐츠 보강+네이티브스러운 UI로 3번째 제출에서 승인. [forum.ionicframework.com](https://forum.ionicframework.com/t/app-store-rejection-4-2-design-minimum-functionality-my-first-after-2-years-of-ionic/200908) — 2차, 직접 fetch.
- **로컬 번들+오프라인 동작+네이티브 플러그인 사용이면 4.2 방어 논리가 강함.** `server.url` 원격 방식은 이중 리스크로 배제 권장.

**PWA 기능(service worker·오프라인)이 Capacitor 안에서 동작하는가 — 안 됨**

- **iOS: `capacitor://localhost` 커스텀 스킴 때문에 service worker 등록이 실패**("TypeError: ...protocol is either HTTP or HTTPS"). 이슈는 **closed as not planned** — 코어 차원 해결 계획 없음. [github.com/ionic-team/capacitor/issues/7069](https://github.com/ionic-team/capacitor/issues/7069) — 1차, 직접 fetch.
- App-Bound Domains 우회도 검증된 해법 없음(기능요청 #4122 미구현). Android는 기본 스킴이 `https://localhost`라 SW 동작 보고 있음(스니펫).
- 실무 결론: Capacitor 앱은 자산이 이미 로컬 번들이라 SW 없이도 "앱 셸 오프라인"이 성립. 오프라인 데이터는 Preferences/SQLite/로컬 저장으로 처리(SenTalk은 이미 next-pwa 제거 상태라 충돌 요소는 없음).

---

### 1.5 React Native/Expo vs Flutter 재작성

**Expo 2026년 성숙도**

- 최신 Expo SDK 57(2026-06-30), RN 0.86+React 19.2 포함. [expo.dev/changelog](https://expo.dev/changelog) — 1차, 직접 fetch.
- SDK 55(2026-02-25)부터 Legacy Architecture 지원 공식 종료. RN 0.82(2025-10-08)부터 **New Architecture가 유일한 아키텍처**(`newArchEnabled=false` 무시됨) — 전환 논쟁은 이미 끝난 상태. State of React Native 2025 서베이: New Architecture 채택률 80%. [results.2025.stateofreactnative.com](https://results.2025.stateofreactnative.com/en-US/) — 1차 서베이, 직접 fetch.
- EAS 무료 티어: 월 15 Android+15 iOS 빌드, EAS Update 1K MAU. [expo.dev/pricing](https://expo.dev/pricing) — 1차, 직접 fetch.
- **Expo Go 리스크**: SDK 55+용 Expo Go가 App Store 승인 대기 중(2026-05-04 공지, 일정 미정) — 실무는 development build 사용이 표준이라 치명적이진 않음. [expo.dev/changelog/expo-go-and-app-store-may-2026](https://expo.dev/changelog/expo-go-and-app-store-may-2026) — 1차, 직접 fetch.

**expo-speech (TTS) — Web Speech API 대체재로 적합**

- Android/iOS/Web/Expo Go 지원. `speak({voice, language, rate, pitch, volume})` + `onStart/onDone/onError/onBoundary/onStopped` 콜백, `getAvailableVoicesAsync()`로 기기 설치 음성 조회(웹의 `getVoices()`와 동일 구조). [docs.expo.dev/versions/latest/sdk/speech](https://docs.expo.dev/versions/latest/sdk/speech/) — 1차, 직접 fetch.
- **제약**: `pause()/resume()`은 iOS·Web만, **Android 미지원**. **iOS 실기기 무음 모드에서 소리 안 남**(문서 원문 명시). Android 음질은 기기 TTS 엔진(보통 `com.google.android.tts`) 의존.
- SenTalk의 `speakSequence`(순차 재생) 로직은 `onDone` 콜백 체이닝으로 동일 구현 가능(추정).

**React 숙련자의 재작성 공수**

- Expo 공식 주장: RN은 동일 컴포넌트 모델·JSX·hooks·state·context 사용("A `<View>` is a `<div>`"). expo-router는 Next.js app/ 디렉토리를 미러링하는 파일 기반 라우팅. [expo.dev/solutions/expo-for-react-to-native](https://expo.dev/solutions/expo-for-react-to-native) — 1차(벤더 마케팅 성격 유의), 직접 fetch.
- **NativeWind stable은 v4**(Tailwind v3 기반) — SenTalk은 Tailwind **v4**라 문법 조정 필요. v5는 pre-release로 Tailwind v4 대응 중. [nativewind.dev](https://www.nativewind.dev/) — 1차, 직접 fetch.
- State of RN 2025: 스타일링 StyleSheet 90.3%·NativeWind 42.1%, 내비게이션 react-navigation 79%·expo-router 71.1%·Solito 5.5%(니치).
- **재사용 구분(추정, SenTalk 코드베이스 기준)**:
  - 그대로 재사용: 순수 TS 로직(`lib/fsrs.ts` — ts-fsrs는 순수 TS, `lib/gamification.ts`, `lib/dialogue.ts`), API 서버(Next.js API Routes를 그대로 두고 HTTP로 호출).
  - 부분 수정 재사용: `useFetch/useMutation`(fetch API는 RN 내장), `useSettings/useDeviceId`(localStorage→AsyncStorage/MMKV 교체), `speech-sequence.ts`(Web Speech 호출부→expo-speech 교체, 세대 토큰 로직 유지).
  - 전면 재작성: 모든 UI 컴포넌트, shadcn/ui 전부, PWA·다크모드 구현부.

**Flutter와 비교**

- 최신 stable Flutter 3.44(3.44.0=2026-05-18, 3.44.7=2026-07-10). [docs.flutter.dev/install/archive](https://docs.flutter.dev/install/archive) — 스니펫.
- Flutter 공식 "Flutter for React Native devs" 전환 가이드가 스스로 "패러다임 전환"이라 서술 — Dart 필수 `main()`, 강타입, Sound Null Safety, 클래스 기반 `setState`, Flexbox 대신 Column/Row 위젯 트리. [docs.flutter.dev/get-started/flutter-for/react-native-devs](https://docs.flutter.dev/get-started/flutter-for/react-native-devs) — 1차, 직접 fetch.
- **로직 재사용 0%는 언어 구조상 사실** — Dart이므로 기존 TS 훅·타입·ts-fsrs를 가져갈 수 없음(서버 API 호출만 재사용). Dart FSRS 구현체 성숙도는 미조사.
- TS 숙련자의 Dart 적응 기간 추정치는 편차가 큼(1~3주 vs 2~3개월) — 신뢰도 낮은 2차 추정.
- Stack Overflow 2025 인용치(RN 14.51% vs Flutter 13.55%)는 원본 페이지 직접 확인 실패 — 2차 인용만 확보.

**포팅 소요 기간 실측 사례 — 정확히 맞는 사례는 확보 못함(미확인)**

- "Next.js 웹앱을 RN으로 포팅한 1인 개발자의 구체 소요 기간" 후기는 찾지 못함.
- 근접 사례: RN 신규(포팅 아님) 소규모 앱(~1,000줄)을 RN 학습 포함 2주 만에 출시. [dev.to/daebeom](https://dev.to/daebeom/i-built-and-launched-a-react-native-app-in-2-weeks-heres-what-i-learned-5bal) — 2차, 직접 fetch. 규모가 SenTalk보다 훨씬 작아 직접 비교 불가.

**WebView hybrid와 App Store 심사 (Capacitor·RN WebView 공통)**

- 4.2·4.2.2 원문은 §1.3과 동일. 2025-11 실사례(§1.3의 forums/thread/806726)도 동일 참조.
- 업계 관행(2025): **"Native Shell, Web Leaf"** — 탭바·내비게이션·핵심 인터랙션은 네이티브, 콘텐츠성 페이지만 WebView로 제한하는 것이 통과 전략(2차, 스니펫).

**종합 판단(추정)**: React/TS 숙련 1인 개발자에게 RN/Expo는 "언어·멘탈모델 유지+UI 재작성", Flutter는 "언어·UI·로직 전부 재작성+학습 기간" — 구조적으로 RN/Expo 쪽 공수가 적다. 이는 ADR-001이 "Flutter가 최적"이라 결론 내린 것과 **상충**하는 조사 결과다(ADR-001은 React 재사용 불가를 Flutter의 단점으로만 인정했을 뿐, RN/Expo 대안 자체를 검토하지 않았음).

---

## 2. 스토어 등록 실무 (Google Play · Apple)

**Google Play 개인 개발자**

- 등록비 $25 1회. 신원 확인: 신분증·주소증명(90일 내 발행, Payments 프로필 주소와 정확히 일치 필요). D-U-N-S는 조직만.
- **비공개 테스트 의무(최중요, §1.2와 동일 사실 교차확인)**: 2023-11-13 이후 생성된 개인 계정은 테스터 **12명 × 14일 연속 opt-in** 필수(2024-12-11에 20명→12명 완화). 신청 후 Google 검토 ≤7일.
- 개인정보 노출: 무료 앱이면 법적 이름+국가+이메일만 공개, **유료화하면 전체 주소까지 공개**.
- **부가세 함정**: 한국 개발자는 **Google Play 한국 구매자 매출 VAT 10%를 직접 납부**해야 함(Google의 부가세 대행은 해외 개발자向 서비스에만 해당, 한국 자체는 대행 대상 아님).
- 통신판매업 신고: 무료+무광고는 불필요. 유료/IAP 시 필요하나 간이과세자 또는 직전년도 50회 미만 거래면 면제.
- 심사: 첫 앱은 7~14일 잡아야 함.
- 미확인: 2025 연령등급 개편 세부.

**Apple Developer Program**

- $99/년, 개인은 D-U-N-S 불필요. 사업자등록 없이 유료앱/IAP 가능(W-8BEN은 App Store Connect에서 자동 생성). 개인 등록 시 법적 이름이 판매자로 고정 공개.
- 심사: 공식 "90%가 24시간 내"이나 **신규 앱 첫 제출은 2~5일, 리젝율 ~25%**.
- 미확인: Apple 원화 연회비 1차 출처(결제 화면에서만 노출).

**공통 필수 제출물**

- 스크린샷·feature graphic·앱 아이콘, **익명 앱도 개인정보처리방침 URL 양쪽 필수**. SenTalk의 deviceId는 "수집 없음"이 아니라 Google "Device or other IDs" / Apple "Identifiers(Not Linked, Not Tracking)"로 신고해야 함.
- 앱 카테고리·콘텐츠 등급 설문(IARC 자동 처리, 비게임 교육앱은 GRAC 등급분류 의무 없음).

**15% Small Business 수수료**

- 양쪽 다 첫 $1M까지 15%, **자동 아님** — Play Console 계정그룹 등록 / Apple SBP 사전 가입 절차 필요.

**출처**: [support.google.com/googleplay/answer/6112435](https://support.google.com/googleplay/android-developer/answer/6112435), [support.google.com/googleplay/answer/14151465](https://support.google.com/googleplay/android-developer/answer/14151465), [developer.apple.com/support/enrollment](https://developer.apple.com/support/enrollment/), [developer.apple.com/app-store/small-business-program](https://developer.apple.com/app-store/small-business-program/) — 전부 1차, 직접 fetch.

---

## 3. 서버·인프라·성능

> 기준: SenTalk(Next.js 16 App Router, API 라우트 10개, Neon ap-southeast-1, postgres-js, 텍스트 ~3만 행/수십 MB, 이미지·미디어 없음, 사용자당 세션 1회/일·API 콜 수십 회). 아래 수치·단가는 대부분 공식 pricing/docs 직접 fetch, 시나리오 비용은 그 수치로 계산한 추정.

### 3.1 Vercel Hobby(무료) 티어 한도 (2026-06-16 문서 기준)

| 자원 | Hobby 포함량/월 |
|---|---|
| Function Invocations | 100만 회 |
| Active CPU (Fluid) | 4 CPU-hrs |
| Provisioned Memory (Fluid) | 360 GB-hrs |
| Fast Data Transfer(대역폭) | 100 GB |
| Edge Requests | 100만 회 |
| 함수 최대 실행시간 | 300초(5분) |
| 배포 | 100회/일 |
| Runtime Logs 보존 | **1시간** |
| Web Analytics | 50,000 events/월 |
| Speed Insights | 10,000 events/월, 1개 프로젝트 |

출처: [vercel.com/docs/plans/hobby](https://vercel.com/docs/plans/hobby), [vercel.com/pricing](https://vercel.com/pricing) — 1차, 직접 fetch.

- **한도 초과 시 과금이 아니라 기능 정지 → 30일 대기**("if you exceed your usage limits on the Hobby plan, you will have to wait until 30 days have passed"). [vercel.com/docs/plans/hobby](https://vercel.com/docs/plans/hobby) — 1차.
- 2026-04-29부터 Hobby는 30일 지난 배포 자동 삭제(최근 프로덕션 10개·alias는 예외). [codingwithai.com](https://codingwithai.com/news/vercel-hobby-deployment-retention-april-2026) — 2차.

### 3.2 Vercel Hobby 상업적 이용 금지 — 원문 (광고 도입 시 핵심)

[fair-use-guidelines#commercial-usage](https://vercel.com/docs/limits/fair-use-guidelines) (last_updated 2026-06-16) 원문:
> "Hobby teams are restricted to non-commercial personal use only. All commercial usage of the platform requires either a Pro or Enterprise plan."
> "Commercial usage is defined as any Deployment that is used for the purpose of financial gain of **anyone** involved in **any part of the production** of the project..."

명시된 위반 예(비한정): 방문자에게 결제 요청/처리, 제품·서비스 판매 광고, 사이트 제작·운영 대가 수령, 제휴 링크가 주목적, **광고 게재(Google AdSense 등 명시)**, **기부 요청(Buy Me a Coffee류)**.
- → **광고·후원 버튼을 붙이면 명백한 위반, Pro($20/월) 필수.** 무료·무광고 개인 프로젝트는 조항상 허용.
- 집행은 신고·이상감지 기반으로 보이며(2025년 Hobby 계정 정지 사례 다수: [community.vercel.com](https://community.vercel.com/t/hobby-plan-account-suspended-not-reset-after-30-days/18307)), 문서상 "가능하면 조치 전 먼저 연락". 집행 통계는 미확인.

### 3.3 Vercel Pro ($20/월)

- $20/월 = 배포 시트 1개 + **월 $20 사용량 크레딧 포함**(미사용분 월말 소멸). 포함량 1TB 대역폭 + 1,000만 Edge Requests. [vercel.com/docs/plans/pro-plan](https://vercel.com/docs/plans/pro-plan) — 1차.
- 초과 단가: Invocations $0.60/100만, **Active CPU 서울 icn1 $0.169/h·워싱턴 iad1 $0.128/h**, Provisioned Memory icn1 $0.0140/GB-hr·iad1 $0.0106/GB-hr, 대역폭 $0.15/GB부터, Edge Requests $2/100만부터. [usage-and-pricing](https://vercel.com/docs/functions/usage-and-pricing) — 1차.
- **Fluid Compute 과금 특성(SenTalk에 유리)**: Active CPU는 실제 CPU 사용 시간만 과금 — **DB 쿼리 등 I/O 대기 중에는 CPU 과금 정지.** 요청 사이 유휴 시간도 과금 없음. [usage-and-pricing](https://vercel.com/docs/functions/usage-and-pricing) — 1차.

### 3.4 Neon 무료/유료 플랜

**Free 한도** ([neon.com/pricing](https://neon.com/pricing), [plans](https://neon.com/docs/introduction/plans), [usage-metrics](https://neon.com/docs/introduction/usage-metrics) — 1차):

| 항목 | Free |
|---|---|
| Compute | **100 CU-hours/프로젝트/월** (= 0.25 CU 기준 400시간/월) |
| 스토리지 | 0.5 GB/프로젝트 (SenTalk 수십 MB → 여유) |
| 프로젝트 / 브랜치 | 100개 / 10개 |
| Autoscaling | 최대 2 CU (8 GB RAM) |
| Scale to zero | **5분 무활동 후 suspend — Free는 고정, 변경 불가** |
| Egress | 5 GB/월 |

- **compute 소진 시 동작이 치명적**: "your compute is suspended until the next billing period or until you upgrade" — 자동 과금 전환 없이 **월 중 소진 = 남은 기간 DB 전면 정지.** [usage-metrics](https://neon.com/docs/introduction/usage-metrics) — 1차.
- **커넥션 한도** ([connection-pooling](https://neon.com/docs/connect/connection-pooling)): 직접 연결은 0.25 CU = 104개(실질 ~97), pooled(-pooler, PgBouncer) `max_client_conn=10,000`·transaction mode(세션 기능 제약). **서버리스에선 -pooler 엔드포인트 사용이 사실상 필수.**
- **유료 플랜(2025 개편, 월 최소요금 없는 종량제)**: Launch = compute **$0.106/CU-hour** + 스토리지 $0.35/GB-월, scale-to-zero 비활성화 가능(5분 고정 해제), autoscale 최대 16 CU. Scale = compute $0.222/CU-hour, scale-to-zero 1분~always-on 자유. [neon.com/pricing](https://neon.com/pricing) — 1차.

### 3.5 콜드스타트 (이중 문제)

- **Neon 웨이크**: 공식 "within a few hundred milliseconds"([scale-to-zero](https://neon.com/docs/introduction/scale-to-zero)), 서드파티 실측 첫 쿼리~첫 응답 300~500ms([Medium](https://medium.com/@philmcc/neon-postgres-review-serverless-postgresql-that-actually-scales-to-zero-ee14d4e109ba)) / 400~750ms([dev.to](https://dev.to/philip_mcclarence_2ef9475/neon-postgres-review-is-serverless-postgresql-ready-for-production-1pck)). `sslnegotiation=direct`로 핸드셰이크 ~120ms 단축.
- **Vercel**: 2025-04-23부터 신규 프로젝트에 Fluid Compute 기본 활성화(bytecode caching + pre-warming + 인스턴스 내 동시성 → 콜드 빈도 감소). 단 최초 1회 콜드스타트 자체는 존재. [vercel.com/docs/fluid-compute](https://vercel.com/docs/fluid-compute) — 1차.
- **겹칠 때**: 한적한 시간대 첫 방문자는 [Vercel 콜드 + Neon 웨이크(300~750ms) + TCP/TLS 핸드셰이크]가 직렬로 겹쳐 첫 API 응답 1~2초대 가능(합산 공식 실측치는 미확인, 개별 수치의 합 추정).
- **keep-alive ping의 함정**: 24시간 깨워두려면 720시간 필요 = 180 CU-hrs → **Free 한도(100 CU-hrs = 400시간)로는 산술적으로 불가능.** 하루 ~13시간까지만 가능. 업타임 모니터는 DB를 건드리지 않는 엔드포인트로 구성할 것.
- **커넥션 전략**: Fluid에서는 표준 TCP + 커넥션 풀이 Neon 공식 권장("With Vercel Fluid, we recommend you use a standard Postgres TCP connection and a connection pool", [neon.com/docs/guides/vercel-connection-methods](https://neon.com/docs/guides/vercel-connection-methods)) — postgres-js 현 구성과 일치. pooler 접속 문자열·함수 리전(기본 iad1 → sin1/icn1 변경)만 점검. `@vercel/functions`의 `attachDatabasePool`은 node-postgres 예시 기준, postgres-js 직접 지원 여부는 미확인.

### 3.6 시나리오별 자원 사용량·비용 (계산 전제: 유저당 1세션/일·세션당 API 콜 50회, API 1콜당 Active CPU ~30ms)

| 자원(월간) | 10 DAU | 100 DAU | 1,000 DAU | Hobby 한도 |
|---|---|---|---|---|
| Invocations | 1.5만(0.2%) | 15만(15%) | **150만(초과)** | 100만 |
| Edge Requests | ~3만 | ~30만 | ~300만(초과) | 100만 |
| Active CPU | 0.13h(3%) | 1.3h(31%) | **12.5h(초과)** | 4h |
| Provisioned Memory | ~3 GB-hrs | ~25 GB-hrs | ~250 GB-hrs | 360 GB-hrs |
| 대역폭 | <1 GB | ~3 GB | ~30 GB | 100 GB |
| **Neon compute** | ~20 CU-hrs(20%) | **60~180 CU-hrs(경계~초과)** | ~180~250 CU-hrs(초과) | 100 CU-hrs |

Neon compute 산정 근거: scale-to-zero 5분이므로 웨이크 시간 = 접속이 5분 이상 안 끊기는 구간 + 마지막 접속 후 5분. 10 DAU는 산발 접속(~2.5h 웨이크/일), 100 DAU는 접속이 하루에 퍼지는 정도에 따라 60~180 CU-hrs로 갈림, 1,000 DAU는 사실상 24h 웨이크(720h × 0.25 CU = 180) + 피크 오토스케일 가산.

| 구성 | 10 DAU | 100 DAU | 1,000 DAU |
|---|---|---|---|
| Vercel | **$0**(Hobby, 비상업 전제) | **$0**(Hobby 수치상 가능) | **$20**(Pro 필수. 초과분 ~$6는 $20 크레딧 내 소화) |
| Neon | **$0**(Free) | **$0~$15**(Free 경계. 초과 시 Launch ~140 CU-hrs × $0.106 ≈ $15) | **~$20**(Launch ~190 CU-hrs × $0.106 ≈ $20) |
| 모니터링 | $0 | $0 | $0 |
| **합계** | **$0** | **$0~$15** | **~$40** |

- **100 DAU의 함정**: Neon Free 초과는 과금이 아니라 월말까지 DB 정지이므로, 100 DAU 공개 베타를 열 거면 시작 시점에 Launch로 올려두는 편이 안전(Launch는 월 최소요금 없어 실사용분만 과금).
- 광고/후원 계획이 있으면 규모 무관 Vercel Pro($20/월) 필요(§3.2).

### 3.7 부하 검증 · 모니터링

- **부하 검증 기준**: 1,000 DAU 피크가 ~10 RPS 수준이라 k6로 10~30 RPS 램프 + 50 RPS 버스트면 충분. Vercel 공식 KB상 50k RPS 미만은 사전 티켓 불요이나, 부하 테스트는 관측 도구 비용 자기 부담 경고가 있으므로 Pro + Spend Management 설정 후 실행 권장.
- **모니터링(전부 무료 가능)**: Sentry Developer(5천 에러/월) + UptimeRobot(50모니터/5분). **Vercel Hobby 로그 보존이 1시간뿐이라 Sentry가 사실상 필수.**

### 3.8 페이지 로딩 최적화 (Next.js App Router, 2026)

- Core Web Vitals 기준: LCP·INP·CLS. 서버 컴포넌트 캐싱(`'use cache'`, revalidate 등 Next.js 16 현행 API), API 응답 캐싱, Vercel Speed Insights(Hobby 10,000 events/월), Lighthouse CI.
- 현 코드의 review API N+1(`api/review/route.ts:58`)과 캐싱 전략 부재는 규모와 무관하게 손볼 항목(20번 문서 체크리스트 참고).

---

## 4. 보안·개인정보·법규

> 법률 자문이 아닌 일반 정보 수준. 실제 처리방침·약관 작성 전 변호사 검토 권장(코퍼스 라이선스 문서 `docs/data-tracks/18/14-korean-copyright.md`도 동일하게 명시).

**현재(익명) 상태 기준 의무**

- 개보위 해석(2024-01 행태정보 정책방안)상 로그인 없이 기기만 구별하는 랜덤 UUID는 원칙적으로 개인정보 처리가 아님 — 단 IP 결합 가능성 논점이 있어 처리방침을 두는 게 안전.
- 한국은 EU식 쿠키 배너 동의 의무 없음 — 처리방침에 "자동 수집 장치 설치·운영·거부" 기재로 충분.
- **Google Play·Apple 모두 수집이 0이어도 Data safety 폼/프라이버시 라벨 + 처리방침 URL 필수.** SenTalk은 서버 전송이 있으므로 "Device ID + App activity 수집"으로 신고해야 함.
- 이용약관은 무료 서비스엔 법적 의무 아님(권장 수준).
- 14세 미만 아동: 익명이면 법정대리인 동의 요건 발동 안 함.

**기능 추가 시 발생하는 의무**

- **AdMob 도입 시**: AD_ID 권한(SDK 자동 병합), Data safety에 광고ID·광고 목적 공유 신고, iOS는 ATT 프롬프트, 처리방침에 행태정보 조항 추가.
- **소셜 로그인(ADR-002) 도입 시**: Apple 4.8 현행은 Sign in with Apple 강제가 아니라 "이름·이메일 제한+이메일 비공개+광고 목적 수집 금지"를 충족하는 대체 로그인 요구(2024 개정) — 카카오 단독도 조건 충족 시 가능하나 심사 편차 있음. 계정 생성 앱은 양 스토어 모두 계정 삭제 기능 필수.
- **서버 STT(ADR-008) 도입 시**: 발음 평가 목적 음성은 화자 식별 목적이 아니라 생체인식 민감정보 아님(개보위 생체정보 가이드라인 구조). 국외이전(OpenAI 미국 서버)은 제28조의8 "계약 이행 위한 처리위탁" 경로로 **별도 동의 없이 처리방침 공개로 갈음 가능** — 항목·국가·받는자·보유기간 기재 필요. OpenAI API는 기본 학습 미사용·30일 보관, 한국 리전 레지던시 옵션 있음.
- 사업자등록: 광고 수익이 계속·반복되면 필요(면세 업종 가능). 부가통신사업 신고는 자본금 1억 이하 면제.
- EU 배포 시 DSA trader 신고(2025-02 강제) 주의.

**보안 체크리스트 (Next.js 공개 배포 최소선)**

- OWASP 관점에서 deviceId(UUID) 난수성은 IDOR 방어가 아님 — deviceId를 URL에 노출 금지, 전 쿼리 deviceId 스코프 강제, **HMAC 서명 토큰 승격이 계정 도입 전 단계의 현실적 완화책.**
- Next.js 공식 CSP(nonce+middleware)+HSTS 구성, Neon은 env 전용·`sslmode=verify-full`.

**콘텐츠 저작권 일반론 (법률 자문 아님)**

- 짧은 대사·명언은 저작물성 부정 경향. 대표 사례: 영화 '왕의 남자'의 "나 여기 있고 너 거기 있지" — 서울고법 2006-11 가처분 항고 기각("일상생활에서 흔히 쓰이는 표현, 창작성 인정 불가" 취지, 사건번호는 미확인). [노컷뉴스](https://www.nocutnews.co.kr/news/214545). 명언 저작재산권은 사후 70년(저작권법 제39조) — 고전은 대부분 만료.
- 인용(제28조) 판단 기준은 대법원 2013.2.15. 선고 **2011도5835**: 인용저작물이 주(主)·피인용이 종(從)인 주종관계 + 원저작물 수요 대체 여부 종합, **영리 목적이면 자유이용 허용 범위가 상당히 좁아진다**고 판시. [casenote](https://casenote.kr/대법원/2011도5835). 교재가 대사를 "예문·본문"으로 편입하는 방식은 종속적 인용이라기보다 콘텐츠 자체로 쓰는 것이어서 주종관계 논리로 불리할 수 있음.
- **광고 수익(영리성)은 인용·공정이용(제35조의5) 판단 모두에서 불리 요소로 작용.**
- 학습앱 직접 관련 판례는 확보 못함(미확인) — 실무적 리스크 축소책: ①일상 표현 위주 선별 ②출처 표시(제37조) ③만료 명언 위주 재구성 ④문제 소지 문구는 자체 창작 예문으로 대체 ⑤광고 모델 도입 전 [한국저작권위원회](https://www.copyright.or.kr) 상담.

**출처**: 개인정보보호위원회 행태정보 정책방안(2024-01), 국내 개보법 국외이전 규정(2023 개정), 스토어 공식 정책 페이지(Google Play Data Safety, Apple Privacy Nutrition Label) — 세부 URL은 원 조사 노트 기준, 실제 적용 전 최신본 재확인 필요.

---

## 5. 수익성·시장 벤치마킹

### 5.1 광고 수익 (AdMob 한국 eCPM)

**한국 eCPM 실측치 (Appodeal Q4 2024 데이터, 2차 인용 — 원본 다운로드 게이트)**

| 형식 | 한국 | 미국 | 일본 |
|---|---|---|---|
| 보상형(rewarded) | **$12.00** | $15.15 | $10.80 |
| 전면(interstitial) | **$8.65** | $12.65 | $7.20 |
| 배너 | **$0.11** | $0.50 | $0.10 |

출처: [business.mistplay.com/resources/mobile-ads-ecpm](https://business.mistplay.com/resources/mobile-ads-ecpm) (2026-03 게재, 데이터는 2024 Q4) — 2차 인용.

- **한국 배너는 미국의 1/5 수준(사실상 무의미)** — 전면·보상형 중심 설계가 필수.
- 한국 개발자 실측 공개(2023-02, 오래됨): 월 $3,600~4,000 수익. 미디에이션 실측: eCPM floor $15 설정 시 fill rate 99.7%→60% 급락.

**SenTalk형 학습앱 DAU별 추정(계산 근거 — 추정치, 실측 아님)**

한국 eCPM(전면 $8.65, 보상형 $12.00, 배너 $0.11) + 보수적 노출 가정(1인당 일 전면 2회+보상형 0.3회+배너 5회, fill 100%):

| DAU | 전면(월) | 보상형(월) | 배너(월) | 합계(월) |
|---|---|---|---|---|
| 100 | $52 | $11 | $1.7 | **~$65 (약 9만 원)** |
| 1,000 | $519 | $108 | $17 | **~$644 (약 90만 원)** |
| 10,000 | $5,190 | $1,080 | $165 | **~$6,400 (약 900만 원)** |

- ARPDAU 약 $0.021로 캐주얼 게임 하한($0.03)보다 낮게 잡은 보수 추정(학습앱은 게임보다 세션 수가 적음).

**리텐션 영향**

- 전면광고 남발 시 D7 리텐션 **10~30% 하락** + 언인스톨 급증(업계 통설, 학술 출처 불명). [mwm.ai/glossary/interstitial](https://mwm.ai/glossary/interstitial) — 업계 가이드.
- **듀오링고 방식**: 광고는 딱 두 곳(레슨 완료 후 전면 + 자발적 보상형), 학습 도중엔 광고 없음. MAU 1.28억, 90%가 무료 티어. AdMob 공식 케이스: 미디에이션 도입으로 광고 수익 +70%, 비딩 추가 +20%. [admob.google.com](https://admob.google.com/home/resources/duolingo-partners-with-admob-to-optimize-mediation-strategy-and-increase-ads-revenue-by-seventy-percent/) — 플랫폼 공식 케이스.
- 웹/PWA 광고(AdSense): 한국 Page RPM 일반 1,000~10,000원, 정보/IT/교육 3,000~7,000원 — **웹 RPM은 앱 인앱 광고보다 한 자릿수 낮음.**

미확인: 2024~2026 한국 개발자의 형식별(배너/전면/보상형) 실측 공개 글 — 확보 실패.

---

### 5.2 1인/인디 개발자 수익 사례

**한국 사례**

| 사례 | 수익 | 기간 |
|---|---|---|
| 김윤후 — '간단'(간헐적 단식) 외 4개 앱 | 월 600만~1,200만원(2025), 300만 다운로드, 프리미엄 전환 10~20%, 마케팅비 월 50만원 이하 | 첫 수익~월 1,000만원까지 **8년** 소요, 앱 50개 기획→15개 출시→3~4개 집중 |
| 클리앙 익명 — 습관추적 앱 | 2020-06 월 10만원→12월 월 600~800만원 페이스 | 2020년(오래된 자료) |
| OKKY 익명 — 앱 2개 | 2018 연 $102K→2019 연 $80K(방치로 -20%) | 2019년(오래된 자료) |

**글로벌 사례**

| 사례 | 수익 | 기간 |
|---|---|---|
| Sebastian Röhl(독일, 솔로, HabitKit 등) | 2025년 총매출 $602K, MRR $28K, 유료구독 25,100명($1~2/월) | 2022년 초 시작→2024년 말 MRR $10K→2025년 $602K |
| Habit Pixel(솔로) | 첫 달 $28 MRR→8개월 만에 $1K MRR(2026-01) | 구글플레이 ~1만 설치 |
| Jack Friks(앱+SaaS) | 합계 월 $10K (앱 $3K+SaaS $7K) | 개발 학습 시작부터 ~12개월, 쇼트폼 대량 업로드 전략 |
| Nihongo(일본어 학습앱, 인디) | 구체 수치 비공개 | 2014 출시→풀타임 전환까지 **6년 이상** |

**실패 사례**: 브런치 환승택시 앱(154 다운로드), Serhii Hryn 앱 3개(6개월 $25 MRR), 김윤후 첫 앱(다운로드 100회 미만).

**"대부분 앱은 돈을 못 번다" — RevenueCat 3개년 데이터 (§5.3과 교차)**

- 2024판: 출시 12개월 후 중앙값 월 **$50 미만**, $1,000 도달 17.2%, $10,000 도달 3.5%.
- 2026판(115,000+ 앱): 출시 2년 내 $1K MRR 도달 **17.3%**, $10K 도달 4.6%. 12개월 후 중앙값 월 **약 $72**.
- 상위 5%가 하위 25%의 400배+ 매출 격차(2025판).

**성공 요인 공통점**: ASO+오가닉 저비용 마케팅(김윤후 마케팅비 월 50만원 이하), 쇼트폼(틱톡·릴스), 미디어 노출 한 방(MKBHD 등), 다작 후 집중(50개→3~4개), 니치+장기전(6~8년 단위).

미확인: 한국 1인 개발 "학습앱" 수익 공개 직접 사례(팀/투자 받은 회사 사례만 검색됨).

---

### 5.3 구독 벤치마크 · 결제 인프라 · 스토어 수수료 정책

**RevenueCat State of Subscription Apps (2024/2025/2026판 — 정의 차이 주의)**

- 2026판(Education 카테고리, 표본 115,000+ 앱): 설치→유료(D35) 중앙값 **2.3%**, 체험→유료(17~32일 체험) **42.5%**, 첫 갱신 연간 **24%(전 카테고리 최하위)** · 월간 56% · 주간 58%(최고). Y1 LTV(유료자당) $22.82.
- Education 구독가 중앙값: **월 $9.99, 연 $39.94**(카테고리 중 고가권).
- 언어학습 앱 실구간: 듀오링고 Super 월 $12.95/연 $71.40, Babbel 연 $108, Rosetta Stone 연 $143.88 — **메이저 앱 월 $8~18, 연 $71~144.**

**1인 개발자 결제 인프라**

- RevenueCat 무료: 월 추적 수익(MTR) $2,500까지, 초과 시 매출의 1%.
- **한국 법인은 Stripe 계정 개설 불가** — 미국 델라웨어 C-Corp(Stripe Atlas $500+연 $1,000~2,500) 또는 싱가포르 법인 필요. 2024년 말부터 해외 법인 계정으로 한국 카드 수신은 가능.
- Paddle·Lemon Squeezy(Merchant of Record): **5% + $0.50**, 세금 신고 대행 포함, **법인 불필요** — 1인 개발자 현실적 대안.

**웹 PWA로 스토어 IAP 회피**

- 웹 전용 PWA(스토어 미배포)는 스토어 수수료 대상이 아님 — Stripe/Paddle 등 아무 PG나 사용 가능, 합법.
- **가이드라인 3.1.1 현행**: 미국 스토어프론트는 entitlement 없이 외부 결제 버튼·링크 허용(명문화), 미국 외 지역은 StoreKit External Purchase Link Entitlement 필요.

**Apple 외부결제 정책 변화 (급변 중 — 재확인 필수)**

- 2025-04-30 Epic v. Apple: 미국 앱 외부 링크 결제 자유화, **수수료 0%**로 27% 폐지.
- 2025-12-11 제9항소법원: "수수료 전면 금지는 과도, 합리적 수수료는 허용" — 지방법원 환송.
- 2026-04-29 항소법원이 Apple의 stay를 뒤집음 — **2026-07 현재 미국 외부 링크 수수료 0% 유지**, 대법원 상고 병행 중(0%가 영구는 아님).
- **한국**: 2021-09 전기통신사업법 개정(인앱결제 강제 금지 세계 최초)에도 Apple은 한국 전용 바이너리+entitlement로 제3자 결제 허용하되 **수수료 26%+PG 수수료 약 5%=사실상 30%+**라 실효성 논란 지속.
- **Google Play 한국**: 대체 결제 시스템 제공 시 수수료 4%p 인하(30%→26%, **15%→11%**, 대다수 개발자가 해당하는 15% 구간이 실질 혜택 큼). PCI DSS 인증·대체 결제 API 통합 필요.

**출처**: [revenuecat.com/state-of-subscription-apps](https://www.revenuecat.com/state-of-subscription-apps), [revenuecat.com/state-of-subscription-apps-2026-education](https://www.revenuecat.com/state-of-subscription-apps-2026-education/), [support.google.com/googleplay/answer/11222040](https://support.google.com/googleplay/android-developer/answer/11222040), [developer.apple.com/app-store/review/guidelines](https://developer.apple.com/app-store/review/guidelines/)(3.1.1) — 1차. Apple 외부결제 소송 경과는 [macrumors.com/2025/12/11](https://www.macrumors.com/2025/12/11/apple-app-store-fees-external-payment-links/), [macrumors.com/2026/04/29](https://www.macrumors.com/2026/04/29/epic-games-wins-reversal-app-store-fee-battle/) — 언론.

**SenTalk 시사점(원 조사자 종합)**: 웹 PWA + Paddle/Lemon Squeezy(MoR, 법인 불필요, 5%+$0.50) 조합이면 스토어 수수료 자체가 없고 RevenueCat도 MTR $2.5K까지 무료 — 초기 비용 0에 가까움. 스토어 진출 시 한국은 제3자 결제 실익 없음(26%+PG≈30%), 미국은 외부 링크 0%지만 법원이 "합리적 요율"을 산정 중이라 변동 리스크 있음.

---

### 5.4 한국 영어 학습 앱 벤치마킹

**말해보카 (이팝소프트)**

- 현재가: 12개월 인앱 119,000원 / 웹결제 99,000원(월평균 8,250원). 2025-09 21.4% 가격 인상.
- **BM**: 구독 단일 모델, 광고 기반 무료 모델을 의도적으로 배제("무료는 학습 집중도를 떨어뜨린다").
- 매출: 2023년 120억→2024년 220억(+83%, 창사 7년 첫 흑자)→2025년 256.4억(+16.5%, 기업DB 참고치·언론 교차확인 못함).
- 다운로드 글로벌 1,000만(2025-12-31). 2024-01 한국 교육 앱 매출 1위.
- 성공 요인: 넥슨 출신 창업진의 게이미피케이션 + 실시간 실력분석·난이도 최적화.

**Cake**

- 하이브에듀 인수(2022-03). BM: freemium(무료+광고, Cake Plus 구독 시 광고제거+무제한). 한국 월 9,900원.
- 글로벌 1억+ 다운로드(2023 기준). MAU·매출 실적 보도는 미확인.

**Speak (스픽)**

- Series C $78M, 기업가치 $1B(유니콘, OpenAI Startup Fund·Accel 참여). 연매출 $100M+(2023년 $24M에서 급성장).
- **한국 비중이 압도적**: 누적 매출의 90.9%가 한국(2023년 시점), 한국 다운로드 550만(전체 60%), 국내 매출 2020년 1억→2023년 60억원.
- 가격(제휴 블로그 기준, 공식가 아님 주의): 연간 프리미엄 129,000원/프리미엄 플러스 299,000원.

**듀오링고(한국)**

- BM: 무료+광고 기본, Super/Max 구독 상향판매. 한국 MAU 335.8만(2025-10, 5년 전 대비 15배).
- 글로벌 MAU 1.28억. 한국 누적 다운로드 ~500만, 누적 매출 ~$10M — 한국 언어앱 매출 3위·DAU 2위.

**산타토익 (뤼이드→소크라 AI, 2025-09 사명변경)**

- 2024년 매출 201억(+161%), 여전히 적자. 사명 변경 후 시장 반응 "싸늘"하다는 평가 기사 존재.

**"매일 한 문장" 류 유사 앱**: "하루 한문장" 등 개인 개발 소규모 앱 외에, "문장 중심+FSRS+쉐도잉" 조합을 정면으로 파는 유의미한 상용 앱은 확인되지 않음 — 가장 근접한 성공사례는 말해보카(단어 중심+구독+게이미피케이션)와 스픽(AI 스피킹+연간권)의 부분 중첩.

**시장 규모**: 한국 에듀테크 2025년 약 $5.1B(IMARC) ~ 9.98조원(2022년 전망치, 오래됨). 영어 학습 앱은 2022년 한국 교육 카테고리 매출의 39.2%.

**출처**: [epop.ai/ko/premium/plan](https://epop.ai/ko/premium/plan), [epop.ai/newsroom](https://epop.ai/newsroom/45), [sensortower.com 블로그 다수](https://sensortower.com/ko/blog/Speak-top-1-by-revenue-in-the-education-category-of-the-Korean-market-for-a-year), [techcrunch.com/2024/12/10](https://techcrunch.com/2024/12/10/openai-backed-speak-raises-78m-at-1b-valuation-to-help-users-learn-languages-by-talking-out-loud) 등 — 세부는 원 조사 노트 참고.

---

### 5.5 시장 트렌드 · 비수익 가치

**글로벌 언어학습 앱 시장 규모 — 기관별 편차 매우 큼**

시장 정의(앱 한정 vs 온라인 언어학습 전체)에 따라 2025년 추정이 **$2.6B~$21B**까지 벌어짐(Market Research Future $13.32B, Mordor Intelligence $21.06B, Market Reports World $2.622B 등) — 절대금액보다 **성장률(CAGR 11~21%)**이 일관된 신호.

**AI 회화 앱 트렌드**

- 듀오링고 Max(AI 롤플레이·Video Call)가 유료 구독자 내 비중 2024년 말 5%→2025년 말 약 9%. AI 비용 증가로 구독 마진은 하락.
- **ChatGPT Advanced Voice Mode(2024-07~)의 충격**: 2025-08 GPT-5가 "몇 분 만에 언어학습 앱 생성" 시연 → 듀오링고 주가 -38% 급락(사업 자체는 FY2025 매출 $1.037B, +39% 성장 — **주가 폭락은 사업 붕괴가 아니라 AI 상시 위협 재평가**).
- 시장 이분화 분석: **"순수 자동화(단순 플래시카드 드릴)가 무료 LLM에 가장 크게 잠식"**당하는 반면, 인간 매개·동기 설계가 있는 플랫폼은 견조. AI가 대체 못하는 것으로 동기 유지·문화 맥락을 꼽음.
- SRS(FSRS) 알고리즘 자체는 여전히 유효하다는 컨센서스가 우세하나, **카드 작성·콘텐츠 생성 부분이 LLM으로 대체**되고 가치는 "큐레이션된 커리큘럼+인출 연습+동기 설계"의 결합으로 이동 중 — 대체가 아니라 역할 재배치.

**듀오링고 실적 (참고 벤치마크)**

- FY2025 매출 $1.037B(+39%), Q4 DAU 52.7M(+30%), 유료구독자 12.2M. 2026 가이던스가 컨센서스 하회해 발표 후 시간외 -24%, 2025년 연간 주가 -46%.

**비수익 가치 (수익화하지 않는 선택의 논거)**

- 한국 실전 후기: 사이드 프로젝트는 서류 통과·커피챗 기회는 늘리나(서류 합격률 ~10%), 기술 면접에서 실무 깊이 부족은 별개 문제 — **"기회 창출 장치이지 실력의 대체재가 아니다."**
- OSS 기여의 커리어 시그널링 가치를 다룬 학술 연구 존재(Labour Economics, 2025).
- 실측: 인디해커 4년간 26개 프로젝트로 총 ~$115K, 수익 발생은 8개(31%)뿐, 첫해 수익 $0 — **프로젝트당 기대값은 낮고 분산이 큼.**
- 기회비용 관점: 빅테크 시니어 총보상 $350K+/년과 비교하면 수익화 노력의 시간당 기대수익이 낮음. "주 40시간 드는 사이드 프로젝트는 또 하나의 직업일 뿐."
- 비수익화 자체의 효용: 상업적 제약(마감·과금 설계) 없는 창의 실험실, 본업 집중 유지, 내재 동기 보존.

**출처**: [investors.duolingo.com](https://investors.duolingo.com/news-releases/news-release-details/duolingo-finishes-2024-51-daus-growth-more-40-million-daus-and)(IR 공식), [revenuecat.com/state-of-subscription-apps](https://www.revenuecat.com/state-of-subscription-apps), [news.ycombinator.com/item?id=44020591](https://news.ycombinator.com/item?id=44020591), [velog.io/@khy2106](https://velog.io/@khy2106/사이드프로젝트-커리어-절망편), [indiehackers.com](https://www.indiehackers.com/post/4-years-26-projects-115k-lessons-from-an-indie-hacker-7ab46733da) — 세부는 원 조사 노트 참고.

---

## 6. 미확인 항목 종합

실제 의사결정 전에 재확인이 필요한 항목들 (원 조사에서 "미확인"으로 명시된 것만 모음):

- Apple Developer Program 한국 원화 연회비의 1차 출처(결제 화면에서만 노출).
- 2025 Google Play 연령등급 개편 세부.
- "DAL 정상인 자기 소유 TWA"가 그 이유만으로 리젝된 2024~2026 사례.
- PWABuilder iOS 패키징 산출물이 실제로 App Store 승인된 2024~2026 공개 후기.
- iOS Safari `speak()`의 사용자 제스처 요구가 Chrome처럼 공식 문서화됐는지.
- iOS WKWebView에서 speechSynthesis(TTS) 자체의 동작 여부(STT는 비활성 확인됨, TTS는 미확인).
- Dart FSRS 구현체(dart-fsrs 등)의 성숙도 — ADR-001은 존재만 언급, 품질 미검증.
- "Next.js 웹앱을 RN/Expo로 포팅한 1인 개발자의 구체적 소요 기간" 실측 후기.
- 2024~2026 한국 개발자의 광고 형식별(배너/전면/보상형) 실측 공개 글.
- 한국 1인 개발 "영어 학습앱" 수익 공개 직접 사례(팀/투자 받은 회사 사례만 확인됨).
- 왕의 남자 판례 등 한국 저작권 관련 정확한 사건번호, 학습앱 직접 관련 판례.
- 개인정보보호위원회 행태정보 가이드라인의 최종 확정 여부.
- 한국 성인 영어교육 시장의 별도(교육 전체와 분리된) 규모 추정.
- Vercel Hobby 상업적 이용 금지 조항의 실제 집행 통계(공식 통계 없음, 계정 정지 사례 보고만).
- Vercel+Neon 이중 콜드스타트의 합산 실측치(개별 수치만 확인, 합산은 추정).
- `@vercel/functions`의 `attachDatabasePool`이 postgres-js를 직접 지원하는지(node-postgres 예시만 확인).
- 2025-04 EU가 Apple에 부과한 5억 유로 벌금의 정확한 사유(anti-steering vs 브라우저 엔진 — 2차 출처 간 서술 갈림).
- iOS 대체 브라우저 엔진 entitlement에 일본이 추가된 정확한 시점(일본 스마트폰법 대응 2025년 말 추정).

이 목록에 있는 항목은 **문서 어디에서도 확정 사실로 인용하지 말 것** — 결정에 영향을 주는 항목이라면 재조사 후 사용.
