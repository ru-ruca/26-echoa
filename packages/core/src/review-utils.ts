import type { QuizMode, RatingValue, ReviewItem } from './types/review';

/**
 * FSRS 반복 횟수와 아이템 타입에 따라 복습 퀴즈 유형을 선택한다.
 *
 * - reps 0~1 (초기 학습): 플립카드 유지 (아직 익숙하지 않아 퀴즈는 좌절감 유발)
 * - reps >= 2 + sentence: fill_blank 또는 listening 랜덤
 * - reps >= 2 + word: matching (단어 4개 그룹핑 필요)
 * - reps >= 2 + collocation: fill_blank (빈칸 채우기)
 */
export function selectQuizType(item: ReviewItem): QuizMode {
  // 초기 학습: 플립카드
  if (!item.reps || item.reps <= 1) return 'flip';

  // 문장: fill_blank 또는 listening 랜덤
  if (item.itemType === 'sentence') {
    // 안정적 랜덤: itemId 기반 해시로 결정 (리렌더 시 일관성 유지)
    const hash = item.itemId.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
    return hash % 2 === 0 ? 'fill_blank' : 'listening';
  }

  // 단어: matching (호출 측에서 4개 그룹핑 필요)
  if (item.itemType === 'word') {
    return 'matching';
  }

  // collocation: reps >= 2면 빈칸 채우기, 초기는 플립카드
  if (item.itemType === 'collocation') {
    return 'fill_blank';
  }

  return 'flip';
}

/** 퀴즈 정답/오답 결과를 FSRS rating으로 매핑 */
export function quizResultToRating(correct: boolean): RatingValue {
  return correct ? 'good' : 'again';
}
