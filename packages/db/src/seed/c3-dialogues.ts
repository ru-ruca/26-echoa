/**
 * C-3 대화 적재 — 148행 (대화 37개 × 4턴).
 *
 * 파이프라인 산출물 중 유일하게 **지금 바로 적재 가능**한 것이다:
 *  - `c3_rows_final.jsonl` 의 14개 키가 `sentences` 컬럼과 1:1 대응한다
 *  - 신규 INSERT 라 legacy DB 접속이 필요 없다
 *  - 대화 번호 101~ 로 발번돼 기존 001·002 와 충돌하지 않는다
 *
 * 다만 레코드에 `content_origin` 이 없다 — ADR-010 §2가 모든 공개 문장에 필수로 요구하므로
 * 적재 시 `ai_generated` 를 주입한다.
 */

import { sql } from 'drizzle-orm';

import { adminDb, sentences, type NewSentence } from '../admin';
import { chunk, readJsonlAll } from './jsonl';
import { CONTENT_FILES } from './paths';

/** c3_rows_final.jsonl 한 행 */
interface C3Row {
  id: string;
  month: number;
  week: number;
  day: number;
  day_type: string;
  text_en: string;
  text_kr: string;
  cefr_level: string;
  dialogue_id: string;
  speaker: string;
  dialogue_title: string;
  dialogue_situation: string;
  notes: string;
  is_new: boolean;
}

function toSentence(row: C3Row): NewSentence {
  return {
    id: row.id,
    month: row.month,
    week: row.week,
    day: row.day,
    dayType: row.day_type,
    textEn: row.text_en,
    textKr: row.text_kr,
    cefrLevel: row.cefr_level,
    // 산출물에 없는 필드 — ADR-010 §2가 공개 문장에 필수로 요구한다
    contentOrigin: 'ai_generated',
    dialogueId: row.dialogue_id,
    speaker: row.speaker,
    dialogueTitle: row.dialogue_title,
    dialogueSituation: row.dialogue_situation,
    notes: row.notes,
    isNew: row.is_new,
  };
}

export async function seedC3Dialogues(): Promise<{ read: number; inserted: number }> {
  const rows = await readJsonlAll<C3Row>(CONTENT_FILES.c3Rows);
  const values = rows.map(toSentence);

  let inserted = 0;
  for (const batch of chunk(values, 100)) {
    // 재실행해도 결과가 같도록 — 이미 있는 id 는 본문만 갱신한다
    const result = await adminDb
      .insert(sentences)
      .values(batch)
      .onConflictDoUpdate({
        target: sentences.id,
        set: {
          textEn: sql`excluded.text_en`,
          textKr: sql`excluded.text_kr`,
          contentOrigin: sql`excluded.content_origin`,
          speaker: sql`excluded.speaker`,
          dialogueTitle: sql`excluded.dialogue_title`,
          dialogueSituation: sql`excluded.dialogue_situation`,
          notes: sql`excluded.notes`,
          updatedAt: new Date(),
        },
      })
      .returning({ id: sentences.id });
    inserted += result.length;
  }

  return { read: rows.length, inserted };
}
