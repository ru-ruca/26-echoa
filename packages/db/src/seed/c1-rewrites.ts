/**
 * C-1 재작성 적재 — 446건 (파일럿 27 + 확대 419).
 *
 * ⚠️ **이번 단계에서는 실행하지 않는다.** 로더와 정규화만 준비한다.
 *
 * C-1은 INSERT가 아니라 **UPDATE 성격**이다. `seed_id`가 기존 `sentences.id`이고,
 * `text_en`·`text_kr`을 재작성본으로 교체하면서 `content_origin='ai_rewritten'`을 세운다.
 * 그리고 ADR-010 §2에 따라 **원문을 `content_originals`로 격리 보관**해야 하는데,
 * 산출물에는 원문이 없다 — legacy Neon DB(또는 gitignore된
 * `tools/content-pipeline/data/work/c1_full_seeds.jsonl`)에서 가져와야 한다.
 * 그래서 legacy DB 접속이 준비된 뒤에 실행한다.
 *
 * 두 파일은 **스키마가 다르다** — 하나의 로더로 읽으려면 정규화가 필요하다:
 *
 * | | c1_final (파일럿 27) | c1_full_final (확대 419) |
 * |---|---|---|
 * | `day_type`·`cefr_level`·`month` | 없음 (legacy 조인 필요) | 있음 |
 * | `source_cand` | `int \| "reviewer_alternative"` | `int` |
 * | 채택 경로 | `review.result` (`adopted`) | `review.source` (`judge_best`\|`human_review`) |
 * | 원문 유사도 | 없음 | `review.seed_sim` |
 * | 외부 교차검토 | `review.external` | 없음 |
 *
 * 적재 순서 제약: **C-1 → C-2 → C-3**.
 * C-2 씨앗 116개 중 25개가 C-1 재작성 텍스트를 패턴 고정부로 쓰기 때문에,
 * C-1을 먼저 적재해야 계보가 맞는다.
 */

import type { RewriteMeta } from '../schema/restricted';

/** c1_final.jsonl (파일럿 27) 한 행 */
interface C1PilotRow {
  seed_id: string;
  source_cand: number | string;
  text_en: string;
  text_kr: string;
  kept_function: string;
  content_origin: string;
  review: {
    result: string;
    modified: boolean;
    reason: string | null;
    judge_avg: number;
    reviewed_at: string;
    external?: Record<string, unknown>;
  };
  gen_meta: { prompt: string; date: string; adopted_at: string };
}

/** c1_full_final.jsonl (확대 419) 한 행 */
interface C1FullRow {
  seed_id: string;
  source_cand: number;
  day_type: string;
  cefr_level: string;
  month: number;
  text_en: string;
  text_kr: string;
  kept_function: string;
  content_origin: string;
  review: {
    source: string;
    modified: boolean;
    judge_avg: number;
    seed_sim: number;
    reviewed_at: string;
  };
  gen_meta: { prompt: string; date: string; adopted_at: string };
}

/** 두 파일을 합쳐 다루기 위한 공통 형태 */
export interface NormalizedC1Rewrite {
  /** 기존 sentences.id — UPDATE 키 */
  sentenceId: string;
  textEn: string;
  textKr: string;
  /** 원문에서 보존한 기능 설명 (한국어) */
  keptFunction: string;
  /** 파일럿은 legacy 조인으로 채워야 한다 */
  dayType: string | null;
  cefrLevel: string | null;
  month: number | null;
  /** content_originals.rewrite_meta 로 들어갈 감사 정보 */
  rewriteMeta: RewriteMeta;
}

export function normalizePilotRow(row: C1PilotRow): NormalizedC1Rewrite {
  return {
    sentenceId: row.seed_id,
    textEn: row.text_en,
    textKr: row.text_kr,
    keptFunction: row.kept_function,
    dayType: null,
    cefrLevel: null,
    month: null,
    rewriteMeta: {
      prompt: row.gen_meta.prompt,
      date: row.gen_meta.date,
      adoptedAt: row.gen_meta.adopted_at,
      // 파일럿은 source_cand 가 "reviewer_alternative" 일 수 있다
      source: typeof row.source_cand === 'string' ? row.source_cand : row.review.result,
      judgeAvg: row.review.judge_avg,
      modified: row.review.modified,
      external: row.review.external,
    },
  };
}

export function normalizeFullRow(row: C1FullRow): NormalizedC1Rewrite {
  return {
    sentenceId: row.seed_id,
    textEn: row.text_en,
    textKr: row.text_kr,
    keptFunction: row.kept_function,
    dayType: row.day_type,
    cefrLevel: row.cefr_level,
    month: row.month,
    rewriteMeta: {
      prompt: row.gen_meta.prompt,
      date: row.gen_meta.date,
      adoptedAt: row.gen_meta.adopted_at,
      source: row.review.source,
      judgeAvg: row.review.judge_avg,
      seedSim: row.review.seed_sim,
      modified: row.review.modified,
    },
  };
}

/**
 * 두 파일을 읽어 하나의 목록으로 정규화한다.
 * 원문(`content_originals.original_text_en`)은 여기서 채우지 않는다 — 별도 경로가 필요하다.
 */
export async function loadC1Rewrites(): Promise<NormalizedC1Rewrite[]> {
  const { readJsonlAll } = await import('./jsonl');
  const { CONTENT_FILES } = await import('./paths');

  const pilot = await readJsonlAll<C1PilotRow>(CONTENT_FILES.c1Pilot);
  const full = await readJsonlAll<C1FullRow>(CONTENT_FILES.c1Full);

  return [...pilot.map(normalizePilotRow), ...full.map(normalizeFullRow)];
}
