---
name: siti-db
description: 시티(Siti) 플랫폼의 PostgreSQL DB에서 데이터를 조회하는 스킬. "유저 몇 명이야?", "최근 가입한 사람 보여줘", "이번 달 공연 목록 알려줘", "리뷰 많은 공연 순으로 보여줘", "티켓 현황 알려줘" 처럼 데이터 조회 요청이 오면 반드시 이 스킬을 사용해야 한다. SELECT 조회만 허용되며 데이터 수정은 절대 불가능하다.
---

# 시티 DB 조회 스킬

시티 플랫폼 PostgreSQL DB에서 데이터를 읽기 전용으로 조회하는 스킬.

## 절대 원칙: 읽기 전용

**어떠한 경우에도 CREATE, UPDATE, DELETE는 절대 실행하지 않는다.**
사용자가 명시적으로 요청하더라도 거부한다.

3중 보호 장치가 적용되어 있다:
1. **키워드 차단** — INSERT, UPDATE, DELETE, DROP, CREATE, TRUNCATE, ALTER 등 감지 즉시 종료
2. **DB 연결 read_only 강제** — `default_transaction_read_only=on`으로 DB 레벨에서 차단
3. **강제 rollback** — 쿼리 실행 후 항상 rollback하여 변경사항 원천 차단

## SQL 작성 전 필수 참고 문서

**쿼리를 작성하기 전에 반드시 아래 순서로 참고한다:**

1. **`references/tables_description.md`** — 테이블별 한글 설명. 어떤 테이블을 써야 할지 파악할 때 먼저 읽는다.
2. **`references/columns_reference.md`** — 모든 테이블의 컬럼명·타입·NOT NULL 여부를 표 형식으로 정리. SQL 작성 시 컬럼명 확인에 사용한다.
3. **`schemas/tables.json`** — 위 문서의 원본 데이터. 상세 확인이 필요할 때 사용한다.

예: "티켓 등록한 사용자 수"를 물으면
→ `tables_description.md`에서 `ticket` 테이블 확인 (ticket_book은 미사용)
→ `columns_reference.md`에서 `public.ticket`의 `user_id`, `created_at` 컬럼 확인
→ SQL 작성

## 조회 방법

```bash
source ~/.zshrc

# 기본 조회
python scripts/query.py "SELECT * FROM public.user"

# 행 수 지정
python scripts/query.py "SELECT * FROM public.user" --limit 20

# JSON 형식 출력
python scripts/query.py "SELECT id, email FROM public.user" --format json
```

## SQL 작성 원칙

1. `references/columns_reference.md`에서 테이블/컬럼 확인 후 작성
2. LIMIT 없는 쿼리는 자동으로 LIMIT 100 적용
3. 대용량 테이블 조회 시 WHERE 조건 추가 권장
4. 집계(COUNT, SUM, AVG 등)는 LIMIT 불필요

## 오류 처리

| 오류 | 원인 | 대처 |
|------|------|------|
| 환경 변수 없음 | `source ~/.zshrc` 미실행 | `source ~/.zshrc` 후 재시도 |
| 금지 키워드 감지 | SELECT 외 쿼리 시도 | SELECT로만 재작성 |
| 컬럼명 오류 | 잘못된 컬럼명 | `schemas/tables.json` 재확인 |
| 접속 타임아웃 | 네트워크 문제 | 재시도 |
