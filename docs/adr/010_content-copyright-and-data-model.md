# ADR-010: 콘텐츠 저작권 대응 및 원문 격리 데이터 모델

> Status: **Accepted** (2026-07-28)
> 관련: [ADR-004 콘텐츠 워크플로](../../../26-SenTalk-en-study-app/docs/adr/004_content-workflow.md) · [ADR-009 재구성 스택](009_stack-monorepo-decision.md) · [재구성 계획 21](../project-review/21_rebuild-plan.md)
> 저작권 분석 근거: [출시 타당성 20 §2.1·§7](../project-review/20_release-feasibility.md) · [보안·법규 리서치 R4 §7](../research/2026-07_release-feasibility-research.md)

## Context

**저작권 실측(2026-07-27)**: 문장 3,622개 중 저작권 위험 슬라이스가 예상보다 크다.
- `quote` 222 + `movie` 119 = **341개(9.4%)** — 사전 추정(year1 각 48개)을 크게 초과.
- 추가 위험 계열: `news`(120)·`ted`(64)·`drama`(30)·`interview`(23)·`comedy`(14) — 실제 저작물 verbatim이면 리스크.

**수익 모델 확정**: 구독 포기, **무료 + 광고**([D-23](000_decision-log.md)). 광고 수익은 저작권법상 **영리**로 취급되어 인용(제28조)·공정이용(제35조의5) 항변이 모두 불리해진다.

### 저작권 분석 (법률 자문 아님)

- **출처 표시(제37조)는 면책 수단이 아니다.** 인용이 성립할 때 따라오는 별개 의무일 뿐. "출처·링크를 제공하면 괜찮다"는 성립하지 않는다.
- **인용(제28조)의 핵심은 "정당한 범위 + 공정한 관행"** — 대법원 2011도5835: 인용물이 主·피인용이 從인 주종관계 + 원저작물 수요 대체 여부. 학습 교재가 대사를 예문·본문으로 편입하면 그 문장이 콘텐츠의 主가 되어 주종관계가 깨진다.
- **영리성(광고)은 제28조·제35조의5 판단 모두에서 불리 요소.**
- **짧은 문구·명언은 저작물성이 약해** 상대적으로 안전(왕의 남자: 서울고법 2006 가처분 항고 기각). 사후 70년 미경과 인물의 명언은 주의.
- **가장 안전한 길은 "표현의 대체"** — 저작권은 표현을 보호하지 아이디어·상황·문법 패턴은 보호하지 않는다. 원문과 같은 상황·표현·난이도를 담은 **새 문장을 AI로 생성**하면 문제가 소멸한다(실질적 유사성이 남지 않을 만큼 바꿀 것. 일상 회화체는 창작성이 낮아 대체가 쉽다).
- **사적복제(제30조)**: 원저작물을 개인 학습·관리 용도로 소량 보관하는 것은 허용 여지가 있으나, 서버 DB에 대량 보관 + 외부 노출은 회색지대다. → 원문은 **외부 미공개 + 격리 보관**을 전제로만 둔다.

## Decision

### 1. 공개 콘텐츠는 저작권 free만 (광고=영리 전제의 원칙)
앱·공개 API가 반환하는 문장(`text_en`)은 반드시 다음 중 하나여야 한다: **자체 작성 / AI 생성 / AI 재작성(저작권물 기반이되 표현 대체) / 퍼블릭 도메인.** 저작권물 verbatim은 공개 경로에 절대 들어가지 않는다.

### 2. 원문은 격리 보관 (사용자 제안 채택 + 보완)
사용자 제안("오리지널은 관리에서만 확인 + AI 생성 문장을 추가 필드로 + 오리지널 외부 미공개")을 채택하되, 컬럼 혼재 대신 **별도 테이블로 물리 격리**한다:

```
sentences (공개)                    content_originals (관리 전용, 격리)
├ id                          1  ─┐  ├ sentence_id  (FK → sentences.id)
├ text_en   ← 공개용(free)        └─ ├ original_text_en  ← 저작권 원문(verbatim)
├ text_kr                            ├ source_id       (FK → sources)
├ content_origin  (enum)            ├ rewrite_meta     (모델·프롬프트·날짜)
├ source_id       (출처 메타)       └ created_at
└ ...
```

- `content_origin` enum: `self_authored` · `ai_generated` · `ai_rewritten` · `public_domain`. 감사(audit) 가능하도록 모든 공개 문장에 필수.
- `content_originals`는 **원저작물 verbatim 전용**. 재생성 품질 비교·출처 추적 용도로만 존재한다.
- 현 스키마의 `original_id`·`notes`·`sources`(title/author/year/url)를 이 구조로 정리·계승.

### 3. 원문 격리 정책 (외부 유출 차단 — 필수)
- **공개 API·앱에서 `content_originals` 절대 미노출** — 쿼리 레이어에서 원천 차단.
- **git·공개 CSV·공개 백업에서 제외** — 원문은 별도 비공개 저장(개발자 로컬/비공개 백업). `.gitignore`·CSV 추출 스크립트가 `content_originals`를 건드리지 않음.
- **admin 인증 하에서만 조회.**
- DB 년 단위 CSV 추출([21번 DB 전략](../project-review/21_rebuild-plan.md))은 **공개분(sentences)과 원문분(content_originals)을 분리 추출**, 원문 CSV는 비공개.

### 4. 재생성을 기본 전략으로
위험 슬라이스(movie·drama·comedy·interview·news·ted 등)는 **AI 재작성으로 교체**한다. quote는 만료·저작물성 약한 것 위주로 선별, 나머지 재생성. proverb·tale·real 등 저위험은 유지. day_type별 처리는 [21번 자산표](../project-review/21_rebuild-plan.md) 참고.

## 처리 기준 (day_type별)

| 계열 | 위험 | 처리 |
|---|---|---|
| proverb·tale·real·business·daily(자체작성) | 낮음 | 유지 |
| quote | 낮음~중간 | 만료/저작물성 약한 것 선별, 나머지 재생성 |
| movie·drama·comedy·interview | 높음 | **AI 재작성 교체**, 원문은 격리 보관 |
| news·ted·academic | 중간~높음 | **재작성 또는 자체작성** |

## 결과 / 트레이드오프

- **얻는 것**: 공개분은 저작권 안전(광고 모델에 부합), 원문은 재생성 비교·감사용으로 보존, 감사 가능한 출처 추적(`content_origin`).
- **감수**: 재생성 작업량(위험 슬라이스 수백 개), 원문 격리 운영 규율(공개 경로·백업에서 계속 배제해야 함).
- **잔여 리스크**: 원문 서버 보관의 회색지대. 완화 = 외부 미공개 철저 + 상업화(광고 게재) 정식 전 저작권위원회/변호사 검토([20번 §7](../project-review/20_release-feasibility.md)).

## 참고 출처

- [출시 타당성 20 §2.1·§7](../project-review/20_release-feasibility.md) · [보안·법규 리서치 R4 §7](../research/2026-07_release-feasibility-research.md)
- 저작권법 [제28조](https://www.law.go.kr/법령/저작권법)(인용)·제30조(사적복제)·제35조의5(공정이용)·제37조(출처명시) · 대법원 [2011도5835](https://casenote.kr/대법원/2011도5835)
- [한국저작권위원회](https://www.copyright.or.kr)
