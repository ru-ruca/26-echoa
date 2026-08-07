# Echoa — 영어 학습 앱 (구 SenTalk 재구성)

> **상태**: 모노레포 스캐폴딩 완료(2026-08-07) — 21 단계 2(웹 재구성) 대기.
> **방향**: Next.js 모노레포로 **웹 먼저**. 앱 껍데기는 TTS 제약이 실제로 보일 때 결정([ADR-011](docs/adr/011_scaffolding-and-app-shell-deferral.md)). 일상 소통 중심(말하기 내장), 무료+광고.
> **legacy(참고 자산)**: `../26-SenTalk-en-study-app` (Next.js PWA 원형, git 태그 `legacy-nextjs-pwa`). legacy-only 문서(ADR-001~008·트랙18·archive 등)는 그 repo 참조.

---

## 확정 사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 앱 이름 | **Echoa** | [D-25](docs/adr/000_decision-log.md), [name research](docs/research/2026-07_app-name-research.md) |
| 스택 | Next.js 16.3 + pnpm/Turborepo 모노레포, tRPC v11, Drizzle | [ADR-009](docs/adr/009_stack-monorepo-decision.md) + [ADR-011](docs/adr/011_scaffolding-and-app-shell-deferral.md) |
| 앱 껍데기 | **유예** — TTS 제약 실측 후 결정(기본 후보 Capacitor). Flutter 앱은 배제 | [ADR-011](docs/adr/011_scaffolding-and-app-shell-deferral.md), [D-29](docs/adr/000_decision-log.md) |
| 수익 | 무료 + 광고(포인트·자발광고·소액기부, 학습은 안 막음) | [22 §6](docs/project-review/22_learning-design-spec.md) |
| DB | 개발 docker(`echoa_db`) + 프로덕션 Neon, 년 단위 CSV 평가 | [21 §7](docs/project-review/21_rebuild-plan.md) |
| SSO | 구글 기본 + 카카오/네이버 선택(앱 단계 Apple) | [21 §7](docs/project-review/21_rebuild-plan.md) |
| 저작권 | 공개분 free만, 원문 격리, 위험 슬라이스 AI 재작성 | [ADR-010](docs/adr/010_content-copyright-and-data-model.md) |

## 디렉토리 구조

```
26-echoa/
├── apps/web/                 # Next.js 16.3 · React 19.2 · Tailwind 4 (UI·디자인 시스템도 여기)
├── packages/
│   ├── core/                 # 순수 TS — fsrs·gamification 규칙·dialogue·speech-sequence·review-utils
│   ├── db/                   # Drizzle 스키마(+ content_originals 격리) + seed
│   └── api/                  # tRPC v11 라우터
├── tooling/{typescript,eslint,prettier}/
├── docs/                     # 기획·설계·조사·UI 디자인
└── tools/content-pipeline/   # Python(uv) — pnpm 워크스페이스 밖
```

**`apps/native`·`packages/ui`는 없다** — 앱 껍데기를 유예했고 UI 소비처가 하나뿐이라 미리 가르지 않는다([ADR-011](docs/adr/011_scaffolding-and-app-shell-deferral.md)).
공유 경계는 좁게(타입·zod·API·순수 로직만). `packages/core`의 런타임 의존은 `ts-fsrs` 하나뿐이다.

### 개발 명령

```bash
pnpm dev          # 웹 http://localhost:3000
pnpm typecheck    # pnpm lint / pnpm test / pnpm build / pnpm format
pnpm db:push      # 스키마 → echoa_db   (db:studio · db:generate · db:seed)

# 개발 DB — 공용 컨테이너 (dev-env/common-docker)
cd ../../dev-env/common-docker && docker compose up -d
```

각 앱·패키지의 `.env.example`을 `.env`로 복사해 쓴다.

## 주요 문서 (SSOT)

| 문서 | 경로 | 설명 |
|------|------|------|
| **재구성 계획** | [docs/project-review/21_rebuild-plan.md](docs/project-review/21_rebuild-plan.md) | 모노레포 구조·자산 이관·로드맵 |
| **학습설계·UI/UX spec** | [docs/project-review/22_learning-design-spec.md](docs/project-review/22_learning-design-spec.md) | 흐름·세션·콘텐츠·동기·수익·4기능 확장·화면 |
| **콘텐츠 파이프라인 spec** | [docs/project-review/23_content-pipeline-spec.md](docs/project-review/23_content-pipeline-spec.md) | C-2 패턴 문장·C-3 대화 생성·검수 게이트 |
| 학습 재설계 SSOT(계승) | [docs/project-review/19_communication-first-redesign.md](docs/project-review/19_communication-first-redesign.md) | 5축(말하기·회화·이정표·뜻암기0·세션) |
| 학습 플로우 명세(계승) | [docs/project-review/15_learning-flow-spec.md](docs/project-review/15_learning-flow-spec.md) | 4단계 아코디언 기준선 |
| 스택 결정 | [docs/adr/009_stack-monorepo-decision.md](docs/adr/009_stack-monorepo-decision.md) | RN/Expo 모노레포, Flutter 배제 |
| **스캐폴딩·앱 껍데기 유예** | [docs/adr/011_scaffolding-and-app-shell-deferral.md](docs/adr/011_scaffolding-and-app-shell-deferral.md) | ADR-009 개정 — 최신 버전 손수 구성, 껍데기 유예, tRPC 확정 |
| 저작권·데이터모델 | [docs/adr/010_content-copyright-and-data-model.md](docs/adr/010_content-copyright-and-data-model.md) | 공개분 free·원문 격리 |
| UI 디자인 진행 순서 | [docs/ui-design/README.md](docs/ui-design/README.md) | claude.ai/design 두 경로·전제·순서 |
| 이월: legacy 테이블 4개 | [docs/project-review/24_deferred-legacy-tables.md](docs/project-review/24_deferred-legacy-tables.md) | quizzes 934 등 — 22번 검토 때 판정 |
| 출시 타당성 | [docs/project-review/20_release-feasibility.md](docs/project-review/20_release-feasibility.md) | 경로·서버·보안·수익 조사 |
| 결정 로그 | [docs/adr/000_decision-log.md](docs/adr/000_decision-log.md) | 재구성 결정(D-22~), 남은 결정(E-02~E-06) |

> 원자료 조사는 [docs/research/](docs/research/) (스택·출시타당성·이름·콘텐츠확장·앱껍데기 재검토).

## 개발 현황 / 다음

- [x] 기획·설계·조사 문서 이관 (SenTalk → echoa)
- [x] 콘텐츠 확장 조사(C-2/C-3) → [23 spec](docs/project-review/23_content-pipeline-spec.md)
- [x] 콘텐츠 파이프라인 파일럿 착수(D-26·D-27) — Phase 0 완료: 추출·허용 어휘·baseline 실측 → [tools/content-pipeline/](tools/content-pipeline/README.md)
- [x] 파일럿 Phase 1(C-1 재작성 27개) **완료** — 인간 검수 100% 채택(수정 11), 23 §5 전 기준 충족. 확정본 [output/c1_adopted.jsonl](tools/content-pipeline/output/c1_adopted.jsonl), [지표](tools/content-pipeline/reports/04_c1_pilot_metrics.md), 교훈 [style_lessons](tools/content-pipeline/prompts/style_lessons.md)
- [x] C-1 외부 AI 교차 검토 반영 — 최종본 [output/c1_final.jsonl](tools/content-pipeline/output/c1_final.jsonl) (유지 19·외부수정 5·대안교체 3)
- [x] 파일럿 Phase 2(C-2 패턴 문장, 씨앗 145×6=870) 생성·게이트·채점 완료 — 게이트 738 통과(패턴파괴 0), judge 전체 3.95 / **적격 씨앗분 4.15**. [지표](tools/content-pipeline/reports/05_c2_pilot_metrics.md)
- [x] C-2 인간 검수·씨앗결함 처리 완료 — 확정본 [output/c2_final.jsonl](tools/content-pipeline/output/c2_final.jsonl) **528건/씨앗 116개**, 23 §5 조건부 통과. [최종 요약](tools/content-pipeline/reports/07_c2_final_summary.md)
- [x] 파일럿 Phase 3(C-3 대화 50개) 생성·게이트·채점 완료 — 게이트·스키마 검증 100%, **마지막 턴 A1 유지 50/50**, judge 3.74(A군 4.10/B군 3.46). [지표](tools/content-pipeline/reports/08_c3_pilot_metrics.md)
- [x] C-3 인간 검수·확정 완료 — [output/c3_final.jsonl](tools/content-pipeline/output/c3_final.jsonl) **대화 37개/148행**, 마지막 턴 A1 50/50·스키마 적재 검증 통과. [최종 요약](tools/content-pipeline/reports/10_c3_final_summary.md)
- [x] 어휘 목록 보강(546→912, 레벨별 A1~B2 구축) · 씨앗 적격성 자동 분류(무익 씨앗 72% 사전 차단)
- [x] **C-1 확대 생성 완료** — 위험 계열 616건 선별 → 재작성 426씨앗 × 3후보 = 1,278건, 게이트 100%. [지표](tools/content-pipeline/reports/15_c1_full_metrics.md)
- [x] **C-1 확대 완료** — 검수 122씨앗 채택 94%·저작권 탈락 0건, 확정 [c1_full_final.jsonl](tools/content-pipeline/output/c1_full_final.jsonl) **419건**(파일럿 27 포함 총 446). [최종 요약](tools/content-pipeline/reports/17_c1_full_summary.md)
- [x] **콘텐츠 파이프라인 종료** — 산출 1,122건(C-1 446·C-2 528·C-3 148행). 출시 전제(저작권)는 해소됨. [handoff: 21 §9](docs/project-review/21_rebuild-plan.md)
- [x] **스택 전면 재검토**(2026-08-07) — create-t3-turbo 8개월 정체 + Flutter 경험 전제 변화를 확인하고 선택지 5개 비교 → [research](docs/research/2026-08_app-shell-reassessment.md) · [ADR-011](docs/adr/011_scaffolding-and-app-shell-deferral.md)
- [x] **모노레포 스캐폴딩(21 단계1) 완료** — `apps/web` + `packages/{core,db,api}` + `tooling/*`.
      테스트 87개(core 74·db 7·api 6), `db:push` 정상 복구(22테이블), C-3 148행 적재로 웹→api→core→db 관통 확인.
      [검증 결과: 21 §8](docs/project-review/21_rebuild-plan.md)
- [ ] **다음: 21 단계 2 — [22번 학습설계 spec 검토·확정](docs/project-review/22_learning-design-spec.md)부터.**
      §9 화면 명세가 디자인 시스템의 입력이고, §3 세션 구조가 `review`·`progress` 라우터 스텁을 채울 근거다.
      착수 순서는 [21 §9](docs/project-review/21_rebuild-plan.md)

### 이월 목록

| # | 항목 | 선행 조건 |
|---|------|-----------|
| 1 | 앱 껍데기 확정(Capacitor/Expo/Flutter 래퍼) — [E-06](docs/adr/000_decision-log.md) | 웹 학습 흐름 완성 → TTS 제약 실측 |
| 2 | C-2 528건 적재 방식 — [E-04](docs/project-review/23_content-pipeline-spec.md) | 22번 spec 확정 |
| 3 | 미모델링 legacy 테이블 4개 존폐 — [E-05](docs/project-review/24_deferred-legacy-tables.md) | 2번과 **묶어서** 판정 (같은 문제 공간) |
| 4 | C-1 446건 적재 + `content_originals` 격리 | legacy Neon 접속 (로더·정규화는 준비됨) |
| 5 | legacy 데이터 이관(문장 3,622·단어 3,920·콜로케이션 5,705) | 3번 판정 · drift 실측 |
| 6 | Better Auth 연결 → 소셜 프로바이더([E-02](docs/adr/000_decision-log.md))·가입 유도 시점([E-03](docs/adr/000_decision-log.md)) | 스키마는 이미 있음 |
| 7 | M17 씨앗 교체 7건(원문 그대로 남아 있음) · B1·B2 어휘 보강 · 월 단위 확대(M04~48) | 7의 앞 항목은 공개 적재 전, 나머지는 2번 |
| 8 | `rate-limit` Upstash 전환 | 서버리스 배포 시 |

## Git

- `main`(메인) + `develop`(작업). remote `ru-ruca/26-echoa`.
- 커밋: Conventional Commits, 트레일러 없음(사용자 규칙). 기본 브랜치 직접 커밋 회피.
