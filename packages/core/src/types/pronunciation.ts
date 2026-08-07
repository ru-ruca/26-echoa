/**
 * 발음 도메인 타입.
 *
 * legacy는 `IntonationPatternId`가 `components/pronunciation/intonation-badge.tsx`
 * ('use client' 파일) 안에 있어 서버 로직이 클라이언트 컴포넌트를 참조했다.
 * 타입만 여기로 승격한다 — 배지 UI는 웹/앱이 각각 그린다.
 */

/** 억양 패턴 1~8 (1 평서문 하강 … 8) */
export type IntonationPatternId = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;
