/**
 * @echoa/db/admin — 저작권 원문(`content_originals`)에 닿는 유일한 경로.
 *
 * ⚠️ 이 모듈을 import 하는 코드는 반드시 admin 인증 뒤에 있어야 한다 (ADR-010 §3).
 * 앱 코드·공개 API 라우터에서는 import 하지 않는다. 적재(seed)와 admin 조회만 쓴다.
 */

import { createLazyDb } from './client';
import * as allSchema from './schema/all';

export const adminDb = createLazyDb(allSchema, '__echoa_db_admin__');

export * from './schema/all';
