#!/usr/bin/env python3
"""시티 DB 읽기 전용 조회 스크립트 — SELECT만 허용"""

import argparse
import json
import os
import re
import sys

import psycopg2
import psycopg2.extras


# ── 안전성 검사 ──────────────────────────────────────────────────────────────

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE|REPLACE|MERGE|UPSERT"
    r"|EXEC|EXECUTE|CALL|DO|COPY|VACUUM|ANALYZE|REINDEX|CLUSTER|COMMENT|LOCK|NOTIFY|LISTEN"
    r"|SET|RESET|SAVEPOINT|RELEASE|ROLLBACK|COMMIT|BEGIN)\b",
    re.IGNORECASE,
)


def assert_read_only(sql: str):
    """3중 안전 검사 — SELECT 외 모든 쿼리 차단"""
    # 1. SELECT로 시작하는지 확인
    stripped = sql.strip()
    if not re.match(r"^\s*(WITH\s+.+\s+)?SELECT\b", stripped, re.IGNORECASE | re.DOTALL):
        print("오류: SELECT (또는 WITH ... SELECT) 쿼리만 허용됩니다.", file=sys.stderr)
        sys.exit(1)

    # 2. 금지 키워드 포함 여부 확인
    match = FORBIDDEN_KEYWORDS.search(stripped)
    if match:
        print(
            f"오류: '{match.group()}' 은(는) 허용되지 않습니다. SELECT만 사용 가능합니다.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 3. 세미콜론으로 여러 쿼리 연결 시도 차단
    if ";" in stripped.rstrip(";"):
        print("오류: 다중 쿼리는 허용되지 않습니다.", file=sys.stderr)
        sys.exit(1)


# ── DB 연결 ──────────────────────────────────────────────────────────────────

def get_connection():
    required = ["SITI_DB_HOST", "SITI_DB_PORT", "SITI_DB_USER", "SITI_DB_PASSWORD", "SITI_DB_NAME"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"오류: 환경 변수 없음 — {', '.join(missing)}\nreferences/setup.md 참고", file=sys.stderr)
        sys.exit(1)

    return psycopg2.connect(
        host=os.environ["SITI_DB_HOST"],
        port=int(os.environ["SITI_DB_PORT"]),
        user=os.environ["SITI_DB_USER"],
        password=os.environ["SITI_DB_PASSWORD"],
        dbname=os.environ["SITI_DB_NAME"],
        options="-c default_transaction_read_only=on",  # DB 레벨 읽기 전용 강제
        connect_timeout=10,
    )


# ── 실행 ─────────────────────────────────────────────────────────────────────

def run_query(sql: str, limit: int = 100, output_format: str = "table"):
    assert_read_only(sql)

    # LIMIT 없는 쿼리에 자동으로 LIMIT 추가
    if not re.search(r"\bLIMIT\b", sql, re.IGNORECASE):
        sql = sql.rstrip(";") + f" LIMIT {limit}"

    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        rows = [dict(r) for r in rows]

        if not rows:
            print("결과 없음")
            return

        if output_format == "json":
            print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
        else:
            # 테이블 형식 출력
            headers = list(rows[0].keys())
            col_widths = {h: max(len(h), max(len(str(r.get(h, ""))) for r in rows)) for h in headers}
            col_widths = {h: min(w, 40) for h, w in col_widths.items()}  # 최대 40자

            header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
            sep_line = "-+-".join("-" * col_widths[h] for h in headers)
            print(header_line)
            print(sep_line)
            for row in rows:
                print(" | ".join(str(row.get(h, "")).ljust(col_widths[h])[:col_widths[h]] for h in headers))

            print(f"\n{len(rows)}행")
    finally:
        conn.rollback()  # 3중 보호: 어떠한 경우에도 변경사항 롤백
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="시티 DB 읽기 전용 조회")
    parser.add_argument("sql", help="실행할 SELECT 쿼리")
    parser.add_argument("--limit", type=int, default=100, help="최대 행 수 (기본값: 100)")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="출력 형식")
    args = parser.parse_args()

    run_query(args.sql, limit=args.limit, output_format=args.format)


if __name__ == "__main__":
    main()
