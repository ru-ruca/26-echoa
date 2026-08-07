import { buildDialogueWindow } from '@echoa/core';

import { api } from '~/trpc/server';

/**
 * 스캐폴딩 점검 페이지.
 *
 * 여기서 증명하려는 것 세 가지 (21 §8 단계 1 검증 기준):
 *  1. 웹 → `@echoa/api`(tRPC) → `@echoa/db` → docker echoa_db 경로가 실제로 돈다
 *  2. `@echoa/core`의 순수 로직(`buildDialogueWindow`)을 웹이 그대로 쓴다
 *  3. seed 로 적재한 C-3 대화(148행)가 조회된다
 *
 * 학습 UI는 22번 spec 확정 + 디자인 시스템 뒤에 만든다 — 이 페이지는 그때 교체된다.
 */
export default async function Page() {
  const lines = await api.sentence.dialogue({ dialogueId: 'DLG_M01_101' });
  const window = buildDialogueWindow(lines, 1);
  const first = lines[0];

  return (
    <main className="mx-auto max-w-2xl px-6 py-16">
      <h1 className="text-2xl font-bold">Echoa</h1>
      <p className="mt-1 text-sm text-neutral-500">모노레포 스캐폴딩 점검</p>

      <section className="mt-10">
        <h2 className="text-sm font-semibold text-neutral-500">
          웹 → api(tRPC) → db(docker echoa_db)
        </h2>
        <p className="mt-2 text-sm">
          <code>sentence.dialogue</code> 가 <strong>{lines.length}행</strong> 반환 —{' '}
          {first?.dialogueTitle}
        </p>
        <p className="mt-1 text-sm text-neutral-500">{first?.dialogueSituation}</p>
      </section>

      <section className="mt-8">
        <h2 className="text-sm font-semibold text-neutral-500">
          @echoa/core — buildDialogueWindow(lines, 1)
        </h2>
        <ol className="mt-3 space-y-3">
          {window.map((line) => (
            <li key={line.id} className="rounded-lg border border-neutral-200 p-4">
              <div className="text-xs text-neutral-500">{line.speaker}</div>
              <div className="mt-1">{line.textEn}</div>
              <div className="mt-1 text-sm text-neutral-500">{line.textKr}</div>
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
