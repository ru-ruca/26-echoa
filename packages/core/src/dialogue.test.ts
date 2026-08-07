import { describe, it, expect } from 'vitest';
import { buildDialogueWindow } from './dialogue';

const lines = (n: number) => Array.from({ length: n }, (_, i) => `L${i + 1}`);

describe('buildDialogueWindow', () => {
  it('4줄 이하는 전체 반환 (year3/4 대화)', () => {
    expect(buildDialogueWindow(lines(4), 0)).toEqual(['L1', 'L2', 'L3', 'L4']);
    expect(buildDialogueWindow(lines(2), 1)).toEqual(['L1', 'L2']);
    expect(buildDialogueWindow([], 0)).toEqual([]);
  });

  it('중간 초점: 이전 1 + 현재 + 이후 2', () => {
    expect(buildDialogueWindow(lines(10), 4)).toEqual(['L4', 'L5', 'L6', 'L7']);
  });

  it('첫 줄 초점: 앞이 없으면 뒤로 채워 4줄 유지', () => {
    expect(buildDialogueWindow(lines(10), 0)).toEqual(['L1', 'L2', 'L3', 'L4']);
  });

  it('마지막 줄 초점: 뒤가 없으면 앞으로 채워 4줄 유지', () => {
    expect(buildDialogueWindow(lines(10), 9)).toEqual(['L7', 'L8', 'L9', 'L10']);
    expect(buildDialogueWindow(lines(10), 8)).toEqual(['L7', 'L8', 'L9', 'L10']);
  });

  it('범위 밖 focusIndex는 안쪽으로 클램프', () => {
    expect(buildDialogueWindow(lines(10), -3)).toEqual(['L1', 'L2', 'L3', 'L4']);
    expect(buildDialogueWindow(lines(10), 99)).toEqual(['L7', 'L8', 'L9', 'L10']);
  });

  it('원본 배열을 변경하지 않는다', () => {
    const src = lines(10);
    buildDialogueWindow(src, 5);
    expect(src).toHaveLength(10);
  });
});
