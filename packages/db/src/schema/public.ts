/**
 * 공개 스키마 배럴 — 앱·공개 API가 닿을 수 있는 전부.
 *
 * ⚠️ `./restricted`(content_originals)는 **의도적으로 빠져 있다** (ADR-010 §3).
 * 여기에 추가하는 순간 저작권 원문이 공개 경로로 새어 나갈 수 있다.
 * 원문이 필요한 코드는 `@echoa/db/admin`을 쓴다.
 */

export * from './auth';
export * from './content';
export * from './learner';
