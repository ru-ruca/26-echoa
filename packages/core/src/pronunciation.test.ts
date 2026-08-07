import { describe, it, expect } from 'vitest';
import { toIntonationPatternId } from './pronunciation';

describe('toIntonationPatternId', () => {
  it('1~8 정수는 그대로 통과', () => {
    for (let n = 1; n <= 8; n++) {
      expect(toIntonationPatternId(n)).toBe(n);
    }
  });

  it('범위 밖 정수는 null (0, 9)', () => {
    expect(toIntonationPatternId(0)).toBeNull();
    expect(toIntonationPatternId(9)).toBeNull();
  });

  it('비정수는 null (2.5)', () => {
    expect(toIntonationPatternId(2.5)).toBeNull();
  });

  it('null·undefined는 null', () => {
    expect(toIntonationPatternId(null)).toBeNull();
    expect(toIntonationPatternId(undefined)).toBeNull();
  });
});
