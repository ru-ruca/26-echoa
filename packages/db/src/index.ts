/**
 * @echoa/db — 공개 진입점.
 *
 * 여기서 얻는 `db`는 **공개 스키마만** 알고 있다. `content_originals`는 이 클라이언트의
 * 스키마에 없으므로 `db.query.contentOriginals`가 존재하지 않고, 테이블 객체도
 * 여기서는 import 할 수 없다 (ADR-010 §3 — 쿼리 레이어에서 원천 차단).
 *
 * 원문이 필요한 admin 코드만 `@echoa/db/admin`을 쓴다.
 */

import { createLazyDb } from './client';
import * as publicSchema from './schema/public';

export const db = createLazyDb(publicSchema, '__echoa_db_public__');

export * from './schema/public';
export type { DbSchema } from './client';
