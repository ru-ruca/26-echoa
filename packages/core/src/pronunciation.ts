import type { IntonationPatternId } from './types/pronunciation';

const MIN_PATTERN_ID = 1;
const MAX_PATTERN_ID = 8;

/**
 * DB의 nullable integer 억양 패턴 값을 1~8 리터럴 유니온으로 좁힌다.
 * 범위 밖·비정수·null/undefined는 억양 정보 없음(null)으로 처리한다.
 */
export function toIntonationPatternId(
  value: number | null | undefined,
): IntonationPatternId | null {
  if (value == null || !Number.isInteger(value)) return null;
  if (value < MIN_PATTERN_ID || value > MAX_PATTERN_ID) return null;
  return value as IntonationPatternId;
}
