/**
 * 어휘 라우터 — legacy `/api/vocabulary`·`/api/favorites` 대응. **스텁.**
 *
 * legacy 데이터 이관(단어 3,920·콜로케이션 5,705)이 끝나야 의미 있는 조회가 된다.
 */

import { createTRPCRouter } from '../trpc';

export const vocabularyRouter = createTRPCRouter({});
