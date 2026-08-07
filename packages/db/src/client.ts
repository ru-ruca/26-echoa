/**
 * DB 클라이언트 — 개발 docker / 프로덕션 Neon 드라이버 분기.
 *
 * legacy `web/src/db/index.ts`는 모듈 로드 시점에 `DATABASE_URL`이 없으면 throw 했다.
 * 그래서 테스트가 이 모듈을 통째로 mock 해야 했고 결국 로직 테스트를 못 썼다.
 * 여기서는 **첫 쿼리 시점까지 연결을 미룬다** — import 만으로는 아무 일도 일어나지 않는다.
 *
 * 드라이버 선택:
 *  - 개발(로컬 docker `local-pgvector-18`) → `postgres.js` (TCP)
 *  - 프로덕션(Neon) → `neon-serverless` (WebSocket).
 *    HTTP 드라이버(`neon-http`)는 다중 statement 트랜잭션을 지원하지 않는데,
 *    XP 지급·스트릭 갱신이 한 트랜잭션이어야 해서 WebSocket 쪽을 쓴다.
 */

import { drizzle as drizzleNeon } from 'drizzle-orm/neon-serverless';
import { drizzle as drizzlePg, type PostgresJsDatabase } from 'drizzle-orm/postgres-js';
import { Pool, neonConfig } from '@neondatabase/serverless';
import postgres from 'postgres';

export type DbSchema = Record<string, unknown>;

/**
 * 두 드라이버의 공통 타입.
 *
 * 유니온(`PostgresJsDatabase | NeonDatabase`)으로 두면 TS가 호출 시그니처를 교집합으로
 * 좁히면서 `.returning(fields)` 같은 오버로드가 사라진다. 쿼리 빌더 API는 양쪽이 동일하고
 * 다른 건 세션·드라이버 내부뿐이라, 하나로 통일해 선언한다.
 */
export type EchoaDatabase<TSchema extends DbSchema> = PostgresJsDatabase<TSchema>;

function requireDatabaseUrl(): string {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      'DATABASE_URL 이 없습니다. 개발은 .env 에 로컬 docker(echoa_db) URL 을 넣으세요 — ' +
        'postgresql://user1:userpw!!@localhost:5432/echoa_db',
    );
  }
  return url;
}

function isNeon(url: string): boolean {
  return url.includes('neon.tech');
}

/** 드라이버를 골라 drizzle 인스턴스를 만든다. */
function connect<TSchema extends DbSchema>(schema: TSchema, url: string): EchoaDatabase<TSchema> {
  if (isNeon(url)) {
    // Node 22+ 는 전역 WebSocket 을 제공한다. 없는 런타임이면 여기서 주입해야 한다.
    if (typeof WebSocket !== 'undefined') {
      neonConfig.webSocketConstructor = WebSocket;
    }
    return drizzleNeon({
      client: new Pool({ connectionString: url }),
      schema,
    }) as unknown as EchoaDatabase<TSchema>;
  }

  const client = postgres(url, {
    max: process.env.NODE_ENV === 'production' ? 10 : 5,
    // 로컬 docker 는 TLS 를 쓰지 않는다
    ssl: url.includes('sslmode=require') ? 'require' : false,
  });
  return drizzlePg({ client, schema });
}

/**
 * 지연 초기화 클라이언트.
 *
 * 반환된 객체의 프로퍼티에 처음 접근할 때 연결이 만들어진다.
 * Next.js dev 의 HMR 에서 커넥션이 새지 않도록 globalThis 에 캐시한다.
 */
export function createLazyDb<TSchema extends DbSchema>(
  schema: TSchema,
  cacheKey: string,
): EchoaDatabase<TSchema> {
  type Client = EchoaDatabase<TSchema>;
  const globalCache = globalThis as unknown as Record<string, Client | undefined>;

  let instance: Client | undefined;
  const resolve = (): Client => {
    instance ??= globalCache[cacheKey];
    if (!instance) {
      instance = connect(schema, requireDatabaseUrl());
      if (process.env.NODE_ENV !== 'production') globalCache[cacheKey] = instance;
    }
    return instance;
  };

  return new Proxy({} as Client, {
    get(_target, prop, receiver) {
      return Reflect.get(resolve() as object, prop, receiver);
    },
    has(_target, prop) {
      return Reflect.has(resolve() as object, prop);
    },
  });
}
