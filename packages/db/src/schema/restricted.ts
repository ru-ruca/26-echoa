/**
 * ⚠️ 격리 스키마 — 저작권 원문 전용 (ADR-010 §2·§3).
 *
 * **이 파일은 공개 배럴(`schema/public.ts`)에서 절대 re-export 하지 않는다.**
 * `@echoa/db`(공개 진입점)로는 이 테이블에 닿을 수 없고, `@echoa/db/admin`으로만 닿는다.
 * 공개 클라이언트는 이 테이블을 모르는 schema로 만들어져 `db.query.contentOriginals`도 없다.
 *
 * ADR-010 §3이 요구하는 4가지:
 *  1. 공개 API·앱에서 절대 미노출 — 쿼리 레이어에서 원천 차단 (이 파일 격리가 그 장치)
 *  2. git·공개 CSV·공개 백업에서 제외 — 루트 `.gitignore`의 `**\/originals/` 규칙
 *  3. admin 인증 하에서만 조회
 *  4. 년 단위 CSV 추출은 공개분/원문분 분리, 원문 CSV는 비공개
 */

import { relations } from 'drizzle-orm';
import { index, jsonb, pgTable, serial, text, timestamp, integer } from 'drizzle-orm/pg-core';

import { sentences, sources } from './content';

/** 재작성 이력 메타 — 어떤 모델·프롬프트로 언제 만들었는지 (감사·품질 비교용) */
export interface RewriteMeta {
  /** 생성 프롬프트 식별자 (예: "c1_rewrite_v1_full") */
  prompt?: string;
  /** 생성일 (YYYY-MM-DD) */
  date?: string;
  /** 채택일 (YYYY-MM-DD) */
  adoptedAt?: string;
  /** 채택 경로 — judge_best · human_review · reviewer_alternative … */
  source?: string;
  /** LLM judge 평균 점수 */
  judgeAvg?: number;
  /** 원문과의 유사도 (낮을수록 표현이 대체됐다는 뜻) */
  seedSim?: number;
  /** 검수 시 수정 여부 */
  modified?: boolean;
  /** 외부 AI 교차 검토 결과 */
  external?: Record<string, unknown>;
}

/**
 * 원저작물 verbatim 격리 테이블.
 *
 * 재생성 품질 비교·출처 추적 용도로만 존재한다. 공개 경로로 나가지 않는다.
 */
export const contentOriginals = pgTable(
  'content_originals',
  {
    id: serial('id').primaryKey(),
    sentenceId: text('sentence_id')
      .notNull()
      .unique()
      .references(() => sentences.id, { onDelete: 'cascade' }),
    /** ⚠️ 저작권 원문 verbatim — 이 컬럼이 공개 경로로 나가면 ADR-010 위반이다. */
    originalTextEn: text('original_text_en').notNull(),
    originalTextKr: text('original_text_kr'),
    sourceId: integer('source_id').references(() => sources.id, { onDelete: 'set null' }),
    rewriteMeta: jsonb('rewrite_meta').$type<RewriteMeta>(),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [index('idx_content_originals_sentence').on(t.sentenceId)],
);

export const contentOriginalsRelations = relations(contentOriginals, ({ one }) => ({
  sentence: one(sentences, {
    fields: [contentOriginals.sentenceId],
    references: [sentences.id],
  }),
  source: one(sources, { fields: [contentOriginals.sourceId], references: [sources.id] }),
}));

export type ContentOriginal = typeof contentOriginals.$inferSelect;
export type NewContentOriginal = typeof contentOriginals.$inferInsert;
