# Echoa

매일 한 문장으로 영어를 익히는 학습 앱. 일상 소통 중심으로 **듣고, 따라 말하고, 대화로 굳힌다**.

구 SenTalk(Next.js PWA)을 학습설계·콘텐츠·구조까지 재구성한 프로젝트다.

## 구조

```
apps/web/        Next.js 16.3 — 공개 웹
packages/core/   순수 TS 학습 로직 (FSRS·게이미피케이션·대화·복습)
packages/db/     Drizzle 스키마 + 콘텐츠 적재
packages/api/    tRPC v11 라우터
tooling/         tsconfig · eslint · prettier
docs/            기획·설계·조사 (SSOT)
tools/           콘텐츠 생성 파이프라인 (Python)
```

## 시작하기

```bash
# 개발 DB (공용 PG18 컨테이너)
cd ../../dev-env/common-docker && docker compose up -d

# 의존성 · 환경변수
pnpm install
cp packages/db/.env.example packages/db/.env
cp apps/web/.env.example apps/web/.env

# 스키마 적용 + 콘텐츠 적재
pnpm db:push
pnpm -F @echoa/db seed:c3

pnpm dev          # http://localhost:3000
```

검증: `pnpm typecheck` · `pnpm lint` · `pnpm test` · `pnpm build` · `pnpm format`

## 문서

- 프로젝트 지침·현황: [CLAUDE.md](CLAUDE.md)
- 재구성 계획(SSOT): [docs/project-review/21_rebuild-plan.md](docs/project-review/21_rebuild-plan.md)
- 결정 기록: [docs/adr/](docs/adr/)
- 문서 전체 안내: [docs/README.md](docs/README.md)
