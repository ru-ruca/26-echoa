/**
 * 진행 라우터 — legacy `/api/progress`·`/api/next-lesson` 대응. **스텁.**
 *
 * 쓰기 경로(XP 지급·스트릭 갱신·배지 부여)가 여기 들어온다. 규칙은 이미 `@echoa/core`의
 * 순수 함수로 분리돼 있고(`applyXpGain`·`nextStreak`·`selectNewlyEarnedBadges`),
 * 이 라우터는 그 반환값을 트랜잭션 안에서 DB에 반영하는 역할만 맡는다.
 *
 * 채우기 전 선행 조건: Better Auth 연결(단계 2) — `protectedProcedure`가 실제로 동작해야 한다.
 */

import { createTRPCRouter } from '../trpc';

export const progressRouter = createTRPCRouter({});
