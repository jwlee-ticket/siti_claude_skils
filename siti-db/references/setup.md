# 시티 DB 접속 설정

## 환경 변수 설정

`~/.zshrc`에 아래 항목이 추가되어 있어야 합니다:

```bash
export SITI_DB_HOST="ts-db-prod.cluster-c7oy62uqaei0.ap-northeast-2.rds.amazonaws.com"
export SITI_DB_PORT="5432"
export SITI_DB_USER="postgres"
export SITI_DB_PASSWORD="..."
export SITI_DB_NAME="ts"
```

설정 후 반드시 `source ~/.zshrc` 실행.

## 패키지 설치

```bash
pip3 install psycopg2-binary
```
