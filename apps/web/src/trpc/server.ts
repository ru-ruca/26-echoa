import 'server-only';

import { cache } from 'react';
import { headers } from 'next/headers';

import { createCaller, createTRPCContext } from '@echoa/api';

/**
 * RSC 에서 HTTP 왕복 없이 라우터를 직접 호출한다.
 * `cache()` 로 감싸 한 요청 안에서는 컨텍스트가 한 번만 만들어지게 한다.
 */
const createContext = cache(async () => {
  return createTRPCContext({
    headers: await headers(),
    // Better Auth 연결은 단계 2. 그전까지 서버 컴포넌트는 비로그인 컨텍스트로 돈다.
    session: null,
  });
});

export const api = createCaller(createContext);
