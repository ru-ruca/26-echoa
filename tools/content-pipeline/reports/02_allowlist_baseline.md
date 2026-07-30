# s02 — 허용 어휘 구성·baseline 초과율 리포트 (M01~03)

생성: 2026-07-30T08:10:27+00:00

## 허용 어휘

| 집합 | 크기 | 구성 |
|---|---|---|
| core | 415 | CEFR A1 vocabulary (word+lemma 정규화, 다단어는 토큰 분해 포함) |
| extended 추가분 | 119 | M01~03 실등장 content lemma 중 core 밖 |

기능어(관사·전치사·대명사·조동사·접속사·고유명사·감탄사·수사)는 POS 기반 자동 허용 — 검사 대상은 NOUN·VERB·ADJ·ADV lemma만.

## 기존 문장 baseline (core 기준 초과율, review 제외 205문장)

| 지표 | 값 |
|---|---|
| 초과 0개 문장 | 77 (38%) |
| 문장당 초과 개수 평균 / p90 / 최대 | 0.95 / 2 / 3 |
| 문장당 초과 비율 평균 / p90 / 최대 | 33.9% / 75.0% / 100.0% |

### 초과 빈도 상위 20 lemma

| lemma | 빈도 |
|---|---|
| turn | 8 |
| wake | 6 |
| bus | 5 |
| dinner | 5 |
| forest | 4 |
| late | 4 |
| brush | 4 |
| princess | 4 |
| once | 3 |
| fun | 3 |
| care | 3 |
| fly | 3 |
| hurry | 3 |
| dress | 3 |
| quickly | 3 |
| wolf | 3 |
| catch | 2 |
| someday | 2 |
| laugh | 2 |
| race | 2 |

### 초과가 많은 문장 상위 10

| id | class | 초과/전체 | 초과 단어 |
|---|---|---|---|
| M02_004 | c2_seed | 3/5 | inside, bowl, porridge |
| M02_013 | c2_seed | 3/4 | princess, bear, kingdom |
| M02_014 | c2_seed | 3/5 | fairy, curse, princess |
| M02_017 | c2_seed | 3/3 | kiss, princess, wake |
| M02_018 | c2_seed | 3/3 | turn, tv, dinner |
| M02_D01_L05 | c3_reference | 3/4 | dressed, quickly, late |
| M02_031 | c2_seed | 3/6 | plant, tree, ago |
| M02_D02_L04 | c3_reference | 3/3 | turn, tv, dinner |
| M03_001 | c1_rewrite | 3/4 | journey, mile, step |
| M03_D01_L04 | c3_reference | 3/5 | straight, turn, corner |

## 하드필터 임계값 제안 (파일럿 s04에 적용, 실행 결과 보고 조정)

1. **extended 기준**: 생성물의 content lemma는 extended 안에 있어야 한다 — 초과 0 목표.
2. **core 기준 참고치**: 초과 content lemma 문장당 ≤ 2개 (기존 p90 수준).
   extended를 통과했더라도 core 밖 단어가 이보다 많으면 A1 이탈로 보고 탈락.
3. judge 재랭킹에서 core 밖 단어 수를 감점 요소로 반영.
