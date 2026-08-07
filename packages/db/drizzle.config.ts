import { defineConfig } from 'drizzle-kit';

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL 이 없습니다 (packages/db/.env 를 확인하세요)');
}

export default defineConfig({
  // 마이그레이션은 격리 테이블까지 포함한 전체 스키마 기준으로 생성한다.
  // 앱 코드가 쓰는 배럴은 schema/public.ts 로 따로 있다 (ADR-010 §3).
  schema: './src/schema/all.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: { url: process.env.DATABASE_URL },
  casing: 'snake_case',
});
