/**
 * 여러 줄 TTS 순차 재생 컨트롤러 (미니대화)
 *
 * TTS 구현에 직접 의존하지 않고 speakLine/cancel을 주입받는다 — 순서·중단·줄 간
 * 쉼만 책임진다. 덕분에 웹(Web Speech API)·앱(expo-speech / Capacitor TTS) 어디에
 * 붙여도 이 파일은 그대로다. vitest node 환경에서 fake로 테스트도 된다.
 *
 * 세대 토큰이 필수인 이유: speechSynthesis.cancel() 시 Chrome은
 * onerror('interrupted'), Safari는 onend를 발화한다. 토큰 없이 완료 콜백을
 * 믿으면 stop 직후 다음 줄이 재생된다.
 */

/** 한 줄 재생. 완료·실패 어느 쪽이든 반드시 onFinished를 1회 호출해야 한다. */
export type SpeakLineFn = (text: string, onFinished: () => void) => void;

/** 줄 사이 쉼 (ms) — speaker 교대가 들리도록 짧게 */
const DEFAULT_LINE_PAUSE_MS = 450;

export class SpeechSequenceController {
  private generation = 0;
  private timer: ReturnType<typeof setTimeout> | null = null;

  constructor(
    private readonly speakLine: SpeakLineFn,
    private readonly cancelSynth: () => void,
    private readonly pauseMs: number = DEFAULT_LINE_PAUSE_MS,
  ) {}

  /** 진행 중 시퀀스를 무효화하고 texts를 처음부터 재생. 끝나면 onEnd 1회 호출. */
  play(texts: string[], onEnd: () => void): void {
    this.stop();
    const gen = this.generation;

    if (texts.length === 0) {
      onEnd();
      return;
    }

    const playFrom = (index: number) => {
      if (gen !== this.generation) return;
      const text = texts[index];
      if (text === undefined) return;

      this.speakLine(text, () => {
        if (gen !== this.generation) return;
        if (index + 1 >= texts.length) {
          onEnd();
          return;
        }
        this.timer = setTimeout(() => {
          this.timer = null;
          playFrom(index + 1);
        }, this.pauseMs);
      });
    };

    playFrom(0);
  }

  /** 시퀀스 중단: 이후 도착하는 완료 콜백·대기 타이머를 모두 무효화. */
  stop(): void {
    this.generation++;
    if (this.timer !== null) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    this.cancelSynth();
  }
}
