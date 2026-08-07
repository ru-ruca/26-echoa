import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));

/** 26-echoa 저장소 루트 (packages/db/src/seed → ../../../..) */
export const REPO_ROOT = resolve(here, '../../../..');

/**
 * 콘텐츠 파이프라인 산출물.
 *
 * 파이프라인(Python/uv)은 생성·검수 도구이고, 적재는 앱 자산이라 여기(packages/db)에 둔다 (21 §9).
 */
export const PIPELINE_OUTPUT = resolve(REPO_ROOT, 'tools/content-pipeline/output');

export const CONTENT_FILES = {
  /** C-1 파일럿 27건 (M01~03) — 기존 문장 UPDATE 대상 */
  c1Pilot: resolve(PIPELINE_OUTPUT, 'c1_final.jsonl'),
  /** C-1 확대 419건 (M04~48) — 기존 문장 UPDATE 대상 */
  c1Full: resolve(PIPELINE_OUTPUT, 'c1_full_final.jsonl'),
  /** C-2 패턴 문장 528건 — 23 §9 미결정으로 적재 보류 */
  c2: resolve(PIPELINE_OUTPUT, 'c2_final.jsonl'),
  /**
   * C-3 대화 148행 — sentences 컬럼과 1:1.
   * `c3_rows_preview.jsonl` 은 이 파일과 바이트 동일한 검증 산출물이니 쓰지 않는다.
   */
  c3Rows: resolve(PIPELINE_OUTPUT, 'c3_rows_final.jsonl'),
} as const;
