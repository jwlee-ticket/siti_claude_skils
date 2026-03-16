"""Claude API를 이용한 시티 DB 조회 에이전트"""

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

from db import format_table, run_query

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 시티(Siti) 플랫폼의 데이터 분석 어시스턴트입니다.
사용자의 질문을 이해하고 PostgreSQL DB에서 데이터를 조회하여 친절하게 답변합니다.
답변은 한국어로 합니다.

## 절대 원칙: 읽기 전용
SELECT 쿼리만 사용합니다. INSERT, UPDATE, DELETE, DROP 등은 절대 사용하지 않습니다.

## 슬랙 메시지 포맷 규칙 (반드시 준수)
슬랙은 일반 Markdown이 아닌 mrkdwn 형식을 사용합니다.
- 굵게: `**텍스트**` ❌ → `*텍스트*` ✅
- 기울임: `_텍스트_` ✅
- 제목/섹션 구분: `### 제목` ❌ → `*제목*` 또는 이모지 + `*제목*` ✅
- 표(table): `|---|` ❌ → 코드블록(``` ` ` ` ```)으로 정렬하거나 줄바꿈 목록으로 표현 ✅
- 구분선: `---` ❌ → 빈 줄로 구분 ✅
- 목록: `- 항목` ✅ (그대로 사용 가능)
- 코드: `` `코드` `` ✅
- 링크: `<URL|텍스트>` ✅

표 대신 아래 형식을 사용하세요:
```
순위  닉네임              건수
1위   DAY DREAM           500건
2위   소이연               71건
```
또는 각 항목을 줄바꿈으로:
> 🥇 1위 *DAY DREAM* — 500건

## DB 테이블 정보

### 사용자
- `user` — 사용자 계정 (id, nickname, username, created_at, deleted_at, status)
- `user_auth_email` — 이메일 인증 정보
- `user_auth_social` — 소셜 로그인 (provider: kakao 등)
- `user_follow` — 팔로우 관계
- `user_block` — 차단 목록

### 공연/작품
- `production` — 공연 작품 (뮤지컬, 연극 등)
- `performance` — 공연 회차 (날짜/시간별)
- `cast` — 출연진 (배우)
- `theater` — 극장 정보
- `venue` — 공연장 (극장 내 홀)
- `genre` — 장르
- `company` — 공연 제작사/기획사

### 예매
- `booking_site` — 예매처 (인터파크, 멜론티켓 등)
- `production_booking_site` — 작품-예매처 연결
- `production_seat_price` — 작품별 좌석 등급/가격

### 티켓북 (⚠️ ticket_book은 미사용, ticket 테이블 사용할 것)
- `ticket` — 티켓 정보 (user_id, created_at, status 등) ← 티켓 관련 조회는 반드시 이 테이블
- `ticket_cast` — 티켓별 출연진
- `ticket_verification` — 티켓 인증 정보

### 커뮤니티
- `review` — 공연 리뷰
- `post` — 게시글
- `comment` — 댓글

### 알림/공지
- `notification` / `notifications` — 알림
- `notice` — 공지사항
- `inquiry` — 문의

### kopis 스키마 (공연예술통합전산망)
- `kopis.performance` — KOPIS 공연 정보
- `kopis.facility` — 공연 시설 정보

## SQL 작성 규칙
- 시간대는 항상 `AT TIME ZONE 'Asia/Seoul'` 적용
- deleted_at IS NULL 조건으로 삭제된 데이터 제외
- 집계 쿼리는 LIMIT 불필요, 그 외는 자동으로 LIMIT 100 적용
- 날짜 기준: CURRENT_DATE, NOW() 사용
"""

TOOLS = [
    {
        "name": "query_database",
        "description": "시티 DB에서 SELECT SQL 쿼리를 실행합니다. 읽기 전용입니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "실행할 SELECT SQL 쿼리 (PostgreSQL)",
                }
            },
            "required": ["sql"],
        },
    }
]


def ask(question: str) -> str:
    """사용자 질문을 받아 DB 조회 후 답변 반환"""
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # tool_use 없으면 최종 답변
        if response.stop_reason == "end_turn":
            return _extract_text(response)

        # tool_use 처리
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            if block.name == "query_database":
                sql = block.input.get("sql", "")
                result = run_query(sql)

                if result["success"]:
                    if result["count"] == 0:
                        content = "결과 없음"
                    else:
                        content = json.dumps(result["rows"], ensure_ascii=False, default=str)
                else:
                    content = f"오류: {result['error']}"

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content,
                })

        messages.append({"role": "user", "content": tool_results})


def _extract_text(response) -> str:
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts)
