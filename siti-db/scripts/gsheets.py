#!/usr/bin/env python3
"""시티 마케팅 Google Sheets 조회 스크립트 — 읽기 전용"""

import argparse
import csv
import io
import sys
import urllib.request
import urllib.error

SHEET_ID = "1nl--0mHSnNob3lZiQ459cVpPBUYOg-gxT7Tl8QuxokI"

SHEETS = {
    "일정":        {"gid": "0",          "header_row": 4, "desc": "2025-2026 마케팅 플랜 (주차별 일정, KPI, 채널별 전략)"},
    "콘텐츠리스트": {"gid": "2147291860", "header_row": 1, "desc": "SNS 콘텐츠 업로드 일정 (날짜, 채널, 콘텐츠 유형)"},
    "초대권리스트": {"gid": "1320460430", "header_row": 1, "desc": "공연별 초대권 수급 현황 (공연명, 좌석등급, 수급상태)"},
}

# 각 시트의 핵심 컬럼만 표시 (None이면 전체 표시)
DISPLAY_COLUMNS = {
    "초대권리스트": ["순번", "장르", "제목", "이벤트 시작일", "이벤트 종료일", "관람일", "관람시각", "좌석등급", "당첨인원\n(1인 2매)", "티켓 매수", "제작사", "티켓 수급 상황", "이벤트 진행 "],
    "콘텐츠리스트": ["순번", "업로드 일자", "업로드 시각", "전략 구분", "내용 구분", "길이", "내용", "매체", "캡션"],
    "일정": None,
}


def fetch_raw_csv(gid: str) -> list[list[str]]:
    """CSV 원본 데이터를 2D 리스트로 가져오기"""
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"오류: Google Sheets 접근 실패 — {e}", file=sys.stderr)
        sys.exit(1)

    reader = csv.reader(io.StringIO(content))
    return list(reader)


def fetch_sheet(sheet_name: str) -> tuple[list[str], list[list[str]]]:
    """헤더와 데이터 행 반환"""
    if sheet_name not in SHEETS:
        print(f"오류: 알 수 없는 시트명 '{sheet_name}'", file=sys.stderr)
        print(f"사용 가능한 시트: {', '.join(SHEETS.keys())}", file=sys.stderr)
        sys.exit(1)

    info = SHEETS[sheet_name]
    raw = fetch_raw_csv(info["gid"])

    if not raw:
        return [], []

    header_row_idx = info["header_row"]
    headers = raw[header_row_idx]
    data_rows = raw[header_row_idx + 1:]

    # 빈 행 제거 — 인덱스 2(장르/업로드일자 등 첫 실데이터 컬럼) 이후에 값이 있는 행만 유지
    data_rows = [r for r in data_rows if any(v.strip() for v in r[2:] if v.strip())]

    return headers, data_rows


def print_table(headers: list[str], rows: list[list[str]], display_cols: list[str] | None = None, max_col_width: int = 25):
    """테이블 형식으로 출력"""
    if not rows:
        print("결과 없음")
        return

    # 표시할 컬럼 인덱스 결정
    if display_cols:
        col_indices = []
        col_names = []
        for col in display_cols:
            if col in headers:
                col_indices.append(headers.index(col))
                col_names.append(col)
    else:
        # 전체 컬럼 중 비어있지 않은 것만
        col_indices = [i for i in range(len(headers)) if headers[i].strip()]
        col_names = [headers[i] for i in col_indices]

    if not col_indices:
        print("표시할 컬럼 없음")
        return

    # 각 컬럼 너비 계산
    col_widths = []
    for idx, name in zip(col_indices, col_names):
        max_data_len = max((len(str(r[idx]).strip()) if idx < len(r) else 0) for r in rows)
        col_widths.append(min(max_col_width, max(len(name.replace('\n', ' ')), max_data_len)))

    # 헤더 출력
    header_line = " | ".join(name.replace('\n', ' ').ljust(w) for name, w in zip(col_names, col_widths))
    sep_line = "-+-".join("-" * w for w in col_widths)
    print(header_line)
    print(sep_line)

    for row in rows:
        cells = []
        for idx, w in zip(col_indices, col_widths):
            val = str(row[idx]).strip() if idx < len(row) else ""
            cells.append(val.ljust(w)[:w])
        print(" | ".join(cells))

    print(f"\n{len(rows)}행")


def print_list():
    """사용 가능한 시트 목록 출력"""
    print("사용 가능한 마케팅 시트:")
    print()
    for name, info in SHEETS.items():
        print(f"  {name:12} — {info['desc']}")


def main():
    parser = argparse.ArgumentParser(description="시티 마케팅 Google Sheets 조회")
    parser.add_argument("sheet", nargs="?", help="시트명 (일정 / 콘텐츠리스트 / 초대권리스트)")
    parser.add_argument("--list", action="store_true", help="사용 가능한 시트 목록 보기")
    parser.add_argument("--filter", help="특정 키워드로 행 필터링 (예: --filter 3월)")
    args = parser.parse_args()

    if args.list or not args.sheet:
        print_list()
        return

    headers, rows = fetch_sheet(args.sheet)

    if args.filter:
        keyword = args.filter.lower()
        rows = [r for r in rows if any(keyword in str(v).lower() for v in r)]
        if not rows:
            print(f"'{args.filter}' 검색 결과 없음")
            return

    display_cols = DISPLAY_COLUMNS.get(args.sheet)
    print_table(headers, rows, display_cols)


if __name__ == "__main__":
    main()
