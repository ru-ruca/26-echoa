# Echoa 재구성 계획 (RN/Expo 모노레포)

> **Status**: 단계 1(모노레포 스캐폴딩) 완료 — 단계 2 대기 (2026-08-07)
> **작성일**: 2026-07-27 (2026-07-28 echoa repo로 이관)
> **스택 결정**: [ADR-009](../adr/009_stack-monorepo-decision.md) (legacy ADR-001 supersede) + [ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md)(개정: 최신 버전 손수 구성·앱 껍데기 유예) · **근거**: [네이티브 스택 리서치](../research/2026-07_native-stack-research.md) · [앱 껍데기 재검토](../research/2026-08_app-shell-reassessment.md) · [출시 타당성](20_release-feasibility.md)
> **학습 재설계 SSOT**: [19_communication-first-redesign.md](19_communication-first-redesign.md) 계승 · **학습설계 spec**: [22](22_learning-design-spec.md) · **콘텐츠 파이프라인**: [23](23_content-pipeline-spec.md)

이 문서는 "legacy SenTalk(`../../../26-SenTalk-en-study-app`)을 참고 자산으로 남기고 Echoa를 새로 구성"하는 계획의 SSOT다.

---

## 1. 왜 재구성인가

출시 타당성 조사(20번) 후 사용자가 확정한 방향:
1. **학습설계까지 재설계** — 특히 학습자료(콘텐츠 품질·저작권) + UI/UX
2. **개인 우선 → 공개 확장**
3. **네이티브 고려** — MVP 단계를 넘어섬
4. **새 프로젝트로 깔끔하게 재구성** — 현 프로젝트는 참고 자산

현 코드베이스의 근본 부채(deviceId 임시 인증·IDOR, admin 잔재 제거 후 구조, 웹 단일 앱)를 점진 수리하기보다, 검증된 모노레포 스타터에서 깨끗이 시작하는 편이 낫다는 판단.

## 2. 목표 구조 (pnpm + Turborepo) — 2026-08-07 실측 반영

```
26-echoa/ (모노레포 루트)
├── apps/
│   └── web/                  # Next.js 16.3 — 공개용, SEO
│       └── src/components/   # UI + 디자인 시스템 (/design-sync 실행 지점)
├── packages/
│   ├── core/                 # 순수 TS — fsrs·gamification 규칙·dialogue·
│   │                         #   speech-sequence·review-utils·errors + 도메인 타입
│   ├── db/                   # Drizzle 스키마(+ content_originals 격리) + seed
│   └── api/                  # tRPC v11 라우터
├── tooling/{typescript,eslint,prettier}/   # 공유 설정
├── docs/
└── tools/content-pipeline/   # Python(uv) — pnpm 워크스페이스 밖
```

**`apps/native`와 `packages/ui`는 만들지 않았다** ([ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md)):
- 앱 껍데기를 유예했다(ADR-009 §4 트리거 준수). 빈 Expo 셸은 turbo 그래프·CI·의존성만 늘리고 아무것도 검증하지 않는다.
- UI 소비처가 `apps/web` 하나뿐이라 UI 패키지를 미리 가르지 않는다. 두 번째 소비처가 생기면 그때 토큰만 추출한다.
- `packages/config` → `tooling/{typescript,eslint,prettier}`로 분리(create-t3-turbo 관례).

- **스타터를 clone하지 않았다** — [`create-t3-turbo`](https://github.com/t3-oss/create-t3-turbo) main이
  2025-12-12 이후 정체(Next 15·Expo SDK 54·better-auth 1.4-beta)라 배선 패턴만 참조하고
  버전은 착수 시점 최신으로 고정했다. 근거: [ADR-011 §1](../adr/011_scaffolding-and-app-shell-deferral.md)
- **공유 경계는 좁게**: 타입·zod·API·순수 로직만 `packages/`. **UI는 웹/앱 각각 작성**(Tamagui 전면 도입 등 억지 공유 금지 — 1인에 과함). Solito 스킵.
- `packages/api` = **tRPC v11 확정**([D-30](../adr/000_decision-log.md)) — "라우터 또는 API 클라이언트" 미확정 해소.

## 3. 자산 처리 (참고 남기기 → 이관/재작성 판별)

| 자산 | 처리 | 현 위치 |
|---|---|---|
| 콘텐츠 데이터(문장 3,622·단어 3,920·콜로케이션 5,705) | **이관**(재작성 아님) — 저작권 슬라이스 재검토·교체(실측: quote 222+movie 119=341, 9.4%. news·ted·drama 등 실출처 계열도 검토) | Neon DB + `data/` |
| FSRS·게이미피케이션·대화·리뷰 로직 | **이관** → `packages/core` | `web/src/lib/{fsrs,gamification,dialogue,speech-sequence,review-utils}.ts` |
| Drizzle 스키마 | **이관** → `packages/db` | `web/src/db/schema.ts` |
| API 라우트 10개 | **이관·재정리** → `apps/web` + `packages/api` | `web/src/app/api/*` |
| 인증(deviceId) | **재작성** — Better Auth(계정 + 다기기, IDOR 해소) | `web/src/lib/auth.ts` 폐기 |
| TTS(Web Speech) | 웹=유지, 앱=**expo-speech 재작성** | `web/src/hooks/use-speech.ts` |
| UI 컴포넌트 | 웹=이관·정리, 앱=**재작성**(RN 프리미티브) | `web/src/components/*` |
| 학습자료·학습 UI/UX | **재설계** (§5) | — |
| 조사·명세 문서(15·19·20·20a·research) | **참고 이관** | `docs/` |

## 4. 단계별 로드맵

| 단계 | 내용 | 산출 | 상태 |
|---|---|---|---|
| **0. 결정 문서화** | ADR-009 + 이 문서 + research 아카이브 | 문서 3종 | ✅ 완료 |
| **1. 모노레포 스캐폴딩** | 최신 버전으로 워크스페이스 구성, `packages/{core,db,api}` 이관, 웹 기동, C-3 적재 경로 증명 | 빌드되는 골격 | ✅ 완료 (2026-08-07) |
| **2. 웹 재구성·공개** | 학습 흐름 구현 + Better Auth + legacy 데이터 이관 + 보안헤더 + Vercel 배포 | 공개 웹(개인→공개) | 대기 |
| **3. 학습자료·UI/UX 재설계** | spec([22](22_learning-design-spec.md)) → 콘텐츠 슬라이스 교체 → UI 재구현 (§5) | 재설계된 학습 흐름 | spec 초안 완료 |
| **4. 앱 껍데기** | **TTS가 실제 제약될 때 착수.** 그 시점에 Capacitor·Expo·Flutter 래퍼를 재평가([E-06](../adr/000_decision-log.md), 기본 후보 Capacitor) + TTS·녹음·AdMob 연결 | iOS·Android 앱 | 대기(트리거 대기) |

## 5. 학습설계·UI/UX 재설계 (방향·원칙 — 상세 spec은 후속)

Spec-driven(자연어 spec → 타입/스키마 → 구현, spec이 SSOT):
- **학습자료**: 저작권 안전 + 품질 재검증. 처리 방침은 [ADR-010](../adr/010_content-copyright-and-data-model.md)(공개분 free만, 원문 격리, 위험 슬라이스 AI 재작성). [19번](19_communication-first-redesign.md)의 "일상 소통 중심" 계승.
- **UI/UX**: 기존 4단계 플로우([15_learning-flow-spec.md](15_learning-flow-spec.md)) 기준선 재검토, "발화 + 동기 설계"(쉐도잉·대화) 강화.
- **시장 근거**: AI 시대에 순수 드릴(단순 플래시카드)은 LLM에 잠식, 발화·동기 설계형은 견조([20번 §5.5](20_release-feasibility.md)). Duolingo·Babbel도 네이티브 UI + 로직 공유 구조.
- **상세 spec**: [22_learning-design-spec.md](22_learning-design-spec.md) — 흐름·세션·콘텐츠·동기·광고·화면(초안 완료).

## 6. 효율적 진행 원칙

1. **Spec 먼저** — 학습설계·UI/UX는 코드보다 spec 우선.
2. **공유 경계 좁게** — 타입·zod·API·순수 로직만 공유, UI는 2벌.
3. **create-t3-turbo에서 시작** — 인증·타입공유 재발명 회피. Solito 스킵.
4. **콘텐츠는 이관, 재작성 아님** — 3만 행 DB 유지, 저작권 슬라이스만 교체.
5. **웹 먼저, 앱은 트리거(TTS/스토어)가 왔을 때.**
6. **조사 자산 재활용** — 20·20a·research 문서를 판단 기준으로 계속 참조.
7. **AI 코딩 활용 극대화** — TS/React 단일 언어라 LLM 지원 강함, 반복 UI·테스트·마이그레이션 위임.

## 7. 결정 현황

### 확정 (2026-07-28)
- **수익 모델**: 구독 포기, **무료 + 광고**(AdMob). [D-23](../adr/000_decision-log.md). → Vercel Hobby 상업금지라 배포 시 Pro 필요, 광고 시 처리방침에 행태정보 조항 추가.
- **DB**: 개발 = 로컬 docker postgres, 프로덕션 = Neon(Drizzle 단일 스키마). **학습자료를 년 단위 CSV로 추출 → 저작권·품질 평가 → 재사용/교체 판별**. 공개분(sentences)과 원문분(content_originals)은 분리 추출, 원문 CSV는 비공개.
- **SSO**: 구글 기본 + 카카오/네이버 선택적(연동 쉬운 순: 구글→카카오→네이버). **iOS 앱 단계에서 Apple 로그인 추가**(심사 4.8).
- **앱 이름**: **Echoa**("에코아", SenTalk→Echoa 리브랜딩). [D-25](../adr/000_decision-log.md)·[name research](../research/2026-07_app-name-research.md). KIPRIS·도메인은 출시 전 확인.
- **위치**: `my-project/26-echoa`(이 repo, remote `ru-ruca/26-echoa`, main+develop). 기획·설계 문서 이관 완료(2026-07-28).
- **콘텐츠 저작권·데이터 모델**: [ADR-010](../adr/010_content-copyright-and-data-model.md) — 공개분은 저작권 free만, 원문은 `content_originals` 격리, 위험 슬라이스 AI 재작성 기본.
- **콘텐츠 확장 방법**: [23 콘텐츠 파이프라인 spec](23_content-pipeline-spec.md) — C-2 패턴 문장(substitution drill)·C-3 대화(4턴), overgenerate+재랭킹, 3단 검수 게이트.

### 남은 결정
- 착수 순서: 콘텐츠 파이프라인 파일럿(M01~03, [23](23_content-pipeline-spec.md)) vs 모노레포 스캐폴딩(단계 1).
- 가입 유도 시점, 게스트 복습 잠금 — legacy [ADR-002](../../../26-SenTalk-en-study-app/docs/adr/002_authentication.md)

## 8. 검증 (각 단계)

- 단계 1: ~~`pnpm build`·`pnpm dev` 웹/앱 동시 기동~~ → **웹 기동 + `packages/core` 타입 공유 + seed 적재 경로 증명**
  으로 조정([ADR-011](../adr/011_scaffolding-and-app-shell-deferral.md)에서 앱 껍데기를 유예했으므로 "앱 동시 기동"은
  검증할 대상이 없다). **2026-08-07 실측 결과**:
  - `pnpm typecheck`·`lint`·`test`·`build`·`format` 전부 통과. 테스트 **87개**(core 74 · db 7 · api 6)
  - `pnpm db:push` → `No changes` — legacy에서 drift로 금지였던 상태가 복구됐다
  - C-3 148행 적재 후 `select count(distinct dialogue_id), count(*) from sentences where day_type='conversation'`
    → **37 / 148**. 재실행해도 148 유지(멱등)
  - `/` 페이지가 `sentence.dialogue` → docker `echoa_db` 결과를 `buildDialogueWindow`로 잘라 렌더 (웹→api→core→db 관통)
  - `@echoa/db`(공개 진입점)에 `content_originals`가 없음을 테스트로 고정 (ADR-010 §3)
- 단계 2: Better Auth 로그인 E2E, 보안헤더(CSP·HSTS) 응답 확인, Vercel 배포 후 Lighthouse.
- 단계 3: 학습 플로우 E2E, 저작권 슬라이스 교체 완료 확인.
- 단계 4: 실기기(iOS·Android) TTS 동작, 녹음-재생, AdMob 표시 확인.

---

## 9. 다음 세션 착수 (handoff) — 2026-08-07 저녁 갱신: **단계 2 웹 재구성**

### 단계 1에서 만든 것

| 패키지 | 내용 |
|---|---|
| `apps/web` | Next.js 16.3 · React 19.2 · Tailwind 4. tRPC RSC caller + `/api/trpc` 라우트. 점검용 페이지 1개 |
| `packages/core` | legacy 순수 로직 7파일 + 도메인 타입. 테스트 74개. `gamification`은 규칙만 남기고 DB I/O 분리 |
| `packages/db` | 22테이블 clean baseline, 실 FK, Better Auth 코어 테이블, `content_originals` 격리, seed |
| `packages/api` | tRPC v11. `sentence` 라우터만 동작, 나머지 3개는 사유 적힌 스텁 |
| `tooling/*` | tsconfig · eslint(flat, ESLint 10) · prettier |

개발 DB는 공용 컨테이너 `local-pgvector-18`의 **`echoa_db`**
(`dev-env/common-docker/init/01-databases.sql`·README 등록 완료).

### 단계 2에서 할 일 (의존 순서)

1. **[22번 학습설계 spec 검토·확정](22_learning-design-spec.md)** — 지금 "초안 · 검토 대기".
   이게 나머지 거의 전부의 선행 조건이다:
   - §9 화면 명세 → 디자인 시스템 입력 ([docs/ui-design/README.md](../ui-design/README.md))
   - §3 세션 구조 → `review`·`progress` 라우터 스텁을 채울 근거
   - C-2 소비 방식([E-04](../adr/000_decision-log.md))과 미모델링 4테이블([E-05](24_deferred-legacy-tables.md))을
     **묶어서** 판정 — 둘 다 "패턴 변형을 학습 흐름에서 어떻게 쓸까"라는 같은 문제다
2. **디자인 시스템** — claude.ai/design "Create here"(코드 불필요, 지금도 가능) → 구현 → `/design-sync`.
   1번과 병행 가능하지만 §9가 흔들리면 두 번 그리게 된다.
3. **Better Auth 연결** — `packages/db`에 스키마는 이미 있다. `protectedProcedure`가 실제로 동작하게 되고
   [E-02·E-03](../adr/000_decision-log.md)(소셜 프로바이더·가입 유도 시점)이 여기서 풀린다.
4. **legacy 데이터 이관** — 문장 3,622·단어 3,920·콜로케이션 5,705.
   1번의 4테이블 판정이 선행돼야 이관 스크립트를 두 번 안 짠다. drift 실측도 필요.
5. **C-1 446건 적재** — 로더·정규화는 `packages/db/src/seed/c1-rewrites.ts`에 준비돼 있다.
   막힌 것은 **원문**이다 — `content_originals.original_text_en`이 legacy Neon DB(또는 gitignore된
   `tools/content-pipeline/data/work/c1_full_seeds.jsonl`)에만 있어 4번과 같이 처리한다.

### 착수 프롬프트 (복붙용)

> Echoa 단계 2를 시작한다. 단계 1(모노레포 스캐폴딩)은 끝났다 —
> `docs/project-review/21_rebuild-plan.md` §9와 `docs/adr/011_scaffolding-and-app-shell-deferral.md`를 먼저 읽어라.
> 먼저 `docs/project-review/22_learning-design-spec.md`를 검토해 확정 상태로 올린다.
> 특히 §9 화면 명세, §3 세션 구조, 그리고 미결정 두 개를 **묶어서** 판정한다 —
> C-2 변형 소비 방식(23 §9 / E-04)과 미모델링 legacy 테이블 4개(docs/project-review/24_deferred-legacy-tables.md / E-05).
> 둘 다 "패턴 변형을 학습 흐름에서 어떻게 쓸까"라는 같은 문제다.

---

## 9-0. 이전 handoff (2026-08-07 오전, 스캐폴딩 착수 시점)

### 콘텐츠 파이프라인은 여기서 멈춘다 (완료·보류 구분)

**완료**: 파일럿 3트랙 + C-1 확대. 산출 **1,122건** — C-1 446(`ai_rewritten`) · C-2 528 · C-3 대화 37(148행).
구현·리포트는 [tools/content-pipeline/](../../tools/content-pipeline/README.md),
종합 판정은 [11 결론](../../tools/content-pipeline/reports/11_pilot_conclusion.md) ·
[17 C-1 확대 요약](../../tools/content-pipeline/reports/17_c1_full_summary.md).

**출시 전제였던 저작권 처리(C-1)가 끝났다** — ADR-010 위험 슬라이스 616건을 선별해 426건 재작성,
인간 검수에서 저작권 사유 탈락 0건. 콘텐츠는 지금 상태로 출시 가능하다.

**보류(고도화로 이월)**: ① M17 문어체 커넥터 씨앗 교체 7건 ② B1·B2 어휘 목록 보강 ③ 월 단위 확대(M04~48).
셋 다 출시를 막지 않는다. 특히 ③은 [23 §9 미결정](23_content-pipeline-spec.md)이 선행 조건이다 —
**C-2 변형을 학습 흐름에서 어떻게 쓸지 모른 채 48개월분을 만들면 잘못된 형태를 대량 생산**하게 된다.
앱이 실제로 콘텐츠를 소비하는 모습을 본 뒤 확대한다.

### 왜 스캐폴딩이 먼저인가

1. **코드가 콘텐츠에 의존하지 않는다** — 스캐폴딩은 워크스페이스 구성 + legacy TS 로직 이관이라 독립적이다.
2. **콘텐츠는 코드에 의존한다** — 23 §9의 미결정이 앱 흐름에서만 풀린다.
3. 기존 커리큘럼 3,622문장이 이미 있고 파일럿 1,122건이 더해졌다 — year1 학습에 충분하다.
4. 21 §6 원칙("웹 먼저")과 19번의 "48개월 일괄 생성 금지"에 부합한다.

### 스캐폴딩 단계에 추가된 요건 — 파이프라인 산출물 적재

`packages/db` 스키마에 ADR-010을 반영할 때 아래를 함께 고려한다:

| 산출물 | 적재 대상 | 2026-08-07 실제 처리 |
|---|---|---|
| `c1_final.jsonl` 27 + `c1_full_final.jsonl` 419 | `sentences.text_en` 교체, `content_origin='ai_rewritten'` | **로더·정규화만 완료**(`seed/c1-rewrites.ts`, 446건 확인). 원문이 legacy DB에만 있어 적재는 단계 2 |
| `c2_final.jsonl` 528 | 신규 문장 (`ai_generated`) | **보류 확정** — 23 §9 미결정 + `id` 발번 규칙 없음 |
| `c3_rows_final.jsonl` 148행 | `day_type='conversation'` 기존 스키마 그대로 | **적재 완료** (대화 37개 / 148행). `content_origin='ai_generated'` 주입 |

`content_origin` enum(`self_authored`·`ai_generated`·`ai_rewritten`·`public_domain`)은 ADR-010 §2 그대로.
적재 스크립트는 `tools/content-pipeline/`이 아니라 `packages/db`의 seed로 뒀다
(파이프라인은 생성·검수 도구, 적재는 앱 자산).

**적재하며 확인한 것**:
- 두 C-1 파일은 **스키마가 다르다** — 파일럿엔 `day_type`·`cefr_level`·`month`가 없고 `review.external`이 있으며
  `source_cand`가 `int | "reviewer_alternative"`다. 정규화 레이어를 뒀다.
- 적재 순서 제약은 **C-1 → C-2 → C-3** (C-2 씨앗 25개가 C-1 재작성 텍스트를 패턴 고정부로 쓴다).
- `c3_rows_preview.jsonl`은 `_final`과 바이트 동일한 검증 산출물이라 쓰지 않는다.

---

## 9-1. 이전 handoff (2026-07-28, 콘텐츠 착수 시점)

**여기까지 완료(2026-07-28)**: 스택 결정(ADR-009)·저작권 데이터모델(ADR-010)·재구성 계획(이 문서)·학습설계 spec(22)·콘텐츠 파이프라인 spec(23)·조사 아카이브 4종. legacy repo에 `legacy-nextjs-pwa` 태그로 재구성 직전 시점 보존. `quote`·`movie` 저작권 슬라이스 실측(341개=9.4%). **echoa repo 생성 + 문서 이관 완료.**

### 착수 전 선결 결정 (§7 참조) — 전부 확정
- [x] 수익=광고(포인트·자발광고·기부), DB=docker+Neon+CSV, SSO=구글+카카오/네이버, 저작권=ADR-010
- [x] **앱 이름 = Echoa**, repo `26-echoa`(remote `ru-ruca/26-echoa`, main+develop). KIPRIS·도메인만 출시 전 확인
- [ ] **착수 순서만 남음**: 콘텐츠 파이프라인 파일럿([23](23_content-pipeline-spec.md), M01~03) vs 모노레포 스캐폴딩(단계 1)

### 작업 환경 권장

**VS Code workspace에 두 폴더를 함께 열 것** — `26-echoa`(첫 폴더, 작업 대상) + `26-SenTalk-en-study-app`(legacy 참조). 단계 1이 legacy의 `web/src/lib/*`·`web/src/db/schema.ts`를 읽어 `packages/`로 옮기는 작업이라 참조가 필수. 이관이 끝나면 echoa 단독으로 좁혀도 됨.

### 다음 세션 착수 프롬프트 (복붙용)

**옵션 A — 콘텐츠 파이프라인 파일럿** ([23](23_content-pipeline-spec.md), 콘텐츠 우선):
> Echoa 콘텐츠 파이프라인 파일럿을 착수한다. spec은 `docs/project-review/23_content-pipeline-spec.md`, 제약은 `docs/adr/010_content-copyright-and-data-model.md`. 순서: ① legacy DB(`../26-SenTalk-en-study-app`, Neon)에서 M01~03 문장·허용 어휘를 추출 ② 허용 어휘 목록 구성(month 누적 + CEFR) ③ C-2(substitution drill, 씨앗당 5~8) 생성 프롬프트와 검수 게이트(하드필터→LLM judge→인간 5~10%)를 설계·구현 ④ C-1 저작권 위험 씨앗(quote·movie 등 341개) 우선 처리. 성공 기준은 23 §5(judge ≥4/5, 인간 합격 ≥90%, 중복 <2%, 씨앗 유사도 초과 0건). 48개월 일괄 생성·생성물 재씨앗 금지.

**옵션 B — 모노레포 스캐폴딩** ([21 단계1](21_rebuild-plan.md), 코드 골격 우선):
> Echoa 모노레포를 스캐폴딩한다. 결정은 `docs/adr/009_stack-monorepo-decision.md`, 계획은 `docs/project-review/21_rebuild-plan.md` §2·§3. create-t3-turbo 기반으로 이 repo(`26-echoa`) 루트에 `apps/{web,native}`·`packages/{db,core,api,config}`를 만들고, legacy(`../26-SenTalk-en-study-app`)의 `web/src/lib/{fsrs,gamification,dialogue,speech-sequence,review-utils}.ts`를 `packages/core`로, `web/src/db/schema.ts`를 `packages/db`로 이관하라. DB는 개발 docker + 프로덕션 Neon, 스키마에 ADR-010(`content_originals` 격리·`content_origin` 필드)을 반영. 공유 경계는 좁게(UI는 웹/앱 각각), Solito 스킵.

> ↑ **이것이 2026-08-07 현재 착수할 작업이다.** 위 §9의 판단 근거와 추가 요건(파이프라인 산출물 적재)을 함께 볼 것.

### 착수 전 사전 점검(선택)
- `packages/core` 이관 대상(fsrs·gamification·dialogue·review-utils)의 외부 의존성 점검 — 순수 TS인지 확인해 이관 난이도 사전 파악.
- 저작권 위험 슬라이스 실제 문장 샘플 검토 → 재작성/교체/유지 판별 기준 구체화.
