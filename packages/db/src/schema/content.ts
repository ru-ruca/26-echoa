/**
 * 콘텐츠 스키마 — 공개 학습 자료.
 *
 * legacy `web/src/db/schema.ts`를 복사가 아니라 재선언한 것이다. 고친 것:
 *  1. 실 FK 선언 — legacy는 `references()` 호출이 0건이라 참조 무결성을 DB가 보장하지 않았다.
 *  2. `vocabulary.id`(text) ↔ `vocabulary_morphemes.vocabulary_id`(integer) 타입 불일치 해소.
 *  3. ADR-010의 `content_origin` NOT NULL 도입 (원문 격리 테이블은 `restricted.ts`).
 *  4. `$inferInsert` 타입 export 추가.
 *
 * legacy의 drizzle 스냅샷은 라이브 DB와 어긋나 `db:push`가 금지 상태였다.
 * 여기서는 깨끗한 baseline으로 다시 시작한다 — legacy 마이그레이션은 계승하지 않는다.
 */

import { relations } from 'drizzle-orm';
import {
  boolean,
  decimal,
  index,
  integer,
  jsonb,
  pgEnum,
  pgTable,
  primaryKey,
  serial,
  text,
  timestamp,
  uniqueIndex,
} from 'drizzle-orm/pg-core';

/**
 * 공개 문장의 출처 구분 (ADR-010 §2).
 *
 * 앱·공개 API가 반환하는 `text_en`은 반드시 이 넷 중 하나여야 한다.
 * 저작권물 verbatim은 공개 경로에 절대 들어가지 않는다 — 원문은 `content_originals`로 격리.
 * 감사(audit) 가능하도록 모든 공개 문장에 필수(NOT NULL)다.
 */
export const contentOriginEnum = pgEnum('content_origin', [
  'self_authored',
  'ai_generated',
  'ai_rewritten',
  'public_domain',
]);

/** 콘텐츠 출처 메타 (저작권물 원문 자체는 여기 없다) */
export const sources = pgTable('sources', {
  id: serial('id').primaryKey(),
  sourceType: text('source_type'),
  title: text('title'),
  author: text('author'),
  year: integer('year'),
  url: text('url'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

/** 억양 패턴 (1~8) */
export const intonationPatterns = pgTable('intonation_patterns', {
  id: serial('id').primaryKey(),
  patternName: text('pattern_name').notNull().unique(),
  descriptionKr: text('description_kr'),
  visualNotation: text('visual_notation'), // "↗↘", "↘", "↗"
  exampleSentenceIds: jsonb('example_sentence_ids').$type<string[]>(),
  audioUrl: text('audio_url'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

/** 단어 사전 */
export const vocabulary = pgTable(
  'vocabulary',
  {
    id: text('id').primaryKey(), // "W_A1_0001"
    word: text('word').notNull(),
    pos: text('pos'), // noun, verb, adj …
    cefrLevel: text('cefr_level'),
    meaningKr: text('meaning_kr'),
    pronunciation: text('pronunciation'), // IPA
    pronunciationKr: text('pronunciation_kr'),
    examples: jsonb('examples').$type<{ en: string; kr: string }[]>(),
    firstMonth: integer('first_month'),
    syllableBreakdown: text('syllable_breakdown'), // "beau·ti·ful"
    syllableCount: integer('syllable_count'),
    primaryStressPosition: integer('primary_stress_position'),
    secondaryStressPosition: integer('secondary_stress_position'),
    audioUrl: text('audio_url'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_vocabulary_word').on(t.word),
    index('idx_vocabulary_cefr_level').on(t.cefrLevel),
  ],
);

/** 학습 문장 */
export const sentences = pgTable(
  'sentences',
  {
    id: text('id').primaryKey(), // "M01_001" 일반 / "M01_D101_L01" 대화 / "M01_R01" 복습
    month: integer('month').notNull(),
    week: integer('week').notNull(),
    day: integer('day').notNull(),
    dayType: text('day_type'), // quote, business, conversation, movie, news, ted …
    textEn: text('text_en').notNull(),
    textKr: text('text_kr').notNull(),
    cefrLevel: text('cefr_level'),
    /** ADR-010 §2 — 공개 문장의 출처 구분. 감사 가능하도록 필수. */
    contentOrigin: contentOriginEnum('content_origin').notNull(),
    sourceId: integer('source_id').references(() => sources.id, { onDelete: 'set null' }),
    stressPattern: text('stress_pattern'),
    isNew: boolean('is_new').notNull().default(true),
    notes: text('notes'),
    audioUrl: text('audio_url'),
    chunkBreaks: jsonb('chunk_breaks').$type<number[]>(),
    speakingDurationSec: decimal('speaking_duration_sec'),
    intonationPatternId: integer('intonation_pattern_id').references(() => intonationPatterns.id, {
      onDelete: 'set null',
    }),
    // 대화 필드 — day_type='conversation' 줄에만 값
    dialogueId: text('dialogue_id'), // "DLG_M01_101"
    speaker: text('speaker'),
    dialogueTitle: text('dialogue_title'),
    dialogueSituation: text('dialogue_situation'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_sentences_month').on(t.month),
    index('idx_sentences_week').on(t.week),
    index('idx_sentences_day').on(t.day),
    index('idx_sentences_day_type').on(t.dayType),
    index('idx_sentences_dialogue_id').on(t.dialogueId),
    index('idx_sentences_content_origin').on(t.contentOrigin),
  ],
);

/** 문장-단어 연결 */
export const sentenceWords = pgTable(
  'sentence_words',
  {
    id: serial('id').primaryKey(),
    sentenceId: text('sentence_id')
      .notNull()
      .references(() => sentences.id, { onDelete: 'cascade' }),
    wordId: text('word_id')
      .notNull()
      .references(() => vocabulary.id, { onDelete: 'cascade' }),
    wordText: text('word_text'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_sentence_words_sentence_id').on(t.sentenceId),
    index('idx_sentence_words_word_id').on(t.wordId),
    uniqueIndex('sentence_words_unique').on(t.sentenceId, t.wordId),
  ],
);

/** 문장 IPA */
export const sentenceIpa = pgTable(
  'sentence_ipa',
  {
    id: serial('id').primaryKey(),
    sentenceId: text('sentence_id')
      .notNull()
      .unique()
      .references(() => sentences.id, { onDelete: 'cascade' }),
    ipaFull: text('ipa_full'),
    ipaChunks: jsonb('ipa_chunks').$type<string[]>(),
    stressWords: jsonb('stress_words').$type<string[]>(),
    intonationPatternId: integer('intonation_pattern_id').references(() => intonationPatterns.id, {
      onDelete: 'set null',
    }),
    ttsSpeed: decimal('tts_speed').notNull().default('1.0'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [index('idx_sentence_ipa_sentence').on(t.sentenceId)],
);

/** 콜로케이션 */
export const collocations = pgTable(
  'collocations',
  {
    id: serial('id').primaryKey(),
    phrase: text('phrase').notNull(),
    /** vocabulary.word 를 가리킨다 (id 가 아님 — legacy 관계 계승) */
    baseWord: text('base_word').notNull(),
    collocationType: text('collocation_type'),
    cefrLevel: text('cefr_level'),
    meaningKr: text('meaning_kr'),
    exampleEn: text('example_en'),
    exampleKr: text('example_kr'),
    frequencyRank: integer('frequency_rank'),
    source: text('source').notNull().default('ai_generated'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_collocations_base_word').on(t.baseWord),
    index('idx_collocations_cefr').on(t.cefrLevel),
  ],
);

/** 형태소 */
export const morphemes = pgTable(
  'morphemes',
  {
    id: serial('id').primaryKey(),
    morpheme: text('morpheme').notNull().unique(),
    type: text('type').notNull(), // prefix, suffix, root
    meaningKr: text('meaning_kr'),
    meaningEn: text('meaning_en'),
    origin: text('origin'), // Latin, Greek, Germanic
    examples: jsonb('examples').$type<string[]>(),
    frequencyRank: integer('frequency_rank'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [index('idx_morphemes_type').on(t.type)],
);

/**
 * 단어-형태소 연결.
 * legacy는 `vocabulary_id`가 integer인데 `vocabulary.id`는 text라 조인 자체가 불가능했다 — text로 맞춘다.
 */
export const vocabularyMorphemes = pgTable(
  'vocabulary_morphemes',
  {
    vocabularyId: text('vocabulary_id')
      .notNull()
      .references(() => vocabulary.id, { onDelete: 'cascade' }),
    morphemeId: integer('morpheme_id')
      .notNull()
      .references(() => morphemes.id, { onDelete: 'cascade' }),
    position: text('position'), // prefix, stem, suffix
    orderIndex: integer('order_index').notNull().default(1),
  },
  (t) => [primaryKey({ columns: [t.vocabularyId, t.morphemeId] })],
);

/** 표현 (구동사·이디엄) */
export const expressions = pgTable('expressions', {
  id: serial('id').primaryKey(),
  expression: text('expression').notNull(),
  type: text('type'), // phrasal_verb, idiom
  meaningKr: text('meaning_kr'),
  cefrLevel: text('cefr_level'),
  example1En: text('example1_en'),
  example1Kr: text('example1_kr'),
  example2En: text('example2_en'),
  example2Kr: text('example2_kr'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

// =============================================================================
// Relations
// =============================================================================

export const vocabularyRelations = relations(vocabulary, ({ many }) => ({
  sentenceWords: many(sentenceWords),
  collocations: many(collocations),
  morphemes: many(vocabularyMorphemes),
}));

export const sentencesRelations = relations(sentences, ({ one, many }) => ({
  source: one(sources, { fields: [sentences.sourceId], references: [sources.id] }),
  intonationPattern: one(intonationPatterns, {
    fields: [sentences.intonationPatternId],
    references: [intonationPatterns.id],
  }),
  words: many(sentenceWords),
  ipa: one(sentenceIpa, { fields: [sentences.id], references: [sentenceIpa.sentenceId] }),
}));

export const sentenceWordsRelations = relations(sentenceWords, ({ one }) => ({
  sentence: one(sentences, { fields: [sentenceWords.sentenceId], references: [sentences.id] }),
  vocabulary: one(vocabulary, { fields: [sentenceWords.wordId], references: [vocabulary.id] }),
}));

export const sentenceIpaRelations = relations(sentenceIpa, ({ one }) => ({
  sentence: one(sentences, { fields: [sentenceIpa.sentenceId], references: [sentences.id] }),
  intonationPattern: one(intonationPatterns, {
    fields: [sentenceIpa.intonationPatternId],
    references: [intonationPatterns.id],
  }),
}));

export const collocationsRelations = relations(collocations, ({ one }) => ({
  vocabulary: one(vocabulary, {
    fields: [collocations.baseWord],
    references: [vocabulary.word],
  }),
}));

export const vocabularyMorphemesRelations = relations(vocabularyMorphemes, ({ one }) => ({
  vocabulary: one(vocabulary, {
    fields: [vocabularyMorphemes.vocabularyId],
    references: [vocabulary.id],
  }),
  morpheme: one(morphemes, {
    fields: [vocabularyMorphemes.morphemeId],
    references: [morphemes.id],
  }),
}));

// =============================================================================
// Types
// =============================================================================

export type ContentOrigin = (typeof contentOriginEnum.enumValues)[number];

export type Vocabulary = typeof vocabulary.$inferSelect;
export type NewVocabulary = typeof vocabulary.$inferInsert;
export type Sentence = typeof sentences.$inferSelect;
export type NewSentence = typeof sentences.$inferInsert;
export type SentenceWord = typeof sentenceWords.$inferSelect;
export type NewSentenceWord = typeof sentenceWords.$inferInsert;
export type IntonationPattern = typeof intonationPatterns.$inferSelect;
export type SentenceIpa = typeof sentenceIpa.$inferSelect;
export type Collocation = typeof collocations.$inferSelect;
export type NewCollocation = typeof collocations.$inferInsert;
export type Morpheme = typeof morphemes.$inferSelect;
export type Source = typeof sources.$inferSelect;
export type NewSource = typeof sources.$inferInsert;
export type Expression = typeof expressions.$inferSelect;
