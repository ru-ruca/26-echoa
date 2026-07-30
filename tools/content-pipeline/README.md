# Echoa 콘텐츠 생성 파이프라인

C-1(저작권 재작성) · C-2(패턴 문장 확장) · C-3(대화 확장)을 만드는 배치 파이프라인.
**Spec**: [23_content-pipeline-spec.md](../../docs/project-review/23_content-pipeline-spec.md) · **제약**: [ADR-010](../../docs/adr/010_content-copyright-and-data-model.md)

## 구조 — 스크립트 단계와 세션 단계

결정적 작업(추출·필터·리포트)은 **Python 스크립트**, 생성·채점은 **Claude Code 세션**이 수행한다.
API 키가 필요 없고, 세션 수행 단계의 입출력 계약(JSONL)을 지키면 나중에 Batches API로 교체할 수 있다.

| 단계 | 수행 | 내용 |
|---|---|---|
| s01 extract | 스크립트 | legacy DB(읽기 전용) → 씨앗·어휘·출처·연결 JSONL |
| s02 allowlist | 스크립트 | 허용 어휘 목록(core/extended) + 기존 문장 초과율 baseline 실측 |
| s03 generate | **세션** | `prompts/c1·c2·c3` 프롬프트 + 입력 JSONL → 생성 후보 JSONL (메타 기입) |
| s04 gate-hard | 스크립트 | 문법·씨앗 유사도·근접 중복·어휘 초과·패턴 구조 필터 |
| s05 judge | **세션** | `prompts/judge` — 1~5점 채점 → 재랭킹 (생성과 **다른 세션/서브에이전트**로) |
| s06 report | 스크립트 | 23 §5 지표 리포트 + 인간 검수 시트(5~10% + judge 저점 전량) |

## 실행

```sh
cd tools/content-pipeline
uv sync                                   # 최초 1회 (spacy 모델 포함)
uv run python -m src.steps.s01_extract    # legacy .env의 DATABASE_URL 자동 로드
uv run python -m src.steps.s02_allowlist
```

- legacy DB 접속: `LEGACY_DATABASE_URL` 환경변수 우선, 없으면 `../../../26-SenTalk-en-study-app/.env`의 `DATABASE_URL`.
- 접속은 **readonly 세션**으로 강제된다 (`src/db.py`).

## 원문 격리 규칙 (ADR-010 — 반드시 지킬 것)

- `data/` 전체와 `reports/restricted/`는 **git 제외**. 저작권 원문(quote·movie 등 verbatim)이 들어가는 파일은 이 두 경로 밖에 만들지 않는다.
- C-1 재작성의 원문 대조 자료·검수 시트는 `reports/restricted/`에 생성.
- 승인된 생성물(공개 가능분)만 이후 echoa DB 적재 대상이 된다. 원문은 `content_originals` 격리 테이블로만 이관.

## 씨앗 분류 (M01~03 실측 기준)

| seed_class | 대상 | 개수 |
|---|---|---|
| `c1_rewrite` | quote·movie — 재작성 후 그 결과가 C-2 씨앗이 됨 | 27 |
| `c2_seed` | real·tale·proverb — 저위험, 그대로 씨앗 | 118 |
| `c3_reference` | 기존 conversation(대화 6개×10턴) — C-3 스키마 검증 참조용 | 60 |
| `excluded_review` | review — original_id로 기존 문장 재사용이라 씨앗 제외 | 24 |

## 허용 어휘 이원화 (s02)

- **core** = CEFR A1 vocabulary + 기능어(POS 기반 자동 허용: 관사·전치사·대명사·조동사·접속사·고유명사·감탄사 등)
- **extended** = core ∪ M01~03 문장 실등장 content lemma
- baseline 실측은 **core 기준**(기존 문장도 core 밖 단어를 쓰는 정도를 측정 → 생성물 임계값 근거),
  생성물 하드필터는 **extended 기준**(배운 단어는 허용).

## 성공 기준 (23 §5)

judge 평균 ≥ 4/5 · 인간 검수 합격 ≥ 90% · 근접 중복 < 2% · 씨앗 유사도 초과 0건 · C-3 마지막 턴 CEFR 유지.
기준 미달 시 프롬프트·필터 수정 후 재실행. 통과 후에만 월 단위 확대(48개월 일괄 생성 금지).
