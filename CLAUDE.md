# Echoa — 영어 학습 앱 (구 SenTalk 재구성)

> **상태**: 재구성 착수 — 기획·설계 문서 이관 완료(2026-07-28), 코드 스캐폴딩 전.
> **방향**: RN/Expo + Next.js **모노레포**로 새로 구축. 일상 소통 중심(말하기 내장), 무료+광고.
> **legacy(참고 자산)**: `../26-SenTalk-en-study-app` (Next.js PWA 원형, git 태그 `legacy-nextjs-pwa`). legacy-only 문서(ADR-001~008·트랙18·archive 등)는 그 repo 참조.

---

## 확정 사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 앱 이름 | **Echoa** | [D-25](docs/adr/000_decision-log.md), [name research](docs/research/2026-07_app-name-research.md) |
| 스택 | RN/Expo + Next.js 모노레포 | [ADR-009](docs/adr/009_stack-monorepo-decision.md) |
| 수익 | 무료 + 광고(포인트·자발광고·소액기부, 학습은 안 막음) | [22 §6](docs/project-review/22_learning-design-spec.md) |
| DB | 개발 docker + 프로덕션 Neon, 년 단위 CSV 평가 | [21 §7](docs/project-review/21_rebuild-plan.md) |
| SSO | 구글 기본 + 카카오/네이버 선택(앱 단계 Apple) | [21 §7](docs/project-review/21_rebuild-plan.md) |
| 저작권 | 공개분 free만, 원문 격리, 위험 슬라이스 AI 재작성 | [ADR-010](docs/adr/010_content-copyright-and-data-model.md) |

## 디렉토리 구조 (예정)

```
26-echoa/
├── apps/
│   ├── web/        # Next.js 16 — 공개용, SEO
│   └── native/     # Expo (RN) — iOS·Android, TTS·녹음
├── packages/
│   ├── db/         # Drizzle 스키마 (+ content_originals 격리)
│   ├── core/       # fsrs·gamification·dialogue·review-utils (순수 TS)
│   ├── api/        # tRPC 라우터 / API 클라이언트
│   └── config/     # tsconfig·eslint 공유
└── docs/           # 기획·설계·조사 (이관 완료)
```

기반: [create-t3-turbo](https://github.com/t3-oss/create-t3-turbo)(Better Auth·Drizzle·tRPC·NativeWind). 공유 경계는 좁게(타입·zod·API·순수 로직만, UI는 웹/앱 각각).

## 주요 문서 (SSOT)

| 문서 | 경로 | 설명 |
|------|------|------|
| **재구성 계획** | [docs/project-review/21_rebuild-plan.md](docs/project-review/21_rebuild-plan.md) | 모노레포 구조·자산 이관·로드맵 |
| **학습설계·UI/UX spec** | [docs/project-review/22_learning-design-spec.md](docs/project-review/22_learning-design-spec.md) | 흐름·세션·콘텐츠·동기·수익·4기능 확장·화면 |
| **콘텐츠 파이프라인 spec** | [docs/project-review/23_content-pipeline-spec.md](docs/project-review/23_content-pipeline-spec.md) | C-2 패턴 문장·C-3 대화 생성·검수 게이트 |
| 학습 재설계 SSOT(계승) | [docs/project-review/19_communication-first-redesign.md](docs/project-review/19_communication-first-redesign.md) | 5축(말하기·회화·이정표·뜻암기0·세션) |
| 학습 플로우 명세(계승) | [docs/project-review/15_learning-flow-spec.md](docs/project-review/15_learning-flow-spec.md) | 4단계 아코디언 기준선 |
| 스택 결정 | [docs/adr/009_stack-monorepo-decision.md](docs/adr/009_stack-monorepo-decision.md) | RN/Expo 모노레포, Flutter 배제 |
| 저작권·데이터모델 | [docs/adr/010_content-copyright-and-data-model.md](docs/adr/010_content-copyright-and-data-model.md) | 공개분 free·원문 격리 |
| 출시 타당성 | [docs/project-review/20_release-feasibility.md](docs/project-review/20_release-feasibility.md) | 경로·서버·보안·수익 조사 |
| 결정 로그 | [docs/adr/000_decision-log.md](docs/adr/000_decision-log.md) | 재구성 결정(D-22~) |

> 원자료 조사는 [docs/research/](docs/research/) (스택·출시타당성·이름·콘텐츠확장).

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
- [ ] **다음: 모노레포 스캐폴딩(21 단계1)** — 코드가 콘텐츠에 의존하지 않고, 반대로 [23 §9 미결정](docs/project-review/23_content-pipeline-spec.md)(C-2 변형의 학습 흐름 소비 방식)이 앱에서만 풀린다
- [ ] 고도화 이월: M17 씨앗 교체 7건 · B1·B2 어휘 보강 · 월 단위 확대(M04~48)
- [ ] 이후: 모노레포 스캐폴딩(21 단계1)

## Git

- `main`(메인) + `develop`(작업). remote `ru-ruca/26-echoa`.
- 커밋: Conventional Commits, 트레일러 없음(사용자 규칙). 기본 브랜치 직접 커밋 회피.
