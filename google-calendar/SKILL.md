---
name: google-calendar
description: Google Calendar 일정을 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)하는 스킬. 사용자가 "캘린더에 일정 추가해줘", "회의 잡아줘", "미팅 수정해줘", "일정 삭제해줘", "이번 주 일정 알려줘", "구글 캘린더에서 ~~ 해줘" 처럼 말할 때 반드시 이 스킬을 사용해야 한다. 일정 관련 모든 요청에 적극적으로 트리거하라.
---

# Google Calendar 스킬

Google Calendar CRUD 작업을 수행하는 스킬.

## 지원 기능

| 기능 | 예시 표현 |
|------|----------|
| **Create** 일정 생성 | "내일 오후 2시에 팀 미팅 잡아줘" |
| **Read** 일정 조회 | "이번 주 일정 뭐 있어?", "오늘 미팅 알려줘" |
| **Update** 일정 수정 | "팀 미팅을 오후 3시로 바꿔줘" |
| **Delete** 일정 삭제 | "내일 미팅 취소해줘" |

---

## 사전 준비 확인

```bash
ls ~/.google_calendar_credentials/credentials.json
```

없으면 `references/setup_google.md` 참고.

---

## CRUD 작업

모든 작업은 `scripts/gcal.py`로 처리한다.

### Create — 일정 생성

```bash
python scripts/gcal.py create \
  --title "제목" \
  --start "2025-03-15T14:00:00" \
  --end "2025-03-15T15:00:00"
```

- 종료 시간 없으면 시작 + 1시간으로 자동 설정
- 날짜/시간은 ISO 8601 형식으로 변환해서 전달
- 성공 시 event ID와 링크 출력

### Read — 일정 조회

```bash
# 오늘 일정
python scripts/gcal.py list --date today

# 특정 날짜
python scripts/gcal.py list --date "2025-03-15"

# 기간 조회
python scripts/gcal.py list --start "2025-03-15" --end "2025-03-21"

# 키워드 검색
python scripts/gcal.py list --query "팀 미팅"
```

### Update — 일정 수정

수정 전에 먼저 `list`로 대상 이벤트의 ID를 찾는다.

```bash
# 이벤트 ID 찾기
python scripts/gcal.py list --query "팀 미팅"

# 수정 (변경할 항목만 지정)
python scripts/gcal.py update \
  --event-id "abc123" \
  --title "새 제목" \
  --start "2025-03-15T15:00:00" \
  --end "2025-03-15T16:00:00"
```

이벤트 ID가 불확실할 때: 사용자에게 후보 목록을 보여주고 확인 받는다.

### Delete — 일정 삭제

삭제는 되돌릴 수 없으므로 반드시 사용자에게 확인한다.

```bash
# 이벤트 ID 찾기
python scripts/gcal.py list --query "팀 미팅"

# 삭제
python scripts/gcal.py delete --event-id "abc123"
```

---

## 날짜/시간 파싱 가이드

| 표현 | 변환 기준 |
|------|----------|
| "오늘" | 현재 날짜 |
| "내일" | 현재 날짜 + 1일 |
| "다음주 월요일" | 다음 주 월요일 |
| "이번 주" | 이번 주 월~일 |
| "오후 N시" | N+12:00:00 (N < 12일 때) |
| "오전 N시" | N:00:00 |
| "N시 M분" | N:M:00 |

모호한 경우 사용자에게 확인한다. 예: "3일" → "이번 달 3일인가요, 3일 후인가요?"

---

## 오류 처리

| 오류 | 대처 |
|------|------|
| credentials.json 없음 | `references/setup_google.md` 안내 |
| token 만료 | token.json 삭제 후 재인증 안내 |
| 이벤트 못 찾음 | 다른 키워드로 재검색 제안 |
