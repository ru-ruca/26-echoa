import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { SpeechSequenceController, type SpeakLineFn } from './speech-sequence';

/** speakLine fake: 호출을 기록하고, finish()로 완료 콜백을 수동 발화한다 */
function createFakeSynth() {
  const spoken: string[] = [];
  const pending: Array<() => void> = [];
  const speakLine: SpeakLineFn = (text, onFinished) => {
    spoken.push(text);
    pending.push(onFinished);
  };
  const finish = () => {
    const cb = pending.shift();
    cb?.();
  };
  const cancel = vi.fn();
  return { spoken, speakLine, finish, cancel };
}

describe('SpeechSequenceController', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  it('줄 사이 pause를 두고 순서대로 재생하고 끝에 onEnd 1회', () => {
    const synth = createFakeSynth();
    const controller = new SpeechSequenceController(synth.speakLine, synth.cancel, 450);
    const onEnd = vi.fn();

    controller.play(['A', 'B', 'C'], onEnd);
    expect(synth.spoken).toEqual(['A']);

    synth.finish(); // A 완료 → pause 대기
    expect(synth.spoken).toEqual(['A']);
    vi.advanceTimersByTime(450);
    expect(synth.spoken).toEqual(['A', 'B']);

    synth.finish();
    vi.advanceTimersByTime(450);
    expect(synth.spoken).toEqual(['A', 'B', 'C']);

    expect(onEnd).not.toHaveBeenCalled();
    synth.finish(); // 마지막 줄은 pause 없이 즉시 종료
    expect(onEnd).toHaveBeenCalledTimes(1);
  });

  it('stop 후 도착한 완료 콜백(cancel로 인한 onend/onerror)은 무시된다', () => {
    const synth = createFakeSynth();
    const controller = new SpeechSequenceController(synth.speakLine, synth.cancel, 450);
    const onEnd = vi.fn();

    controller.play(['A', 'B'], onEnd);
    controller.stop();
    expect(synth.cancel).toHaveBeenCalled();

    synth.finish(); // cancel이 발화시킨 A의 완료 콜백
    vi.advanceTimersByTime(1000);
    expect(synth.spoken).toEqual(['A']); // B 재생 안 됨
    expect(onEnd).not.toHaveBeenCalled();
  });

  it('stop은 pause 대기 타이머도 취소한다', () => {
    const synth = createFakeSynth();
    const controller = new SpeechSequenceController(synth.speakLine, synth.cancel, 450);

    controller.play(['A', 'B'], vi.fn());
    synth.finish(); // pause 대기 중
    controller.stop();
    vi.advanceTimersByTime(1000);
    expect(synth.spoken).toEqual(['A']);
  });

  it('재생 중 play 재호출(더블탭)은 이전 시퀀스를 무효화하고 처음부터', () => {
    const synth = createFakeSynth();
    const controller = new SpeechSequenceController(synth.speakLine, synth.cancel, 450);
    const firstEnd = vi.fn();
    const secondEnd = vi.fn();

    controller.play(['A', 'B'], firstEnd);
    controller.play(['A', 'B'], secondEnd);
    expect(synth.spoken).toEqual(['A', 'A']);

    synth.finish(); // 1번째 시퀀스 A의 콜백 → 무효화됐으므로 무시
    vi.advanceTimersByTime(1000);
    expect(synth.spoken).toEqual(['A', 'A']);

    synth.finish(); // 2번째 시퀀스 A 완료
    vi.advanceTimersByTime(450);
    expect(synth.spoken).toEqual(['A', 'A', 'B']);
    synth.finish();
    expect(firstEnd).not.toHaveBeenCalled();
    expect(secondEnd).toHaveBeenCalledTimes(1);
  });

  it('빈 배열은 즉시 onEnd', () => {
    const synth = createFakeSynth();
    const controller = new SpeechSequenceController(synth.speakLine, synth.cancel);
    const onEnd = vi.fn();
    controller.play([], onEnd);
    expect(onEnd).toHaveBeenCalledTimes(1);
    expect(synth.spoken).toEqual([]);
  });
});
