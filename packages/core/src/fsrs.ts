import {
  createEmptyCard,
  fsrs,
  generatorParameters,
  Rating,
  State,
  type Card,
  type Grade,
  type RecordLog,
} from 'ts-fsrs';

// =============================================================================
// FSRS 인스턴스 (싱글톤)
// =============================================================================

const params = generatorParameters({
  maximum_interval: 365, // 최대 복습 간격: 1년
  request_retention: 0.9, // 목표 유지율: 90%
});

const scheduler = fsrs(params);

// =============================================================================
// 저장소 ↔ FSRS Card 변환
// =============================================================================

/**
 * FSRS 계산에 필요한 최소 필드.
 *
 * legacy는 여기서 `UserProgress`(drizzle `$inferSelect`)를 직접 import 했다.
 * 그러면 core → db 의존이 생겨 core가 순수 TS로 남지 못한다. 필요한 컬럼만
 * 구조적으로 선언해 두면 `packages/db`의 `UserProgress`가 그대로 대입된다.
 */
export interface FsrsCardFields {
  nextReviewAt: Date | null;
  fsrsStability: number | null;
  fsrsDifficulty: number | null;
  fsrsElapsedDays: number | null;
  fsrsScheduledDays: number | null;
  fsrsReps: number | null;
  fsrsLapses: number | null;
  fsrsState: number | null;
  fsrsLastReview: Date | null;
}

/** 저장소의 진행 행을 FSRS Card 객체로 변환 */
export function progressToCard(progress: FsrsCardFields): Card {
  // 신규 항목이면 빈 카드 반환
  if (progress.fsrsState === 0 && progress.fsrsReps === 0) {
    return createEmptyCard();
  }

  return {
    due: progress.nextReviewAt ?? new Date(),
    stability: progress.fsrsStability ?? 0,
    difficulty: progress.fsrsDifficulty ?? 0,
    elapsed_days: progress.fsrsElapsedDays ?? 0,
    scheduled_days: progress.fsrsScheduledDays ?? 0,
    reps: progress.fsrsReps ?? 0,
    lapses: progress.fsrsLapses ?? 0,
    state: (progress.fsrsState ?? 0) as State,
    last_review: progress.fsrsLastReview ?? undefined,
    learning_steps: 0,
  };
}

/** FSRS Card 결과를 저장소 업데이트용 객체로 변환 */
export function cardToProgressUpdate(card: Card) {
  return {
    fsrsDifficulty: card.difficulty,
    fsrsStability: card.stability,
    fsrsElapsedDays: card.elapsed_days,
    fsrsScheduledDays: card.scheduled_days,
    fsrsReps: card.reps,
    fsrsLapses: card.lapses,
    fsrsState: card.state as number,
    fsrsLastReview: card.last_review ?? new Date(),
    nextReviewAt: card.due,
    lastReviewedAt: new Date(),
    updatedAt: new Date(),
  };
}

// =============================================================================
// 스케줄링
// =============================================================================

/** 현재 카드에 대해 4가지 평가별 스케줄 계산 */
export function getSchedules(card: Card, now: Date = new Date()): RecordLog {
  return scheduler.repeat(card, now);
}

/** 특정 평가(rating)에 대한 스케줄 결과 반환 */
export function scheduleByRating(card: Card, rating: Grade, now: Date = new Date()) {
  const schedules = scheduler.repeat(card, now);
  return schedules[rating];
}

// =============================================================================
// Rating 유틸리티
// =============================================================================

/** 문자열 rating을 FSRS Grade로 변환 (hard/easy는 하위호환으로 Good에 매핑) */
export function parseRating(ratingStr: string): Grade | null {
  const map: Record<string, Grade> = {
    again: Rating.Again,
    hard: Rating.Good,
    good: Rating.Good,
    easy: Rating.Good,
  };
  return map[ratingStr.toLowerCase()] ?? null;
}

// =============================================================================
// 복습 큐 유틸리티
// =============================================================================

/** 복습 항목의 우선순위 점수 계산 (낮을수록 우선) */
export function getReviewPriority(progress: Pick<FsrsCardFields, 'nextReviewAt'>): number {
  if (!progress.nextReviewAt) return Infinity;

  const now = new Date();
  const due = new Date(progress.nextReviewAt);
  const overdueMs = now.getTime() - due.getTime();

  // 기한이 많이 지날수록 우선순위 높음 (값이 작을수록)
  return -overdueMs;
}

// Re-export — 소비자가 ts-fsrs를 직접 import하지 않도록
export { Rating, State, createEmptyCard };
export type { Card, Grade, RecordLog };
