"""legacy SenTalk DB 읽기 전용 접속.

파이프라인은 legacy DB에 아무것도 쓰지 않는다 — readonly 세션으로 강제.
접속 정보: LEGACY_DATABASE_URL 환경변수 우선, 없으면 legacy repo의 .env.
"""
from __future__ import annotations

import os
from pathlib import Path

import psycopg2
from dotenv import dotenv_values
from psycopg2.extensions import connection as Connection

# tools/content-pipeline/src/db.py → my-project/ 까지 4단계 상위
LEGACY_ENV = (
    Path(__file__).resolve().parents[3].parent / "26-SenTalk-en-study-app" / ".env"
)


def resolve_url() -> str:
    url = os.getenv("LEGACY_DATABASE_URL")
    if not url and LEGACY_ENV.exists():
        url = dotenv_values(LEGACY_ENV).get("DATABASE_URL")
    if not url:
        raise SystemExit(
            "legacy DB 접속 정보 없음 — LEGACY_DATABASE_URL을 설정하거나 "
            f"{LEGACY_ENV} 에 DATABASE_URL이 있어야 한다."
        )
    return url


def connect_readonly() -> Connection:
    conn = psycopg2.connect(resolve_url())
    conn.set_session(readonly=True, autocommit=True)
    return conn
