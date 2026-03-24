"""봇 사용 로그 기록 모듈 (BigQuery)"""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv(Path(__file__).parent / ".env", override=True)

logger = logging.getLogger(__name__)

PROJECT_ID  = os.environ["GCP_PROJECT_ID"]
DATASET_ID  = os.environ.get("BQ_DATASET_ID", "siti_bot")
TABLE_ID    = os.environ.get("BQ_TABLE_ID",   "bot_usage_log")

SCHEMA = [
    bigquery.SchemaField("created_at",   "TIMESTAMP"),
    bigquery.SchemaField("user_id",      "STRING"),
    bigquery.SchemaField("channel",      "STRING"),
    bigquery.SchemaField("channel_type", "STRING"),   # 'dm' | 'channel'
    bigquery.SchemaField("question",     "STRING"),
    bigquery.SchemaField("answer",       "STRING"),
    bigquery.SchemaField("duration_ms",  "INTEGER"),
]


def _get_client() -> bigquery.Client:
    """GOOGLE_APPLICATION_CREDENTIALS 환경변수 또는 기본 인증으로 클라이언트 생성"""
    return bigquery.Client(project=PROJECT_ID)


def _ensure_table(client: bigquery.Client):
    """데이터셋·테이블이 없으면 자동 생성"""
    dataset_ref = client.dataset(DATASET_ID)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "asia-northeast3"   # 서울 리전
        client.create_dataset(dataset)
        logger.info("BigQuery 데이터셋 생성: %s", DATASET_ID)

    table_ref = dataset_ref.table(TABLE_ID)
    try:
        client.get_table(table_ref)
    except Exception:
        table = bigquery.Table(table_ref, schema=SCHEMA)
        client.create_table(table)
        logger.info("BigQuery 테이블 생성: %s.%s", DATASET_ID, TABLE_ID)


def log_usage(
    user_id: str,
    channel: str,
    channel_type: str,   # 'dm' | 'channel'
    question: str,
    answer: str,
    duration_ms: int,
):
    """사용 로그를 BigQuery에 스트리밍 삽입"""
    try:
        client = _get_client()
        _ensure_table(client)

        full_table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
        rows = [{
            "created_at":   datetime.now(timezone.utc).isoformat(),
            "user_id":      user_id,
            "channel":      channel,
            "channel_type": channel_type,
            "question":     question,
            "answer":       answer,
            "duration_ms":  duration_ms,
        }]

        errors = client.insert_rows_json(full_table_id, rows)
        if errors:
            logger.warning("BigQuery 삽입 오류: %s", errors)

    except Exception as e:
        # 로그 저장 실패해도 봇 응답에는 영향 없도록 경고만 출력
        logger.warning("사용 로그 저장 실패: %s", e)
