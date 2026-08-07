/**
 * 미니대화 window 계산 (매일 회화)
 *
 * 쉐도잉 훈련 단위는 2~4줄이 효과적(legacy research/2026-07_shadowing-ui-benchmark §1 U6~U8).
 * 10줄짜리 대화(year1/2)에서 초점 줄 중심으로 최대 4줄만 잘라 보여준다.
 */

/** 초점 줄 앞에 붙일 문맥 줄 수 (상대방 발화가 있어야 대화가 이해된다) */
const WINDOW_BEFORE = 1;
/** window 최대 줄 수 */
const WINDOW_MAX = 4;

/**
 * 초점 줄 중심의 미니대화 window를 자른다.
 *
 * 기본 [초점-1, 초점+2] 범위(4줄)이고, 경계에서는 남는 몫을 반대쪽으로 채워
 * 항상 min(전체, 4)줄을 유지한다. focusIndex가 범위 밖이면 안쪽으로 클램프.
 */
export function buildDialogueWindow<T>(lines: T[], focusIndex: number): T[] {
  if (lines.length <= WINDOW_MAX) return [...lines];

  const focus = Math.max(0, Math.min(focusIndex, lines.length - 1));
  let start = focus - WINDOW_BEFORE;
  if (start < 0) start = 0;
  if (start + WINDOW_MAX > lines.length) start = lines.length - WINDOW_MAX;

  return lines.slice(start, start + WINDOW_MAX);
}
