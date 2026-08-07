# Decision Log — Echoa

> Echoa 재구성 이후 주요 결정 인덱스. **D-01~D-21은 legacy(SenTalk) 결정**으로, 원본 [../26-SenTalk-en-study-app/docs/adr/000_decision-log.md] 참조(git 태그 `legacy-nextjs-pwa`). 여기는 재구성 결정(D-22~)부터 계승·기록.
> 최종 업데이트: 2026-08-07

---

## 결정 완료 (재구성 이후)

| # | 결정 | 선택 | 근거 | 날짜 | 문서 |
|---|------|------|------|------|-----|
| D-22 | 네이티브 스택 + 구조 | **RN/Expo + Next.js 웹 모노레포**(create-t3-turbo). Flutter 배제. 착수 트리거=TTS | Flutter는 웹 SEO 치명적(canvas)·TS 자산 재사용 0·Dart 학습·AI 코딩 약세. RN/Expo는 언어·타입·로직 재사용 + 웹 공유 | 2026-07-27 | [009](009_stack-monorepo-decision.md) |
| D-23 | 수익 모델 | **무료 + 광고**(포인트·자발광고·소액기부). 구독 포기. **학습 자체는 안 막음** | 교육앱 구독 기저율 낮음. 강제 전면광고는 리텐션 해침 → opt-in/포인트. 기부는 Vercel Pro·웹결제 주의 | 2026-07-28 | [22 §6](../project-review/22_learning-design-spec.md) |
| D-24 | 콘텐츠 저작권 + 데이터모델 | 공개분 free만(자작·AI·PD·재작성). 원문 `content_originals` 격리(공개 API·git·CSV·백업 제외). 위험 슬라이스 AI 재작성 | 실측 341개(9.4%)+news·ted·drama. 광고=영리라 인용 항변 불리, 출처표시는 면책 아님. 표현 대체가 안전 | 2026-07-28 | [010](010_content-copyright-and-data-model.md) |
| D-25 | 앱 이름 | **Echoa**("에코아"). SenTalk→Echoa 리브랜딩 | 3라운드 조사(ShadowLoop·Speaky·Sayly 배제, Echoly 발음약점→Echoa). 언어학습 동명 없음, 발음 용이. KIPRIS·도메인 출시 전 확인 | 2026-07-28 | [name research](../research/2026-07_app-name-research.md) |
| D-26 | 착수 순서 (E-01 해소) | **콘텐츠 파이프라인 파일럿 먼저**, 모노레포 스캐폴딩은 후속 | 콘텐츠가 학습의 핵심 + C-1 재작성이 출시 전제. 파이프라인은 모노레포와 독립(`tools/content-pipeline/`) | 2026-07-30 | [23](../project-review/23_content-pipeline-spec.md) |
| D-27 | 파일럿 생성·채점 수행 방식 | **Claude Code 세션(구독)이 생성·judge 수행**, 스크립트는 결정적 작업만. API 키 불요 | 추가 비용 0, 파일럿 규모에 충분. 입출력 JSONL 계약 유지로 대량 확대 시 Batches API 교체 가능. 생성/채점은 별도 서브에이전트로 분리(self-review bias 완화) | 2026-07-30 | [pipeline README](../../tools/content-pipeline/README.md) |
| D-28 | 스캐폴딩 실행 방식 | **create-t3-turbo를 clone하지 않고 최신 버전으로 손수 구성**(배선만 참조) | 스타터 main이 2025-12-12 이후 정체 — Next 15·Expo SDK 54·better-auth 1.4-beta 고정이라 legacy(Next 16.2.3)보다 뒤로 감. 스타터를 고른 이유는 배선 패턴이지 버전이 아님 | 2026-08-07 | [011](011_scaffolding-and-app-shell-deferral.md) |
| D-29 | 앱 껍데기 | **유예** — `apps/web`+`packages/*`만 먼저. TTS 제약이 실제로 보일 때 Expo·Capacitor·Flutter 래퍼를 재평가(기본 후보 Capacitor). Flutter 앱은 계속 배제 | Echoa가 웹으로 못 하는 건 TTS·녹음·AdMob 3개뿐이라 진짜 축은 "UI 몇 벌". `packages/{core,db,api}`는 어느 껍데기든 동일해 미뤄도 버리는 작업 없음. ADR-009 §4 트리거를 그대로 따름 | 2026-08-07 | [011](011_scaffolding-and-app-shell-deferral.md) · [research](../research/2026-08_app-shell-reassessment.md) |
| D-30 | API 계층 (21 §2 미확정 해소) | **tRPC v11** | Next 16 App Router 정식 지원. 입력 스키마가 라우터에 붙어 있어 **DB 없이 계약 자동 검증** 가능(1인 개발 요건). 껍데기가 무엇이든 타입이 이어짐 | 2026-08-07 | [011 §5](011_scaffolding-and-app-shell-deferral.md) |
| D-31 | DB 스키마 처리 | **복사 아닌 정리 재선언** — 실 FK 도입·Better Auth users 테이블·타입 불일치 해소·clean baseline. 원문 격리는 배럴 분리로 코드 강제 | legacy는 `references()` 0건이라 참조 무결성 미보장, `users` 테이블 자체가 없었고, 스냅샷 drift로 `db:push` 금지 상태였음 | 2026-08-07 | [011 §6](011_scaffolding-and-app-shell-deferral.md) |

## 남은 결정 (재구성 중 확정)

| # | 항목 | 선택지 | 선행 조건 | 문서 |
|---|------|--------|-----------|------|
| E-02 | 소셜 프로바이더 조합 | 구글+카카오 / +네이버 / 앱 단계 Apple | Better Auth 연결(단계 2) | (legacy [ADR-002]) |
| E-03 | 가입 유도 시점·게스트 잠금 | UX 테스트 후 | 동상 | (legacy [ADR-002]) |
| E-04 | C-2 528건 적재 방식 | 복습 변형 문제 / 신규 문장 | 앱 학습 흐름 확정 | [23 §9](../project-review/23_content-pipeline-spec.md) |
| E-05 | 미모델링 legacy 테이블 4개 존폐 | quizzes 934·daily_expressions 105·question_patterns 91·grammar_patterns 48 | 22번 spec 검토 — E-04와 **묶어서** 판정 | [24](../project-review/24_deferred-legacy-tables.md) |
| E-06 | 앱 껍데기 확정 (D-29 유예분) | Capacitor / Expo / Flutter 래퍼 | 웹 학습 흐름 완성 → TTS 제약 실측 | [011 §3](011_scaffolding-and-app-shell-deferral.md) |
