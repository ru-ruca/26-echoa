import { describe, it, expect } from 'vitest';
import { checkRateLimit } from './rate-limit';

// store는 모듈 레벨 Map이라 테스트 간 상태가 공유된다 — 각 테스트에서 고유 키로 격리.

describe('checkRateLimit', () => {
  const config = { max: 3, windowMs: 1000 };

  it('제한 내 요청은 limited=false', () => {
    const result = checkRateLimit('test-within-limit', config);

    expect(result.limited).toBe(false);
    expect(result.remaining).toBe(2); // max(3) - 1
  });

  it('연속 요청 시 remaining 감소', () => {
    const key = 'test-decreasing';

    expect(checkRateLimit(key, config).remaining).toBe(2);
    expect(checkRateLimit(key, config).remaining).toBe(1);

    const r3 = checkRateLimit(key, config);
    expect(r3.remaining).toBe(0);
    expect(r3.limited).toBe(false);
  });

  it('제한 초과 시 limited=true', () => {
    const key = 'test-exceeded';

    for (let i = 0; i < 3; i++) {
      checkRateLimit(key, config);
    }

    const result = checkRateLimit(key, config);
    expect(result.limited).toBe(true);
    expect(result.remaining).toBe(0);
  });

  it('다른 키는 독립 카운팅', () => {
    for (let i = 0; i < 3; i++) {
      checkRateLimit('test-key-a', config);
    }

    const result = checkRateLimit('test-key-b', config);
    expect(result.limited).toBe(false);
    expect(result.remaining).toBe(2);
  });

  it('윈도우 만료 후 카운트 초기화', async () => {
    const shortConfig = { max: 1, windowMs: 50 };
    const key = 'test-window-reset';

    checkRateLimit(key, shortConfig);
    expect(checkRateLimit(key, shortConfig).limited).toBe(true);

    await new Promise((resolve) => setTimeout(resolve, 60));

    const reset = checkRateLimit(key, shortConfig);
    expect(reset.limited).toBe(false);
    expect(reset.remaining).toBe(0); // max(1) - 1
  });
});
