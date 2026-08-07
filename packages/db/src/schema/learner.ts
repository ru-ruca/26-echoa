/**
 * 학습자 스키마 — 진행·게이미피케이션.
 *
 * legacy는 `user_id`가 참조 대상 없는 text 컬럼이었다(익명 device UUID). 여기서는
 * 전부 `user.id`를 FK로 참조한다 — 계정이 사라지면 그 사람의 학습 기록도 함께 정리된다.
 */

import { relations } from 'drizzle-orm';
import {
  index,
  integer,
  pgTable,
  real,
  serial,
  text,
  timestamp,
  uniqueIndex,
} from 'drizzle-orm/pg-core';

import { users } from './auth';
import { vocabulary } from './content';

/**
 * 복습 대상 종류. `user_progress.item_id` 가 어느 테이블을 가리키는지 결정한다 —
 * sentence → sentences.id · word → vocabulary.id · collocation → collocations.id
 */
export const REVIEW_ITEM_TYPES = ['sentence', 'word', 'collocation'] as const;

/** 찜하기 */
export const favorites = pgTable(
  'favorites',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }),
    wordId: text('word_id')
      .notNull()
      .references(() => vocabulary.id, { onDelete: 'cascade' }),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_favorites_user').on(t.userId),
    index('idx_favorites_word').on(t.wordId),
    uniqueIndex('favorites_user_word_unique').on(t.userId, t.wordId),
  ],
);

/**
 * 학습 진행 (FSRS 통합).
 *
 * `itemId`는 itemType에 따라 sentences.id · vocabulary.id · collocations.id 를 가리킨다 —
 * 다형 참조라 DB FK를 걸 수 없다. 무결성은 적재·API 레이어가 지킨다.
 */
export const userProgress = pgTable(
  'user_progress',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }),
    itemType: text('item_type').notNull(), // 'sentence' | 'word' | 'collocation'
    itemId: text('item_id').notNull(),
    correctCount: integer('correct_count').notNull().default(0),
    wrongCount: integer('wrong_count').notNull().default(0),
    lastReviewedAt: timestamp('last_reviewed_at'),
    nextReviewAt: timestamp('next_review_at'),
    // FSRS — @echoa/core 의 FsrsCardFields 와 컬럼이 1:1 대응한다
    fsrsDifficulty: real('fsrs_difficulty').default(0), // D (0~10)
    fsrsStability: real('fsrs_stability').default(0), // S (일수)
    fsrsElapsedDays: integer('fsrs_elapsed_days').default(0),
    fsrsScheduledDays: integer('fsrs_scheduled_days').default(0),
    fsrsReps: integer('fsrs_reps').default(0),
    fsrsLapses: integer('fsrs_lapses').default(0),
    fsrsState: integer('fsrs_state').default(0), // 0 New / 1 Learning / 2 Review / 3 Relearning
    fsrsLastReview: timestamp('fsrs_last_review'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_user_progress_user').on(t.userId),
    index('idx_user_progress_next_review').on(t.userId, t.nextReviewAt),
    uniqueIndex('user_progress_user_item_unique').on(t.userId, t.itemType, t.itemId),
  ],
);

/** 스트릭 */
export const userStreaks = pgTable(
  'user_streaks',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .unique()
      .references(() => users.id, { onDelete: 'cascade' }),
    currentStreak: integer('current_streak').notNull().default(0),
    longestStreak: integer('longest_streak').notNull().default(0),
    lastStudyDate: text('last_study_date'), // 'YYYY-MM-DD'
    freezeAvailableAt: timestamp('freeze_available_at'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => [index('idx_user_streaks_user').on(t.userId)],
);

/** XP 누적 */
export const userXp = pgTable(
  'user_xp',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .unique()
      .references(() => users.id, { onDelete: 'cascade' }),
    totalXp: integer('total_xp').notNull().default(0),
    dailyXp: integer('daily_xp').notNull().default(0),
    dailyXpDate: text('daily_xp_date'), // 'YYYY-MM-DD' — 일일 XP 리셋 기준
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => [index('idx_user_xp_user').on(t.userId)],
);

/** XP 히스토리 */
export const xpHistory = pgTable(
  'xp_history',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }),
    xpAmount: integer('xp_amount').notNull(),
    /** @echoa/core 의 XpSource 와 같은 값 집합 */
    source: text('source').notNull(),
    itemType: text('item_type'),
    itemId: text('item_id'),
    createdAt: timestamp('created_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_xp_history_user').on(t.userId),
    index('idx_xp_history_date').on(t.userId, t.createdAt),
  ],
);

/** 배지 정의 */
export const badges = pgTable('badges', {
  id: serial('id').primaryKey(),
  name: text('name').notNull().unique(),
  descriptionKr: text('description_kr').notNull(),
  icon: text('icon').notNull(),
  /** @echoa/core 의 BadgeConditionType 과 같은 값 집합 */
  conditionType: text('condition_type').notNull(),
  conditionValue: integer('condition_value').notNull(),
  bonusXp: integer('bonus_xp').notNull().default(0),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

/** 배지 획득 */
export const userBadges = pgTable(
  'user_badges',
  {
    id: serial('id').primaryKey(),
    userId: text('user_id')
      .notNull()
      .references(() => users.id, { onDelete: 'cascade' }),
    badgeId: integer('badge_id')
      .notNull()
      .references(() => badges.id, { onDelete: 'cascade' }),
    earnedAt: timestamp('earned_at').notNull().defaultNow(),
  },
  (t) => [
    index('idx_user_badges_user').on(t.userId),
    uniqueIndex('user_badges_user_badge_unique').on(t.userId, t.badgeId),
  ],
);

// =============================================================================
// Relations
// =============================================================================

export const favoritesRelations = relations(favorites, ({ one }) => ({
  user: one(users, { fields: [favorites.userId], references: [users.id] }),
  word: one(vocabulary, { fields: [favorites.wordId], references: [vocabulary.id] }),
}));

export const userProgressRelations = relations(userProgress, ({ one }) => ({
  user: one(users, { fields: [userProgress.userId], references: [users.id] }),
}));

export const userBadgesRelations = relations(userBadges, ({ one }) => ({
  user: one(users, { fields: [userBadges.userId], references: [users.id] }),
  badge: one(badges, { fields: [userBadges.badgeId], references: [badges.id] }),
}));

export const usersRelations = relations(users, ({ many, one }) => ({
  progress: many(userProgress),
  favorites: many(favorites),
  badges: many(userBadges),
  streak: one(userStreaks, { fields: [users.id], references: [userStreaks.userId] }),
  xp: one(userXp, { fields: [users.id], references: [userXp.userId] }),
}));

// =============================================================================
// Types
// =============================================================================

export type Favorite = typeof favorites.$inferSelect;
export type UserProgress = typeof userProgress.$inferSelect;
export type NewUserProgress = typeof userProgress.$inferInsert;
export type UserStreak = typeof userStreaks.$inferSelect;
export type UserXp = typeof userXp.$inferSelect;
export type XpHistory = typeof xpHistory.$inferSelect;
export type NewXpHistory = typeof xpHistory.$inferInsert;
export type Badge = typeof badges.$inferSelect;
export type NewBadge = typeof badges.$inferInsert;
export type UserBadge = typeof userBadges.$inferSelect;
