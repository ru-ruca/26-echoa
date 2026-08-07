/**
 * 콘텐츠 적재 엔트리포인트.
 *
 * 파이프라인(`tools/content-pipeline/`, Python)은 **생성·검수 도구**이고,
 * 적재는 **앱 자산**이라 여기 `packages/db`에 둔다 (21 §9).
 *
 * 적재 순서 제약: **C-1 → C-2 → C-3**
 * (C-2 씨앗 25개가 C-1 재작성 텍스트를 패턴 고정부로 쓴다.)
 *
 * 현재 실행 가능한 것:
 *   pnpm -F @echoa/db seed:c3   # C-3 대화 148행
 *
 * 아직 막힌 것:
 *   C-1 446건 — 원문(content_originals)이 legacy DB에만 있어 접속이 필요하다
 *   C-2 528건 — 학습 흐름 소비 방식이 23 §9 미결정 + id 발번 규칙 없음
 */

import { loadC1Rewrites } from './c1-rewrites';
import { seedC3Dialogues } from './c3-dialogues';

type Task = 'c3' | 'c1-dry-run';

const TASKS: Record<Task, () => Promise<void>> = {
  async c3() {
    const { read, inserted } = await seedC3Dialogues();
    console.log(`[seed:c3] ${read}행 읽음 → ${inserted}행 적재 (content_origin='ai_generated')`);
    if (read !== inserted) {
      throw new Error(`적재 수가 맞지 않습니다: 읽음 ${read} / 적재 ${inserted}`);
    }
  },

  /** DB를 건드리지 않고 두 파일의 정규화가 되는지만 확인한다 */
  async 'c1-dry-run'() {
    const rows = await loadC1Rewrites();
    const withCoords = rows.filter((r) => r.month !== null).length;
    console.log(
      `[seed:c1 dry-run] ${rows.length}건 정규화 완료 ` +
        `(좌표 보유 ${withCoords} / legacy 조인 필요 ${rows.length - withCoords})`,
    );
    console.log('  실제 적재는 legacy DB 접속(원문 격리)이 준비된 뒤에 한다.');
  },
};

async function main() {
  const requested = (process.argv[2] ?? 'c3') as Task;
  const task = TASKS[requested];

  if (!task) {
    console.error(`알 수 없는 작업: ${requested}. 가능한 값: ${Object.keys(TASKS).join(', ')}`);
    process.exit(1);
  }

  await task();
}

main()
  .then(() => process.exit(0))
  .catch((error: unknown) => {
    console.error(error);
    process.exit(1);
  });
