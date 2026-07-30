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
- [ ] 다음: 콘텐츠 파이프라인 파일럿(M01~03) 또는 모노레포 스캐폴딩(21 단계1)

## Git

- `main`(메인) + `develop`(작업). remote `ru-ruca/26-echoa`.
- 커밋: Conventional Commits, 트레일러 없음(사용자 규칙). 기본 브랜치 직접 커밋 회피.
