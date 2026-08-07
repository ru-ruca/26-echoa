import { describe, it, expect } from 'vitest';
import { Rating } from 'ts-fsrs';
import {
  XP_REWARDS,
  getXpForRating,
  formatDateInTz,
  getTodayString,
  getYesterdayString,
  nextStreak,
  resolveStreakView,
  applyXpGain,
  resolveXpView,
  isBadgeConditionMet,
  selectNewlyEarnedBadges,
  type StreakRecord,
  type LearnerStats,
} from './gamification';

// legacy gamification.test.ts 는 XP_REWARDS 상수 3개만 assert 하는 껍데기였다
// (@/db 를 통째로 mock 해야 해서 로직을 건드릴 수 없었다).
// DB I/O 를 분리한 지금은 규칙을 직접 검증한다.

describe('getXpForRating', () => {
  it('신규 학습은 rating 무관 10XP', () => {
    expect(getXpForRating(Rating.Good, true)).toBe(XP_REWARDS.LESSON_COMPLETE);
    expect(getXpForRating(Rating.Again, true)).toBe(XP_REWARDS.LESSON_COMPLETE);
  });

  it('복습 Good → 5XP, Again → 1XP', () => {
    expect(getXpForRating(Rating.Good, false)).toBe(XP_REWARDS.REVIEW_GOOD);
    expect(getXpForRating(Rating.Again, false)).toBe(XP_REWARDS.REVIEW_AGAIN);
  });
});

describe('날짜 유틸', () => {
  it('타임존 기준 YYYY-MM-DD 로 포맷', () => {
    // 2026-08-07T15:30Z 는 Asia/Seoul 기준 2026-08-08 00:30
    const utcEvening = new Date('2026-08-07T15:30:00Z');
    expect(formatDateInTz(utcEvening, 'Asia/Seoul')).toBe('2026-08-08');
    expect(formatDateInTz(utcEvening, 'UTC')).toBe('2026-08-07');
  });

  it('타임존을 인자로 받는다 (legacy 는 Asia/Seoul 하드코딩)', () => {
    const now = new Date('2026-08-07T01:00:00Z');
    expect(getTodayString('UTC', now)).toBe('2026-08-07');
    expect(getTodayString('Asia/Seoul', now)).toBe('2026-08-07');
    expect(getYesterdayString('UTC', now)).toBe('2026-08-06');
  });

  it('어제는 오늘보다 하루 앞선다', () => {
    const now = new Date('2026-03-01T05:00:00Z');
    expect(getYesterdayString('UTC', now)).toBe('2026-02-28');
  });
});

describe('nextStreak', () => {
  const today = '2026-08-07';
  const yesterday = '2026-08-06';

  it('기록 없음 → 1일차 시작', () => {
    expect(nextStreak(null, today, yesterday)).toEqual({
      currentStreak: 1,
      longestStreak: 1,
      isNewStreak: true,
      awardsStreakBonus: false,
    });
  });

  it('오늘 이미 학습 → 변화 없음 (DB 쓰기 불필요)', () => {
    const record: StreakRecord = {
      currentStreak: 5,
      longestStreak: 9,
      lastStudyDate: today,
    };
    expect(nextStreak(record, today, yesterday)).toEqual({
      currentStreak: 5,
      longestStreak: 9,
      isNewStreak: false,
      awardsStreakBonus: false,
    });
  });

  it('어제 학습 → +1', () => {
    const record: StreakRecord = {
      currentStreak: 3,
      longestStreak: 3,
      lastStudyDate: yesterday,
    };
    const result = nextStreak(record, today, yesterday);
    expect(result.currentStreak).toBe(4);
    expect(result.longestStreak).toBe(4);
    expect(result.isNewStreak).toBe(true);
  });

  it('하루 이상 건너뜀 → 1로 리셋, 최장 기록은 보존', () => {
    const record: StreakRecord = {
      currentStreak: 12,
      longestStreak: 12,
      lastStudyDate: '2026-08-01',
    };
    const result = nextStreak(record, today, yesterday);
    expect(result.currentStreak).toBe(1);
    expect(result.longestStreak).toBe(12);
  });

  it('7일 배수 도달 시 보너스 플래그', () => {
    const at6: StreakRecord = { currentStreak: 6, longestStreak: 6, lastStudyDate: yesterday };
    expect(nextStreak(at6, today, yesterday).awardsStreakBonus).toBe(true);

    const at5: StreakRecord = { currentStreak: 5, longestStreak: 5, lastStudyDate: yesterday };
    expect(nextStreak(at5, today, yesterday).awardsStreakBonus).toBe(false);

    const at13: StreakRecord = { currentStreak: 13, longestStreak: 13, lastStudyDate: yesterday };
    expect(nextStreak(at13, today, yesterday).awardsStreakBonus).toBe(true);
  });

  it('리셋된 1일차는 보너스 대상이 아니다', () => {
    const stale: StreakRecord = { currentStreak: 7, longestStreak: 7, lastStudyDate: '2026-07-01' };
    expect(nextStreak(stale, today, yesterday).awardsStreakBonus).toBe(false);
  });
});

describe('resolveStreakView', () => {
  const today = '2026-08-07';
  const yesterday = '2026-08-06';

  it('기록 없으면 0', () => {
    expect(resolveStreakView(null, today, yesterday)).toEqual({
      currentStreak: 0,
      longestStreak: 0,
      studiedToday: false,
    });
  });

  it('오늘 학습했으면 studiedToday=true', () => {
    const record: StreakRecord = { currentStreak: 4, longestStreak: 8, lastStudyDate: today };
    expect(resolveStreakView(record, today, yesterday)).toEqual({
      currentStreak: 4,
      longestStreak: 8,
      studiedToday: true,
    });
  });

  it('어제까지 학습했으면 스트릭은 살아있지만 studiedToday=false', () => {
    const record: StreakRecord = { currentStreak: 4, longestStreak: 8, lastStudyDate: yesterday };
    const view = resolveStreakView(record, today, yesterday);
    expect(view.currentStreak).toBe(4);
    expect(view.studiedToday).toBe(false);
  });

  it('오늘도 어제도 아니면 이미 끊긴 것으로 0 표시', () => {
    const record: StreakRecord = {
      currentStreak: 4,
      longestStreak: 8,
      lastStudyDate: '2026-08-01',
    };
    const view = resolveStreakView(record, today, yesterday);
    expect(view.currentStreak).toBe(0);
    expect(view.longestStreak).toBe(8);
  });
});

describe('applyXpGain / resolveXpView', () => {
  const today = '2026-08-07';

  it('기록 없으면 첫 지급', () => {
    expect(applyXpGain(null, 10, today)).toEqual({
      totalXp: 10,
      dailyXp: 10,
      dailyXpDate: today,
    });
  });

  it('같은 날은 누적', () => {
    const record = { totalXp: 100, dailyXp: 30, dailyXpDate: today };
    expect(applyXpGain(record, 5, today)).toEqual({
      totalXp: 105,
      dailyXp: 35,
      dailyXpDate: today,
    });
  });

  it('날짜가 바뀌면 dailyXp 는 새로 센다', () => {
    const record = { totalXp: 100, dailyXp: 30, dailyXpDate: '2026-08-06' };
    expect(applyXpGain(record, 5, today)).toEqual({
      totalXp: 105,
      dailyXp: 5,
      dailyXpDate: today,
    });
  });

  it('조회 시 지난 날짜의 dailyXp 는 0으로 보인다', () => {
    expect(resolveXpView({ totalXp: 100, dailyXp: 30, dailyXpDate: '2026-08-06' }, today)).toEqual({
      totalXp: 100,
      dailyXp: 0,
    });
    expect(resolveXpView(null, today)).toEqual({ totalXp: 0, dailyXp: 0 });
  });
});

describe('배지 판정', () => {
  const stats: LearnerStats = {
    currentStreak: 7,
    totalXp: 500,
    completedLessons: 30,
    completedReviews: 120,
  };

  it('조건 타입별로 판정', () => {
    expect(isBadgeConditionMet({ conditionType: 'streak', conditionValue: 7 }, stats)).toBe(true);
    expect(isBadgeConditionMet({ conditionType: 'streak', conditionValue: 8 }, stats)).toBe(false);
    expect(isBadgeConditionMet({ conditionType: 'xp', conditionValue: 500 }, stats)).toBe(true);
    expect(isBadgeConditionMet({ conditionType: 'lessons', conditionValue: 31 }, stats)).toBe(
      false,
    );
    expect(isBadgeConditionMet({ conditionType: 'reviews', conditionValue: 100 }, stats)).toBe(
      true,
    );
  });

  it('month_complete 는 커리큘럼 조회가 필요해 여기서는 항상 false', () => {
    expect(isBadgeConditionMet({ conditionType: 'month_complete', conditionValue: 1 }, stats)).toBe(
      false,
    );
  });

  it('알 수 없는 조건 타입은 false', () => {
    expect(isBadgeConditionMet({ conditionType: 'nonsense', conditionValue: 0 }, stats)).toBe(
      false,
    );
  });

  it('이미 받은 배지는 다시 고르지 않는다', () => {
    const all = [
      { id: 1, conditionType: 'streak', conditionValue: 3 },
      { id: 2, conditionType: 'xp', conditionValue: 100 },
      { id: 3, conditionType: 'lessons', conditionValue: 999 },
    ];
    expect(selectNewlyEarnedBadges(all, [1], stats).map((b) => b.id)).toEqual([2]);
    expect(selectNewlyEarnedBadges(all, [], stats).map((b) => b.id)).toEqual([1, 2]);
  });
});
