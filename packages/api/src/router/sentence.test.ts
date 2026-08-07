/**
 * 라우터 계약 테스트 — DB 없이 도는 부분만 검증한다.
 *
 * "검증 자동화가 쉬울 것"이 스택 선택 조건이었다. tRPC는 입력 스키마가 라우터에 붙어 있어
 * 실제 DB 없이도 입력 검증·에러 코드 계약을 확인할 수 있다.
 * DB가 필요한 쿼리 자체는 `pnpm dev` 로 뜬 웹에서 확인한다.
 */

import { describe, expect, it } from 'vitest';

import { appRouter } from '../root';
import { createCallerFactory } from '../trpc';

const createCaller = createCallerFactory(appRouter);

/** DB에 닿기 전에 입력 검증에서 걸리는지 보려는 것이라 db는 접근 시 던지게 둔다 */
const caller = createCaller({
  db: new Proxy(
    {},
    {
      get() {
        throw new Error('입력 검증 단계에서 DB에 닿으면 안 된다');
      },
    },
  ) as never,
  session: null,
  headers: new Headers(),
});

describe('appRouter 구조', () => {
  it('도메인 라우터 4개를 노출한다', () => {
    expect(Object.keys(appRouter._def.record).sort()).toEqual([
      'progress',
      'review',
      'sentence',
      'vocabulary',
    ]);
  });
});

describe('sentence 입력 검증', () => {
  it('빈 id 는 BAD_REQUEST', async () => {
    await expect(caller.sentence.byId({ id: '' })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
  });

  it('커리큘럼 범위를 벗어난 month 는 BAD_REQUEST (1~48)', async () => {
    await expect(caller.sentence.byDay({ month: 49, week: 1, day: 1 })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
    await expect(caller.sentence.byDay({ month: 0, week: 1, day: 1 })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
  });

  it('week 는 1~4, day 는 1~7', async () => {
    await expect(caller.sentence.byDay({ month: 1, week: 5, day: 1 })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
    await expect(caller.sentence.byDay({ month: 1, week: 1, day: 8 })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
  });

  it('정수가 아닌 좌표는 BAD_REQUEST', async () => {
    await expect(caller.sentence.byDay({ month: 1.5, week: 1, day: 1 })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
  });

  it('빈 dialogueId 는 BAD_REQUEST', async () => {
    await expect(caller.sentence.dialogue({ dialogueId: '' })).rejects.toMatchObject({
      code: 'BAD_REQUEST',
    });
  });
});
