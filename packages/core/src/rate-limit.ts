/**
 * In-memory Rate Limiter (Sliding Window Counter)
 *
 * 서버리스 환경에서의 한계:
 * - 인스턴스별 독립 Map → 다중 인스턴스 간 공유 안됨
 * - Cold start 시 초기화
 * - 프로덕션에서 더 강력한 보호가 필요하면 Upstash Redis로 전환 (이월 항목)
 */

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

interface RateLimitConfig {
  /** 윈도우 내 최대 요청 수 */
  max: number;
  /** 윈도우 크기 (ms) */
  windowMs: number;
}

const store = new Map<string, RateLimitEntry>();

// 1000개 이상 쌓이면 만료 항목 정리 (메모리 누수 방지)
const MAX_STORE_SIZE = 1000;

function cleanup() {
  if (store.size < MAX_STORE_SIZE) return;
  const now = Date.now();
  for (const [key, entry] of store.entries()) {
    if (now > entry.resetAt) store.delete(key);
  }
}

/** Rate limit 체크. 제한 초과 시 remaining: 0 반환. */
export function checkRateLimit(
  key: string,
  config: RateLimitConfig,
): { limited: boolean; remaining: number; resetAt: number } {
  cleanup();

  const now = Date.now();
  const entry = store.get(key);

  // 새 윈도우 시작
  if (!entry || now > entry.resetAt) {
    const resetAt = now + config.windowMs;
    store.set(key, { count: 1, resetAt });
    return { limited: false, remaining: config.max - 1, resetAt };
  }

  entry.count++;

  if (entry.count > config.max) {
    return { limited: true, remaining: 0, resetAt: entry.resetAt };
  }

  return { limited: false, remaining: config.max - entry.count, resetAt: entry.resetAt };
}
