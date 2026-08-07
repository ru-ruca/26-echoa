/**
 * 복습 라우터 — legacy `/api/review` 대응. **스텁.**
 *
 * FSRS 큐 구성·퀴즈 분기 규칙은 이미 `@echoa/core`에 있다(`getReviewPriority`·`selectQuizType`).
 * 여기서 채워야 할 것은 "무엇을 몇 개 꺼낼지"인데, 그 답이 22번 학습설계 spec(§3 세션 구조 —
 * 복습 워밍업 4~5분 / FSRS 약 6장)에 달려 있고 22번은 아직 "초안 · 검토 대기"다.
 * spec 확정 후 채운다.
 */

import { createTRPCRouter } from '../trpc';

export const reviewRouter = createTRPCRouter({});
