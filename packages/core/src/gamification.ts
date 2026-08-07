/**
 * 게이미피케이션 — 순수 규칙만.
 *
 * legacy `lib/gamification.ts`(319줄)는 규칙과 DB 쓰기가 한 파일에 섞여 있어
 * `@/db`를 런타임 import 했다. 그래서 테스트가 DB 모듈을 통째로 mock 해야 했고,
 * 결과적으로 로직 테스트가 한 줄도 없었다(상수 3개만 assert).
 *
 * 여기에는 입력→출력이 결정적인 규칙만 둔다. 쓰기(insert/update)는
 * `packages/api`가 이 함수들의 반환값을 받아 수행한다.
 */

import { Rating, type Grade } from 'ts-fsrs';

// =============================================================================
// XP 규칙
// =============================================================================

export const XP_REWARDS = {
  LESSON_COMPLETE: 10,
  REVIEW_GOOD: 5,
  REVIEW_AGAIN: 1,
  QUIZ_CORRECT: 5,
  DAILY_GOAL: 20,
  STREAK_7_BONUS: 50,
} as const;

export type XpSource =
  | 'lesson_complete'
  | 'review_good'
  | 'review_again'
  | 'quiz_correct'
  | 'daily_goal'
  | 'streak_bonus'
  | 'badge_bonus';

/** Rating에 따른 XP 보상 (2버튼: Again/Good — D-01) */
export function getXpForRating(rating: Grade, isNewLesson: boolean): number {
  if (isNewLesson) return XP_REWARDS.LESSON_COMPLETE;

  switch (rating) {
    case Rating.Again:
      return XP_REWARDS.REVIEW_AGAIN;
    case Rating.Good:
    default:
      return XP_REWARDS.REVIEW_GOOD;
  }
}

// =============================================================================
// 날짜 (타임존은 인자로 받는다 — legacy는 'Asia/Seoul' 하드코딩이었다)
// =============================================================================

export const DEFAULT_TIMEZONE = 'Asia/Seoul';

/** 지정 타임존 기준 날짜 문자열 (YYYY-MM-DD) */
export function formatDateInTz(date: Date, tz: string = DEFAULT_TIMEZONE): string {
  return new Intl.DateTimeFormat('sv-SE', {
    timeZone: tz,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date);
}

export function getTodayString(tz: string = DEFAULT_TIMEZONE, now: Date = new Date()): string {
  return formatDateInTz(now, tz);
}

export function getYesterdayString(tz: string = DEFAULT_TIMEZONE, now: Date = new Date()): string {
  const d = new Date(now);
  d.setDate(d.getDate() - 1);
  return formatDateInTz(d, tz);
}

// =============================================================================
// 스트릭 전이 규칙
// =============================================================================

/** 저장된 스트릭 상태 (DB 행에서 필요한 부분만) */
export interface StreakRecord {
  currentStreak: number | null;
  longestStreak: number | null;
  lastStudyDate: string | null;
}

export interface StreakTransition {
  currentStreak: number;
  longestStreak: number;
  /** 오늘 처음 학습해서 값이 바뀌었는지 — false면 DB 쓰기가 필요 없다 */
  isNewStreak: boolean;
  /** 7일 배수 도달 — 호출 측이 보너스 XP를 지급해야 하는지 */
  awardsStreakBonus: boolean;
}

/**
 * 학습 완료 시 스트릭이 어떻게 바뀌는지 계산한다.
 *
 * - 기록 없음 → 1일차 시작
 * - 오늘 이미 학습 → 변화 없음
 * - 어제 학습 → +1
 * - 그 외 → 1로 리셋
 */
export function nextStreak(
  record: StreakRecord | null,
  today: string,
  yesterday: string,
): StreakTransition {
  if (record === null) {
    return {
      currentStreak: 1,
      longestStreak: 1,
      isNewStreak: true,
      awardsStreakBonus: false,
    };
  }

  if (record.lastStudyDate === today) {
    return {
      currentStreak: record.currentStreak ?? 0,
      longestStreak: record.longestStreak ?? 0,
      isNewStreak: false,
      awardsStreakBonus: false,
    };
  }

  const current = record.lastStudyDate === yesterday ? (record.currentStreak ?? 0) + 1 : 1;

  return {
    currentStreak: current,
    longestStreak: Math.max(current, record.longestStreak ?? 0),
    isNewStreak: true,
    awardsStreakBonus: current > 0 && current % 7 === 0,
  };
}

export interface StreakView {
  currentStreak: number;
  longestStreak: number;
  studiedToday: boolean;
}

/** 조회용 — 마지막 학습이 오늘도 어제도 아니면 스트릭은 이미 끊긴 것으로 본다. */
export function resolveStreakView(
  record: StreakRecord | null,
  today: string,
  yesterday: string,
): StreakView {
  if (record === null) {
    return { currentStreak: 0, longestStreak: 0, studiedToday: false };
  }

  const alive = record.lastStudyDate === today || record.lastStudyDate === yesterday;

  return {
    currentStreak: alive ? (record.currentStreak ?? 0) : 0,
    longestStreak: record.longestStreak ?? 0,
    studiedToday: record.lastStudyDate === today,
  };
}

// =============================================================================
// 일일 XP 롤오버 규칙
// =============================================================================

export interface DailyXpRecord {
  totalXp: number | null;
  dailyXp: number | null;
  dailyXpDate: string | null;
}

/** XP 지급 후의 누적값. 날짜가 바뀌었으면 dailyXp를 이어붙이지 않고 새로 센다. */
export function applyXpGain(
  record: DailyXpRecord | null,
  amount: number,
  today: string,
): { totalXp: number; dailyXp: number; dailyXpDate: string } {
  if (record === null) {
    return { totalXp: amount, dailyXp: amount, dailyXpDate: today };
  }

  const isNewDay = record.dailyXpDate !== today;
  return {
    totalXp: (record.totalXp ?? 0) + amount,
    dailyXp: isNewDay ? amount : (record.dailyXp ?? 0) + amount,
    dailyXpDate: today,
  };
}

/** 조회용 — 날짜가 지났으면 오늘 XP는 0으로 보인다. */
export function resolveXpView(
  record: DailyXpRecord | null,
  today: string,
): { totalXp: number; dailyXp: number } {
  if (record === null) return { totalXp: 0, dailyXp: 0 };
  return {
    totalXp: record.totalXp ?? 0,
    dailyXp: record.dailyXpDate === today ? (record.dailyXp ?? 0) : 0,
  };
}

// =============================================================================
// 배지 조건 판정
// =============================================================================

export type BadgeConditionType = 'streak' | 'xp' | 'lessons' | 'reviews' | 'month_complete';

export interface BadgeCondition {
  conditionType: string;
  conditionValue: number;
}

export interface LearnerStats {
  currentStreak: number;
  totalXp: number;
  completedLessons: number;
  completedReviews: number;
}

/**
 * 배지 조건 충족 여부.
 * `month_complete`는 커리큘럼 진행 조회가 필요해 여기서 판정하지 않는다(항상 false).
 */
export function isBadgeConditionMet(badge: BadgeCondition, stats: LearnerStats): boolean {
  switch (badge.conditionType) {
    case 'streak':
      return stats.currentStreak >= badge.conditionValue;
    case 'xp':
      return stats.totalXp >= badge.conditionValue;
    case 'lessons':
      return stats.completedLessons >= badge.conditionValue;
    case 'reviews':
      return stats.completedReviews >= badge.conditionValue;
    default:
      return false;
  }
}

/** 아직 못 받은 배지 중 조건을 충족한 것만 고른다. */
export function selectNewlyEarnedBadges<T extends BadgeCondition & { id: number }>(
  allBadges: readonly T[],
  earnedBadgeIds: readonly number[],
  stats: LearnerStats,
): T[] {
  const earned = new Set(earnedBadgeIds);
  return allBadges.filter((b) => !earned.has(b.id) && isBadgeConditionMet(b, stats));
}
