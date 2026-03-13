#!/usr/bin/env python3
"""Google Calendar CRUD 스크립트"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_DIR = Path.home() / ".google_calendar_credentials"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"
TOKEN_FILE = CREDENTIALS_DIR / "token.json"
KST = timezone(timedelta(hours=9))
DEFAULT_CALENDAR = "c_fa2b82bc9501be6f9d1683690868af3411e942b142d349d9ab49d29ce643521f@group.calendar.google.com"


def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(
                    f"오류: {CREDENTIALS_FILE} 없음\n"
                    "references/setup_google.md를 참고해 설정하세요.",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json())

    return creds


def get_service():
    return build("calendar", "v3", credentials=get_credentials())


def format_datetime(dt_str: str) -> str:
    """ISO 8601 형식 보정 (시간대 없으면 KST 적용)"""
    if "+" not in dt_str and dt_str[-1] != "Z":
        dt_str += "+09:00"
    return dt_str


def format_event_display(event: dict) -> str:
    start = event["start"].get("dateTime", event["start"].get("date", ""))
    end = event["end"].get("dateTime", event["end"].get("date", ""))
    title = event.get("summary", "(제목 없음)")
    link = event.get("htmlLink", "")
    event_id = event.get("id", "")
    return f"  ID: {event_id}\n  제목: {title}\n  시작: {start}\n  종료: {end}\n  링크: {link}"


# ── CALENDARS ────────────────────────────────────────────────────────────────

def cmd_calendars(args):
    service = get_service()
    try:
        result = service.calendarList().list().execute()
        print("📅 캘린더 목록:")
        for cal in result.get("items", []):
            print(f"  이름: {cal['summary']}")
            print(f"  ID:   {cal['id']}")
            print()
    except HttpError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


# ── CREATE ──────────────────────────────────────────────────────────────────

def cmd_create(args):
    service = get_service()
    cal_id = args.calendar or DEFAULT_CALENDAR
    start = format_datetime(args.start)
    if args.end:
        end = format_datetime(args.end)
    else:
        # 종료 시간 미지정 시 1시간 후
        dt = datetime.fromisoformat(start)
        end = (dt + timedelta(hours=1)).isoformat()

    event = {
        "summary": args.title,
        "start": {"dateTime": start, "timeZone": "Asia/Seoul"},
        "end": {"dateTime": end, "timeZone": "Asia/Seoul"},
    }

    try:
        created = service.events().insert(calendarId=cal_id, body=event).execute()
        print("✅ 일정 생성 완료")
        print(format_event_display(created))
        # 후속 처리를 위해 JSON도 출력
        print("\n[JSON]")
        print(json.dumps({"id": created["id"], "link": created.get("htmlLink", ""), "title": created["summary"], "start": start, "end": end}, ensure_ascii=False))
    except HttpError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


# ── LIST ─────────────────────────────────────────────────────────────────────

def cmd_list(args):
    service = get_service()
    cal_id = args.calendar or DEFAULT_CALENDAR
    now = datetime.now(KST)

    if args.date == "today":
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = now.replace(hour=23, minute=59, second=59, microsecond=0)
    elif args.date:
        d = datetime.fromisoformat(args.date).replace(tzinfo=KST)
        time_min = d.replace(hour=0, minute=0, second=0)
        time_max = d.replace(hour=23, minute=59, second=59)
    elif args.start and args.end:
        time_min = datetime.fromisoformat(args.start).replace(tzinfo=KST)
        time_max = datetime.fromisoformat(args.end).replace(tzinfo=KST)
    else:
        # 기본: 오늘부터 7일
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = time_min + timedelta(days=7)

    params = {
        "calendarId": cal_id,
        "timeMin": time_min.isoformat(),
        "timeMax": time_max.isoformat(),
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": 20,
    }
    if args.query:
        params["q"] = args.query

    try:
        result = service.events().list(**params).execute()
        events = result.get("items", [])

        if not events:
            print("해당 기간에 일정이 없습니다.")
            return

        print(f"📋 일정 {len(events)}건:")
        for ev in events:
            print(format_event_display(ev))
            print()
    except HttpError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


# ── UPDATE ───────────────────────────────────────────────────────────────────

def cmd_update(args):
    service = get_service()
    cal_id = args.calendar or DEFAULT_CALENDAR

    try:
        event = service.events().get(calendarId=cal_id, eventId=args.event_id).execute()
    except HttpError as e:
        print(f"이벤트를 찾을 수 없습니다 (ID: {args.event_id}): {e}", file=sys.stderr)
        sys.exit(1)

    if args.title:
        event["summary"] = args.title
    if args.start:
        event["start"] = {"dateTime": format_datetime(args.start), "timeZone": "Asia/Seoul"}
    if args.end:
        event["end"] = {"dateTime": format_datetime(args.end), "timeZone": "Asia/Seoul"}

    try:
        updated = service.events().update(
            calendarId=cal_id, eventId=args.event_id, body=event
        ).execute()
        print("✅ 일정 수정 완료")
        print(format_event_display(updated))
        print("\n[JSON]")
        print(json.dumps({"id": updated["id"], "link": updated.get("htmlLink", ""), "title": updated["summary"]}, ensure_ascii=False))
    except HttpError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


# ── DELETE ───────────────────────────────────────────────────────────────────

def cmd_delete(args):
    service = get_service()
    cal_id = args.calendar or DEFAULT_CALENDAR

    try:
        event = service.events().get(calendarId=cal_id, eventId=args.event_id).execute()
        print(f"삭제할 일정:\n{format_event_display(event)}")
    except HttpError as e:
        print(f"이벤트를 찾을 수 없습니다: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        service.events().delete(calendarId=cal_id, eventId=args.event_id).execute()
        print(f"\n🗑️ 일정 삭제 완료: {event.get('summary', '')}")
    except HttpError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Google Calendar CRUD")
    sub = parser.add_subparsers(dest="command", required=True)

    # calendars
    sub.add_parser("calendars", help="캘린더 목록 조회")

    # create
    p_create = sub.add_parser("create", help="일정 생성")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--start", required=True, help="ISO 8601 (예: 2025-03-15T14:00:00)")
    p_create.add_argument("--end", help="ISO 8601 (생략 시 시작+1시간)")
    p_create.add_argument("--calendar", help="캘린더 ID (생략 시 기본 캘린더)")

    # list
    p_list = sub.add_parser("list", help="일정 조회")
    p_list.add_argument("--date", help="'today' 또는 날짜 (예: 2025-03-15)")
    p_list.add_argument("--start", help="기간 조회 시작")
    p_list.add_argument("--end", help="기간 조회 종료")
    p_list.add_argument("--query", help="키워드 검색")
    p_list.add_argument("--calendar", help="캘린더 ID (생략 시 기본 캘린더)")

    # update
    p_update = sub.add_parser("update", help="일정 수정")
    p_update.add_argument("--event-id", required=True)
    p_update.add_argument("--title")
    p_update.add_argument("--start")
    p_update.add_argument("--end")
    p_update.add_argument("--calendar", help="캘린더 ID (생략 시 기본 캘린더)")

    # delete
    p_delete = sub.add_parser("delete", help="일정 삭제")
    p_delete.add_argument("--event-id", required=True)
    p_delete.add_argument("--calendar", help="캘린더 ID (생략 시 기본 캘린더)")

    args = parser.parse_args()

    commands = {
        "calendars": cmd_calendars,
        "create": cmd_create,
        "list": cmd_list,
        "update": cmd_update,
        "delete": cmd_delete,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
