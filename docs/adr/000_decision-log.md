# Decision Log — Echoa

> Echoa 재구성 이후 주요 결정 인덱스. **D-01~D-21은 legacy(SenTalk) 결정**으로, 원본 [../26-SenTalk-en-study-app/docs/adr/000_decision-log.md] 참조(git 태그 `legacy-nextjs-pwa`). 여기는 재구성 결정(D-22~)부터 계승·기록.
> 최종 업데이트: 2026-07-30

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

## 남은 결정 (재구성 중 확정)

| # | 항목 | 선택지 | 문서 |
|---|------|--------|------|
| E-02 | 소셜 프로바이더 조합 | 구글+카카오 / +네이버 / 앱 단계 Apple | (legacy [ADR-002]) |
| E-03 | 가입 유도 시점·게스트 잠금 | UX 테스트 후 | (legacy [ADR-002]) |
| E-04 | C-2/C-3 콘텐츠 확장 실행 | [23 spec](../project-review/23_content-pipeline-spec.md) 파일럿 후 전개 | [23](../project-review/23_content-pipeline-spec.md) |
