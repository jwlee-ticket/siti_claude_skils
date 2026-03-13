# Google Calendar API 설정 가이드

## 1. Google Cloud Console에서 프로젝트 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 선택)
3. **API 및 서비스 > 라이브러리**에서 "Google Calendar API" 검색 후 사용 설정

## 2. OAuth 자격증명 생성

1. **API 및 서비스 > 사용자 인증 정보** 클릭
2. **사용자 인증 정보 만들기 > OAuth 클라이언트 ID** 선택
3. 애플리케이션 유형: **데스크톱 앱** 선택
4. **만들기** → **JSON 다운로드**

## 3. 파일 저장

```bash
mkdir -p ~/.google_calendar_credentials
mv ~/Downloads/client_secret_*.json ~/.google_calendar_credentials/credentials.json
```

## 4. 패키지 설치

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 5. 최초 인증

스크립트 첫 실행 시 브라우저가 열려 Google 계정 로그인 요청.
허용 후 `~/.google_calendar_credentials/token.json` 자동 생성.
이후에는 자동 인증.

## 문제 해결

- **"앱이 확인되지 않음" 경고**: "고급 > 계속" 클릭
- **토큰 만료**: `rm ~/.google_calendar_credentials/token.json` 후 재실행
- **권한 오류**: credentials.json 재발급 필요
