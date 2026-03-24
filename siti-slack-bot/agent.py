"""Claude API를 이용한 시티 DB 조회 에이전트"""

import json
import os
import subprocess
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

from db import format_table, run_query

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """당신은 시티(Siti) 플랫폼의 데이터 분석 어시스턴트입니다.
사용자의 질문을 이해하고 PostgreSQL DB와 마케팅 Google Sheets 데이터를 조회하여 친절하게 답변합니다.
답변은 한국어로 합니다.

## 절대 원칙: 읽기 전용
SELECT 쿼리만 사용합니다. INSERT, UPDATE, DELETE, DROP 등은 절대 사용하지 않습니다.

## 툴 사용 원칙 (반드시 준수)

이벤트 날짜, 마케팅 일정, 시티 셀렉션 정보가 필요한 경우 **반드시 `query_marketing_sheets`를 먼저 호출**한다.
절대로 이벤트 기간이나 마케팅 일정을 추정하거나 임의로 정의하지 않는다.

`query_marketing_sheets`를 반드시 써야 하는 경우:
- 시티 셀렉션 이벤트 날짜/기간이 필요할 때 → `초대권리스트` 조회
- 마케팅 전략 실행 시점이 필요할 때 → `일정` 조회
- 이벤트 기간과 DB 지표를 함께 분석할 때 → 먼저 `초대권리스트`로 날짜 확인 후 DB 조회
- "마케팅 효율", "이벤트 효과", "셀렉션 분석" 등의 질문 → 반드시 Sheets 데이터 기반으로 분석

예시:
- "시티 셀렉션 효과 분석해줘" → `초대권리스트` 조회 → 각 이벤트의 정확한 날짜 확인 → DB에서 해당 기간 지표 조회
- "3월 마케팅 어땠어?" → `일정` 조회 → DB 지표와 함께 분석

## 슬랙 메시지 포맷 규칙 (절대 준수 — 위반 금지)

슬랙은 일반 Markdown이 아니라 mrkdwn 형식을 사용합니다.

❌ 절대 사용 금지:
- `**굵게**` → 반드시 `*굵게*` 로 (별표 하나)
- `### 제목` / `## 제목` / `# 제목` → 반드시 `*제목*` 으로
- `| 컬럼 | 컬럼 |` 마크다운 표 → 절대 사용 금지
- `---` 구분선 → 절대 사용 금지

✅ 반드시 이렇게:
- 굵게: `*텍스트*` (별표 하나)
- 제목: `*제목*` 또는 이모지 + `*제목*`
- 표 데이터: 코드블록(```) 안에 정렬된 텍스트로 표현
- 순위/리스트: 이모지 + `*닉네임*` — 값 형식

표 예시 (반드시 이 형식):
```
날짜        가입자 수
----------  --------
2026-03-09  11명
2026-03-10  17명
```

순위 예시 (반드시 이 형식):
🥇 1위 *DAY DREAM* — 500건
🥈 2위 *소이연* — 71건
🥉 3위 *TU또하자* — 70건

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

## 마케팅 데이터 (Google Sheets)

`query_marketing_sheets` 툴로 시티 마케팅 전략 데이터를 조회할 수 있습니다.
시티 DB 데이터와 함께 사용하면 마케팅 효과 분석이 가능합니다.

### 시트 종류
- `초대권리스트` — 공연별 시티 셀렉션 이벤트 현황 (공연명, 이벤트 시작/종료일, 관람일, 좌석등급, 당첨인원, 티켓 수급 상황)
- `콘텐츠리스트` — SNS 콘텐츠 업로드 일정 (날짜, 채널, 전략 구분, 내용)
- `일정` — 2025-2026 전체 마케팅 플랜 (주차별 KPI, MAIN ISSUE, 채널별 콘텐츠, 프로모션/이벤트)

### 함께 사용하는 예시
- "시티 셀렉션 이벤트 목록 보여줘" → `초대권리스트` 조회
- "3월 마케팅 일정과 가입자 추이 같이 보여줘" → `일정` + DB 조회
- "셀렉션 #2 기간 동안 어떤 공연이 많이 등록됐어?" → `초대권리스트`로 날짜 확인 후 DB 조회
"""

GSHEETS_SCRIPT = Path(__file__).parent.parent / "siti-db" / "scripts" / "gsheets.py"

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
    },
    {
        "name": "query_marketing_sheets",
        "description": "시티 마케팅 Google Sheets 데이터를 조회합니다. 초대권리스트(시티 셀렉션 이벤트), 콘텐츠리스트(SNS 콘텐츠 일정), 일정(전체 마케팅 플랜)을 조회할 수 있습니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {
                    "type": "string",
                    "enum": ["초대권리스트", "콘텐츠리스트", "일정"],
                    "description": "조회할 시트명",
                },
                "filter": {
                    "type": "string",
                    "description": "행 필터링 키워드 (선택). 예: '완료', '3월', '셀렉션'",
                },
            },
            "required": ["sheet"],
        },
    },
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

            elif block.name == "query_marketing_sheets":
                sheet = block.input.get("sheet", "")
                filter_kw = block.input.get("filter", "")

                cmd = ["python3", str(GSHEETS_SCRIPT), sheet]
                if filter_kw:
                    cmd += ["--filter", filter_kw]

                try:
                    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
                    content = proc.stdout if proc.stdout else f"오류: {proc.stderr}"
                except subprocess.TimeoutExpired:
                    content = "오류: Google Sheets 조회 타임아웃"
                except Exception as e:
                    content = f"오류: {e}"

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
