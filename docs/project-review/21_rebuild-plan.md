# Echoa 재구성 계획 (RN/Expo 모노레포)

> **Status**: 계획 확정 — 스캐폴딩 착수 대기
> **작성일**: 2026-07-27 (2026-07-28 echoa repo로 이관)
> **스택 결정**: [ADR-009](../adr/009_stack-monorepo-decision.md) (legacy ADR-001 supersede) · **근거**: [네이티브 스택 리서치](../research/2026-07_native-stack-research.md) · [출시 타당성](20_release-feasibility.md)
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

## 2. 목표 구조 (create-t3-turbo 기반, pnpm + Turborepo)

```
26-echoa/ (모노레포 루트)
├── apps/
│   ├── web/        # Next.js 16 — 공개용, SEO. 기존 web/ 이관·정리
│   └── native/     # Expo (RN) — iOS·Android. TTS·녹음 네이티브
├── packages/
│   ├── db/         # Drizzle 스키마 (기존 schema.ts 이관)
│   ├── api/        # tRPC 라우터 또는 API 클라이언트 (기존 api/ 로직)
│   ├── core/       # fsrs·gamification·dialogue·review-utils (순수 TS 이관)
│   └── config/     # tsconfig·eslint 공유
```

- 스타터: [`create-t3-turbo`](https://github.com/t3-oss/create-t3-turbo) — Better Auth·Drizzle·tRPC·NativeWind 세팅됨.
- **공유 경계는 좁게**: 타입·zod·API 클라이언트·순수 로직만 `packages/`. **UI는 웹/앱 각각 작성**(Tamagui 전면 도입 등 억지 공유 금지 — 1인에 과함). Solito 스킵.

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
| **1. 모노레포 스캐폴딩** | create-t3-turbo로 새 repo, `packages/{db,core,api}` 이관, 웹 기동 | 빌드되는 골격 | 대기 |
| **2. 웹 재구성·공개** | Next.js 웹 이관·정리 + Better Auth + 보안헤더 + Vercel 배포 | 공개 웹(개인→공개) | 대기 |
| **3. 학습자료·UI/UX 재설계** | spec([22](22_learning-design-spec.md)) → 콘텐츠 슬라이스 교체 → UI 재구현 (§5) | 재설계된 학습 흐름 | spec 초안 완료 |
| **4. Expo 앱** | native 앱 + expo-speech TTS + 녹음. **TTS가 실제 제약될 때 착수** | iOS·Android 앱 | 대기(트리거 대기) |

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

- 단계 1: `pnpm build`·`pnpm dev` 웹/앱 동시 기동, `packages/core` 타입 공유 확인.
- 단계 2: Better Auth 로그인 E2E, 보안헤더(CSP·HSTS) 응답 확인, Vercel 배포 후 Lighthouse.
- 단계 3: 학습 플로우 E2E, 저작권 슬라이스 교체 완료 확인.
- 단계 4: expo-speech TTS 실기기(iOS·Android) 동작, 녹음-재생 확인.

---

## 9. 다음 세션 착수 (handoff)

**여기까지 완료(2026-07-28)**: 스택 결정(ADR-009)·저작권 데이터모델(ADR-010)·재구성 계획(이 문서)·학습설계 spec(22)·콘텐츠 파이프라인 spec(23)·조사 아카이브 4종. legacy repo에 `legacy-nextjs-pwa` 태그로 재구성 직전 시점 보존. `quote`·`movie` 저작권 슬라이스 실측(341개=9.4%). **echoa repo 생성 + 문서 이관 완료.**

### 착수 전 선결 결정 (§7 참조) — 전부 확정
- [x] 수익=광고(포인트·자발광고·기부), DB=docker+Neon+CSV, SSO=구글+카카오/네이버, 저작권=ADR-010
- [x] **앱 이름 = Echoa**, repo `26-echoa`(remote `ru-ruca/26-echoa`, main+develop). KIPRIS·도메인만 출시 전 확인
- [ ] **착수 순서만 남음**: 콘텐츠 파이프라인 파일럿([23](23_content-pipeline-spec.md), M01~03) vs 모노레포 스캐폴딩(단계 1)

### 다음 세션 착수 프롬프트 (복붙용)

**옵션 A — 모노레포 스캐폴딩(단계 1)**:
> Echoa(구 SenTalk)를 RN/Expo + Next.js 모노레포로 재구성한다. 결정·계획은 `docs/adr/009_stack-monorepo-decision.md`·`010_content-copyright-and-data-model.md`·`docs/project-review/21_rebuild-plan.md` 참고. create-t3-turbo 기반으로 이 repo(`26-echoa`) 루트에 모노레포를 스캐폴딩하고, legacy(`../26-SenTalk-en-study-app`)의 `web/src/lib/{fsrs,gamification,dialogue,review-utils}.ts`·`web/src/db/schema.ts`를 `packages/{core,db}`로 이관하는 계획을 세워라. DB는 개발 docker + 프로덕션 Neon, 콘텐츠 데이터 모델은 ADR-010(공개분 free만, `content_originals` 격리)을 반영할 것.

**옵션 B — 학습설계·UI/UX spec(단계 3 선행)**:
> Echoa(구 SenTalk) 학습설계·UI/UX를 재설계한다. `docs/project-review/19_communication-first-redesign.md`(일상 소통 중심)·`15_learning-flow-spec.md`(4단계 플로우)를 기준선으로, `20_release-feasibility.md §5.5`(발화+동기 설계) 방향을 반영한 학습 흐름 spec을 자연어로 작성하라. 콘텐츠 처리 방침은 `docs/adr/010_content-copyright-and-data-model.md`(공개분 free만·원문 격리·위험 슬라이스 AI 재작성)를 준수 — 실측 341개(9.4%)+news·ted·drama 계열.

### 현 repo에서 남은 무후회 작업(선택, 새 repo 없이 가능)
- 저작권 위험 슬라이스(quote·movie·news·ted·drama 등)의 실제 문장 샘플 검토 → 재생성/교체/유지 판별 기준 마련.
- `packages/core` 이관 대상(fsrs·gamification 등)의 외부 의존성 점검(순수 TS 여부 확인 — 이관 난이도 사전 파악).
