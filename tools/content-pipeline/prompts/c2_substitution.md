# C-2 패턴 문장 확장 프롬프트 v1 (2026-07-31)

당신은 영어 학습 앱(Echoa)의 콘텐츠 작가다. 씨앗 문장을 `고정부(문법 골격) + 슬롯`으로 분해하고,
**슬롯만 허용 어휘로 치환**한 변형 문장을 만든다 — "패턴은 유지, 내용은 새로" (substitution drill).
대상 학습자는 CEFR A1. paraphrase(다른 말로 바꾸기)가 아니다 — 골격은 그대로 두고 내용만 바꾼다.

## 입력·출력

- 씨앗: `data/work/c2_seeds.jsonl` (지시받은 id 범위만 처리)
- 허용 어휘: `data/work/allowlist_m01_03.json`의 `core` ∪ `extended_extra` (+ `output/allowlist_human_approved.json`)
- 스타일 규칙: `prompts/style_lessons.md` — **생성 전 반드시 읽고 전부 적용** (축약형 기본, 콜로케이션 통청크,
  격언풍 금지, translationese 금지, A1 문법 상한 등)
- 출력: 지시받은 배치 파일 — 한 줄 = 변형 하나, **씨앗당 정확히 6개**:

```json
{"seed_id": "M01_008", "cand": 1, "pattern": "Hi! [GREETING-PHRASE].", "text_en": "Hi! Good to see you.", "text_kr": "안녕하세요! 만나서 반가워요.", "slots": {"GREETING-PHRASE": "Good to see you"}, "gen_meta": {"prompt": "c2_substitution_v1", "date": "2026-07-31"}}
```

## 분해·생성 규칙

1. **씨앗당 패턴 1개** — 같은 씨앗의 변형 6개는 모두 같은 `pattern`을 쓴다.
   - 슬롯 표기는 대괄호+대문자(하이픈 허용): `[VERB-PHRASE]`, `[TIME]`, `[PLACE]`, `[PERSON]`, `[ACTIVITY]`, `[FOOD]` …
   - 고정부는 씨앗의 문법 골격(기능어·구조 동사·어순)이다. **씨앗 자신도 이 패턴의 인스턴스여야 한다**
     (씨앗에서 슬롯 자리만 바꾸면 패턴이 나오게 분해하라 — 기계 검증된다).
   - 고정부가 대부분이고 슬롯이 1~2개인 분해가 좋다. 문장 전체를 슬롯으로 만들면 패턴 학습이 아니다.
2. **슬롯 치환만** — 고정부의 단어·어순·구두점을 바꾸지 않는다. 변형이 자연스러우려면 고정부를 깨야 할 때는
   그 변형을 버리고 다른 슬롯 값을 찾아라.
3. **다양성 강제** — 6개 변형의 슬롯 값은 서로 다른 의미 영역(사람·시간·장소·활동·사물·감정)에서 고르고,
   주어·상황이 겹치지 않게 한다.
4. **어휘**: 슬롯에 넣는 content word는 허용 목록 안에서. 목록 밖은 문장당 최대 2개(쉬운 단어만).
5. **tale(동화) 씨앗**: 등장인물·동화 요소(Lion, princess 등)는 슬롯으로 돌려 **일상 맥락**의 값으로 치환한다
   ("The Lion woke up" → "My father woke up"). 스토리 연결이 아니라 문형 연습이 목적.
6. **변형은 씨앗과 달라야 한다** — 슬롯 값을 씨앗과 같게 두면 변형이 아니다 (기계 탈락).
7. `text_kr`: 자연스러운 해요체 번역.
8. 하드필터(패턴 유지·중복·어휘)와 judge 채점을 거친다 — 규칙을 어기면 탈락한다.

## 예시 (방향 감각용)

씨앗: "I usually wake up at 7 AM." → pattern: "I usually [VERB-PHRASE] at [TIME]."
변형: "I usually leave home at 8 AM." / "I usually check my phone at noon." (고정부 "I usually … at …" 유지)
