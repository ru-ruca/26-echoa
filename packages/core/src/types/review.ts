/**
 * 복습 도메인 타입.
 *
 * legacy는 이 타입들이 `components/review/types.ts`(UI 폴더)에 있어서 로직이 UI를
 * 거꾸로 참조했다. 여기로 승격해 의존 방향을 core → UI 로 바로잡는다.
 * `QuizMode`가 legacy에서 두 곳에 중복 정의돼 있던 것도 여기 한 곳으로 합친다.
 */

export type ReviewItemType = 'sentence' | 'word' | 'collocation';

export interface ReviewSentenceDetail {
  id: string;
  textEn: string;
  textKr: string;
  cefrLevel: string | null;
}

export interface ReviewWordDetail {
  id: string;
  word: string;
  pronunciation: string | null;
  meaningKr: string | null;
  cefrLevel: string | null;
  pos: string | null;
}

export interface ReviewCollocationDetail {
  id: number;
  phrase: string;
  baseWord: string;
  collocationType: string | null;
  meaningKr: string | null;
  exampleEn: string | null;
  exampleKr: string | null;
}

export type ReviewDetail = ReviewSentenceDetail | ReviewWordDetail | ReviewCollocationDetail;

export interface ReviewItem {
  progressId: number;
  itemType: ReviewItemType;
  itemId: string;
  nextReviewAt: string;
  reps: number | null;
  difficulty: number | null;
  detail: ReviewDetail;
}

/** 복습 응답 2버튼 (D-01: hard/easy 제거) */
export type RatingValue = 'again' | 'good';

/** 복습 퀴즈 유형 */
export type QuizMode = 'flip' | 'fill_blank' | 'listening' | 'matching';
