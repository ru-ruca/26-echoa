import { describe, it, expect } from 'vitest';
import { selectQuizType, quizResultToRating } from './review-utils';
import type { ReviewItem } from './types/review';

function makeItem(overrides: Partial<ReviewItem>): ReviewItem {
  return {
    progressId: 1,
    itemType: 'sentence',
    itemId: 'M01_001',
    nextReviewAt: '2026-08-07T00:00:00.000Z',
    reps: 0,
    difficulty: null,
    detail: { id: 'M01_001', textEn: 'Hello', textKr: '안녕', cefrLevel: 'A1' },
    ...overrides,
  };
}

describe('selectQuizType', () => {
  it('reps=0 → flip (초기 학습)', () => {
    expect(selectQuizType(makeItem({ reps: 0 }))).toBe('flip');
  });

  it('reps=1 → flip (1회차)', () => {
    expect(selectQuizType(makeItem({ reps: 1 }))).toBe('flip');
  });

  it('reps=2, sentence → fill_blank 또는 listening', () => {
    const result = selectQuizType(makeItem({ reps: 2, itemType: 'sentence' }));
    expect(['fill_blank', 'listening']).toContain(result);
  });

  it('같은 itemId는 항상 같은 quizType 반환 (일관적 랜덤)', () => {
    const item = makeItem({ reps: 2, itemType: 'sentence', itemId: 'M01_001' });
    const first = selectQuizType(item);
    const second = selectQuizType(item);
    expect(first).toBe(second);
  });

  it('reps=2, word → matching', () => {
    expect(selectQuizType(makeItem({ reps: 2, itemType: 'word' }))).toBe('matching');
  });

  it('collocation reps=0 → flip (초기)', () => {
    expect(selectQuizType(makeItem({ reps: 0, itemType: 'collocation' }))).toBe('flip');
  });

  it('collocation reps>=2 → fill_blank (능동 학습)', () => {
    expect(selectQuizType(makeItem({ reps: 2, itemType: 'collocation' }))).toBe('fill_blank');
    expect(selectQuizType(makeItem({ reps: 5, itemType: 'collocation' }))).toBe('fill_blank');
  });
});

describe('quizResultToRating', () => {
  it('정답 → good', () => {
    expect(quizResultToRating(true)).toBe('good');
  });

  it('오답 → again', () => {
    expect(quizResultToRating(false)).toBe('again');
  });
});
