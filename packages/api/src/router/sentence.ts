/**
 * 문장 라우터 — legacy `/api/sentences`·`/api/today` 대응.
 *
 * 이 라우터가 웹 → api → db 경로가 실제로 도는지 증명하는 지점이다.
 * 나머지 라우터는 스텁이고, 학습 흐름이 22번 spec에서 확정된 뒤에 채운다.
 */

import { TRPCError } from '@trpc/server';
import { and, asc, eq } from 'drizzle-orm';
import { z } from 'zod';

import { sentences } from '@echoa/db/schema';

import { createTRPCRouter, publicProcedure } from '../trpc';

export const sentenceRouter = createTRPCRouter({
  /** 단일 문장 조회 */
  byId: publicProcedure.input(z.object({ id: z.string().min(1) })).query(async ({ ctx, input }) => {
    const [row] = await ctx.db.select().from(sentences).where(eq(sentences.id, input.id)).limit(1);

    if (!row) {
      throw new TRPCError({ code: 'NOT_FOUND', message: `문장을 찾을 수 없습니다: ${input.id}` });
    }
    return row;
  }),

  /** 커리큘럼 좌표(month/week/day)로 하루치 문장 */
  byDay: publicProcedure
    .input(
      z.object({
        month: z.number().int().min(1).max(48),
        week: z.number().int().min(1).max(4),
        day: z.number().int().min(1).max(7),
      }),
    )
    .query(async ({ ctx, input }) => {
      return ctx.db
        .select()
        .from(sentences)
        .where(
          and(
            eq(sentences.month, input.month),
            eq(sentences.week, input.week),
            eq(sentences.day, input.day),
          ),
        )
        .orderBy(asc(sentences.id));
    }),

  /**
   * 대화 한 편 (미니대화 window의 원본).
   * `@echoa/core`의 `buildDialogueWindow`가 이 결과를 잘라 쓴다.
   */
  dialogue: publicProcedure
    .input(z.object({ dialogueId: z.string().min(1) }))
    .query(async ({ ctx, input }) => {
      const lines = await ctx.db
        .select()
        .from(sentences)
        .where(eq(sentences.dialogueId, input.dialogueId))
        .orderBy(asc(sentences.id));

      if (lines.length === 0) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: `대화를 찾을 수 없습니다: ${input.dialogueId}`,
        });
      }
      return lines;
    }),
});
