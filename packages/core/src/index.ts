/**
 * @echoa/core — 웹·앱이 공유하는 순수 TS 학습 로직.
 *
 * 규칙: 여기에는 런타임 의존이 `ts-fsrs` 하나뿐이어야 한다.
 * DB·네트워크·브라우저 API·React를 import하지 않는다 — 그래야 웹(Next.js)과
 * 앱(어떤 껍데기든) 양쪽에서 그대로 돌아간다.
 */

export * from './dialogue';
export * from './speech-sequence';
export * from './fsrs';
export * from './gamification';
export * from './review-utils';
export * from './pronunciation';
export * from './errors';
export * from './error-messages';
export * from './rate-limit';
export * from './types';
