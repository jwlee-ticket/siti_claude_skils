# siti-claude-skills

시티(Siti) 플랫폼 운영에 필요한 데이터 조회, 일정 관리를 자연어로 처리하는 Claude 커스텀 스킬 모음.

---

## Skills

### siti-db
시티 플랫폼 PostgreSQL DB와 마케팅 Google Sheets를 자연어로 조회하는 스킬.

- 자연어 질문 → SQL 자동 생성 → 결과 반환
- 사용자 / 공연·작품 / 티켓 / 커뮤니티 / KOPIS 등 약 60개 테이블 커버
- 초대권 이벤트 현황 / SNS 콘텐츠 일정 / 마케팅 플랜 Google Sheets 연동
- DB 지표와 마케팅 활동을 함께 분석하는 교차 조회 지원
- 3중 읽기 전용 보호 장치 (SELECT만 허용)

### siti-slack-bot
siti-db 스킬을 Slack에서 사용할 수 있도록 연동한 Bot.

- Slack 채널 멘션 또는 DM으로 데이터 조회
- Claude API 기반 Tool Use 에이전트 구조
- GCP VM에서 systemd로 상시 운영

### google-calendar
Google Calendar 일정을 자연어로 관리하는 스킬.

- 일정 생성 / 조회 / 수정 / 삭제 (CRUD)
- "내일 오후 2시에 팀 미팅 잡아줘" 같은 자연어 표현 지원
