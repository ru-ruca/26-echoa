# s13 — A1 허용 어휘 목록 확장 (2026-08-06)

## 근거

year1(M01~12) 커리큘럼 **904문장이 전부 `cefr_level='A1'`** 이다.
커리큘럼 설계자가 A1 학습자에게 내보내도 된다고 판정한 문장들이므로, **그 문장들이 쓰는 단어는 A1 적정**이다.
외부 워드리스트를 들여오지 않고 우리 자산만으로 검증 가능한 기준이다.

## 확장 결과

| 집합 | 크기 |
|---|---|
| A1 사전(core) | 415 |
| M01~03 실등장(파일럿 extended_extra) | 119 |
| 인간 승인 누적 | 17 |
| **확장 전 합계** | **546** |
| **year1 실등장 신규 추가** | **+366** |
| **확장 후 합계** | **912** |

## 확장 효과 — C-2 어휘 탈락분 회수

| 지표 | 값 |
|---|---|
| C-2에서 `vocab_extended`로 탈락 | 94건 |
| **확장 목록으로 회수 가능** | **35건 (37%)** |
| 여전히 목록 밖 | 59건 |

### 확장 후에도 목록 밖인 lemma (상위 20)

| lemma | 탈락 유발 |
|---|---|
| taxi | 4 |
| path | 4 |
| swimming | 3 |
| neighbor | 3 |
| drank | 2 |
| reading | 2 |
| hat | 2 |
| heavy | 2 |
| wash | 2 |
| sock | 2 |
| windy | 2 |
| dark | 2 |
| toy | 1 |
| smile | 1 |
| funny | 1 |
| swam | 1 |
| playing | 1 |
| sweet | 1 |
| careful | 1 |
| quiet | 1 |

이들은 year1 커리큘럼이 쓰지 않는 단어다 — 생성기가 임의로 끌어온 것이므로 **탈락이 정상**이다.
확장 목록은 "커리큘럼이 실제로 A1에서 쓰는 어휘"라는 경계를 유지한다.

## 신규 추가 어휘 빈도 상위 30

| lemma | year1 등장 |
|---|---|
| check | 15 |
| pig | 10 |
| build | 9 |
| card | 8 |
| medicine | 8 |
| away | 7 |
| feel | 7 |
| stay | 7 |
| fox | 6 |
| pick | 6 |
| tonight | 6 |
| accept | 5 |
| bring | 5 |
| course | 5 |
| credit | 5 |
| delicious | 5 |
| exchange | 5 |
| exercise | 5 |
| folk | 5 |
| free | 5 |
| laughter | 5 |
| loud | 5 |
| meeting | 5 |
| moment | 5 |
| noise | 5 |
| party | 5 |
| size | 5 |
| soup | 5 |
| stroke | 5 |
| travel | 5 |

## 운영

- `s04_gate_hard.load_allowlist()`가 이 파일을 extended에 병합한다 (인간 승인 목록과 동일 방식).
- 월 단위 확대 시 해당 연차 문장으로 다시 돌리면 된다 (year2는 A2, year3~4는 B1·B2 — 레벨별로 분리 적용).

### 적용 범위 — 앞으로만, 소급 아님

확장 목록은 **이후 라운드(C-1 341 확대·월 단위 확대)에 적용**한다.
이미 확정된 [c2_final.jsonl](../output/c2_final.jsonl) 528건에는 소급하지 않는다 —
회수 가능한 35건은 **인간 검수를 거치지 않은 후보**라, 검수 없이 합류시키면
"노출 전 전량 검수"(23 §4) 원칙이 깨진다. 필요하면 별도 라운드로 judge·검수를 태워 합류시킨다.
