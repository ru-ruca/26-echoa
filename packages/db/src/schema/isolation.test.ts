/**
 * ADR-010 §3 원문 격리 경계 테스트.
 *
 * "공개 API·앱에서 `content_originals` 절대 미노출 — 쿼리 레이어에서 원천 차단"이
 * 주석이 아니라 실제로 성립하는지 확인한다. 누군가 `public.ts`에 `restricted`를
 * 실수로 re-export 하면 여기서 깨진다.
 */

import { describe, expect, it } from 'vitest';

import * as adminSchema from './all';
import * as publicSchema from './public';
import * as restricted from './restricted';

const RESTRICTED_EXPORTS = ['contentOriginals', 'contentOriginalsRelations'] as const;

describe('공개 배럴 (schema/public)', () => {
  it('저작권 원문 테이블을 노출하지 않는다', () => {
    for (const name of RESTRICTED_EXPORTS) {
      expect(publicSchema).not.toHaveProperty(name);
    }
  });

  it('학습에 필요한 공개 테이블은 전부 노출한다', () => {
    for (const name of [
      'sentences',
      'vocabulary',
      'collocations',
      'sentenceWords',
      'sources',
      'users',
      'userProgress',
      'userStreaks',
      'userXp',
      'badges',
    ]) {
      expect(publicSchema).toHaveProperty(name);
    }
  });
});

describe('admin 배럴 (schema/all)', () => {
  it('원문 테이블에 닿는 유일한 경로다', () => {
    for (const name of RESTRICTED_EXPORTS) {
      expect(adminSchema).toHaveProperty(name);
    }
  });

  it('공개 배럴의 모든 export 를 포함한다', () => {
    for (const name of Object.keys(publicSchema)) {
      expect(adminSchema).toHaveProperty(name);
    }
  });
});

describe('content_originals 컬럼', () => {
  it('원문 verbatim 과 출처 추적 컬럼을 갖는다', () => {
    const columns = Object.keys(restricted.contentOriginals);
    for (const name of ['sentenceId', 'originalTextEn', 'sourceId', 'rewriteMeta']) {
      expect(columns).toContain(name);
    }
  });
});

describe('content_origin enum (ADR-010 §2)', () => {
  it('네 값을 정확히 갖는다', () => {
    expect([...publicSchema.contentOriginEnum.enumValues].sort()).toEqual([
      'ai_generated',
      'ai_rewritten',
      'public_domain',
      'self_authored',
    ]);
  });

  it('sentences.content_origin 은 NOT NULL 이다 — 감사 가능하도록 모든 공개 문장에 필수', () => {
    expect(publicSchema.sentences.contentOrigin.notNull).toBe(true);
  });
});
