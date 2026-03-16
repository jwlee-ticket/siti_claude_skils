"""시티 DB 읽기 전용 조회 모듈"""

import json
import os
import re

import psycopg2
import psycopg2.extras

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE|REPLACE|MERGE|UPSERT"
    r"|EXEC|EXECUTE|CALL|DO|COPY|VACUUM|ANALYZE|REINDEX|CLUSTER|COMMENT|LOCK|NOTIFY|LISTEN"
    r"|SET|RESET|SAVEPOINT|RELEASE|ROLLBACK|COMMIT|BEGIN)\b",
    re.IGNORECASE,
)


def assert_read_only(sql: str):
    stripped = sql.strip()
    # SQL 주석 제거 후 검사 (-- 한줄 주석, /* */ 블록 주석)
    stripped_no_comment = re.sub(r"--[^\n]*", "", stripped)
    stripped_no_comment = re.sub(r"/\*.*?\*/", "", stripped_no_comment, flags=re.DOTALL)
    stripped_no_comment = stripped_no_comment.strip()
    if not re.match(r"^\s*(WITH\b[\s\S]+?SELECT\b|SELECT\b)", stripped_no_comment, re.IGNORECASE):
        raise ValueError("SELECT (또는 WITH ... SELECT) 쿼리만 허용됩니다.")

    match = FORBIDDEN_KEYWORDS.search(stripped)
    if match:
        raise ValueError(f"'{match.group()}' 은(는) 허용되지 않습니다. SELECT만 사용 가능합니다.")

    if ";" in stripped.rstrip(";"):
        raise ValueError("다중 쿼리는 허용되지 않습니다.")


def get_connection():
    return psycopg2.connect(
        host=os.environ["SITI_DB_HOST"],
        port=int(os.environ["SITI_DB_PORT"]),
        user=os.environ["SITI_DB_USER"],
        password=os.environ["SITI_DB_PASSWORD"],
        dbname=os.environ["SITI_DB_NAME"],
        options="-c default_transaction_read_only=on",
        connect_timeout=10,
    )


def run_query(sql: str, limit: int = 100) -> dict:
    """SQL 실행 후 결과를 dict로 반환"""
    assert_read_only(sql)

    if not re.search(r"\bLIMIT\b", sql, re.IGNORECASE):
        sql = sql.rstrip(";") + f" LIMIT {limit}"

    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        return {"success": False, "error": str(e), "rows": [], "count": 0}
    finally:
        conn.rollback()
        conn.close()


def format_table(rows: list) -> str:
    """결과를 Slack 코드블록용 텍스트 테이블로 변환"""
    if not rows:
        return "결과 없음"

    headers = list(rows[0].keys())
    col_widths = {
        h: max(len(h), max(len(str(r.get(h, ""))) for r in rows))
        for h in headers
    }
    col_widths = {h: min(w, 30) for h, w in col_widths.items()}

    lines = []
    lines.append(" | ".join(h.ljust(col_widths[h]) for h in headers))
    lines.append("-+-".join("-" * col_widths[h] for h in headers))
    for row in rows:
        lines.append(" | ".join(str(row.get(h, "")).ljust(col_widths[h])[:col_widths[h]] for h in headers))
    lines.append(f"\n총 {len(rows)}행")
    return "\n".join(lines)
