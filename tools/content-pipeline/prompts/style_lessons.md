# 생성 스타일 교훈 (누적) — 모든 생성·judge 프롬프트가 참조

> 출처: C-1 인간 검수 2026-07-31 (27씨앗 전량, 수정 11건·judge 불일치 4건 분석).
> C-2·C-3 프롬프트와 judge v2는 이 문서를 규칙으로 포함한다. 새 검수 라운드마다 갱신.

## 생성 규칙 (검수에서 실증된 것)

1. **축약형이 기본이다** — I'm, You're, I'll, Don't, It's. 비축약형은 문어체 신호 (수정 사유 4/11건).
2. **콜로케이션을 통째로** — 단어 조합이 관용적으로 굳은 형태만 쓴다 (수정 사유 4/11건):
   `waste time`(lose ✗) · `get home`(귀가 문맥, come ✗) · `do something fun`(find ✗) ·
   `along the way`(on the way ✗) · `roads lead to`(go ✗) · `just the way I am`(just as you are ✗).
3. **`my friend` 호칭 금지** — 친근함이 아니라 비원어민 화자 신호로 읽힌다.
4. **격언풍·표어·광고 카피체 회피** — "지어낸 속담"(A big hello opens every door)은 실제 발화 상황이 없다.
   기준: *이 문장을 원어민이 오늘 실제로 말할 상황이 그려지는가.*
5. **문어·고어체 회피** — "All will be well" → "Everything will be okay."
6. **A1 문법 상한** — 비교급·최상급·접촉절(the most important thing we have)·'No place is too far' 구조 금지.
   단, 고빈도 관용 청크는 분해 불가능한 통청크로 취급해 허용 가능 (예: just the way I am).
7. **시간대·상황 제약이 적은 문장 우선** — "Hello"가 "Good morning"보다 재사용 범위가 넓다.

## judge v2 반영 사항 (judge 1위 ≠ 인간 채택 4건의 원인)

- **실제 발화 빈도(관용성)** 가중이 부족했다 — naturalness에 "원어민이 이 조합을 실제로 쓰는가"를 명시.
- 콜로케이션 오류는 grammar가 아니라 naturalness 감점으로 잡혔다 → 별도 체크 항목으로 승격 검토.
- "수정 가능한 결함"(동사 1개 교체 등)과 "구조적 결함"(격언풍 조어)을 comment에 구분 표기하면
  인간 검수에서 살릴 후보를 빨리 찾는다.

## 운영 규칙

- 검수자 승인 어휘는 [output/allowlist_human_approved.json](../output/allowlist_human_approved.json)에 누적 (okay·waste).
- 검수자가 "별도 씨앗 회수 권장"한 청크는 Phase 2 씨앗 후보로 검토:
  `Why is there no X?` (M01_040 c3) · `get dressed / get ready` (M02_022 c2) · `See you soon` (M03_041 c1).
- 재생성 후보: M03_001 (후보 품질 최저 — 속담 재작성 티).
