# Echoa 문서

Echoa(구 SenTalk) 재구성의 기획·설계·조사 문서. 2026-07-28 SenTalk repo에서 이관.

## 구조

- **project-review/** — 계획·spec
  - `21_rebuild-plan.md` 재구성 계획(SSOT) · `22_learning-design-spec.md` 학습설계·UI/UX · `23_content-pipeline-spec.md` 콘텐츠 생성 파이프라인
  - `19_communication-first-redesign.md` 학습 재설계 5축(계승) · `15_learning-flow-spec.md` 4단계 플로우(계승)
  - `20_release-feasibility.md`·`20a_release-comparison-tables.md` 출시 타당성
- **adr/** — 결정 기록: `000_decision-log.md`(인덱스) · `009`(스택) · `010`(저작권·데이터모델)
- **research/** — 원자료 조사 아카이브: 스택·출시타당성·이름·콘텐츠확장

## 이관·링크 정책

- 이 문서들은 SenTalk repo에서 복사됐다. **legacy 전체 git 이력은 SenTalk repo**(`../26-SenTalk-en-study-app`, 태그 `legacy-nextjs-pwa`)에 보존.
- 문서 내 링크 중 **legacy-only 대상**(ADR-001~008, `data-tracks/18`, `archive/`, `phase4/`, `analysis/`, `research/2026-07_speaking-redesign-research.md` 등)은 이관하지 않았으므로 **SenTalk repo에서 참조**한다. echoa로 함께 온 문서 간 링크는 정상 동작.
- 앞으로의 기획·설계·결정은 **이 repo가 SSOT**.
