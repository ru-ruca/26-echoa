import { progressRouter } from './router/progress';
import { reviewRouter } from './router/review';
import { sentenceRouter } from './router/sentence';
import { vocabularyRouter } from './router/vocabulary';
import { createTRPCRouter } from './trpc';

/**
 * 루트 라우터.
 *
 * legacy는 Next.js Route Handler 8개(`sentences`·`today`·`progress`·`next-lesson`·
 * `review`·`vocabulary`·`favorites`·`stats`)였다. 이를 도메인 4개로 다시 묶는다.
 * 지금 실제로 동작하는 건 `sentence`뿐이고 나머지는 스텁이다 — 각 파일에 사유를 적어 뒀다.
 */
export const appRouter = createTRPCRouter({
  sentence: sentenceRouter,
  review: reviewRouter,
  progress: progressRouter,
  vocabulary: vocabularyRouter,
});

export type AppRouter = typeof appRouter;
