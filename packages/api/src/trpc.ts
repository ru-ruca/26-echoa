/**
 * tRPC 초기화 — 컨텍스트·프로시저 빌더.
 *
 * 컨텍스트가 노출하는 `db`는 `@echoa/db`의 **공개 클라이언트**다.
 * `content_originals`는 이 스키마에 없으므로 라우터에서 원문에 닿을 방법이 아예 없다
 * (ADR-010 §3 — 쿼리 레이어에서 원천 차단).
 */

import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';
import { ZodError } from 'zod';

import { db } from '@echoa/db';

/** 요청마다 만들어지는 컨텍스트 */
export interface CreateContextOptions {
  headers: Headers;
  /** Better Auth 세션 — 단계 2에서 연결한다. 그전엔 항상 null. */
  session: { user: { id: string } } | null;
}

export function createTRPCContext(opts: CreateContextOptions) {
  return {
    db,
    session: opts.session,
    headers: opts.headers,
  };
}

export type Context = ReturnType<typeof createTRPCContext>;

const t = initTRPC.context<Context>().create({
  transformer: superjson,
  errorFormatter: ({ shape, error }) => ({
    ...shape,
    data: {
      ...shape.data,
      // 클라이언트가 필드별 오류를 그대로 쓸 수 있게 zod 결과를 펼쳐 준다
      zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
    },
  }),
});

export const createTRPCRouter = t.router;
export const createCallerFactory = t.createCallerFactory;

/** 로그인 없이 쓸 수 있는 프로시저 (콘텐츠 조회 등) */
export const publicProcedure = t.procedure;

/**
 * 로그인이 필요한 프로시저.
 *
 * legacy는 `Authorization: Bearer <deviceId>`를 검증 없이 그대로 신뢰해서 임의 문자열로
 * 타인 행세가 가능했다(IDOR). 여기서는 세션이 없으면 통과 자체를 못 한다.
 */
export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED', message: '로그인이 필요합니다.' });
  }
  return next({ ctx: { ...ctx, session: ctx.session } });
});
