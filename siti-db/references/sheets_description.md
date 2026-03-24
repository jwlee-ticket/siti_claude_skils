# 시티 마케팅 Google Sheets 설명

시티 마케팅 데이터는 Google Sheets에서 관리되며 `scripts/gsheets.py`로 조회한다.

## 조회 방법

```bash
# 시트 목록 확인
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py --list

# 시트 전체 조회
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py 초대권리스트
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py 콘텐츠리스트
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py 일정

# 키워드 필터링
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py 초대권리스트 --filter 완료
python3 /Users/jwlee/.claude/skills/siti-db/scripts/gsheets.py 콘텐츠리스트 --filter 2월
```

---

## 시트별 설명

### 초대권리스트 (gid=1320460430)
공연별 시티 초대권 이벤트 수급 및 진행 현황.

| 컬럼명 | 설명 |
|--------|------|
| 순번 | 행 번호 |
| 장르 | 콘서트 / 뮤지컬 / 연극 |
| 제목 | 공연명 |
| 이벤트 시작일 | 초대권 이벤트 신청 시작일 |
| 이벤트 종료일 | 초대권 이벤트 신청 종료일 |
| 당첨자 발표일 | 당첨자 발표 날짜 |
| 관람일 | 실제 공연 관람일 |
| 관람시각 | 공연 시작 시각 |
| 좌석등급 | S / R / VIP / B 등 |
| 당첨인원(1인 2매) | 당첨 인원 수 |
| 티켓 매수 | 총 티켓 수량 (당첨인원 × 2) |
| 제작사 | 공연 제작/주관사 |
| 티켓 수급 상황 | 완료 / 예정 |
| 이벤트 진행 | 완료 / 진행중 / 예정 |

---

### 콘텐츠리스트 (gid=2147291860)
SNS 채널별 콘텐츠 업로드 일정 및 전략.

| 컬럼명 | 설명 |
|--------|------|
| 순번 | 행 번호 |
| 업로드 일자 | 업로드 예정 날짜 (YYYY.MM.DD) |
| 업로드 시각 | 업로드 예정 시각 |
| 전략 구분 | 콘텐츠 목적 (다운로드/회원가입, 티켓 등록, 보관함 활성화 등) |
| 내용 구분 | 브랜딩 / 기능 / 이벤트 |
| 길이 | 이미지 / 영상 / 릴스 등 |
| 내용 | 콘텐츠 제목/설명 |
| 매체 | IG / X / IG+X 등 |
| 캡션 | 게시물 캡션 |

---

### 일정 (gid=0)
2025-2026 시티 전체 마케팅 플랜. 주차별(W-5 ~ W+12) 전략.

| 컬럼명 | 설명 |
|--------|------|
| 주차 | W-5, W-4 ... W+12 형식 |
| KPI | 해당 주차 핵심 성과 지표 |
| 일자 | 해당 날짜 |
| 요일 | 요일 |
| MAIN ISSUE | 주요 이슈/이벤트 |
| MKT ISSUE | 마케팅 이슈 |
| 콘텐츠 (앱/X/인스타그램/블로그 등) | 채널별 콘텐츠 계획 |
| 프로모션/이벤트 | 프로모션 및 이벤트 계획 |
| 퍼포먼스/광고 | APP STORE / X / META 광고 |
| PR | 보도자료, 인플루언서, 핵심 유저 |
| CRM | 유저 관리, 외부 협업 |

---

## 시티 DB와 함께 사용하는 예시

**"3월에 시티 가입자 추이와 그 때 어떤 마케팅을 했는지 같이 보여줘"**
1. siti DB: `SELECT date, COUNT(*) FROM user WHERE created_at >= '2026-03-01' GROUP BY date`
2. 마케팅 시트: `python3 gsheets.py 일정 --filter 3월`
3. 두 결과를 함께 제시

**"초대권 이벤트 공연 중에 시티에서 티켓 등록된 건 얼마나 돼?"**
1. 마케팅 시트: `python3 gsheets.py 초대권리스트` → 공연명 목록 확인
2. siti DB: 해당 공연명으로 ticket 테이블 조회
