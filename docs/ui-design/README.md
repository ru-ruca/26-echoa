# UI 디자인 — 진행 순서

> 작성일: 2026-08-07
> 관련: [22 §9 화면 명세](../project-review/22_learning-design-spec.md) · [ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md)

legacy(SenTalk)는 Stitch·v0로 화면을 뽑았다. 이번엔 **claude.ai/design**으로
디자인 시스템을 만들어 쓴다. 두 경로가 있는데 **전제가 다르다**.

| 경로 | 전제 | 산출 | 시점 |
|---|---|---|---|
| **Create here** (claude.ai/design 웹) | 코드 불필요. 회사·제품 설명 + 노트 + (선택) GitHub·로컬 폴더·`.fig`·폰트/로고 | 디자인 시스템 초안 | 지금 가능 |
| **Create using Claude Code** (`/design-sync`) | **React 컴포넌트가 있어야 함** — 토큰과 컴포넌트를 직접 읽는다 (BEST FIDELITY) | 코드 ↔ 디자인 시스템 동기화 | 컴포넌트 구현 후 |

> `/design-sync`는 **사용자가 직접 프롬프트에 입력**해야 동작한다. 에이전트에게 대신 실행시켜도 안 된다.
> Claude Code를 최신으로 유지하고 Claude 계정으로 로그인돼 있어야 한다 (Bedrock·Vertex·Foundry 미지원).

## 순서

1. **[22번 학습설계 spec 확정](../project-review/22_learning-design-spec.md)** — 현재 "초안 · 검토 대기".
   §9 화면 명세(홈 오늘의 플랜 · 학습 4단계 아코디언 · 복습 큐 · 진도·통계)가 디자인의 입력이다.
   이게 흔들리면 와이어프레임을 두 번 그리게 된다.
2. **claude.ai/design "Create here"로 디자인 시스템 초안** — 사용자가 직접. 입력 재료:
   - Echoa 한 줄 설명 (일상 소통 중심 영어 학습, 말하기 내장, 무료+광고)
   - 22 §9 화면 명세
   - legacy 화면 참고: `../../../26-SenTalk-en-study-app/docs/ui-design/01-UI-SCREENS.md`
   - 톤 노트 (색·모서리·브랜드 목소리)
3. **`apps/web/src/components/`에 구현** — [ADR-011 §2](../adr/011_scaffolding-and-app-shell-deferral.md)에 따라
   `packages/ui`는 만들지 않았다. UI 소비처가 `apps/web` 하나뿐이라 미리 가르지 않는다.
   앱 껍데기가 정해져 두 번째 소비처가 생기면 그때 토큰만 추출한다.
4. **`/design-sync`로 역방향 동기화** — `apps/web`에서 실행. 컴포넌트가 쌓일수록 충실도가 올라간다.

스캐폴딩(코드 골격)과 1·2단계는 **독립**이라 병행할 수 있다.

## 디렉토리

```
docs/ui-design/
├── README.md      이 파일
├── _reference/    claude.ai/design 화면 캡처·안내 (gitignore)
└── _archive/      (gitignore)
```

`_reference/`·`_archive/`는 루트 `.gitignore`로 제외돼 있다 — 참고용 캡처라 저장소에 넣지 않는다.

## 토큰 자리

`apps/web/src/app/globals.css`의 `@theme` 블록이 Tailwind v4 디자인 토큰 자리다.
지금은 한글 폰트 스택만 있고, 2단계 산출물을 여기에 반영한다.
