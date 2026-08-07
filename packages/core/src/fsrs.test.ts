import { describe, it, expect } from 'vitest';
import { Rating } from 'ts-fsrs';
import { parseRating, progressToCard, createEmptyCard, type FsrsCardFields } from './fsrs';

describe('parseRating', () => {
  it('유효한 문자열을 Grade로 변환', () => {
    expect(parseRating('good')).toBe(Rating.Good);
    expect(parseRating('again')).toBe(Rating.Again);
  });

  it('hard/easy는 하위호환으로 Good에 매핑', () => {
    expect(parseRating('hard')).toBe(Rating.Good);
    expect(parseRating('easy')).toBe(Rating.Good);
  });

  it('잘못된 입력에 null 반환', () => {
    expect(parseRating('invalid')).toBeNull();
    expect(parseRating('')).toBeNull();
  });
});

describe('progressToCard', () => {
  it('신규 항목(reps=0, state=0)은 빈 카드 반환', () => {
    const progress: FsrsCardFields = {
      fsrsState: 0,
      fsrsReps: 0,
      nextReviewAt: null,
      fsrsStability: null,
      fsrsDifficulty: null,
      fsrsElapsedDays: null,
      fsrsScheduledDays: null,
      fsrsLapses: null,
      fsrsLastReview: null,
    };

    const card = progressToCard(progress);
    const empty = createEmptyCard();

    expect(card.reps).toBe(empty.reps);
    expect(card.state).toBe(empty.state);
  });

  it('기존 항목은 learning_steps=0 포함', () => {
    const progress: FsrsCardFields = {
      fsrsState: 2,
      fsrsReps: 5,
      nextReviewAt: new Date(),
      fsrsStability: 10.5,
      fsrsDifficulty: 5.2,
      fsrsElapsedDays: 3,
      fsrsScheduledDays: 7,
      fsrsLapses: 1,
      fsrsLastReview: new Date(),
    };

    const card = progressToCard(progress);
    expect(card.learning_steps).toBe(0);
    expect(card.reps).toBe(5);
    expect(card.stability).toBe(10.5);
  });
});
