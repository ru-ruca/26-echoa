import { fetchRequestHandler } from '@trpc/server/adapters/fetch';

import { appRouter, createTRPCContext } from '@echoa/api';

/**
 * tRPC HTTP 엔드포인트 — 브라우저 클라이언트와 (나중에) 앱이 여기로 붙는다.
 * RSC 는 이 경로를 거치지 않고 `~/trpc/server` 의 caller 를 직접 쓴다.
 */
function handler(req: Request) {
  return fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext: () =>
      createTRPCContext({
        headers: req.headers,
        session: null, // 단계 2에서 Better Auth 세션으로 교체
      }),
    onError({ error, path }) {
      console.error(`[trpc] ${path ?? '<no-path>'}: ${error.message}`);
    },
  });
}

export { handler as GET, handler as POST };
