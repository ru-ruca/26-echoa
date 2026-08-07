import { createCallerFactory } from './trpc';
import { appRouter } from './root';

export { appRouter, type AppRouter } from './root';
export { createTRPCContext, type Context, type CreateContextOptions } from './trpc';

/** 서버 내부(RSC·스크립트·테스트)에서 HTTP 없이 라우터를 직접 호출할 때 쓴다. */
export const createCaller = createCallerFactory(appRouter);
